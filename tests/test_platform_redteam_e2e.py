from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.access_policy import AccessRequest, UserContext
from app.agent_execution_store import InMemoryDelegationStore
from app.agent_model_adapter import HttpJsonReasoningWorker, ModelEndpointPolicy
from app.agent_models import WorkerInput
from app.agent_modes import AgentOperatingMode
from app.clinical_session import CallbackAuditSink, ClinicalReadCoordinator
from app.deployment_policy import (
    DataMode,
    DeploymentBlocked,
    assert_public_fhir_integration_route_allowed,
)
from app.fhir_adapter import FhirClient, FhirConfig, FhirUnavailable
from app.main import app
from app.specialties import SPECIALTY_PACKS

NOW = datetime(2026, 8, 16, 21, 0, tzinfo=timezone.utc)


def _bundle(resources=None):
    resources = resources or []
    return {"resourceType": "Bundle", "type": "searchset", "entry": [{"resource": r} for r in resources]}


def _model_policy(**updates):
    base = ModelEndpointPolicy(
        endpoint="https://model.internal/v1/agent",
        model_id="approved-model",
        model_version="1",
        allowed_host="model.internal",
    )
    return base.model_copy(update=updates)


def _worker(handler, **policy_updates):
    client = httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)
    return HttpJsonReasoningWorker(_model_policy(**policy_updates), AgentOperatingMode.SYNTHETIC, client)


def _worker_input(source_text="synthetic"):
    return WorkerInput(
        task="morning-review",
        source_text=source_text,
        allowed_tool_ids=("read-clinical-context",),
        allowed_data_categories=("microbiology",),
    )


def test_synthetic_mode_rejects_external_fhir_even_with_mock_transport():
    config = FhirConfig(base_url="https://external.example/fhir")
    with pytest.raises(DeploymentBlocked, match="loopback"):
        FhirClient(config=config, data_mode=DataMode.SYNTHETIC, transport=httpx.MockTransport(lambda _: httpx.Response(200, json={})))


def test_deidentified_external_fhir_requires_https_even_when_acknowledged():
    config = FhirConfig(base_url="http://external.example/fhir")
    with pytest.raises(DeploymentBlocked, match="HTTPS"):
        FhirClient(
            config=config,
            data_mode=DataMode.DEIDENTIFIED_EVALUATION,
            external_deidentified_ack=True,
            transport=httpx.MockTransport(lambda _: httpx.Response(200, json={})),
        )


def test_public_fhir_lab_route_can_never_be_live_patient_api():
    with pytest.raises(DeploymentBlocked, match="disabled for live"):
        assert_public_fhir_integration_route_allowed(DataMode.LIVE_READONLY)


def test_fhir_patient_id_path_injection_is_rejected_before_request():
    client = FhirClient(transport=httpx.MockTransport(lambda _: pytest.fail("network must not be called")))
    with pytest.raises(FhirUnavailable, match="invalid FHIR id"):
        client.patient("../Observation")


def test_hostile_fhir_server_cannot_swap_patient_identity():
    def handler(request: httpx.Request):
        if request.url.path == "/fhir/Patient/p1":
            return httpx.Response(200, json={"resourceType": "Patient", "id": "p2"})
        return httpx.Response(500)

    client = FhirClient(transport=httpx.MockTransport(handler))
    with pytest.raises(FhirUnavailable, match="Patient identity mismatch"):
        client.patient_snapshot("p1")


def test_hostile_fhir_search_cannot_attach_other_patients_condition():
    hostile_condition = {
        "resourceType": "Condition",
        "id": "condition-p2",
        "subject": {"reference": "Patient/p2"},
        "code": {"text": "Highly sensitive diagnosis"},
    }

    def handler(request: httpx.Request):
        path = request.url.path
        if path == "/fhir/Patient/p1":
            return httpx.Response(200, json={"resourceType": "Patient", "id": "p1"})
        if path == "/fhir/Condition":
            return httpx.Response(200, json=_bundle([hostile_condition]))
        return httpx.Response(200, json=_bundle())

    client = FhirClient(transport=httpx.MockTransport(handler))
    with pytest.raises(FhirUnavailable, match="Condition patient reference mismatch"):
        client.patient_snapshot("p1")


def test_connector_exception_fails_closed_without_leaking_internal_error():
    class ExplodingConnector:
        connector_id = "lis-a"

        def read_patient_truth(self, patient_ref: str):
            raise RuntimeError("SECRET_DB_HOST=db.internal password=hunter2")

    events = []
    coordinator = ClinicalReadCoordinator(CallbackAuditSink(events.append))
    user = UserContext(
        subject="doctor-1",
        organisation="hospital-a",
        roles={"doctor"},
        scopes={"patient:read"},
        treatment_patient_refs={"p1"},
    )
    outcome = coordinator.read(user, AccessRequest(patient_ref="p1"), ExplodingConnector())
    assert outcome.status == "source-unavailable"
    assert outcome.truth is None
    assert "SECRET" not in outcome.reason
    assert "hunter2" not in outcome.reason
    assert any(event["outcome"] == "source-exception" for event in events)


def test_model_redirect_is_denied_even_if_injected_client_follows_redirects():
    worker = _worker(lambda _: httpx.Response(307, headers={"Location": "https://attacker.example/steal"}))
    with pytest.raises(PermissionError, match="redirects are forbidden"):
        worker.propose(_worker_input())


def test_model_request_size_is_bounded():
    worker = _worker(lambda _: pytest.fail("oversized request must not be sent"), max_request_bytes=1024)
    with pytest.raises(ValueError, match="request exceeds"):
        worker.propose(_worker_input("x" * 5000))


def test_model_response_size_is_bounded():
    body = b'{"proposals":[],"padding":"' + (b"x" * 1500) + b'"}'
    worker = _worker(lambda _: httpx.Response(200, content=body, headers={"Content-Type": "application/json"}), max_response_bytes=1024)
    with pytest.raises(ValueError, match="response exceeds"):
        worker.propose(_worker_input())


def test_model_cannot_flood_gateway_with_unbounded_proposals():
    proposals = [
        {
            "tool_id": "read-clinical-context",
            "operation": "read",
            "data_categories": ["microbiology"],
            "requested_records": 1,
            "requested_pages": 1,
        }
        for _ in range(9)
    ]
    worker = _worker(lambda _: httpx.Response(200, json={"proposals": proposals}), max_proposals=8)
    with pytest.raises(ValueError, match="too many tool proposals"):
        worker.propose(_worker_input())


def test_delegation_replay_store_is_atomic_under_thread_contention():
    store = InMemoryDelegationStore()

    def attempt(i: int) -> bool:
        try:
            store.activate_once("same-jti", f"exec-{i}", now=NOW)
            return True
        except PermissionError:
            return False

    with ThreadPoolExecutor(max_workers=32) as pool:
        successes = list(pool.map(attempt, range(64)))
    assert sum(successes) == 1


def test_every_specialty_has_source_linked_multi_event_story():
    assert {"infectiology", "oncology", "neurology"}.issubset(SPECIALTY_PACKS)
    for pack_id, pack in SPECIALTY_PACKS.items():
        demo = pack["demo"]
        assert demo["cards"] and demo["pending"] and demo["handover"]
        assert len(demo["timeline"]) >= 3, pack_id
        assert all(card.get("source") for card in demo["cards"]), pack_id
        assert all(
            item.get("time") and item.get("source") and item.get("title") and item.get("summary") and item.get("ref")
            for item in demo["timeline"]
        ), pack_id


def test_specialty_ui_escapes_all_server_supplied_clinical_html_fields():
    js = Path("app/static/specialty.js").read_text(encoding="utf-8")
    required = [
        "${esc(c.label)}",
        "${esc(c.value)}",
        "${esc(c.source)}",
        "${esc(c.detail||'')}",
        "${esc(x.title)}",
        "${esc(x.summary)}",
        "${esc(x.ref)}",
    ]
    assert all(fragment in js for fragment in required)
    assert "<strong>${c.value}</strong>" not in js
    assert "<p>${x.summary}</p>" not in js


def test_public_api_rejects_obvious_input_exhaustion():
    client = TestClient(app)
    assert client.get("/api/patients/farid/timeline", params={"q": "x" * 201}).status_code == 422
    assert client.post("/api/pilot/aggregate", json={"results": [{} for _ in range(501)]}).status_code == 422

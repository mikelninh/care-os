import json
import httpx

from app.fhir_adapter import FhirClient, snapshot_to_timeline
from app.guidelines import list_sources, select_guidance
from app.security_readiness import readiness
from app.audit import make_audit_event, validate_event
from benchmark.redteam_unseen import run_unseen


def _bundle(resources):
    return {"resourceType":"Bundle","type":"searchset","entry":[{"resource":r} for r in resources]}


def test_fhir_adapter_reads_real_r4_shape_and_preserves_source_ids():
    patient={"resourceType":"Patient","id":"p1","name":[{"given":["Farid"],"family":"Rahman"}],"birthDate":"1979-11-02"}
    allergy={"resourceType":"AllergyIntolerance","id":"a1","patient":{"reference":"Patient/p1"},"code":{"text":"Penicillin"},"recordedDate":"2023-03-10"}
    responses={"/Patient/p1":patient,"/AllergyIntolerance":_bundle([allergy]),"/Condition":_bundle([]),"/Observation":_bundle([]),"/MedicationStatement":_bundle([]),"/Task":_bundle([]),"/DocumentReference":_bundle([])}
    def handler(request): return httpx.Response(200, json=responses[request.url.path.removeprefix("/fhir")])
    timeline=snapshot_to_timeline(FhirClient(transport=httpx.MockTransport(handler)).patient_snapshot("p1"))
    assert timeline["patient"]["name"] == "Farid Rahman"
    assert timeline["items"][0]["resource_id"] == "a1"
    assert timeline["items"][0]["resource_type"] == "AllergyIntolerance"


def test_security_readiness_default_demo_cannot_claim_production_ready():
    r=readiness({}); assert r["ready"] is False and r["blockers"] >= 4


def test_security_readiness_cloud_requires_c5_and_tls():
    env={"DEPLOYMENT_MODE":"cloud","AUTH_MODE":"oidc","OIDC_ISSUER":"https://id.example","OIDC_AUDIENCE":"careos","ALLOW_PHI_IN_LOGS":"false","AUDIT_SINK":"siem","DATA_REGION":"EU","CLINICAL_WRITEBACK":"disabled","FHIR_BASE_URL":"http://fhir"}
    r=readiness(env); ids={c["id"] for c in r["checks"] if c["required"] and not c["ok"]}; assert "c5_evidence" in ids and "fhir_tls" in ids


def test_audit_event_has_no_clinical_free_text():
    e=make_audit_event(actor_id="doctor-1", patient_id="patient-1", action="read", resource_type="Observation", resource_id="o1")
    validate_event(e); assert "patient-1" not in json.dumps(e); assert not ({"note","text","summary"} & set(e))


def test_guideline_registry_is_versioned_source_context_not_treatment_advice():
    assert any(s["publisher"] == "KDIGO" for s in list_sources())
    selected=select_guidance("chronic kidney disease", "DE")
    assert any("not" in p.lower() or "never" in p.lower() for p in selected["policy"])


def test_unseen_redteam_stays_hard_and_visible():
    r=run_unseen(60, seed=772331)
    assert r["dataset"]["unseen_holdout"] is True
    assert r["all_fields_exact"] < 0.5
    assert r["critical_silent_contradiction_misses"] > 0

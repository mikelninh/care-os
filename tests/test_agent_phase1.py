from datetime import datetime, timedelta, timezone

import pytest

from app.agent_execution_store import InMemoryDelegationStore, DelegationState
from app.agent_identity import RevocationSet, WorkloadIdentity
from app.agent_policy import AgentDelegation, AgentOperation, AgentRequest
from app.agent_runtime import AgentGateway
from app.agent_tool_proxy import AgentToolProxy
from app.agent_tools import synthetic_sjk_registry

NOW = datetime(2026, 8, 16, 20, 40, tzinfo=timezone.utc)


def _delegation():
    return AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-1",
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context"},
        allowed_operations={AgentOperation.READ},
        allowed_data_categories={"microbiology"},
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
        max_tool_calls=2,
        max_records=20,
        max_pages=2,
        max_runtime_seconds=60,
    )


def _request():
    return AgentRequest(
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        tool_id="read-clinical-context",
        operation=AgentOperation.READ,
        data_categories={"microbiology"},
        requested_records=1,
        requested_pages=1,
    )


def test_delegation_can_activate_only_once_then_consume():
    store = InMemoryDelegationStore()
    record = store.activate_once("jti-1", "exec-1", now=NOW)
    assert record.state == DelegationState.ACTIVE
    with pytest.raises(PermissionError):
        store.activate_once("jti-1", "exec-2", now=NOW)
    assert store.consume("jti-1", "exec-1", now=NOW).state == DelegationState.CONSUMED


def test_revoked_delegation_cannot_activate():
    store = InMemoryDelegationStore()
    store.revoke("jti-revoked", now=NOW)
    with pytest.raises(PermissionError):
        store.activate_once("jti-revoked", "exec", now=NOW)


def test_workload_identity_is_bound_to_agent_org_version_and_audience():
    identity = WorkloadIdentity(
        subject="workload-123",
        organisation="sjk",
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        audience="careos-agent-gateway",
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
        credential_id="cred-1",
    )
    identity.validate_for(organisation="sjk", agent_id="careos-rounds-agent", agent_version="1.0.0", audience="careos-agent-gateway", now=NOW)
    with pytest.raises(PermissionError):
        identity.validate_for(organisation="other", agent_id="careos-rounds-agent", agent_version="1.0.0", audience="careos-agent-gateway", now=NOW)
    revoked = RevocationSet(); revoked.revoke("cred-1")
    with pytest.raises(PermissionError):
        revoked.assert_active(identity)


def test_tool_proxy_has_no_bypass_for_unregistered_or_cross_patient_request():
    gateway = AgentGateway(delegation=_delegation(), registry=synthetic_sjk_registry())
    proxy = AgentToolProxy(gateway, {"read-clinical-context": lambda req: {"ok": True}})
    assert proxy.call(_request(), now=NOW).payload == {"ok": True}
    bad = _request().model_copy(update={"patient_ref": "patient-2"})
    with pytest.raises(PermissionError):
        proxy.call(bad, now=NOW)

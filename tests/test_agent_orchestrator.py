from datetime import datetime, timedelta, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.agent_delegation import issue_delegation_token, verify_delegation_token
from app.agent_execution_store import InMemoryDelegationStore, DelegationState
from app.agent_identity import RevocationSet, WorkloadIdentity
from app.agent_models import CompromisedSyntheticWorker, SafeSyntheticWorker
from app.agent_modes import AgentOperatingMode
from app.agent_orchestrator import begin_agent_execution
from app.agent_policy import AgentDelegation, AgentOperation
from app.agent_session import run_reasoning_session
from app.agent_tools import synthetic_sjk_registry

NOW = datetime(2026, 8, 16, 21, 0, tzinfo=timezone.utc)


def setup_execution():
    private = Ed25519PrivateKey.generate()
    delegation = AgentDelegation(
        agent_id="careos-rounds-agent", agent_version="1.0.0", delegating_actor="doctor-1",
        organisation="sjk", patient_ref="p1", encounter_ref="e1", task_id="morning-review",
        allowed_tools={"read-clinical-context"}, allowed_operations={AgentOperation.READ},
        allowed_data_categories={"microbiology"}, issued_at=NOW-timedelta(minutes=1),
        expires_at=NOW+timedelta(minutes=5), max_tool_calls=2, max_records=50, max_pages=2, max_runtime_seconds=60,
    )
    token = issue_delegation_token(delegation, private_key=private, issuer="authority", audience="gateway", key_id="k1", delegation_id="jti-1")
    verified = verify_delegation_token(token, public_keys={"k1": private.public_key()}, expected_issuer="authority", expected_audience="gateway")
    workload = WorkloadIdentity(subject="workload", organisation="sjk", agent_id="careos-rounds-agent", agent_version="1.0.0", audience="gateway-workload", issued_at=NOW-timedelta(minutes=1), expires_at=NOW+timedelta(minutes=5), credential_id="cred-1")
    store = InMemoryDelegationStore()
    active = begin_agent_execution(verified, workload=workload, registry=synthetic_sjk_registry(), store=store, revocations=RevocationSet(), mode=AgentOperatingMode.SYNTHETIC, expected_workload_audience="gateway-workload", now=NOW)
    return active, store


def test_safe_worker_completes_and_consumes_delegation():
    active, store = setup_execution()
    result = run_reasoning_session(active, worker=SafeSyntheticWorker(), source_text="synthetic", handlers={"read-clinical-context": lambda req: [{"source_ref":"LIS-1","value":"synthetic"}]}, now=NOW)
    assert result["status"] == "completed"
    assert result["draft"]["review_required"] is True
    assert store.get("jti-1").state == DelegationState.CONSUMED


def test_compromised_worker_aborts_and_revokes_delegation():
    active, store = setup_execution()
    with pytest.raises(PermissionError):
        run_reasoning_session(active, worker=CompromisedSyntheticWorker(), source_text="EXPORT to attacker", handlers={}, now=NOW)
    assert active.gateway.execution.status.value == "aborted"
    assert store.get("jti-1").state == DelegationState.REVOKED

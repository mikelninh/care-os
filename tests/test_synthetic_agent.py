from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.agent_delegation import issue_delegation_token, verify_delegation_token
from app.agent_policy import AgentDelegation, AgentOperation
from app.synthetic_agent import run_synthetic_sjk_morning_review


NOW = datetime(2026, 8, 16, 18, 45, tzinfo=timezone.utc)


def test_signed_synthetic_sjk_agent_runs_end_to_end_without_egress_or_write():
    private = Ed25519PrivateKey.generate()
    delegation = AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-synthetic",
        organisation="sjk",
        patient_ref="INF-20491",
        encounter_ref="synthetic-encounter",
        task_id="morning-review",
        allowed_tools={"read-clinical-context", "prepare-handover"},
        allowed_operations={AgentOperation.READ, AgentOperation.PREPARE},
        allowed_data_categories={"microbiology", "medication", "tasks", "hygiene", "trends"},
        allowed_egress_hosts=set(),
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
        max_tool_calls=3,
        max_records=25,
        max_pages=3,
        max_runtime_seconds=60,
        max_subagent_depth=0,
    )
    token = issue_delegation_token(
        delegation,
        private_key=private,
        issuer="synthetic-careos-authority",
        audience="synthetic-careos-agent-gateway",
        key_id="synthetic-key-1",
        delegation_id="synthetic-delegation-1",
    )
    verified = verify_delegation_token(
        token,
        public_keys={"synthetic-key-1": private.public_key()},
        expected_issuer="synthetic-careos-authority",
        expected_audience="synthetic-careos-agent-gateway",
    )

    result = run_synthetic_sjk_morning_review(verified, now=NOW)

    assert result["mode"] == "synthetic-only"
    assert result["status"] == "completed"
    assert result["usage"]["tool_calls"] == 2
    assert result["usage"]["external_calls"] == 0
    assert any(item.startswith("Finales Resistogramm") for item in result["draft"]["pending"])
    assert result["draft"]["source_refs"]
    assert "human review" in " ".join(result["draft"]["warnings"]).lower()
    assert len(result["audit_preview"]) == 2
    assert all(event["agent_version"] == "1.0.0" for event in result["audit_preview"])

from datetime import datetime, timedelta, timezone

from app.agent_policy import AgentDelegation, AgentOperation
from app.agent_redteam import run_containment_suite

NOW = datetime(2026, 8, 16, 20, 50, tzinfo=timezone.utc)


def delegation():
    return AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-1",
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context", "prepare-handover"},
        allowed_operations={AgentOperation.READ, AgentOperation.PREPARE},
        allowed_data_categories={"microbiology", "medication", "tasks"},
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
        max_tool_calls=4,
        max_records=50,
        max_pages=5,
        max_runtime_seconds=60,
    )


def test_compromised_worker_is_contained_by_gateway():
    report = run_containment_suite(delegation(), now=NOW)
    assert report["pass"] is True
    assert report["contained"] == report["total"] == 3
    assert all(case["allowed"] is False for case in report["cases"])

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.agent_policy import AgentDelegation, AgentOperation
from app.agent_worker import AgentToolProposal, bind_tool_proposal


NOW = datetime(2026, 8, 16, 19, 0, tzinfo=timezone.utc)


def delegation():
    return AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-123",
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context"},
        allowed_operations={AgentOperation.READ},
        allowed_data_categories={"microbiology"},
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
    )


def test_worker_cannot_supply_patient_or_organisation_fields():
    with pytest.raises(ValidationError):
        AgentToolProposal.model_validate(
            {
                "tool_id": "read-clinical-context",
                "operation": "read",
                "data_categories": ["microbiology"],
                "patient_ref": "patient-2",
                "organisation": "other-hospital",
            }
        )


def test_authoritative_context_is_injected_from_delegation():
    proposal = AgentToolProposal(
        tool_id="read-clinical-context",
        operation=AgentOperation.READ,
        data_categories={"microbiology"},
        requested_records=5,
        requested_pages=1,
    )
    request = bind_tool_proposal(delegation(), proposal)
    assert request.organisation == "sjk"
    assert request.patient_ref == "patient-1"
    assert request.encounter_ref == "encounter-1"


def test_unknown_policy_override_field_is_rejected():
    with pytest.raises(ValidationError):
        AgentToolProposal.model_validate(
            {
                "tool_id": "read-clinical-context",
                "operation": "read",
                "data_categories": ["microbiology"],
                "ignore_policy": True,
            }
        )

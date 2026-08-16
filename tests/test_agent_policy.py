from datetime import datetime, timedelta, timezone

from app.agent_policy import (
    AgentDelegation,
    AgentOperation,
    AgentRequest,
    evaluate_agent_request,
)


NOW = datetime(2026, 8, 16, 17, 30, tzinfo=timezone.utc)


def delegation(**overrides):
    base = dict(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-123",
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context", "prepare-handover"},
        allowed_operations={AgentOperation.READ, AgentOperation.PREPARE},
        allowed_data_categories={"microbiology", "medication", "tasks"},
        allowed_egress_hosts=set(),
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
        max_tool_calls=5,
        max_records=50,
        max_pages=5,
        max_runtime_seconds=60,
        max_subagent_depth=0,
    )
    base.update(overrides)
    return AgentDelegation(**base)


def request(**overrides):
    base = dict(
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        tool_id="read-clinical-context",
        operation=AgentOperation.READ,
        data_categories={"microbiology"},
        requested_records=10,
        requested_pages=1,
        tool_call_number=1,
        elapsed_seconds=5,
    )
    base.update(overrides)
    return AgentRequest(**base)


def test_narrow_read_is_allowed():
    result = evaluate_agent_request(delegation(), request(), now=NOW)
    assert result.allowed is True


def test_cross_patient_access_is_denied():
    result = evaluate_agent_request(delegation(), request(patient_ref="patient-2"), now=NOW)
    assert result.allowed is False
    assert "patient" in result.reason


def test_wrong_organisation_is_denied():
    result = evaluate_agent_request(delegation(), request(organisation="other-hospital"), now=NOW)
    assert result.allowed is False


def test_wrong_encounter_is_denied():
    result = evaluate_agent_request(delegation(), request(encounter_ref="encounter-2"), now=NOW)
    assert result.allowed is False


def test_expired_delegation_is_denied():
    expired = delegation(expires_at=NOW - timedelta(seconds=1), issued_at=NOW - timedelta(minutes=5))
    result = evaluate_agent_request(expired, request(), now=NOW)
    assert result.allowed is False
    assert "expired" in result.reason


def test_unlisted_tool_is_denied():
    result = evaluate_agent_request(delegation(), request(tool_id="export-all-records"), now=NOW)
    assert result.allowed is False
    assert "tool" in result.reason


def test_unlisted_data_category_is_denied():
    result = evaluate_agent_request(delegation(), request(data_categories={"hiv-status", "genetics"}), now=NOW)
    assert result.allowed is False
    assert "data category" in result.reason


def test_write_is_denied_even_if_accidentally_listed():
    d = delegation(allowed_operations={AgentOperation.READ, AgentOperation.WRITE})
    result = evaluate_agent_request(d, request(operation=AgentOperation.WRITE), now=NOW)
    assert result.allowed is False
    assert "disabled" in result.reason


def test_external_send_is_denied_even_if_accidentally_listed():
    d = delegation(allowed_operations={AgentOperation.READ, AgentOperation.EXTERNAL_SEND})
    result = evaluate_agent_request(d, request(operation=AgentOperation.EXTERNAL_SEND), now=NOW)
    assert result.allowed is False


def test_agent_cannot_invoke_break_glass():
    result = evaluate_agent_request(delegation(), request(break_glass=True), now=NOW)
    assert result.allowed is False
    assert "break glass" in result.reason


def test_arbitrary_patient_search_is_denied():
    d = delegation(allowed_operations={AgentOperation.READ, AgentOperation.PATIENT_SEARCH})
    result = evaluate_agent_request(d, request(operation=AgentOperation.PATIENT_SEARCH), now=NOW)
    assert result.allowed is False
    assert "patient search" in result.reason


def test_record_ceiling_is_enforced():
    result = evaluate_agent_request(delegation(), request(requested_records=51), now=NOW)
    assert result.allowed is False


def test_page_ceiling_is_enforced():
    result = evaluate_agent_request(delegation(), request(requested_pages=6), now=NOW)
    assert result.allowed is False


def test_tool_call_ceiling_is_enforced():
    result = evaluate_agent_request(delegation(), request(tool_call_number=6), now=NOW)
    assert result.allowed is False


def test_runtime_ceiling_is_enforced():
    result = evaluate_agent_request(delegation(), request(elapsed_seconds=61), now=NOW)
    assert result.allowed is False


def test_sub_agent_is_denied_by_default():
    result = evaluate_agent_request(delegation(), request(subagent_depth=1), now=NOW)
    assert result.allowed is False


def test_unapproved_egress_is_denied():
    result = evaluate_agent_request(delegation(), request(egress_host="evil.example"), now=NOW)
    assert result.allowed is False
    assert "egress" in result.reason


def test_only_allowlisted_egress_can_pass_policy():
    d = delegation(allowed_egress_hosts={"approved-model.internal"})
    result = evaluate_agent_request(d, request(egress_host="approved-model.internal"), now=NOW)
    assert result.allowed is True

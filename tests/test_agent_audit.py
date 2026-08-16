from app.agent_audit import make_agent_audit_event
from app.agent_readiness import agent_gate_manifest


def test_agent_audit_has_dual_attribution_without_raw_phi():
    event = make_agent_audit_event(
        execution_id="exec-1",
        delegation_id="delegation-1",
        human_actor_id="doctor-123",
        agent_id="rounds-agent",
        agent_version="1.0.0",
        organisation="sjk",
        patient_id="patient-4711",
        encounter_id="encounter-1",
        task_id="morning-review",
        event_type="tool_authorization",
        decision="deny",
        reason_code="patient_outside_delegation",
        tool_id="read-clinical-context",
        tool_version="1.0.0",
        operation="read",
        data_categories={"microbiology"},
        pseudonym_key="audit-test-key",
    )
    assert event["human_actor_ref"] != "doctor-123"
    assert event["agent_ref"] != "rounds-agent"
    assert event["patient_ref"] != "patient-4711"
    assert event["decision"] == "deny"
    assert event["reason_code"] == "patient_outside_delegation"
    serialized = str(event)
    assert "patient-4711" not in serialized
    assert "doctor-123" not in serialized


def test_agent_readiness_never_inherits_normal_careos_readiness():
    manifest = agent_gate_manifest()
    assert manifest["agent_live_identifiable_phi_allowed"] is False
    assert manifest["autonomous_consequential_actions_allowed"] is False
    assert manifest["all_agent_gates_pass"] is False
    assert {gate["id"] for gate in manifest["gates"]} == {f"A{i}" for i in range(10)}
    assert all(gate["status"] != "PASS" for gate in manifest["gates"])

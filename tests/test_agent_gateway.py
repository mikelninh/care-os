from datetime import datetime, timedelta, timezone

from app.agent_policy import AgentDelegation, AgentOperation, AgentRequest
from app.agent_runtime import AgentExecutionState, AgentGateway, ExecutionStatus
from app.agent_tools import ToolRegistry, ToolSpec, ToolTrustTier, synthetic_sjk_registry


NOW = datetime(2026, 8, 16, 18, 0, tzinfo=timezone.utc)


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
        expires_at=NOW + timedelta(minutes=10),
        max_tool_calls=3,
        max_records=10,
        max_pages=3,
        max_runtime_seconds=120,
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
        requested_records=4,
        requested_pages=1,
        tool_call_number=999,  # gateway must ignore model-provided accounting
        elapsed_seconds=999,
    )
    base.update(overrides)
    return AgentRequest(**base)


def gateway(**kwargs):
    state = kwargs.pop("execution", AgentExecutionState(started_at=NOW - timedelta(seconds=5)))
    return AgentGateway(
        delegation=kwargs.pop("delegation", delegation()),
        registry=kwargs.pop("registry", synthetic_sjk_registry()),
        execution=state,
        memory_secret="test-secret",
        **kwargs,
    )


def test_valid_read_is_admitted():
    g = gateway()
    decision = g.authorize(request(), now=NOW)
    assert decision.allowed is True
    assert decision.tool is not None
    assert decision.tool.tool_id == "read-clinical-context"
    assert g.execution.status == ExecutionStatus.ACTIVE


def test_runtime_owns_tool_call_counter():
    d = delegation(max_tool_calls=1)
    g = gateway(delegation=d)
    first = request(tool_call_number=99)
    assert g.authorize(first, now=NOW).allowed is True
    g.record_tool_result(first)
    second = request(tool_call_number=1)
    denied = g.authorize(second, now=NOW + timedelta(seconds=1))
    assert denied.allowed is False
    assert "tool-call" in denied.reason


def test_aggregate_record_budget_cannot_be_split_across_calls():
    g = gateway()
    first = request(requested_records=6)
    assert g.authorize(first, now=NOW).allowed is True
    g.record_tool_result(first)
    second = request(requested_records=6)
    decision = g.authorize(second, now=NOW + timedelta(seconds=1))
    assert decision.allowed is False
    assert "budget" in decision.reason


def test_denial_is_terminal_for_execution():
    g = gateway()
    bad = request(patient_ref="patient-2")
    assert g.authorize(bad, now=NOW).allowed is False
    assert g.execution.status == ExecutionStatus.DENIED
    later = g.authorize(request(), now=NOW + timedelta(seconds=1))
    assert later.allowed is False
    assert "execution is denied" in later.reason


def test_unregistered_tool_is_denied():
    d = delegation(allowed_tools={"evil-tool"})
    g = gateway(delegation=d)
    decision = g.authorize(request(tool_id="evil-tool"), now=NOW)
    assert decision.allowed is False
    assert "registered" in decision.reason


def test_registered_tool_effect_mismatch_is_denied():
    d = delegation(allowed_operations={AgentOperation.READ, AgentOperation.PREPARE})
    g = gateway(delegation=d)
    decision = g.authorize(
        request(tool_id="read-clinical-context", operation=AgentOperation.PREPARE), now=NOW
    )
    assert decision.allowed is False
    assert "effect" in decision.reason


def test_tool_contract_caps_data_categories():
    d = delegation(allowed_data_categories={"microbiology", "medication", "genetics"})
    g = gateway(delegation=d)
    decision = g.authorize(request(data_categories={"genetics"}), now=NOW)
    assert decision.allowed is False
    assert "tool contract" in decision.reason


def test_memory_namespace_is_execution_and_patient_scoped():
    g1 = gateway()
    g2 = gateway()
    assert g1.memory_namespace != g2.memory_namespace

    other = gateway(delegation=delegation(patient_ref="patient-2"))
    assert other.memory_namespace != g1.memory_namespace
    assert "patient-1" not in g1.memory_namespace


def test_expiry_is_terminal_and_preserved():
    d = delegation(expires_at=NOW - timedelta(seconds=1), issued_at=NOW - timedelta(minutes=2))
    g = gateway(delegation=d)
    decision = g.authorize(request(), now=NOW)
    assert decision.allowed is False
    assert g.execution.status == ExecutionStatus.EXPIRED


def test_external_tool_requires_both_delegation_and_tool_allowlist():
    tool = ToolSpec(
        tool_id="approved-model",
        version="1.0.0",
        owner="hospital",
        trust_tier=ToolTrustTier.PROVIDER_MANAGED,
        operation=AgentOperation.READ,
        target_system="private-model-endpoint",
        data_categories={"microbiology"},
        allowed_egress_hosts={"model.internal"},
    )
    registry = ToolRegistry([tool])
    d = delegation(
        allowed_tools={"approved-model"},
        allowed_egress_hosts={"model.internal"},
        allowed_operations={AgentOperation.READ},
        allowed_data_categories={"microbiology"},
    )
    g = gateway(delegation=d, registry=registry)
    ok = g.authorize(
        request(tool_id="approved-model", egress_host="model.internal"), now=NOW
    )
    assert ok.allowed is True

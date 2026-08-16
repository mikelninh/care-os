from __future__ import annotations

from datetime import datetime, timezone

from .agent_audit import make_agent_audit_event
from .agent_delegation import VerifiedDelegation
from .agent_policy import AgentOperation, AgentRequest
from .agent_runtime import AgentExecutionState, AgentGateway
from .agent_tools import synthetic_sjk_registry
from .specialties import SPECIALTY_PACKS


class SyntheticAgentError(RuntimeError):
    pass


def run_synthetic_sjk_morning_review(
    verified: VerifiedDelegation,
    *,
    now: datetime | None = None,
    pseudonym_key: str | bytes = "synthetic-agent-audit-key",
) -> dict:
    """Run the first safe CareOS agent use case end to end on synthetic data.

    There is intentionally no model here. Stage 0 proves that the gateway, delegation,
    tool contracts, budgets, memory namespace and audit attribution work before a
    probabilistic reasoning worker is connected.
    """

    current = now or datetime.now(timezone.utc)
    delegation = verified.delegation
    if delegation.organisation != "sjk" or delegation.task_id != "morning-review":
        raise SyntheticAgentError("delegation is not for the synthetic SJK morning-review use case")

    demo = SPECIALTY_PACKS["infectiology"]["demo"]
    record_count = len(demo["cards"]) + len(demo["pending"])
    gateway = AgentGateway(
        delegation=delegation,
        registry=synthetic_sjk_registry(),
        execution=AgentExecutionState(started_at=current),
        memory_secret="synthetic-agent-memory-key",
    )

    audit_events: list[dict] = []

    read_request = AgentRequest(
        organisation="sjk",
        patient_ref=delegation.patient_ref,
        encounter_ref=delegation.encounter_ref,
        tool_id="read-clinical-context",
        operation=AgentOperation.READ,
        data_categories={"microbiology", "medication", "tasks", "hygiene", "trends"},
        requested_records=record_count,
        requested_pages=1,
    )
    read_decision = gateway.authorize(read_request, now=current)
    if not read_decision.allowed or read_decision.tool is None:
        raise SyntheticAgentError(f"read denied: {read_decision.reason}")
    gateway.record_tool_result(read_request)
    audit_events.append(
        make_agent_audit_event(
            execution_id=gateway.execution.execution_id,
            delegation_id=verified.delegation_id,
            human_actor_id=delegation.delegating_actor,
            agent_id=delegation.agent_id,
            agent_version=delegation.agent_version,
            organisation=delegation.organisation,
            patient_id=delegation.patient_ref,
            encounter_id=delegation.encounter_ref,
            task_id=delegation.task_id,
            event_type="tool_authorization",
            decision="allow",
            reason_code="inside_narrow_delegation",
            tool_id=read_decision.tool.tool_id,
            tool_version=read_decision.tool.version,
            operation=read_request.operation.value,
            data_categories=read_request.data_categories,
            outcome="success",
            pseudonym_key=pseudonym_key,
        )
    )

    prepare_request = AgentRequest(
        organisation="sjk",
        patient_ref=delegation.patient_ref,
        encounter_ref=delegation.encounter_ref,
        tool_id="prepare-handover",
        operation=AgentOperation.PREPARE,
        data_categories={"microbiology", "medication", "tasks", "hygiene", "trends"},
        requested_records=record_count,
        requested_pages=1,
    )
    prepare_decision = gateway.authorize(prepare_request, now=current)
    if not prepare_decision.allowed or prepare_decision.tool is None:
        raise SyntheticAgentError(f"prepare denied: {prepare_decision.reason}")
    gateway.record_tool_result(prepare_request)

    source_refs = []
    for item in demo["timeline"]:
        ref = item.get("ref")
        if ref and ref not in source_refs:
            source_refs.append(ref)

    draft = {
        "patient_display": "synthetic reference patient",
        "headline": "Synthetic source-linked morning-review draft",
        "handover": demo["handover"],
        "pending": list(demo["pending"]),
        "source_refs": source_refs,
        "warnings": [
            "synthetic data only",
            "draft for human review",
            "no diagnosis or treatment recommendation",
            "pending/unavailable must never be interpreted as negative",
        ],
    }

    audit_events.append(
        make_agent_audit_event(
            execution_id=gateway.execution.execution_id,
            delegation_id=verified.delegation_id,
            human_actor_id=delegation.delegating_actor,
            agent_id=delegation.agent_id,
            agent_version=delegation.agent_version,
            organisation=delegation.organisation,
            patient_id=delegation.patient_ref,
            encounter_id=delegation.encounter_ref,
            task_id=delegation.task_id,
            event_type="draft_prepared",
            decision="allow",
            reason_code="prepared_from_admitted_synthetic_context",
            tool_id=prepare_decision.tool.tool_id,
            tool_version=prepare_decision.tool.version,
            operation=prepare_request.operation.value,
            data_categories=prepare_request.data_categories,
            outcome="human_review_required",
            pseudonym_key=pseudonym_key,
        )
    )

    gateway.complete()
    return {
        "mode": "synthetic-only",
        "execution_id": gateway.execution.execution_id,
        "memory_namespace": gateway.memory_namespace,
        "status": gateway.execution.status.value,
        "usage": {
            "tool_calls": gateway.execution.tool_calls_used,
            "records": gateway.execution.records_used,
            "pages": gateway.execution.pages_used,
            "external_calls": gateway.execution.external_calls_used,
        },
        "draft": draft,
        "audit_preview": audit_events,
    }

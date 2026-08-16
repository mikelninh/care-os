from __future__ import annotations

from typing import Any

from .agent_models import ReasoningWorker, WorkerInput
from .agent_orchestrator import ActiveAgentExecution
from .agent_tool_proxy import AgentToolProxy
from .agent_worker import bind_tool_proposal, validate_low_consequence_draft


def run_reasoning_session(
    active: ActiveAgentExecution,
    *,
    worker: ReasoningWorker,
    source_text: str,
    handlers: dict[str, Any],
    now,
) -> dict:
    """Run an untrusted reasoning worker entirely behind CareOS policy.

    Tool proposals are bound to authoritative delegated context, authorized by the
    gateway, then executed only through trusted handlers. A harmful proposal aborts
    the execution. Low-consequence drafts must be source-linked and review-only.
    """

    delegation = active.verified.delegation
    proxy = AgentToolProxy(active.gateway, handlers)
    worker_input = WorkerInput(
        task=delegation.task_id,
        source_text=source_text,
        allowed_tool_ids=tuple(sorted(delegation.allowed_tools)),
        allowed_data_categories=tuple(sorted(delegation.allowed_data_categories)),
    )

    tool_payloads: list[Any] = []
    try:
        for proposal in worker.propose(worker_input):
            request = bind_tool_proposal(delegation, proposal)
            result = proxy.call(request, now=now)
            tool_payloads.append(result.payload)
    except Exception as exc:
        active.abort(f"worker/tool proposal denied or failed: {exc}")
        raise

    facts: list[dict] = []
    for payload in tool_payloads:
        if isinstance(payload, list):
            facts.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            facts.append(payload)

    draft = validate_low_consequence_draft(worker.draft(facts=facts, task=delegation.task_id))
    active.complete(now=now)
    return {
        "execution_id": active.gateway.execution.execution_id,
        "mode": active.mode.value,
        "worker": {"id": worker.model_id, "version": worker.model_version},
        "status": active.gateway.execution.status.value,
        "usage": {
            "tool_calls": active.gateway.execution.tool_calls_used,
            "records": active.gateway.execution.records_used,
            "pages": active.gateway.execution.pages_used,
            "external_calls": active.gateway.execution.external_calls_used,
        },
        "draft": draft.model_dump(mode="json"),
    }

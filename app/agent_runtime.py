from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from .agent_policy import AgentDecision, AgentDelegation, AgentRequest, evaluate_agent_request
from .agent_tools import ToolRegistry, ToolSpec
from .audit import pseudonymous_ref


class ExecutionStatus(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    COMPLETED = "completed"
    DENIED = "denied"
    ABORTED = "aborted"
    EXPIRED = "expired"


class AgentExecutionState(BaseModel):
    execution_id: str = Field(default_factory=lambda: str(uuid4()))
    status: ExecutionStatus = ExecutionStatus.CREATED
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tool_calls_used: int = 0
    records_used: int = 0
    pages_used: int = 0
    external_calls_used: int = 0
    last_denial_reason: str | None = None


@dataclass(frozen=True)
class GatewayDecision:
    allowed: bool
    reason: str
    tool: ToolSpec | None
    memory_namespace: str
    audit_level: str = "high"


class AgentGateway:
    """Deterministic authorization boundary around an untrusted reasoning worker.

    The gateway does not execute model reasoning. It validates every proposed tool
    request against a signed/narrow delegation, the registered tool metadata and
    execution-local budgets. A hostile model can only request; it cannot mutate the
    policy state directly.
    """

    def __init__(
        self,
        *,
        delegation: AgentDelegation,
        registry: ToolRegistry,
        execution: AgentExecutionState | None = None,
        consequential_actions_enabled: bool = False,
        memory_secret: str | bytes | None = None,
    ):
        self.delegation = delegation
        self.registry = registry
        self.execution = execution or AgentExecutionState()
        self.consequential_actions_enabled = consequential_actions_enabled
        self.memory_secret = memory_secret

    @property
    def memory_namespace(self) -> str:
        raw = "|".join(
            [
                self.delegation.organisation,
                self.delegation.patient_ref,
                self.delegation.encounter_ref or "no-encounter",
                self.execution.execution_id,
            ]
        )
        return f"agent-memory:{pseudonymous_ref(raw, secret=self.memory_secret)}"

    def _deny(self, reason: str, *, tool: ToolSpec | None = None) -> GatewayDecision:
        self.execution.status = ExecutionStatus.DENIED
        self.execution.last_denial_reason = reason
        return GatewayDecision(False, reason, tool, self.memory_namespace)

    def authorize(self, request: AgentRequest, *, now: datetime | None = None) -> GatewayDecision:
        current = now or datetime.now(timezone.utc)
        if self.execution.status in {ExecutionStatus.COMPLETED, ExecutionStatus.ABORTED, ExecutionStatus.EXPIRED}:
            return self._deny(f"execution is {self.execution.status.value}")

        # Runtime-owned counters replace any model-provided accounting fields.
        effective_request = request.model_copy(
            update={
                "tool_call_number": self.execution.tool_calls_used + 1,
                "requested_records": request.requested_records,
                "requested_pages": request.requested_pages,
                "elapsed_seconds": max(0, int((current - self.execution.started_at).total_seconds())),
            }
        )

        base: AgentDecision = evaluate_agent_request(
            self.delegation,
            effective_request,
            now=current,
            consequential_actions_enabled=self.consequential_actions_enabled,
        )
        if not base.allowed:
            if "expired" in base.reason:
                self.execution.status = ExecutionStatus.EXPIRED
            return self._deny(base.reason)

        tool = self.registry.get(request.tool_id)
        if tool is None or not tool.enabled:
            return self._deny("tool is not registered and enabled")
        if tool.operation != request.operation:
            return self._deny("requested operation does not match registered tool effect", tool=tool)
        if not request.data_categories.issubset(tool.data_categories):
            return self._deny("requested data category exceeds registered tool contract", tool=tool)
        if request.requested_records > tool.max_records_per_call:
            return self._deny("request exceeds tool record ceiling", tool=tool)
        if request.requested_pages > tool.max_pages_per_call:
            return self._deny("request exceeds tool page ceiling", tool=tool)
        if request.egress_host is not None and request.egress_host not in tool.allowed_egress_hosts:
            return self._deny("egress exceeds registered tool contract", tool=tool)
        if tool.requires_human_confirmation and not self.consequential_actions_enabled:
            return self._deny("tool requires a separately released human-confirmation flow", tool=tool)

        # Aggregate budgets are checked as well as per-call limits.
        if self.execution.records_used + request.requested_records > self.delegation.max_records:
            return self._deny("execution record budget would be exceeded", tool=tool)
        if self.execution.pages_used + request.requested_pages > self.delegation.max_pages:
            return self._deny("execution page budget would be exceeded", tool=tool)

        self.execution.status = ExecutionStatus.ACTIVE
        return GatewayDecision(True, "request admitted by deterministic agent gateway", tool, self.memory_namespace)

    def record_tool_result(self, request: AgentRequest, *, external_call: bool = False) -> None:
        if self.execution.status != ExecutionStatus.ACTIVE:
            raise RuntimeError("cannot record a tool result outside an active admitted execution")
        self.execution.tool_calls_used += 1
        self.execution.records_used += request.requested_records
        self.execution.pages_used += request.requested_pages
        if external_call:
            self.execution.external_calls_used += 1

    def complete(self) -> None:
        if self.execution.status not in {ExecutionStatus.ACTIVE, ExecutionStatus.CREATED}:
            raise RuntimeError("only a non-terminal execution can complete")
        self.execution.status = ExecutionStatus.COMPLETED

    def abort(self, reason: str) -> None:
        self.execution.status = ExecutionStatus.ABORTED
        self.execution.last_denial_reason = reason

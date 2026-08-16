from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class AgentOperation(str, Enum):
    READ = "read"
    PREPARE = "prepare"
    WRITE = "write"
    EXTERNAL_SEND = "external_send"
    PATIENT_SEARCH = "patient_search"


class AgentDelegation(BaseModel):
    """A narrow authority envelope for one agent execution.

    This is an authorization contract, not an authentication mechanism. Production
    use still requires cryptographically verifiable workload/agent identity and a
    signed delegation token issued by an approved authority.
    """

    agent_id: str = Field(min_length=1)
    agent_version: str = Field(min_length=1)
    delegating_actor: str = Field(min_length=1)
    organisation: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    encounter_ref: str | None = None
    task_id: str = Field(min_length=1)

    allowed_tools: set[str] = Field(default_factory=set)
    allowed_operations: set[AgentOperation] = Field(default_factory=lambda: {AgentOperation.READ})
    allowed_data_categories: set[str] = Field(default_factory=set)
    allowed_egress_hosts: set[str] = Field(default_factory=set)

    issued_at: datetime
    expires_at: datetime

    max_tool_calls: int = Field(default=8, ge=1, le=100)
    max_records: int = Field(default=100, ge=1, le=10_000)
    max_pages: int = Field(default=10, ge=1, le=100)
    max_runtime_seconds: int = Field(default=120, ge=1, le=3_600)
    max_subagent_depth: int = Field(default=0, ge=0, le=4)

    allow_break_glass: bool = False
    allow_subdelegation: bool = False

    @model_validator(mode="after")
    def validate_window(self) -> "AgentDelegation":
        issued = _as_utc(self.issued_at)
        expires = _as_utc(self.expires_at)
        if expires <= issued:
            raise ValueError("agent delegation must expire after it is issued")
        return self


class AgentRequest(BaseModel):
    organisation: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    encounter_ref: str | None = None
    tool_id: str = Field(min_length=1)
    operation: AgentOperation
    data_categories: set[str] = Field(default_factory=set)
    requested_records: int = Field(default=1, ge=0)
    requested_pages: int = Field(default=1, ge=0)
    tool_call_number: int = Field(default=1, ge=1)
    elapsed_seconds: int = Field(default=0, ge=0)
    subagent_depth: int = Field(default=0, ge=0)
    egress_host: str | None = None
    break_glass: bool = False


class AgentDecision(BaseModel):
    allowed: bool
    reason: str
    audit_level: str = "high"


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def evaluate_agent_request(
    delegation: AgentDelegation,
    request: AgentRequest,
    *,
    now: datetime | None = None,
    consequential_actions_enabled: bool = False,
) -> AgentDecision:
    """Fail-closed authorization for a tool-using agent.

    Important: this must be called *after* agent/workload identity and delegation
    signature verification in a real deployment. Model output is never an input to
    the allow/deny policy itself beyond the concrete requested tool arguments.
    """

    current = _as_utc(now or datetime.now(timezone.utc))
    issued = _as_utc(delegation.issued_at)
    expires = _as_utc(delegation.expires_at)

    if current < issued:
        return AgentDecision(allowed=False, reason="delegation not yet valid")
    if current >= expires:
        return AgentDecision(allowed=False, reason="delegation expired")

    if request.organisation != delegation.organisation:
        return AgentDecision(allowed=False, reason="organisation outside delegation")
    if request.patient_ref != delegation.patient_ref:
        return AgentDecision(allowed=False, reason="patient outside delegation")
    if delegation.encounter_ref is not None and request.encounter_ref != delegation.encounter_ref:
        return AgentDecision(allowed=False, reason="encounter outside delegation")

    # Agents do not autonomously break glass. Keep the field on the model so an
    # attempted escalation is visible and explicitly denied rather than ignored.
    if request.break_glass:
        return AgentDecision(allowed=False, reason="agents cannot autonomously invoke break glass")

    if request.operation not in delegation.allowed_operations:
        return AgentDecision(allowed=False, reason="operation outside delegation")

    if request.operation in {AgentOperation.WRITE, AgentOperation.EXTERNAL_SEND} and not consequential_actions_enabled:
        return AgentDecision(allowed=False, reason="consequential agent actions disabled by release policy")

    if request.operation == AgentOperation.PATIENT_SEARCH:
        return AgentDecision(allowed=False, reason="arbitrary patient search is not permitted for patient-scoped agents")

    if request.tool_id not in delegation.allowed_tools:
        return AgentDecision(allowed=False, reason="tool outside delegation")

    if not request.data_categories.issubset(delegation.allowed_data_categories):
        return AgentDecision(allowed=False, reason="data category outside delegation")

    if request.tool_call_number > delegation.max_tool_calls:
        return AgentDecision(allowed=False, reason="tool-call ceiling exceeded")
    if request.requested_records > delegation.max_records:
        return AgentDecision(allowed=False, reason="record ceiling exceeded")
    if request.requested_pages > delegation.max_pages:
        return AgentDecision(allowed=False, reason="page ceiling exceeded")
    if request.elapsed_seconds > delegation.max_runtime_seconds:
        return AgentDecision(allowed=False, reason="runtime ceiling exceeded")

    if request.subagent_depth > delegation.max_subagent_depth:
        return AgentDecision(allowed=False, reason="sub-agent depth outside delegation")
    if request.subagent_depth > 0 and not delegation.allow_subdelegation:
        return AgentDecision(allowed=False, reason="sub-delegation disabled")

    if request.egress_host is not None and request.egress_host not in delegation.allowed_egress_hosts:
        return AgentDecision(allowed=False, reason="egress destination outside delegation")

    return AgentDecision(allowed=True, reason="request is inside narrow agent delegation")

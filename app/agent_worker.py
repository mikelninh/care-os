from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .agent_policy import AgentDelegation, AgentOperation, AgentRequest


class AgentToolProposal(BaseModel):
    """Untrusted model/worker proposal.

    The reasoning worker is deliberately unable to choose organisation, patient,
    encounter, break-glass state, recursion depth or network destination. Those are
    policy/runtime properties injected by CareOS. Unknown fields are rejected so a
    model cannot smuggle policy overrides into the request envelope.
    """

    model_config = ConfigDict(extra="forbid")

    tool_id: str = Field(min_length=1)
    operation: AgentOperation
    data_categories: set[str] = Field(default_factory=set)
    requested_records: int = Field(default=1, ge=0)
    requested_pages: int = Field(default=1, ge=0)


class AgentDraft(BaseModel):
    """Prepared model output is never a trusted clinical fact or final action."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    source_fact_ids: list[str] = Field(default_factory=list)
    review_required: bool = True
    contains_recommendation: bool = False


def bind_tool_proposal(delegation: AgentDelegation, proposal: AgentToolProposal) -> AgentRequest:
    """Bind untrusted proposal to authoritative delegated context."""

    return AgentRequest(
        organisation=delegation.organisation,
        patient_ref=delegation.patient_ref,
        encounter_ref=delegation.encounter_ref,
        tool_id=proposal.tool_id,
        operation=proposal.operation,
        data_categories=proposal.data_categories,
        requested_records=proposal.requested_records,
        requested_pages=proposal.requested_pages,
        egress_host=None,
        break_glass=False,
        subagent_depth=0,
    )

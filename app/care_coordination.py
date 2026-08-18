from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .audit import make_audit_event


class CareRequestState(str, Enum):
    DRAFT = "draft"
    REQUESTED = "requested"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    SCHEDULED = "scheduled"
    PERFORMED = "performed"
    RESULT_AVAILABLE = "result-available"
    FOLLOW_UP_COMPLETE = "follow-up-complete"
    CANCELLED = "cancelled"


_ALLOWED: dict[CareRequestState, set[CareRequestState]] = {
    CareRequestState.DRAFT: {CareRequestState.REQUESTED, CareRequestState.CANCELLED},
    CareRequestState.REQUESTED: {CareRequestState.RECEIVED, CareRequestState.CANCELLED},
    CareRequestState.RECEIVED: {CareRequestState.ACCEPTED, CareRequestState.DECLINED, CareRequestState.CANCELLED},
    CareRequestState.ACCEPTED: {CareRequestState.SCHEDULED, CareRequestState.PERFORMED, CareRequestState.CANCELLED},
    CareRequestState.SCHEDULED: {CareRequestState.PERFORMED, CareRequestState.CANCELLED},
    CareRequestState.PERFORMED: {CareRequestState.RESULT_AVAILABLE, CareRequestState.FOLLOW_UP_COMPLETE},
    CareRequestState.RESULT_AVAILABLE: {CareRequestState.FOLLOW_UP_COMPLETE},
    CareRequestState.DECLINED: set(),
    CareRequestState.FOLLOW_UP_COMPLETE: set(),
    CareRequestState.CANCELLED: set(),
}


class ContextReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(min_length=1)
    category: str = Field(min_length=1)
    purpose_relevant: bool = True


class CareRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    sender_org: str = Field(min_length=1)
    receiver_org: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    transport_profile: str = Field(min_length=1)
    context_refs: tuple[ContextReference, ...]
    state: CareRequestState = CareRequestState.DRAFT

    @model_validator(mode="after")
    def require_minimum_purpose_relevant_context(self) -> "CareRequest":
        if not self.context_refs:
            raise ValueError("care request requires explicit minimum-necessary context references")
        if any(not ref.purpose_relevant for ref in self.context_refs):
            raise ValueError("care request includes context not declared relevant to the stated purpose")
        return self


class CoordinationTransition(BaseModel):
    request: CareRequest
    previous_state: CareRequestState
    new_state: CareRequestState
    actor_id: str
    human_confirmed: bool
    audit_event: dict


def transition_request(
    request: CareRequest,
    new_state: CareRequestState,
    *,
    actor_id: str,
    human_confirmed: bool = False,
) -> CoordinationTransition:
    if new_state not in _ALLOWED[request.state]:
        raise ValueError(f"invalid care-request transition: {request.state.value} -> {new_state.value}")

    if request.state == CareRequestState.DRAFT and new_state == CareRequestState.REQUESTED and not human_confirmed:
        raise ValueError("sending a prepared care request requires governed human/workflow confirmation")

    previous = request.state
    updated = request.model_copy(update={"state": new_state})
    event = make_audit_event(
        actor_id=actor_id,
        patient_id=request.patient_ref,
        action="care-request-transition",
        resource_type="care-request",
        resource_id=request.request_id,
        outcome=new_state.value,
        audit_level="normal",
        reason_code=f"{previous.value}-to-{new_state.value}",
    )
    return CoordinationTransition(
        request=updated,
        previous_state=previous,
        new_state=new_state,
        actor_id=actor_id,
        human_confirmed=human_confirmed,
        audit_event=event,
    )


def synthetic_coordination_request() -> CareRequest:
    return CareRequest(
        request_id="synthetic-referral-001",
        patient_ref="synthetic-patient-001",
        sender_org="Synthetic Hospital",
        receiver_org="Synthetic Practice",
        purpose="post-discharge follow-up",
        owner="discharge-team",
        transport_profile="approved-digital-rail",
        context_refs=(
            ContextReference(source_ref="kis:discharge-plan-1", category="follow-up-plan"),
            ContextReference(source_ref="kis:med-change-2", category="medication-change"),
            ContextReference(source_ref="lis:pending-result-3", category="pending-result"),
        ),
    )

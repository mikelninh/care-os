from __future__ import annotations

from pydantic import BaseModel, Field


class AssistanceDraft(BaseModel):
    patient_ref: str = Field(min_length=1)
    encounter_ref: str | None = None
    task: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    pending_items: list[str] = Field(default_factory=list)
    review_required: bool = True
    can_write: bool = False
    can_send: bool = False
    can_order: bool = False


def validate_read_only_assistance(draft: AssistanceDraft) -> AssistanceDraft:
    if not draft.review_required:
        raise ValueError("CareOS agent assistance requires explicit human review")
    if draft.can_write or draft.can_send or draft.can_order:
        raise ValueError("read-only assistance cannot perform consequential actions")
    if not draft.source_refs:
        raise ValueError("read-only assistance requires source references")
    return draft

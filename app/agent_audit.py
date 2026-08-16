from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from .audit import pseudonymous_ref, validate_event


class AgentAuditEvent(BaseModel):
    timestamp: str
    execution_id: str = Field(min_length=1)
    delegation_id: str = Field(min_length=1)
    human_actor_ref: str = Field(min_length=1)
    agent_ref: str = Field(min_length=1)
    agent_version: str = Field(min_length=1)
    organisation_ref: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    encounter_ref: str | None = None
    task_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    tool_id: str | None = None
    tool_version: str | None = None
    operation: str | None = None
    decision: str = Field(min_length=1)
    reason_code: str = Field(min_length=1)
    data_categories: list[str] = Field(default_factory=list)
    egress_host: str | None = None
    model_provider: str | None = None
    model_id: str | None = None
    human_confirmation_id: str | None = None
    outcome: str | None = None


def make_agent_audit_event(
    *,
    execution_id: str,
    delegation_id: str,
    human_actor_id: str,
    agent_id: str,
    agent_version: str,
    organisation: str,
    patient_id: str,
    encounter_id: str | None,
    task_id: str,
    event_type: str,
    decision: str,
    reason_code: str,
    tool_id: str | None = None,
    tool_version: str | None = None,
    operation: str | None = None,
    data_categories: set[str] | None = None,
    egress_host: str | None = None,
    model_provider: str | None = None,
    model_id: str | None = None,
    human_confirmation_id: str | None = None,
    outcome: str | None = None,
    pseudonym_key: str | bytes | None = None,
) -> dict[str, Any]:
    """Create structured audit metadata without clinical free text.

    `reason_code` must be a stable machine reason, not a copied model response or
    clinical note. Production storage still belongs in a protected provider audit
    boundary; this helper only defines the event schema.
    """

    event = AgentAuditEvent(
        timestamp=datetime.now(timezone.utc).isoformat(),
        execution_id=execution_id,
        delegation_id=delegation_id,
        human_actor_ref=pseudonymous_ref(human_actor_id, secret=pseudonym_key),
        agent_ref=pseudonymous_ref(agent_id, secret=pseudonym_key),
        agent_version=agent_version,
        organisation_ref=pseudonymous_ref(organisation, secret=pseudonym_key),
        patient_ref=pseudonymous_ref(patient_id, secret=pseudonym_key),
        encounter_ref=pseudonymous_ref(encounter_id, secret=pseudonym_key) if encounter_id else None,
        task_id=task_id,
        event_type=event_type,
        tool_id=tool_id,
        tool_version=tool_version,
        operation=operation,
        decision=decision,
        reason_code=reason_code,
        data_categories=sorted(data_categories or set()),
        egress_host=egress_host,
        model_provider=model_provider,
        model_id=model_id,
        human_confirmation_id=human_confirmation_id,
        outcome=outcome,
    ).model_dump(mode="json")
    validate_event(event)
    return event

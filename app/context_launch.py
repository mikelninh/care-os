from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Protocol

from pydantic import BaseModel, Field, model_validator

from .access_policy import AccessRequest, UserContext
from .auth_oidc import AuthenticatedIdentity


class ClinicalLaunchContext(BaseModel):
    """Short-lived patient/encounter context supplied by a trusted hospital launcher.

    This is a contract, not a claim that a particular KIS already supports it. The
    production resolver must obtain/verify context from a trusted hospital integration;
    the browser must not be allowed to invent patient IDs as authoritative context.
    """

    context_id: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    organisation: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    encounter_ref: str | None = None
    launcher: str = Field(min_length=1)
    issued_at: datetime
    expires_at: datetime

    @model_validator(mode="after")
    def validate_window(self) -> "ClinicalLaunchContext":
        if self.expires_at <= self.issued_at:
            raise ValueError("launch context must expire after issuance")
        if self.expires_at - self.issued_at > timedelta(minutes=15):
            raise ValueError("launch context lifetime may not exceed 15 minutes")
        return self

    def is_current(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.issued_at <= now < self.expires_at


class ContextResolver(Protocol):
    def resolve(self, context_token: str) -> ClinicalLaunchContext: ...


class ContextBindingError(ValueError):
    pass


def bind_context(identity: AuthenticatedIdentity, user: UserContext, context: ClinicalLaunchContext) -> AccessRequest:
    """Bind authenticated identity to the short-lived hospital patient context."""

    if not context.is_current():
        raise ContextBindingError("launch context expired or not yet valid")
    if identity.subject != user.subject or identity.subject != context.subject:
        raise ContextBindingError("launch context subject does not match authenticated identity")
    if user.organisation != context.organisation:
        raise ContextBindingError("launch context organisation does not match authorized organisation")
    if context.patient_ref not in user.treatment_patient_refs:
        raise ContextBindingError("launch patient is outside current treatment context")
    return AccessRequest(patient_ref=context.patient_ref)

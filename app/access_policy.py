from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class AccessAction(str, Enum):
    READ = "read"
    WRITE = "write"


class UserContext(BaseModel):
    subject: str = Field(min_length=1)
    organisation: str = Field(min_length=1)
    roles: set[str] = Field(default_factory=set)
    scopes: set[str] = Field(default_factory=set)
    treatment_patient_refs: set[str] = Field(default_factory=set)


class AccessRequest(BaseModel):
    patient_ref: str = Field(min_length=1)
    action: AccessAction = AccessAction.READ
    break_glass: bool = False
    break_glass_reason: str | None = None


class AccessDecision(BaseModel):
    allowed: bool
    reason: str
    audit_level: str = "normal"
    break_glass: bool = False


CLINICAL_ROLES = {"doctor", "nurse", "pharmacist", "therapist"}


def evaluate_access(user: UserContext, request: AccessRequest, *, writeback_enabled: bool = False) -> AccessDecision:
    """Fail-closed policy contract for the future hospital identity integration.

    This function does not authenticate users. Production identity must verify OIDC/JWT
    and then construct UserContext from trusted claims/authoritative mappings.
    """

    if not (user.roles & CLINICAL_ROLES):
        return AccessDecision(allowed=False, reason="no recognised clinical role")

    required_scope = "patient:write" if request.action == AccessAction.WRITE else "patient:read"
    if required_scope not in user.scopes:
        return AccessDecision(allowed=False, reason=f"missing scope {required_scope}")

    if request.action == AccessAction.WRITE and not writeback_enabled:
        return AccessDecision(allowed=False, reason="clinical write-back disabled by release policy")

    if request.patient_ref in user.treatment_patient_refs:
        return AccessDecision(allowed=True, reason="active treatment context")

    if request.break_glass:
        reason = (request.break_glass_reason or "").strip()
        if len(reason) < 10:
            return AccessDecision(allowed=False, reason="break-glass requires a meaningful reason", audit_level="high")
        return AccessDecision(
            allowed=True,
            reason="break-glass emergency access; elevated audit required",
            audit_level="high",
            break_glass=True,
        )

    return AccessDecision(allowed=False, reason="patient is outside current treatment context")

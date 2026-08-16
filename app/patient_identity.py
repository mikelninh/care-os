from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class IdentifierStrength(str, Enum):
    STRONG = "strong"
    SUPPORTING = "supporting"


class PatientIdentifier(BaseModel):
    system: str = Field(min_length=1)
    value: str = Field(min_length=1)
    issuer: str | None = None
    strength: IdentifierStrength = IdentifierStrength.SUPPORTING
    verified: bool = False

    @property
    def key(self) -> tuple[str, str, str | None]:
        return (self.system, self.value, self.issuer)


class PatientIdentityRecord(BaseModel):
    local_ref: str = Field(min_length=1)
    identifiers: list[PatientIdentifier] = Field(default_factory=list)
    display_name: str | None = None
    birth_date: str | None = None


class IdentityDecision(str, Enum):
    EXACT = "exact"
    REVIEW = "review"
    CONFLICT = "conflict"
    NO_MATCH = "no-match"


class IdentityResolution(BaseModel):
    decision: IdentityDecision
    candidate_ref: str | None = None
    reason: str
    matched_identifiers: list[tuple[str, str, str | None]] = Field(default_factory=list)

    @property
    def automatic_attachment_allowed(self) -> bool:
        return self.decision == IdentityDecision.EXACT


def _verified_strong(record: PatientIdentityRecord) -> set[tuple[str, str, str | None]]:
    return {i.key for i in record.identifiers if i.verified and i.strength == IdentifierStrength.STRONG}


def resolve_patient_identity(incoming: PatientIdentityRecord, candidates: list[PatientIdentityRecord]) -> IdentityResolution:
    """Deterministic, fail-closed identity resolution.

    Automatic attachment requires one unique candidate sharing a verified strong
    identifier. Demographics/supporting identifiers may trigger review but never auto
    attachment. Conflicting strong identifiers block automatic resolution.
    """

    incoming_strong = _verified_strong(incoming)
    exact: list[tuple[PatientIdentityRecord, set[tuple[str, str, str | None]]]] = []

    for candidate in candidates:
        shared = incoming_strong & _verified_strong(candidate)
        if shared:
            exact.append((candidate, shared))

    if len(exact) == 1:
        candidate, shared = exact[0]
        candidate_strong = _verified_strong(candidate)
        for inc in incoming_strong:
            for cand in candidate_strong:
                if inc[0] == cand[0] and inc != cand:
                    return IdentityResolution(decision=IdentityDecision.CONFLICT, reason="verified strong identifiers conflict within the same identifier system")
        return IdentityResolution(
            decision=IdentityDecision.EXACT,
            candidate_ref=candidate.local_ref,
            reason="unique shared verified strong identifier",
            matched_identifiers=sorted(shared, key=lambda item: (item[0], item[1], item[2] or "")),
        )

    if len(exact) > 1:
        return IdentityResolution(decision=IdentityDecision.CONFLICT, reason="verified strong identifier maps to multiple candidates")

    demographic_candidates = [
        c for c in candidates
        if incoming.display_name and incoming.birth_date
        and c.display_name == incoming.display_name
        and c.birth_date == incoming.birth_date
    ]
    if demographic_candidates:
        return IdentityResolution(
            decision=IdentityDecision.REVIEW,
            candidate_ref=demographic_candidates[0].local_ref if len(demographic_candidates) == 1 else None,
            reason="demographic similarity without shared verified strong identifier",
        )

    return IdentityResolution(decision=IdentityDecision.NO_MATCH, reason="no shared verified strong identifier")

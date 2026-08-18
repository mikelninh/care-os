from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ResolutionState(str, Enum):
    RESOLVED = "resolved"
    NOT_FOUND = "not-found"
    AMBIGUOUS = "ambiguous"
    UNAVAILABLE = "unavailable"
    STALE = "stale"


class SourcePatientMapping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    source_patient_ref: str = Field(min_length=1)
    namespace: str = Field(min_length=1)
    resolver_id: str = Field(min_length=1)
    resolver_version: str = Field(min_length=1)
    resolved_at: datetime
    expires_at: datetime | None = None

    def current(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.expires_at is None or self.expires_at > now


class PatientResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enterprise_patient_ref: str = Field(min_length=1)
    state: ResolutionState
    mappings: tuple[SourcePatientMapping, ...] = ()
    detail: str | None = None

    @model_validator(mode="after")
    def validate_resolution(self) -> "PatientResolution":
        if self.state == ResolutionState.RESOLVED and not self.mappings:
            raise ValueError("resolved patient identity requires source mappings")
        if self.state != ResolutionState.RESOLVED and self.mappings:
            raise ValueError("non-resolved patient identity may not carry authoritative mappings")
        if self.state != ResolutionState.RESOLVED and not self.detail:
            raise ValueError("non-resolved patient identity requires a visible detail")
        source_ids = [mapping.source_id for mapping in self.mappings]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("resolved patient identity contains duplicate source mappings")
        return self

    def mapping_for(self, source_id: str, *, now: datetime | None = None) -> SourcePatientMapping:
        if self.state != ResolutionState.RESOLVED:
            raise ValueError(f"patient identity is {self.state.value}: {self.detail or ''}".strip())
        matches = [mapping for mapping in self.mappings if mapping.source_id == source_id]
        if len(matches) != 1:
            raise ValueError(f"expected exactly one patient mapping for source {source_id!r}")
        mapping = matches[0]
        if not mapping.current(now):
            raise ValueError(f"patient mapping for source {source_id!r} is stale/expired")
        return mapping


class PatientIdResolver(Protocol):
    resolver_id: str

    def resolve(self, enterprise_patient_ref: str, source_ids: tuple[str, ...]) -> PatientResolution: ...


class StaticPatientIdResolver:
    """Synthetic/deidentified deterministic resolver for tests and approved mappings.

    This is deliberately not a fuzzy matcher. A production adapter may call a hospital
    MPI/EMPI/identity service, but it must return the same typed fail-closed contract.
    """

    def __init__(
        self,
        *,
        mappings: dict[str, dict[str, str]],
        resolver_id: str = "static-synthetic-mpi",
        resolver_version: str = "1",
        namespace_by_source: dict[str, str] | None = None,
    ):
        self.resolver_id = resolver_id
        self.resolver_version = resolver_version
        self._mappings = mappings
        self._namespaces = namespace_by_source or {}

    def resolve(self, enterprise_patient_ref: str, source_ids: tuple[str, ...]) -> PatientResolution:
        by_source = self._mappings.get(enterprise_patient_ref)
        if by_source is None:
            return PatientResolution(
                enterprise_patient_ref=enterprise_patient_ref,
                state=ResolutionState.NOT_FOUND,
                detail="enterprise patient identifier is not present in the configured resolver",
            )
        missing = [source_id for source_id in source_ids if not by_source.get(source_id)]
        if missing:
            return PatientResolution(
                enterprise_patient_ref=enterprise_patient_ref,
                state=ResolutionState.NOT_FOUND,
                detail="no authoritative source mapping for: " + ", ".join(sorted(missing)),
            )
        now = datetime.now(timezone.utc)
        return PatientResolution(
            enterprise_patient_ref=enterprise_patient_ref,
            state=ResolutionState.RESOLVED,
            mappings=tuple(
                SourcePatientMapping(
                    source_id=source_id,
                    source_patient_ref=by_source[source_id],
                    namespace=self._namespaces.get(source_id, source_id),
                    resolver_id=self.resolver_id,
                    resolver_version=self.resolver_version,
                    resolved_at=now,
                )
                for source_id in source_ids
            ),
        )

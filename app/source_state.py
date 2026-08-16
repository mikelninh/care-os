from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class SourceAvailability(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class SourceState(BaseModel):
    source_id: str = Field(min_length=1)
    availability: SourceAvailability
    last_success_at: datetime | None = None
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    max_age_seconds: int = Field(default=300, gt=0)
    detail: str | None = None

    @model_validator(mode="after")
    def validate_state(self) -> "SourceState":
        if self.availability in {SourceAvailability.CURRENT, SourceAvailability.STALE} and not self.last_success_at:
            raise ValueError("current/stale source state requires last_success_at")
        if self.availability in {SourceAvailability.UNAVAILABLE, SourceAvailability.UNKNOWN} and not self.detail:
            raise ValueError("unavailable/unknown source state requires a detail")
        return self

    def evaluated_availability(self, now: datetime | None = None) -> SourceAvailability:
        """Re-evaluate freshness without turning transport failure into clinical absence."""
        if self.availability in {SourceAvailability.UNAVAILABLE, SourceAvailability.UNKNOWN}:
            return self.availability
        now = now or datetime.now(timezone.utc)
        if not self.last_success_at:
            return SourceAvailability.UNKNOWN
        age = now - self.last_success_at
        return SourceAvailability.STALE if age > timedelta(seconds=self.max_age_seconds) else SourceAvailability.CURRENT

    @property
    def may_assert_absence(self) -> bool:
        """Only a successfully refreshed/current source may support an 'absent' claim.

        Even then, domain-specific query completeness must be checked separately. This
        property exists mainly to prevent UI code from converting source outages/stale
        caches into reassuring empty states.
        """
        return self.evaluated_availability() == SourceAvailability.CURRENT


def source_result(*, state: SourceState, items: list[dict]) -> dict:
    evaluated = state.evaluated_availability()
    return {
        "source_id": state.source_id,
        "availability": evaluated.value,
        "last_success_at": state.last_success_at.isoformat() if state.last_success_at else None,
        "observed_at": state.observed_at.isoformat(),
        "max_age_seconds": state.max_age_seconds,
        "items": items if evaluated in {SourceAvailability.CURRENT, SourceAvailability.STALE} else [],
        "count": len(items) if evaluated in {SourceAvailability.CURRENT, SourceAvailability.STALE} else None,
        "absence_claim_allowed": evaluated == SourceAvailability.CURRENT,
        "warning": (
            None if evaluated == SourceAvailability.CURRENT
            else "Source data is stale; do not interpret missing items as absent." if evaluated == SourceAvailability.STALE
            else "Source unavailable/unknown; no clinical absence claim may be made."
        ),
    }

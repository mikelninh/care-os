from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable

from .clinical_truth import AssertionStage, ClinicalFact, FactStatus, TruthEnvelope


class ReconciliationDisposition(str, Enum):
    CURRENT = "current"
    SUPERSEDED = "superseded"
    REVIEW = "review"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ReconciliationIssue:
    code: str
    fact_ids: tuple[str, ...]
    reason: str


@dataclass
class ReconciliationResult:
    patient_ref: str
    current: list[ClinicalFact] = field(default_factory=list)
    superseded: list[ClinicalFact] = field(default_factory=list)
    review: list[ClinicalFact] = field(default_factory=list)
    cancelled: list[ClinicalFact] = field(default_factory=list)
    corroborating_fact_ids: dict[str, tuple[str, ...]] = field(default_factory=dict)
    issues: list[ReconciliationIssue] = field(default_factory=list)

    @property
    def safe_for_default_surface(self) -> bool:
        return not any(issue.code.startswith("critical-") for issue in self.issues)

    @property
    def provenance_coverage(self) -> float:
        surfaced = self.current + self.review
        if not surfaced:
            return 1.0
        return sum(1 for f in surfaced if f.provenance_complete) / len(surfaced)


# These rules are intentionally explicit. "Newest wins" is dangerous as a generic
# medical rule, so only fact families whose semantics are state snapshots opt in.
LATEST_STATE_FACT_TYPES = frozenset({
    "renal_function",
    "current_medications",
    "open_followups",
    "discharge",
})

_STAGE_RANK = {
    AssertionStage.UNKNOWN: 0,
    AssertionStage.PRELIMINARY: 1,
    AssertionStage.FINAL: 2,
    AssertionStage.CORRECTED: 3,
    AssertionStage.CANCELLED: -1,
}


def _time(fact: ClinicalFact) -> datetime:
    value = fact.effective_time or fact.recorded_time or fact.ingested_at
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _normalized_value(fact: ClinicalFact):
    return fact.value_normalized if fact.value_normalized is not None else fact.value_original


def _same_value(facts: list[ClinicalFact]) -> bool:
    if not facts:
        return True
    first = _normalized_value(facts[0])
    return all(_normalized_value(f) == first for f in facts[1:])


def _pick_by_stage(facts: list[ClinicalFact]) -> tuple[ClinicalFact | None, list[ClinicalFact]]:
    """Choose a uniquely most mature assertion; never break ties by confidence."""

    if not facts:
        return None, []
    top_rank = max(_STAGE_RANK[f.assertion_stage] for f in facts)
    top = [f for f in facts if _STAGE_RANK[f.assertion_stage] == top_rank]
    if len(top) == 1 and top[0].assertion_stage in {
        AssertionStage.FINAL,
        AssertionStage.CORRECTED,
    }:
        return top[0], [f for f in facts if f.fact_id != top[0].fact_id]
    return None, []


def _validate_patient(envelopes: Iterable[TruthEnvelope]) -> tuple[str, list[ClinicalFact]]:
    envs = list(envelopes)
    if not envs:
        raise ValueError("at least one truth envelope is required")
    patient = envs[0].patient_ref
    if any(env.patient_ref != patient for env in envs):
        raise ValueError("cross-patient reconciliation rejected")
    facts = [fact for env in envs for fact in env.facts]
    ids = [f.fact_id for f in facts]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate fact_id across truth envelopes")
    return patient, facts


def reconcile_truth(envelopes: Iterable[TruthEnvelope]) -> ReconciliationResult:
    """Reconcile source assertions without inventing clinical truth.

    Order of authority:
    1. unsafe/unknown/ambiguous facts go to review, never quiet display;
    2. explicit source correction/supersession is honored when valid;
    3. cancelled assertions do not surface as current;
    4. final/corrected may replace preliminary for the same logical assertion;
    5. only explicitly governed state-snapshot fact types may use latest effective time;
    6. unresolved conflicting current assertions are routed to review.

    Confidence is never used to choose between conflicting clinical assertions.
    """

    patient, facts = _validate_patient(envelopes)
    result = ReconciliationResult(patient_ref=patient)
    by_id = {f.fact_id: f for f in facts}

    eligible: list[ClinicalFact] = []
    explicitly_superseded: set[str] = set()

    for fact in facts:
        if fact.status != FactStatus.CONFIRMED or not fact.provenance_complete:
            result.review.append(fact)
            continue
        if fact.assertion_stage == AssertionStage.CANCELLED:
            result.cancelled.append(fact)
            continue
        if fact.supersedes_fact_id:
            target = by_id.get(fact.supersedes_fact_id)
            if target is None:
                result.review.append(fact)
                result.issues.append(ReconciliationIssue(
                    code="broken-supersedes-reference",
                    fact_ids=(fact.fact_id,),
                    reason="source claims to supersede a fact that is not present in the reconciled evidence set",
                ))
                continue
            if target.reconciliation_key != fact.reconciliation_key:
                result.review.append(fact)
                result.issues.append(ReconciliationIssue(
                    code="critical-cross-concept-supersedes",
                    fact_ids=(fact.fact_id, target.fact_id),
                    reason="a fact attempted to supersede a different clinical concept",
                ))
                continue
            explicitly_superseded.add(target.fact_id)
        eligible.append(fact)

    remaining = []
    for fact in eligible:
        if fact.fact_id in explicitly_superseded:
            result.superseded.append(fact)
        else:
            remaining.append(fact)

    groups: dict[str, list[ClinicalFact]] = {}
    for fact in remaining:
        groups.setdefault(fact.reconciliation_key, []).append(fact)

    for key, group in groups.items():
        if len(group) == 1:
            result.current.append(group[0])
            continue

        # Corroborating sources that make the same assertion are useful evidence,
        # not a contradiction. Keep one representative while retaining all IDs.
        if _same_value(group):
            chosen = max(group, key=lambda f: (_STAGE_RANK[f.assertion_stage], _time(f)))
            result.current.append(chosen)
            result.corroborating_fact_ids[chosen.fact_id] = tuple(
                f.fact_id for f in group if f.fact_id != chosen.fact_id
            )
            continue

        # A final/corrected result may replace a preliminary assertion for the same
        # logical concept. Two conflicting finals/corrections still require review.
        chosen, older = _pick_by_stage(group)
        if chosen is not None:
            result.current.append(chosen)
            result.superseded.extend(older)
            continue

        fact_type = group[0].fact_type
        if fact_type in LATEST_STATE_FACT_TYPES:
            latest_time = max(_time(f) for f in group)
            latest = [f for f in group if _time(f) == latest_time]
            if len(latest) == 1:
                result.current.append(latest[0])
                result.superseded.extend(f for f in group if f.fact_id != latest[0].fact_id)
                continue
            if _same_value(latest):
                chosen = max(latest, key=lambda f: _STAGE_RANK[f.assertion_stage])
                result.current.append(chosen)
                result.superseded.extend(f for f in group if f.fact_id != chosen.fact_id)
                continue

        # Unresolved conflict: no winner is guessed. All competing current assertions
        # become visible review work and are removed from quiet/default display.
        result.review.extend(group)
        result.issues.append(ReconciliationIssue(
            code="critical-unresolved-current-conflict",
            fact_ids=tuple(f.fact_id for f in group),
            reason=f"conflicting current assertions for {key}; no governed rule can choose a winner",
        ))

    return result

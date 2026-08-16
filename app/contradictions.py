from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .clinical_truth import ClinicalFact


class ContradictionSeverity(str, Enum):
    INFO = "info"
    REVIEW = "review"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ContradictionRule:
    """Explicit, governed contradiction rule.

    Rules use canonical fact types/codes and must come from an approved rule registry.
    This module deliberately does not infer medical incompatibilities from free text.
    """

    rule_id: str
    left_fact_type: str
    right_fact_type: str
    left_code: str | None = None
    right_code: str | None = None
    severity: ContradictionSeverity = ContradictionSeverity.REVIEW
    rationale: str = ""


@dataclass(frozen=True)
class Contradiction:
    rule_id: str
    left_fact_id: str
    right_fact_id: str
    severity: ContradictionSeverity
    rationale: str


def _matches(fact: ClinicalFact, fact_type: str, code: str | None) -> bool:
    if fact.fact_type != fact_type:
        return False
    if code is None:
        return True
    return fact.code == code


def detect_contradictions(facts: list[ClinicalFact], rules: list[ContradictionRule]) -> list[Contradiction]:
    """Detect contradictions without silently deciding which source is 'true'."""

    out: list[Contradiction] = []
    for rule in rules:
        lefts = [f for f in facts if _matches(f, rule.left_fact_type, rule.left_code)]
        rights = [f for f in facts if _matches(f, rule.right_fact_type, rule.right_code)]
        for left in lefts:
            for right in rights:
                if left.patient_ref != right.patient_ref or left.fact_id == right.fact_id:
                    continue
                out.append(Contradiction(
                    rule_id=rule.rule_id,
                    left_fact_id=left.fact_id,
                    right_fact_id=right.fact_id,
                    severity=rule.severity,
                    rationale=rule.rationale,
                ))
    return out


def contradiction_groups(facts: list[ClinicalFact], contradictions: list[Contradiction]) -> dict[str, set[str]]:
    """Return explicit fact groups for UI/review; never choose a winner automatically."""

    groups: dict[str, set[str]] = {}
    for contradiction in contradictions:
        group = groups.setdefault(contradiction.rule_id, set())
        group.add(contradiction.left_fact_id)
        group.add(contradiction.right_fact_id)
    return groups

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PRF:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 1.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 1.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0

    def add(self, other: "PRF") -> "PRF":
        return PRF(self.tp + other.tp, self.fp + other.fp, self.fn + other.fn)

    def as_dict(self) -> dict[str, Any]:
        return {
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1": round(self.f1, 4),
        }


def _stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def field_items(field: str, value: Any) -> set[str]:
    if field in {"allergies"}:
        return {_stable(item) for item in (value or [])}
    if field in {"current_medications", "relevant_diagnoses", "open_followups"}:
        return {str(item) for item in (value or [])}
    if field in {"last_renal_function", "discharge"}:
        if value is None:
            return set()
        if field == "discharge" and value == {"status": "none", "date": None}:
            return set()
        return {_stable(value)}
    raise ValueError(f"unsupported benchmark field: {field}")


def score_items(predicted: set[str], gold: set[str]) -> PRF:
    return PRF(
        tp=len(predicted & gold),
        fp=len(predicted - gold),
        fn=len(gold - predicted),
    )


def score_case(pred: dict[str, Any], gold: dict[str, Any]) -> dict[str, Any]:
    fields = [
        "allergies",
        "current_medications",
        "relevant_diagnoses",
        "last_renal_function",
        "open_followups",
        "discharge",
    ]
    field_scores: dict[str, PRF] = {}
    silent_misses: list[str] = []
    unknown = set(pred.get("unknown_fields", []))

    for field in fields:
        p = field_items(field, pred.get(field))
        g = field_items(field, gold.get(field))
        field_scores[field] = score_items(p, g)
        if g and not p and field not in unknown:
            silent_misses.append(field)

    provenance_gold = gold.get("provenance", {})
    provenance_pred = pred.get("provenance", {})
    expected_sources = [(key, value) for key, value in provenance_gold.items() if value is not None]
    wrong_sources = [
        key for key, expected in expected_sources
        if provenance_pred.get(key) not in {None, expected}
    ]
    missing_sources = [
        key for key, expected in expected_sources
        if provenance_pred.get(key) is None
    ]

    total_predicted = sum(s.tp + s.fp for s in field_scores.values())
    total_fp = sum(s.fp for s in field_scores.values())

    return {
        "field_scores": field_scores,
        "silent_misses": silent_misses,
        "wrong_sources": wrong_sources,
        "missing_sources": missing_sources,
        "unsupported_claim_rate": total_fp / total_predicted if total_predicted else 0.0,
        "review_required": bool(pred.get("review_required") or pred.get("unknown_fields")),
    }


def aggregate_case_scores(scores: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [
        "allergies",
        "current_medications",
        "relevant_diagnoses",
        "last_renal_function",
        "open_followups",
        "discharge",
    ]
    totals = {field: PRF() for field in fields}
    silent = 0
    wrong_source = 0
    missing_source = 0
    unsupported_weighted_num = 0.0
    review_cases = 0

    for score in scores:
        for field in fields:
            totals[field] = totals[field].add(score["field_scores"][field])
        silent += len(score["silent_misses"])
        wrong_source += len(score["wrong_sources"])
        missing_source += len(score["missing_sources"])
        unsupported_weighted_num += score["unsupported_claim_rate"]
        review_cases += int(score["review_required"])

    micro = PRF()
    for total in totals.values():
        micro = micro.add(total)

    count = len(scores)
    return {
        "per_field": {field: totals[field].as_dict() for field in fields},
        "micro": micro.as_dict(),
        "critical_silent_field_misses": silent,
        "wrong_source_count": wrong_source,
        "missing_source_count": missing_source,
        "mean_unsupported_claim_rate": round(unsupported_weighted_num / count, 4) if count else 0.0,
        "review_case_rate": round(review_cases / count, 4) if count else 0.0,
    }

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any


TRUE = {"1", "true", "yes", "ja", "y"}
FALSE = {"0", "false", "no", "nein", "n"}


def _filled(row: dict[str, str]) -> bool:
    return bool((row.get("participant_code") or "").strip()) and any(
        (value or "").strip() for key, value in row.items() if key != "participant_code"
    )


def _bool(value: str, field: str) -> bool | None:
    v = (value or "").strip().lower()
    if not v:
        return None
    if v in TRUE:
        return True
    if v in FALSE:
        return False
    raise ValueError(f"{field} must be yes/no or true/false")


def _float(value: str, field: str, *, minimum: float = 0) -> float | None:
    if not (value or "").strip():
        return None
    parsed = float(value)
    if parsed < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return parsed


def _int(value: str, field: str, *, minimum: int = 0) -> int | None:
    if not (value or "").strip():
        return None
    parsed = int(value)
    if parsed < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return parsed


def _pct(values: list[bool]) -> float | None:
    return round(100 * sum(values) / len(values), 1) if values else None


def _median(values: list[float]) -> float | None:
    return round(statistics.median(values), 1) if values else None


def _mean(values: list[float]) -> float | None:
    return round(statistics.mean(values), 2) if values else None


def summarize(path: Path) -> dict[str, Any]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if _filled(row)]

    parsed = []
    seen_codes: set[str] = set()
    for row in rows:
        code = row["participant_code"].strip()
        if code in seen_codes:
            raise ValueError(f"duplicate participant_code: {code}")
        seen_codes.add(code)
        effort = _int(row.get("effort_1_5", ""), "effort_1_5", minimum=1)
        if effort is not None and effort > 5:
            raise ValueError("effort_1_5 must be <= 5")
        parsed.append({
            "participant_code": code,
            "total_seconds": _float(row.get("total_seconds", ""), "total_seconds"),
            "microbiology_correct": _bool(row.get("microbiology_correct", ""), "microbiology_correct"),
            "pending_status_correct": _bool(row.get("pending_status_correct", ""), "pending_status_correct"),
            "documented_therapy_correct": _bool(row.get("documented_therapy_correct", ""), "documented_therapy_correct"),
            "source_found": _bool(row.get("source_found", ""), "source_found"),
            "handover_seconds": _float(row.get("handover_seconds", ""), "handover_seconds"),
            "wrong_answers": _int(row.get("wrong_answers", ""), "wrong_answers"),
            "pending_items_missed": _int(row.get("pending_items_missed", ""), "pending_items_missed"),
            "source_opens": _int(row.get("source_opens", ""), "source_opens"),
            "corrections": _int(row.get("corrections", ""), "corrections"),
            "coaching_required": _bool(row.get("coaching_required", ""), "coaching_required"),
            "effort": effort,
            "would_use_tomorrow": _bool(row.get("would_use_tomorrow", ""), "would_use_tomorrow"),
        })

    bool_fields = [
        "microbiology_correct", "pending_status_correct", "documented_therapy_correct",
        "source_found", "coaching_required", "would_use_tomorrow",
    ]

    def bool_values(field: str) -> list[bool]:
        return [row[field] for row in parsed if row[field] is not None]

    def numeric(field: str) -> list[float]:
        return [float(row[field]) for row in parsed if row[field] is not None]

    safety_flags = []
    if any(value is False for value in bool_values("pending_status_correct")):
        safety_flags.append("at least one participant misunderstood pending/final status")
    if any(value is False for value in bool_values("documented_therapy_correct")):
        safety_flags.append("at least one participant failed the documented-therapy task")
    if sum(numeric("wrong_answers")) > 0:
        safety_flags.append("wrong answers were observed")
    if sum(numeric("pending_items_missed")) > 0:
        safety_flags.append("pending items were missed")

    metrics = {
        "participants": len(parsed),
        "median_total_seconds": _median(numeric("total_seconds")),
        "median_handover_seconds": _median(numeric("handover_seconds")),
        "microbiology_correct_pct": _pct(bool_values("microbiology_correct")),
        "pending_status_correct_pct": _pct(bool_values("pending_status_correct")),
        "documented_therapy_correct_pct": _pct(bool_values("documented_therapy_correct")),
        "source_found_pct": _pct(bool_values("source_found")),
        "coaching_required_pct": _pct(bool_values("coaching_required")),
        "would_use_tomorrow_pct": _pct(bool_values("would_use_tomorrow")),
        "mean_wrong_answers": _mean(numeric("wrong_answers")),
        "mean_pending_items_missed": _mean(numeric("pending_items_missed")),
        "mean_source_opens": _mean(numeric("source_opens")),
        "mean_corrections": _mean(numeric("corrections")),
        "median_effort_1_5": _median(numeric("effort")),
    }

    return {
        "study": "SJK synthetic CareOS workflow test",
        "data_policy": "aggregate structured test metrics only; free-text notes are intentionally not included in this report",
        "evidence_status": "insufficient_participants" if len(parsed) < 5 else "ready_for_human_review",
        "metrics": metrics,
        "safety_flags": safety_flags,
        "decision_rule": "No automatic go/no-go. Clinical/product leads review metrics, observed behavior and safety flags together.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = summarize(args.csv)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

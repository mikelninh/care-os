#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

STUDY_ID = "careos-sjk-synthetic-agent-ab"
CONDITIONS = {"careos", "careos-agent"}
HARD_SAFETY_FIELDS = ("pending_as_negative", "recommendation_misread", "agent_truth_confusion")


def _mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 2) if values else None


def _median(values: list[float]) -> float | None:
    return round(statistics.median(values), 2) if values else None


def _rate(values: list[bool]) -> float | None:
    return round(sum(bool(v) for v in values) / len(values), 4) if values else None


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("study") != STUDY_ID:
        raise ValueError(f"{path}: unexpected study id")
    if data.get("synthetic_only") is not True:
        raise ValueError(f"{path}: synthetic_only must be true")
    participant = str(data.get("participant_code") or "").strip()
    if not participant:
        raise ValueError(f"{path}: participant_code missing")
    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{path}: records missing")
    return data


def aggregate_payloads(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    by_participant: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    duplicates: list[str] = []

    for payload in payloads:
        participant = str(payload["participant_code"])
        for record in payload["records"]:
            condition = record.get("condition")
            if condition not in CONDITIONS:
                continue
            if condition in by_participant[participant]:
                duplicates.append(f"{participant}:{condition}")
                continue
            by_participant[participant][condition] = record

    complete = {p: rows for p, rows in by_participant.items() if CONDITIONS.issubset(rows)}
    incomplete = sorted(set(by_participant) - set(complete))

    condition_rows = {
        condition: [rows[condition] for rows in complete.values()]
        for condition in sorted(CONDITIONS)
    }

    paired_time_delta = [
        float(rows["careos-agent"]["task_seconds"]) - float(rows["careos"]["task_seconds"])
        for rows in complete.values()
    ]
    paired_source_delta = [
        int(rows["careos-agent"]["source_opens"]) - int(rows["careos"]["source_opens"])
        for rows in complete.values()
    ]
    verification_decay_delta = [
        int(bool(rows["careos-agent"]["accepted_without_source_check"]))
        - int(bool(rows["careos"]["accepted_without_source_check"]))
        for rows in complete.values()
    ]

    def safety_stop(row: dict[str, Any]) -> bool:
        return any(bool(row.get(field)) for field in HARD_SAFETY_FIELDS)

    condition_summary: dict[str, Any] = {}
    for condition, rows in condition_rows.items():
        times = [float(r["task_seconds"]) for r in rows]
        condition_summary[condition] = {
            "n": len(rows),
            "task_seconds_mean": _mean(times),
            "task_seconds_median": _median(times),
            "wrong_answers_total": sum(int(r["wrong_answers"]) for r in rows),
            "missed_pending_items_total": sum(int(r["missed_pending_items"]) for r in rows),
            "source_opens_mean": _mean([float(r["source_opens"]) for r in rows]),
            "corrections_total": sum(int(r["corrections"]) for r in rows),
            "accepted_without_source_check_rate": _rate([bool(r["accepted_without_source_check"]) for r in rows]),
            "pending_as_negative_count": sum(bool(r.get("pending_as_negative")) for r in rows),
            "recommendation_misread_count": sum(bool(r.get("recommendation_misread")) for r in rows),
            "agent_truth_confusion_count": sum(bool(r.get("agent_truth_confusion")) for r in rows),
            "hard_safety_stop_count": sum(safety_stop(r) for r in rows),
            "effort_mean": _mean([float(r["effort"]) for r in rows]),
            "would_use_tomorrow_rate": _rate([bool(r["would_use_tomorrow"]) for r in rows]),
        }

    agent_safety_stops = condition_summary["careos-agent"]["hard_safety_stop_count"]
    safety_gate_pass = agent_safety_stops == 0
    verification_gate_pass = sum(1 for x in verification_decay_delta if x > 0) == 0
    paired_speed_signal = _median(paired_time_delta)
    speed_improved = paired_speed_signal is not None and paired_speed_signal < 0

    return {
        "schema_version": "1.0",
        "study": STUDY_ID,
        "analysis": "paired-formative-usability",
        "synthetic_only": True,
        "complete_pairs": len(complete),
        "incomplete_participants": incomplete,
        "duplicate_condition_records": sorted(duplicates),
        "conditions": condition_summary,
        "paired": {
            "agent_minus_control_task_seconds_mean": _mean(paired_time_delta),
            "agent_minus_control_task_seconds_median": paired_speed_signal,
            "agent_minus_control_source_opens_mean": _mean([float(x) for x in paired_source_delta]),
            "verification_decay_positive_pairs": sum(1 for x in verification_decay_delta if x > 0),
            "verification_decay_zero_pairs": sum(1 for x in verification_decay_delta if x == 0),
            "verification_decay_negative_pairs": sum(1 for x in verification_decay_delta if x < 0),
        },
        "gates": {
            "agent_hard_safety_gate_pass": safety_gate_pass,
            "verification_decay_gate_pass": verification_gate_pass,
            "speed_signal_improved": speed_improved,
            "formative_success_signal": safety_gate_pass and verification_gate_pass and speed_improved,
        },
        "claim_boundary": (
            "Formative usability evidence on synthetic cases only. This report does not establish clinical efficacy, "
            "patient-safety validation, production performance or statistical generalizability."
        ),
    }


def to_markdown(report: dict[str, Any]) -> str:
    c = report["conditions"]
    p = report["paired"]
    g = report["gates"]
    yes = lambda value: "PASS" if value else "NOT PASS"
    return f"""# CareOS × Recare formative usability report

**Complete paired sessions:** {report['complete_pairs']}  
**Data:** synthetic cases only  
**Analysis:** paired formative usability; not clinical validation

## Primary signal

| Metric | CareOS | CareOS + agent |
|---|---:|---:|
| Median task time | {c['careos']['task_seconds_median']} s | {c['careos-agent']['task_seconds_median']} s |
| Mean task time | {c['careos']['task_seconds_mean']} s | {c['careos-agent']['task_seconds_mean']} s |
| Wrong answers | {c['careos']['wrong_answers_total']} | {c['careos-agent']['wrong_answers_total']} |
| Missed pending items | {c['careos']['missed_pending_items_total']} | {c['careos-agent']['missed_pending_items_total']} |
| Hard safety stops | {c['careos']['hard_safety_stop_count']} | {c['careos-agent']['hard_safety_stop_count']} |
| Mean source opens | {c['careos']['source_opens_mean']} | {c['careos-agent']['source_opens_mean']} |
| Mean effort (1–5) | {c['careos']['effort_mean']} | {c['careos-agent']['effort_mean']} |
| Would use tomorrow | {c['careos']['would_use_tomorrow_rate']} | {c['careos-agent']['would_use_tomorrow_rate']} |

## Paired deltas

- Agent − control median task time: **{p['agent_minus_control_task_seconds_median']} s**
- Agent − control mean task time: **{p['agent_minus_control_task_seconds_mean']} s**
- Agent − control mean source opens: **{p['agent_minus_control_source_opens_mean']}**
- Pairs with worse verification-decay indicator: **{p['verification_decay_positive_pairs']}**

## Gates

- Hard safety gate: **{yes(g['agent_hard_safety_gate_pass'])}**
- Verification-decay gate: **{yes(g['verification_decay_gate_pass'])}**
- Speed signal: **{yes(g['speed_signal_improved'])}**
- Combined formative success signal: **{yes(g['formative_success_signal'])}**

> {report['claim_boundary']}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate local-only CareOS synthetic clinician A/B exports.")
    parser.add_argument("inputs", nargs="+", type=Path, help="careos-ab-*.json files")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--md-out", type=Path, default=None)
    args = parser.parse_args()

    report = aggregate_payloads([load_payload(path) for path in args.inputs])
    rendered_json = json.dumps(report, indent=2, ensure_ascii=False)
    rendered_md = to_markdown(report)

    if args.json_out:
        args.json_out.write_text(rendered_json + "\n", encoding="utf-8")
    else:
        print(rendered_json)
    if args.md_out:
        args.md_out.write_text(rendered_md, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

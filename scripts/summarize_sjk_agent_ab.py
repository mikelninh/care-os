from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from app.agent_study import StudyObservation, summarize_paired_study


BOOL_FIELDS = {
    "accepted_without_source_check",
    "pending_as_negative",
    "recommendation_misread",
    "agent_truth_confusion",
    "would_use_tomorrow",
}
INT_FIELDS = {
    "order_position",
    "wrong_answers",
    "missed_pending_items",
    "source_opens",
    "corrections",
    "effort",
}
FLOAT_FIELDS = {"task_seconds"}
REQUIRED_FIELDS = {
    "participant_code",
    "condition",
    "case_id",
    "order_position",
    "task_seconds",
    "wrong_answers",
    "missed_pending_items",
    "source_opens",
    "corrections",
    "accepted_without_source_check",
    "pending_as_negative",
    "recommendation_misread",
    "agent_truth_confusion",
    "effort",
    "would_use_tomorrow",
}


def _bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "ja"}:
        return True
    if normalized in {"false", "0", "no", "nein"}:
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def read_observations(paths: list[Path]) -> list[StudyObservation]:
    rows: list[StudyObservation] = []
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            missing = REQUIRED_FIELDS - fields
            if missing:
                raise ValueError(f"{path}: missing required fields: {', '.join(sorted(missing))}")
            for line_number, raw in enumerate(reader, start=2):
                try:
                    payload = {key: raw.get(key, "") for key in REQUIRED_FIELDS}
                    for key in BOOL_FIELDS:
                        payload[key] = _bool(str(payload[key]))
                    for key in INT_FIELDS:
                        payload[key] = int(str(payload[key]).strip())
                    for key in FLOAT_FIELDS:
                        payload[key] = float(str(payload[key]).strip())
                    rows.append(StudyObservation(**payload))
                except Exception as exc:
                    raise ValueError(f"{path}:{line_number}: invalid study row: {exc}") from exc
    return rows


def summarize(paths: list[Path]) -> dict:
    observations = read_observations(paths)
    report = summarize_paired_study(observations)
    report["input_files"] = len(paths)
    report["input_rows"] = len(observations)
    report["study"] = "careos-sjk-synthetic-agent-ab"
    report["synthetic_only"] = True
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize locally exported CareOS synthetic clinician A/B CSV files.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = summarize(args.inputs)
    rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

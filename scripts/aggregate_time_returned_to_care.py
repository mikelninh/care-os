from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.time_returned_to_care import WorkflowObservation, build_time_back_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate pseudonymous paired Time Returned to Care workflow observations.")
    parser.add_argument("input", help="JSON file containing a list of WorkflowObservation objects or {'observations': [...]}.")
    parser.add_argument("--minimum-pairs", type=int, default=5)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = raw["observations"] if isinstance(raw, dict) else raw
    observations = [WorkflowObservation.model_validate(row) for row in rows]
    report = build_time_back_report(observations, minimum_pairs=args.minimum_pairs)

    print("CareOS · Time Returned to Care")
    print(f"observations: {len(report.observations)} · complete pairs: {len(report.pairs)}")
    for aggregate in report.aggregates:
        label = "PUBLISHABLE DIRECTIONAL WORKFLOW RESULT" if aggregate.result_publishable else "DIRECTIONAL / INSUFFICIENT OR SAFETY-BLOCKED"
        print(
            f"{aggregate.role.value}: n={aggregate.pair_count} · median returned={aggregate.median_minutes_returned:.2f} min · "
            f"safety stops={aggregate.total_careos_safety_stops} · verification decay pairs={aggregate.verification_decay_pairs} · {label}"
        )

    if args.json_out:
        Path(args.json_out).write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

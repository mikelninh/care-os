import json
from pathlib import Path

from app.time_returned_to_care import WorkflowObservation, build_time_back_report


FIXTURE = Path(__file__).parent / "fixtures" / "time_back_study_v2_dry_run.json"


def test_study_v2_dry_run_export_validates_and_preserves_counterbalance():
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert raw["schema"] == "careos-time-returned-to-care-v2"
    assert raw["synthetic_only"] is True

    observations = [WorkflowObservation.model_validate(row) for row in raw["observations"]]
    report = build_time_back_report(observations, minimum_pairs=2)

    assert len(report.pairs) == 2
    aggregate = report.aggregates[0]
    assert aggregate.baseline_first_pairs == 1
    assert aggregate.careos_first_pairs == 1
    assert aggregate.order_balance_ok is True
    assert aggregate.total_careos_safety_stops == 0
    assert aggregate.result_publishable is True

    p01 = next(pair for pair in report.pairs if pair.participant_code == "DRY-P01")
    p02 = next(pair for pair in report.pairs if pair.participant_code == "DRY-P02")
    assert (p01.baseline_case_variant, p01.careos_case_variant) == ("A", "B")
    assert (p02.baseline_case_variant, p02.careos_case_variant) == ("B", "A")

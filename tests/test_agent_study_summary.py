from pathlib import Path

import pytest

from app.agent_study import assignment_for
from scripts.summarize_sjk_agent_ab import summarize


HEADER = "participant_code,role_band,sequence,condition,case_id,order_position,task_seconds,wrong_answers,missed_pending_items,source_opens,corrections,accepted_without_source_check,pending_as_negative,recommendation_misread,agent_truth_confusion,effort,would_use_tomorrow\n"


def _pair_rows(code: str, *, agent_unverified=False, agent_pending_negative=False):
    rows = []
    for round_ in assignment_for(code)["rounds"]:
        is_agent = round_["condition"] == "careos-agent"
        rows.append(
            ",".join(
                [
                    code,
                    "facharzt",
                    str(assignment_for(code)["sequence"]),
                    round_["condition"],
                    round_["case_id"],
                    str(round_["order_position"]),
                    "70" if is_agent else "100",
                    "0",
                    "0",
                    "1" if is_agent else "2",
                    "0",
                    "true" if is_agent and agent_unverified else "false",
                    "true" if is_agent and agent_pending_negative else "false",
                    "false",
                    "false",
                    "2",
                    "true",
                ]
            )
        )
    return rows


def _write(path: Path, rows: list[str]) -> Path:
    path.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_multiple_local_exports_can_be_aggregated_as_paired_evidence(tmp_path):
    files = []
    for i in range(5):
        files.append(_write(tmp_path / f"p{i}.csv", _pair_rows(f"P{i}", agent_unverified=i < 2)))
    report = summarize(files)
    assert report["complete_pairs"] == 5
    assert report["verification_decay"] == 0.4
    assert report["paired_agent_minus_control"]["median_task_seconds"] == -30.0
    assert report["evidence_status"] == "ready-for-clinician-review"
    assert report["input_files"] == 5
    assert report["input_rows"] == 10


def test_safety_event_overrides_speed_gain(tmp_path):
    files = []
    for i in range(5):
        files.append(_write(tmp_path / f"p{i}.csv", _pair_rows(f"P{i}", agent_pending_negative=i == 0)))
    report = summarize(files)
    assert report["evidence_status"] == "safety-stop"
    assert report["paired_agent_minus_control"]["median_task_seconds"] == -30.0
    assert any(x["event"] == "pending-as-negative" for x in report["hard_stop_events"])


def test_missing_required_field_is_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("participant_code,condition\nP01,careos\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required fields"):
        summarize([path])

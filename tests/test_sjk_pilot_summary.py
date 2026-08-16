from pathlib import Path

import pytest

from scripts.summarize_sjk_pilot import summarize


HEADER = "participant_code,role_band,device_browser,total_seconds,microbiology_correct,pending_status_correct,documented_therapy_correct,source_found,handover_seconds,wrong_answers,pending_items_missed,source_opens,corrections,coaching_required,effort_1_5,would_use_tomorrow,notes_no_patient_data\n"


def _write(tmp_path: Path, rows: list[str]) -> Path:
    path = tmp_path / "results.csv"
    path.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_summary_aggregates_without_returning_free_text(tmp_path):
    rows = [
        "P01,assistenz,Chrome,90,yes,yes,yes,yes,20,0,0,2,0,no,2,yes,ignore this",
        "P02,facharzt,Safari,110,yes,yes,yes,yes,25,0,0,1,1,no,2,yes,also ignored",
        "P03,assistenz,Edge,100,yes,yes,yes,yes,22,0,0,2,0,no,3,yes,ignored",
        "P04,oberarzt,Chrome,130,yes,yes,yes,yes,30,0,0,2,0,no,2,yes,ignored",
        "P05,facharzt,Edge,105,yes,yes,yes,yes,24,0,0,1,0,no,2,yes,ignored",
    ]
    report = summarize(_write(tmp_path, rows))
    assert report["evidence_status"] == "ready_for_human_review"
    assert report["metrics"]["participants"] == 5
    assert report["metrics"]["pending_status_correct_pct"] == 100.0
    assert report["metrics"]["would_use_tomorrow_pct"] == 100.0
    assert "notes" not in str(report).lower()


def test_summary_surfaces_safety_flags_instead_of_auto_go(tmp_path):
    rows = [
        "P01,assistenz,Chrome,90,yes,no,yes,yes,20,1,1,2,0,no,2,yes,",
        "P02,facharzt,Chrome,90,yes,yes,yes,yes,20,0,0,2,0,no,2,yes,",
        "P03,facharzt,Chrome,90,yes,yes,yes,yes,20,0,0,2,0,no,2,yes,",
        "P04,facharzt,Chrome,90,yes,yes,yes,yes,20,0,0,2,0,no,2,yes,",
        "P05,facharzt,Chrome,90,yes,yes,yes,yes,20,0,0,2,0,no,2,yes,",
    ]
    report = summarize(_write(tmp_path, rows))
    assert report["safety_flags"]
    assert "No automatic go/no-go" in report["decision_rule"]


def test_summary_requires_unique_participant_codes(tmp_path):
    rows = [
        "P01,a,Chrome,90,yes,yes,yes,yes,20,0,0,1,0,no,2,yes,",
        "P01,b,Chrome,95,yes,yes,yes,yes,20,0,0,1,0,no,2,yes,",
    ]
    with pytest.raises(ValueError, match="duplicate participant_code"):
        summarize(_write(tmp_path, rows))


def test_less_than_five_is_not_enough_for_decision_review(tmp_path):
    rows = ["P01,a,Chrome,90,yes,yes,yes,yes,20,0,0,1,0,no,2,yes,"]
    report = summarize(_write(tmp_path, rows))
    assert report["evidence_status"] == "insufficient_participants"

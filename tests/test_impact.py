import pytest
from app.impact import score_pilot_task, aggregate_results


def test_score_includes_speed_and_burden_signals():
    r = score_pilot_task("allergy", 12, 45, clicks=4, searches=1, calls=0, corrections=0, effort=1)
    assert r["saved_minutes"] == 11.25
    assert r["clicks"] == 4
    assert r["effort"] == 1


def test_no_negative_savings_claim():
    r = score_pilot_task("slow", 1, 120, effort=5)
    assert r["saved_minutes"] == 0
    assert r["reduction_percent"] == 0


def test_failed_fast_task_never_counts_as_time_saved():
    r = score_pilot_task("wrong-but-fast", 10, 10, success=False)
    assert r["gross_saved_minutes"] > 9
    assert r["saved_minutes"] == 0
    assert r["reduction_percent"] == 0


def test_effort_range_is_enforced():
    with pytest.raises(ValueError):
        score_pilot_task("x", 5, 30, effort=6)


def test_aggregate_uses_medians_and_quality_signals():
    rows = [score_pilot_task("a", 10, 60, calls=0, corrections=0, effort=1),score_pilot_task("b", 5, 30, calls=1, corrections=1, effort=3),score_pilot_task("c", 8, 90, calls=0, corrections=0, effort=2)]
    a = aggregate_results(rows)
    assert a["tasks"] == 3
    assert a["median_seconds"] == 60
    assert a["calls"] == 1
    assert a["corrections"] == 1
    assert a["median_effort"] == 2


def test_aggregate_recomputes_and_ignores_forged_saved_minutes():
    forged = {
        "task_id":"a", "baseline_minutes":10, "actual_seconds":60,
        "clicks":0, "searches":0, "calls":0, "corrections":0,
        "effort":1, "success":True, "saved_minutes":999999,
    }
    a = aggregate_results([forged])
    assert a["total_saved_minutes"] == 9.0


def test_aggregate_failed_tasks_are_never_credited():
    rows = [
        score_pilot_task("success", 10, 60, success=True),
        score_pilot_task("failed", 10, 10, success=False),
    ]
    a = aggregate_results(rows)
    assert a["completed"] == 1
    assert a["total_saved_minutes"] == 9.0
    assert a["failed_tasks_credited_minutes"] == 0.0


def test_impact_inputs_are_bounded():
    with pytest.raises(ValueError):
        score_pilot_task("x", 241, 10)
    with pytest.raises(ValueError):
        score_pilot_task("x", 10, 14401)
    with pytest.raises(ValueError):
        aggregate_results([{"task_id":"x","baseline_minutes":999999,"actual_seconds":0}])

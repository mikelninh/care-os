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

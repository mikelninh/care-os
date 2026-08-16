from datetime import datetime, timedelta, timezone

from app.source_state import SourceAvailability, SourceState, source_result


def test_unavailable_source_never_becomes_empty_clinical_success():
    state = SourceState(source_id="lis", availability=SourceAvailability.UNAVAILABLE, detail="timeout")
    result = source_result(state=state, items=[])
    assert result["availability"] == "unavailable"
    assert result["count"] is None
    assert result["absence_claim_allowed"] is False
    assert result["warning"]


def test_stale_source_is_visible_and_cannot_assert_absence():
    now = datetime.now(timezone.utc)
    state = SourceState(
        source_id="kis",
        availability=SourceAvailability.CURRENT,
        last_success_at=now - timedelta(minutes=20),
        observed_at=now,
        max_age_seconds=300,
    )
    result = source_result(state=state, items=[])
    assert result["availability"] == "stale"
    assert result["count"] == 0
    assert result["absence_claim_allowed"] is False


def test_current_source_can_report_empty_result_without_transport_ambiguity():
    now = datetime.now(timezone.utc)
    state = SourceState(
        source_id="fhir",
        availability=SourceAvailability.CURRENT,
        last_success_at=now,
        observed_at=now,
        max_age_seconds=300,
    )
    result = source_result(state=state, items=[])
    assert result["availability"] == "current"
    assert result["count"] == 0
    assert result["absence_claim_allowed"] is True

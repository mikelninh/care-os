from datetime import datetime, timedelta, timezone

import pytest

from app.patient_view import (
    PatientFacingItem,
    PatientItemState,
    ProxyGrant,
    default_teach_back,
    synthetic_patient_view,
)


def test_pending_and_preliminary_patient_items_keep_uncertainty_visible():
    view = synthetic_patient_view()
    assert view.pending
    assert all(item.requires_attention for item in view.pending)
    assert all(item.next_step for item in view.pending)
    assert any(item.state == PatientItemState.PRELIMINARY for item in view.changed)


def test_patient_view_keeps_original_source_wording_next_to_plain_language():
    view = synthetic_patient_view()
    item = view.happened[0]
    assert item.original_text
    assert item.plain_language
    assert item.source_ref
    assert item.original_text != item.plain_language


def test_unavailable_item_cannot_look_reassuring_without_next_step():
    with pytest.raises(ValueError, match="what happens next"):
        PatientFacingItem(
            item_id="x",
            category="lab",
            original_text="Quelle nicht verfügbar",
            original_language="de",
            plain_language="The source is unavailable.",
            state=PatientItemState.UNAVAILABLE,
            source_ref="lis:x",
            source_label="Synthetic LIS",
            requires_attention=True,
        )


def test_proxy_access_is_a_dedicated_revocable_grant():
    active = ProxyGrant(
        grant_id="g1",
        patient_ref="p1",
        proxy_ref="family-1",
        scopes=("patient-summary", "appointments"),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    revoked = active.model_copy(update={"revoked": True})
    assert active.active() is True
    assert revoked.active() is False


def test_teach_back_checks_pending_medication_and_follow_up_understanding():
    checks = default_teach_back(synthetic_patient_view())
    assert {check.id for check in checks} == {"pending", "medication", "follow-up"}
    assert all(check.expected_concept for check in checks)

import pytest

from app.global_interop import (
    ClinicalState,
    GlobalPortabilityEnvelope,
    IssuerEvidence,
    PortableClinicalItem,
    TrustState,
    synthetic_cross_border_envelope,
)


def test_cross_border_envelope_preserves_pending_and_conflict_states():
    env = synthetic_cross_border_envelope(target_country="VN", presentation_language="vi")
    states = {item.item_id: item.clinical_state for item in env.items}
    assert states["micro-1"] == ClinicalState.PENDING
    assert states["allergy-1"] == ClinicalState.CONTRADICTORY
    assert env.policy["clinical_state_must_survive_mapping"] is True


def test_translation_never_replaces_original_clinical_text():
    env = synthetic_cross_border_envelope(target_country="DK", presentation_language="en")
    allergy = next(item for item in env.items if item.item_id == "allergy-1")
    assert allergy.original_language == "de"
    assert "Urtikaria" in allergy.original_text
    assert allergy.presentation[0].language == "en"
    assert allergy.presentation[0].text != allergy.original_text
    assert env.policy["original_clinical_text_preserved"] is True


def test_unverified_issuer_is_explicit_in_prototype():
    env = synthetic_cross_border_envelope()
    assert env.issuer.trust_state == TrustState.UNVERIFIED
    assert env.ips_conformance == "not-validated"
    assert env.policy["unverified_issuer_must_be_visible"] is True


def test_safety_sensitive_state_cannot_be_marked_no_review():
    with pytest.raises(ValueError):
        PortableClinicalItem(
            item_id="x",
            category="lab",
            original_text="pending",
            original_language="en",
            clinical_state=ClinicalState.PENDING,
            source_ref="LAB:x",
            source_organisation="demo",
            requires_review=False,
        )


def test_country_and_language_are_orthogonal():
    env = synthetic_cross_border_envelope(target_country="DK", presentation_language="vi")
    assert env.origin_country == "DE"
    assert env.target_country == "DK"
    assert env.presentation_language == "vi"


def test_envelope_round_trip_keeps_safety_meaning():
    env = synthetic_cross_border_envelope(target_country="VN", presentation_language="vi")
    restored = GlobalPortabilityEnvelope.model_validate_json(env.model_dump_json())
    before = [(x.item_id, x.clinical_state, x.requires_review, x.original_text) for x in env.items]
    after = [(x.item_id, x.clinical_state, x.requires_review, x.original_text) for x in restored.items]
    assert after == before

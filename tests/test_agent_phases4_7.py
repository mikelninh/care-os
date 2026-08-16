import pytest

from app.agent_assistance import AssistanceDraft, validate_read_only_assistance
from app.agent_modes import AgentOperatingMode, assert_agent_mode_allowed
from app.agent_sandbox import SandboxProfile, sjk_deidentified_target_profile
from app.agent_shadow import ShadowComparison, evaluate_shadow
from app.agent_study import StudyObservation, summarize_paired_study


def test_paired_study_exposes_verification_decay_and_never_auto_passes():
    report = summarize_paired_study([
        StudyObservation(participant_code="p1", condition="careos", task_seconds=100, source_opens=2, effort=3),
        StudyObservation(participant_code="p1", condition="careos-agent", task_seconds=60, source_opens=0, accepted_without_source_check=True, effort=2),
    ])
    assert report["agent"]["median_task_seconds"] < report["control"]["median_task_seconds"]
    assert report["verification_decay"] > 0
    assert report["automatic_pass"] is False


def test_sjk_sandbox_contract_is_deidentified_read_only_and_no_egress():
    profile = sjk_deidentified_target_profile()
    assert profile.identifiable_phi is False
    assert profile.read_only is True
    assert profile.external_egress is False
    with pytest.raises(ValueError):
        SandboxProfile(profile_id="bad", provider="x", identifiable_phi=True, identity_shape="x", audit_shape="x")


def test_live_shadow_and_read_only_modes_are_locked_today():
    assert assert_agent_mode_allowed(AgentOperatingMode.SYNTHETIC) == AgentOperatingMode.SYNTHETIC
    assert assert_agent_mode_allowed(AgentOperatingMode.DEIDENTIFIED_SANDBOX) == AgentOperatingMode.DEIDENTIFIED_SANDBOX
    with pytest.raises(RuntimeError):
        assert_agent_mode_allowed(AgentOperatingMode.SHADOW_LIVE)
    with pytest.raises(RuntimeError):
        assert_agent_mode_allowed(AgentOperatingMode.READ_ONLY_LIVE)
    with pytest.raises(RuntimeError):
        assert_agent_mode_allowed(AgentOperatingMode.CONSEQUENTIAL)


def test_shadow_mode_has_no_operational_effect_and_surfaces_discrepancies():
    report = evaluate_shadow(ShadowComparison(case_id="c1", agent_items={"micro", "med"}, clinician_items={"micro", "med", "pending"}))
    assert report["missed_items"] == ["pending"]
    assert report["unsafe_effect"] is False


def test_read_only_assistance_requires_sources_review_and_no_actions():
    good = validate_read_only_assistance(AssistanceDraft(patient_ref="p1", task="morning review", text="draft", source_refs=["src-1"]))
    assert good.review_required is True
    with pytest.raises(ValueError):
        validate_read_only_assistance(AssistanceDraft(patient_ref="p1", task="x", text="draft", source_refs=["src"], can_send=True))
    with pytest.raises(ValueError):
        validate_read_only_assistance(AssistanceDraft(patient_ref="p1", task="x", text="draft", source_refs=[]))

from app.time_returned_to_care import (
    StakeholderRole,
    TimeUnit,
    WorkflowImpactMeasurement,
    evaluate_workflow_impact,
    synthetic_inspiration_cases,
)


def test_time_saving_never_overrides_safety_stop():
    measurement = WorkflowImpactMeasurement(
        workflow_id="unsafe-fast",
        role=StakeholderRole.PHYSICIAN,
        unit=TimeUnit.SHIFT,
        before_minutes=90,
        after_minutes=20,
        missed_pending_items=1,
    )
    result = evaluate_workflow_impact(measurement)
    assert result.time_target_met is True
    assert result.safety_gate_met is False
    assert result.passes is False


def test_verification_decay_blocks_pilot_pass_even_with_time_target():
    measurement = WorkflowImpactMeasurement(
        workflow_id="verification-decay",
        role=StakeholderRole.NURSE,
        unit=TimeUnit.SHIFT,
        before_minutes=60,
        after_minutes=35,
        verification_decay_events=1,
    )
    result = evaluate_workflow_impact(measurement)
    assert result.time_target_met is True
    assert result.verification_gate_met is False
    assert result.passes is False


def test_clean_targeted_workflow_can_pass():
    measurement = WorkflowImpactMeasurement(
        workflow_id="clean",
        role=StakeholderRole.SOCIAL_DISCHARGE,
        unit=TimeUnit.CASE,
        before_minutes=60,
        after_minutes=30,
    )
    result = evaluate_workflow_impact(measurement)
    assert result.passes is True
    assert result.minutes_returned == 30
    assert result.relative_time_reduction == 0.5


def test_synthetic_cases_are_explicitly_identifiable_as_synthetic():
    cases = synthetic_inspiration_cases()
    assert cases
    assert all(case.workflow_id.startswith("synthetic-") for case in cases)

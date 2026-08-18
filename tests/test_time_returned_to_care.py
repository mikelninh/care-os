import pytest

from app.time_returned_to_care import (
    SafetyStop,
    StakeholderRole,
    StudyCondition,
    TimeUnit,
    WorkflowImpactMeasurement,
    WorkflowObservation,
    build_time_back_report,
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


def observation(
    *,
    participant="P01",
    condition=StudyCondition.BASELINE,
    seconds=3600,
    source_opens=4,
    accepted=0,
    missed=0,
    stops=(),
    order_index=None,
    case_variant=None,
):
    digits = "".join(ch for ch in participant if ch.isdigit())
    participant_number = int(digits or "1")
    baseline_first = participant_number % 2 == 1
    if order_index is None:
        order_index = 1 if (condition == StudyCondition.BASELINE) == baseline_first else 2
    if case_variant is None:
        case_variant = "A" if order_index == 1 else "B"
    return WorkflowObservation(
        participant_code=participant,
        workflow_id="physician-morning-review",
        case_variant=case_variant,
        role=StakeholderRole.PHYSICIAN,
        condition=condition,
        order_index=order_index,
        task_seconds=seconds,
        systems_opened=5 if condition == StudyCondition.BASELINE else 1,
        searches=8 if condition == StudyCondition.BASELINE else 2,
        context_switches=12 if condition == StudyCondition.BASELINE else 3,
        copy_paste_actions=5 if condition == StudyCondition.BASELINE else 0,
        clarification_contacts=1 if condition == StudyCondition.BASELINE else 0,
        wrong_answers=0,
        missed_pending_items=missed,
        source_opens=source_opens,
        corrections=0,
        accepted_without_source_check=accepted,
        cognitive_effort=4 if condition == StudyCondition.BASELINE else 2,
        safety_stops=stops,
    )


def test_paired_report_requires_five_safe_counterbalanced_pairs_before_highlighting_result():
    observations = []
    for index in range(5):
        participant = f"P{index + 1:02d}"
        observations.append(observation(participant=participant, condition=StudyCondition.BASELINE, seconds=3600))
        observations.append(observation(participant=participant, condition=StudyCondition.CAREOS, seconds=2100, source_opens=2))
    report = build_time_back_report(observations)
    assert len(report.pairs) == 5
    aggregate = report.aggregates[0]
    assert aggregate.median_minutes_returned == 25
    assert aggregate.total_careos_safety_stops == 0
    assert aggregate.baseline_first_pairs == 3
    assert aggregate.careos_first_pairs == 2
    assert aggregate.order_balance_ok is True
    assert aggregate.result_publishable is True
    assert aggregate.directional_only is False


def test_verification_collapse_is_derived_as_safety_stop():
    report = build_time_back_report(
        [
            observation(condition=StudyCondition.BASELINE, source_opens=3, accepted=0),
            observation(condition=StudyCondition.CAREOS, seconds=1800, source_opens=0, accepted=1),
        ],
        minimum_pairs=1,
    )
    pair = report.pairs[0]
    assert SafetyStop.VERIFICATION_COLLAPSE in pair.careos_safety_stops
    assert pair.passes_safety_gate is False
    assert report.aggregates[0].result_publishable is False


def test_more_missed_pending_items_blocks_pair_even_when_fast():
    report = build_time_back_report(
        [
            observation(condition=StudyCondition.BASELINE, missed=0),
            observation(condition=StudyCondition.CAREOS, seconds=1200, missed=1),
        ],
        minimum_pairs=1,
    )
    assert SafetyStop.MISSED_PENDING in report.pairs[0].careos_safety_stops
    assert report.aggregates[0].result_publishable is False


def test_pair_rejects_same_case_variant_to_reduce_learning_bias():
    with pytest.raises(ValueError, match="different matched synthetic case variants"):
        build_time_back_report(
            [
                observation(condition=StudyCondition.BASELINE, case_variant="A", order_index=1),
                observation(condition=StudyCondition.CAREOS, case_variant="A", order_index=2),
            ],
            minimum_pairs=1,
        )


def test_pair_rejects_invalid_counterbalance_order():
    with pytest.raises(ValueError, match="distinct order_index values 1 and 2"):
        build_time_back_report(
            [
                observation(condition=StudyCondition.BASELINE, case_variant="A", order_index=1),
                observation(condition=StudyCondition.CAREOS, case_variant="B", order_index=1),
            ],
            minimum_pairs=1,
        )


def test_single_order_direction_never_becomes_publishable_directional_result():
    observations = []
    for index in range(5):
        participant = f"X{index + 1:02d}"
        observations.append(
            observation(
                participant=participant,
                condition=StudyCondition.BASELINE,
                seconds=3600,
                order_index=1,
                case_variant="A",
            )
        )
        observations.append(
            observation(
                participant=participant,
                condition=StudyCondition.CAREOS,
                seconds=2100,
                source_opens=2,
                order_index=2,
                case_variant="B",
            )
        )
    aggregate = build_time_back_report(observations).aggregates[0]
    assert aggregate.order_balance_ok is False
    assert aggregate.result_publishable is False
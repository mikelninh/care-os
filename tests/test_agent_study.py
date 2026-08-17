from app.agent_study import StudyObservation, assignment_for, summarize_paired_study


def obs(code: str, condition: str, case_id: str, order: int, **updates):
    base = dict(
        participant_code=code,
        condition=condition,
        case_id=case_id,
        order_position=order,
        task_seconds=90,
        wrong_answers=0,
        missed_pending_items=0,
        source_opens=2,
        corrections=0,
        accepted_without_source_check=False,
        pending_as_negative=False,
        recommendation_misread=False,
        agent_truth_confusion=False,
        effort=2,
        would_use_tomorrow=True,
    )
    base.update(updates)
    return StudyObservation(**base)


def test_assignment_is_deterministic_and_balances_two_cases_two_conditions():
    a = assignment_for("P01")
    b = assignment_for("P01")
    assert a == b
    assert {row["condition"] for row in a["rounds"]} == {"careos", "careos-agent"}
    assert {row["case_id"] for row in a["rounds"]} == {"case-a", "case-b"}
    assert {row["order_position"] for row in a["rounds"]} == {1, 2}


def test_incomplete_participant_never_changes_agent_effect():
    rows = [
        obs("P01", "careos", "case-a", 1, task_seconds=100),
        obs("P01", "careos-agent", "case-b", 2, task_seconds=70),
        obs("P02", "careos-agent", "case-a", 1, task_seconds=1, wrong_answers=20),
    ]
    report = summarize_paired_study(rows)
    assert report["complete_pairs"] == 1
    assert report["incomplete_participants"] == 1
    assert report["agent"]["median_task_seconds"] == 70
    assert report["agent"]["wrong_answers"] == 0
    assert report["paired_agent_minus_control"]["median_task_seconds"] == -30


def test_duplicate_condition_or_case_is_rejected_instead_of_double_weighted():
    rows = [
        obs("P01", "careos", "case-a", 1),
        obs("P01", "careos", "case-b", 2),
    ]
    try:
        summarize_paired_study(rows)
    except ValueError as exc:
        assert "invalid paired study rows" in str(exc)
    else:
        raise AssertionError("invalid pair should be rejected")


def test_verification_decay_is_agent_minus_control_unverified_acceptance():
    rows = []
    for i in range(5):
        code = f"P{i}"
        rows.extend([
            obs(code, "careos", "case-a", 1, accepted_without_source_check=False),
            obs(code, "careos-agent", "case-b", 2, accepted_without_source_check=(i < 2)),
        ])
    report = summarize_paired_study(rows)
    assert report["complete_pairs"] == 5
    assert report["verification_decay"] == 0.4
    assert report["evidence_status"] == "ready-for-clinician-review"
    assert report["automatic_pass"] is False


def test_any_pending_as_negative_or_recommendation_confusion_triggers_safety_stop():
    rows = []
    for i in range(5):
        code = f"P{i}"
        rows.extend([
            obs(code, "careos", "case-a", 1),
            obs(
                code,
                "careos-agent",
                "case-b",
                2,
                pending_as_negative=(i == 0),
                recommendation_misread=(i == 1),
                agent_truth_confusion=(i == 2),
            ),
        ])
    report = summarize_paired_study(rows)
    assert report["evidence_status"] == "safety-stop"
    assert {event["event"] for event in report["hard_stop_events"]} == {
        "pending-as-negative",
        "documented-treatment-read-as-recommendation",
        "agent-draft-confused-with-source-truth",
    }

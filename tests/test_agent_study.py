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


def assigned_pair(code: str, *, control_updates=None, agent_updates=None):
    control_updates = control_updates or {}
    agent_updates = agent_updates or {}
    rows = []
    for round_ in assignment_for(code)["rounds"]:
        updates = control_updates if round_["condition"] == "careos" else agent_updates
        rows.append(obs(code, round_["condition"], round_["case_id"], round_["order_position"], **updates))
    return rows


def test_assignment_is_deterministic_and_balances_two_cases_two_conditions():
    a = assignment_for("P01")
    b = assignment_for("P01")
    assert a == b
    assert {row["condition"] for row in a["rounds"]} == {"careos", "careos-agent"}
    assert {row["case_id"] for row in a["rounds"]} == {"case-a", "case-b"}
    assert {row["order_position"] for row in a["rounds"]} == {1, 2}


def test_incomplete_participant_never_changes_agent_effect():
    rows = assigned_pair("P01", control_updates={"task_seconds": 100}, agent_updates={"task_seconds": 70})
    lone = assignment_for("P02")["rounds"][0]
    rows.append(obs("P02", lone["condition"], lone["case_id"], lone["order_position"], task_seconds=1, wrong_answers=20))
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


def test_complete_pair_must_match_counterbalanced_assignment():
    rows = [
        obs("P01", "careos", "case-a", 1),
        obs("P01", "careos-agent", "case-b", 2),
    ]
    try:
        summarize_paired_study(rows)
    except ValueError as exc:
        assert "counterbalanced assignment" in str(exc)
    else:
        raise AssertionError("assignment mismatch should be rejected")


def test_more_than_two_rows_for_participant_is_rejected():
    rows = assigned_pair("P01")
    rows.append(rows[0].model_copy())
    try:
        summarize_paired_study(rows)
    except ValueError as exc:
        assert "duplicate or extra study rows" in str(exc)
    else:
        raise AssertionError("extra study row should be rejected")


def test_verification_decay_is_agent_minus_control_unverified_acceptance():
    rows = []
    for i in range(5):
        rows.extend(
            assigned_pair(
                f"P{i}",
                control_updates={"accepted_without_source_check": False},
                agent_updates={"accepted_without_source_check": i < 2},
            )
        )
    report = summarize_paired_study(rows)
    assert report["complete_pairs"] == 5
    assert report["verification_decay"] == 0.4
    assert report["evidence_status"] == "ready-for-clinician-review"
    assert report["automatic_pass"] is False


def test_any_pending_as_negative_or_recommendation_confusion_triggers_safety_stop():
    rows = []
    for i in range(5):
        rows.extend(
            assigned_pair(
                f"P{i}",
                agent_updates={
                    "pending_as_negative": i == 0,
                    "recommendation_misread": i == 1,
                    "agent_truth_confusion": i == 2,
                },
            )
        )
    report = summarize_paired_study(rows)
    assert report["evidence_status"] == "safety-stop"
    assert {event["event"] for event in report["hard_stop_events"]} == {
        "pending-as-negative",
        "documented-treatment-read-as-recommendation",
        "agent-draft-confused-with-source-truth",
    }

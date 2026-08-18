from scripts.aggregate_recare_study import aggregate_payloads, to_markdown


def payload(code, control_seconds, agent_seconds, *, agent_safety=False, agent_unverified=False):
    common = {
        "wrong_answers": 0,
        "missed_pending_items": 0,
        "source_opens": 2,
        "corrections": 0,
        "accepted_without_source_check": False,
        "pending_as_negative": False,
        "recommendation_misread": False,
        "agent_truth_confusion": False,
        "effort": 2,
        "would_use_tomorrow": True,
    }
    control = {**common, "participant_code": code, "role_band": "facharzt", "sequence": 1,
               "condition": "careos", "case_id": "case-a", "order_position": 1, "task_seconds": control_seconds}
    agent = {**common, "participant_code": code, "role_band": "facharzt", "sequence": 1,
             "condition": "careos-agent", "case_id": "case-b", "order_position": 2, "task_seconds": agent_seconds,
             "accepted_without_source_check": agent_unverified, "agent_truth_confusion": agent_safety}
    return {"schema_version": "1.0", "study": "careos-sjk-synthetic-agent-ab", "synthetic_only": True,
            "participant_code": code, "sequence": 1, "records": [control, agent]}


def test_aggregator_reports_paired_speed_and_safe_success_signal():
    report = aggregate_payloads([
        payload("P01", 100, 70),
        payload("P02", 120, 80),
    ])
    assert report["complete_pairs"] == 2
    assert report["paired"]["agent_minus_control_task_seconds_mean"] == -35.0
    assert report["paired"]["agent_minus_control_task_seconds_median"] == -35.0
    assert report["gates"]["agent_hard_safety_gate_pass"] is True
    assert report["gates"]["verification_decay_gate_pass"] is True
    assert report["gates"]["speed_signal_improved"] is True
    assert report["gates"]["formative_success_signal"] is True


def test_any_agent_safety_stop_overrides_speed_signal():
    report = aggregate_payloads([
        payload("P01", 100, 50, agent_safety=True),
        payload("P02", 120, 60),
    ])
    assert report["gates"]["speed_signal_improved"] is True
    assert report["conditions"]["careos-agent"]["hard_safety_stop_count"] == 1
    assert report["gates"]["agent_hard_safety_gate_pass"] is False
    assert report["gates"]["formative_success_signal"] is False


def test_verification_decay_overrides_speed_signal():
    report = aggregate_payloads([
        payload("P01", 100, 50, agent_unverified=True),
        payload("P02", 120, 60),
    ])
    assert report["paired"]["verification_decay_positive_pairs"] == 1
    assert report["gates"]["verification_decay_gate_pass"] is False
    assert report["gates"]["formative_success_signal"] is False


def test_markdown_preserves_claim_boundary():
    report = aggregate_payloads([payload("P01", 100, 80)])
    md = to_markdown(report)
    assert "Formative usability" in md
    assert "not clinical validation" in md
    assert "Combined formative success signal" in md

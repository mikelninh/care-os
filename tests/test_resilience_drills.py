import pytest

from app.resilience_drills import (
    DrillScenario,
    QueuedWork,
    run_drill,
    standard_recovery_drill,
)
from app.resilience_mode import Capability, OperatingMode


def test_standard_recovery_never_asserts_absence_or_write_until_reconciled():
    report = standard_recovery_drill()
    assert [step.decision.mode for step in report.steps] == [
        OperatingMode.OFFLINE,
        OperatingMode.RECOVERY,
        OperatingMode.NORMAL,
    ]
    assert report.absence_claim_ever_allowed_while_stale_or_offline is False
    assert report.hidden_write_ever_allowed is False
    assert report.normal_restored is True


def test_model_outage_preserves_source_context_but_removes_ai_assist():
    report = run_drill([DrillScenario.MODEL_LOSS])
    decision = report.steps[0].decision
    assert decision.mode == OperatingMode.NORMAL
    assert Capability.SOURCE_READ in decision.allowed
    assert Capability.SOURCE_VERIFY in decision.allowed
    assert Capability.MODEL_ASSIST in decision.denied
    assert Capability.WRITE in decision.denied


def test_identity_or_audit_outage_disables_agent_and_consequential_capabilities():
    for scenario in (DrillScenario.IDENTITY_LOSS, DrillScenario.AUDIT_LOSS):
        decision = run_drill([scenario]).steps[0].decision
        assert decision.mode == OperatingMode.DEGRADED
        assert Capability.MODEL_ASSIST in decision.denied
        assert Capability.DRAFT in decision.denied
        assert Capability.WRITE in decision.denied


def test_source_loss_copy_tells_user_what_failed_what_works_and_what_to_do():
    step = run_drill([DrillScenario.SOURCE_LOSS]).steps[0]
    assert step.guidance.what_failed
    assert step.guidance.what_still_works
    assert step.guidance.what_to_do
    assert "absent" in step.guidance.what_to_do.lower()
    assert step.audit_event["audit_level"] == "safety"


def test_nonconsequential_queue_is_explicit_and_idempotent():
    report = run_drill([DrillScenario.NETWORK_LOSS])
    queued = report.steps[0].queued_work
    assert queued
    assert queued[0].consequential is False
    assert queued[0].idempotency_key


def test_consequential_work_cannot_be_hidden_in_resilience_queue():
    with pytest.raises(ValueError, match="may not hide consequential"):
        QueuedWork(idempotency_key="x", task_type="clinical-write", consequential=True)

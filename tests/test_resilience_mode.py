from app.resilience_mode import Capability, DependencyState, OperatingMode, decide_resilience

# CI verification marker: run the current master-foundation invariants on a PR merge ref.


def state(**overrides):
    base = dict(
        source_truth_available=True,
        source_current=True,
        identity_available=True,
        audit_available=True,
        model_available=True,
        network_available=True,
        legacy_fallback_available=True,
        recovery_reconciled=True,
    )
    base.update(overrides)
    return DependencyState(**base)


def test_normal_mode_still_does_not_grant_write_or_external_send():
    decision = decide_resilience(state())
    assert decision.mode == OperatingMode.NORMAL
    assert Capability.SOURCE_READ in decision.allowed
    assert Capability.ASSERT_ABSENCE in decision.allowed
    assert Capability.WRITE in decision.denied
    assert Capability.EXTERNAL_SEND in decision.denied


def test_stale_source_disables_absence_and_write():
    decision = decide_resilience(state(source_current=False))
    assert decision.mode == OperatingMode.DEGRADED
    assert Capability.SHOW_LAST_KNOWN in decision.allowed
    assert Capability.ASSERT_ABSENCE in decision.denied
    assert Capability.WRITE in decision.denied


def test_offline_keeps_legacy_fallback_and_blocks_model_and_absence():
    decision = decide_resilience(state(network_available=False, source_truth_available=False))
    assert decision.mode == OperatingMode.OFFLINE
    assert Capability.LEGACY_FALLBACK in decision.allowed
    assert Capability.MODEL_ASSIST in decision.denied
    assert Capability.ASSERT_ABSENCE in decision.denied


def test_identity_failure_disables_agent_and_consequential_capabilities():
    decision = decide_resilience(state(identity_available=False))
    assert decision.mode == OperatingMode.DEGRADED
    assert Capability.SOURCE_READ in decision.allowed
    assert Capability.MODEL_ASSIST in decision.denied
    assert Capability.DRAFT in decision.denied
    assert Capability.WRITE in decision.denied


def test_recovery_requires_reconciliation_before_normal_mode():
    decision = decide_resilience(state(recovery_reconciled=False))
    assert decision.mode == OperatingMode.RECOVERY
    assert Capability.SOURCE_VERIFY in decision.allowed
    assert Capability.DRAFT in decision.denied
    assert Capability.WRITE in decision.denied

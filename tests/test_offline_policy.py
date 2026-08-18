from app.offline_policy import ConnectivityState, OperationKind, decide_offline_operation


def test_degraded_context_can_be_read_but_never_supports_absence_claims():
    decision = decide_offline_operation(
        connectivity=ConnectivityState.DEGRADED,
        operation=OperationKind.READ_CONTEXT,
        source_set_complete=False,
    )
    assert decision.allowed is True
    assert decision.may_assert_absence is False
    assert "show unavailable sources" in decision.restrictions


def test_degraded_generic_write_is_blocked():
    decision = decide_offline_operation(
        connectivity=ConnectivityState.DEGRADED,
        operation=OperationKind.WRITE,
    )
    assert decision.allowed is False
    assert decision.may_assert_absence is False


def test_offline_agent_tool_and_send_are_blocked():
    for operation in (OperationKind.AGENT_TOOL, OperationKind.EXTERNAL_SEND, OperationKind.WRITE, OperationKind.DRAFT):
        decision = decide_offline_operation(
            connectivity=ConnectivityState.OFFLINE,
            operation=operation,
        )
        assert decision.allowed is False


def test_approved_recent_cache_is_read_only_and_never_complete():
    decision = decide_offline_operation(
        connectivity=ConnectivityState.OFFLINE,
        operation=OperationKind.READ_CACHED_CONTEXT,
        cache_available=True,
        cache_age_seconds=60,
        approved_cache_max_age_seconds=300,
    )
    assert decision.allowed is True
    assert decision.may_assert_absence is False
    assert "read-only" in decision.restrictions
    assert "show last-refresh age prominently" in decision.restrictions


def test_stale_or_unbounded_cache_is_blocked():
    stale = decide_offline_operation(
        connectivity=ConnectivityState.OFFLINE,
        operation=OperationKind.READ_CACHED_CONTEXT,
        cache_available=True,
        cache_age_seconds=600,
        approved_cache_max_age_seconds=300,
    )
    unknown_age = decide_offline_operation(
        connectivity=ConnectivityState.OFFLINE,
        operation=OperationKind.READ_CACHED_CONTEXT,
        cache_available=True,
    )
    assert stale.allowed is False
    assert unknown_age.allowed is False

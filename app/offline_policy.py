from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ConnectivityState(str, Enum):
    ONLINE = "online"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class OperationKind(str, Enum):
    READ_CONTEXT = "read-context"
    READ_CACHED_CONTEXT = "read-cached-context"
    DRAFT = "draft"
    AGENT_TOOL = "agent-tool"
    WRITE = "write"
    EXTERNAL_SEND = "external-send"


class OfflineDecision(BaseModel):
    allowed: bool
    may_assert_absence: bool = False
    human_review_required: bool = True
    visible_state_required: bool = True
    reason: str
    restrictions: list[str] = Field(default_factory=list)


def decide_offline_operation(
    *,
    connectivity: ConnectivityState,
    operation: OperationKind,
    cache_available: bool = False,
    cache_age_seconds: int | None = None,
    approved_cache_max_age_seconds: int | None = None,
    source_set_complete: bool = True,
) -> OfflineDecision:
    """Fail-safe policy for network/source degradation.

    This is deliberately conservative. Workflow-specific offline writes may be designed
    later, but there is no platform-wide queued-write shortcut.
    """

    if connectivity == ConnectivityState.ONLINE:
        if operation in {OperationKind.WRITE, OperationKind.EXTERNAL_SEND, OperationKind.AGENT_TOOL}:
            return OfflineDecision(
                allowed=True,
                may_assert_absence=source_set_complete,
                human_review_required=True,
                reason="Online transport is available; normal capability/authorization policy still applies.",
                restrictions=["offline policy does not grant write/tool/send authority"],
            )
        return OfflineDecision(
            allowed=True,
            may_assert_absence=source_set_complete,
            human_review_required=(operation == OperationKind.DRAFT),
            reason="Online transport is available; source completeness still determines absence semantics.",
        )

    if connectivity == ConnectivityState.DEGRADED:
        if operation in {OperationKind.WRITE, OperationKind.EXTERNAL_SEND}:
            return OfflineDecision(
                allowed=False,
                may_assert_absence=False,
                reason="Degraded operation disables general consequential writes/sends until target/source state is explicitly re-established.",
                restrictions=["use existing authoritative hospital workflow", "no queued platform-wide write"],
            )
        if operation == OperationKind.AGENT_TOOL:
            return OfflineDecision(
                allowed=False,
                may_assert_absence=False,
                reason="Agent tools are disabled by the generic degraded-mode policy; a narrower tool-specific policy must re-admit them.",
            )
        if operation in {OperationKind.READ_CONTEXT, OperationKind.DRAFT}:
            return OfflineDecision(
                allowed=True,
                may_assert_absence=False,
                human_review_required=True,
                reason="Partial current context may remain useful, but unavailable dependencies make completeness unknown.",
                restrictions=["show unavailable sources", "suppress absence/negative conclusions", "suppress dependent agent claims"],
            )
        # cached read in degraded state follows the same cache rules as offline below

    if operation != OperationKind.READ_CACHED_CONTEXT:
        return OfflineDecision(
            allowed=False,
            may_assert_absence=False,
            reason="Offline mode permits no normal CareOS draft/tool/write/send operation; fall back to the authoritative local workflow.",
            restrictions=["legacy/source workflow remains fallback"],
        )

    if not cache_available:
        return OfflineDecision(
            allowed=False,
            may_assert_absence=False,
            reason="No approved local cache is available.",
        )

    if cache_age_seconds is None or approved_cache_max_age_seconds is None:
        return OfflineDecision(
            allowed=False,
            may_assert_absence=False,
            reason="Cached clinical context cannot be displayed without an explicit age and approved maximum-age policy.",
        )

    if cache_age_seconds > approved_cache_max_age_seconds:
        return OfflineDecision(
            allowed=False,
            may_assert_absence=False,
            reason="Cached clinical context is older than the approved offline display window.",
            restrictions=["use authoritative local source workflow"],
        )

    return OfflineDecision(
        allowed=True,
        may_assert_absence=False,
        human_review_required=True,
        reason="Approved last-known context may be displayed read-only while offline.",
        restrictions=[
            "show last-refresh age prominently",
            "read-only",
            "no absence/negative inference",
            "no agent tool execution",
            "no write/send",
        ],
    )

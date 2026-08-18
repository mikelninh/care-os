from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class OperatingMode(str, Enum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    RECOVERY = "recovery"


class Capability(str, Enum):
    SOURCE_READ = "source-read"
    SOURCE_VERIFY = "source-verify"
    SHOW_LAST_KNOWN = "show-last-known"
    ASSERT_ABSENCE = "assert-absence"
    MODEL_ASSIST = "model-assist"
    DRAFT = "draft"
    QUEUE_NONCONSEQUENTIAL = "queue-nonconsequential"
    WRITE = "write"
    EXTERNAL_SEND = "external-send"
    LEGACY_FALLBACK = "legacy-fallback"


class DependencyState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_truth_available: bool
    source_current: bool
    identity_available: bool
    audit_available: bool
    model_available: bool
    network_available: bool
    legacy_fallback_available: bool = True
    recovery_reconciled: bool = False


class ResilienceDecision(BaseModel):
    mode: OperatingMode
    allowed: set[Capability] = Field(default_factory=set)
    denied: set[Capability] = Field(default_factory=set)
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def never_allow_and_deny_same_capability(self) -> "ResilienceDecision":
        overlap = self.allowed & self.denied
        if overlap:
            raise ValueError(f"capabilities cannot be both allowed and denied: {sorted(overlap)}")
        return self


def decide_resilience(state: DependencyState) -> ResilienceDecision:
    all_capabilities = set(Capability)

    if not state.network_available or not state.source_truth_available:
        mode = OperatingMode.OFFLINE
        allowed = {Capability.SHOW_LAST_KNOWN}
        warnings = [
            "Source truth is unavailable. Last-known data, if shown, must remain visibly stale/unverified.",
            "Missing information must not be interpreted as clinical absence.",
        ]
        if state.legacy_fallback_available:
            allowed.add(Capability.LEGACY_FALLBACK)
        if state.identity_available and state.audit_available:
            allowed.add(Capability.QUEUE_NONCONSEQUENTIAL)
        denied = all_capabilities - allowed
        return ResilienceDecision(mode=mode, allowed=allowed, denied=denied, warnings=warnings)

    if not state.identity_available or not state.audit_available:
        mode = OperatingMode.DEGRADED
        allowed = {Capability.SOURCE_READ, Capability.SHOW_LAST_KNOWN}
        if state.legacy_fallback_available:
            allowed.add(Capability.LEGACY_FALLBACK)
        denied = all_capabilities - allowed
        reason = "identity" if not state.identity_available else "audit"
        return ResilienceDecision(
            mode=mode,
            allowed=allowed,
            denied=denied,
            warnings=[f"{reason} dependency unavailable; consequential/agent operations are disabled."],
        )

    if not state.source_current:
        mode = OperatingMode.DEGRADED
        allowed = {
            Capability.SOURCE_READ,
            Capability.SOURCE_VERIFY,
            Capability.SHOW_LAST_KNOWN,
            Capability.DRAFT,
            Capability.LEGACY_FALLBACK,
        }
        if state.model_available:
            allowed.add(Capability.MODEL_ASSIST)
        denied = all_capabilities - allowed
        return ResilienceDecision(
            mode=mode,
            allowed=allowed,
            denied=denied,
            warnings=["Source is stale; absence assertions, writes and external sends are disabled."],
        )

    if not state.recovery_reconciled:
        mode = OperatingMode.RECOVERY
        allowed = {
            Capability.SOURCE_READ,
            Capability.SOURCE_VERIFY,
            Capability.SHOW_LAST_KNOWN,
            Capability.LEGACY_FALLBACK,
        }
        denied = all_capabilities - allowed
        return ResilienceDecision(
            mode=mode,
            allowed=allowed,
            denied=denied,
            warnings=["Connectivity returned but missed versions/events are not reconciled yet; dependent actions remain blocked."],
        )

    mode = OperatingMode.NORMAL
    allowed = {
        Capability.SOURCE_READ,
        Capability.SOURCE_VERIFY,
        Capability.SHOW_LAST_KNOWN,
        Capability.ASSERT_ABSENCE,
        Capability.DRAFT,
        Capability.QUEUE_NONCONSEQUENTIAL,
        Capability.LEGACY_FALLBACK,
    }
    if state.model_available:
        allowed.add(Capability.MODEL_ASSIST)

    # Writes and external sends remain denied by this general resilience policy.
    # Those require separate workflow capability + human approval + deployment gates.
    denied = all_capabilities - allowed
    return ResilienceDecision(mode=mode, allowed=allowed, denied=denied)

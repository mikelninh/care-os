from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .audit import make_audit_event
from .resilience_mode import Capability, DependencyState, OperatingMode, ResilienceDecision, decide_resilience


class DrillScenario(str, Enum):
    NETWORK_LOSS = "network-loss"
    SOURCE_LOSS = "source-loss"
    STALE_SOURCE = "stale-source"
    IDENTITY_LOSS = "identity-loss"
    AUDIT_LOSS = "audit-loss"
    MODEL_LOSS = "model-loss"
    RECOVERY_PENDING = "recovery-pending"
    RECOVERY_COMPLETE = "recovery-complete"


class UserGuidance(BaseModel):
    headline: str
    what_failed: str
    what_still_works: str
    what_to_do: str


class QueuedWork(BaseModel):
    model_config = ConfigDict(extra="forbid")

    idempotency_key: str = Field(min_length=1)
    task_type: str = Field(min_length=1)
    consequential: bool = False

    @model_validator(mode="after")
    def never_queue_consequential_work(self) -> "QueuedWork":
        if self.consequential:
            raise ValueError("CareOS resilience queue may not hide consequential clinical work")
        return self


class DrillStep(BaseModel):
    scenario: DrillScenario
    decision: ResilienceDecision
    guidance: UserGuidance
    queued_work: tuple[QueuedWork, ...] = ()
    audit_event: dict


class ResilienceDrillReport(BaseModel):
    patient_ref: str
    steps: list[DrillStep]
    normal_restored: bool
    absence_claim_ever_allowed_while_stale_or_offline: bool
    hidden_write_ever_allowed: bool


def state_for_scenario(scenario: DrillScenario) -> DependencyState:
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
    if scenario == DrillScenario.NETWORK_LOSS:
        base.update(network_available=False, source_truth_available=False, recovery_reconciled=False)
    elif scenario == DrillScenario.SOURCE_LOSS:
        base.update(source_truth_available=False, recovery_reconciled=False)
    elif scenario == DrillScenario.STALE_SOURCE:
        base.update(source_current=False, recovery_reconciled=False)
    elif scenario == DrillScenario.IDENTITY_LOSS:
        base.update(identity_available=False)
    elif scenario == DrillScenario.AUDIT_LOSS:
        base.update(audit_available=False)
    elif scenario == DrillScenario.MODEL_LOSS:
        base.update(model_available=False)
    elif scenario == DrillScenario.RECOVERY_PENDING:
        base.update(recovery_reconciled=False)
    elif scenario == DrillScenario.RECOVERY_COMPLETE:
        pass
    return DependencyState(**base)


def guidance_for(scenario: DrillScenario, decision: ResilienceDecision) -> UserGuidance:
    if scenario in {DrillScenario.NETWORK_LOSS, DrillScenario.SOURCE_LOSS}:
        return UserGuidance(
            headline="Source connection unavailable",
            what_failed="Current source truth cannot be refreshed.",
            what_still_works="The legacy source remains the fallback. Last-known CareOS context may be shown only as visibly stale/unverified.",
            what_to_do="Use the legacy source for current clinical facts. Do not interpret missing CareOS items as absent.",
        )
    if scenario == DrillScenario.STALE_SOURCE:
        return UserGuidance(
            headline="Source data is stale",
            what_failed="CareOS has not confirmed a fresh source version within the expected window.",
            what_still_works="Existing context and direct source verification remain available where the source can be reached.",
            what_to_do="Verify important facts at source. CareOS disables absence assertions and consequential actions.",
        )
    if scenario == DrillScenario.IDENTITY_LOSS:
        return UserGuidance(
            headline="Identity service unavailable",
            what_failed="CareOS cannot establish the authority needed for agent or consequential operations.",
            what_still_works="Read-only source context may remain visible under the current trusted session boundary.",
            what_to_do="Continue through the legacy workflow; do not start a new agent/action session until identity is restored.",
        )
    if scenario == DrillScenario.AUDIT_LOSS:
        return UserGuidance(
            headline="Audit service unavailable",
            what_failed="CareOS cannot durably record consequential activity.",
            what_still_works="Read-only source context remains available.",
            what_to_do="CareOS disables agent/consequential operations until audit is restored.",
        )
    if scenario == DrillScenario.MODEL_LOSS:
        return UserGuidance(
            headline="AI assistance temporarily unavailable",
            what_failed="The reasoning/model service is unavailable.",
            what_still_works="Source-linked clinical context and verification continue without AI assistance.",
            what_to_do="Continue using direct context/source views. No clinical source access should depend on the model.",
        )
    if scenario == DrillScenario.RECOVERY_PENDING:
        return UserGuidance(
            headline="Connection restored — reconciling changes",
            what_failed="Nothing is assumed current until versions/events missed during the outage are reconciled.",
            what_still_works="Read and source verification are available while reconciliation runs.",
            what_to_do="Wait for reconciliation before relying on drafts or absence assertions; use source systems for urgent decisions.",
        )
    return UserGuidance(
        headline="CareOS current",
        what_failed="No active dependency failure detected by this drill.",
        what_still_works="Current source-linked context, verification and non-consequential drafting are available under normal policy.",
        what_to_do="Continue normally. Write/send authority still requires separate workflow policy and human approval.",
    )


def run_drill(
    scenarios: list[DrillScenario],
    *,
    patient_ref: str = "synthetic-patient-001",
) -> ResilienceDrillReport:
    steps: list[DrillStep] = []
    absence_while_unsafe = False
    hidden_write = False

    for index, scenario in enumerate(scenarios):
        state = state_for_scenario(scenario)
        decision = decide_resilience(state)
        if decision.mode in {OperatingMode.OFFLINE, OperatingMode.DEGRADED, OperatingMode.RECOVERY}:
            absence_while_unsafe = absence_while_unsafe or Capability.ASSERT_ABSENCE in decision.allowed
        hidden_write = hidden_write or Capability.WRITE in decision.allowed or Capability.EXTERNAL_SEND in decision.allowed

        queued: tuple[QueuedWork, ...] = ()
        if Capability.QUEUE_NONCONSEQUENTIAL in decision.allowed and decision.mode != OperatingMode.NORMAL:
            queued = (
                QueuedWork(
                    idempotency_key=f"{patient_ref}:{scenario.value}:{index}:telemetry",
                    task_type="non-clinical-operational-telemetry",
                ),
            )
        event = make_audit_event(
            actor_id="careos-resilience-drill",
            patient_id=patient_ref,
            action=f"resilience-{decision.mode.value}",
            resource_type="resilience-drill",
            resource_id=scenario.value,
            outcome="observed",
            audit_level="safety",
            reason_code=scenario.value,
        )
        steps.append(
            DrillStep(
                scenario=scenario,
                decision=decision,
                guidance=guidance_for(scenario, decision),
                queued_work=queued,
                audit_event=event,
            )
        )

    normal_restored = bool(steps and steps[-1].decision.mode == OperatingMode.NORMAL)
    return ResilienceDrillReport(
        patient_ref=patient_ref,
        steps=steps,
        normal_restored=normal_restored,
        absence_claim_ever_allowed_while_stale_or_offline=absence_while_unsafe,
        hidden_write_ever_allowed=hidden_write,
    )


def standard_recovery_drill() -> ResilienceDrillReport:
    return run_drill(
        [
            DrillScenario.NETWORK_LOSS,
            DrillScenario.RECOVERY_PENDING,
            DrillScenario.RECOVERY_COMPLETE,
        ]
    )

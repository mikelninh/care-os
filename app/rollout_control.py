from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .hospital_upgrade import UpgradePlan


class RolloutState(str, Enum):
    PROPOSED = "proposed"
    PREFLIGHT_PASSED = "preflight-passed"
    CONFORMANCE_PASSED = "conformance-passed"
    CANARY_RUNNING = "canary-running"
    PROMOTED = "promoted"
    ROLLED_BACK = "rolled-back"
    BLOCKED = "blocked"


class CanaryEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observations: int = Field(gt=0)
    source_availability_ok: bool
    source_freshness_ok: bool
    patient_identity_errors: int = Field(ge=0)
    connector_errors: int = Field(ge=0)
    incomplete_reads: int = Field(ge=0)
    unsupported_claims: int = Field(ge=0)
    safety_stop_events: int = Field(ge=0)
    operator_stop: bool = False
    new_write_authority_detected: bool = False

    @property
    def passes(self) -> bool:
        return all(
            (
                self.source_availability_ok,
                self.source_freshness_ok,
                self.patient_identity_errors == 0,
                self.connector_errors == 0,
                self.incomplete_reads == 0,
                self.unsupported_claims == 0,
                self.safety_stop_events == 0,
                not self.operator_stop,
                not self.new_write_authority_detected,
            )
        )


class RolloutRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hospital_id: str
    release_id: str = Field(min_length=1)
    previous_release_id: str = Field(min_length=1)
    state: RolloutState = RolloutState.PROPOSED
    upgrade_requires_shadow: bool
    preflight_evidence_ref: str | None = None
    conformance_evidence_ref: str | None = None
    canary_evidence: CanaryEvidence | None = None
    rollback_reason: str | None = None
    history: tuple[str, ...] = ()

    @model_validator(mode="after")
    def promoted_requires_complete_evidence(self) -> "RolloutRecord":
        if self.state == RolloutState.PROMOTED:
            if not self.preflight_evidence_ref or not self.conformance_evidence_ref:
                raise ValueError("promotion requires preflight and conformance evidence")
            if self.upgrade_requires_shadow and (not self.canary_evidence or not self.canary_evidence.passes):
                raise ValueError("upgrade requiring shadow revalidation needs passing canary evidence before promotion")
        return self


def begin_rollout(upgrade: UpgradePlan, *, release_id: str, previous_release_id: str) -> RolloutRecord:
    blocked = any(finding.severity == "block" for finding in upgrade.findings)
    return RolloutRecord(
        hospital_id=upgrade.hospital_id,
        release_id=release_id,
        previous_release_id=previous_release_id,
        state=RolloutState.BLOCKED if blocked else RolloutState.PROPOSED,
        upgrade_requires_shadow=upgrade.requires_shadow_revalidation,
        history=("upgrade-preflight-blocked",) if blocked else ("rollout-proposed",),
    )


def record_preflight(record: RolloutRecord, evidence_ref: str) -> RolloutRecord:
    if record.state == RolloutState.BLOCKED:
        return record
    if record.state != RolloutState.PROPOSED:
        raise ValueError(f"preflight evidence cannot be recorded from {record.state.value}")
    return record.model_copy(
        update={
            "state": RolloutState.PREFLIGHT_PASSED,
            "preflight_evidence_ref": evidence_ref,
            "history": record.history + (f"preflight:{evidence_ref}",),
        }
    )


def record_conformance(record: RolloutRecord, evidence_ref: str) -> RolloutRecord:
    if record.state != RolloutState.PREFLIGHT_PASSED:
        raise ValueError(f"conformance evidence cannot be recorded from {record.state.value}")
    return record.model_copy(
        update={
            "state": RolloutState.CONFORMANCE_PASSED,
            "conformance_evidence_ref": evidence_ref,
            "history": record.history + (f"conformance:{evidence_ref}",),
        }
    )


def start_canary(record: RolloutRecord) -> RolloutRecord:
    if record.state != RolloutState.CONFORMANCE_PASSED:
        raise ValueError(f"canary cannot start from {record.state.value}")
    return record.model_copy(
        update={
            "state": RolloutState.CANARY_RUNNING,
            "history": record.history + ("canary-started",),
        }
    )


def evaluate_canary(record: RolloutRecord, evidence: CanaryEvidence) -> RolloutRecord:
    if record.state != RolloutState.CANARY_RUNNING:
        raise ValueError(f"canary evidence cannot be applied from {record.state.value}")
    if evidence.passes:
        return record.model_copy(
            update={
                "canary_evidence": evidence,
                "history": record.history + ("canary-passed",),
            }
        )
    reasons = []
    if not evidence.source_availability_ok:
        reasons.append("source availability")
    if not evidence.source_freshness_ok:
        reasons.append("source freshness")
    for label, count in (
        ("patient identity error", evidence.patient_identity_errors),
        ("connector error", evidence.connector_errors),
        ("incomplete read", evidence.incomplete_reads),
        ("unsupported claim", evidence.unsupported_claims),
        ("safety-stop event", evidence.safety_stop_events),
    ):
        if count:
            reasons.append(f"{label}={count}")
    if evidence.operator_stop:
        reasons.append("operator stop")
    if evidence.new_write_authority_detected:
        reasons.append("new write authority")
    return rollback(record.model_copy(update={"canary_evidence": evidence}), reason="; ".join(reasons) or "canary failed")


def promote(record: RolloutRecord) -> RolloutRecord:
    if record.state not in {RolloutState.CONFORMANCE_PASSED, RolloutState.CANARY_RUNNING}:
        raise ValueError(f"rollout cannot promote from {record.state.value}")
    if record.upgrade_requires_shadow:
        if record.state != RolloutState.CANARY_RUNNING or not record.canary_evidence or not record.canary_evidence.passes:
            raise ValueError("shadow/canary evidence is required before this upgrade may be promoted")
    return RolloutRecord.model_validate(
        record.model_copy(
            update={
                "state": RolloutState.PROMOTED,
                "history": record.history + ("promoted",),
            }
        ).model_dump()
    )


def rollback(record: RolloutRecord, *, reason: str) -> RolloutRecord:
    if record.state == RolloutState.ROLLED_BACK:
        return record
    if record.state == RolloutState.PROMOTED:
        # Post-promotion rollback remains allowed and deliberately points to the last known good release.
        pass
    return record.model_copy(
        update={
            "state": RolloutState.ROLLED_BACK,
            "rollback_reason": reason,
            "history": record.history + (f"rollback:{reason}",),
        }
    )

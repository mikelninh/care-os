from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class StakeholderRole(str, Enum):
    PHYSICIAN = "physician"
    NURSE = "nurse"
    SOCIAL_DISCHARGE = "social-discharge"
    ADMIN_CODING = "admin-coding"
    HOSPITAL_IT = "hospital-it"


class TimeUnit(str, Enum):
    SHIFT = "shift"
    CASE = "case"
    WORKFLOW = "workflow"
    SITE_CHANGE = "site-change"


class ImpactTarget(BaseModel):
    role: StakeholderRole
    unit: TimeUnit
    pilot_minutes_returned: float = Field(ge=0)
    mature_minutes_returned: float = Field(ge=0)
    description: str


ROLE_TARGETS: tuple[ImpactTarget, ...] = (
    ImpactTarget(
        role=StakeholderRole.PHYSICIAN,
        unit=TimeUnit.SHIFT,
        pilot_minutes_returned=20,
        mature_minutes_returned=60,
        description="Targeted information-reconstruction/documentation workflows; product target, not current measured outcome.",
    ),
    ImpactTarget(
        role=StakeholderRole.NURSE,
        unit=TimeUnit.SHIFT,
        pilot_minutes_returned=15,
        mature_minutes_returned=45,
        description="Targeted handover/documentation/coordination workflows.",
    ),
    ImpactTarget(
        role=StakeholderRole.SOCIAL_DISCHARGE,
        unit=TimeUnit.CASE,
        pilot_minutes_returned=20,
        mature_minutes_returned=45,
        description="Eligible discharge/aftercare coordination cases.",
    ),
    ImpactTarget(
        role=StakeholderRole.ADMIN_CODING,
        unit=TimeUnit.WORKFLOW,
        pilot_minutes_returned=10,
        mature_minutes_returned=20,
        description="Evidence search/clarification workflow; percentage reduction should also be tracked.",
    ),
    ImpactTarget(
        role=StakeholderRole.HOSPITAL_IT,
        unit=TimeUnit.SITE_CHANGE,
        pilot_minutes_returned=120,
        mature_minutes_returned=480,
        description="Routine already-supported integration/version change compared with repeated manual discovery; validate per real site.",
    ),
)


class WorkflowImpactMeasurement(BaseModel):
    workflow_id: str
    role: StakeholderRole
    unit: TimeUnit
    before_minutes: float = Field(gt=0)
    after_minutes: float = Field(ge=0)
    wrong_patient_events: int = Field(default=0, ge=0)
    missed_pending_items: int = Field(default=0, ge=0)
    unsupported_claims: int = Field(default=0, ge=0)
    stale_state_confusions: int = Field(default=0, ge=0)
    unauthorised_actions: int = Field(default=0, ge=0)
    verification_decay_events: int = Field(default=0, ge=0)
    corrections: int = Field(default=0, ge=0)
    source_opens_before: int = Field(default=0, ge=0)
    source_opens_after: int = Field(default=0, ge=0)
    completed: bool = True

    @model_validator(mode="after")
    def after_cannot_exceed_impossible_bounds(self) -> "WorkflowImpactMeasurement":
        if self.after_minutes > self.before_minutes * 5:
            raise ValueError("after_minutes is implausibly high relative to the captured baseline")
        return self

    @property
    def minutes_returned(self) -> float:
        return self.before_minutes - self.after_minutes

    @property
    def relative_time_reduction(self) -> float:
        return self.minutes_returned / self.before_minutes

    @property
    def safety_stop_count(self) -> int:
        return sum(
            (
                self.wrong_patient_events,
                self.missed_pending_items,
                self.unsupported_claims,
                self.stale_state_confusions,
                self.unauthorised_actions,
            )
        )


class ImpactEvaluation(BaseModel):
    passes: bool
    time_target_met: bool
    safety_gate_met: bool
    verification_gate_met: bool
    minutes_returned: float
    relative_time_reduction: float
    reasons: list[str]


def target_for(role: StakeholderRole, unit: TimeUnit) -> ImpactTarget | None:
    return next((target for target in ROLE_TARGETS if target.role == role and target.unit == unit), None)


def evaluate_workflow_impact(measurement: WorkflowImpactMeasurement) -> ImpactEvaluation:
    target = target_for(measurement.role, measurement.unit)
    time_target_met = bool(target and measurement.minutes_returned >= target.pilot_minutes_returned)
    safety_gate_met = measurement.safety_stop_count == 0
    verification_gate_met = measurement.verification_decay_events == 0

    reasons: list[str] = []
    if not measurement.completed:
        reasons.append("workflow measurement is incomplete")
    if not target:
        reasons.append("no pilot target is registered for this role/unit")
    elif not time_target_met:
        reasons.append(
            f"returned {measurement.minutes_returned:.1f} min; pilot target is {target.pilot_minutes_returned:.1f} min/{target.unit.value}"
        )
    if not safety_gate_met:
        reasons.append(f"{measurement.safety_stop_count} safety-stop event(s) override any speed improvement")
    if not verification_gate_met:
        reasons.append("verification decay observed; easier UI must not reduce source checking in the evaluation phase")

    passes = measurement.completed and time_target_met and safety_gate_met and verification_gate_met
    if passes:
        reasons.append("pilot time target met without observed safety-stop or verification-decay events")

    return ImpactEvaluation(
        passes=passes,
        time_target_met=time_target_met,
        safety_gate_met=safety_gate_met,
        verification_gate_met=verification_gate_met,
        minutes_returned=measurement.minutes_returned,
        relative_time_reduction=measurement.relative_time_reduction,
        reasons=reasons,
    )


def synthetic_inspiration_cases() -> list[WorkflowImpactMeasurement]:
    """Illustrative hypotheses only — never report these as observed CareOS outcomes."""

    return [
        WorkflowImpactMeasurement(
            workflow_id="synthetic-physician-complex-morning-review",
            role=StakeholderRole.PHYSICIAN,
            unit=TimeUnit.SHIFT,
            before_minutes=75,
            after_minutes=48,
            source_opens_before=18,
            source_opens_after=8,
        ),
        WorkflowImpactMeasurement(
            workflow_id="synthetic-nurse-handover",
            role=StakeholderRole.NURSE,
            unit=TimeUnit.SHIFT,
            before_minutes=55,
            after_minutes=35,
            source_opens_before=10,
            source_opens_after=6,
        ),
        WorkflowImpactMeasurement(
            workflow_id="synthetic-aftercare-case",
            role=StakeholderRole.SOCIAL_DISCHARGE,
            unit=TimeUnit.CASE,
            before_minutes=60,
            after_minutes=30,
            source_opens_before=8,
            source_opens_after=3,
        ),
    ]

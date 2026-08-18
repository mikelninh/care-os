from __future__ import annotations

from collections import defaultdict
from enum import Enum
from statistics import median

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class StudyCondition(str, Enum):
    BASELINE = "baseline"
    CAREOS = "careos"


class SafetyStop(str, Enum):
    WRONG_PATIENT = "wrong-patient"
    MISSED_PENDING = "missed-pending"
    UNSUPPORTED_CLAIM = "unsupported-claim"
    STALE_AS_CURRENT = "stale-as-current"
    DRAFT_AS_RECOMMENDATION = "draft-as-recommendation"
    VERIFICATION_COLLAPSE = "verification-collapse"


class WorkflowObservation(BaseModel):
    """One bounded workflow observation with no names or free-text clinical data."""

    model_config = ConfigDict(extra="forbid")

    participant_code: str = Field(min_length=1)
    workflow_id: str = Field(min_length=1)
    case_variant: str = Field(min_length=1)
    role: StakeholderRole
    condition: StudyCondition
    order_index: int = Field(ge=1, le=2)
    task_seconds: int = Field(gt=0)
    systems_opened: int = Field(ge=0)
    searches: int = Field(ge=0)
    context_switches: int = Field(ge=0)
    copy_paste_actions: int = Field(ge=0)
    clarification_contacts: int = Field(ge=0)
    wrong_answers: int = Field(ge=0)
    missed_pending_items: int = Field(ge=0)
    source_opens: int = Field(ge=0)
    corrections: int = Field(ge=0)
    accepted_without_source_check: int = Field(ge=0)
    cognitive_effort: int = Field(ge=1, le=5)
    safety_stops: tuple[SafetyStop, ...] = ()
    friction_tags: tuple[str, ...] = ()


class PairedWorkflowResult(BaseModel):
    participant_code: str
    workflow_id: str
    role: StakeholderRole
    baseline_case_variant: str
    careos_case_variant: str
    baseline_order_index: int
    careos_order_index: int
    baseline_seconds: int
    careos_seconds: int
    seconds_returned: int
    minutes_returned: float
    baseline_source_opens: int
    careos_source_opens: int
    baseline_wrong_answers: int
    careos_wrong_answers: int
    baseline_missed_pending: int
    careos_missed_pending: int
    careos_safety_stops: tuple[SafetyStop, ...]
    passes_safety_gate: bool


class RoleAggregate(BaseModel):
    role: StakeholderRole
    pair_count: int
    median_minutes_returned: float
    median_seconds_baseline: float
    median_seconds_careos: float
    total_careos_safety_stops: int
    verification_decay_pairs: int
    baseline_first_pairs: int
    careos_first_pairs: int
    order_balance_ok: bool
    result_publishable: bool
    directional_only: bool


def pair_observations(observations: list[WorkflowObservation]) -> list[PairedWorkflowResult]:
    grouped: dict[tuple[str, str, StakeholderRole], dict[StudyCondition, WorkflowObservation]] = defaultdict(dict)
    for observation in observations:
        key = (observation.participant_code, observation.workflow_id, observation.role)
        if observation.condition in grouped[key]:
            raise ValueError(f"duplicate condition for pair: {key} / {observation.condition.value}")
        grouped[key][observation.condition] = observation

    pairs: list[PairedWorkflowResult] = []
    for (participant_code, workflow_id, role), conditions in grouped.items():
        if set(conditions) != {StudyCondition.BASELINE, StudyCondition.CAREOS}:
            continue
        baseline = conditions[StudyCondition.BASELINE]
        careos = conditions[StudyCondition.CAREOS]
        if {baseline.order_index, careos.order_index} != {1, 2}:
            raise ValueError(f"paired observations must use distinct order_index values 1 and 2: {(participant_code, workflow_id, role)}")
        if baseline.case_variant == careos.case_variant:
            raise ValueError(f"paired observations must use different matched synthetic case variants: {(participant_code, workflow_id, role)}")

        careos_stops = set(careos.safety_stops)
        if careos.missed_pending_items > baseline.missed_pending_items:
            careos_stops.add(SafetyStop.MISSED_PENDING)
        verification_decay = (
            baseline.source_opens > 0
            and careos.source_opens == 0
            and careos.accepted_without_source_check > baseline.accepted_without_source_check
        )
        if verification_decay:
            careos_stops.add(SafetyStop.VERIFICATION_COLLAPSE)
        seconds_returned = baseline.task_seconds - careos.task_seconds
        pairs.append(
            PairedWorkflowResult(
                participant_code=participant_code,
                workflow_id=workflow_id,
                role=role,
                baseline_case_variant=baseline.case_variant,
                careos_case_variant=careos.case_variant,
                baseline_order_index=baseline.order_index,
                careos_order_index=careos.order_index,
                baseline_seconds=baseline.task_seconds,
                careos_seconds=careos.task_seconds,
                seconds_returned=seconds_returned,
                minutes_returned=round(seconds_returned / 60.0, 2),
                baseline_source_opens=baseline.source_opens,
                careos_source_opens=careos.source_opens,
                baseline_wrong_answers=baseline.wrong_answers,
                careos_wrong_answers=careos.wrong_answers,
                baseline_missed_pending=baseline.missed_pending_items,
                careos_missed_pending=careos.missed_pending_items,
                careos_safety_stops=tuple(sorted(careos_stops, key=lambda item: item.value)),
                passes_safety_gate=not careos_stops,
            )
        )
    return sorted(pairs, key=lambda pair: (pair.role.value, pair.participant_code, pair.workflow_id))


def aggregate_by_role(pairs: list[PairedWorkflowResult], *, minimum_pairs: int = 5) -> list[RoleAggregate]:
    grouped: dict[StakeholderRole, list[PairedWorkflowResult]] = defaultdict(list)
    for pair in pairs:
        grouped[pair.role].append(pair)

    aggregates: list[RoleAggregate] = []
    for role, role_pairs in sorted(grouped.items(), key=lambda item: item[0].value):
        safety_stops = sum(len(pair.careos_safety_stops) for pair in role_pairs)
        verification_decay_pairs = sum(
            1 for pair in role_pairs if SafetyStop.VERIFICATION_COLLAPSE in pair.careos_safety_stops
        )
        baseline_first_pairs = sum(1 for pair in role_pairs if pair.baseline_order_index == 1)
        careos_first_pairs = sum(1 for pair in role_pairs if pair.careos_order_index == 1)
        enough_pairs = len(role_pairs) >= minimum_pairs
        safe = safety_stops == 0
        order_balance_ok = baseline_first_pairs > 0 and careos_first_pairs > 0
        publishable = enough_pairs and safe and order_balance_ok
        aggregates.append(
            RoleAggregate(
                role=role,
                pair_count=len(role_pairs),
                median_minutes_returned=round(median(pair.minutes_returned for pair in role_pairs), 2),
                median_seconds_baseline=median(pair.baseline_seconds for pair in role_pairs),
                median_seconds_careos=median(pair.careos_seconds for pair in role_pairs),
                total_careos_safety_stops=safety_stops,
                verification_decay_pairs=verification_decay_pairs,
                baseline_first_pairs=baseline_first_pairs,
                careos_first_pairs=careos_first_pairs,
                order_balance_ok=order_balance_ok,
                result_publishable=publishable,
                directional_only=not publishable,
            )
        )
    return aggregates


class TimeBackReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observations: list[WorkflowObservation]
    pairs: list[PairedWorkflowResult]
    aggregates: list[RoleAggregate]
    clinical_efficacy_claim: bool = False

    @model_validator(mode="after")
    def never_claim_clinical_efficacy(self) -> "TimeBackReport":
        if self.clinical_efficacy_claim:
            raise ValueError("Time Returned to Care is workflow evidence, not clinical efficacy validation")
        return self


def build_time_back_report(observations: list[WorkflowObservation], *, minimum_pairs: int = 5) -> TimeBackReport:
    pairs = pair_observations(observations)
    return TimeBackReport(
        observations=observations,
        pairs=pairs,
        aggregates=aggregate_by_role(pairs, minimum_pairs=minimum_pairs),
    )
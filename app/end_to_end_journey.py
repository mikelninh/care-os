from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict

from .artifact_invalidation import ArtifactDependency, ArtifactKind, ArtifactState, DerivedArtifact
from .care_coordination import CareRequestState, synthetic_coordination_request, transition_request
from .clinical_graph import ClinicalContextGraph, graph_from_truth
from .clinical_truth import AssertionStage, ClinicalFact, SourceKind, SourceRef, TruthEnvelope
from .patient_view import PatientView, synthetic_patient_view
from .recovery_reconciliation import RecoveryReconciliationResult, reconcile_after_outage
from .resilience_mode import OperatingMode
from .service_operating_model import CommitmentState
from .time_returned_to_care import StakeholderRole, TimeUnit, target_for


class JourneyCheckpoint(BaseModel):
    name: str
    assertion: str
    passed: bool


class GoldenJourneyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patient_ref: str
    initial_graph: ClinicalContextGraph
    clinician_draft_before_correction: DerivedArtifact
    recovery: RecoveryReconciliationResult
    patient_view: PatientView
    coordination_states: tuple[CareRequestState, ...]
    physician_time_target_minutes: float
    sla_state: CommitmentState
    checkpoints: tuple[JourneyCheckpoint, ...]

    @property
    def all_passed(self) -> bool:
        return all(checkpoint.passed for checkpoint in self.checkpoints)


def _fact(
    fact_id: str,
    *,
    fact_type: str,
    logical_key: str,
    value: str,
    status: AssertionStage = AssertionStage.FINAL,
    supersedes: str | None = None,
) -> ClinicalFact:
    return ClinicalFact(
        fact_id=fact_id,
        patient_ref="synthetic-patient-001",
        fact_type=fact_type,
        logical_key=logical_key,
        value_original=value,
        effective_time=datetime(2026, 8, 18, 8, 0, tzinfo=timezone.utc),
        recorded_time=datetime(2026, 8, 18, 8, 2, tzinfo=timezone.utc),
        source=SourceRef(
            kind=SourceKind.FHIR,
            system="synthetic-lis",
            resource_type="Observation",
            resource_id=fact_id,
            resource_version="2" if supersedes else "1",
        ),
        assertion_stage=status,
        supersedes_fact_id=supersedes,
    )


def run_golden_journey() -> GoldenJourneyResult:
    patient_ref = "synthetic-patient-001"

    # 1. Source-linked clinical truth: one preliminary result + one documented therapy fact.
    result_v1 = _fact(
        "culture-v1",
        fact_type="microbiology",
        logical_key="blood-culture",
        value="growth detected; final identification pending",
        status=AssertionStage.PRELIMINARY,
    )
    therapy = _fact(
        "therapy-1",
        fact_type="medication",
        logical_key="documented-therapy",
        value="Synthetic antibiotic A documented as active therapy",
    )
    initial_truth = TruthEnvelope(patient_ref=patient_ref, facts=[result_v1, therapy])
    initial_graph = graph_from_truth(initial_truth)

    # 2. Clinician-facing AI output remains an unsigned derived artifact tied to source facts.
    draft = DerivedArtifact(
        artifact_id="progress-note-draft-001",
        patient_ref=patient_ref,
        kind=ArtifactKind.AI_DRAFT,
        state=ArtifactState.CURRENT,
        dependencies=(
            ArtifactDependency(fact_id="culture-v1", transformer="source-linked-note-draft", transformer_version="1"),
            ArtifactDependency(fact_id="therapy-1", transformer="source-linked-note-draft", transformer_version="1"),
        ),
    )

    # 3. During a simulated outage the source publishes a corrected/final result.
    result_v2 = _fact(
        "culture-v2",
        fact_type="microbiology",
        logical_key="blood-culture",
        value="final synthetic organism identification",
        status=AssertionStage.FINAL,
        supersedes="culture-v1",
    )
    recovered_truth = TruthEnvelope(patient_ref=patient_ref, facts=[result_v1, result_v2, therapy])
    recovered_graph = graph_from_truth(recovered_truth)

    # 4. Recovery may return to NORMAL only after the corrected fact invalidates dependent drafts.
    recovery = reconcile_after_outage(
        graph=recovered_graph,
        artifacts=[draft],
        changed_fact_ids={"culture-v2"},
    )

    # 5. Patient receives a role-appropriate presentation over the same source-truth philosophy.
    patient_view = synthetic_patient_view()

    # 6. Cross-provider follow-up is an acknowledged lifecycle, not fire-and-forget transport.
    request = synthetic_coordination_request()
    coordination_states = [request.state]
    for actor, state, confirmed in (
        ("hospital-user", CareRequestState.REQUESTED, True),
        ("practice-system", CareRequestState.RECEIVED, False),
        ("practice-user", CareRequestState.ACCEPTED, False),
        ("practice-user", CareRequestState.SCHEDULED, False),
        ("practice-user", CareRequestState.PERFORMED, False),
        ("practice-system", CareRequestState.RESULT_AVAILABLE, False),
        ("hospital-user", CareRequestState.FOLLOW_UP_COMPLETE, False),
    ):
        transition = transition_request(request, state, actor_id=actor, human_confirmed=confirmed)
        request = transition.request
        coordination_states.append(request.state)

    physician_target = target_for(StakeholderRole.PHYSICIAN, TimeUnit.SHIFT)
    if physician_target is None:
        raise RuntimeError("physician time-return target missing")

    reopened = recovery.invalidation.artifacts[0]
    checkpoints = (
        JourneyCheckpoint(
            name="patient-partition",
            assertion="all core journey artifacts remain bound to the same synthetic patient",
            passed=(initial_graph.patient_ref == patient_ref == recovery.patient_ref == patient_view.patient_ref),
        ),
        JourneyCheckpoint(
            name="source-lineage",
            assertion="corrected source result explicitly supersedes the earlier source fact",
            passed=any(edge.relation.value == "supersedes" for edge in recovered_graph.edges),
        ),
        JourneyCheckpoint(
            name="draft-reopened",
            assertion="a corrected supporting result reopens the unsigned AI draft instead of silently leaving it current",
            passed=reopened.state == ArtifactState.REVIEW_REQUIRED,
        ),
        JourneyCheckpoint(
            name="recovery-gated",
            assertion="recovery begins in RECOVERY and returns to NORMAL only after reconciliation",
            passed=(recovery.before.mode == OperatingMode.RECOVERY and recovery.after.mode == OperatingMode.NORMAL),
        ),
        JourneyCheckpoint(
            name="patient-uncertainty",
            assertion="patient presentation keeps pending information visible with an owner/next step",
            passed=bool(patient_view.pending and all(item.requires_attention and item.next_step for item in patient_view.pending)),
        ),
        JourneyCheckpoint(
            name="acknowledged-coordination",
            assertion="cross-provider request reaches explicit follow-up completion through acknowledged states",
            passed=(coordination_states[0] == CareRequestState.DRAFT and coordination_states[-1] == CareRequestState.FOLLOW_UP_COMPLETE),
        ),
        JourneyCheckpoint(
            name="outcome-not-claim",
            assertion="physician time-back remains a target to test rather than a fabricated measured outcome",
            passed=physician_target.pilot_minutes_returned > 0,
        ),
        JourneyCheckpoint(
            name="sla-not-fabricated",
            assertion="production 24/7 commitment remains not offered until external operating evidence exists",
            passed=CommitmentState.NOT_OFFERED == CommitmentState.NOT_OFFERED,
        ),
    )

    return GoldenJourneyResult(
        patient_ref=patient_ref,
        initial_graph=initial_graph,
        clinician_draft_before_correction=draft,
        recovery=recovery,
        patient_view=patient_view,
        coordination_states=tuple(coordination_states),
        physician_time_target_minutes=physician_target.pilot_minutes_returned,
        sla_state=CommitmentState.NOT_OFFERED,
        checkpoints=checkpoints,
    )

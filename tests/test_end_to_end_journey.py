from app.artifact_invalidation import ArtifactState
from app.care_coordination import CareRequestState
from app.end_to_end_journey import run_golden_journey
from app.resilience_mode import OperatingMode
from app.service_operating_model import CommitmentState


def test_golden_journey_connects_truth_graph_recovery_patient_and_coordination():
    result = run_golden_journey()

    assert result.all_passed is True
    assert result.clinician_draft_before_correction.state == ArtifactState.CURRENT
    assert result.recovery.invalidation.artifacts[0].state == ArtifactState.REVIEW_REQUIRED
    assert result.recovery.before.mode == OperatingMode.RECOVERY
    assert result.recovery.after.mode == OperatingMode.NORMAL
    assert result.patient_view.pending
    assert result.coordination_states == (
        CareRequestState.DRAFT,
        CareRequestState.REQUESTED,
        CareRequestState.RECEIVED,
        CareRequestState.ACCEPTED,
        CareRequestState.SCHEDULED,
        CareRequestState.PERFORMED,
        CareRequestState.RESULT_AVAILABLE,
        CareRequestState.FOLLOW_UP_COMPLETE,
    )
    assert result.physician_time_target_minutes > 0
    assert result.sla_state == CommitmentState.NOT_OFFERED

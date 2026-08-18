import pytest

from app.service_operating_model import (
    CommitmentState,
    IncidentSeverity,
    ServiceCapability,
    ServiceCommitment,
    ServiceCriticality,
    classify_incident,
)


def test_core_context_cannot_depend_on_shared_phi_control_plane():
    with pytest.raises(ValueError, match="shared control plane"):
        ServiceCapability(
            service_id="bad-core",
            criticality=ServiceCriticality.C1_CLINICAL_CONTEXT,
            routine_phi_control_plane_dependency=True,
            hospital_local_fallback_required=True,
            description="bad",
        )


def test_contracted_sla_cannot_exist_without_staffing_and_target_environment_evidence():
    with pytest.raises(ValueError, match="staffed on-call"):
        ServiceCommitment(
            service_id="careos-context",
            state=CommitmentState.CONTRACTED,
            target="99.95% monthly availability",
            evidence_refs=("synthetic-only",),
            staffed_on_call=False,
            target_environment_exercised=True,
        )


def test_wrong_patient_or_unauthorised_action_is_systemic_sev0():
    result = classify_incident(wrong_patient_risk=True, unauthorized_action_risk=True)
    assert result.severity == IncidentSeverity.SEV0
    assert result.hospital_notification_required is True
    assert result.recommended_kill_scopes


def test_agent_only_outage_is_lower_severity_when_context_survives():
    result = classify_incident(agent_only_unavailable=True)
    assert result.severity == IncidentSeverity.SEV2
    assert result.hospital_notification_required is False


def test_clinical_context_outage_requires_hospital_notification_and_legacy_fallback():
    result = classify_incident(clinical_context_unavailable=True)
    assert result.severity == IncidentSeverity.SEV1
    assert result.hospital_notification_required is True

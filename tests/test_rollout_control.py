import pytest

from app.hospital_install import DeploymentIntent, HospitalManifest, InterfaceKind, PatientIdentityStrategy, SourceSystem, SystemRole
from app.hospital_upgrade import compare_hospital_manifests
from app.rollout_control import (
    CanaryEvidence,
    RolloutState,
    begin_rollout,
    evaluate_canary,
    promote,
    record_conformance,
    record_preflight,
    rollback,
    start_canary,
)


def manifest(version="1", write=False):
    return HospitalManifest(
        hospital_id="H1",
        site_name="Synthetic Hospital",
        deployment_intent=DeploymentIntent.DEIDENTIFIED,
        sources=[
            SourceSystem(
                source_id="kis",
                role=SystemRole.KIS,
                vendor="Vendor",
                product="KIS",
                version=version,
                interfaces=[InterfaceKind.FHIR_R4],
                patient_identity_available=True,
                source_resource_ids_available=True,
                effective_time_available=True,
                lifecycle_state_available=True,
                write_supported=write,
            )
        ],
        patient_identity_strategy=PatientIdentityStrategy.SHARED_ENTERPRISE_ID,
        oidc_or_sso_available=True,
        trusted_patient_context_launch=True,
        audit_destination_available=True,
        rollback_owner_named=True,
        security_owner_named=True,
        privacy_owner_named=True,
        clinical_owner_named=True,
    )


def passing_evidence():
    return CanaryEvidence(
        observations=100,
        source_availability_ok=True,
        source_freshness_ok=True,
        patient_identity_errors=0,
        connector_errors=0,
        incomplete_reads=0,
        unsupported_claims=0,
        safety_stop_events=0,
    )


def test_version_change_requires_shadow_before_promotion():
    upgrade = compare_hospital_manifests(manifest("1"), manifest("2"))
    assert upgrade.requires_shadow_revalidation is True
    record = begin_rollout(upgrade, release_id="careos-2", previous_release_id="careos-1")
    record = record_preflight(record, "preflight:1")
    record = record_conformance(record, "conformance:1")
    with pytest.raises(ValueError, match="shadow/canary evidence"):
        promote(record)
    record = start_canary(record)
    record = evaluate_canary(record, passing_evidence())
    promoted = promote(record)
    assert promoted.state == RolloutState.PROMOTED


def test_canary_failure_rolls_back_to_last_known_good_release():
    upgrade = compare_hospital_manifests(manifest("1"), manifest("2"))
    record = record_conformance(record_preflight(begin_rollout(upgrade, release_id="2", previous_release_id="1"), "p"), "c")
    record = start_canary(record)
    failed = passing_evidence().model_copy(update={"patient_identity_errors": 1})
    result = evaluate_canary(record, failed)
    assert result.state == RolloutState.ROLLED_BACK
    assert result.previous_release_id == "1"
    assert "patient identity error=1" in result.rollback_reason


def test_rollback_is_idempotent():
    upgrade = compare_hospital_manifests(manifest("1"), manifest("2"))
    record = begin_rollout(upgrade, release_id="2", previous_release_id="1")
    first = rollback(record, reason="operator stop")
    second = rollback(first, reason="ignored duplicate")
    assert second == first


def test_new_write_authority_blocks_upgrade_before_canary():
    upgrade = compare_hospital_manifests(manifest("1", write=False), manifest("1", write=True))
    assert any(f.code == "write-capability-added" and f.severity == "block" for f in upgrade.findings)
    record = begin_rollout(upgrade, release_id="2", previous_release_id="1")
    assert record.state == RolloutState.BLOCKED


def test_operator_stop_or_unsupported_claim_fails_canary():
    upgrade = compare_hospital_manifests(manifest("1"), manifest("2"))
    record = record_conformance(record_preflight(begin_rollout(upgrade, release_id="2", previous_release_id="1"), "p"), "c")
    record = start_canary(record)
    evidence = passing_evidence().model_copy(update={"operator_stop": True, "unsupported_claims": 1})
    result = evaluate_canary(record, evidence)
    assert result.state == RolloutState.ROLLED_BACK
    assert "operator stop" in result.rollback_reason
    assert "unsupported claim=1" in result.rollback_reason

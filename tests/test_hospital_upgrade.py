from copy import deepcopy

from app.hospital_install import DeploymentIntent, HospitalManifest, InterfaceKind, SourceSystem, SystemRole
from app.hospital_upgrade import compare_hospital_manifests


def source():
    return SourceSystem(
        source_id="kis-main",
        role=SystemRole.KIS,
        vendor="Vendor",
        product="KIS",
        version="1.0",
        interfaces=[InterfaceKind.FHIR_R4],
        authentication_mode="oidc",
        endpoint_env="KIS_ENDPOINT",
        credential_env="KIS_TOKEN",
        patient_identity_available=True,
        encounter_identity_available=True,
        source_resource_ids_available=True,
        source_versions_available=True,
        effective_time_available=True,
        lifecycle_state_available=True,
        incremental_refresh_available=True,
    )


def manifest():
    return HospitalManifest(
        hospital_id="DE-BERLIN-DEMO",
        site_name="Synthetic Hospital",
        deployment_intent=DeploymentIntent.DEIDENTIFIED,
        sources=[source()],
        oidc_or_sso_available=True,
        trusted_patient_context_launch=True,
        audit_destination_available=True,
        rollback_owner_named=True,
        security_owner_named=True,
        privacy_owner_named=True,
        clinical_owner_named=True,
    )


def test_identical_manifest_is_safe_for_automatic_rollout():
    previous = manifest()
    proposed = HospitalManifest.model_validate(previous.model_dump())
    plan = compare_hospital_manifests(previous, proposed)
    assert plan.safe_for_automatic_rollout is True
    assert plan.requires_shadow_revalidation is False
    assert plan.findings == []


def test_version_change_requires_shadow_revalidation():
    previous = manifest()
    proposed = HospitalManifest.model_validate(previous.model_dump())
    proposed.sources[0].version = "2.0"
    plan = compare_hospital_manifests(previous, proposed)
    assert plan.safe_for_automatic_rollout is False
    assert plan.requires_shadow_revalidation is True
    assert any(f.code == "version-changed" and f.severity == "warn" for f in plan.findings)


def test_interface_loss_blocks_upgrade():
    previous = manifest()
    proposed = HospitalManifest.model_validate(previous.model_dump())
    proposed.sources[0].interfaces = []
    plan = compare_hospital_manifests(previous, proposed)
    assert plan.safe_for_automatic_rollout is False
    assert any(f.code == "interface-lost" and f.severity == "block" for f in plan.findings)
    assert any(f.code == "proposed-preflight-blocked" for f in plan.findings)


def test_patient_identity_loss_blocks_upgrade():
    previous = manifest()
    proposed = HospitalManifest.model_validate(previous.model_dump())
    proposed.sources[0].patient_identity_available = False
    plan = compare_hospital_manifests(previous, proposed)
    assert any(f.code == "capability-lost:patient_identity_available" and f.severity == "block" for f in plan.findings)


def test_new_write_capability_never_activates_as_routine_upgrade():
    previous = manifest()
    proposed = HospitalManifest.model_validate(previous.model_dump())
    proposed.sources[0].write_supported = True
    plan = compare_hospital_manifests(previous, proposed)
    assert any(f.code == "write-capability-added" and f.severity == "block" for f in plan.findings)

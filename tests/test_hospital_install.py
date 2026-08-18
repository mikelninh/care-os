import pytest

from app.hospital_install import (
    DeploymentIntent,
    HospitalManifest,
    InterfaceKind,
    SourceSystem,
    SystemRole,
    build_hospital_install_plan,
)


def source(*, source_id: str, vendor: str, product: str, interfaces: list[InterfaceKind]):
    return SourceSystem(
        source_id=source_id,
        role=SystemRole.KIS,
        vendor=vendor,
        product=product,
        version="2026.1",
        interfaces=interfaces,
        authentication_mode="oidc",
        endpoint_env="KIS_ENDPOINT",
        credential_env="KIS_TOKEN",
        resources=["Patient", "Encounter", "Observation"],
        patient_identity_available=True,
        encounter_identity_available=True,
        source_resource_ids_available=True,
        source_versions_available=True,
        effective_time_available=True,
        lifecycle_state_available=True,
        incremental_refresh_available=True,
    )


def manifest(sources: list[SourceSystem], intent=DeploymentIntent.DEIDENTIFIED):
    return HospitalManifest(
        hospital_id="DE-BERLIN-DEMO",
        site_name="Synthetic Berlin Hospital",
        deployment_intent=intent,
        sources=sources,
        oidc_or_sso_available=True,
        trusted_patient_context_launch=True,
        audit_destination_available=True,
        rollback_owner_named=True,
        security_owner_named=True,
        privacy_owner_named=True,
        clinical_owner_named=True,
    )


def test_same_standard_adapter_reused_across_different_vendors():
    vendor_a = source(source_id="kis-a", vendor="Vendor A", product="KIS-A", interfaces=[InterfaceKind.FHIR_R4])
    vendor_b = source(source_id="kis-b", vendor="Vendor B", product="KIS-B", interfaces=[InterfaceKind.FHIR_R4])

    plan = build_hospital_install_plan(manifest([vendor_a, vendor_b]))

    read_adapters = [a for a in plan.adapters if a.direction == "read"]
    assert {a.adapter_id for a in read_adapters} == {"standard-fhir-r4"}
    assert all(a.adapter_family == "fhir" for a in read_adapters)
    assert all(a.implementation_status == "implemented" for a in read_adapters)
    assert all(a.runtime_available for a in read_adapters)
    assert plan.installable_for_synthetic_or_deidentified is True


def test_isik_is_preferred_over_generic_fhir_but_keeps_validation_path_label():
    kis = source(
        source_id="kis",
        vendor="ExampleVendor",
        product="ExampleKIS",
        interfaces=[InterfaceKind.FHIR_R4, InterfaceKind.ISIK_FHIR],
    )
    plan = build_hospital_install_plan(manifest([kis]))
    assert plan.adapters[0].adapter_id == "standard-isik-fhir"
    assert plan.adapters[0].implementation_status == "validation-path"
    assert plan.adapters[0].runtime_available is True
    assert any(c.status == "warn" and c.id.endswith("adapter-runtime") for c in plan.checks)


def test_hl7_is_visible_as_target_but_blocks_self_service_until_runtime_exists():
    lis = source(source_id="lis", vendor="ExampleLIS", product="LIS", interfaces=[InterfaceKind.HL7V2])
    lis.role = SystemRole.LIS
    plan = build_hospital_install_plan(manifest([lis]))
    assert plan.adapters[0].adapter_id == "standard-hl7v2-read"
    assert plan.adapters[0].implementation_status == "contract-only"
    assert plan.adapters[0].runtime_available is False
    assert plan.installable_for_synthetic_or_deidentified is False
    assert any(c.status == "block" and c.id.endswith("adapter-runtime") for c in plan.checks)


def test_manifest_rejects_endpoint_or_secret_values_in_versionable_config():
    with pytest.raises(ValueError, match="environment variable"):
        SourceSystem(
            source_id="kis",
            role=SystemRole.KIS,
            vendor="Vendor",
            product="KIS",
            version="1",
            interfaces=[InterfaceKind.FHIR_R4],
            endpoint_env="https://hospital.example/fhir",
        )


def test_missing_patient_identity_blocks_shadow_readiness():
    kis = source(source_id="kis", vendor="Vendor", product="KIS", interfaces=[InterfaceKind.FHIR_R4])
    kis.patient_identity_available = False
    plan = build_hospital_install_plan(manifest([kis]))
    assert plan.ready_for_shadow is False
    assert any(c.status == "block" and "patient-identity" in c.id for c in plan.checks)


def test_no_interface_fails_closed_instead_of_inventing_custom_adapter():
    kis = source(source_id="kis", vendor="Vendor", product="KIS", interfaces=[])
    plan = build_hospital_install_plan(manifest([kis]))
    assert not any(a.source_id == "kis" for a in plan.adapters)
    assert any(c.status == "block" and c.id.endswith("read-path") for c in plan.checks)


def test_live_shadow_plan_is_describable_but_current_release_remains_locked():
    kis = source(source_id="kis", vendor="Vendor", product="KIS", interfaces=[InterfaceKind.ISIK_FHIR])
    plan = build_hospital_install_plan(manifest([kis], DeploymentIntent.SHADOW_READONLY))
    assert plan.ready_for_shadow is True
    assert plan.execution_allowed_by_current_release is False
    assert "G0-G5" in (plan.release_blocker or "")


def test_write_never_appears_without_explicit_controlled_write_opt_in():
    kis = source(source_id="kis", vendor="Vendor", product="KIS", interfaces=[InterfaceKind.FHIR_R4])
    kis.write_supported = True
    plan = build_hospital_install_plan(manifest([kis], DeploymentIntent.DEIDENTIFIED))
    assert all(a.direction == "read" for a in plan.adapters)
    assert plan.ready_for_controlled_write is False

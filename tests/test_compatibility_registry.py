from pathlib import Path

from app.compatibility_registry import (
    CompatibilityRecord,
    CompatibilityRegistry,
    EvidenceClass,
    VersionMatchPolicy,
    assess_upgrade_compatibility,
    validate_registry_against_adapter_catalog,
)
from app.hospital_install import HospitalManifest
from app.hospital_upgrade import compare_hospital_manifests


def registry():
    return CompatibilityRegistry.from_directory("compatibility")


def manifest():
    return HospitalManifest.model_validate_json(Path("deploy/hospital.example.json").read_text(encoding="utf-8"))


def test_registry_records_validate_against_known_adapter_catalog():
    validate_registry_against_adapter_catalog(registry())


def test_exact_synthetic_record_matches_but_never_auto_approves():
    lookup = registry().lookup(
        source_id="kis-main",
        adapter_id="standard-fhir-r4",
        vendor="Example KIS Vendor",
        product="Example KIS",
        version="2026.1",
    )
    assert len(lookup.matches) == 1
    assert lookup.matches[0].evidence_class == EvidenceClass.SYNTHETIC_ONLY
    assert lookup.exact_real_evidence is False
    assert lookup.may_auto_approve_rollout is False


def test_exact_policy_does_not_assume_neighboring_version_compatibility():
    lookup = registry().lookup(
        source_id="kis-main",
        adapter_id="standard-fhir-r4",
        vendor="Example KIS Vendor",
        product="Example KIS",
        version="2026.2",
    )
    assert lookup.matches == ()


def test_explicit_allowlist_requires_versions():
    try:
        CompatibilityRecord(
            record_id="x",
            adapter_id="standard-fhir-r4",
            vendor="V",
            product="P",
            tested_version="1",
            version_match_policy=VersionMatchPolicy.EXPLICIT_ALLOWLIST,
            interface_profile="FHIR",
            authentication_pattern="none",
            patient_identity_behavior="explicit",
            encounter_identity_behavior="explicit",
            paging_behavior="bounded",
            versioning_behavior="versioned",
            lifecycle_behavior="explicit",
            conformance_suite_version="1",
            conformance_result="synthetic",
            evidence_class=EvidenceClass.SYNTHETIC_ONLY,
            tested_on="2026-08-18",
            synthetic_only=True,
        )
    except ValueError as exc:
        assert "compatible_versions" in str(exc)
    else:
        raise AssertionError("explicit allowlist without compatible_versions must be rejected")


def test_upgrade_preflight_can_consume_compatibility_without_changing_approval():
    current = manifest()
    proposed = current.model_copy(deep=True)
    proposed.sources[0].version = "2026.2"
    upgrade = compare_hospital_manifests(current, proposed)
    lookups = assess_upgrade_compatibility(upgrade, proposed, registry())
    kis = next(item for item in lookups if item.source_id == "kis-main")
    assert kis.matches == ()
    assert kis.may_auto_approve_rollout is False
    assert upgrade.requires_shadow_revalidation is True

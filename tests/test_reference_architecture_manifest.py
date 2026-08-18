import json
from pathlib import Path


MANIFEST = Path("architecture/reference-architecture.json")


def _load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_reference_architecture_manifest_is_explicitly_not_production_clearance():
    data = _load()
    assert data["reference_architecture_readiness"]["state"] == "proposal-ready"
    assert "not production approval" in data["reference_architecture_readiness"]["meaning"]
    assert data["production_claim"] == "not-production-ready"
    assert data["live_patient_data_allowed"] is False


def test_careos_is_not_system_of_record_or_central_phi_control_plane():
    data = _load()
    assert data["system_of_record"] is False
    assert data["routine_phi_in_control_plane"] is False
    assert data["default_data_locality"] == "provider-data-plane"


def test_read_write_model_and_cross_source_identity_boundaries_are_machine_readable():
    data = _load()
    assert data["default_clinical_mode"] == "read-only"
    assert data["autonomous_clinical_writeback"] is False
    principles = set(data["architecture_principles"])
    assert "models-are-untrusted-proposers" in principles
    assert "read-write-capability-separation" in principles
    assert "mandatory-provenance" in principles
    assert "explicit-unknown-and-failure-state" in principles
    assert "explicit-cross-source-patient-identity" in principles
    assert "adapter-maturity-is-machine-readable" in principles


def test_provider_data_plane_has_install_identity_truth_policy_and_audit():
    data = _load()
    components = set(data["planes"]["provider_data_plane"]["components"])
    assert {
        "hospital-capability-manifest",
        "connector-gateway",
        "patient-and-encounter-identity",
        "clinical-truth-layer",
        "authorization-policy",
        "provider-audit",
    }.issubset(components)


def test_self_install_manifest_does_not_claim_real_hospital_repeatability():
    data = _load()
    install = data["self_install"]
    assert install["state"] == "synthetic-deidentified-scaffold"
    assert install["live_self_service_proven"] is False
    assert install["multi_hospital_repeatability_proven"] is False
    assert data["adapter_maturity"]["hl7v2"] == "contract-only"
    assert data["adapter_maturity"]["live-write"] == "unsupported-current-release"


def test_every_key_reference_document_is_declared():
    data = _load()
    docs = data["documents"]
    expected = {
        "canonical_architecture",
        "endgame",
        "hospital_self_install",
        "connector_sdk",
        "government_reference",
        "deployment_patterns",
        "trust_and_data_flow",
        "national_integration_map",
        "technical_documentation_index",
        "adrs",
        "production_gates",
    }
    assert expected.issubset(docs)
    for path in docs.values():
        assert Path(path).exists(), path

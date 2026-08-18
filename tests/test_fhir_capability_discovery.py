import pytest

from app.fhir_capability_discovery import compare_manifest_resources, parse_capability_statement


CAPABILITY = {
    "resourceType": "CapabilityStatement",
    "fhirVersion": "4.0.1",
    "format": ["json", "xml"],
    "software": {"name": "Synthetic FHIR", "version": "1.2.3"},
    "rest": [
        {
            "mode": "server",
            "resource": [
                {
                    "type": "Patient",
                    "versioning": "versioned-update",
                    "interaction": [{"code": "read"}, {"code": "search-type"}],
                    "searchParam": [{"name": "identifier"}],
                },
                {
                    "type": "Observation",
                    "versioning": "versioned",
                    "interaction": [{"code": "read"}, {"code": "search-type"}],
                    "searchParam": [{"name": "patient"}, {"name": "date"}],
                },
            ],
        }
    ],
}


def test_capability_statement_is_normalized_for_preflight_suggestions():
    result = parse_capability_statement(CAPABILITY)
    assert result.fhir_version == "4.0.1"
    assert result.software_name == "Synthetic FHIR"
    assert result.resource_types == ["Observation", "Patient"]
    assert result.supports_patient_read is True
    assert result.versioned_resource_types == ["Observation", "Patient"]


def test_manifest_comparison_reports_differences_without_rewriting_manifest():
    discovery = parse_capability_statement(CAPABILITY)
    comparison = compare_manifest_resources(
        "kis",
        ["Patient", "Encounter"],
        discovery,
    )
    assert comparison.undeclared_but_discovered == ["Observation"]
    assert comparison.declared_but_not_advertised == ["Encounter"]
    assert comparison.patient_read_advertised is True


def test_non_capability_statement_is_rejected():
    with pytest.raises(ValueError, match="CapabilityStatement"):
        parse_capability_statement({"resourceType": "Bundle"})

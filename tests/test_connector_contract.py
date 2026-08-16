from app.connectors.fhir_connector import FHIRConnector
from app.fhir_adapter import FhirUnavailable


class GoodFHIRClient:
    def patient_snapshot(self, patient_ref: str):
        return {
            "patient": {"resourceType": "Patient", "id": patient_ref},
            "allergies": [],
            "conditions": [],
            "observations": [
                {
                    "resourceType": "Observation",
                    "id": "o1",
                    "meta": {"versionId": "3"},
                    "code": {"text": "Synthetic value"},
                    "valueQuantity": {"value": 7, "unit": "unit"},
                    "effectiveDateTime": "2026-08-16T08:00:00+00:00",
                }
            ],
            "medications": [],
            "tasks": [],
            "documents": [],
        }


class BrokenFHIRClient:
    def patient_snapshot(self, patient_ref: str):
        raise FhirUnavailable("synthetic outage")


def test_connector_success_returns_truth_plus_current_source_state():
    connector = FHIRConnector(client=GoodFHIRClient())
    result = connector.read_patient_truth("p1")
    assert result.source_state.availability.value == "current"
    assert result.truth is not None
    assert result.truth.patient_ref == "p1"
    assert result.truth.provenance_coverage() == 1.0
    assert result.safe_to_render is True


def test_connector_failure_is_unavailable_not_empty_patient_truth():
    connector = FHIRConnector(client=BrokenFHIRClient())
    result = connector.read_patient_truth("p1")
    assert result.source_state.availability.value == "unavailable"
    assert result.truth is None
    assert result.safe_to_render is False


def test_capabilities_are_explicit_about_missing_production_features():
    caps = FHIRConnector(client=GoodFHIRClient()).capabilities()
    assert caps.read_only is True
    assert caps.supports_paging is False
    assert caps.supports_incremental_refresh is False
    assert "ISiK" in " ".join(caps.notes)

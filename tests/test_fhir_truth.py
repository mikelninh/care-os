from app.fhir_adapter import snapshot_to_truth, snapshot_to_timeline


def test_fhir_truth_preserves_version_time_and_provenance():
    snapshot = {
        "patient": {"resourceType": "Patient", "id": "p1", "name": [{"given": ["Mara"], "family": "Novak"}]},
        "allergies": [],
        "conditions": [],
        "observations": [
            {
                "resourceType": "Observation",
                "id": "cr-1",
                "meta": {"versionId": "12"},
                "code": {"text": "Creatinine", "coding": [{"system": "http://loinc.org", "code": "2160-0", "display": "Creatinine"}]},
                "valueQuantity": {"value": 1.4, "unit": "mg/dL", "system": "http://unitsofmeasure.org", "code": "mg/dL"},
                "effectiveDateTime": "2026-08-16T08:00:00+00:00",
                "issued": "2026-08-16T08:05:00+00:00",
            }
        ],
        "medications": [],
        "tasks": [],
        "documents": [],
    }
    truth = snapshot_to_truth(snapshot)
    fact = truth.facts[0]
    assert fact.patient_ref == "p1"
    assert fact.value_original == 1.4
    assert fact.unit_original == "mg/dL"
    assert fact.source.resource_id == "cr-1"
    assert fact.source.resource_version == "12"
    assert fact.effective_time.isoformat() == "2026-08-16T08:00:00+00:00"
    assert fact.recorded_time.isoformat() == "2026-08-16T08:05:00+00:00"
    assert truth.provenance_coverage() == 1.0


def test_compatibility_timeline_is_rendered_from_truth_contract():
    snapshot = {
        "patient": {"resourceType": "Patient", "id": "p1"},
        "allergies": [{"resourceType": "AllergyIntolerance", "id": "a1", "meta": {"versionId": "2"}, "code": {"text": "Penicillin"}, "recordedDate": "2026-01-01"}],
        "conditions": [],
        "observations": [],
        "medications": [],
        "tasks": [],
        "documents": [],
    }
    timeline = snapshot_to_timeline(snapshot)
    assert timeline["provenance_coverage"] == 1.0
    assert timeline["items"][0]["fact_id"] == "AllergyIntolerance:a1"
    assert timeline["items"][0]["resource_version"] == "2"
    assert timeline["items"][0]["provenance_complete"] is True

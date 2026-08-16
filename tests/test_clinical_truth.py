from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.clinical_truth import ClinicalFact, FactStatus, SourceKind, SourceRef, TruthEnvelope


def fhir_source() -> SourceRef:
    return SourceRef(
        kind=SourceKind.FHIR,
        system="hospital-fhir",
        resource_type="Observation",
        resource_id="egfr-123",
        resource_version="7",
    )


def test_confirmed_fact_requires_traceable_source():
    fact = ClinicalFact(
        fact_id="renal-1",
        patient_ref="patient-1",
        fact_type="renal.egfr",
        value_original=42,
        unit_original="mL/min/1.73m2",
        effective_time=datetime(2026, 8, 16, 8, 0, tzinfo=timezone.utc),
        source=fhir_source(),
    )
    assert fact.provenance_complete is True
    assert fact.safe_default_surface is True


def test_document_fact_requires_exact_evidence_span():
    with pytest.raises(ValidationError):
        SourceRef(
            kind=SourceKind.DOCUMENT,
            system="fax-ingest",
            document_id="fax-55",
        )


def test_ambiguous_fact_is_routed_to_review_not_quiet_view():
    fact = ClinicalFact(
        fact_id="allergy-1",
        patient_ref="patient-1",
        fact_type="allergy",
        value_original="Penicillin?",
        source=SourceRef(
            kind=SourceKind.DOCUMENT,
            system="scan-ingest",
            document_id="scan-9",
            evidence_span="Allergien: Penicillin? laut Eigenanamnese",
        ),
        status=FactStatus.AMBIGUOUS,
        confidence=0.6,
        review_reason="question mark and self-report require confirmation",
    )
    envelope = TruthEnvelope(patient_ref="patient-1", facts=[fact])
    assert fact.safe_default_surface is False
    assert envelope.review_queue() == [fact]
    assert envelope.provenance_coverage() == 1.0


def test_cross_patient_fact_is_rejected():
    fact = ClinicalFact(
        fact_id="renal-2",
        patient_ref="patient-2",
        fact_type="renal.creatinine",
        value_original=1.4,
        source=fhir_source(),
    )
    with pytest.raises(ValidationError):
        TruthEnvelope(patient_ref="patient-1", facts=[fact])


def test_unknown_fact_requires_reason():
    with pytest.raises(ValidationError):
        ClinicalFact(
            fact_id="med-unknown",
            patient_ref="patient-1",
            fact_type="medication.current",
            value_original="unknown",
            source=fhir_source(),
            status=FactStatus.UNKNOWN,
        )

from datetime import datetime, timezone

from app.clinical_truth import FactStatus
from app.document_pipeline import DocumentInput
from app.extractors.base import VerifiedExtractionPipeline
from app.extractors.conservative_de import ConservativeGermanExtractor


def doc(kind: str, text: str) -> DocumentInput:
    return DocumentInput(
        patient_ref="p1",
        document_id=f"d-{kind}",
        source_system="synthetic",
        document_kind=kind,
        recorded_time=datetime(2026, 8, 16, tzinfo=timezone.utc),
        text=text,
    )


def test_explicit_allergy_is_promoted_with_exact_source_evidence():
    result = VerifiedExtractionPipeline(ConservativeGermanExtractor()).run(
        doc("allergy", "Allergie: Penicillin. Reaktion: Hautausschlag. Keine weiteren bekannten Arzneimittelallergien.")
    )
    assert not result.rejected
    assert result.provenance_coverage == 1.0
    fact = result.truth.facts[0]
    assert fact.fact_type == "allergy"
    assert fact.value_original == {"substance": "Penicillin", "reaction": "Hautausschlag"}
    assert fact.source.evidence_span == "Allergie: Penicillin. Reaktion: Hautausschlag."


def test_unsupported_high_risk_form_becomes_review_required_not_silent_empty():
    result = VerifiedExtractionPipeline(ConservativeGermanExtractor()).run(
        doc("allergy", "Arzneimittelunverträglichkeit unklar; bitte Altakte prüfen.")
    )
    assert len(result.truth.facts) == 1
    fact = result.truth.facts[0]
    assert fact.fact_type == "review_required"
    assert fact.status == FactStatus.UNKNOWN
    assert fact.safe_default_surface is False
    assert "unsupported" in fact.review_reason


def test_current_medications_exclude_explicit_historical_sentence():
    result = VerifiedExtractionPipeline(ConservativeGermanExtractor()).run(
        doc("medication", "Aktuelle Medikation: Ramipril, Metformin. Furosemid wurde vor 6 Monaten abgesetzt.")
    )
    facts = result.truth.facts
    assert len(facts) == 1
    assert facts[0].value_original == ["Ramipril", "Metformin"]


def test_renal_fact_preserves_source_time_and_unit():
    result = VerifiedExtractionPipeline(ConservativeGermanExtractor()).run(
        doc("lab", "Krea 1.7 mg/dl · eGFR 52 ml/min/1,73m².")
    )
    fact = result.truth.facts[0]
    assert fact.fact_type == "renal_function"
    assert fact.value_original == {"creatinine": 1.7, "egfr": 52}
    assert fact.unit_original == "mg/dl + ml/min/1.73m2"
    assert fact.effective_time == fact.recorded_time


def test_unknown_kind_does_not_invent_clinical_truth():
    result = VerifiedExtractionPipeline(ConservativeGermanExtractor()).run(
        doc("scan", "Vielleicht Allergie? Altmedikation unklar. OCR beschädigt.")
    )
    assert result.truth.facts == []

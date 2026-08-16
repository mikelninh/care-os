import pytest
from pydantic import ValidationError

from app.clinical_truth import FactStatus
from app.document_pipeline import (
    DocumentInput,
    ExtractedCandidate,
    MAX_DOCUMENT_CANDIDATES,
    MAX_DOCUMENT_TEXT_CHARS,
    UnsupportedEvidence,
    candidate_to_fact,
    ingest_document_candidates,
)


def document() -> DocumentInput:
    text = "Allergien: Penicillin, Exanthem. Aktuell keine weiteren Allergien bekannt."
    return DocumentInput(
        patient_ref="p1",
        document_id="doc-1",
        source_system="arztbrief",
        text=text,
    )


def test_exact_supported_candidate_enters_truth_layer():
    doc = document()
    quote = "Penicillin, Exanthem"
    start = doc.text.index(quote)
    candidate = ExtractedCandidate(
        fact_type="allergy",
        value_original={"substance": "Penicillin", "reaction": "Exanthem"},
        evidence_start=start,
        evidence_end=start + len(quote),
        evidence_quote=quote,
    )
    fact = candidate_to_fact(doc, candidate, transformer="schema-extractor", transformer_version="0.1")
    assert fact.provenance_complete is True
    assert fact.source.document_id == "doc-1"
    assert fact.source.evidence_span == quote
    assert fact.safe_default_surface is True


def test_paraphrased_or_hallucinated_evidence_is_rejected():
    doc = document()
    quote = "Penicillin, Exanthem"
    start = doc.text.index(quote)
    candidate = ExtractedCandidate(
        fact_type="allergy",
        value_original="Penicillin allergy",
        evidence_start=start,
        evidence_end=start + len(quote),
        evidence_quote="Penicillin allergy",
    )
    with pytest.raises(UnsupportedEvidence):
        candidate_to_fact(doc, candidate, transformer="llm", transformer_version="test")


def test_out_of_bounds_span_is_rejected():
    doc = document()
    candidate = ExtractedCandidate(
        fact_type="allergy",
        value_original="Penicillin",
        evidence_start=5,
        evidence_end=len(doc.text) + 100,
        evidence_quote="Penicillin",
    )
    with pytest.raises(UnsupportedEvidence):
        candidate_to_fact(doc, candidate, transformer="llm", transformer_version="test")


def test_ambiguous_but_supported_candidate_goes_to_review_queue():
    doc = DocumentInput(
        patient_ref="p1",
        document_id="doc-2",
        source_system="scan",
        text="Allergie: Penicillin? laut Eigenanamnese.",
    )
    quote = "Penicillin? laut Eigenanamnese"
    start = doc.text.index(quote)
    candidate = ExtractedCandidate(
        fact_type="allergy",
        value_original="Penicillin?",
        evidence_start=start,
        evidence_end=start + len(quote),
        evidence_quote=quote,
        confidence=0.6,
        status=FactStatus.AMBIGUOUS,
        review_reason="uncertain self-report",
    )
    truth = ingest_document_candidates(doc, [candidate], transformer="llm", transformer_version="test")
    assert len(truth.review_queue()) == 1
    assert truth.facts[0].safe_default_surface is False
    assert truth.provenance_coverage() == 1.0


def test_multiple_candidates_keep_distinct_fact_ids_and_same_patient():
    doc = DocumentInput(
        patient_ref="p1",
        document_id="doc-3",
        source_system="lab-pdf",
        text="Kreatinin 1.4 mg/dL. eGFR 42 mL/min/1.73m2.",
    )
    candidates = []
    for fact_type, quote, value in [
        ("renal.creatinine", "1.4 mg/dL", 1.4),
        ("renal.egfr", "42 mL/min/1.73m2", 42),
    ]:
        start = doc.text.index(quote)
        candidates.append(ExtractedCandidate(
            fact_type=fact_type,
            value_original=value,
            evidence_start=start,
            evidence_end=start + len(quote),
            evidence_quote=quote,
        ))
    truth = ingest_document_candidates(doc, candidates, transformer="schema-extractor", transformer_version="0.1")
    assert len({f.fact_id for f in truth.facts}) == 2
    assert {f.patient_ref for f in truth.facts} == {"p1"}


def test_document_text_is_bounded_before_extraction():
    with pytest.raises(ValidationError):
        DocumentInput(patient_ref="p1", document_id="huge", source_system="scan", text="x" * (MAX_DOCUMENT_TEXT_CHARS + 1))


def test_candidate_flood_is_rejected_before_truth_construction():
    doc = DocumentInput(patient_ref="p1", document_id="flood", source_system="scan", text="x")
    candidate = ExtractedCandidate(fact_type="note", value_original="x", evidence_start=0, evidence_end=1, evidence_quote="x")
    with pytest.raises(ValueError, match="candidate count"):
        ingest_document_candidates(
            doc,
            [candidate] * (MAX_DOCUMENT_CANDIDATES + 1),
            transformer="hostile-extractor",
            transformer_version="1",
        )

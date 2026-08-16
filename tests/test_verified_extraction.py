from app.document_pipeline import DocumentInput, ExtractedCandidate
from app.extractors.base import VerifiedExtractionPipeline


class MixedExtractor:
    name = "mixed-test"
    version = "1"

    def extract(self, document):
        good_quote = "Ceftriaxon dokumentiert"
        start = document.text.index(good_quote)
        return [
            ExtractedCandidate(
                fact_type="medication.current",
                value_original="Ceftriaxon",
                evidence_start=start,
                evidence_end=start + len(good_quote),
                evidence_quote=good_quote,
            ),
            ExtractedCandidate(
                fact_type="diagnosis",
                value_original="invented diagnosis",
                evidence_start=0,
                evidence_end=5,
                evidence_quote="not in source",
            ),
        ]


def test_untrusted_extractor_only_promotes_exactly_supported_candidates():
    document = DocumentInput(patient_ref="p1", document_id="doc-1", source_system="arztbrief", text="Therapie: Ceftriaxon dokumentiert. Verlauf stabil.")
    result = VerifiedExtractionPipeline(MixedExtractor()).run(document)
    assert result.candidate_count == 2
    assert len(result.truth.facts) == 1
    assert result.truth.facts[0].fact_type == "medication.current"
    assert result.truth.provenance_coverage() == 1.0
    assert len(result.rejected) == 1
    assert result.unsupported_candidate_rate == 0.5


class EmptyExtractor:
    name = "empty"
    version = "1"

    def extract(self, document):
        return []


def test_no_candidates_is_not_treated_as_extraction_success_claim():
    document = DocumentInput(patient_ref="p1", document_id="doc-2", source_system="scan", text="Unstructured source text")
    result = VerifiedExtractionPipeline(EmptyExtractor()).run(document)
    assert result.truth.facts == []
    assert result.candidate_count == 0
    assert result.unsupported_candidate_rate == 0.0

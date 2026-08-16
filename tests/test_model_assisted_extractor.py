from app.clinical_truth import AssertionStage, FactStatus
from app.document_pipeline import DocumentInput
from app.extractors.base import VerifiedExtractionPipeline
from app.extractors.model_assisted import EvidenceFirstModelExtractor, ProposedAssertion, resolve_model_proposals


class StaticProposer:
    def __init__(self, proposals):
        self.proposals = proposals

    def propose(self, document):
        return self.proposals


def _doc(text="Blutkultur: E. coli. Status: vorläufig."):
    return DocumentInput(
        patient_ref="p1",
        document_id="d1",
        source_system="LIS",
        document_kind="microbiology",
        text=text,
    )


def test_model_quote_is_located_by_careos_not_model_offsets():
    proposal = ProposedAssertion(
        fact_type="microbiology",
        logical_key="culture-1",
        value_original="E. coli",
        evidence_quote="Blutkultur: E. coli.",
        assertion_stage=AssertionStage.PRELIMINARY,
    )
    result = resolve_model_proposals(_doc(), [proposal])
    assert len(result.candidates) == 1
    assert result.candidates[0].evidence_start == 0
    assert result.candidates[0].evidence_end == len("Blutkultur: E. coli.")


def test_missing_quote_is_rejected_not_fuzzy_matched():
    proposal = ProposedAssertion(
        fact_type="microbiology",
        value_original="E. coli",
        evidence_quote="Culture grew E coli",
    )
    result = resolve_model_proposals(_doc(), [proposal])
    assert not result.candidates
    assert result.rejected[0].reason == "evidence-missing-or-non-unique"


def test_repeated_quote_is_rejected_as_ambiguous_provenance():
    proposal = ProposedAssertion(
        fact_type="diagnosis",
        value_original="COPD",
        evidence_quote="COPD",
    )
    result = resolve_model_proposals(_doc("COPD. Vorbefund: COPD."), [proposal])
    assert not result.candidates


def test_model_effective_time_is_not_admitted_without_temporal_normalizer():
    proposal = ProposedAssertion(
        fact_type="renal_function",
        value_original={"creatinine": 1.4},
        evidence_quote="Kreatinin 1,4",
        effective_time="2026-08-15",
    )
    result = resolve_model_proposals(_doc("Kreatinin 1,4"), [proposal])
    assert not result.candidates
    assert result.rejected[0].reason == "model-effective-time-not-admitted"


def test_unknown_model_assertion_requires_reason():
    # Pydantic permits construction because ProposedAssertion is only untrusted model
    # schema; the resolver is the admission policy.
    proposal = ProposedAssertion(
        fact_type="medication",
        value_original="unclear",
        evidence_quote="Medikation unklar",
        status=FactStatus.UNKNOWN,
    )
    result = resolve_model_proposals(_doc("Medikation unklar"), [proposal])
    assert not result.candidates
    assert result.rejected[0].reason == "review-reason-required"


def test_model_adapter_still_passes_normal_exact_evidence_firewall():
    proposer = StaticProposer([ProposedAssertion(
        fact_type="microbiology",
        logical_key="culture-1",
        value_original="E. coli",
        evidence_quote="Blutkultur: E. coli.",
        assertion_stage=AssertionStage.PRELIMINARY,
    )])
    pipeline = VerifiedExtractionPipeline(EvidenceFirstModelExtractor(proposer))
    result = pipeline.run(_doc())
    assert result.provenance_coverage == 1.0
    assert result.truth.facts[0].source.document_id == "d1"
    assert result.truth.facts[0].source.evidence_span == "Blutkultur: E. coli."

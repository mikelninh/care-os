from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..clinical_truth import TruthEnvelope
from ..document_pipeline import DocumentInput, ExtractedCandidate, UnsupportedEvidence, candidate_to_fact


class DocumentExtractor(Protocol):
    name: str
    version: str

    def extract(self, document: DocumentInput) -> list[ExtractedCandidate]: ...


@dataclass(frozen=True)
class RejectedCandidate:
    index: int
    fact_type: str
    reason: str


@dataclass(frozen=True)
class VerifiedExtractionResult:
    truth: TruthEnvelope
    candidate_count: int
    rejected: tuple[RejectedCandidate, ...]

    @property
    def provenance_coverage(self) -> float:
        return self.truth.provenance_coverage()

    @property
    def unsupported_candidate_rate(self) -> float:
        if self.candidate_count == 0:
            return 0.0
        return len(self.rejected) / self.candidate_count


class VerifiedExtractionPipeline:
    """Trust boundary between an extractor/model and CareOS clinical truth.

    Extractor output is always untrusted. Each proposed fact must independently pass
    exact source-span verification and ClinicalFact validation. One bad candidate does
    not erase valid candidates, but its rejection remains measurable evidence.
    """

    def __init__(self, extractor: DocumentExtractor):
        self.extractor = extractor

    def run(self, document: DocumentInput) -> VerifiedExtractionResult:
        candidates = self.extractor.extract(document)
        facts = []
        rejected: list[RejectedCandidate] = []
        for index, candidate in enumerate(candidates):
            try:
                facts.append(candidate_to_fact(
                    document,
                    candidate,
                    transformer=self.extractor.name,
                    transformer_version=self.extractor.version,
                    ordinal=index,
                ))
            except (UnsupportedEvidence, ValueError) as exc:
                rejected.append(RejectedCandidate(index=index, fact_type=candidate.fact_type, reason=type(exc).__name__))
        return VerifiedExtractionResult(
            truth=TruthEnvelope(patient_ref=document.patient_ref, facts=facts),
            candidate_count=len(candidates),
            rejected=tuple(rejected),
        )

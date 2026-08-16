from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from .clinical_truth import ClinicalFact, FactStatus, SourceKind, SourceRef, TruthEnvelope


class DocumentInput(BaseModel):
    patient_ref: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    source_system: str = Field(min_length=1)
    text: str = Field(min_length=1)
    recorded_time: datetime | None = None


class ExtractedCandidate(BaseModel):
    """Untrusted extractor output.

    Candidates may come from a deterministic parser or model. They do not become
    clinical facts until the cited character span is proven to match the source text.
    Normalization is optional but can never replace the original source value.
    """

    fact_type: str = Field(min_length=1)
    value_original: Any
    value_normalized: Any | None = None
    evidence_start: int = Field(ge=0)
    evidence_end: int = Field(gt=0)
    evidence_quote: str = Field(min_length=1)
    effective_time: datetime | None = None
    code: str | None = None
    code_system: str | None = None
    unit_original: str | None = None
    unit_normalized: str | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    status: FactStatus = FactStatus.CONFIRMED
    review_reason: str | None = None
    contradiction_group: str | None = None

    @model_validator(mode="after")
    def validate_offsets(self) -> "ExtractedCandidate":
        if self.evidence_end <= self.evidence_start:
            raise ValueError("evidence_end must be greater than evidence_start")
        if self.value_normalized is not None and self.value_original is None:
            raise ValueError("normalized value requires original value")
        if self.unit_normalized and not self.unit_original:
            raise ValueError("normalized unit requires original unit")
        if self.status in {FactStatus.AMBIGUOUS, FactStatus.UNKNOWN} and not self.review_reason:
            raise ValueError("ambiguous/unknown candidate requires review_reason")
        return self


class UnsupportedEvidence(ValueError):
    pass


def candidate_to_fact(
    document: DocumentInput,
    candidate: ExtractedCandidate,
    *,
    transformer: str,
    transformer_version: str,
    ordinal: int = 0,
) -> ClinicalFact:
    """Promote an untrusted candidate only when its evidence is byte-for-text exact.

    The extractor is not trusted to invent or paraphrase evidence. Offsets and quote
    must match the original document exactly. This prevents unsupported generated
    claims from entering the canonical fact layer with fake provenance.
    """

    if candidate.evidence_end > len(document.text):
        raise UnsupportedEvidence("evidence span exceeds document length")
    actual = document.text[candidate.evidence_start:candidate.evidence_end]
    if actual != candidate.evidence_quote:
        raise UnsupportedEvidence("evidence quote does not exactly match source span")

    return ClinicalFact(
        fact_id=f"doc:{document.document_id}:{candidate.fact_type}:{ordinal}",
        patient_ref=document.patient_ref,
        fact_type=candidate.fact_type,
        value_original=candidate.value_original,
        value_normalized=candidate.value_normalized,
        code=candidate.code,
        code_system=candidate.code_system,
        unit_original=candidate.unit_original,
        unit_normalized=candidate.unit_normalized,
        effective_time=candidate.effective_time,
        recorded_time=document.recorded_time,
        source=SourceRef(
            kind=SourceKind.DOCUMENT,
            system=document.source_system,
            document_id=document.document_id,
            evidence_span=candidate.evidence_quote,
        ),
        transformer=transformer,
        transformer_version=transformer_version,
        confidence=candidate.confidence,
        status=candidate.status,
        contradiction_group=candidate.contradiction_group,
        review_reason=candidate.review_reason,
    )


def ingest_document_candidates(
    document: DocumentInput,
    candidates: list[ExtractedCandidate],
    *,
    transformer: str,
    transformer_version: str,
) -> TruthEnvelope:
    facts = [
        candidate_to_fact(
            document,
            candidate,
            transformer=transformer,
            transformer_version=transformer_version,
            ordinal=i,
        )
        for i, candidate in enumerate(candidates)
    ]
    return TruthEnvelope(patient_ref=document.patient_ref, facts=facts)

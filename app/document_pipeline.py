from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from .clinical_truth import (
    AssertionStage,
    ClinicalFact,
    FactStatus,
    SourceKind,
    SourceRef,
    TruthEnvelope,
)

MAX_DOCUMENT_TEXT_CHARS = 5_000_000
MAX_DOCUMENT_CANDIDATES = 1_000


class DocumentInput(BaseModel):
    patient_ref: str = Field(min_length=1, max_length=256)
    document_id: str = Field(min_length=1, max_length=256)
    source_system: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=MAX_DOCUMENT_TEXT_CHARS)
    document_kind: str | None = Field(default=None, max_length=128)
    recorded_time: datetime | None = None


class ExtractedCandidate(BaseModel):
    """Untrusted extractor output; exact source evidence is mandatory for promotion."""

    fact_type: str = Field(min_length=1, max_length=256)
    logical_key: str | None = Field(default=None, max_length=512)
    value_original: Any
    value_normalized: Any | None = None
    evidence_start: int = Field(ge=0)
    evidence_end: int = Field(gt=0)
    evidence_quote: str = Field(min_length=1, max_length=100_000)
    effective_time: datetime | None = None
    code: str | None = Field(default=None, max_length=256)
    code_system: str | None = Field(default=None, max_length=1_000)
    unit_original: str | None = Field(default=None, max_length=256)
    unit_normalized: str | None = Field(default=None, max_length=256)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    status: FactStatus = FactStatus.CONFIRMED
    assertion_stage: AssertionStage = AssertionStage.UNKNOWN
    review_reason: str | None = Field(default=None, max_length=2_000)
    contradiction_group: str | None = Field(default=None, max_length=512)
    supersedes_fact_id: str | None = Field(default=None, max_length=512)
    blocks_fact_types: tuple[str, ...] = Field(default=(), max_length=100)

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
        if self.blocks_fact_types and self.status == FactStatus.CONFIRMED:
            raise ValueError("review barriers must be ambiguous/unknown")
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
    if candidate.evidence_end > len(document.text):
        raise UnsupportedEvidence("evidence span exceeds document length")
    actual = document.text[candidate.evidence_start:candidate.evidence_end]
    if actual != candidate.evidence_quote:
        raise UnsupportedEvidence("evidence quote does not exactly match source span")

    return ClinicalFact(
        fact_id=f"doc:{document.document_id}:{candidate.fact_type}:{ordinal}",
        patient_ref=document.patient_ref,
        fact_type=candidate.fact_type,
        logical_key=candidate.logical_key,
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
        assertion_stage=candidate.assertion_stage,
        contradiction_group=candidate.contradiction_group,
        supersedes_fact_id=candidate.supersedes_fact_id,
        blocks_fact_types=candidate.blocks_fact_types,
        review_reason=candidate.review_reason,
    )


def ingest_document_candidates(
    document: DocumentInput,
    candidates: list[ExtractedCandidate],
    *,
    transformer: str,
    transformer_version: str,
) -> TruthEnvelope:
    if len(candidates) > MAX_DOCUMENT_CANDIDATES:
        raise ValueError("document candidate count exceeds configured limit")
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

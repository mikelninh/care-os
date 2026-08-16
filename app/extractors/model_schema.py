from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..clinical_truth import FactStatus
from ..document_pipeline import ExtractedCandidate


class ModelCandidate(BaseModel):
    """Provider-neutral structured output expected from a document model.

    The model is explicitly not authoritative. Its offsets/quote are checked against
    the original document by VerifiedExtractionPipeline before promotion to truth.
    """

    fact_type: str = Field(min_length=1)
    value_original: Any
    evidence_start: int = Field(ge=0)
    evidence_end: int = Field(gt=0)
    evidence_quote: str = Field(min_length=1)
    effective_time: str | None = None
    code: str | None = None
    code_system: str | None = None
    unit_original: str | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    status: FactStatus = FactStatus.CONFIRMED
    review_reason: str | None = None
    contradiction_group: str | None = None

    def to_candidate(self) -> ExtractedCandidate:
        return ExtractedCandidate.model_validate(self.model_dump())


class ModelExtractionResponse(BaseModel):
    candidates: list[ModelCandidate] = Field(default_factory=list)


MODEL_EXTRACTION_RULES = (
    "Return only facts directly supported by the supplied document. "
    "For every candidate, evidence_start/evidence_end must identify an exact verbatim "
    "evidence_quote in the original document. Do not paraphrase the evidence. "
    "If a safety-critical value is uncertain, emit status=ambiguous or unknown with a "
    "review_reason, or omit it. Do not infer a missing diagnosis, medication, allergy, "
    "date, negation state, or contradiction from general medical knowledge. "
    "Never resolve contradictory sources; source comparison happens downstream."
)

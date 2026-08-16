from __future__ import annotations

from pydantic import BaseModel, Field

from .model_assisted import ProposedAssertion


# Backwards-facing name for callers, but the contract is now quote-only: the model
# never supplies authoritative character offsets. CareOS locates unique exact quotes.
ModelCandidate = ProposedAssertion


class ModelExtractionResponse(BaseModel):
    candidates: list[ModelCandidate] = Field(default_factory=list)


MODEL_EXTRACTION_RULES = (
    "Return only facts directly supported by the supplied document. "
    "For every candidate, evidence_quote must be an exact verbatim quote copied from "
    "the original document. Do not return or infer character offsets; CareOS resolves "
    "the quote to a unique span independently. Do not paraphrase the evidence. "
    "Do not invent clinical effective time; temporal normalization happens in a "
    "separate governed layer. If a safety-critical value is uncertain, emit "
    "status=ambiguous or unknown with a review_reason, or omit it. Do not infer a "
    "missing diagnosis, medication, allergy, date, negation state, or contradiction "
    "from general medical knowledge. Never resolve contradictory sources; source "
    "comparison happens downstream in deterministic reconciliation."
)

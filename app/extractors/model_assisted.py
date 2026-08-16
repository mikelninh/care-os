from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel, Field

from ..clinical_truth import AssertionStage, FactStatus
from ..document_pipeline import DocumentInput, ExtractedCandidate


class ProposedAssertion(BaseModel):
    """Untrusted structured assertion proposed by a model.

    The model is asked for the exact supporting quote, not trusted character offsets.
    CareOS independently locates that quote in the immutable source text. Missing or
    non-unique evidence is rejected before the normal candidate evidence firewall.
    """

    fact_type: str = Field(min_length=1)
    logical_key: str | None = None
    value_original: Any
    evidence_quote: str = Field(min_length=1)
    effective_time: str | None = None
    code: str | None = None
    code_system: str | None = None
    unit_original: str | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    assertion_stage: AssertionStage = AssertionStage.UNKNOWN
    status: FactStatus = FactStatus.CONFIRMED
    review_reason: str | None = None
    blocks_fact_types: tuple[str, ...] = ()


class ModelProposer(Protocol):
    def propose(self, document: DocumentInput) -> list[ProposedAssertion]: ...


@dataclass(frozen=True)
class ProposalRejection:
    index: int
    reason: str


@dataclass(frozen=True)
class ProposalResolution:
    candidates: tuple[ExtractedCandidate, ...]
    rejected: tuple[ProposalRejection, ...]


def _unique_span(text: str, quote: str) -> tuple[int, int] | None:
    first = text.find(quote)
    if first < 0:
        return None
    second = text.find(quote, first + 1)
    if second >= 0:
        return None
    return first, first + len(quote)


def resolve_model_proposals(document: DocumentInput, proposals: list[ProposedAssertion]) -> ProposalResolution:
    """Convert model proposals to candidates only when evidence is uniquely grounded.

    No fuzzy matching, paraphrase matching or LLM self-verification is permitted here.
    A quote must exist exactly once in the original source. Effective-time strings are
    not parsed/guessed by this layer; a separate governed temporal normalizer may add
    them later.
    """

    candidates: list[ExtractedCandidate] = []
    rejected: list[ProposalRejection] = []

    for index, proposal in enumerate(proposals):
        span = _unique_span(document.text, proposal.evidence_quote)
        if span is None:
            rejected.append(ProposalRejection(index=index, reason="evidence-missing-or-non-unique"))
            continue
        if proposal.effective_time is not None:
            # Do not let a model-invented date silently enter clinical time. The model
            # may point to date evidence as another assertion; parsing belongs to the
            # deterministic temporal layer.
            rejected.append(ProposalRejection(index=index, reason="model-effective-time-not-admitted"))
            continue
        if proposal.status in {FactStatus.AMBIGUOUS, FactStatus.UNKNOWN} and not proposal.review_reason:
            rejected.append(ProposalRejection(index=index, reason="review-reason-required"))
            continue

        start, end = span
        candidates.append(ExtractedCandidate(
            fact_type=proposal.fact_type,
            logical_key=proposal.logical_key,
            value_original=proposal.value_original,
            evidence_start=start,
            evidence_end=end,
            evidence_quote=proposal.evidence_quote,
            effective_time=document.recorded_time,
            code=proposal.code,
            code_system=proposal.code_system,
            unit_original=proposal.unit_original,
            confidence=proposal.confidence,
            assertion_stage=proposal.assertion_stage,
            status=proposal.status,
            review_reason=proposal.review_reason,
            blocks_fact_types=proposal.blocks_fact_types,
        ))

    return ProposalResolution(tuple(candidates), tuple(rejected))


class EvidenceFirstModelExtractor:
    """Adapter that lets any LLM/provider propose assertions without becoming trusted.

    Provider/network/model selection is intentionally outside this module. That keeps
    the clinical truth boundary testable and allows a hospital-approved local model or
    cloud model to be swapped without changing CareOS truth semantics.
    """

    name = "evidence-first-model"
    version = "0.1.0"

    def __init__(self, proposer: ModelProposer):
        self.proposer = proposer
        self.last_rejections: tuple[ProposalRejection, ...] = ()

    def extract(self, document: DocumentInput) -> list[ExtractedCandidate]:
        resolved = resolve_model_proposals(document, self.proposer.propose(document))
        self.last_rejections = resolved.rejected
        return list(resolved.candidates)

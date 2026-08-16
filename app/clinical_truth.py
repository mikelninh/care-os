from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class FactStatus(str, Enum):
    CONFIRMED = "confirmed"
    AMBIGUOUS = "ambiguous"
    UNKNOWN = "unknown"
    REJECTED = "rejected"


class AssertionStage(str, Enum):
    """Maturity of the source assertion, independent from model confidence."""

    UNKNOWN = "unknown"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"


class SourceKind(str, Enum):
    FHIR = "fhir"
    STRUCTURED_VENDOR = "structured-vendor"
    DOCUMENT = "document"
    MANUAL = "manual"


class SourceRef(BaseModel):
    """Immutable locator for the source that supports a clinical fact."""

    kind: SourceKind
    system: str = Field(min_length=1)
    resource_type: str | None = None
    resource_id: str | None = None
    resource_version: str | None = None
    document_id: str | None = None
    evidence_span: str | None = None
    source_url: str | None = None

    @model_validator(mode="after")
    def validate_locator(self) -> "SourceRef":
        has_resource = bool(self.resource_type and self.resource_id)
        has_document = bool(self.document_id)
        if not (has_resource or has_document):
            raise ValueError("source must identify a structured resource or document")
        if self.kind == SourceKind.DOCUMENT and not (self.document_id and self.evidence_span):
            raise ValueError("document-derived facts require document_id + exact evidence_span")
        return self


class ClinicalFact(BaseModel):
    """Canonical, source-grounded fact used by CareOS downstream views.

    Clinical time, source maturity, extraction confidence and review state are
    deliberately separate dimensions. `blocks_fact_types` is used only for explicit
    review barriers: e.g. an unparsed newer lab document can prevent an older renal
    value from being misrepresented as the current state.
    """

    fact_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    fact_type: str = Field(min_length=1)
    logical_key: str | None = None

    value_original: Any
    value_normalized: Any | None = None
    code: str | None = None
    code_system: str | None = None
    unit_original: str | None = None
    unit_normalized: str | None = None

    effective_time: datetime | None = None
    recorded_time: datetime | None = None
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    source: SourceRef
    transformer: str = Field(default="source-native", min_length=1)
    transformer_version: str = Field(default="1", min_length=1)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    status: FactStatus = FactStatus.CONFIRMED
    assertion_stage: AssertionStage = AssertionStage.UNKNOWN

    contradiction_group: str | None = None
    supersedes_fact_id: str | None = None
    blocks_fact_types: tuple[str, ...] = ()
    review_reason: str | None = None

    @model_validator(mode="after")
    def validate_semantics(self) -> "ClinicalFact":
        if self.value_normalized is not None and self.value_original is None:
            raise ValueError("normalized values may never replace the original value")
        if self.unit_normalized and not self.unit_original:
            raise ValueError("normalized units require the original unit")
        if self.status in {FactStatus.AMBIGUOUS, FactStatus.UNKNOWN} and not self.review_reason:
            raise ValueError("ambiguous/unknown facts require an explicit review_reason")
        if self.supersedes_fact_id == self.fact_id:
            raise ValueError("a fact cannot supersede itself")
        if self.blocks_fact_types and self.status == FactStatus.CONFIRMED:
            raise ValueError("review barriers must not be confirmed facts")
        return self

    @property
    def provenance_complete(self) -> bool:
        if self.source.kind == SourceKind.DOCUMENT:
            return bool(self.source.document_id and self.source.evidence_span)
        return bool(self.source.resource_type and self.source.resource_id)

    @property
    def reconciliation_key(self) -> str:
        if self.logical_key:
            return self.logical_key
        if self.code and self.code_system:
            return f"{self.fact_type}|{self.code_system}|{self.code}"
        return self.fact_type

    @property
    def safe_default_surface(self) -> bool:
        return (
            self.status == FactStatus.CONFIRMED
            and self.provenance_complete
            and self.assertion_stage != AssertionStage.CANCELLED
        )


class TruthEnvelope(BaseModel):
    patient_ref: str = Field(min_length=1)
    facts: list[ClinicalFact]

    @model_validator(mode="after")
    def validate_patient_and_ids(self) -> "TruthEnvelope":
        ids = [f.fact_id for f in self.facts]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate fact_id in truth envelope")
        wrong_patient = [f.fact_id for f in self.facts if f.patient_ref != self.patient_ref]
        if wrong_patient:
            raise ValueError(f"cross-patient facts rejected: {wrong_patient}")
        # supersedes_fact_id may point across source envelopes; reconciliation validates it.
        return self

    def provenance_coverage(self) -> float:
        if not self.facts:
            return 1.0
        return sum(1 for f in self.facts if f.provenance_complete) / len(self.facts)

    def review_queue(self) -> list[ClinicalFact]:
        return [f for f in self.facts if not f.safe_default_surface]

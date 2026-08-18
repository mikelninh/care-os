from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ClinicalState(str, Enum):
    FINAL = "final"
    PRELIMINARY = "preliminary"
    PENDING = "pending"
    STALE = "stale"
    CONTRADICTORY = "contradictory"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class TrustState(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class Coding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system: str = Field(min_length=1)
    code: str = Field(min_length=1)
    display: str | None = None
    version: str | None = None


class TranslationPresentation(BaseModel):
    """A translated presentation may never replace the source clinical wording."""

    model_config = ConfigDict(extra="forbid")

    language: str = Field(min_length=2, max_length=35)
    text: str = Field(min_length=1)
    method: Literal["human", "machine", "terminology-rendering", "not-translated"]
    method_version: str | None = None
    reviewed_by_human: bool = False


class PortableClinicalItem(BaseModel):
    """Portable clinical meaning with state/time/provenance kept explicit."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1)
    category: str = Field(min_length=1)
    original_text: str = Field(min_length=1)
    original_language: str = Field(min_length=2, max_length=35)
    clinical_state: ClinicalState
    source_ref: str = Field(min_length=1)
    source_organisation: str = Field(min_length=1)
    effective_time: datetime | None = None
    recorded_time: datetime | None = None
    coding_original: list[Coding] = Field(default_factory=list)
    coding_mapped: list[Coding] = Field(default_factory=list)
    presentation: list[TranslationPresentation] = Field(default_factory=list)
    requires_review: bool = False

    @model_validator(mode="after")
    def safety_state_requires_review(self) -> "PortableClinicalItem":
        if self.clinical_state in {
            ClinicalState.PENDING,
            ClinicalState.STALE,
            ClinicalState.CONTRADICTORY,
            ClinicalState.UNAVAILABLE,
            ClinicalState.UNKNOWN,
        } and not self.requires_review:
            raise ValueError("non-final/safety-sensitive portable clinical state must require review")
        return self


class IssuerEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issuer_id: str = Field(min_length=1)
    issuer_name: str = Field(min_length=1)
    trust_state: TrustState = TrustState.UNVERIFIED
    trust_framework: str | None = None
    signature_format: str | None = None
    verification_time: datetime | None = None
    verification_reason: str = Field(default="prototype has no cross-border issuer verification")


class GlobalPortabilityEnvelope(BaseModel):
    """Country-neutral minimum continuity-of-care envelope.

    This is not an IPS conformance model. `ips_profile_hint` records the intended
    standards path while keeping the prototype's conformance state explicit.
    """

    model_config = ConfigDict(extra="forbid")

    envelope_version: str = "0.1.0"
    subject_ref: str = Field(min_length=1)
    origin_country: str = Field(min_length=2, max_length=3)
    target_country: str = Field(min_length=2, max_length=3)
    intended_use: Literal["unplanned-care", "planned-transfer", "patient-held-copy"]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    presentation_language: str = Field(default="en", min_length=2, max_length=35)
    ips_profile_hint: str = "http://hl7.org/fhir/uv/ips/ImplementationGuide/hl7.fhir.uv.ips"
    ips_conformance: Literal["not-validated", "validated"] = "not-validated"
    issuer: IssuerEvidence
    items: list[PortableClinicalItem] = Field(default_factory=list)
    policy: dict[str, bool | str] = Field(default_factory=lambda: {
        "original_clinical_text_preserved": True,
        "translation_may_change_presentation_only": True,
        "clinical_state_must_survive_mapping": True,
        "unverified_issuer_must_be_visible": True,
        "receiving_jurisdiction_controls_use": True,
    })


def synthetic_cross_border_envelope(
    *, target_country: str = "VN", presentation_language: str = "vi"
) -> GlobalPortabilityEnvelope:
    """Synthetic Berlin -> foreign care example for interoperability regression tests."""

    origin = "DE"
    items = [
        PortableClinicalItem(
            item_id="allergy-1",
            category="allergy",
            original_text="Penicillin: Urtikaria dokumentiert; ältere Entlassung nennt keine Allergien.",
            original_language="de",
            clinical_state=ClinicalState.CONTRADICTORY,
            source_ref="KIS:ALLERGY-71 + DOC:2024-02-12",
            source_organisation="DEMO Berlin Hospital",
            presentation=[TranslationPresentation(
                language=presentation_language,
                text="Penicillin allergy conflict — verify original German sources before use.",
                method="machine" if presentation_language != "de" else "not-translated",
                method_version="synthetic-demo-1",
                reviewed_by_human=False,
            )],
            requires_review=True,
        ),
        PortableClinicalItem(
            item_id="micro-1",
            category="microbiology",
            original_text="Finales Resistogramm ausstehend.",
            original_language="de",
            clinical_state=ClinicalState.PENDING,
            source_ref="LIS:BC-1842:FINAL",
            source_organisation="DEMO Berlin Hospital",
            presentation=[TranslationPresentation(
                language=presentation_language,
                text="Final antimicrobial susceptibility result is pending — not negative.",
                method="machine" if presentation_language != "de" else "not-translated",
                method_version="synthetic-demo-1",
                reviewed_by_human=False,
            )],
            requires_review=True,
        ),
        PortableClinicalItem(
            item_id="med-1",
            category="medication",
            original_text="Ceftriaxon 2 g i.v. als aktuelle Medikation dokumentiert.",
            original_language="de",
            clinical_state=ClinicalState.FINAL,
            source_ref="KIS:MED-922",
            source_organisation="DEMO Berlin Hospital",
            presentation=[TranslationPresentation(
                language=presentation_language,
                text="Ceftriaxone 2 g IV documented as current medication; not an AI recommendation.",
                method="machine" if presentation_language != "de" else "not-translated",
                method_version="synthetic-demo-1",
                reviewed_by_human=False,
            )],
            requires_review=False,
        ),
    ]
    return GlobalPortabilityEnvelope(
        subject_ref="SYNTHETIC-DEMO-1842",
        origin_country=origin,
        target_country=target_country.upper(),
        intended_use="unplanned-care",
        presentation_language=presentation_language,
        issuer=IssuerEvidence(
            issuer_id="demo-berlin-hospital",
            issuer_name="DEMO Berlin Hospital",
            trust_state=TrustState.UNVERIFIED,
            trust_framework="future-EHDS/WHO-GDHCN-compatible-boundary",
            verification_reason="synthetic prototype; no real issuer signature or trust-network verification",
        ),
        items=items,
    )

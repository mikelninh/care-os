from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PatientItemState(str, Enum):
    FINAL = "final"
    PRELIMINARY = "preliminary"
    PENDING = "pending"
    CORRECTED = "corrected"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class PatientAgentCapability(str, Enum):
    EXPLAIN = "explain"
    TRANSLATE_PRESENTATION = "translate-presentation"
    FIND_SOURCE = "find-source"
    PREPARE_QUESTIONS = "prepare-questions"


class PatientFacingItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1)
    category: str = Field(min_length=1)
    original_text: str = Field(min_length=1)
    original_language: str = Field(min_length=2)
    plain_language: str = Field(min_length=1)
    state: PatientItemState
    source_ref: str = Field(min_length=1)
    source_label: str = Field(min_length=1)
    owner: str | None = None
    next_step: str | None = None
    requires_attention: bool = False

    @model_validator(mode="after")
    def uncertainty_must_remain_visible(self) -> "PatientFacingItem":
        if self.state in {
            PatientItemState.PRELIMINARY,
            PatientItemState.PENDING,
            PatientItemState.UNAVAILABLE,
            PatientItemState.UNKNOWN,
        } and not self.requires_attention:
            raise ValueError("uncertain/pending/unavailable patient items must require attention")
        if self.state in {PatientItemState.PENDING, PatientItemState.UNAVAILABLE} and not self.next_step:
            raise ValueError("pending/unavailable patient items must say what happens next")
        return self


class MedicationChange(BaseModel):
    medication: str = Field(min_length=1)
    previous: str | None = None
    current: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    explanation: str = Field(min_length=1)


class ProxyGrant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    grant_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    proxy_ref: str = Field(min_length=1)
    scopes: tuple[str, ...]
    expires_at: datetime | None = None
    revoked: bool = False

    def active(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return not self.revoked and (self.expires_at is None or self.expires_at > now)


class PatientView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patient_ref: str = Field(min_length=1)
    happened: tuple[PatientFacingItem, ...] = ()
    changed: tuple[PatientFacingItem, ...] = ()
    pending: tuple[PatientFacingItem, ...] = ()
    medication_changes: tuple[MedicationChange, ...] = ()
    follow_up: tuple[PatientFacingItem, ...] = ()
    agent_capabilities: tuple[PatientAgentCapability, ...] = tuple(PatientAgentCapability)

    @model_validator(mode="after")
    def pending_section_contains_only_nonfinal_work(self) -> "PatientView":
        invalid = [item.item_id for item in self.pending if item.state not in {PatientItemState.PENDING, PatientItemState.PRELIMINARY, PatientItemState.UNAVAILABLE, PatientItemState.UNKNOWN}]
        if invalid:
            raise ValueError(f"patient pending section contains final items: {invalid}")
        return self


class TeachBackCheck(BaseModel):
    id: str
    prompt: str
    expected_concept: str


def default_teach_back(view: PatientView) -> list[TeachBackCheck]:
    checks = [
        TeachBackCheck(
            id="pending",
            prompt="What are we still waiting for, and who owns the next step?",
            expected_concept="pending state + owner/next step",
        ),
        TeachBackCheck(
            id="medication",
            prompt="What medication changed, if anything?",
            expected_concept="medication change from source-linked record",
        ),
        TeachBackCheck(
            id="follow-up",
            prompt="What happens next after discharge or this visit?",
            expected_concept="follow-up action + responsible service/date where known",
        ),
    ]
    if not view.medication_changes:
        checks[1] = TeachBackCheck(
            id="medication",
            prompt="Were any medication changes shown in this view?",
            expected_concept="no medication change displayed; do not infer beyond source record",
        )
    return checks


def synthetic_patient_view() -> PatientView:
    return PatientView(
        patient_ref="synthetic-patient-001",
        happened=(
            PatientFacingItem(
                item_id="event-1",
                category="hospital-stay",
                original_text="Aufnahme wegen Fieber bei immunsupprimiertem Patienten.",
                original_language="de",
                plain_language="You were admitted because of fever while your immune system is weakened.",
                state=PatientItemState.FINAL,
                source_ref="doc:admission-1",
                source_label="Admission note · synthetic",
            ),
        ),
        changed=(
            PatientFacingItem(
                item_id="change-1",
                category="microbiology",
                original_text="Blutkultur: Wachstum; finale Speziesbestimmung ausstehend.",
                original_language="de",
                plain_language="A blood culture is growing something, but the final identification is not ready yet.",
                state=PatientItemState.PRELIMINARY,
                source_ref="lis:culture-17",
                source_label="Microbiology · synthetic",
                owner="Microbiology laboratory",
                next_step="Final identification will replace this preliminary result when available.",
                requires_attention=True,
            ),
        ),
        pending=(
            PatientFacingItem(
                item_id="pending-1",
                category="microbiology",
                original_text="Resistenztestung ausstehend.",
                original_language="de",
                plain_language="The laboratory is still testing which medicines the organism is sensitive to.",
                state=PatientItemState.PENDING,
                source_ref="lis:susceptibility-17",
                source_label="Microbiology · synthetic",
                owner="Microbiology laboratory",
                next_step="The treating team reviews the final result when the laboratory releases it.",
                requires_attention=True,
            ),
        ),
        medication_changes=(
            MedicationChange(
                medication="Synthetic antibiotic A",
                previous="not documented in this synthetic episode",
                current="documented as active therapy",
                source_ref="kis:med-23",
                explanation="This view reports what the hospital record currently documents; it is not an AI recommendation.",
            ),
        ),
        follow_up=(
            PatientFacingItem(
                item_id="follow-1",
                category="follow-up",
                original_text="Kontrolle nach finalem mikrobiologischen Befund.",
                original_language="de",
                plain_language="The team plans to review the final microbiology result after it is released.",
                state=PatientItemState.FINAL,
                source_ref="kis:plan-7",
                source_label="Documented plan · synthetic",
                owner="Treating team",
                next_step="Ask the treating team how you will receive the final result if you leave before it is available.",
            ),
        ),
    )

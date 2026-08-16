from __future__ import annotations

import re
from datetime import datetime

from ..clinical_truth import AssertionStage, FactStatus
from ..document_pipeline import DocumentInput, ExtractedCandidate


class ConservativeGermanExtractor:
    """Conservative development extractor for explicit German clinical statements.

    Every supported document kind fails visibly. Snapshot-like unresolved sources can
    block older state; additive allergy history stays visible while the unresolved
    allergy source is separately flagged for review.
    """

    name = "conservative-de"
    version = "0.3.2"

    SUPPORTED_KINDS = {"allergy", "medication", "diagnosis", "lab", "followup", "discharge"}
    REVIEW_BLOCKS = {
        "allergy": (),
        "medication": ("current_medications", "new_medication_order"),
        "diagnosis": ("relevant_diagnoses",),
        "lab": ("renal_function",),
        "followup": ("open_followups",),
        "discharge": ("discharge",),
    }

    def extract(self, document: DocumentInput) -> list[ExtractedCandidate]:
        kind = (document.document_kind or "").lower()
        parser = {
            "allergy": self._allergy,
            "medication": self._medication,
            "diagnosis": self._diagnosis,
            "lab": self._lab,
            "followup": self._followup,
            "discharge": self._discharge,
        }.get(kind)

        candidates = parser(document) if parser else []
        if not candidates and kind in self.SUPPORTED_KINDS:
            return [self._review_required(document, f"unsupported explicit {kind} document form")]
        return candidates

    @staticmethod
    def _assertion_stage(text: str) -> AssertionStage:
        lower = text.lower()
        if any(token in lower for token in ("korrigiert", "korrektur", "berichtigt")):
            return AssertionStage.CORRECTED
        if any(token in lower for token in ("storniert", "zurückgezogen", "ungueltig", "ungültig")):
            return AssertionStage.CANCELLED
        if any(token in lower for token in ("final", "endgültig", "endgueltig", "abschließend", "abschliessend")):
            return AssertionStage.FINAL
        if any(token in lower for token in ("vorläufig", "vorlaeufig", "vorab", "pending", "ausstehend")):
            return AssertionStage.PRELIMINARY
        return AssertionStage.UNKNOWN

    @classmethod
    def _candidate(
        cls,
        document: DocumentInput,
        *,
        match: re.Match[str],
        fact_type: str,
        value_original,
        logical_key: str | None = None,
        value_normalized=None,
        unit_original: str | None = None,
        unit_normalized: str | None = None,
        effective_time: datetime | None = None,
        status: FactStatus = FactStatus.CONFIRMED,
        review_reason: str | None = None,
        confidence: float = 1.0,
        assertion_stage: AssertionStage | None = None,
    ) -> ExtractedCandidate:
        start, end = match.span()
        return ExtractedCandidate(
            fact_type=fact_type,
            logical_key=logical_key,
            value_original=value_original,
            value_normalized=value_normalized,
            evidence_start=start,
            evidence_end=end,
            evidence_quote=document.text[start:end],
            effective_time=effective_time or document.recorded_time,
            unit_original=unit_original,
            unit_normalized=unit_normalized,
            confidence=confidence,
            status=status,
            assertion_stage=assertion_stage or cls._assertion_stage(document.text),
            review_reason=review_reason,
        )

    def _review_required(self, document: DocumentInput, reason: str) -> ExtractedCandidate:
        kind = (document.document_kind or "").lower()
        return ExtractedCandidate(
            fact_type="review_required",
            logical_key=f"review:{document.document_id}",
            value_original={"document_kind": document.document_kind, "reason": reason},
            evidence_start=0,
            evidence_end=len(document.text),
            evidence_quote=document.text,
            effective_time=document.recorded_time,
            confidence=0.0,
            status=FactStatus.UNKNOWN,
            assertion_stage=self._assertion_stage(document.text),
            blocks_fact_types=self.REVIEW_BLOCKS.get(kind, ()),
            review_reason=reason,
        )

    def _allergy(self, document: DocumentInput) -> list[ExtractedCandidate]:
        match = re.search(r"Allergie:\s*([^\.\n]+?)(?:\.\s*|\s+)Reaktion:\s*([^\.\n]+)\.", document.text, flags=re.IGNORECASE)
        if not match:
            return []
        substance = match.group(1).strip()
        value = {"substance": substance, "reaction": match.group(2).strip()}
        return [self._candidate(document, match=match, fact_type="allergy", logical_key=f"allergy:{substance.casefold()}", value_original=value)]

    def _medication(self, document: DocumentInput) -> list[ExtractedCandidate]:
        out: list[ExtractedCandidate] = []
        current = re.search(r"Aktuelle Medikation:\s*([^\.]+)\.", document.text, flags=re.IGNORECASE)
        if current:
            medicines = [item.strip() for item in re.split(r"[,;]", current.group(1)) if item.strip()]
            out.append(self._candidate(document, match=current, fact_type="current_medications", logical_key="medication-list", value_original=medicines))
        new_order = re.search(r"Neu verordnet:\s*([^\.]+)\.\s*Bitte heute beginnen\.", document.text, flags=re.IGNORECASE)
        if new_order:
            medication = new_order.group(1).strip()
            out.append(self._candidate(document, match=new_order, fact_type="new_medication_order", logical_key=f"medication-order:{medication.casefold()}", value_original=medication))
        return out

    def _diagnosis(self, document: DocumentInput) -> list[ExtractedCandidate]:
        match = re.search(r"Relevante Diagnosen:\s*([^\.]+(?:\.[^\.]*)?)\.", document.text, flags=re.IGNORECASE)
        if not match:
            return []
        diagnoses = [item.strip() for item in match.group(1).split(";") if item.strip()]
        return [self._candidate(document, match=match, fact_type="relevant_diagnoses", logical_key="relevant-diagnoses", value_original=diagnoses)]

    def _lab(self, document: DocumentInput) -> list[ExtractedCandidate]:
        match = re.search(r"(?:Krea|Kreatinin):?\s*([0-9]+(?:[\.,][0-9]+)?)\s*mg/dl\s*(?:·|,|\n)\s*eGFR:?\s*([0-9]+)\s*ml/min/1,73m²\. ?", document.text, flags=re.IGNORECASE)
        if not match:
            return []
        creatinine = float(match.group(1).replace(",", "."))
        egfr = int(match.group(2))
        return [self._candidate(document, match=match, fact_type="renal_function", logical_key="renal-function", value_original={"creatinine": creatinine, "egfr": egfr}, unit_original="mg/dl + ml/min/1.73m2")]

    def _followup(self, document: DocumentInput) -> list[ExtractedCandidate]:
        match = re.search(r"Offen:\s*([^\.]+(?:\.[^\.]*)?)\.", document.text, flags=re.IGNORECASE)
        if not match:
            return []
        items = [item.strip() for item in match.group(1).split(";") if item.strip()]
        return [self._candidate(document, match=match, fact_type="open_followups", logical_key="open-followups", value_original=items)]

    def _discharge(self, document: DocumentInput) -> list[ExtractedCandidate]:
        planned = re.search(r"Entlassung geplant für:?\s*(\d{4}-\d{2}-\d{2})\.\s*Entlassbrief noch nicht freigegeben\.", document.text, flags=re.IGNORECASE)
        if planned:
            return [self._candidate(document, match=planned, fact_type="discharge", logical_key="discharge-state", value_original={"status": "planned", "date": planned.group(1)}, assertion_stage=AssertionStage.PRELIMINARY)]
        completed = re.search(r"Entlassen am:?\s*(\d{4}-\d{2}-\d{2})\.\s*Entlassbrief final freigegeben\.", document.text, flags=re.IGNORECASE)
        if completed:
            return [self._candidate(document, match=completed, fact_type="discharge", logical_key="discharge-state", value_original={"status": "completed", "date": completed.group(1)}, assertion_stage=AssertionStage.FINAL)]
        return []

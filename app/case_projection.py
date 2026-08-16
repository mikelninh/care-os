from __future__ import annotations

from dataclasses import dataclass, field

from .clinical_truth import ClinicalFact, TruthEnvelope
from .reconciliation import ReconciliationResult, reconcile_truth


FACT_TO_FIELD = {
    "allergy": "allergies",
    "current_medications": "current_medications",
    "new_medication_order": "current_medications",
    "relevant_diagnoses": "relevant_diagnoses",
    "renal_function": "last_renal_function",
    "open_followups": "open_followups",
    "discharge": "discharge",
}

DOCUMENT_KIND_TO_FIELD = {
    "allergy": "allergies",
    "medication": "current_medications",
    "diagnosis": "relevant_diagnoses",
    "lab": "last_renal_function",
    "followup": "open_followups",
    "discharge": "discharge",
}


@dataclass
class CaseProjection:
    patient_ref: str
    allergies: list[dict] = field(default_factory=list)
    current_medications: list[str] = field(default_factory=list)
    relevant_diagnoses: list[str] = field(default_factory=list)
    last_renal_function: dict | None = None
    open_followups: list[str] = field(default_factory=list)
    discharge: dict = field(default_factory=lambda: {"status": "none", "date": None})
    provenance: dict[str, str | None] = field(default_factory=lambda: {
        "allergy": None,
        "current_medication": None,
        "diagnoses": None,
        "last_renal_function": None,
        "open_followups": None,
        "discharge": None,
    })
    review_required: list[str] = field(default_factory=list)
    unknown_fields: list[str] = field(default_factory=list)
    reconciliation_issues: list[dict] = field(default_factory=list)


def _source_id(fact: ClinicalFact) -> str | None:
    return fact.source.document_id or fact.source.resource_id


def _review_fields(fact: ClinicalFact) -> set[str]:
    fields = {FACT_TO_FIELD[x] for x in fact.blocks_fact_types if x in FACT_TO_FIELD}
    if fact.fact_type == "review_required" and isinstance(fact.value_original, dict):
        kind = str(fact.value_original.get("document_kind") or "").lower()
        if kind in DOCUMENT_KIND_TO_FIELD:
            fields.add(DOCUMENT_KIND_TO_FIELD[kind])
    elif fact.fact_type in FACT_TO_FIELD:
        fields.add(FACT_TO_FIELD[fact.fact_type])
    return fields


def project_case(envelopes: list[TruthEnvelope]) -> tuple[CaseProjection, ReconciliationResult]:
    """Render UI/benchmark context only after truth reconciliation.

    Explicit abstention maps to the same public field names used by evaluation and UI,
    so a visible `unknown/review` state can never be miscounted as a silent omission.
    """

    reconciled = reconcile_truth(envelopes)
    out = CaseProjection(patient_ref=reconciled.patient_ref)

    for fact in reconciled.review:
        source_id = _source_id(fact)
        if source_id:
            out.review_required.append(source_id)
        out.unknown_fields.extend(_review_fields(fact))

    for issue in reconciled.issues:
        out.reconciliation_issues.append({
            "code": issue.code,
            "fact_ids": list(issue.fact_ids),
            "reason": issue.reason,
        })

    for fact in reconciled.current:
        source_id = _source_id(fact)
        if fact.fact_type == "allergy":
            if isinstance(fact.value_original, dict):
                out.allergies.append(fact.value_original)
                out.provenance["allergy"] = out.provenance["allergy"] or source_id
        elif fact.fact_type == "current_medications":
            out.current_medications = sorted(fact.value_original)
            out.provenance["current_medication"] = source_id
        elif fact.fact_type == "relevant_diagnoses":
            out.relevant_diagnoses = sorted(fact.value_original)
            out.provenance["diagnoses"] = source_id
        elif fact.fact_type == "renal_function":
            value = fact.value_original
            out.last_renal_function = {
                "creatinine_mg_dl": value["creatinine"],
                "egfr_ml_min": value["egfr"],
                "date": fact.effective_time.date().isoformat() if fact.effective_time else None,
            }
            out.provenance["last_renal_function"] = source_id
        elif fact.fact_type == "open_followups":
            out.open_followups = sorted(fact.value_original)
            out.provenance["open_followups"] = source_id
        elif fact.fact_type == "discharge":
            out.discharge = fact.value_original
            out.provenance["discharge"] = source_id

    out.allergies.sort(key=lambda x: (str(x.get("substance", "")), str(x.get("reaction", ""))))
    out.review_required = sorted(set(out.review_required))
    out.unknown_fields = sorted(set(out.unknown_fields))
    return out, reconciled

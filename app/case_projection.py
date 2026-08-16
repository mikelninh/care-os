from __future__ import annotations

from dataclasses import dataclass, field

from .clinical_truth import ClinicalFact, TruthEnvelope
from .reconciliation import ReconciliationResult, reconcile_truth


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


def project_case(envelopes: list[TruthEnvelope]) -> tuple[CaseProjection, ReconciliationResult]:
    """Render a benchmark/UI-friendly patient context from reconciled truth.

    Projection is downstream of reconciliation. If a clinical concept is unresolved,
    the projection records it as unknown/review instead of selecting a convenient
    source. This function contains no clinical inference.
    """

    reconciled = reconcile_truth(envelopes)
    out = CaseProjection(patient_ref=reconciled.patient_ref)

    review_types = {fact.fact_type for fact in reconciled.review}
    for fact in reconciled.review:
        source_id = _source_id(fact)
        if source_id:
            out.review_required.append(source_id)
    for fact_type in sorted(review_types):
        if fact_type != "review_required":
            out.unknown_fields.append(fact_type)

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
                # Historical benchmark has one allergy; retain first source for
                # compatibility while the truth layer itself supports many.
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

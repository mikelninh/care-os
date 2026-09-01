from __future__ import annotations

import pytest

from app.access_policy import UserContext
from app.clinical_truth import ClinicalFact, SourceKind, SourceRef
from app.clinical_trust import (
    InMemoryClinicalTrustLedger,
    build_clinical_decision,
    build_clinical_finding,
    clinical_production_gate,
    clinical_review_gate,
)


def doctor(**overrides) -> UserContext:
    data = {
        "subject": "doctor-1",
        "organisation": "hospital-a",
        "roles": {"doctor"},
        "scopes": {"patient:read"},
        "treatment_patient_refs": {"p1"},
    }
    data.update(overrides)
    return UserContext(**data)


def med_fact(fact_id: str, document_id: str, dose: str, locator: str) -> ClinicalFact:
    return ClinicalFact(
        fact_id=fact_id,
        patient_ref="p1",
        fact_type="medication.ramipril",
        value_original=dose,
        source=SourceRef(
            kind=SourceKind.DOCUMENT,
            system="clinical-document-store",
            document_id=document_id,
            evidence_span=locator,
        ),
    )


def medication_discrepancy():
    return [
        med_fact("med-discharge", "discharge-2026-08-31", "Ramipril 5 mg", "page 4 > medication table > Ramipril"),
        med_fact("med-list", "med-list-2026-09-01", "Ramipril 2.5 mg", "page 1 > current medication > Ramipril"),
    ]


def finding(facts):
    return build_clinical_finding(
        finding_id="finding-med-1",
        finding_type="medication_reconciliation",
        summary="Discharge letter says Ramipril 5 mg while the current medication list says 2.5 mg; clinician reconciliation required.",
        facts=facts,
        trace_id="trace-med-1",
        created_at="2026-09-01T17:00:00+00:00",
    )


def test_exact_source_to_human_review_golden_path_but_production_stays_blocked():
    facts = medication_discrepancy()
    item = finding(facts)
    ledger = InMemoryClinicalTrustLedger()
    ledger.add_finding(item)

    pending = clinical_review_gate(item, ledger.decisions(item.finding_id), facts)
    assert pending.allow is False
    assert "clinical_human_decision_pending" in pending.reasons

    decision = build_clinical_decision(
        item,
        actor=doctor(),
        status="approved",
        decision_id="decision-1",
        current_facts=facts,
        note="Medication discrepancy confirmed; reconcile in source system.",
        at="2026-09-01T17:05:00+00:00",
    )
    ledger.add_decision(decision)

    review = clinical_review_gate(item, ledger.decisions(item.finding_id), facts)
    assert review.allow is True
    assert review.reasons == []
    assert review.decision_id == "decision-1"

    production = clinical_production_gate(item, ledger.decisions(item.finding_id), facts)
    assert production.allow is False
    assert "clinical_production_release_not_proven" in production.reasons
    assert "clinical_writeback_disabled_by_release_policy" in production.reasons


def test_structured_clinical_fact_needs_exact_element_locator_for_consequential_finding():
    record_level_only = ClinicalFact(
        fact_id="lab-1",
        patient_ref="p1",
        fact_type="renal.egfr",
        value_original=42,
        source=SourceRef(
            kind=SourceKind.FHIR,
            system="hospital-fhir",
            resource_type="Observation",
            resource_id="obs-42",
            resource_version="7",
        ),
    )
    assert record_level_only.provenance_complete is True
    with pytest.raises(ValueError, match="clinical_exact_evidence_locator_required"):
        build_clinical_finding(
            finding_id="finding-lab",
            finding_type="clinical_review",
            summary="Review eGFR source.",
            facts=[record_level_only],
            trace_id="trace-lab",
        )


def test_unqualified_or_out_of_context_reviewer_cannot_approve():
    facts = medication_discrepancy()
    item = finding(facts)

    nurse = doctor(subject="nurse-1", roles={"nurse"})
    with pytest.raises(PermissionError, match="not_qualified"):
        build_clinical_decision(
            item,
            actor=nurse,
            status="approved",
            decision_id="nurse-decision",
            current_facts=facts,
        )

    other_patient_doctor = doctor(subject="doctor-2", treatment_patient_refs={"p2"})
    with pytest.raises(PermissionError, match="access_denied"):
        build_clinical_decision(
            item,
            actor=other_patient_doctor,
            status="approved",
            decision_id="other-patient-decision",
            current_facts=facts,
        )


def test_source_drift_after_approval_closes_review_gate_again():
    facts = medication_discrepancy()
    item = finding(facts)
    decision = build_clinical_decision(
        item,
        actor=doctor(),
        status="approved",
        decision_id="decision-before-drift",
        current_facts=facts,
    )
    assert clinical_review_gate(item, [decision], facts).allow is True

    drifted = [fact.model_copy(deep=True) for fact in facts]
    drifted[0].value_original = "Ramipril 10 mg"
    gate = clinical_review_gate(item, [decision], drifted)
    assert gate.allow is False
    assert "clinical_source_drift" in gate.reasons
    assert any(reason.startswith("clinical_evidence_mismatch") for reason in gate.reasons)


def test_decision_history_is_append_only_and_latest_rejection_closes_gate():
    facts = medication_discrepancy()
    item = finding(facts)
    ledger = InMemoryClinicalTrustLedger()
    ledger.add_finding(item)

    approved = build_clinical_decision(
        item,
        actor=doctor(),
        status="approved",
        decision_id="decision-approved",
        current_facts=facts,
        at="2026-09-01T17:05:00+00:00",
    )
    ledger.add_decision(approved)

    rejected = build_clinical_decision(
        item,
        actor=doctor(),
        status="rejected",
        decision_id="decision-rejected",
        current_facts=facts,
        note="New clinical context means this prepared finding must not be used.",
        at="2026-09-01T17:10:00+00:00",
    )
    ledger.add_decision(rejected)

    history = ledger.decisions(item.finding_id)
    assert [record.decision_id for record in history] == ["decision-approved", "decision-rejected"]
    assert history[0].status == "approved"
    assert history[1].status == "rejected"
    gate = clinical_review_gate(item, history, facts)
    assert gate.allow is False
    assert gate.decision_id == "decision-rejected"
    assert "clinical_human_decision_rejected" in gate.reasons


def test_cross_patient_evidence_cannot_form_one_clinical_finding():
    facts = medication_discrepancy()
    other = facts[1].model_copy(deep=True)
    other.patient_ref = "p2"
    with pytest.raises(ValueError, match="cross_patient"):
        finding([facts[0], other])

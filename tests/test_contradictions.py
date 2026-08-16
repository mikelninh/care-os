from app.clinical_truth import ClinicalFact, SourceKind, SourceRef
from app.contradictions import (
    ContradictionRule,
    ContradictionSeverity,
    contradiction_groups,
    detect_contradictions,
)


def source(resource_id: str) -> SourceRef:
    return SourceRef(kind=SourceKind.FHIR, system="FHIR", resource_type="Observation", resource_id=resource_id)


def fact(fact_id: str, fact_type: str, code: str) -> ClinicalFact:
    return ClinicalFact(
        fact_id=fact_id,
        patient_ref="p1",
        fact_type=fact_type,
        value_original=code,
        code=code,
        code_system="urn:careos:test",
        source=source(fact_id),
    )


def test_explicit_rule_surfaces_conflict_without_picking_winner():
    facts = [fact("a", "status.a", "A"), fact("b", "status.b", "B")]
    rules = [ContradictionRule(
        rule_id="test-conflict",
        left_fact_type="status.a",
        right_fact_type="status.b",
        left_code="A",
        right_code="B",
        severity=ContradictionSeverity.CRITICAL,
        rationale="Synthetic governed contradiction rule",
    )]
    conflicts = detect_contradictions(facts, rules)
    assert len(conflicts) == 1
    assert conflicts[0].severity == ContradictionSeverity.CRITICAL
    assert contradiction_groups(facts, conflicts) == {"test-conflict": {"a", "b"}}


def test_no_free_text_medical_inference_without_rule():
    facts = [fact("a", "allergy", "X"), fact("b", "medication.current", "X")]
    assert detect_contradictions(facts, []) == []


def test_rules_do_not_cross_patient_boundary():
    a = fact("a", "status.a", "A")
    b = ClinicalFact(
        fact_id="b",
        patient_ref="p2",
        fact_type="status.b",
        value_original="B",
        code="B",
        code_system="urn:careos:test",
        source=source("b"),
    )
    rule = ContradictionRule(
        rule_id="test",
        left_fact_type="status.a",
        right_fact_type="status.b",
        left_code="A",
        right_code="B",
    )
    assert detect_contradictions([a, b], [rule]) == []

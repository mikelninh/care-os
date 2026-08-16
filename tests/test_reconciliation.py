from datetime import datetime, timezone
from itertools import permutations

from app.clinical_truth import AssertionStage, ClinicalFact, FactStatus, SourceKind, SourceRef, TruthEnvelope
from app.reconciliation import reconcile_truth


def _fact(
    fact_id: str,
    fact_type: str,
    value,
    *,
    day: int = 1,
    stage: AssertionStage = AssertionStage.UNKNOWN,
    logical_key: str | None = None,
    confidence: float = 1.0,
    supersedes: str | None = None,
    status: FactStatus = FactStatus.CONFIRMED,
    blocks: tuple[str, ...] = (),
    review_reason: str | None = None,
):
    return ClinicalFact(
        fact_id=fact_id,
        patient_ref="p1",
        fact_type=fact_type,
        logical_key=logical_key,
        value_original=value,
        effective_time=datetime(2026, 8, day, tzinfo=timezone.utc),
        source=SourceRef(
            kind=SourceKind.DOCUMENT,
            system="test",
            document_id=f"doc-{fact_id}",
            evidence_span=str(value),
        ),
        assertion_stage=stage,
        confidence=confidence,
        supersedes_fact_id=supersedes,
        status=status,
        blocks_fact_types=blocks,
        review_reason=review_reason,
    )


def _env(*facts):
    return TruthEnvelope(patient_ref="p1", facts=list(facts))


def test_latest_effective_time_is_allowed_for_governed_state_snapshot():
    old = _fact("renal-old", "renal_function", {"creatinine": 1.2}, day=1)
    new = _fact("renal-new", "renal_function", {"creatinine": 1.7}, day=2)
    result = reconcile_truth([_env(old, new)])
    assert [f.fact_id for f in result.current] == ["renal-new"]
    assert [f.fact_id for f in result.superseded] == ["renal-old"]


def test_newer_alone_does_not_resolve_ungoverned_conflict():
    old = _fact("dx-old", "diagnosis", "A", day=1, logical_key="primary-diagnosis")
    new = _fact("dx-new", "diagnosis", "B", day=2, logical_key="primary-diagnosis")
    result = reconcile_truth([_env(old, new)])
    assert result.current == []
    assert {f.fact_id for f in result.review} == {"dx-old", "dx-new"}
    assert any(i.code == "critical-unresolved-current-conflict" for i in result.issues)


def test_final_can_replace_preliminary_for_same_logical_assertion():
    prelim = _fact("micro-pre", "microbiology", "E. coli?", stage=AssertionStage.PRELIMINARY, logical_key="culture-1")
    final = _fact("micro-final", "microbiology", "E. coli", stage=AssertionStage.FINAL, logical_key="culture-1")
    result = reconcile_truth([_env(prelim, final)])
    assert [f.fact_id for f in result.current] == ["micro-final"]
    assert [f.fact_id for f in result.superseded] == ["micro-pre"]


def test_conflicting_final_results_require_review():
    a = _fact("micro-a", "microbiology", "E. coli", stage=AssertionStage.FINAL, logical_key="culture-1")
    b = _fact("micro-b", "microbiology", "Klebsiella", stage=AssertionStage.FINAL, logical_key="culture-1")
    result = reconcile_truth([_env(a, b)])
    assert not result.current
    assert {f.fact_id for f in result.review} == {"micro-a", "micro-b"}


def test_explicit_correction_can_supersede_fact_from_another_envelope():
    old = _fact("old", "microbiology", "prelim", logical_key="culture-1")
    corrected = _fact(
        "corrected", "microbiology", "corrected", logical_key="culture-1",
        stage=AssertionStage.CORRECTED, supersedes="old",
    )
    result = reconcile_truth([_env(old), _env(corrected)])
    assert [f.fact_id for f in result.current] == ["corrected"]
    assert [f.fact_id for f in result.superseded] == ["old"]


def test_explicit_cancellation_removes_cancelled_target_from_current_surface():
    old = _fact("micro-wrong", "microbiology", "E. coli", day=1, stage=AssertionStage.FINAL, logical_key="culture-1")
    cancelled = _fact(
        "micro-cancel", "microbiology", "result cancelled", day=2,
        stage=AssertionStage.CANCELLED, logical_key="culture-1", supersedes="micro-wrong",
    )
    for ordered in permutations([old, cancelled]):
        result = reconcile_truth([_env(*ordered)])
        assert "micro-wrong" not in {f.fact_id for f in result.current}
        assert "micro-wrong" in {f.fact_id for f in result.superseded}
        assert "micro-cancel" in {f.fact_id for f in result.cancelled}


def test_newer_unbound_cancellation_withholds_older_same_concept_for_review():
    old = _fact("micro-old", "microbiology", "E. coli", day=1, stage=AssertionStage.FINAL, logical_key="culture-1")
    cancelled = _fact("micro-cancel", "microbiology", "cancelled", day=2, stage=AssertionStage.CANCELLED, logical_key="culture-1")
    result = reconcile_truth([_env(old, cancelled)])
    assert not result.current
    assert "micro-old" in {f.fact_id for f in result.review}
    assert any(i.code == "critical-unbound-cancellation" for i in result.issues)


def test_valid_assertion_newer_than_unbound_cancellation_can_restore_current_state():
    old = _fact("micro-old", "microbiology", "E. coli", day=1, stage=AssertionStage.FINAL, logical_key="culture-1")
    cancelled = _fact("micro-cancel", "microbiology", "cancelled", day=2, stage=AssertionStage.CANCELLED, logical_key="culture-1")
    restored = _fact("micro-new", "microbiology", "No growth", day=3, stage=AssertionStage.FINAL, logical_key="culture-1")
    result = reconcile_truth([_env(old, cancelled, restored)])
    assert {f.fact_id for f in result.current} == {"micro-new"}


def test_cross_concept_supersession_is_blocked():
    allergy = _fact("allergy", "allergy", "Penicillin", logical_key="allergy-pen")
    med = _fact("med", "current_medications", ["Amoxicillin"], logical_key="med-list", supersedes="allergy")
    result = reconcile_truth([_env(allergy), _env(med)])
    assert "med" in {f.fact_id for f in result.review}
    assert any(i.code == "critical-cross-concept-supersedes" for i in result.issues)


def test_confidence_never_breaks_clinical_conflict():
    high = _fact("high", "diagnosis", "A", logical_key="dx", confidence=0.99)
    low = _fact("low", "diagnosis", "B", logical_key="dx", confidence=0.60)
    result = reconcile_truth([_env(high, low)])
    assert not result.current
    assert {f.fact_id for f in result.review} == {"high", "low"}


def test_identical_assertions_are_corroborating_not_conflicting():
    a = _fact("a", "diagnosis", "Endokarditis", logical_key="dx-endo")
    b = _fact("b", "diagnosis", "Endokarditis", logical_key="dx-endo")
    result = reconcile_truth([_env(a, b)])
    assert len(result.current) == 1
    chosen = result.current[0]
    assert result.corroborating_fact_ids[chosen.fact_id]


def test_newer_unresolved_lab_blocks_older_renal_state_from_quiet_display():
    old = _fact("renal-old", "renal_function", {"creatinine": 1.2}, day=1, logical_key="renal-function")
    barrier = _fact(
        "lab-review",
        "review_required",
        {"document_kind": "lab"},
        day=2,
        status=FactStatus.UNKNOWN,
        blocks=("renal_function",),
        review_reason="newer lab document could not be parsed safely",
    )
    result = reconcile_truth([_env(old), _env(barrier)])
    assert "renal-old" not in {f.fact_id for f in result.current}
    assert {"renal-old", "lab-review"} <= {f.fact_id for f in result.review}
    assert any(i.code == "critical-newer-unresolved-source" for i in result.issues)


def test_newer_successfully_parsed_state_can_restore_current_after_older_barrier():
    barrier = _fact(
        "lab-review",
        "review_required",
        {"document_kind": "lab"},
        day=1,
        status=FactStatus.UNKNOWN,
        blocks=("renal_function",),
        review_reason="older lab unresolved",
    )
    current = _fact("renal-new", "renal_function", {"creatinine": 1.4}, day=2, logical_key="renal-function")
    result = reconcile_truth([_env(barrier), _env(current)])
    assert "renal-new" in {f.fact_id for f in result.current}

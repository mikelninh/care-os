from benchmark.holdout3 import HOLDOUT_FAMILIES, evaluate_holdout, fingerprint, generate_holdout


DEV_FAMILIES = {
    "allergy_multiline",
    "medication_multiline_semicolon",
    "diagnosis_multiline",
    "followup_multiline",
    "renal_multiline_colon",
    "discharge_colon_multiline",
}


def test_holdout3_families_are_disjoint_from_development_mutations():
    assert HOLDOUT_FAMILIES.isdisjoint(DEV_FAMILIES)


def test_holdout3_generation_is_deterministic():
    first = generate_holdout(count=20)
    second = generate_holdout(count=20)
    assert fingerprint(first) == fingerprint(second)
    assert first == second


def test_holdout3_report_declares_no_tuning_and_tracks_safety_metrics():
    report = evaluate_holdout(count=25)
    assert report["holdout"]["development_tuning_allowed"] is False
    assert len(report["holdout"]["fingerprint_sha256"]) == 64
    assert "precision_recall_f1" in report
    assert "critical_silent_misses" in report["contradiction_safety"]
    assert report["minimum_provenance_coverage"] == 1.0

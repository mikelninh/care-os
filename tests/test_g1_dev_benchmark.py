from benchmark.g1_dev import run_dev


def test_g1_dev_corpus_is_explicitly_not_frozen_holdout_and_keeps_provenance():
    report = run_dev(count=40, seed=90517)
    assert report["dataset"]["development_only"] is True
    assert report["dataset"]["frozen_unseen_holdout_used_for_tuning"] is False
    assert report["minimum_provenance_coverage"] == 1.0


def test_g1_supported_development_forms_do_not_require_review_fallback():
    report = run_dev(count=40, seed=90517)
    assert report["cases_routed_to_review"] == 0
    # The generic unsupported-high-risk fallback is tested directly in
    # tests/test_conservative_extractor.py. This corpus contains only forms we have
    # intentionally admitted into the development grammar.

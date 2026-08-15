# CareOS Stress Benchmark

CareOS V8 ships with a deterministic 500-case synthetic gold dataset plus two red-team suites.

## Gold labels

Each case labels allergies, current medication, relevant diagnoses, latest renal function, open follow-ups, discharge state, contradictions, and per-field provenance.

## Why two red-team suites?

The first suite exposed severe brittleness. We hardened against those known attacks. A second holdout was written *after* the hardening pass and intentionally uses unseen phrasing. We do not tune against that holdout.

Current unseen-holdout result: 1.2% all-fields exact and 126 silent contradiction misses across 500 cases. This is a failure signal, not a launch claim. It tells us the deterministic extractor is not safe enough for clinical deployment.

## Benchmark discipline

- Development cases may be used to improve the system.
- Frozen validation holdouts must not be used as prompt/rule tuning material.
- Safety-critical metrics are reported separately from average accuracy.
- Provenance is part of correctness, not an optional explanation layer.
- Unknown/ambiguous output is preferable to unsupported certainty.

## Next benchmark layer

Move from regex-style extraction toward source-native structured FHIR where available, schema-constrained extraction for documents, temporal normalization, unit normalization, source spans, contradiction rules, and human review for safety-critical uncertainty. Add clinician-reviewed de-identified cases only under appropriate governance.

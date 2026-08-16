# CareOS Clinical Truth Benchmark

CareOS uses synthetic benchmarks to test extraction/reconciliation failure modes before any real-patient evaluation. These benchmarks are **engineering evidence, not clinical validation**.

## Why the benchmark became stricter

The original deterministic 500-case corpus showed that apparently strong extraction results could collapse under unseen phrasing. The second unseen holdout produced only **1.2% all-fields exact** and **126 silent contradiction misses**. That result remains preserved as evidence that the legacy deterministic extractor was unsafe.

Instead of adding regexes against that holdout, CareOS introduced a different architecture:

`source -> untrusted candidate -> exact evidence verification -> ClinicalFact -> deterministic reconciliation -> projection`

Key safety changes:

- source evidence is mandatory;
- extraction confidence is separate from source maturity (`preliminary/final/corrected/cancelled`);
- confidence never resolves conflicting clinical assertions;
- only explicitly governed state-snapshot fact families may use recency;
- a newer unresolved high-risk source can block older parsed state from looking current;
- explicit `unknown/review` is measured separately from silent omission.

## Frozen Holdout #3 — first result

**ID:** `g1-holdout3-2026-08-16`  
**Cases:** 500  
**Fingerprint:** `e21633181e2d592c9a16653c9a99fb5a0c96dcf787e716dc4ea155cedbfa3ea4`  
**Development tuning allowed:** **NO**

Holdout #3 was generated from mutation families deliberately disjoint from the development corpus and evaluated once after the reconciliation/review-barrier architecture was frozen.

### Result

| Metric | Result |
|---|---:|
| Micro precision | **100.0%** |
| Micro recall | **26.32%** |
| Micro F1 | **41.67%** |
| Unsupported-claim rate | **0.0%** |
| Wrong-source count | **0** |
| Minimum provenance coverage | **100%** |
| Critical silent field misses | **0** |
| Critical silent contradiction misses | **0** |
| Review case rate | **100%** |
| All-fields exact | **0%** |

Per-field recall was deliberately poor under unseen forms: allergy 28.8%, current medication 21.08%, diagnoses 30.41%, renal function 25.2%, follow-ups 31.33%, discharge 27.35%. Precision remained 100% on surfaced benchmark items.

### Interpretation

This is **not a G1 pass**.

It demonstrates a valuable safety transition: on this synthetic holdout, CareOS stopped silently guessing and instead abstained/review-routed unsupported information. But the abstention burden is unusably high. A system that needs review on every case has not solved the clinician workflow.

The next extractor generation must therefore improve recall **without spending the safety gains**.

## Holdout discipline

Holdout #3 is now historical evidence. Do **not**:

- add parser rules based on its individual failures;
- edit its mutation families to make the score prettier;
- repeatedly run prompt/rule variants against it and choose the best;
- call zero silent misses a clinical-safety guarantee.

Further development must use a new development corpus. When that architecture is frozen, evaluate against a future untouched holdout.

## Release metrics

CareOS reports at least:

- precision / recall / F1 per field;
- provenance coverage;
- wrong-source rate;
- unsupported-claim rate;
- critical silent-miss rate;
- contradiction detection vs explicit-review vs silent miss;
- review/abstention burden;
- false-review burden once richer gold labels exist.

The desired direction is not simply “higher accuracy.” It is:

> **high recall + extremely high precision + traceability + low silent-risk + tolerable review burden.**

## What comes next

1. build a model-assisted/schema-constrained extractor behind the same exact-evidence firewall;
2. develop only on a fresh development set and source-native structured data;
3. keep deterministic reconciliation downstream of any model;
4. evaluate the next frozen holdout once the new extraction architecture is fixed;
5. eventually add clinician-reviewed, appropriately governed de-identified cases.

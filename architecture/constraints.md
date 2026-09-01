<!-- paos:reviewed=2026-09-01 -->
# Constraints

## Four correctness invariants

1. **Pending ≠ negative.**
2. **Unavailable ≠ absent.**
3. **Documented therapy ≠ AI recommendation.**
4. **Agent draft ≠ source truth.**

Any feature that weakens these invariants is a product regression even if it improves speed or visual simplicity.

## Human authority

- models may propose structure, summaries or drafts;
- final clinical interpretation/action remains human;
- current research stage has no production write-back;
- a passing agent eval may not expand clinical authority automatically.

## Safety / evidence

- provenance, lifecycle, time and freshness remain attached to important clinical context;
- corrected/final data must invalidate or flag dependent stale artefacts;
- degraded/offline states must fail visibly;
- safety stops must be counted in any positive workflow result;
- speed is not considered a win when error or verification behaviour worsens.

## Privacy / security

- production PHI operations are blocked by design at the current stage;
- real hospital deployment requires approved privacy/security review and governance;
- patient boundaries must fail closed;
- no public proof may expose patient-identifying clinical data.

## Evidence truth

- synthetic/deidentified evaluation ≠ clinical validation;
- research-runtime FHIR/ISiK/HL7 paths ≠ proven target-system integration;
- Docker/Helm scaffold ≠ hospital production readiness;
- repository-green ≠ clinician-safe;
- one hospital/vendor ≠ proven repeatability.

## Current hard blocker

The frozen 500-case synthetic clinical-truth holdout currently preserves precision/provenance but reports **26.32% recall with 100% review-case burden**. Production G1 remains blocked.

This result may not be hidden, re-labelled as production-ready or tuned away against the frozen holdout. Improvement must be demonstrated on fresh development data and then stronger external evidence.

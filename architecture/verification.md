<!-- paos:reviewed=2026-09-01 -->
# Verification

## Evidence ladder

`DECLARED → STATIC → AUTOMATED → E2E → CLINICIAN STUDY → SHADOW → PILOT → PRODUCTION`

Clinical claims require stronger evidence than repository behaviour alone.

## Current evidence

- source-linked lifecycle/provenance: synthetically tested;
- patient-local graph + stale-artifact invalidation: implemented/tested;
- bounded agent authority: synthetic + adversarial tests;
- NORMAL/DEGRADED/OFFLINE/RECOVERY: synthetic implementation/tests;
- clinical review UX: interactive synthetic demo + DOM/mobile/desktop QA;
- FHIR R4 and ISiK-oriented paths: research implementation;
- time-returned study machinery: implemented, participant evidence pending;
- real KIS/LIS integration, production PHI operations, repeatability and clinical/regulatory assurance: externally unproven/blocked.

## Golden-case status

### GC1 — Morning review

- [x] synthetic workflow exists;
- [x] source/provenance and human-review behaviour are testable;
- [ ] ≥5 complete safe paired clinician sessions for one workflow family;
- [ ] measured baseline vs CareOS timing/errors/source checks/cognitive effort;
- [ ] zero hidden safety-stop events in any positive result.

### GC2 — Correction/recovery

- [x] permanent synthetic end-to-end journey;
- [x] stale-artifact/recovery behaviour tested;
- [ ] external reviewers challenge source variation and recovery assumptions.

### GC3 — Authority boundary

- [x] bounded agent/tool tests + adversarial scenarios;
- [x] production write-back blocked in current stage;
- [ ] independent clinical/privacy/security review validates the intended boundary;
- [ ] governed shadow workflow proves behaviour in an approved environment.

## Blocking metric

Frozen 500-case synthetic holdout: **26.32% recall, 100% review-case burden**. Production G1 is blocked.

## Next proof level

External evidence is more valuable than broad feature expansion:

1. ≥5 safe paired clinician sessions;
2. ≥3 independent reviewer perspectives;
3. one real non-secret hospital capability manifest;
4. every external finding classified supported/falsified/blocked/unknown;
5. at least one assumption corrected or falsified.

The project becomes stronger when reality changes the architecture, not when every external reviewer agrees with it.

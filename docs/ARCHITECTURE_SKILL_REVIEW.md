# Architecture Skill Review — CareOS

## Decision

**Do not refactor the clinical truth/read core right now.**

The strongest modules already pass the deep-module deletion test:

- `ClinicalFact` / `TruthEnvelope` own source/provenance/trust semantics;
- `ClinicalReadCoordinator.read(...)` owns authorization, runtime safety controls, connector failure handling, patient-context matching, source-currentness and mandatory audit before returning renderable truth;
- case projection happens only after reconciliation.

Deleting these modules would spread safety-critical logic across callers, which is evidence that they are earning their abstraction cost.

## Current bottleneck

CareOS itself records that external evidence is now more valuable than another broad feature. Production remains blocked until real clinician, integration, privacy/security and hospital evidence improves the proof frontier.

## Highest-leverage next seam

The next module/product boundary to deepen should be the **repeatable hospital adoption/pilot package**, not a new clinical abstraction:

```text
Hospital workflow
      ↓
capability manifest
      ↓
connector / governance preflight
      ↓
paired clinician evidence
      ↓
assurance + evidence ledger
      ↓
go / blocked / next proof
```

This lets hospital #2 reuse what was learned at hospital #1 while clinical truth remains provider-controlled.

See `PILOT_COMMERCIAL_MODEL.md` for the corresponding ethical payer/value model.

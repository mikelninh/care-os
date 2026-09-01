<!-- paos:reviewed=2026-09-01 -->
# Product specification

## Core workflow 1 — Clinical morning review

A clinician opens one patient and needs to reconstruct what changed, what is pending, what is critical and what requires verification before preparing documentation or transfer work.

### Acceptance criteria

- source, timestamp, lifecycle and freshness remain visible;
- pending is never collapsed into negative;
- unavailable is never collapsed into absent;
- contradictory/corrected information is surfaced;
- documentation prepared by an agent remains visibly derived/draft;
- the clinician can open the underlying source before accepting important context.

## Core workflow 2 — Source correction / degraded operation

A preliminary result or derived draft exists, then the source changes or a source/network interruption occurs.

### Acceptance criteria

- stale derived work is invalidated or marked `REVIEW REQUIRED`;
- degraded/offline state is explicit;
- corrected/final information does not silently coexist as equivalent truth;
- recovery requires reconciliation before normal state resumes;
- audit can reconstruct what changed and what human review occurred.

## Core workflow 3 — Bounded agent assistance

An agent prepares structure or documentation using patient-local context.

### Acceptance criteria

- tool/capability authority is explicit and bounded;
- documented therapy is not transformed into an AI recommendation;
- agent draft is never promoted to source truth;
- production write-back remains blocked in the current research stage;
- human clinical authority remains the release boundary.

## Failure states that block progression

- cross-patient context leakage;
- stale or corrected evidence shown as current without warning;
- missing provenance for consequential context;
- clinically important pending state hidden;
- derived content presented as source truth;
- a green engineering test suite presented as clinical validation.

## Public proof surface

The public demos may show synthetic/deidentified versions of the workflows and engineering assurance. They must continue to state that CareOS is pre-hospital research, not for clinical use and not proven in production hospital environments.

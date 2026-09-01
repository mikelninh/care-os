# CareOS — Product Spec

## Core workflow
1. Retrieve source-system context.
2. Resolve patient/encounter identity fail-closed.
3. Preserve provenance, lifecycle, freshness and uncertainty.
4. Reconcile conflicting/pending/final information.
5. Present role-specific context and bounded drafts.
6. Require human review for clinical truth and consequential action.
7. Audit corrections, outages, recovery and derived-artifact invalidation.

## User-visible invariants
- Pending ≠ negative.
- Unavailable ≠ absent.
- Documented therapy ≠ AI recommendation.
- Agent draft ≠ source truth.

## Acceptance direction
A clinician should be able to reconstruct the relevant context faster or with less friction **without more errors, missed pending items, unsafe acceptance or verification collapse**.

## Current product state
Research/reference implementation with synthetic/deidentified evaluation. Not for clinical production use.

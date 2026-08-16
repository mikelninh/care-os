# ADR-007 — Demographic similarity cannot silently merge patients

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Wrong-patient attachment is a catastrophic failure class. Names, birth dates and addresses are not unique enough to establish identity automatically in all cases.

## Decision

Automatic patient attachment requires a unique verified strong identifier or another explicitly approved authoritative identity mechanism. Conflicting strong identifiers block. Demographic similarity is review evidence, not automatic authority.

## Consequences

- patient-context mismatch fails closed;
- KIS/portal context launch is preferred over manual search;
- ambiguous identity creates explicit review work;
- patient identity metrics are first-class safety metrics;
- cross-provider identity mechanisms should align with national infrastructure where applicable.

## Rejected alternative

Probabilistically merge records above a demographic similarity threshold without human review.

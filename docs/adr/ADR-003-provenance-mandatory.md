# ADR-003 — Provenance is mandatory for surfaced clinical facts

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Clinical summaries without traceable origin are difficult to verify, audit, correct and safely reconcile.

## Decision

A clinical fact is not complete enough for quiet clinician display unless it retains source identity and sufficient provenance to verify its origin. Document-derived facts additionally require exact evidence spans/quotes.

## Consequences

- provenance is part of correctness metrics;
- wrong-source claims are measured independently;
- normalization never destroys original wording/value;
- users can inspect the underlying source;
- generated summaries must be derived from traceable facts rather than free-floating model prose.

## Rejected alternative

Show concise AI summaries first and make source linking optional.

# ADR-005 — Missing, negative, stale, unavailable and unknown are distinct

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Clinical risk arises when system failures are rendered as reassuring absence. A source timeout is not equivalent to a negative result; an unreadable document is not equivalent to no finding.

## Decision

CareOS models source/data state explicitly. At minimum it distinguishes:

- current data;
- stale data;
- source unavailable;
- unknown/unresolved;
- contradictory;
- explicitly negative/absent where the source truly states that.

## Consequences

- UI must surface degraded state;
- connectors return `SourceState` in addition to data;
- partial logical reads may fail instead of silently truncating;
- unresolved newer high-risk documents can block stale older state from appearing current;
- reliability tests must include source/audit/identity failures.

## Rejected alternative

Return an empty list or `null` for every no-data/error state and let the UI interpret it.

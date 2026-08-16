# ADR-010 — Vendor-specific integrations stay behind an open stable connector contract

**Status:** Accepted  
**Date:** 2026-08-16

## Context

German providers use heterogeneous KIS/LIS/PVS/vendor stacks. If vendor logic leaks into CareOS core/UI, every hospital becomes bespoke implementation work and creates new lock-in.

## Decision

All source integrations expose a stable vendor-neutral connector contract covering:

- capabilities;
- source identity;
- read/write capability;
- `TruthEnvelope`;
- source version/timestamp;
- freshness/state;
- failure/partial semantics.

Vendor-specific implementation remains behind the contract.

## Consequences

- core clinical truth/security semantics do not change by vendor;
- capability differences remain explicit;
- procurement can demand documented/exportable contracts;
- second-hospital deployment tests whether the platform scales without a core fork;
- vendor adapters can be replaced independently.

## Rejected alternative

Implement each hospital integration directly in UI/business logic.

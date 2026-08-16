# ADR-002 — Identifiable clinical data stays provider-side by default

**Status:** Accepted  
**Date:** 2026-08-16

## Context

A central longitudinal CareOS database would increase privacy, sovereignty, security and procurement risk and would duplicate provider/source-system records.

## Decision

Routine identifiable patient data remains in the provider environment or a dedicated provider-controlled tenant. The shared CareOS control plane distributes software, configuration/policy bundles, pack versions and non-PHI operational metadata.

## Consequences

- provider data planes own patient-context processing;
- provider-specific keys, audit and retention can be enforced;
- national scale does not require a national CareOS PHI lake;
- cross-provider interoperability uses authorized exchange standards rather than central copying by default;
- any exception requires explicit data-flow, legal basis, retention and security review.

## Rejected alternative

A shared multi-tenant central clinical database containing all provider patients.

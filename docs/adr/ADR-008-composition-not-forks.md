# ADR-008 — Scale by composition, not hospital/specialty core forks

**Status:** Accepted  
**Date:** 2026-08-16

## Context

If every specialty, hospital, language or country requires a separate CareOS codebase, maintenance and safety assurance will fragment rapidly.

## Decision

CareOS scales through one core plus composable extensions:

`Core + Specialty Pack + Country Pack + Language Presentation + Audience Policy/View`

Provider-specific differences live in connectors, mappings, policy/configuration and approved SOP overlays rather than core forks.

## Consequences

- truth semantics stay common across deployments;
- specialty packs change attention/workflow, not source truth;
- country packs contain national interoperability/identity/terminology rules;
- language changes presentation rather than the underlying fact;
- Hospital B repeatability becomes a formal platform test.

## Rejected alternative

Maintain independent hospital/specialty branches with custom truth and security logic.

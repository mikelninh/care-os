# ADR-009 — Consume national/EU rails before inventing private equivalents

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Germany and the EU already define/operate health identity, interoperability, communication and future EHR exchange infrastructure. Duplicating those functions privately creates fragmentation and public-sector resistance.

## Decision

Where applicable and fit for purpose, CareOS consumes established national/EU rails such as ISiK, ISiP, ePA/TI, digital identity/context mechanisms and EHDS interoperability/logging requirements rather than creating competing national infrastructure.

CareOS-specific contracts fill gaps above/between systems but do not claim to replace statutory/national standards.

## Consequences

- standard interfaces are preferred before vendor-specific APIs;
- CareOS must track changing national specifications by version;
- government proposal positions CareOS as a reference implementation/context layer, not a parallel TI;
- formal confirmation/conformity procedures are evaluated where product scope requires them.

## Rejected alternative

Create a proprietary national CareOS identity, health-data exchange and messaging network.

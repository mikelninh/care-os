# ADR-001 — CareOS is not the clinical system of record

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Replacing KIS/PVS/EHR systems would dramatically increase migration risk, procurement scope, regulatory burden and time-to-value. Existing systems remain authoritative for their clinical records.

## Decision

CareOS is a clinical context/orchestration layer, not the primary clinical system of record.

CareOS may retrieve, normalize, reconcile and present source-linked context and prepare documentation for human review. Authoritative source ownership remains with the originating system unless a separately governed future capability explicitly changes that relationship.

## Consequences

- every surfaced fact preserves source identity;
- CareOS can start read-only;
- source corrections/versioning must propagate visibly;
- CareOS must not create silent independent truth disconnected from the source;
- later write-back requires a separate capability and release decision.

## Rejected alternative

Build a new national/enterprise EHR and migrate all source data into CareOS.

Rejected because it creates unnecessary replacement risk and duplicates infrastructure that already exists.

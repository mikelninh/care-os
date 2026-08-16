# ADR-006 — Read and write capabilities are separated

**Status:** Accepted  
**Date:** 2026-08-16

## Context

Read-only retrieval can create value with materially lower operational and clinical risk than changing source-system state. Combining read/write permissions increases blast radius and makes least privilege harder.

## Decision

Read and write are separate connector capabilities, authorization scopes, release gates and audit events.

The current CareOS production boundary is read-only. Transactional/write-back mode is not released.

## Consequences

- every connector declares read/write capabilities explicitly;
- read tokens/scopes do not imply write access;
- future write-back requires human review, source version checks and separate safety/regulatory assessment;
- pilots begin read-only;
- kill/rollback can disable CareOS without altering source records.

## Rejected alternative

Create broad integration credentials and rely on application UI to avoid accidental writes.

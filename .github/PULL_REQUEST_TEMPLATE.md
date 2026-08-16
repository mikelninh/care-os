## What changes?

Describe the behavior change and why it is needed.

## Readiness / safety impact

Check every area touched by this PR:

- [ ] No clinical-truth behavior change
- [ ] Clinical fact / extraction / reconciliation
- [ ] Patient identity / record matching
- [ ] Authentication / authorization / treatment context
- [ ] Audit / logging / telemetry / PHI handling
- [ ] Connector / FHIR / ISiK / terminology / freshness
- [ ] Model / prompt / provider / schema
- [ ] Intended purpose / clinical workflow boundary
- [ ] Data flow / retention / processor / deployment pattern
- [ ] Write capability
- [ ] Reliability / degraded-mode / rollback
- [ ] Regulatory / quality documentation
- [ ] Architecture contract / ADR

## Evidence

- [ ] tests added/updated
- [ ] current regression CI green
- [ ] safety/failure tests added where relevant
- [ ] provenance/source behavior tested where relevant
- [ ] benchmark impact assessed where relevant
- [ ] architecture/gate docs updated where relevant
- [ ] dependency/security impact assessed

Link exact evidence/artifacts:

## Gate impact

Does this PR change evidence or blockers for G0–G9?

- Gate(s):
- Previous status:
- Proposed status:
- Evidence supporting any status change:

> A code change alone is not sufficient to mark an assurance gate PASS.

## Clinical truth questions

If clinical data behavior changes:

1. Can this create or hide a wrong-patient fact?
2. Can source unavailable/stale become a reassuring empty state?
3. Can a model-derived claim bypass exact provenance/evidence checks?
4. Can conflicting sources be silently resolved?
5. Can a newer unresolved source leave stale state looking current?
6. Does the user still have a direct route to the source?

## Privacy / security questions

If data flow/access changes:

1. Is any new identifiable data processed or retained?
2. Does any new data leave the provider boundary?
3. Does any new processor/model/provider receive PHI?
4. Is the action auditable?
5. Does authentication remain distinct from patient authorization?
6. Is rollback/kill-switch behavior preserved?

## Intended purpose / write boundary

- [ ] This PR does not add autonomous diagnosis/treatment selection.
- [ ] This PR does not make production write-back reachable.
- [ ] If either boundary changes, a superseding ADR + safety/regulatory review is included before merge.

## Rollback

How can this change be disabled or reverted safely?

---
name: Bug or safety regression
description: Report a reproducible synthetic failure or unsafe state
 title: "[bug] "
labels: []
assignees: []
---

## What happened?

Describe the observed behaviour.

## What should have happened?

Describe the safe / expected behaviour.

## Minimal synthetic reproduction

Please use synthetic data only.

```text
steps / fixture / request
```

## Why it matters

Check any relevant invariant:

- [ ] wrong-patient risk
- [ ] pending → negative / complete
- [ ] unavailable → absent
- [ ] stale → current
- [ ] contradiction hidden / silently resolved
- [ ] provenance lost
- [ ] agent authority / tool-scope issue
- [ ] write / egress issue
- [ ] accessibility / workflow issue
- [ ] other

## Evidence

Logs, screenshots or traces are welcome **only if they contain no PHI, credentials or private hospital information**.

> For a vulnerability that would materially increase exploit risk if published, follow `SECURITY.md` instead of posting exploit details here.

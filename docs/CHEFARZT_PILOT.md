# CareOS — 2-minute Chefarzt pitch

## One sentence
**Wir ersetzen Ihr KIS nicht. CareOS sitzt zunächst lesend daneben und bringt die Informationen zusammen, die Ärzt:innen heute über KIS, Labor, Mikrobiologie, Hygiene, Dokumente, Fax und Telefon zusammensuchen.**

## Why start small
The first request is **not** production access. It is permission for a non-productive usability pilot with synthetic cases.

### Pilot 0 — usability
- 5–10 clinicians
- 20 minutes each
- synthetic data only
- measure task time, clicks/searches, calls that would have been necessary, corrections and cognitive effort

### Pilot 1 — technical read-only evaluation
Only if Pilot 0 shows real value:
- hospital IT + DPO/DSB + information security review
- supported browser/VDI/client environment
- hospital SSO and role/treatment-context policy
- one read-only connector first
- no production write-back

### Pilot 2 — controlled live-data pilot
Only after governance approval:
- one department / narrow workflows
- explicit safety and success metrics
- audit and provenance
- fail-closed behavior
- no autonomous diagnosis or treatment decisions

## Stop rule
If CareOS does not measurably reduce administrative effort, or if correction/error burden rises, stop the pilot.

## What leadership gets
- a measurable answer instead of a transformation promise
- no rip-and-replace of the KIS
- a standards-first path toward FHIR/ISiK where available
- explicit security/privacy gates before PHI
- evidence from the actual clinicians who would use it
# CareOS V8 threat model — first pass

Highest-consequence failure classes:

1. **Wrong patient** — document/fact attached to the wrong person.
2. **Stale truth** — old result displayed as current because ingestion time was mistaken for clinical effective time.
3. **Silent source loss** — summary cannot be traced to the source record/version.
4. **Prompt/document injection** — external document contains instructions that alter system behavior.
5. **Over-broad access** — authenticated user sees patients outside legitimate care context.
6. **Silent partial write** — one downstream action fails while UI says "done".
7. **PHI leakage** — logs, analytics, model provider or error traces contain unnecessary clinical content.
8. **Model/version regression** — update changes extraction/routing behavior without detection.
9. **Guideline drift** — withdrawn/old guidance remains presented as current.
10. **Availability dependency** — FHIR/KIS/identity outage creates false success or unusable clinical workflow.

Controls already demonstrated in prototype form:
- ambiguous identity blocks automatic attachment
- source IDs retained
- red-team benchmark includes stale-result and contradiction attacks
- write-back disabled
- guideline changes enter review, not auto-application
- FHIR outage maps to explicit 503

Still required for real deployment:
- authenticated/authorised end-to-end path
- security testing against real network boundaries
- formal risk ownership and clinical safety process
- operational monitoring + incident response
- external penetration test

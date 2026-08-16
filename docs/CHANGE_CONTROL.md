# CareOS Change Control

Status: target release discipline for the prototype and future regulated/assured lifecycle. The final quality process must be adapted to the independent regulatory assessment and actual deployment obligations.

## Principle

A code change is not just a software change when it can alter **what a clinician sees, which patient it is attributed to, who may access it, how current it is, or what CareOS claims to do**.

Every material change is assigned one or more change classes before release.

## Change classes and mandatory revalidation

| Class | Examples | Required evidence before release |
|---|---|---|
| **C1 Clinical truth** | extraction, normalization, fact schema, contradiction rules, temporal logic, terminology mapping | G1 tests + benchmark comparison + provenance/unsupported-claim metrics + safety review for material behavior changes |
| **C2 Patient identity/context** | matching, patient identifiers, encounter/context binding | wrong-patient adversarial tests + G1/G3 review + integration tests |
| **C3 Interoperability** | FHIR/ISiK profiles, connector mapping, paging, sync/version behavior | connector conformance suite + relevant profile/terminology validation + source freshness tests |
| **C4 Authentication/authorization** | OIDC config, role mapping, treatment context, break-glass, scopes | negative auth tests + authorization suite + audit verification + security review |
| **C5 Privacy/data flow** | new data category, processor/subprocessor, telemetry, export, retention | data-flow update + minimization review + DSFA/DPIA/AVV reassessment as applicable |
| **C6 Reliability/operations** | retry, cache, queue, failover, backup, source-state policy | failure injection + stale/unavailable behavior + rollback/restore evidence |
| **C7 Clinician UX** | default priority, alert/review presentation, source visibility | usability test + safety review where presentation could change interpretation/automation bias |
| **C8 Guideline/evidence** | source/version/local SOP overlay | governed diff + named clinical approval + rollback/version trace |
| **C9 Intended purpose** | diagnosis, treatment recommendation, prioritisation/risk scoring, autonomous actions | G0/G5 external regulatory + clinical-safety reassessment **before implementation/release** |
| **C10 Write capability** | KIS/EHR write-back, orders, messages, task completion | prohibited in current programme; separate transactional safety/regulatory programme required |

A change may belong to multiple classes; all applicable evidence is required.

## Version lineage

Every behaviorally relevant artifact must be identifiable in incident/evaluation evidence where applicable:

- application build/commit;
- connector version/configuration;
- interoperability profile/validator version;
- terminology/rule-pack version;
- specialty-pack version;
- guideline/SOP version;
- parser/extractor/model identifier and version;
- prompt/schema version for model-assisted extraction;
- access-policy version;
- data-mode/safety-control configuration.

## Model / prompt changes

A newer model is **not automatically an upgrade**.

Changing model, provider, prompt, schema or decoding settings is C1 and potentially C5/C6/C9. The change must be evaluated on development cases plus untouched validation holdouts. A model change may be rejected even if average accuracy rises when critical silent misses, unsupported claims, calibration or review burden worsens.

## Benchmark discipline

- frozen holdouts are not prompt/rule-development material;
- new failure families discovered in a holdout are recorded, then a separate development set is created;
- after architectural hardening, create a new untouched holdout;
- safety-critical metrics are reported separately from aggregate accuracy;
- provenance coverage and unsupported-claim rate are part of correctness.

## Release record

A material release record should contain:

1. commit/build identifier;
2. change classes;
3. intended-purpose impact: none / reviewed change;
4. affected workflows/connectors/specialties;
5. linked tests/CI/validation artifacts;
6. benchmark delta where applicable;
7. known residual risks;
8. rollback target/procedure;
9. required external approvals/sign-offs;
10. decision: release / hold / rollback.

## Emergency change

Emergency fixes may reduce the normal lead time but may not bypass evidence needed to prevent a more dangerous release. When evidence cannot be produced quickly enough, the preferred emergency control is disabling the affected CareOS function/connector using the kill switch and returning clinicians to the existing source workflow.

## Regulatory trigger

Any change that could alter CareOS qualification/classification, high-risk AI applicability, or its role as an EHR/interoperability component is automatically C9 and requires a dated reassessment against the then-current rules/guidance.

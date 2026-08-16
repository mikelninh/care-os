# CareOS Safety Case — living argument

Status: **prototype safety case skeleton**. It is not a clinical-safety certification and must be independently reviewed before any live-data clinical deployment.

## Top-level claim

CareOS may only be used in a clinical workflow when evidence supports the claim that it can surface and prepare information **without increasing unacceptable patient-safety risk** relative to the workflow it augments.

This top-level claim is currently **NOT PROVEN**.

## Safety strategy

CareOS does not try to prove that AI is always correct. It aims to make uncertainty, provenance, failure and review explicit enough that unsafe confidence is hard to create and easy to detect.

### S1 — Correct patient context

Hazard: information from the wrong patient is displayed or attached.

Required controls:
- deterministic identifiers where available;
- explicit identity evidence;
- no silent fuzzy merge;
- ambiguous matching enters review;
- cross-patient facts rejected by the canonical fact layer;
- break-glass does not bypass patient identity checks.

Release evidence required:
- wrong-patient adversarial tests;
- zero known silent wrong-patient attachments in validation set;
- real integration test with hospital identity semantics.

### S2 — Source-grounded clinical facts

Hazard: CareOS shows a clinical claim that cannot be traced to supporting source data.

Required controls:
- every fact has immutable source identity;
- document-derived facts require exact evidence span;
- original wording/value preserved;
- transformation/model/parser version recorded;
- provenance coverage is a release metric.

Release target:
- 100% provenance coverage for all surfaced facts.

### S3 — Time and freshness are clinically meaningful

Hazard: stale data is presented as current, or ingestion time is confused with clinical effective time.

Required controls:
- effective time and ingestion time stored separately;
- source refresh state visible;
- stale-data threshold by source/workflow;
- source outage cannot render as an empty/normal result.

### S4 — Contradiction is visible

Hazard: conflicting sources are silently reconciled into one confident statement.

Required controls:
- contradiction groups;
- source/version/time retained for each side;
- unresolved safety-critical contradictions enter review;
- no generated prose may erase the contradiction state.

Primary release metric:
- critical silent contradiction miss rate.

### S5 — Unknown is safer than unsupported certainty

Hazard: extraction/model uncertainty is converted into a plausible but unsupported value.

Required controls:
- explicit `unknown` and `ambiguous` states;
- safety-critical uncertain facts do not enter the quiet/default view;
- human review queue;
- unsupported-claim rate measured separately from general accuracy.

### S6 — Human review is real, not decorative

Hazard: a human-approval button exists but the workflow encourages rubber-stamping.

Required controls:
- source shown at review time;
- changed/uncertain fields highlighted;
- review burden measured;
- correction rate measured;
- consequential write-back remains disabled until separately validated.

### S7 — Failure is fail-visible

Hazard: network, KIS/FHIR, identity, audit or model failure looks like clinical success.

Required controls:
- explicit unavailable/stale/degraded states;
- timeouts and retries do not fabricate currentness;
- partial operations cannot report complete success;
- audit-sink failure has defined policy;
- kill switch and rollback are tested.

### S8 — Access is legitimate and auditable

Hazard: a valid user accesses an illegitimate patient context or excessive data.

Required controls:
- hospital identity/SSO;
- organisation + role + treatment-context policy;
- least privilege;
- break-glass reason and elevated audit;
- central immutable audit without unnecessary clinical free text.

### S9 — Clinical scope does not drift silently

Hazard: product features cross from retrieval/documentation into diagnosis/treatment recommendation without the required regulatory and clinical-risk programme.

Required controls:
- written intended purpose;
- feature-level scope review;
- regulatory change assessment;
- patient-specific treatment recommendation work isolated behind a separate release programme.

## Current evidence

Evidence already present in the repository:

- ambiguous identity can block automatic matching;
- FHIR resource identity is retained in the current adapter;
- FHIR outage maps to explicit 503;
- autonomous clinical write-back is disabled;
- benchmark contains stale-result and contradiction attacks;
- guideline updates require review rather than silent auto-application;
- `app/clinical_truth.py` now rejects facts without source locators and cross-patient truth envelopes.

## Current blockers

- current unseen extraction benchmark contains critical silent contradiction misses;
- no production hospital identity/authorisation path;
- no real KIS/LIS read-only sandbox yet;
- no ISiK profile-validation evidence yet;
- no immutable production audit infrastructure;
- no independent penetration test;
- no external clinical-safety review;
- no formal regulatory qualification/classification assessment;
- no production reliability/failure-injection evidence.

## Release rule

A gate may only be marked `PASS` when evidence is linked. “Implemented” without validation evidence is not sufficient.

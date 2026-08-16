# CareOS Independent Review Brief — G0 / G5

CareOS cannot self-certify the scope, clinical-safety or regulatory gates. This brief defines the questions for qualified independent reviewers.

## Product under review

Current intended-purpose boundary:

> CareOS aggregates and presents source-linked clinical information and prepares administrative clinical documentation for human review. It does not autonomously diagnose, prescribe, select treatment or execute clinical write-back.

Current deployment status: synthetic prototype only; identifiable live patient data is locked by policy.

## Reviewer lane 1 — clinical safety

Preferred reviewer profile: practicing clinician with clinical-safety / health-IT risk experience independent of the core implementation.

Questions:

1. Are the top hazards in `docs/SAFETY_CASE.md` complete enough for the proposed read-only context workflow?
2. Which safety-critical facts/workflows require stronger release thresholds than general extraction accuracy?
3. Are `unknown`, `ambiguous`, `stale`, `unavailable` and `contradictory` states presented safely?
4. Does the human-review design create a realistic verification step rather than automation bias/rubber stamping?
5. Which clinical scenarios should be prohibited from the first live-data pilot?
6. What stop/rollback criteria should the pilot use?

Required output:
- findings with severity;
- missing hazards;
- required mitigations;
- initial-pilot exclusion list;
- explicit go/no-go position for the proposed pilot scope.

## Reviewer lane 2 — MDR / medical-software regulatory

Preferred reviewer profile: EU MDR medical-software regulatory/quality specialist.

Questions:

1. Given the written intended purpose and actual functionality, does any current feature qualify as medical device software?
2. Which proposed features would change that conclusion?
3. If MDSW applies, what classification/rule and conformity path need to be planned?
4. What QMS/software lifecycle/risk-management artifacts are required before the proposed use?
5. How should CareOS separate administrative/context functionality from any future patient-specific clinical decision support?
6. What change-control triggers require regulatory reassessment?

Required output:
- dated qualification/classification memo;
- assumptions and cited guidance;
- feature boundary/red lines;
- required quality/regulatory work programme.

## Reviewer lane 3 — Datenschutz

Preferred reviewer profile: German healthcare Datenschutz expert / DSB or specialised counsel.

Questions:

1. For the proposed hospital deployment, what are the controller/processor roles and legal bases?
2. Is a DSFA required and what risks/mitigations must it include?
3. Are the proposed data minimisation, retention and telemetry boundaries adequate?
4. What patient/data-subject rights processes are required?
5. How should AVV/subprocessor/hosting/international-transfer documentation be structured?
6. Does the proposed provider-data-plane architecture materially reduce privacy risk and what residual issues remain?

Required output:
- data-flow/privacy findings;
- DSFA decision/support;
- documentation requirements;
- go/no-go blockers for live data.

## Reviewer lane 4 — information security

Preferred reviewer profile: healthcare CISO/security architect independent of implementation.

Questions:

1. Is the threat model sufficient for a read-only clinical-context system?
2. Are hospital SSO, treatment-context authorization and break-glass semantics appropriate?
3. What network/deployment architecture is acceptable inside the target hospital?
4. Which audit events are necessary without creating a second PHI leak surface?
5. What must be true for C5/customer controls / §393 SGB V in the chosen hosting model?
6. What penetration-test scope and operational controls are required before live data?

Required output:
- architecture/security findings;
- required controls;
- penetration-test scope;
- deployment blockers.

## Reviewer lane 5 — interoperability

Preferred reviewer profile: German FHIR/ISiK implementer with KIS integration experience.

Questions:

1. Are our selected ISiK modules/resources appropriate for the first hospital workflow?
2. What terminology validation remains outside the reference validator?
3. What vendor-specific gaps should the connector contract expect?
4. Are resource versioning, paging, freshness and identity semantics sufficient?
5. How do we prove that the second hospital does not require a core fork?

## Evidence package

Reviewers should receive at minimum:

- `docs/ARCHITECTURE_V1.md`
- `docs/SAFETY_CASE.md`
- `docs/DATA_FLOW_AND_PRIVACY.md`
- `docs/THREAT_MODEL.md`
- `docs/PRODUCTION_READINESS.md`
- `docs/REGULATORY_BASELINE_DE.md`
- `docs/GATES.md`
- benchmark results
- ISiK CI artifacts
- current public synthetic demo

## Pass rule

G0/G5 may not become `PASS` because a document exists. They require named, dated independent findings and closure of all release-blocking findings for the intended pilot scope.

# CareOS DSFA / DPIA Support Dossier

Status: **support material only**. The responsible controller / Datenschutzbeauftragte must decide applicability, complete the assessment and approve the deployment.

## 1. Processing under assessment

Proposed first live scope:

- one provider / hospital;
- one clinical department;
- read-only clinical context;
- no autonomous diagnosis/treatment decision;
- no autonomous clinical write-back;
- provider-controlled data plane preferred;
- explicit clinician authentication and patient/treatment-context authorization.

## 2. Purpose

Reduce manual reconstruction of patient context across existing authorised clinical sources while preserving source provenance and making uncertainty/failure visible.

The assessment must reject vague secondary purposes such as "future AI improvement" unless separately justified and governed.

## 3. Data categories to document per deployment

For every enabled connector/view, record:

- data element/category;
- source system;
- purpose;
- affected data subjects;
- recipients/audience;
- storage/processing location;
- retention period;
- export/transfer path;
- whether identifiable data leaves the provider data plane;
- whether subprocessors can access it.

## 4. Data-flow inventory

Use `docs/DATA_FLOW_AND_PRIVACY.md` as the architecture baseline and replace all generic boxes with the target hospital's actual systems, network zones, identities, vendors and processors.

## 5. Threat / privacy risk prompts

Assess at minimum:

- excessive patient access by a legitimate user;
- wrong-patient context;
- PHI leakage through logs/analytics/errors;
- cloud/subprocessor access beyond intended scope;
- stale or incorrectly reconciled data affecting a person's care;
- insufficient transparency/auditability;
- re-identification of evaluation data;
- uncontrolled secondary use/model training;
- retention beyond necessity/legal duty;
- insecure export/download;
- proxy/family/payer audience leakage;
- support/admin access;
- incident and recovery processes.

## 6. Controls already designed / prototype evidence

- federated provider data-plane architecture;
- fail-closed treatment-context policy contract;
- no payer mirror of clinician record;
- clinical free text forbidden from ordinary audit-event schema;
- source-grounded fact contract;
- explicit stale/unavailable states;
- autonomous clinical write-back disabled;
- live-data gate remains locked.

These are not equivalent to deployed controls and must be re-evaluated against the actual infrastructure.

## 7. Required live-deployment evidence

- working hospital SSO/OIDC;
- authoritative org/role/treatment-context mapping;
- central immutable audit;
- encryption/key/secrets architecture;
- production network diagram;
- retention/deletion configuration;
- subprocessor list and agreements;
- hosting location/evidence;
- support/admin-access policy;
- backup/restore design;
- incident-response process;
- independent penetration test;
- applicable §393 SGB V/C5/customer-control evidence where relevant.

## 8. Residual-risk decision

For each high risk, record:

| Risk | Initial severity | Mitigation | Evidence | Residual severity | Owner | Accepted by |
|---|---|---|---|---|---|---|
| _hospital-specific_ | | | | | | |

No CareOS code or automated gate may substitute for the controller's documented residual-risk decision.

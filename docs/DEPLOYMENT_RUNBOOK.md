# CareOS Hospital Deployment & Rollback Runbook

Target scope: first controlled **read-only** live-data pilot after G0–G5 pass and hospital approval.

## Pre-deployment checklist

### Governance
- pilot owner and clinical owner named;
- Datenschutz/IT-security/integration approvals recorded;
- intended purpose and prohibited actions agreed;
- exact patient/user population defined;
- stop criteria agreed;
- support/escalation contacts tested.

### Identity / authorization
- hospital IdP issuer/audience/JWKS verified;
- trusted role/organisation mapping tested;
- treatment-context source tested;
- break-glass behavior tested;
- write scopes absent/disabled;
- unauthorized/wrong-context test cases fail closed.

### Connectivity
For each connector record:
- source/vendor/version;
- endpoint/network zone;
- auth mechanism;
- resources/data allowlist;
- pagination/version/freshness behavior;
- timeout/retry limits;
- expected volume/latency;
- degraded-mode behavior.

### Security / privacy
- secrets in managed secret store;
- TLS/certificates validated;
- audit sink reachable;
- PHI-safe telemetry verified;
- backup/restore tested for CareOS-owned state;
- data retention configured;
- penetration-test blockers closed;
- subprocessor/hosting evidence current.

## Deployment stages

### Stage 0 — synthetic environment
Run complete regression, ISiK validation, failure injection and smoke tests.

### Stage 1 — hospital network, no PHI
Validate DNS/TLS/SSO/network/audit/monitoring with synthetic identities/data where possible.

### Stage 2 — tightly scoped read-only live connection
- allowlisted users;
- limited pilot department;
- no write-back;
- source freshness visible;
- heightened monitoring;
- pilot metrics collection without unnecessary PHI.

### Stage 3 — expand only after review
Expansion requires review of incidents, corrections, provenance, silent-miss metrics, user burden and source reliability.

## Go-live checks

- health endpoints green;
- readiness gates evidence linked;
- all enabled connectors current/reachable or explicitly degraded;
- wrong-audience/wrong-context auth tests fail;
- audit events observed centrally;
- rollback/kill switch tested immediately before activation;
- clinical owner confirms pilot scope.

## Kill switch

A pilot must have a documented method to:

1. deny all CareOS user access;
2. disable individual connectors;
3. disable any generated/prepared outputs;
4. preserve audit/evidence needed for investigation;
5. return clinicians to the existing source-system workflow.

CareOS must never be a single point of failure for basic care during the first deployment stages.

## Immediate rollback triggers

- suspected wrong-patient data;
- unsupported clinical claim without provenance;
- critical contradiction silently hidden;
- authorization bypass;
- PHI leakage;
- audit failure that violates agreed policy;
- source outage represented as current/complete;
- material unexplained discrepancy with source system;
- security incident requiring containment;
- clinical owner requests stop.

## Post-deployment review

At agreed intervals review:
- availability/freshness;
- auth denials/break-glass;
- corrections;
- critical silent misses;
- provenance coverage;
- review burden;
- workflow time saved;
- incidents/security findings;
- clinician feedback.

No automatic expansion based solely on usage or satisfaction.

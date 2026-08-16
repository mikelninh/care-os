# CareOS AVV / DPA Requirements Checklist

Status: requirements checklist for counsel/Datenschutz review, **not a legal contract template**.

Before any processor relationship involving identifiable health data, the parties should turn the actual deployment architecture into the appropriate binding agreement(s).

## Deployment facts that must be fixed first

- controller / processor / subprocessor roles;
- exact service scope and purposes;
- categories of personal/health data;
- affected data subjects;
- processing duration;
- provider/control-plane boundaries;
- hosting and processing locations;
- support/admin-access paths;
- all subprocessors;
- deletion/return obligations and clinical-retention constraints.

## Security annex inputs

The final contractual/security annex should reference deployed, testable controls rather than promises:

- identity and authentication;
- role/treatment-context authorization;
- privileged/admin access;
- encryption in transit/at rest;
- managed keys/secrets and rotation;
- immutable audit;
- vulnerability/patch management;
- backup/restore;
- availability/recovery;
- tenant segregation where applicable;
- logging/monitoring/incident response;
- secure development/release process;
- penetration testing;
- data deletion/return;
- support access controls.

## Subprocessor change control

For each subprocessor maintain:

- legal entity;
- purpose/service;
- data categories accessible;
- processing location(s);
- security/compliance evidence;
- contractual chain;
- change notification/objection mechanism where required;
- exit/deletion procedure.

## Incident cooperation

Define operationally—not only legally:

- who detects;
- who triages;
- notification contacts;
- required evidence/log preservation;
- timelines/escalation path;
- containment authority;
- patient-safety escalation where confidentiality/integrity/availability could affect care;
- post-incident corrective-action process.

## Audit / assistance capability

CareOS must be able to provide evidence needed for the agreed controller oversight and rights/obligations workflows without exporting unrelated patient data.

## Gate rule

G3 cannot pass because this checklist exists. It passes only when the actual target deployment has the necessary agreements, technical controls, evidence and responsible-party approval.

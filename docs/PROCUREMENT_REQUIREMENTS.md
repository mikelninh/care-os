# CareOS Procurement / Public-Sector Requirements

Purpose: define architecture-neutral requirements that a hospital group or public body could use to evaluate a clinical context-layer implementation without locking itself to CareOS or one KIS vendor.

## 1. Architecture

A compliant solution should:

- operate beside existing systems of record;
- not require a central national copy of all identifiable patient data;
- support provider-local/dedicated-tenant processing;
- document trust boundaries and every patient-data flow;
- support read-only deployment before write-back;
- provide a documented exit/rollback path.

## 2. Interoperability

The supplier should:

- use applicable German/EU standards before proprietary interfaces;
- document exact FHIR/ISiK/ISiP/profile versions where used;
- expose vendor-specific differences through documented adapter/capability contracts;
- preserve source identifiers, versions and timestamps;
- document pagination/partial-read behavior;
- distinguish profile validation from terminology validation;
- provide machine-readable export of the canonical context/provenance model where legally permitted.

## 3. Clinical truth / provenance

Every surfaced clinical assertion should provide:

- source system;
- source/resource/document identifier;
- source version/time where available;
- original source value/wording;
- normalized representation without destroying original value;
- effective clinical time where known;
- evidence span for document-derived facts;
- uncertainty/review state;
- contradiction/supersession state where applicable.

Generated prose without source-grounded structured evidence should not be accepted as the sole clinical context representation.

## 4. Identity and access

Required:

- strong provider-approved authentication;
- organization/role/scope authorization;
- patient/encounter/treatment-context binding;
- deterministic patient identity safeguards;
- break-glass control + high-signal audit;
- separate read/write capabilities;
- session/revocation behavior documented.

Name/DOB similarity alone must not silently merge patients.

## 5. Failure semantics

The solution must distinguish:

- no matching data;
- source unavailable;
- source stale;
- source response partial/incomplete;
- ambiguous/unknown;
- contradictory;
- explicitly negative.

A dependency outage must not become a clinically reassuring empty state.

## 6. AI/model independence

If AI is used:

- model output must not directly become trusted clinical truth without validation;
- exact supporting source evidence must be available;
- model/provider/version must be recorded where relevant;
- model failure must have a defined degraded mode;
- data sent to external model providers must be documented and approved;
- retention/training/processing-location terms must be explicit;
- the basic clinical truth model must not depend on one proprietary model vendor.

## 7. Security

Supplier evidence should include:

- threat model;
- encryption/key/secrets design;
- audit integrity design;
- tenant isolation evidence;
- vulnerability/dependency/SBOM process;
- penetration-test report before live deployment;
- backup/restore tests;
- incident-response and breach process;
- SIEM/security monitoring integration;
- software supply-chain evidence;
- secure update/rollback process.

## 8. Cloud / German healthcare requirements

Where §393 SGB V applies, procurement must include:

- processing locations/legal entity requirements;
- current C5 Type 2 evidence or legally recognized equivalent as applicable;
- the corresponding customer-control mapping;
- subprocessors;
- shared-responsibility matrix.

A C5 report alone must not be treated as evidence that customer-side controls are implemented.

## 9. Datenschutz

Before live data:

- controller/processor roles determined;
- purpose/data-minimization register;
- provider-specific data-flow diagram;
- legal-basis assessment by responsible parties;
- DSFA/DPIA where required;
- AVV/DPA where applicable;
- subprocessor register;
- retention/deletion schedule;
- transparency/data-subject-rights process;
- provider DSB approval process.

## 10. Regulatory / quality

The supplier should provide:

- intended purpose;
- MDR/MDSW qualification/classification analysis by qualified persons;
- AI Act applicability analysis;
- EHDS applicability mapping;
- risk-management file;
- classification-appropriate QMS/lifecycle evidence;
- software/model/data change-control records.

## 11. Reliability / operations

Required before production:

- SLOs;
- RPO/RTO;
- dependency inventory;
- measured backup/restore;
- source freshness policies;
- failure-injection results;
- incident/rollback exercise;
- kill switch;
- support and escalation model;
- maintenance/update windows.

## 12. Usability and workflow

A context layer should not create another independent daily system.

Evidence should demonstrate:

- same-login / SSO path;
- same-patient context launch where possible;
- supported managed browser/Citrix/VDI environment;
- no mandatory duplicate patient search;
- reduction rather than increase in copy/paste/duplicate documentation;
- source verification discoverable without specialist training.

## 13. Outcome/evidence requirements

At pilot and scale stages, measure:

- time to required fact;
- clinician task time returned;
- correction rate;
- provenance coverage;
- wrong-source rate;
- wrong-patient rate;
- critical silent miss rate;
- review/false-alert burden;
- source freshness;
- calls/faxes/manual searches avoided;
- cognitive effort;
- weekly/repeated use;
- cross-site/vendor repeatability.

Avoid accepting unsupported claims of mortality, cost savings or national impact before appropriate evaluation.

## 14. Portability and exit

Procurement should require:

- documented canonical export format;
- exportable configuration/mappings where contractually possible;
- source references preserved;
- no proprietary patient identifier as sole key;
- documented data deletion/return on exit;
- provider-owned audit export;
- transition plan to another implementation/vendor.

## 15. Open reference approach

A public-sector programme can use CareOS as one reference implementation while making these contracts implementation-neutral. That enables competition on UX, integration quality and operations without repeatedly reinventing core safety/interoperability semantics.

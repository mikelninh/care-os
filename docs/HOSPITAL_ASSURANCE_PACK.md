# CareOS Hospital Assurance Pack

This is the document index a hospital should receive before a live-data pilot is proposed.

The pack is intentionally designed for four reviewers who ask different questions:

- **Clinical leadership:** does this improve care workflow without hiding risk?
- **CIO / integration:** how does it connect, fail and recover?
- **CISO / Informationssicherheit:** what can an attacker or failure expose or corrupt?
- **Datenschutz:** why is each data flow necessary and under what governance?

## A. Product & clinical boundary

- `README.md` — product thesis and public demo scope
- `docs/ARCHITECTURE_V1.md` — federated target architecture
- `docs/SAFETY_CASE.md` — safety claims, evidence and blockers
- written intended-purpose statement
- specialty-pack workflow description for the pilot department
- explicit list of prohibited/autonomous actions

## B. Interoperability dossier

- `docs/FHIR_INTEGRATION.md`
- pinned ISiK validation CI artifact
- exact ISiK/plugin/validator versions
- hospital/vendor capability matrix
- resources/fields requested from each source
- paging/version/freshness behavior
- source outage/degraded-mode behavior
- read/write capability separation

## C. Datenschutz dossier

- `docs/DATA_FLOW_AND_PRIVACY.md`
- system/data-flow diagram
- purpose + data-category register
- controller/processor role assessment
- AVV/DPA draft where appropriate
- subprocessor register
- hosting/processing locations
- retention/deletion schedule
- DPIA/DSFA support material and final assessment by responsible parties
- data-subject rights process where applicable
- §393 SGB V/C5 evidence and customer-control mapping if applicable

## D. Information-security dossier

- `docs/THREAT_MODEL.md`
- authentication/authorization design
- treatment-context + break-glass policy
- immutable audit design
- encryption/key/secrets design
- tenant isolation evidence
- vulnerability/dependency/SBOM process
- penetration-test scope/report
- incident-response + breach workflow
- backup/restore evidence
- security logging/SIEM design

## E. Reliability / operations dossier

- dependency inventory
- SLOs and alerting
- failure-injection results
- stale/current/unavailable source semantics
- RPO/RTO
- backup/restore test record
- rollback/kill-switch procedure
- maintenance/update process
- support/on-call/escalation model

## F. Regulatory / quality dossier

- `docs/REGULATORY_BASELINE_DE.md`
- independent MDR/MDSW qualification/classification assessment
- AI Act applicability assessment
- EHDS applicability/interoperability mapping
- clinical risk-management file
- change-control process
- software/model/data versioning and release records
- QMS/lifecycle evidence appropriate to the resulting classification

## G. Pilot evidence dossier

Before scaling, the hospital should receive the protocol and results for:

- usability;
- median time-to-required-fact;
- clicks/searches/calls/faxes avoided;
- documentation reuse;
- correction rate;
- provenance coverage;
- unsupported-claim rate;
- wrong-patient rate;
- critical silent contradiction miss rate;
- false-alert/review burden;
- clinician cognitive-effort score;
- availability/freshness.

## Pilot go/no-go rule

No one document makes CareOS safe. A live-data pilot can only be proposed when the machine-readable core gates G0–G5 are `PASS`, the hospital's own responsible reviewers accept the deployment, and a rollback/stop condition is agreed before activation.

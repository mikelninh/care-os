# Production security & compliance gap map (Germany)

CareOS V8 is **not production-certified**. This document turns the gap into explicit gates.

## Before any live patient-data pilot

### Identity and access
- OIDC/SSO with issuer + audience validation
- role and organisation context
- treatment/patient context where required
- least-privilege scopes
- session expiry and revocation
- break-glass workflow with audit

### Data protection
- controller/processor roles agreed
- DPA / AVV and subprocessor inventory
- DPIA/DSFA where required
- data minimisation and retention schedule
- encryption in transit and at rest
- no PHI in ordinary product telemetry
- access/export/deletion workflows matching applicable law and clinical retention duties

### German cloud requirements
For covered German health/social data cloud processing, §393 SGB V imposes location/security conditions and an applicable current C5 attestation/equivalent-security route. CareOS therefore treats cloud compliance evidence as a deployment blocker, not a marketing checkbox.

### Security operations
- central immutable audit sink
- SIEM alerting
- incident response + breach process
- vulnerability management and dependency/SBOM scanning
- penetration test before live deployment
- backup, restore, RPO/RTO tests
- secrets management and key rotation
- tenant isolation testing

### Clinical/product boundary
- written intended purpose
- regulatory classification assessment (MDR / AI Act as applicable)
- clinical risk management
- human approval boundary
- model/data versioning
- rollback and kill switch
- measured error/correction/critical-miss rates

### Interoperability
- FHIR transport tests
- relevant ISiK profile validation for German hospital workflows
- vendor-specific capability matrix
- explicit stale-data and outage behavior
- no automatic patient merge under ambiguity

## Deployment stages

1. **Synthetic demo** — no PHI.
2. **Controlled usability study** — synthetic/de-identified data.
3. **Read-only live-data pilot** — security/privacy/legal gates complete.
4. **Transactional pilot** — write-back-specific risk and conformance gates complete.
5. **Scaled production** — operations, attestations/certifications and vendor integrations proven.

The repository's `/api/security/readiness` endpoint is a configuration gate only. It is intentionally impossible for a default demo environment to claim production readiness.

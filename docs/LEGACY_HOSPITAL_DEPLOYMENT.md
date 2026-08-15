# CareOS legacy-hospital deployment strategy

## Principle
Do **not** weaken CareOS to support an unsafe, unsupported operating system. Keep the legacy KIS untouched and put CareOS behind a supported execution surface.

## Immediate demo
- Public static browser app with synthetic data only.
- No PHI, login or backend patient persistence.
- Works as a zero-install test on phone, tablet and supported desktop browsers.

## Hospital pilot path
1. Use a current hospital-supported browser on a managed workstation where available.
2. If a ward workstation is legacy, use a hospital-managed Citrix/VDI/RDS session running a current supported browser.
3. Alternative: a managed tablet/thin client for CareOS while the old KIS stays on the existing terminal.
4. For real patient data, deploy internally or on an approved health-cloud setup; never use the public demo infrastructure.
5. Integrate **read-only first**. No production write-back until policy, audit, idempotency, transaction status and rollback/compensation are proven.

## Production controls before PHI
- hospital SSO/OIDC and organisation + role + treatment-context authorization
- least privilege; read does not imply write
- purpose limitation and data minimisation
- encryption in transit and at rest
- no PHI in ordinary telemetry
- append-only access/audit events
- retention/deletion policy
- DPA/AVV, DPIA/DSFA support, subprocessor inventory
- deployment/cloud evidence appropriate to §393 SGB V where applicable
- incident response, backup/restore and vulnerability management

## Compatibility boundary
For real clinical use, require a hospital-supported browser and client environment with current TLS/security patches. Do not target IE6/IE11 or unsupported Windows versions for PHI. The synthetic share demo can degrade gracefully on older/low-power browsers, but that is **not** security approval for those clients.

## German interoperability
The hospital integration path is standards-first: FHIR/ISiK where available, then vendor/read adapters, document/fax ingestion and safe human-mediated fallback. The existing KIS remains the source of truth.
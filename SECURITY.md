# Security & clinical-safety policy

CareOS is a healthcare software research project with explicit production-readiness gates.

## Do not use this repository for live patient care

The public repository and browser demos are **synthetic-only**. They are not approved, certified, validated, or configured for identifiable live patient data or clinical use.

The current project must not be used to:

- process identifiable real patient data in the public/demo deployment;
- make autonomous diagnoses or treatment decisions;
- write directly into a production KIS/PVS/EHR;
- automatically merge ambiguous patient identities;
- replace clinical review or professional judgement.

Identifiable live-patient-data mode remains locked until the required readiness gates are evidence-backed PASS and the target provider's responsible security, privacy, clinical and regulatory reviewers approve the deployment.

## Current security / safety principles

- Provider-side PHI by default; no routine identifiable PHI in the shared control plane.
- Source provenance is mandatory for surfaced clinical facts.
- Missing, stale, unavailable, contradictory and explicitly negative are separate states.
- Ambiguous patient matching fails closed.
- Authentication does not by itself authorize access to patient data.
- Treatment-context / patient-context policy is explicit.
- Read and write are separate connector capabilities.
- AI/model output is an untrusted candidate until evidence is independently verified.
- Required audit failure can fail closed rather than permit invisible access.
- Pilot claims are derived from measured evidence rather than hard-coded savings claims.

## Reporting a vulnerability

Please do **not** open a public issue containing:

- exploit details that would materially increase risk before remediation;
- credentials, tokens, keys or secrets;
- personal data or health data;
- hospital network architecture/details that are not already public;
- screenshots/logs containing patient or staff identifiers.

Preferred route: use GitHub's private security-advisory / vulnerability-reporting mechanism for this repository when available. If private reporting is unavailable, contact the repository owner privately before sharing technical exploit details.

## Never use patient data for security testing

Do not demonstrate a vulnerability with real patient data. Use synthetic fixtures only unless a future formally approved test environment and protocol explicitly authorizes otherwise.

## High-priority vulnerability classes

Treat as release-blocking/high priority:

- wrong-patient disclosure or cross-tenant access;
- authentication or authorization bypass;
- treatment-context bypass;
- break-glass bypass or missing high-signal audit;
- leakage of PHI into logs, telemetry or the control plane;
- connector origin confusion, SSRF or unsafe redirects;
- source-state failures that turn unavailable/stale data into reassuring absence;
- audit tampering/bypass;
- secret/key disclosure;
- unsafe model/document admission that bypasses provenance/evidence checks;
- write capability reachable through a read-only deployment;
- supply-chain compromise affecting release artifacts.

## Architecture and assurance references

- `docs/ARCHITECTURE_V2.md`
- `docs/TRUST_AND_DATA_FLOW.md`
- `docs/THREAT_MODEL.md`
- `docs/HOSPITAL_ASSURANCE_PACK.md`
- `docs/GATES.md`
- `docs/TECHNICAL_DOCUMENTATION_INDEX.md`

## Dependency and supply-chain evidence

The repository runs scheduled/push dependency vulnerability auditing and emits a CycloneDX SBOM artifact via `.github/workflows/supply-chain-security.yml`.

Dependabot is configured for Python and GitHub Actions updates.

These controls reduce known supply-chain risk but do not replace code review, artifact signing/provenance, penetration testing or provider-specific security assurance.

## Production requirements still external

Before a real hospital deployment, CareOS still requires, among other things:

- provider IdP/SSO integration;
- production authorization/context mapping;
- provider-approved KMS/secrets/encryption;
- protected central audit/SIEM integration;
- backup/restore and incident exercises;
- target-environment threat review;
- independent penetration test;
- hospital-specific privacy/security approvals;
- classification-appropriate regulatory/quality evidence.

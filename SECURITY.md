# Security & clinical-safety boundaries

CareOS is currently a **synthetic-data research and clinician-UX prototype**.

## Do not use this repository for live patient care

The current version is not approved, certified, validated, or configured for production healthcare use. In particular, it must not be used to:

- process real patient data;
- make autonomous diagnoses or treatment decisions;
- write directly into a production KIS/PVS/EHR;
- automatically merge ambiguous patient identities;
- replace clinical review or professional judgement.

## Current safety principles

- Synthetic patient data only.
- Source provenance remains visible for surfaced clinical information.
- Ambiguous patient matching fails closed and requires human confirmation.
- AI/workflow output is treated as preparation for human review, not autonomous execution.
- Pilot claims are derived from measured task completion rather than hard-coded savings claims.

## Responsible disclosure

If you discover a security or safety issue in this prototype, please open a GitHub issue that contains no personal or patient data. For sensitive vulnerabilities, contact the repository owner privately rather than publishing exploit details.

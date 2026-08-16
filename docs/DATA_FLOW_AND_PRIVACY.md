# CareOS Data Flow & Privacy Boundary — hospital pilot dossier

Status: **assurance-design document**, not a GDPR compliance attestation or legal advice.

## Deployment principle

For identifiable clinical data, CareOS prefers a **provider-controlled data plane**. The CareOS control plane should distribute software/configuration/policy and collect only the minimum non-PHI operational data required to operate the service.

## Proposed read-only hospital flow

```text
Hospital identity provider
        │ authenticated clinician
        ▼
CareOS policy enforcement ────────► central audit sink
        │                              (no note free text)
        │ legitimate patient context
        ▼
Provider CareOS data plane
        │
        ├── KIS / ISiK / FHIR
        ├── LIS / microbiology
        ├── RIS/PACS metadata where required
        ├── document gateway
        └── local SOP/evidence metadata
        │
        ▼
Canonical Clinical Fact Graph
        │ source/time/version/uncertainty
        ▼
Clinician view
```

## Data categories

### Identifiable clinical data — provider data plane
Examples:
- patient identifiers;
- diagnoses and findings;
- medications/allergies;
- laboratory/microbiology results;
- clinical documents;
- care-team tasks and follow-up state.

Default architecture rule: do not export these to a general SaaS control plane merely for analytics or model improvement.

### Security/audit metadata
Examples:
- pseudonymous actor/patient reference;
- resource/action identifier;
- access outcome;
- timestamp;
- break-glass flag/reason category where appropriate.

No ordinary audit/telemetry event should contain clinical note free text.

### Product/operational metrics
Preferred examples:
- latency;
- source availability;
- clicks/searches/calls saved in a pilot;
- correction counts;
- error category;
- application/version identifiers.

Where a metric can be measured without PHI, it should be.

## Purpose limitation

A field entering CareOS must have:

1. a defined workflow purpose;
2. a source and lineage;
3. an audience/access policy;
4. a retention rule;
5. a reason it is necessary for the configured deployment.

Adding data because it might be useful later is not an acceptable default.

## Processing-role questions for each deployment

Before live data, the hospital and CareOS legal/privacy reviewers must document:

- controller / processor / joint-controller roles for each flow;
- legal basis and, where relevant, Article 9 condition;
- hosting and subprocessor chain;
- international transfer position;
- retention/deletion obligations and clinical-record duties;
- patient/data-subject rights workflow;
- whether a DPIA/DSFA is required and its outcome;
- whether §393 SGB V applies to the chosen cloud path and which C5/equivalent evidence/customer controls apply.

## Data-minimisation controls to implement

- connector-level field allowlists;
- purpose-specific API/view schemas;
- no payer access to clinician-only fields by default;
- no clinical free text in ordinary telemetry;
- configurable retention by data class;
- explicit export/delete workflows where legally applicable;
- local processing for transformation tasks when practical and beneficial;
- de-identification/pseudonymisation for evaluation datasets where appropriate;
- no secondary model-training use without a separate lawful/governed basis.

## Live-data blockers

This design does not authorize live use. G0–G5 must pass, including actual authentication/authorization, immutable audit, encryption/key management, operational security, privacy assurance and independent review.

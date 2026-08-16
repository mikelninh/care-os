# CareOS Architecture V1 — Federated Clinical Context Layer

Status: **architecture decision record / target architecture**, not a production-readiness claim.

## Product boundary

CareOS is designed to aggregate and present source-linked clinical information and prepare administrative clinical documentation for human review.

The default CareOS intended-use boundary does **not** include autonomous diagnosis, prescribing, treatment selection, or autonomous clinical write-back. Features crossing that boundary require a separate clinical-risk and regulatory programme before implementation or release.

## Core architecture decision

CareOS must not become a national central patient database.

Clinical data should remain in the provider environment, or in a tightly controlled provider-specific tenant, while CareOS distributes software, versioned specialty packs, policy/configuration and non-PHI operational metadata.

```text
                         CAREOS CONTROL PLANE
              releases · pack versions · policy bundles
              guideline metadata · non-PHI operations
                                │
                    no routine identifiable PHI
                                │
────────────────────────────────┼──────────────────────────────
                                │
                       PROVIDER DATA PLANE
                                │
 KIS · LIS · RIS/PACS · PVS · ePA · KIM · documents · nursing
                                │
                                ▼
                       Connector Gateway
                                │
                                ▼
                     Patient Identity Layer
                                │
                                ▼
                   Canonical Clinical Fact Graph
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
      provenance          temporal semantics       terminology
      + versions          + freshness              + units
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
                    contradiction / review engine
                                │
                         policy enforcement
                                │
               ┌────────────────┼────────────────┐
               ▼                ▼                ▼
            Clinician       Patient/family   Coordination
```

## Mandatory fact contract

A surfaced clinical fact must carry, at minimum:

- patient reference;
- canonical fact type;
- original value/wording;
- normalized value/code where available without overwriting the original;
- source system;
- resource/document identity;
- resource version where available;
- exact evidence span for document-derived facts;
- clinical effective time where known;
- recorded/ingestion time separately;
- transformer/parser/model version;
- status (`confirmed`, `ambiguous`, `unknown`, `rejected`);
- contradiction/review state.

The implementation begins in `app/clinical_truth.py`.

## Failure semantics

CareOS must distinguish:

- `source returned no matching data`;
- `source is unavailable`;
- `source data is stale`;
- `data is contradictory`;
- `data is ambiguous`;
- `data is unknown`.

**Absence of data is never silently converted into evidence of absence.**

## German interoperability

The target connector gateway supports:

1. FHIR R4 transport where available;
2. applicable gematik ISiK profiles for hospital workflows;
3. applicable ISiP profiles for nursing/care workflows;
4. ePA/TI/KIM paths where legally and technically appropriate;
5. vendor-specific read adapters only behind a common connector contract;
6. controlled document ingestion for legacy gaps.

Generic FHIR compatibility is not equivalent to ISiK confirmation/conformance.

## Security boundary

No live-data deployment is allowed until working controls replace the current configuration-only gates, including:

- hospital OIDC/SSO;
- organisation/role/treatment-context authorisation;
- least privilege and read/write separation;
- break-glass with reason and audit;
- central append-only/immutable audit;
- PHI-safe observability;
- encryption and managed secrets/keys;
- backup/restore and incident response;
- tenant isolation tests;
- applicable German cloud evidence and customer controls.

## Architectural anti-goals

CareOS must not:

- require replacing the KIS/PVS/EHR to create initial value;
- silently merge uncertain patient identities;
- silently reconcile contradictory clinical facts;
- silently hide source provenance;
- depend on one model vendor for basic availability;
- turn a source outage into a clinically reassuring empty state;
- force every specialty or country into a separate product fork;
- create a payer-accessible mirror of the clinician record.

## Scale criterion

A second hospital must be deployable by adding/configuring connectors, terminology mappings, local policy/SOP overlays and specialty packs — not by forking the CareOS core.

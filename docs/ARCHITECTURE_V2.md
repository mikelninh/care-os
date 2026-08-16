# CareOS Reference Architecture V2

Status: **proposal-ready reference architecture** — not a claim of production approval, certification, or clinical validation.

Baseline date: **2026-08-16**.

## 1. Executive architecture statement

CareOS is a **federated clinical context layer** for fragmented healthcare environments.

It is designed to:

- keep authoritative clinical records in existing provider systems;
- connect through standards-first, read-only interfaces before any transactional capability;
- transform source data into a canonical, provenance-preserving clinical fact model;
- make uncertainty, source unavailability, staleness, ambiguity and contradiction explicit;
- separate clinical truth from presentation, specialty workflow, country rules and audience permissions;
- integrate into the clinician's existing patient context rather than create another independent patient-search workflow;
- allow providers to retain operational sovereignty over identifiable patient data.

CareOS is **not** intended to become a national central patient database or replace every KIS/PVS/EHR.

## 2. Architectural principles

1. **System of record remains authoritative.** CareOS is not the primary clinical record.
2. **Provider-side PHI by default.** Routine identifiable patient data remains in the provider data plane or a dedicated provider-controlled tenant.
3. **Provenance is part of correctness.** A surfaced clinical fact without traceable origin is incomplete.
4. **Unknown is a valid state.** Missing, stale, unavailable, contradictory and negative are not interchangeable.
5. **Models are untrusted proposers.** LLM/model output cannot directly become trusted clinical truth.
6. **Read and write are separate capabilities.** Read-only value must be demonstrable before transactional integration is considered.
7. **Identity is deterministic where possible.** Names/dates of birth alone never silently merge patients.
8. **Same patient context, not another search box.** Production workflow should receive trusted patient/encounter context from the surrounding clinical system.
9. **Composition over forks.** Specialty, country, language and audience behavior extend one core rather than create separate products.
10. **Fail visibly.** Source outage, stale data, partial reads or audit failure must not look like a normal empty chart.
11. **Least privilege and treatment context.** Authentication alone never grants patient access.
12. **Evidence-backed gates.** Production readiness is earned through explicit evidence and independent review.

## 3. Logical architecture

```text
                            CAREOS CONTROL PLANE

          releases · signed pack versions · policy/config bundles
       terminology metadata · guideline metadata · non-PHI operations
                                 │
                       no routine identifiable PHI
                                 │
═════════════════════════════════╪════════════════════════════════════
                                 │
                    PROVIDER / HOSPITAL DATA PLANE
                                 │
 KIS/EHR ─┐                      │
 LIS/Micro├───> Connector Gateway / Integration Boundary
 RIS/PACS ┤                      │
 PVS      ┤                      ▼
 ePA/TI   ┤              Identity + Encounter Layer
 KIM      ┤                      │
 Docs     ┘                      ▼
                         Clinical Truth Layer
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
     provenance/version     temporal/freshness    terminology/units
           │                     │                     │
           └─────────────────────┼─────────────────────┘
                                 ▼
                       Reconciliation Engine
                contradiction · supersession · review
                                 │
                                 ▼
                       Policy Enforcement Point
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
      Clinician             Patient/family         Coordination
         UX                      UX                   minimum data
```

## 4. Control plane vs provider data plane

### CareOS control plane

May contain:

- software releases and integrity metadata;
- versioned specialty/country/language/audience packs;
- policy schemas;
- terminology/guideline metadata and version references;
- non-PHI health/telemetry and deployment status;
- connector capability definitions;
- conformance artifacts and release evidence.

It should **not** require routine copies of identifiable longitudinal patient records.

### Provider data plane

Contains or processes identifiable clinical context required for care:

- source-system retrieval;
- patient/encounter identity resolution;
- canonical clinical facts;
- source provenance and evidence spans;
- access decisions;
- provider audit events;
- short-lived caches where explicitly approved;
- local configuration/SOP overlays where required.

The preferred deployment model places these functions inside the provider trust boundary or in a dedicated provider-controlled tenant.

## 5. Connector gateway

Every connector implements the same behavioral contract regardless of vendor:

```text
Connector request
  + authenticated organisation/user context
  + patient/encounter context
  + requested capability
            ↓
ConnectorReadResult
  = SourceState
  + TruthEnvelope
  + capability metadata
```

Mandatory semantics:

- bounded paging;
- source identity;
- version/timestamp preservation where available;
- explicit `current / stale / unavailable / unknown` state;
- no silent truncation;
- no cross-origin pagination continuation;
- no write capability unless separately authorised, implemented and released;
- source-specific failures remain visible upstream.

Preferred interoperability order:

1. applicable gematik/FHIR interfaces (including ISiK in hospitals where applicable);
2. other documented standards/interfaces;
3. vendor APIs behind the common connector contract;
4. controlled document ingestion for remaining legacy gaps.

## 6. Patient and encounter identity

The identity layer separates **strong identifiers** from demographic similarity.

Rules:

- a unique shared verified identifier may support automatic attachment;
- conflicting strong identifiers block automatic attachment;
- name + date of birth + address may support review but not silent merge;
- patient and encounter context supplied by the clinical launcher must be bound to the authenticated organisation/user context;
- any mismatch between launch context, connector response and truth envelope fails closed.

Future national identity integration should align with the German TI identity direction rather than invent a competing national identity mechanism.

## 7. Canonical clinical fact contract

Every surfaced fact must carry enough information to reconstruct what CareOS believed and why.

Minimum fields:

- `fact_id`;
- `patient_ref`;
- `encounter_ref` where applicable;
- `fact_type`;
- `value_original`;
- `value_normalized` where governed;
- `code` + `code_system` where governed;
- `unit_original` + normalized unit where governed;
- `effective_time` where explicitly known;
- `recorded_time` / ingestion time separately;
- `source_type`;
- `source_id`;
- `source_version` where available;
- `source_span` for document-derived facts;
- `extractor` / model / transformer version;
- extraction confidence;
- assertion maturity (for example preliminary/final/corrected where applicable);
- trust status (`confirmed / ambiguous / unknown / rejected`);
- contradiction/review group;
- supersession lineage where applicable.

Original source wording is never overwritten by normalization.

## 8. Model / AI trust boundary

Model-assisted extraction is permitted only behind an admission firewall:

```text
source text
   ↓
untrusted model candidate
   ↓
exact evidence quote
   ↓
CareOS independently locates/verifies evidence
   ↓
schema + terminology + temporal checks
   ↓
ClinicalFact candidate
   ↓
reconciliation / review
```

Models may not:

- invent source offsets;
- invent clinical effective dates;
- silently resolve contradictory sources;
- create unsupported diagnoses/medications/allergies;
- directly write to the clinician-facing truth store;
- use confidence alone to determine which conflicting fact wins.

## 9. Temporal and lifecycle semantics

Clinical systems contain multiple notions of time. CareOS separates at least:

- clinical effective time;
- specimen/collection time;
- order time;
- result time;
- document authoring time;
- source update/version time;
- ingestion time.

Lifecycle states such as `ordered`, `collected`, `pending`, `preliminary`, `final`, `corrected`, `cancelled`, `active`, `stopped` or `historical` must remain explicit where the source supports them.

A later unreadable high-risk source may create a **review barrier** preventing older state from appearing current.

## 10. Terminology architecture

CareOS distinguishes:

- structural/profile validation;
- code-system validity;
- value-set membership;
- local-code mapping;
- display translation.

Passing ISiK profile validation is not treated as proof that every terminology code is semantically valid.

Terminology services should support governed mappings for relevant systems such as ICD-10-GM, SNOMED CT, LOINC, UCUM, ATC/OPS where applicable and legally/licensing-wise available.

Uncertain mappings remain reviewable and preserve the original source representation.

## 11. Security architecture

### Authentication

- hospital/provider IdP via OIDC or approved equivalent;
- asymmetric token verification;
- issuer, audience, signature, expiry and key-rotation validation;
- no implicit trust based on internal network location.

### Authorization

Access decision includes:

- user identity;
- organisation;
- role/scopes;
- patient context;
- encounter/treatment context where applicable;
- requested operation;
- break-glass reason/elevation where applicable.

A valid login is not sufficient to access patient data.

### Audit

Audit must support:

- actor;
- organisation;
- patient pseudonymous reference or approved identifier strategy;
- categories of data accessed;
- action;
- timestamp;
- source/origin where relevant;
- break-glass context;
- integrity protection;
- central provider-controlled retention/monitoring in production.

Routine telemetry must not contain clinical free text.

### Keys/secrets

Production deployment requires managed keys/secrets, rotation, least privilege, separation of duties and provider-approved operational controls.

## 12. Reliability and degraded operation

CareOS treats external dependencies as fallible.

Required failure modes include:

- KIS/LIS/FHIR timeout;
- partial Bundle/page failure;
- stale source;
- duplicated event;
- corrected/deleted source resource;
- IdP outage;
- audit sink outage;
- terminology service outage;
- model provider outage;
- network partition;
- deployment rollback.

Key invariant:

> **Source unavailable is never rendered as “no relevant result.”**

Clinical truth is withheld when required identity, authorization, source-state or audit guarantees fail.

## 13. Three supported deployment patterns

CareOS defines three target patterns; details are in `DEPLOYMENT_PATTERNS.md`.

1. **Provider on-prem/private infrastructure** — strongest local control, highest provider operations burden.
2. **Dedicated provider cloud tenant** — isolated data plane, managed platform controls, subject to German healthcare cloud requirements.
3. **Federated managed service** — central control plane plus provider-isolated data planes; intended long-term scale pattern.

No pattern changes the clinical truth, identity, audit or fail-closed contracts.

## 14. Germany interoperability alignment

The reference architecture is intentionally aligned with the direction of German national infrastructure rather than replacing it.

As of the baseline date:

- gematik describes ISiK as the standardized hospital interface and is establishing binding implementation of ISiK Stage 5;
- TI 2.0 is moving toward Zero Trust Access (ZETA), mTLS-based access and digital identity models;
- Proof of Patient Presence (PoPP) provides a cryptographically secured treatment-context signal for TI 2.0 use cases;
- ISiP defines corresponding standardized interoperability for care/nursing systems;
- §393 SGB V imposes healthcare cloud requirements including current C5 evidence and customer-side controls where applicable.

CareOS should consume these rails where appropriate instead of creating private equivalents.

## 15. EHDS-forward design

Regulation (EU) 2025/327 establishes mandatory European interoperability and logging components for EHR systems in scope and requires technical documentation, verification evidence and lifecycle change documentation.

CareOS does not assume its final legal classification under EHDS. Instead, the architecture is designed so that if CareOS or a deployable component falls within EHR-system scope, the required interoperability/logging and technical-documentation evidence can be mapped without redesigning the whole platform.

See `TECHNICAL_DOCUMENTATION_INDEX.md`.

## 16. Specialty/country/language/audience composition

```text
CareOS Core
   + Specialty Pack
   + Country Pack
   + Language Presentation
   + Audience Policy/View
```

Clinical truth is not translated or rewritten per specialty. Specialty packs determine attention/workflow; country packs determine national interoperability, terminology, identity and governance; language controls presentation; audience controls minimum necessary access.

## 17. Governance and change control

Changes to any of these require explicit impact review:

- intended purpose;
- patient identity semantics;
- clinical fact contract;
- terminology mapping logic;
- source reconciliation;
- authentication/authorization;
- write capabilities;
- model admission rules;
- retention/audit behavior;
- country/regulatory assumptions.

Architecture decisions are recorded in `docs/adr/`.

## 18. Scale criterion

CareOS is only a platform if Hospital B can deploy without a core fork.

Allowed variation:

- connector implementation/configuration;
- terminology mapping;
- organisation policy;
- local SOP/guideline overlay;
- specialty pack configuration;
- deployment pattern.

Not allowed as the default scaling strategy:

- hospital-specific branches of the CareOS core;
- specialty-specific truth stores;
- different security semantics per customer;
- hidden vendor-specific logic in the UI.

## 19. Proposal vs production status

This document can be used as a **reference architecture proposal** now.

It must not be interpreted as evidence that:

- CareOS is certified;
- CareOS is approved for live patient care;
- all G0–G9 gates are PASS;
- an SJK or other hospital deployment exists;
- MDR/AI Act/EHDS applicability has been finally determined;
- Datenschutz approval has been granted;
- a production C5-compliant environment has been independently verified.

Production eligibility remains controlled by `docs/GATES.md` and the code-enforced live-data lock.

## 20. Normative/current baseline sources

Official sources checked on 2026-08-16:

- gematik ISiK: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik
- gematik ISiK/ISiP confirmation: https://fachportal.gematik.de/shop/bestaetigungsverfahren-isik-isip
- gematik TI 2.0: https://www.gematik.de/telematikinfrastruktur/ti-2-0
- gematik TI access / Zero Trust + mTLS direction: https://fachportal.gematik.de/telematikinfrastruktur/ti-zugang
- gematik PoPP: https://fachportal.gematik.de/telematikinfrastruktur/komponenten-dienste/popp
- gematik ISiP: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isip
- §393 SGB V: https://www.gesetze-im-internet.de/sgb_5/__393.html
- BSI C5:2020: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/c5_node.html
- EHDS Regulation (EU) 2025/327: https://eur-lex.europa.eu/eli/reg/2025/327/oj/

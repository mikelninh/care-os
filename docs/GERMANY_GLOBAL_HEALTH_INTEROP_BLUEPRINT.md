# Germany as a Global Health Interoperability Reference Model

Baseline: 18 August 2026

> **Mission:** turn Germany's fragmented, bureaucracy-heavy health IT environment into a proving ground for a health-data architecture that is safer, more portable and easier to integrate than today's status quo — without replacing systems that already work.

> **North-star outcome:** clinicians spend less time hunting, re-entering and reconciling information, while patients can safely carry a trustworthy minimum clinical context across providers, regions and borders.

This document is a strategy/reference architecture, not a claim of deployment, regulatory approval or national endorsement.

---

# 1. The central idea

Germany does **not** need another EHR, another national database or another proprietary integration bus.

Germany already has / is building:

- ePA as a national patient-access and longitudinal-data layer;
- Telematikinfrastruktur (TI) for national health infrastructure;
- ISiK/FHIR for binding hospital interoperability interfaces;
- national terminology / identity / trust services;
- EHDS obligations and European exchange infrastructure ahead;
- existing local KIS/LIS/RIS/PACS/PVS systems that remain authoritative in their domains.

The missing layer is **usable trusted context**:

```text
existing systems of record
        ↓
standardised + vendor adapters
        ↓
source / identity / time / status / provenance normalisation
        ↓
reconciliation and contradiction handling
        ↓
policy + treatment-context enforcement
        ↓
clinician workflow / patient view / bounded agents
        ↓
portable EU/global summary when needed
```

CareOS should remain this layer — not become the system beneath it.

---

# 2. What the strongest countries teach us

There is no single country to copy. Each solved a different layer well.

## Estonia — auditability + once-only + national longitudinal access

Useful reference patterns:

- a national health information system shared across providers;
- citizen-visible access logs (who viewed my data and when);
- digital identity and strong authentication;
- once-only principle: do not repeatedly ask for information the state already has;
- redesign documentation around workflows rather than digitising paper;
- central citizen access without forcing all provider systems to be identical.

**Copy the principle:** every clinically consequential access and transformation should be inspectable; duplicate data collection is a system failure.

**Do not copy blindly:** Germany's scale, federal structure and installed vendor landscape make a single Estonia-style implementation unrealistic.

Official references:
- https://www.tehik.ee/en/health-information-system
- https://www.tehik.ee/en/health-portal
- https://www.tehik.ee/en/uptis

## Finland — certification + joint testing + national repository

Useful reference patterns:

- systems connecting to Kanta must satisfy functional, interoperability and security requirements;
- joint testing with the national service;
- independent information-security assessment;
- formal production deployment tests;
- national data structures + gradually increasing FHIR use;
- public compliance visibility.

**Copy the principle:** interoperability is not a PDF specification; it is something vendors must prove continuously in executable test environments.

Official references:
- https://www.kanta.fi/en/system-developers/certification-and-key-requirements
- https://www.kanta.fi/en/system-developers/development-and-maintenance-of-a-kanta-compatible-information-system
- https://www.kanta.fi/en/system-developers/fhir-technology-and-kanta

## Denmark — national services embedded inside local clinical software

Useful reference patterns:

- national service platform;
- Shared Medication Record (FMK) used across hospitals, primary care, municipalities and pharmacies;
- data remains available directly through local clinical systems rather than forcing clinicians into a separate national UI;
- shared identity/access services and trust agreements;
- explicit national governance with regions, municipalities and clinical sectors.

**Copy the principle:** national interoperability should become invisible infrastructure inside the workflow.

Official references:
- https://english.sundhedsdatastyrelsen.dk/digital-health-solutions/examples-of-digital-health-solutions
- https://sundhedsdatastyrelsen.dk/digitale-loesninger/faelles-medicinkort/baggrund-og-organisering/baggrund-for-fmk
- https://sundhedsdatastyrelsen.dk/digitale-loesninger/seb/seb-borger-og-seb-sundhed

## Netherlands — trust framework + patient-controlled ecosystem

Useful reference patterns:

- MedMij separates provider-domain systems from citizen personal-health environments;
- certification/label creates a trusted ecosystem rather than requiring pairwise contracts between every participant;
- information standards are based heavily on existing standards including HL7 FHIR;
- user choice over personal-health environment.

**Copy the principle:** interoperability requires technical standards **plus a trust/participation contract**.

Official references:
- https://medmij.nl/en/medmij-framework/
- https://medmij.nl/en/information-standards/

## England / NHS — the last mile: AI documentation + national assurance

Useful reference patterns:

- ambient AI is treated as a workflow intervention, not merely a model;
- national implementation guidance for boards/CIOs/CCIOs;
- national supplier registry to accelerate local assurance;
- local organisations retain procurement and deployment accountability;
- output remains draft material for professional review/validation.

**Copy the principle:** AI scales when government standardises the assurance evidence, while hospitals retain responsibility for local deployment.

Official references:
- https://digital.nhs.uk/services/ambient-scribing
- https://digital.nhs.uk/services/ambient-scribing/ambient-voice-technology-self-certified-supplier-registry

---

# 3. Germany already has more of the foundation than the stereotype suggests

As of August 2026:

- ePA is mandatory in medical facilities since October 2025 and is intended to become increasingly structured;
- ISiK defines binding FHIR/REST interoperability interfaces for relevant hospital systems, with ISiK stage 5 becoming binding and stage 6 under development;
- gematik provides test/confirmation tooling for ISiK-conformant products;
- Germany is preparing for EHDS interoperability and logging requirements;
- the July 2026 GeDIG proposal pushes ePA toward fuller search, structured content and AI-supported patient-facing use cases.

Germany's problem is less **absence of standards** than **fragmented implementation + poor workflow composition + vendor heterogeneity + weak end-to-end usability**.

Official references:
- https://fachportal.gematik.de/anwendungen/epa-fuer-alle
- https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik
- https://www.ina.gematik.de/themenbereiche/informationstechniche-systeme-im-krankenhaus
- https://www.bundesgesundheitsministerium.de/themen/digitalisierung/elektronische-patientenakte/epa-fuer-alle
- https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen/kabinett-beschliesst-gedig-pm-15-07-2026

---

# 4. The German reference model: six national capabilities

## Capability A — Provider-local systems remain authoritative

KIS, LIS, RIS/PACS, PVS, ePA and specialist systems keep their existing domain responsibility.

National rule:

> No new programme may require a hospital to replace an otherwise compliant system merely to participate in the trusted context layer.

## Capability B — A mandatory Open Clinical Context Contract

Every participating source or connector exposes a stable contract containing:

```text
patient + encounter binding
source organisation / system / resource
clinical effective time
recorded / ingestion time
status (final / preliminary / pending / cancelled / corrected)
freshness / version
terminology coding + original value
provenance / evidence pointer
restriction / consent state
availability / outage state
supersession relationship
```

FHIR/ISiK should carry the contract wherever possible. Vendor-specific adapters map into it rather than inventing new semantics.

This is the most important CareOS extension to national interoperability: **interoperable fields are not enough; state, time and provenance are part of clinical correctness.**

## Capability C — National executable conformance lab

Germany should evolve ISiK-style testing into a broader automated environment inspired by Finland and EHDS:

- synthetic patient packs;
- hospital workflows rather than resource-only tests;
- adversarial/wrong-patient cases;
- status lifecycle tests (preliminary → final → corrected → cancelled);
- source-outage and partial-read cases;
- terminology/value-set tests;
- access/logging tests;
- latency/SLO tests;
- agent/tool-policy tests for AI-capable systems;
- public versioned conformance reports.

Goal: **a vendor should be able to prove interoperability before entering a hospital.**

## Capability D — Patient/clinician transparency ledger

Borrow Estonia's transparency principle:

Patients should be able to inspect:

- which organisation/person/system accessed their record;
- purpose/treatment context where legally appropriate;
- which agent or automated workflow participated;
- which source facts were used to generate a draft or summary;
- whether any data left the provider boundary;
- corrections / revocations / exceptional access.

This does not mean publishing sensitive internal security detail. It means making consequential access understandable and contestable.

## Capability E — National AI assurance contract

Germany should not approve "AI" as a monolithic category.

For any agentic clinical workflow, require a machine-readable **Agent Capability Manifest**:

```text
agent identity + version
intended task
allowed tools
allowed operations
allowed data categories
patient / encounter binding
record/page/runtime budgets
model/provider + retention policy
human approval requirements
write / send capability
logging + evaluation hooks
kill switch / revocation
```

National principle:

> A model may propose; deterministic policy owns authority.

Hospitals should be able to test the same agent against a national red-team suite before local deployment.

## Capability F — Outcome contract: Time Returned to Care

Digital-health procurement should stop rewarding deployment alone.

Every workflow should report a small standard outcome set:

- median task time;
- searches/window switches/calls where measurable;
- clinician correction burden;
- missed pending items;
- unsupported/incorrect claims;
- source-verification behaviour;
- patient-safety incidents/near misses;
- user adoption and abandon rate;
- system availability/degraded-mode behaviour.

For AI workflows:

> time saved **cannot compensate for a safety-stop event**.

This turns "digitalisation" into measurable care capacity.

---

# 5. Three-ring interoperability model

```text
┌───────────────────────────────────────────────────────────┐
│ RING 3 — GLOBAL PORTABILITY                               │
│ HL7 FHIR · IPS · WHO SMART/GDHCN trust · ICD/LOINC/etc.   │
│ signed summary · terminology mapping · translation layer  │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ RING 2 — EU / NATIONAL                              │  │
│  │ EHDS / EEHRxF · MyHealth@EU · ePA · TI · ISiK      │  │
│  │ national identity · consent · logging · terminology │  │
│  │                                                     │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │ RING 1 — PROVIDER / HOSPITAL                 │  │  │
│  │  │ KIS · LIS · RIS/PACS · docs · local truth    │  │  │
│  │  │ reconciliation · policy · clinician workflow │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

The core rule is **progressive disclosure**:

- inside the hospital, use rich provider context;
- across Germany/EU, exchange the harmonised subset appropriate to purpose;
- globally, exchange a minimal verified clinical summary rather than raw internal records.

---

# 6. Global interoperability: Berlin → Copenhagen → Hanoi

Global interoperability does **not** mean every country adopts Germany's software.

It means the exported clinical meaning is portable enough to be understood and trusted elsewhere.

## Portable core

CareOS should target a validated International Patient Summary (IPS) export containing at minimum the clinically relevant IPS sections, with original-source lineage retained locally.

Global wire principles:

- HL7 FHIR as the primary modern API/data representation where supported;
- International Patient Summary as the minimum cross-border continuity-of-care document;
- internationally recognised terminologies where licencing/availability permits (e.g. SNOMED CT, LOINC, UCUM, ICD family, ATC where appropriate);
- original values/text retained alongside mapped codes;
- human-readable presentation available even when receiving system cannot process every structured element;
- explicit language and translation metadata;
- digital signatures / provenance where the issuing ecosystem supports them.

## Trust layer

WHO's Global Digital Health Certification Network is a relevant long-term trust anchor model. It is designed as a global interoperable trust network based on public keys and open standards; WHO itself does not hold individual health data. WHO documentation identifies FHIR and IPS as important building blocks for future continuity-of-care use cases.

CareOS should therefore keep **content interoperability separate from trust interoperability**:

```text
CONTENT: what does this clinical fact mean?
FHIR / IPS / coding / language

TRUST: who issued it and can I verify it?
signature / organisation identity / trust network / revocation

POLICY: am I allowed to use it here?
local law / patient rights / treatment context / purpose
```

Official references:
- https://www.hl7.org/fhir/uv/ips/en/index.html
- https://www.who.int/initiatives/global-digital-health-certification-network
- https://smart.who.int/trust/overview.html

## Translation must never mutate clinical truth

A global view may translate **presentation**, not silently rewrite the source.

Store/preserve:

```text
original clinical text
original code/system
mapped international code (if governed)
presentation language
translation method/version
translation confidence/review status
```

High-risk content always retains direct access to the original.

## Country packs, not product forks

One CareOS core; country-specific policy/interop packs:

```text
core truth envelope
core agent boundary
core audit/eval model
        ↓
Germany pack: ISiK/ePA/TI/EHDS-DE/ICD-10-GM/OPS
Denmark pack: national services + local standards
Finland pack: Kanta + national data structures
Vietnam pack: local identifiers/standards/law/connectors
WHO/global pack: IPS + trust/credential verification
```

The core must never contain German assumptions that prevent another country from adopting it.

---

# 7. What CareOS already does unusually well

These are **design strengths**, not claims of being superior to national production systems.

## 7.1 It treats provenance as correctness

Many exchange programmes focus first on whether a field can move from A to B. CareOS additionally requires consequential facts to preserve source identity/evidence and lineage.

## 7.2 It refuses to collapse clinically different states

CareOS explicitly distinguishes:

- pending vs negative;
- unavailable vs absent;
- stale vs current;
- preliminary vs final;
- corrected/superseded vs active;
- contradictory vs resolved.

This is crucial for AI because a fluent model can otherwise erase these distinctions.

## 7.3 It treats the model as untrusted infrastructure

The CareOS agent architecture separates:

- model proposals;
- patient/encounter identity;
- tool registry;
- deterministic authorization;
- action budgets;
- data categories;
- write/send capability;
- audit;
- human approval.

A compromised reasoning worker cannot grant itself a new patient, tool or network destination.

## 7.4 It makes failure a first-class product state

Wrong patient, stale source, outage, contradiction and unauthorised tool use are designed as observable states rather than edge cases hidden behind generic errors.

## 7.5 It measures usefulness and trust together

The clinician A/B design measures time, errors, pending-work retention, source checking, correction burden and verification decay — with safety stops overriding speed wins.

## 7.6 It avoids replacing systems of record

The provider-local/federated architecture makes CareOS composable with existing infrastructure rather than requiring a giant migration before value appears.

---

# 8. What we should add before claiming global readiness

## Engineering

1. Validate actual IPS conformance against the current published IG.
2. Add terminology mapping provenance and versioning.
3. Add explicit translation provenance to the TruthEnvelope.
4. Add digital-signature / verifiable issuer envelope for portable summaries.
5. Implement country-pack plugin contract and at least one non-German synthetic reference pack.
6. Add cross-country synthetic interoperability fixtures.
7. Add round-trip tests: German source → IPS → receiving-country view → no semantic loss of safety-critical state.
8. Add offline/emergency degraded rendering for minimal summaries.
9. Add international patient-identity handling that never assumes German identifiers.
10. Map EHDS/EEHRxF outputs once implementing acts/specifications stabilise.

## Governance

1. Define the German Open Clinical Context Contract with gematik/provider/vendor stakeholders rather than privately declaring it a standard.
2. Publish conformance fixtures/open-source reference validators.
3. Create an independent clinical-safety + interoperability review group.
4. Establish procurement requirements that prevent vendor lock-in and require export/logging.
5. Define national agent assurance evidence with BSI/gematik/BfArM/medical-software experts as applicable.
6. Engage HL7 Germany / HL7 Europe / IHE / WHO communities for standards alignment.

---

# 9. Implementation roadmap: Germany from laggard stereotype to reference model

## Phase 0 — Now: prove the last mile

**Scope:** one hospital workflow, synthetic first.

- CareOS + Recare capstone;
- real clinician workflow observation;
- paired synthetic usability evidence;
- deidentified KIS/LIS sandbox next;
- read-only, no autonomous clinical action.

Success: evidence that trusted context reduces work without weakening verification.

## Phase 1 — Two hospitals / two vendor stacks

- one common CareOS core;
- different KIS/LIS vendors;
- no core fork;
- publish connector + failure contract;
- demonstrate repeatability.

Success: second-site deployment cost/time materially lower than first.

## Phase 2 — German interoperability reference sandbox

With industry/government partners:

- reusable synthetic cases;
- ISiK/ePA-compatible fixtures;
- lifecycle/contradiction/outage cases;
- agent red-team suite;
- open conformance reports.

Success: vendors can test before entering a hospital.

## Phase 3 — National "Time Returned to Care" programme

Government/payers fund workflows based on measured burden reduction + safety evidence.

Priority workflows:

- discharge documentation;
- medication reconciliation;
- infection/microbiology handover;
- referral / prior-history preparation;
- repeated administrative form completion;
- cross-sector transition hospital → rehab/care/home.

Success: quantified clinician hours returned to patient-facing work.

## Phase 4 — EHDS-ready German reference implementation

- EEHRxF interoperability/logging component mapping;
- Patient Summary/ePrescription path first;
- imaging/lab/discharge-report path next;
- automated EHDS testing-environment compatibility.

Success: Germany ships an open reference implementation others can inspect/reuse.

## Phase 5 — Cross-border EU pilot

Germany ↔ one Nordic country / Netherlands:

- IPS/EEHRxF summary;
- issuer verification;
- terminology/language mapping;
- original-source preservation;
- emergency/degraded mode;
- patient access log.

Success: a foreign clinician can understand essential context without calling/faxing the German provider.

## Phase 6 — Germany ↔ Vietnam demonstrator

Use a deliberately different environment to prove the architecture is not secretly Germany-only.

Example synthetic use case:

> German-resident Vietnamese patient travels to Hanoi and needs unplanned hospital care.

Portable bundle:

- allergies/intolerances;
- active medications;
- major problems;
- recent procedures;
- critical recent results;
- pregnancy/status when relevant;
- emergency contacts / directives where legally exchangeable;
- issuer/provenance/signature;
- German original + Vietnamese/English presentation.

Success: receiving clinician gets useful, verifiable minimum context even without German TI access.

## Phase 7 — Open international reference

Publish:

- open context contract;
- country-pack contract;
- IPS portability validator;
- agent capability manifest;
- red-team suite;
- outcome measurement protocol;
- governance templates;
- synthetic test corpus.

Goal: **Germany exports an interoperability playbook, not another proprietary health platform.**

---

# 10. Proposed German "Health Interop Compact"

A simple national commitment any public procurement could require:

1. **No information without provenance.**
2. **No status collapse:** pending/unavailable/stale/contradictory stay explicit.
3. **No proprietary prison:** authorised export/import through open standards.
4. **No second login/window when integration can be embedded.**
5. **No agent gets implicit authority.**
6. **No consequential AI output without observable evidence and policy.**
7. **No deployment called successful without measured clinician/patient benefit.**
8. **No national format where an accepted international/EU standard suffices.**
9. **No translation may silently replace original clinical meaning.**
10. **No cross-border portability without verifiable issuer/provenance.**

---

# 11. What success looks like

Germany becomes an international reference when a clinician can say:

> "I open the patient once. Relevant information from local systems and authorised national sources is already reconciled, sourced and current. I can see what is pending or contradictory. AI can prepare work but cannot silently change truth or authority. The patient can see access. If they travel, a verified minimum summary goes with them."

And when the government can prove:

- fewer duplicate tests;
- fewer repeated questions/data entry;
- less clinician documentation/search time;
- lower integration cost per hospital/vendor;
- faster onboarding of compliant digital-health products;
- fewer wrong-patient / stale-data / unsupported-agent failures;
- lower vendor switching cost;
- measurable cross-border continuity of care.

That is the goal: **bureaucracy transformed into explicit, testable, interoperable rules — and then made invisible to the clinician and patient.**

# CareOS Pre-Hospital Handoff

Baseline: **18 August 2026**

> **Status:** the synthetic / pre-hospital phase is complete enough for serious external review. The next high-value evidence primarily requires clinicians, hospital systems, production teams or external assurance.

This is the canonical handoff for the work completed before approaching a hospital, implementation partner or healthcare-AI team.

## Mission

Return time to care **without making clinical information less trustworthy**.

CareOS explores a clinician-first layer above existing systems of record. It does not replace the KIS/EHR, LIS, RIS/PACS, PVS, ePA or national infrastructure. The research question is whether fragmented sources can become useful clinical context while preserving identity, provenance, time, lifecycle state, uncertainty, contradiction and human authority.

## What has been built

### Clinician workflow

- synthetic Infectiology workflow for review, microbiology, documented medication context, hygiene/isolation, pending work and handover;
- source-linked facts and evidence inspection;
- explicit `pending != negative`, `unavailable != absent`, `documented therapy != AI recommendation`, `agent draft != source truth` semantics;
- review/approval boundaries;
- paired synthetic clinician A/B study with local-only anonymous export.

### Clinical truth / evidence

- typed source-linked clinical truth envelopes;
- patient/encounter binding;
- effective time vs ingestion/recorded time;
- preliminary/final/corrected/cancelled/stale/unavailable states;
- contradiction and supersession handling;
- conservative document extraction with exact evidence verification;
- frozen synthetic holdout with 100% precision/provenance coverage and 26.32% recall, deliberately leaving G1 blocked because recall/review burden is not acceptable for production.

### Interoperability

- FHIR transport and bounded pagination;
- ISiK-oriented validation path;
- connector boundary for KIS/LIS/RIS/PACS/ePA/vendor interfaces;
- Germany/EU integration map;
- IPS-shaped portability work;
- global portability envelope preserving source wording, clinical state, translation provenance and issuer trust separately;
- synthetic cross-border regression path.

### Agentic AI

- untrusted reasoning-worker abstraction;
- deterministic synthetic worker for reproducible CI;
- provider-neutral HTTPS model adapter for synthetic/deidentified evaluation;
- optional direct OpenAI Responses API worker for synthetic evaluation;
- schema-constrained proposals/drafts;
- deterministic Agent Gateway;
- patient/encounter/task-bound delegation;
- versioned tool registry;
- record/page/tool/runtime budgets;
- deny-default egress;
- trusted Tool Proxy;
- draft firewall;
- no autonomous treatment recommendation in the first capstone use case;
- live-agent and consequential modes locked behind release gates.

### Adversarial evaluation

- wrong-patient resources;
- prompt injection / hostile documents;
- unavailable sources;
- stale data;
- unauthorised write/tool escalation;
- cross-patient/scope escalation;
- partial/failing source behavior;
- platform and hostile-agent red-team workflows;
- supply-chain/container hardening foundations.

### Recare-targeted capstone

The Recare work sample composes the actual CareOS gateway, tool proxy, model-worker boundary and evaluation components into one synthetic discharge-prep workflow.

See:

- [Recare Capstone](RECARE_CAPSTONE.md)
- [Recare Collaboration Map](RECARE_COLLABORATION_MAP.md)
- public work sample: `https://mikelninh.github.io/recare/`

### Hospital implementation

The rollout playbook is:

`workflow archaeology → technical preflight → read-only → shadow → one ward → copilot → bounded execution → measured scale`

See [Hospital Implementation Playbook](HOSPITAL_IMPLEMENTATION_PLAYBOOK.md).

### Germany / global reference model

The national thesis is not another German EHR. It is standards-based composition, executable trust/safety contracts and measurable workflow outcomes above existing infrastructure.

See:

- [German Government Reference Architecture](GOVERNMENT_REFERENCE_ARCHITECTURE.md)
- [National / EU Integration Map](NATIONAL_INTEGRATION_MAP.md)
- [Germany → Global Health Interoperability Blueprint](GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)

## Evidence-state handoff

| Question | Current evidence state |
|---|---|
| Concrete clinician workflow? | **DEMONSTRATED SYNTHETICALLY** |
| Source/provenance/state contracts? | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| Agent containment? | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| Recare work sample runnable? | **YES — SYNTHETIC** |
| Provider-backed model path implemented? | **YES — CAPTURE STILL REQUIRES A REAL CREDENTIAL/RUN** |
| German interoperability proven against a real KIS/LIS? | **NO — EXTERNAL EVIDENCE REQUIRED** |
| Real clinician outcome data? | **NO — STUDY READY, SESSIONS REQUIRED** |
| Production PHI operations? | **NO — BLOCKED BY DESIGN** |
| Production security/regulatory approval? | **NO — EXTERNAL REVIEW/OPERATIONS REQUIRED** |
| Multi-hospital repeatability? | **NOT YET EVIDENCED** |

See [Current Status and Gaps](CURRENT_STATUS_AND_GAPS.md).

## What we should not build next from the outside

Do not create speculative substitutes for infrastructure only real deployments can reveal:

- another fake KIS connector;
- another synthetic specialty for breadth;
- fake PHI operations;
- fake production security attestations;
- fake clinical validation;
- fake multi-hospital scale;
- proprietary replacements for ePA, TI, ISiK, EHDS or IPS.

More feature breadth now produces less signal than one hour observing a real hospital workflow.

## Next evidence ladder

```text
external engineering critique
        ↓
clinicians complete synthetic paired study
        ↓
real workflow observation
        ↓
hospital / vendor technical discovery
        ↓
synthetic or deidentified integration sandbox
        ↓
clinical + privacy + security + regulatory review
        ↓
shadow study
        ↓
limited read-only pilot only when gates permit
        ↓
second ward / hospital / vendor
```

## Collaboration posture

CareOS is **not** an insistence that an external team adopt this product or architecture wholesale.

1. identify what the partner already solves better;
2. delete duplicate assumptions;
3. transfer useful invariants, tests and evaluation methods;
4. find one real unresolved workflow;
5. own it end to end through implementation;
6. let production reality decide what survives.

> **The next version is not a bigger version number. The next version is reality.**

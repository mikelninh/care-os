# CareOS Pre-Hospital Handoff

Baseline: **18 August 2026**

> **Status:** the synthetic / pre-hospital phase is complete enough for serious external review. The next high-value evidence requires real clinicians, real hospital systems and real implementation constraints.

This document is the canonical entry point for the work completed before approaching a hospital, implementation partner or healthcare-AI team.

## The mission

Return time to care **without making clinical information less trustworthy**.

CareOS explores a clinician-first layer above existing systems of record. It does not attempt to replace the KIS/EHR, LIS, RIS/PACS, PVS, ePA or national infrastructure. The core research question is whether fragmented sources can be composed into useful clinical context while preserving patient/encounter identity, provenance, time, clinical state, uncertainty, contradiction and human authority.

## What has been built

### Product / clinician workflow

- synthetic Infectiology workflow for morning review, microbiology, medication context, hygiene/isolation, pending work and handover;
- source-linked facts and evidence drawers;
- explicit `pending != negative`, `unavailable != absent`, `documented therapy != AI recommendation` semantics;
- clinician review/approval states;
- paired synthetic clinician A/B study with local-only anonymous export.

### Clinical truth / evidence

- typed source-linked clinical truth envelopes;
- identity and encounter binding;
- effective time vs ingestion/recorded time;
- freshness, preliminary/final/corrected/cancelled/stale/unavailable states;
- contradiction and supersession handling;
- conservative document extraction with exact evidence verification;
- frozen 500-case synthetic holdout with 100% precision/provenance coverage and 26.32% recall, deliberately leaving G1 blocked because recall/review burden is not acceptable for production.

### Interoperability

- FHIR transport and bounded pagination;
- ISiK-oriented structural/profile validation;
- connector boundary for KIS/LIS/RIS/PACS/ePA/vendor interfaces;
- Germany / EU integration map;
- IPS-shaped portability work;
- country-neutral global portability envelope preserving source wording, clinical state, translation provenance and issuer trust separately;
- Berlin -> foreign-care synthetic regression path.

### Agentic AI

- untrusted reasoning worker abstraction;
- provider-neutral HTTPS model adapter for synthetic/deidentified evaluation;
- schema-constrained tool proposals and drafts;
- deterministic Agent Gateway;
- patient/encounter/task-bound delegation;
- versioned tool registry;
- record/page/tool/runtime budgets;
- deny-default egress;
- trusted Tool Proxy;
- draft firewall;
- no autonomous treatment recommendation in the first use case;
- live-agent modes and consequential actions locked behind separate release gates.

### Adversarial evaluation

- wrong-patient resources;
- prompt injection / hostile documents;
- unavailable sources;
- stale data;
- unauthorised write/tool escalation;
- cross-patient and scope escalation;
- partial/failing source behavior;
- platform and hostile-agent red-team workflows;
- supply-chain and container hardening foundations.

### Recare-targeted capstone

The dedicated Recare work sample composes the real CareOS Agent Gateway, Tool Proxy, model adapter and evaluation components into one synthetic discharge-prep workflow.

See:

- [Recare Capstone](RECARE_CAPSTONE.md)
- [Recare Collaboration Map](RECARE_COLLABORATION_MAP.md)
- public work sample: `https://mikelninh.github.io/recare/`

### Hospital implementation

A separate rollout playbook converts the architecture into a low-friction path:

`workflow archaeology -> technical preflight -> read-only -> shadow -> one ward -> copilot -> bounded execution -> scale`

See [Hospital Implementation Playbook](HOSPITAL_IMPLEMENTATION_PLAYBOOK.md).

### Government / global reference model

The national thesis is not to build another German EHR. It is to make existing systems interoperable and clinically usable through executable contracts, strong assurance and measurable outcomes.

See:

- [German Government Reference Architecture](GOVERNMENT_REFERENCE_ARCHITECTURE.md)
- [National / EU Integration Map](NATIONAL_INTEGRATION_MAP.md)
- [Germany as a Global Health Interoperability Reference Model](GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md)

## What we should **not** build next from the outside

Do not create speculative substitutes for infrastructure that only real deployments can reveal:

- another fake KIS connector;
- another synthetic specialty just for breadth;
- fake PHI operations;
- fake production security attestations;
- fake clinical validation;
- fake multi-hospital scale;
- proprietary replacements for ePA, TI, ISiK, EHDS or IPS.

More synthetic features now produce less signal than one hour observing a real hospital workflow.

## Current readiness

Two ratings are intentionally separated:

| Question | Current status |
|---|---:|
| Ready for serious engineering / hospital architecture review? | **9.5 / 10** |
| Ready as a targeted AI/ML engineering work sample? | **9.6 / 10** |
| Ready to begin a synthetic/deidentified integration discussion? | **9 / 10** |
| Ready for a live hospital production deployment? | **~4 / 10** |
| Clinically validated? | **No** |
| Approved for identifiable live PHI? | **No** |

The production score is deliberately low because the remaining evidence cannot be generated responsibly without provider access.

See [Current Status and Gaps](CURRENT_STATUS_AND_GAPS.md).

## The next evidence ladder

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
second ward / second hospital / second vendor
```

## Collaboration posture

CareOS is **not** an insistence that an external team adopt this product or architecture wholesale.

The correct collaboration posture is:

1. identify what the partner already solves better;
2. delete duplicate assumptions;
3. transfer useful invariants, tests and evaluation methods;
4. find one real unresolved workflow;
5. own it end-to-end through implementation;
6. let production reality decide what survives.

> **The next version is not V15. The next version is reality.**

# CareOS Master Foundation — Implementation Status

Baseline: **18 August 2026**

This document separates **what is implemented now** from **what still requires real users, hospitals, vendors, operations or governance**.

## Implemented in the pre-hospital foundation

### 1. Hospital-local interoperability / self-install scaffold

- Hospital Capability Manifest;
- adapter maturity catalog;
- FHIR/ISiK-over-FHIR runnable path;
- FHIR CapabilityStatement discovery;
- deterministic preflight;
- cross-source identity gate;
- hospital-local multi-source FHIR data-plane API;
- Docker Compose + Helm deployment scaffolds;
- upgrade compatibility preflight;
- container release/SBOM/provenance path;
- direct CLI commands exercised in CI.

Not proven: real KIS/LIS/vendor self-service install or multi-hospital repeatability.

### 2. Source-linked clinical truth

- provenance/time/lifecycle/freshness/contradiction contracts;
- preliminary/final/corrected/cancelled handling;
- failure-as-state;
- conservative synthetic benchmark;
- source-linked clinical context.

Known blocker: frozen synthetic benchmark recall/review burden remains insufficient for production use.

### 3. Patient-local clinical context graph

- hard patient partition;
- source/supersession/contradiction/derived relations;
- evidence + transformer/version lineage for deterministic derivation;
- cross-patient graph rejection.

### 4. Downstream stale-artifact protection

- typed artifact dependencies;
- corrected/superseded facts reopen dependent AI drafts/derived context;
- contradiction changes reopen affected content;
- human-signed artifacts are flagged for review but never silently rewritten;
- invalidations create safety audit events.

### 5. Resilience / offline / recovery

- normal / degraded / offline / recovery capability model;
- source/network/identity/audit/model outage drills;
- absence assertions blocked when stale/offline;
- model failure does not remove source-linked context;
- only explicit idempotent non-consequential work may queue;
- recovery requires reconciliation before normal mode;
- source corrections during outage invalidate downstream artifacts before normal operation resumes.

Not proven: real hospital downtime/disaster exercise.

### 6. Time Returned to Care evidence contract

- product targets separated from outcomes;
- pseudonymous paired observation schema;
- physician/nursing/discharge workflow protocol;
- time + systems/searches/context-switches/copy-paste/contacts capture;
- errors/pending/source-verification/corrections/effort capture;
- explicit safety stops;
- minimum five complete safe pairs before a directional aggregate may be highlighted;
- reproducible JSON aggregation CLI;
- local-only public study instrument.

Not proven: actual participants/results. Issue #35 remains an evidence programme.

### 7. Patient/family foundation

- source-linked patient presentation contract;
- original wording preserved;
- pending/preliminary/unavailable remain explicit;
- medication state separated from AI recommendation;
- teach-back checks;
- explicit revocable proxy grant model;
- bounded patient-agent capabilities;
- responsive synthetic public patient experience.

Not proven: patient/family usability or live portal/ePA/provider integration.

### 8. Cross-provider care coordination

- minimum-purpose-relevant source references;
- explicit ownership;
- transport-agnostic request contract;
- acknowledged lifecycle from draft through follow-up completion;
- draft/send authority separation;
- audit for lifecycle transitions.

Not proven: real KIM/FHIR/vendor/network transport integration or organisational workflow adoption.

### 9. Agent authority / assurance

- zero-trust model-proposal boundary;
- patient/encounter/task/tool binding;
- deterministic authorization;
- bounded tool proxy;
- hostile-worker/adversarial tests;
- provider-neutral and direct-provider synthetic model path;
- no autonomous live clinical write-back.

Not proven: production PHI/model operations or hospital-approved agent workflows.

### 10. Critical-service operating model

- service criticality hierarchy;
- local fallback requirement for source/context layers;
- systemic incident classification;
- narrow kill-scope model;
- upgrade rings/canary/rollback philosophy;
- hospital relationship cadence;
- evidence gate that rejects a contracted SLA without staffing + target-environment exercise evidence;
- synthetic critical-service game-day protocol;
- reusable monthly/quarterly hospital value + safety review template.

Current contractual state: **24/7 SLA NOT OFFERED**.

### 11. Integrated Future API

`app/future_api.py` exposes one bounded synthetic API for:

- golden end-to-end journey;
- patient view + teach-back;
- standard outage/recovery drill;
- cross-provider coordination lifecycle;
- Time Returned to Care targets/report aggregation;
- service catalog/current SLA state.

This API is synthetic/pre-hospital only.

### 12. Golden end-to-end regression journey

`app/end_to_end_journey.py` composes the foundation into one synthetic patient story:

```text
source-linked preliminary clinical fact
→ patient-local graph
→ unsigned source-dependent clinician draft
→ corrected/final source result during outage
→ RECOVERY mode
→ supersession invalidates stale draft + audit
→ NORMAL only after reconciliation
→ source-linked patient/pending view
→ minimum-purpose cross-provider follow-up request
→ requested / received / accepted / scheduled / performed / result / follow-up complete
```

`tests/test_end_to_end_journey.py` and `/api/journey/golden` make this a permanent regression surface. It explicitly keeps Time Returned to Care as a **target to test** and production SLA as **not offered**.

### 13. Hospital-scale reuse foundation

The next scaling layer is now implemented as explicit contracts rather than prose:

- **trusted MPI/source-ID resolver contract** — deterministic, source-specific identifiers, freshness/namespace/resolver evidence, no fuzzy/model matching; multi-source runtime queries each source with its own ID and normalizes admitted facts back to the enterprise patient;
- **generated hospital review pack** — `careos review-pack` creates non-secret JSON/Markdown/Mermaid with sources, adapters, auth modes, owner lanes, read/write boundary, blockers and data flow; it is support evidence, not DSFA/DPIA/security approval;
- **evidence-gated rollout controller** — preflight → conformance → canary → promote/rollback; patient-identity errors, incomplete reads, unsupported claims, safety stops, operator stop or newly detected write authority block promotion/force rollback;
- **vendor/product/version compatibility registry** — evidence classes `synthetic-only`, `real-sandbox`, `real-shadow`, `production-observed`; exact/explicit version matching; compatibility evidence never auto-approves rollout;
- **narrow HL7 v2 read connector** — synthetic/deidentified ADT patient/encounter context + ORU/OBX observations, message-control deduplication, preliminary/final/corrected/cancelled state mapping and fail-visible wrong-patient/malformed behavior.

Important boundaries:

- real hospital MPI integration is **not** configured by the self-install CLI yet; `careos doctor/up` blocks `trusted-mpi` until an approved resolver adapter is injected;
- the HL7 library connector is **not yet a production/self-install MLLP or interface-engine adapter** and the adapter catalog must not advertise a green HL7 self-install path yet;
- compatibility metadata is evidence, never certification;
- the canary state machine is not proof of zero-downtime production behavior.

See `docs/HOSPITAL_SCALE_FOUNDATION.md` for the canonical scale boundary.

## Operations evidence assets

- `docs/CRITICAL_SERVICE_OPERATING_MODEL.md`
- `docs/OPERATIONS_GAME_DAY.md`
- `docs/HOSPITAL_VALUE_SAFETY_REVIEW_TEMPLATE.md`

These define the operating discipline. They do not prove a staffed 24/7 production organisation exists.

## Public surfaces

- Master ground truth: `https://mikelninh.github.io/careos/master.html`
- Future-day stakeholder simulator: `https://mikelninh.github.io/careos/future.html`
- Golden end-to-end journey: `https://mikelninh.github.io/careos/journey.html`
- Hard questions / FAQ: `https://mikelninh.github.io/careos/faq.html`
- Clinician workflow: `https://mikelninh.github.io/careos/sjk/`
- Patient/family synthetic view: `https://mikelninh.github.io/careos/patient.html`
- Time Returned to Care study instrument: `https://mikelninh.github.io/careos/study.html`
- Recare-targeted work sample: `https://mikelninh.github.io/recare/`

## What remains impossible to close honestly from outside

- real clinician/nursing/patient paired-study results;
- real hospital workflow archaeology;
- real KIS/LIS/vendor sandbox;
- real hospital MPI/EMPI and source-ID behavior;
- real HL7 interface-engine/transport compatibility;
- real IdP/role/treatment-context integration;
- hospital Datenschutz/DSFA/AVV/security approval;
- production KMS/SIEM/audit/backup/recovery evidence;
- independent penetration/security review;
- real provider-backed operating evidence at clinical scale;
- production 24/7 support organisation and contractual SLA;
- first live shadow deployment;
- second vendor + second hospital repeatability;
- real cross-provider acknowledgement transport;
- regulatory/classification determination for exact intended use;
- clinical outcome evidence.

## Engineering rule from here

> **Do not add broad speculative healthcare features merely because they are imaginable.**

Prefer:

```text
real stakeholder friction
→ one bounded workflow/problem
→ implementation
→ measurable evidence
→ regression/compatibility knowledge
→ reuse at the next site
```

The pre-hospital foundation should now be judged by how much survives contact with Recare, clinicians, hospital IT and a real hospital environment.

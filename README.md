<div align="center">

# CareOS

### **Return time to care — without making clinical information less trustworthy.**

A clinician-first **interoperability + assurance layer** that sits beside existing hospital systems, turns fragmented sources into source-linked clinical context, and makes that context usable by clinicians and bounded AI applications.

[**▶ Explore CareOS**](https://mikelninh.github.io/careos/) · [**▶ Clinician demo**](https://mikelninh.github.io/careos/sjk/) · [**▶ Recare work sample**](https://mikelninh.github.io/recare/) · [**Hospital self-install**](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) · [**Endgame**](docs/ENDGAME.md)

[![tests](https://github.com/mikelninh/care-os/actions/workflows/test.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/test.yml)
[![hospital-self-install](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/hospital-self-install.yml)
[![recare-capstone](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/recare-capstone.yml)
[![agent-redteam](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml/badge.svg)](https://github.com/mikelninh/care-os/actions/workflows/agent-redteam.yml)
[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Synthetic / pre-hospital research only · not for clinical use · no identifiable patient data in public demos · no production write-back**

</div>

---

## CareOS in 10 seconds

Hospitals already have KIS/EHR, LIS, RIS/PACS, documents, ePA and other systems of record.

**CareOS does not ask them to replace those systems.** It explores a stable layer above them:

```text
legacy KIS · LIS · RIS/PACS · documents · ePA
                        ↓
                 reusable adapters
                        ↓
            canonical clinical context
 identity · provenance · time · lifecycle · freshness
                        ↓
             deterministic policy boundary
                 ↙               ↘
          clinician UX        bounded apps/agents
                 ↘               ↙
                    human authority
```

Two questions drive the project:

> **Clinical:** Can clinicians spend less time hunting, reconciling and re-entering information without losing provenance, uncertainty or human control?

> **Infrastructure:** Can hospital #100 inherit the integration knowledge of hospitals #1–99 instead of starting another bespoke IT project?

North star: **Time Returned to Care — safety gated.**

---

## Three ways in

| If you are… | Start here |
|---|---|
| **Clinician** | [Try the synthetic Infectiology workflow →](https://mikelninh.github.io/careos/sjk/) |
| **Hospital IT / integration engineer** | [Self-install platform →](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) · [Connector SDK →](docs/CONNECTOR_SDK.md) |
| **Recare / AI engineering** | [90-second work sample →](https://mikelninh.github.io/recare/) · [Integration accelerator hypothesis →](docs/RECARE_INTEGRATION_ACCELERATOR.md) |

For the whole architecture: [Architecture V2](docs/ARCHITECTURE_V2.md) · [Current evidence/gaps](docs/CURRENT_STATUS_AND_GAPS.md) · [Endgame](docs/ENDGAME.md)

---

# Hospital IT: from repo to validated local scaffold

The long-term target is deliberately simple:

```text
careos init
careos doctor
careos preflight
careos discover-fhir
careos up
```

Today that command surface exists as a Python CLI and is restricted to **synthetic/deidentified evaluation**.

```bash
git clone https://github.com/mikelninh/care-os.git
cd care-os

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.lock

python scripts/careos.py init \
  --hospital-id DE-DEMO-001 \
  --site-name "Example Hospital"

# Fill the non-secret hospital manifest, then:
python scripts/careos.py doctor hospital.json --env-file deploy/hospital.env.example
python scripts/careos.py preflight hospital.json
python scripts/careos.py discover-fhir hospital.json --env-file deploy/hospital.env.example
python scripts/careos.py up hospital.json --env-file deploy/hospital.env.example
```

The installer does **not** make safety gates optional. If patient identity, cross-source mapping, a runnable adapter or accountable ownership is missing, preflight blocks instead of generating magical glue code.

### What the hospital describes once

`HospitalManifest` records non-secret capability facts such as:

```text
vendor / product / version
source role: KIS · LIS · RIS/PACS · documents
available interfaces
authentication mode
patient / encounter identity capability
cross-source identity strategy
resource IDs + versioning
effective time + lifecycle support
read / write capability
SSO + patient-context launch
audit + security/privacy/clinical/rollback owners
```

Real endpoints, certificates, tokens and passwords stay outside the versionable manifest in hospital-controlled secret/environment infrastructure.

[Example manifest →](deploy/hospital.example.json) · [Machine contract →](app/hospital_install.py)

---

## Adapter truth: what CareOS actually supports today

The installer distinguishes **a standard the hospital exposes** from **a CareOS adapter that actually exists**.

| Adapter path | CareOS status today |
|---|---|
| **FHIR R4 read** | **IMPLEMENTED research runtime** |
| **ISiK / FHIR read** | **FHIR runtime + ISiK validation path** |
| HL7 v2 | **CONTRACT ONLY — no generic runtime yet** |
| Vendor API | **CONTRACT ONLY** |
| Document/source feed | **CONTRACT ONLY** |
| UI / computer-use bridge | **CONTRACT ONLY** |
| Live transactional/write | **NOT RUNNABLE — blocked by release policy** |

The machine-readable source of truth is [`architecture/adapter-catalog.json`](architecture/adapter-catalog.json).

If a hospital exposes both ISiK/FHIR and generic FHIR, CareOS prefers the stronger standard path. If it exposes only an adapter family we have not implemented, **self-service stops there and tells us exactly what is missing**.

---

# The scaling model

```text
Hospital A / Vendor A / FHIR ─┐
                              ├── standard-fhir-r4 adapter
Hospital B / Vendor B / FHIR ─┘
                              ↓
                    canonical context contract
                              ↓
                    every compatible application
```

We want differences to live in **configuration, mappings and versioned conformance evidence**, not in `hospital-a.py`, `hospital-b.py`, `hospital-c.py`.

Every deployment should make the next one easier:

```text
hospital capability manifest
        ↓
reusable adapter selected
        ↓
conformance + shadow evidence
        ↓
compatibility knowledge captured
        ↓
regression test added
        ↓
next compatible hospital inherits it
```

The endgame is not one world EHR. It is an **open clinical interoperability fabric** where hospitals can change applications—or eventually source-system vendors—without rebuilding every integration from zero.

[Read the endgame →](docs/ENDGAME.md)

---

## Smooth migration, not big-bang replacement

```text
legacy stays authoritative
        ↓
read-only connection
        ↓
shadow mode
        ↓
one workflow / one ward
        ↓
human-approved copilot
        ↓
bounded actions only when earned
        ↓
retire one redundant legacy capability
        ↓
repeat
```

We cannot guarantee that software never fails. We can design stronger migration guarantees:

- **no big-bang cutover**;
- legacy remains the operational fallback until the new path earns dependency;
- **unavailable / stale / pending data never becomes false absence**;
- read permission never implies write permission;
- every stage has a rollback owner;
- upgrades are compatibility-checked before rollout;
- vendor/version changes require shadow revalidation;
- new write capability can never activate as an ordinary upgrade.

`app/hospital_upgrade.py` makes those upgrade rules executable.

[Hospital rollout playbook →](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md)

---

# What is already built

### Clinician workflow

The first synthetic workflow is Infectiology: microbiology lifecycle, documented anti-infective therapy, hygiene/isolation context, trends, contradictions, pending work, source inspection and handover/documentation drafts.

<div align="center">
  <img src="docs/screenshots/sjk-clinician-current.svg" alt="CareOS synthetic Infectiology clinician interface" width="820">
</div>

### Clinical truth with provenance

Consequential facts can retain:

```text
patient + encounter binding
source organisation / system / resource
original value / wording
clinical effective time
recorded / ingestion time
version + freshness
preliminary / final / corrected / cancelled / pending / stale / unavailable
terminology + unit mapping lineage
evidence span for document-derived facts
contradiction / supersession / review state
```

The model may propose structure. **It does not become the authority that creates trusted clinical truth.**

### Hospital-local data plane

`app/hospital_runtime.py` can compose currently implemented FHIR-family sources in synthetic/deidentified mode under an explicit cross-source patient identity strategy.

If one source becomes unavailable, admitted facts from another source may remain visible, but the combined response becomes:

```text
complete = false
may_assert_absence = false
```

Partial integration therefore cannot masquerade as a complete negative record.

### Zero-trust agent boundary

```text
untrusted model proposal
        ↓
deterministic Agent Gateway
patient · encounter · task · tools · operations · budgets
        ↓
trusted Tool Proxy
        ↓
source-linked context
        ↓
untrusted draft
        ↓
human review
```

The reasoning worker cannot grant itself a different patient, tool, network destination, break-glass state or write permission.

### Replayable hostile cases

The Recare capstone includes synthetic regression scenarios for wrong patient, prompt injection, source outage, stale data and unauthorised write escalation. A correctly blocked hostile run counts as a safety success.

[Recare capstone →](docs/RECARE_CAPSTONE.md)

---

## Four invariants

| | CareOS rule |
|---|---|
| **01** | **Pending ≠ negative.** |
| **02** | **Unavailable ≠ absent.** |
| **03** | **Documented therapy ≠ AI recommendation.** |
| **04** | **Agent draft ≠ source truth.** |

---

# Evidence state — no self-scores

| Area | Current evidence state |
|---|---|
| Clinician workflow | **DEMONSTRATED SYNTHETICALLY** |
| Clinical truth / provenance | **DEMONSTRATED SYNTHETICALLY** |
| Agent containment / adversarial evals | **DEMONSTRATED SYNTHETICALLY** |
| Hospital manifest / preflight | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| Hospital-local FHIR-family data plane | **IMPLEMENTED — NON-LIVE** |
| Docker / Helm install scaffold | **IMPLEMENTED — NON-LIVE** |
| FHIR CapabilityStatement discovery | **IMPLEMENTED** |
| Upgrade compatibility guard | **IMPLEMENTED + SYNTHETICALLY TESTED** |
| German real KIS/LIS interoperability | **EXTERNAL EVIDENCE REQUIRED** |
| Real clinician outcomes | **EXTERNAL EVIDENCE REQUIRED** |
| Production PHI operations | **BLOCKED BY DESIGN** |
| Generic HL7 / UI-bridge runtime | **NOT IMPLEMENTED** |
| Multi-hospital repeatability | **NOT YET EVIDENCED** |

The frozen synthetic clinical-truth holdout is intentionally not hidden: surfaced facts reached 100% precision/provenance in that benchmark, but recall is only 26.32% with 100% review-case burden, so **G1 remains blocked for production**.

[Full evidence + gaps →](docs/CURRENT_STATUS_AND_GAPS.md)

---

# Deployment shape

### Small / local evaluation

```text
Docker Compose
+ hospital manifest
+ hospital-owned env/secrets
+ local hospital data-plane API
```

### Enterprise scaffold

```text
Kubernetes / Helm
+ non-root container
+ read-only filesystem
+ hospital manifest ConfigMap
+ hospital Secret references
+ deny-outbound-by-default NetworkPolicy
```

The repo also contains an explicit GHCR image-build workflow with SBOM + build provenance support. **A published image is not automatically a clinical release**; hospital approval, pinned artifacts, security controls and production gates remain separate.

[Self-install architecture →](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md)

---

# Recare: collaboration, not duplication

Recare already operates the real hospital product/integration layer. CareOS is not a proposal to replace that platform.

The collaboration hypothesis is narrower:

> **Can real integration knowledge become increasingly productized — typed hospital capability manifests, reusable adapter/version profiles, automated conformance, upgrade preflight and fleet-safe regression tests — so marginal hospital integration effort trends toward configuration + conformance rather than custom engineering?**

We do **not** assume Recare lacks those capabilities internally. The next step is to compare this prototype with their production architecture and discard anything they already solve better.

[Recare collaboration map →](docs/RECARE_COLLABORATION_MAP.md) · [Integration accelerator →](docs/RECARE_INTEGRATION_ACCELERATOR.md)

---

# Build with us

> **We are all in this together.**

CareOS is Apache-2.0 and welcomes careful contributions from engineers, clinicians, designers, security researchers and interoperability specialists.

High-value lanes now include:

- 🔌 real adapter/conformance work;
- 🏥 installer + hospital IT UX;
- 🪪 cross-source identity / MPI integration;
- 🧪 vendor/version compatibility regressions;
- 🔐 generated network/security review artifacts;
- 🔴 agent security and patient isolation;
- 🎨 clinician/source-verification UX;
- 🌍 IPS / cross-border portability.

> **One failure → one fix → one regression test.**

[Contributing →](CONTRIBUTING.md) · [Community roadmap →](docs/COMMUNITY_ROADMAP.md) · [Open issues →](https://github.com/mikelninh/care-os/issues)

---

## What happens next

```text
Recare / production integration critique
        ↓
first real hospital capability manifest
        ↓
approved synthetic/deidentified KIS/LIS sandbox
        ↓
measure configuration vs custom engineering
        ↓
implement the highest-frequency real missing adapter
        ↓
shadow workflow
        ↓
second hospital / different vendor
        ↓
prove the infrastructure hypothesis
```

More speculative application features are lower value than proving this deployment model against reality.

---

## Deep review

| Need | Evidence |
|---|---|
| Big vision | [CareOS Endgame](docs/ENDGAME.md) |
| Hospital install / scale | [Self-Install Platform](docs/HOSPITAL_SELF_INSTALL_PLATFORM.md) |
| Adapter contract | [Connector SDK](docs/CONNECTOR_SDK.md) |
| Current truth / gaps | [Status & Gap Register](docs/CURRENT_STATUS_AND_GAPS.md) |
| Recare integration hypothesis | [Recare Integration Accelerator](docs/RECARE_INTEGRATION_ACCELERATOR.md) |
| Hospital rollout | [Implementation Playbook](docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md) |
| Logical architecture | [Architecture V2](docs/ARCHITECTURE_V2.md) |
| Germany / EU | [National Integration Map](docs/NATIONAL_INTEGRATION_MAP.md) |
| Germany → world | [Global Interoperability Blueprint](docs/GERMANY_GLOBAL_HEALTH_INTEROP_BLUEPRINT.md) |
| Agent security | [Agent Security Model](docs/AGENT_SECURITY_MODEL.md) |
| Full evidence index | [Technical Documentation Index](docs/TECHNICAL_DOCUMENTATION_INDEX.md) |

---

<div align="center">

### **Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

</div>

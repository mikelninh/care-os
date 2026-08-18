# CareOS Hospital Self-Install Platform

Baseline: **18 August 2026**

> Goal: a hospital IT team should be able to deploy a hospital-local CareOS data plane, describe existing systems once, run deterministic preflight/conformance checks and enter synthetic/deidentified evaluation without starting a bespoke integration project from zero.

This is now an **executable pre-hospital scaffold**, not proof of production self-service. CareOS remains blocked from identifiable live patient data until G0–G5 and hospital-specific approvals permit it.

---

## The product we are really building

Not:

> one new KIS every hospital must migrate to.

Instead:

```text
legacy KIS / LIS / RIS / PACS / documents / ePA
                        ↓
                 reusable adapters
                        ↓
            canonical clinical context
 identity · provenance · time · lifecycle · trust
                        ↓
             deterministic policy layer
                        ↓
        compatible clinician / agent applications
```

The scaling unit is the **adapter + capability profile + conformance evidence**, not the hospital project.

If two hospitals expose compatible FHIR R4 interfaces, they should reuse the same FHIR adapter even when the source vendors differ. Vendor/site differences belong in versioned configuration and compatibility evidence whenever possible — not forks of the clinical core.

---

## What is runnable now

### One CLI surface

```bash
python scripts/careos.py init \
  --hospital-id DE-BERLIN-001 \
  --site-name "Example Hospital"

python scripts/careos.py doctor hospital.json --env-file hospital.env
python scripts/careos.py preflight hospital.json
python scripts/careos.py up hospital.json --env-file hospital.env
python scripts/careos.py upgrade-check last-known-good.json proposed.json
python scripts/careos.py down hospital.json --env-file hospital.env
```

The CLI makes setup easier. It **does not bypass deployment gates**.

### Hospital-local API

`app/hospital_api.py` exposes:

```text
GET /health
GET /api/hospital/preflight
GET /api/hospital/patients/{patient_ref}/context
```

The patient-context route is currently restricted to synthetic/deidentified runtime modes and implemented FHIR-family adapters. It is **not** the future live clinical endpoint; a live route must additionally use hospital identity, treatment-context authorization and production audit.

### Docker Compose

```bash
docker compose -f deploy/docker-compose.hospital.yml run --rm preflight
docker compose -f deploy/docker-compose.hospital.yml up -d --build careos
```

### Kubernetes / Helm

Initial chart: `deploy/helm/careos/`.

The default chart:

- runs as non-root;
- uses read-only root filesystem;
- drops Linux capabilities;
- mounts the hospital manifest read-only;
- takes runtime secrets from an existing hospital Secret;
- denies outbound network by default;
- runs the hospital-local data-plane API.

The default image reference is a **deployment scaffold**, not evidence that a signed production image has already been released.

---

## Hospital Capability Manifest

Every site gets one non-secret, versionable manifest.

It records facts that integration teams otherwise rediscover manually:

```text
hospital/site
country
source system role
vendor/product/version
available interfaces
authentication mode
resources/domains
patient/encounter identity capability
cross-source identity strategy
resource/version provenance
clinical effective-time capability
lifecycle-state capability
incremental refresh capability
read/write capability
SSO/context launch
audit destination
security/privacy/clinical/rollback owners
```

It stores only **names of environment/secret references**, never real endpoints/tokens/passwords in the versionable document.

Example: `deploy/hospital.example.json`.

Machine model: `app/hospital_install.py`.

---

## Cross-source identity is not assumed

A hospital may have patient identifiers in both KIS and LIS without those identifiers being interchangeable.

CareOS therefore requires an explicit strategy:

```text
shared-enterprise-id
trusted-mpi
unknown
```

The current automatic multi-source runtime only accepts `shared-enterprise-id`.

A real trusted MPI/resolver can be added later as its own adapter. Until then, CareOS refuses to send one source's patient ID to every other system by assumption.

---

## Adapter selection policy

Preference order:

```text
1. ISiK/FHIR
2. standard FHIR R4
3. HL7 v2
4. stable vendor API
5. document/source feed
6. UI/computer-use bridge only as fallback
```

But **preference does not mean implementation**.

Current CareOS adapter maturity is machine-readable in `architecture/adapter-catalog.json`:

| Adapter family | Current CareOS status |
|---|---|
| FHIR R4 read | **implemented** |
| ISiK/FHIR read | **FHIR runtime + validation path** |
| HL7 v2 | **contract-only** |
| vendor API | **contract-only** |
| document/source feed | **contract-only** |
| UI/computer-use bridge | **contract-only** |
| live write adapters | **not runnable / blocked** |

A hospital that only exposes HL7 v2 does **not** receive a green self-install result today. Preflight identifies the target adapter and blocks until a runnable/tested implementation exists.

That honesty is part of the product.

---

## Adapter reuse

Illustrative example:

```text
Hospital A / Vendor A / FHIR ─┐
                              ├── standard-fhir-r4
Hospital B / Vendor B / FHIR ─┘
```

We do not want:

```text
hospital-a-fhir.py
hospital-b-fhir.py
hospital-c-fhir.py
```

unless conformance evidence proves a real incompatible difference.

The preflight plan emits a reuse key such as:

```text
standard-fhir-r4:read:vendor:product:version
```

Over time this becomes a compatibility knowledge base:

```text
adapter family
vendor/product/version
known deviations
conformance result
hospital count
last tested
supported workflow domains
known outage/lifecycle behavior
```

A fix found at one hospital should become a regression test before the next compatible hospital receives it.

---

## Hospital-local multi-source runtime

`app/hospital_runtime.py` currently composes implemented FHIR-family connectors.

For each source it preserves:

- source availability;
- source-linked truth;
- patient scope;
- namespaced fact identity.

If one source fails:

```text
KIS = current
LIS = unavailable
```

CareOS may still return the admitted KIS facts, but the combined result becomes:

```text
complete = false
may_assert_absence = false
```

A partial integration therefore cannot silently become a reassuring empty clinical state.

---

## Federated deployment: data plane local, control plane light

Long-term architecture:

```text
                    SHARED CONTROL PLANE
 signed releases · schemas · adapter catalog · policy packs
 conformance suites · non-PHI fleet health · compatibility matrix
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Hospital A      Hospital B      Hospital C
        data plane      data plane      data plane
             │              │              │
          KIS/LIS         KIS/LIS         KIS/LIS
```

The shared control plane should not require routine longitudinal PHI.

Each hospital controls:

- source credentials;
- provider identity/treatment context;
- patient-level clinical context;
- network permissions;
- audit destination;
- secrets/keys;
- local retention/cache policy;
- kill/rollback authority.

Shared infrastructure may distribute:

- signed software releases;
- adapter packages;
- schemas/terminology/policy versions;
- synthetic conformance fixtures;
- compatibility metadata;
- non-PHI operational telemetry where approved.

---

## Conformance before connection

Every adapter/site must prove behavior, not merely TCP connectivity.

Minimum suite:

```text
identity
- patient identity preserved
- encounter identity preserved where required
- cross-source patient mapping explicit
- patient A can never enter patient B

provenance
- source/resource ID preserved
- source version preserved where available
- effective vs recorded time remains distinguishable

clinical lifecycle
- preliminary
- final
- corrected
- cancelled
- pending
- stale
- unavailable

transport
- paging complete or fail closed
- retry/idempotency behavior
- partial reads visible
- source outage visible

security
- auth failure closed
- no credential in logs/config
- network destination bounded
- read != write

operations
- health/readiness
- latency/error budget
- rollback
- version compatibility
```

A site that fails conformance gets a precise integration blocker — not a custom bypass.

---

## Upgrades are treated like migrations

`app/hospital_upgrade.py` compares a last-known-good manifest with a proposed one.

Automatic rollout is blocked when an upgrade:

- removes a clinical source;
- swaps vendor/product under the same source identity;
- removes an interface;
- loses patient identity;
- loses provenance/effective-time/lifecycle capability;
- introduces new write capability;
- no longer passes current preflight.

A normal vendor/version change still requires shadow revalidation before dependency.

Command:

```bash
python scripts/careos.py upgrade-check current.json proposed.json
```

This creates a path toward KIS/vendor upgrades being tested before they become clinical incidents.

---

## Read and write are two products

Successful read integration never grants write authority.

```text
READ PLANE
source → adapter → canonical context → clinician/agent

WRITE PLANE
human-approved intent
        ↓
deterministic policy
        ↓
typed target adapter / controlled UI bridge
        ↓
write
        ↓
read-after-write verification
        ↓
audit
```

The current CareOS release ships **no runnable live transactional/write adapter**.

---

## Computer-use / Operator role

Computer-use can be an excellent migration bridge where the KIS exposes no practical typed write interface.

Treat it as an explicit fallback tier with separate compatibility evidence for:

- KIS UI/version;
- expected screen state;
- concurrency/session limits;
- field mapping;
- retry/idempotency;
- safe stop after UI changes;
- read-after-write verification.

Typed FHIR/HL7/vendor APIs remain preferable when they can provide stronger schemas, concurrency and conformance testing.

CareOS does not currently implement a production UI bridge.

---

## Smooth migration contract

We cannot guarantee that software never fails.

We can guarantee architectural behavior:

### 1. No big-bang cutover
Legacy remains authoritative until replacement evidence exists.

### 2. Fail back operationally
Early CareOS failure must not prevent clinicians using the existing workflow.

### 3. Fail closed semantically
Unknown/unavailable/stale/pending information never becomes false absence.

### 4. Reversible stages
Every stage has a rollback owner and rollback test.

### 5. Parallel evidence first
Shadow mode precedes dependency.

### 6. One capability retired at a time
Do not retire the entire KIS wholesale.

### 7. Upgrade before rollout is testable
Vendor/version changes go through compatibility + conformance before dependency.

That is the responsible meaning of **smooth from day one**.

---

## What still needs engineering

To reach genuinely low-touch real-hospital self-service:

1. automatic FHIR `CapabilityStatement` discovery;
2. generic HL7 v2 read adapter + conformance fixtures;
3. real vendor/API adapter plugin mechanism and compatibility records;
4. trusted MPI/source patient-ID resolver adapter;
5. generated network/data-flow package for DPO/CISO review;
6. signed/pinned release images + SBOM/provenance verification;
7. canary deployment + automated rollback;
8. one-command shadow observability;
9. non-PHI fleet compatibility/version reporting where approved;
10. secret/KMS integrations beyond environment injection;
11. production identity/context/audit integration;
12. installer UI for teams that prefer GUI over CLI.

These are engineering gaps. They are different from the external evidence gaps that only hospitals can close.

---

## Scale acceptance bar

Do not call CareOS self-service or repeatable because the installer works synthetically.

The hypothesis becomes evidence only when:

```text
Hospital A / Vendor A
        ↓
reusable adapter + configuration
        ↓
works without core fork

Hospital B / different vendor
        ↓
reusable adapter + configuration
        ↓
works without core fork
```

Track:

- integration engineer hours/site;
- time to first validated source;
- time to shadow mode;
- custom code/site;
- adapter/test reuse percentage;
- configuration-only deployment percentage;
- conformance failures caught before rollout;
- upgrade failures caught before production;
- rollback rehearsal success;
- support tickets per hospital/month.

Long-term north star:

> **A normal hospital IT team can get from download to validated shadow-mode readiness in hours, not months — while clinical/security/privacy gates remain stricter than the install UX.**

# CareOS Hospital Self-Install Platform

Baseline: **18 August 2026**

> End-state goal: a hospital IT team should be able to deploy the CareOS data plane, describe its existing systems once, run deterministic preflight/conformance checks and enter synthetic/deidentified evaluation without a bespoke integration project.

This is a **target operating model + executable pre-hospital scaffold**, not a claim that CareOS can process identifiable live patient data today. Live modes remain gated by G0–G5 and hospital-specific approvals.

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
        any compatible clinician / agent app
```

The scaling unit is the **adapter + capability profile**, not the hospital project.

If Hospital A and Hospital B use different vendors but both expose FHIR R4, they should reuse the same FHIR adapter. If both expose ISiK, they should reuse the same ISiK adapter. Vendor/site differences live in versioned configuration and conformance evidence whenever possible — not forks of the clinical core.

---

## The hospital experience

### Target installation journey

```text
1. install CareOS edge/data plane
2. fill non-secret hospital capability manifest
3. point secret references at hospital secret store
4. run preflight
5. adapter plan generated automatically
6. run connector conformance suite
7. synthetic/deidentified shadow evaluation
8. hospital review + gates
9. read-only shadow/live when allowed
10. copilot
11. narrowly controlled write only when separately earned
```

The target UX for hospital IT is eventually:

```bash
careos init
careos preflight hospital.json
careos verify
careos up
```

Current executable scaffold:

```bash
python scripts/hospital_preflight.py deploy/hospital.example.json

docker compose -f deploy/docker-compose.hospital.yml run --rm preflight
docker compose -f deploy/docker-compose.hospital.yml up -d careos
```

The Docker path is currently for synthetic/deidentified evaluation. The application itself refuses current live-data modes while release gates remain incomplete.

---

## Hospital Capability Manifest

Every site gets one **non-secret**, versionable manifest.

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
resource/version provenance
clinical effective-time capability
lifecycle-state capability
incremental refresh capability
read/write capability
SSO/context launch
audit destination
security/privacy/clinical/rollback owners
```

It stores only **references to secret environment variables**, never endpoints/tokens/passwords in the versionable manifest.

Example: `deploy/hospital.example.json`.

Machine model: `app/hospital_install.py`.

---

## Adapter selection policy

CareOS always prefers the least bespoke stable interface:

```text
1. ISiK/FHIR
2. standard FHIR R4
3. HL7 v2
4. stable vendor API
5. controlled document feed
6. UI/computer-use bridge only as pragmatic fallback
```

This is important for scale.

### Example

```text
Dedalus hospital A ── FHIR R4 ──┐
                                ├── standard-fhir-r4 adapter
SAP hospital B ───── FHIR R4 ───┘
```

We do **not** want:

```text
hospital-a-fhir.py
hospital-b-fhir.py
hospital-c-fhir.py
```

unless real conformance evidence proves the standard contract cannot represent the required difference.

### Reuse key

The preflight planner emits a reusable fingerprint such as:

```text
standard-fhir-r4:vendor:product:version
```

Over time this becomes an adapter/version knowledge base:

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

A fix for one deployment can then become a tested improvement for every compatible site.

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

The shared control plane should **not require routine longitudinal PHI**.

Each hospital owns/controls:

- local source credentials;
- provider identity/treatment context;
- data-plane network access;
- patient-level clinical context;
- local audit destination;
- secrets/keys;
- local retention/cache choices;
- kill/rollback authority.

The shared platform can distribute:

- signed software releases;
- adapter packages;
- schema/terminology/policy versions;
- synthetic conformance fixtures;
- compatibility metadata;
- non-PHI operational telemetry where approved.

This is how scale and Datenschutz reinforce rather than fight each other.

---

## Conformance before connection

Every adapter/site must prove behavior, not just establish TCP connectivity.

Minimum reusable conformance suite:

```text
identity
- patient identity preserved
- encounter identity preserved where required
- patient A can never enter patient B

provenance
- source/resource ID preserved
- source version preserved when available
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

A site that fails conformance does not get a magical custom bypass. The output becomes a precise integration issue.

---

## Read and write are two products

Never let successful read integration imply write authority.

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

Write adapter selection is disabled unless the manifest explicitly opts into a controlled-write deployment. The current CareOS release still blocks live transactional use globally.

---

## Operator / computer-use role

Computer-use can be an excellent **migration bridge**, not the canonical standard.

Use it when:

- there is no affordable typed interface;
- the KIS UI is the only supported write path;
- the target workflow is narrow and deterministic enough;
- screen/session state can be verified;
- errors halt safely;
- the action can be audited/replayed/verified.

Prefer typed FHIR/HL7/vendor APIs where available because they usually provide stronger schemas, versioning, concurrency and testability.

A UI bridge should have its own compatibility profile per KIS/version and should fail closed when the UI no longer matches the tested state.

---

## Zero-downtime migration contract

We cannot guarantee that no software component will ever fail.

We can design stronger guarantees:

### 1. No big-bang cutover
Legacy remains authoritative until a replacement capability has earned retirement.

### 2. Fail back operationally
Early CareOS failure must not prevent the clinician from using the existing KIS/LIS workflow.

### 3. Fail closed semantically
Unknown/unavailable/stale/pending information must never be converted into reassuring absence.

### 4. Reversible stages
Every stage has a rollback owner and rollback test.

### 5. Parallel evidence first
Shadow mode compares the new path against the existing workflow before dependency.

### 6. One capability retired at a time
Do not retire the KIS wholesale. Retire duplicated workflows only after measured stability.

This is the closest responsible architecture to a **smooth-from-day-one migration**.

---

## Packaging tiers

### Developer / synthetic

```text
Docker Compose
synthetic fixtures
preflight
conformance
```

### Hospital sandbox

```text
Docker/VM/Kubernetes
hospital manifest
approved deidentified sources
local secret store
audit target
no live PHI unless gates permit
```

### Production target

```text
signed container image
SBOM + provenance
Helm/Kubernetes or approved VM deployment
hospital IdP/context launch
network allowlists
KMS/secrets
audit/SIEM
backup/restore
monitoring/SLO
change/rollback control
independent security/privacy/clinical review
```

Initial Helm scaffold: `deploy/helm/careos/`.

---

## What must become automated next

To reach true self-service deployment, build toward:

1. `careos init` interactive manifest generator;
2. automatic FHIR `CapabilityStatement` discovery;
3. safe HL7/interface-engine capability probes;
4. adapter registry + signed adapter packages;
5. synthetic connector conformance runner;
6. compatibility matrix by vendor/product/version;
7. generated network/data-flow manifest for DPO/CISO review;
8. generated Kubernetes/VM deployment overlay;
9. one-command shadow-mode observability;
10. upgrade compatibility test before rollout;
11. canary + automated rollback;
12. fleet-wide non-PHI health/version reporting;
13. signed release + SBOM/provenance verification;
14. hospital-owned secret/KMS integrations;
15. installer UI/API for teams that do not want a CLI.

---

## Scale acceptance bar

Do not call this self-service or repeatable merely because the installer works synthetically.

The scale hypothesis becomes evidence only when:

```text
Hospital A / Vendor A
        ↓
standard adapter
        ↓
works without core fork

Hospital B / different vendor
        ↓
standard adapter/configuration
        ↓
works without core fork
```

Track:

- human integration hours per site;
- time to first synthetic/deidentified data;
- time to shadow mode;
- custom code lines/site;
- reused adapter/tests percentage;
- configuration-only deployments percentage;
- conformance failures found before rollout;
- rollback rehearsal success;
- support tickets per hospital/month.

Long-term north star:

> **A normal hospital IT team can get from download to validated shadow-mode readiness in hours, not months — while the clinical/security gates remain stricter than the install UX.**

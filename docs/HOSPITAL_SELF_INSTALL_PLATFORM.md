# CareOS Hospital Self-Install Platform

Baseline: **18 August 2026**

> Goal: make the repeatable part of hospital integration feel like a product while refusing to automate the parts that require real hospital authority, evidence or judgment.

This is an **executable synthetic/deidentified scaffold**, not proof of production self-service.

---

# 1. Intended operator experience

```text
careos init
careos doctor
careos preflight
careos review-pack
careos discover-fhir
careos up
careos upgrade-check
careos down
```

The command surface should be simple. The underlying safety requirements should not be optional.

Example:

```bash
python scripts/careos.py init \
  --hospital-id DE-BERLIN-001 \
  --site-name "Example Hospital"

python scripts/careos.py doctor hospital.json --env-file hospital.env
python scripts/careos.py preflight hospital.json
python scripts/careos.py review-pack hospital.json --out-dir /tmp/careos-review
python scripts/careos.py discover-fhir hospital.json --env-file hospital.env
python scripts/careos.py up hospital.json --env-file hospital.env
python scripts/careos.py upgrade-check last-known-good.json proposed.json
```

Current self-install runtime remains restricted to **synthetic/deidentified evaluation**.

---

# 2. Product shape

Not:

> one new KIS that every hospital must migrate to.

Instead:

```text
KIS / LIS / RIS/PACS / documents / ePA
                   ↓
            reusable adapters
                   ↓
       source-linked clinical context
identity · provenance · time · lifecycle · freshness
                   ↓
        deterministic policy boundary
                   ↓
 clinician / patient / bounded application surfaces
```

The scaling unit is the **adapter + capability profile + conformance/compatibility evidence**, not the hospital project.

---

# 3. Hospital Capability Manifest

Every site describes non-secret capabilities once:

```text
hospital/site/country
source role
vendor/product/version
available interfaces
authentication mode
resource/domain coverage
patient/encounter identity capability
cross-source identity strategy
resource/version identifiers
effective-time capability
lifecycle-state capability
incremental-refresh capability
read/write capability
SSO/context launch
audit destination existence
security/privacy/clinical/rollback owners
```

The versionable manifest contains only **environment/secret reference names**, never endpoint/token/password values.

Example: `deploy/hospital.example.json`.

Machine model: `app/hospital_install.py`.

---

# 4. Adapter truth today

| Adapter path | Current CareOS implementation state | Production evidence state |
|---|---|---|
| FHIR R4 read | **implemented research runtime** | real vendor/site evidence required |
| ISiK/FHIR read | **FHIR runtime + ISiK validation path** | real hospital/vendor ISiK evidence required |
| HL7 v2 ADT/ORU parsing | **implemented synthetic/deidentified library connector** | transport/interface-engine + real profile/vendor evidence required |
| HL7 v2 self-install transport | **not runnable** | external environment required |
| Vendor API | **contract only** | adapter/version implementation required |
| Document/source feed | **contract only** | real feed/runtime required |
| UI/computer-use bridge | **contract only** | implementation + compatibility evidence required |
| Live transactional/write | **blocked by release policy** | separate approved programme required |

Machine deployment maturity remains in `architecture/adapter-catalog.json`.

Important: the catalog intentionally does **not** advertise a green HL7 self-install runtime merely because the ADT/ORU parser exists. Production HL7 also requires a governed transport/interface-engine path, acknowledgement/retry/network behavior and real conformance evidence.

---

# 5. Cross-source patient identity

CareOS never assumes two identical-looking source IDs identify the same patient.

Supported architecture strategies:

```text
shared-enterprise-id
trusted-mpi
unknown
```

## Shared enterprise ID

Immediately runnable in the synthetic/deidentified multi-source runtime when the hospital explicitly declares the shared identifier contract.

## Trusted MPI/source-ID resolver

`app/patient_id_resolver.py` now defines and tests a deterministic resolver contract:

```text
enterprise patient
      ↓
trusted resolver
      ↓
KIS source ID
LIS source ID
RIS source ID
      ↓
source reads
      ↓
admitted facts normalized back to enterprise patient
```

Resolution states include resolved, not-found, ambiguous, unavailable and stale. Unsafe states fail before source reads.

The model/agent cannot choose or override patient mappings.

### Self-install boundary

The resolver contract is implemented, but `careos doctor/up` deliberately block trusted-MPI self-install until an **approved real hospital resolver adapter/configuration** is available.

Contract implementation is not named-vendor compatibility.

---

# 6. Generated hospital review pack

Hospital IT/security/privacy teams should not redraw the same architecture manually for every deployment.

```bash
careos review-pack hospital.json --out-dir /tmp/careos-review
```

Generates non-secret:

- JSON;
- Markdown;
- Mermaid data-flow view.

The pack includes:

- systems/vendors/versions;
- selected adapters/interfaces;
- authentication **mode**;
- endpoint/credential **reference names** only;
- read/write direction;
- identity/version/lifecycle capabilities;
- local/shared responsibility boundary;
- owner lanes;
- preflight warnings/blockers.

Secret-pattern regression tests protect the generated artifacts.

Boundary:

> The review pack reduces discovery/documentation work. It is **not** DSFA/DPIA, security, clinical or regulatory approval.

---

# 7. Hospital-local runtime

`app/hospital_runtime.py` composes implemented source connectors under an explicit patient identity strategy.

For each source it preserves:

- availability/freshness;
- patient scope;
- source-linked truth;
- namespaced fact identity.

Example degraded state:

```text
KIS = current
LIS = unavailable
```

CareOS may return admitted KIS facts, but the combined result becomes:

```text
complete = false
may_assert_absence = false
```

Partial integration therefore cannot masquerade as reassuring negative context.

---

# 8. Deployment shapes

## Docker Compose

Useful for local/smaller synthetic/deidentified evaluation.

## Kubernetes / Helm

The current scaffold supports:

- non-root runtime;
- read-only root filesystem;
- dropped Linux capabilities;
- read-only manifest mount;
- hospital-controlled secret references;
- deny-outbound-by-default network policy.

No Kubernetes requirement is implied for every hospital. A future small-provider deployment may use VM/appliance/managed patterns if they preserve the same security/operational contract.

---

# 9. Upgrade safety

`app/hospital_upgrade.py` compares last-known-good and proposed manifests.

Changes such as:

- source removal;
- vendor/product change;
- interface loss;
- patient-identity capability loss;
- provenance/time/lifecycle loss;
- adapter selection change;
- newly detected write authority

become visible findings rather than silent upgrades.

`app/rollout_control.py` adds the evidence state machine:

```text
PROPOSED
→ PREFLIGHT PASSED
→ CONFORMANCE PASSED
→ CANARY RUNNING
→ PROMOTED
        or
→ ROLLED BACK / BLOCKED
```

Promotion can be blocked by source failures, identity errors, incomplete reads, unsupported claims, safety stops, operator stop or unexpected write authority.

This is a reusable rollout contract—not evidence of zero-downtime production behavior.

---

# 10. Compatibility knowledge

`app/compatibility_registry.py` + `compatibility/` capture reusable non-PHI evidence by:

```text
adapter
vendor/product/version
interface/profile
resource/domain support
auth pattern
identity behavior
paging/version/lifecycle behavior
known deviations
conformance suite/result
known upgrade regressions
last tested
evidence class
```

Evidence classes:

```text
synthetic-only
real-sandbox
real-shadow
production-observed
```

Version matching is exact or explicitly allowlisted. Neighboring versions are not guessed compatible.

Critical rule:

> **Compatibility evidence may reduce repeated investigation. It can never auto-approve rollout.**

---

# 11. Federated architecture

Long-term split:

```text
                    LIGHT SHARED CONTROL PLANE
 signed releases · schemas · adapter catalog · policy packs
 conformance suites · non-PHI compatibility/fleet knowledge
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       PROVIDER DATA     PROVIDER DATA    PROVIDER DATA
          PLANE A           PLANE B          PLANE C
              │               │               │
          local PHI        local PHI       local PHI
          source truth     source truth    source truth
```

Core bedside source/context operations should not require routine PHI in a central CareOS control plane.

Shared infrastructure may distribute software/contracts/evidence and receive approved non-PHI operational metadata, but provider policy owns what leaves the local boundary.

---

# 12. Migration

```text
legacy remains authoritative
        ↓
read-only connection
        ↓
shadow mode
        ↓
one workflow / one ward
        ↓
human-reviewed copilot
        ↓
bounded action only when independently earned
        ↓
retire one redundant capability
        ↓
repeat
```

No big-bang cutover.

No read→write implication.

No patient matching by model.

No vendor/version change without revalidation.

No live mode merely because the installer is technically capable of starting a container.

---

# 13. What has to be proven in a real hospital

The self-install hypothesis is falsifiable.

For each site measure:

- discovery hours;
- configuration hours;
- custom engineering hours;
- adapter/core changes;
- conformance failures;
- identity surprises;
- security/review effort;
- time to deidentified connection;
- time to first useful shadow workflow;
- upgrade regressions;
- support burden.

Then ask:

> **Did the second compatible deployment inherit meaningful work from the first?**

If not, the product has not yet converted integration into infrastructure.

---

# 14. Current hard boundary

The pre-hospital scaffold is good enough to test the integration hypothesis with a real team.

It does **not** prove:

- zero-touch installation;
- compatibility with a named hospital/vendor;
- production PHI operations;
- real MPI integration;
- production HL7 transport;
- target-environment reliability/SLOs;
- hospital approvals;
- multi-hospital repeatability.

Those are the next evidence layers, not missing marketing copy.

See also:

- `docs/HOSPITAL_SCALE_FOUNDATION.md`;
- `docs/HOSPITAL_IMPLEMENTATION_PLAYBOOK.md`;
- `docs/CURRENT_STATUS_AND_GAPS.md`;
- `docs/GATES.md`;
- `docs/ENDGAME.md`.
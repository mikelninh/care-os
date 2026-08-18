# CareOS Hospital-Scale Foundation

Baseline: **18 August 2026**

Purpose: define the reusable infrastructure that should make hospital #N easier than hospital #1 while keeping the distinction between **implemented contracts** and **real hospital evidence** explicit.

## North star

> **Hospital variation should become configuration, mappings, adapter/version evidence and policy — not forks of the clinical core.**

The desired flywheel:

```text
hospital capability manifest
→ deterministic adapter selection
→ patient identity strategy
→ conformance
→ generated review artifacts
→ shadow/canary
→ compatibility evidence
→ incident/regression knowledge
→ next compatible hospital inherits the learning
```

---

## 1. Trusted cross-source patient identity

Implemented:

- `app/patient_id_resolver.py`;
- exact deterministic source-ID mapping contract;
- resolver identity/version/namespace/freshness;
- resolved / not-found / ambiguous / unavailable / stale states;
- multi-source hospital runtime can query each source with its own patient identifier and normalize admitted facts back to the enterprise patient reference;
- missing/ambiguous/stale resolution fails before connector reads;
- model/agent has no patient matching authority.

Self-install boundary:

- `shared-enterprise-id` remains the immediately runnable multi-source path;
- `trusted-mpi` runtime contract exists;
- `careos doctor/up` currently block trusted-MPI self-install until an approved real hospital MPI/EMPI resolver adapter is configured.

**Not claimed:** compatibility with a particular hospital MPI/vendor/service.

---

## 2. Generated hospital IT/security/data-flow review pack

Implemented:

- `app/hospital_review_pack.py`;
- `scripts/generate_hospital_review_pack.py`;
- `careos review-pack` CLI;
- JSON, Markdown and Mermaid outputs;
- source/vendor/version/adapter inventory;
- authentication mode and endpoint/credential **reference names**, never values;
- read/write boundary;
- identity/lifecycle/version capabilities;
- accountable owner lanes;
- preflight blockers/warnings;
- provider-local data-flow diagram;
- automated secret-pattern checks.

Boundary:

> The generated pack reduces repeated discovery/documentation effort. It is **not DSFA/DPIA, security, regulatory or clinical approval**.

Accountable hospital reviewers remain responsible for approval.

---

## 3. Evidence-gated rollout / rollback

Implemented in `app/rollout_control.py`:

```text
PROPOSED
→ PREFLIGHT PASSED
→ CONFORMANCE PASSED
→ CANARY RUNNING
→ PROMOTED
        or
→ ROLLED BACK / BLOCKED
```

Canary evidence includes:

- source availability/freshness;
- patient identity errors;
- connector errors;
- incomplete reads;
- unsupported claims;
- safety-stop events;
- operator stop;
- newly detected write authority.

Rules:

- an upgrade requiring shadow revalidation cannot promote without passing canary evidence;
- safety/reliability failures roll back;
- rollback is idempotent and retains the last known-good release reference;
- adding write authority is a blocker, not an ordinary upgrade.

**Not claimed:** real zero-downtime production rollout until this is exercised in approved target infrastructure.

---

## 4. Vendor/product/version compatibility registry

Implemented in `app/compatibility_registry.py` + `compatibility/`.

Each record may capture:

```text
adapter family
vendor / product / version
interface/profile
supported resources/domains
auth pattern (non-secret)
patient/encounter identity behavior
paging/version/lifecycle behavior
known deviations
conformance suite + result
last tested
known upgrade regressions
evidence class
```

Evidence classes:

- `synthetic-only`;
- `real-sandbox`;
- `real-shadow`;
- `production-observed`.

Version matching is explicit:

- exact; or
- explicit allowlist.

No semver-style or neighboring-version compatibility is guessed.

Critical rule:

> **A compatibility record can reduce repeated investigation. It can never auto-approve rollout.**

A rollout must still pass its own site/release evidence gates.

---

## 5. HL7 v2 legacy read connector

Implemented library slice: `app/connectors/hl7v2_connector.py`.

Current supported synthetic/deidentified scope:

- MSH/PID/PV1 patient/encounter context;
- ORU/OBX observations;
- message-control-ID deduplication;
- preliminary/final/corrected/cancelled result-state mapping;
- source/message identity;
- effective timestamp where provided;
- wrong-patient rejection;
- malformed/partial feed becomes UNKNOWN/partial, never reassuring absence;
- read-only connector capability.

Important boundary:

> **This is not yet a self-install production HL7 adapter.**

Missing before the adapter catalog may advertise a runnable self-install HL7 path:

- approved transport/interface-engine adapter (for example a governed MLLP/channel integration or equivalent);
- authentication/networking/acknowledgement/retry contract for that transport;
- real vendor/interface-engine sandbox evidence;
- deployment-specific message/profile mapping;
- conformance/regression evidence against the real environment.

Do not claim universal HL7 v2 compatibility.

---

## 6. Hospital IT command surface

Current CLI:

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

The command surface is deliberately easier than the internal architecture.

It must never make a missing safety dependency disappear:

- missing patient identity → block;
- contract-only adapter → block;
- trusted MPI with no real resolver configuration → block;
- live patient mode while gates fail → block;
- new write authority during upgrade → block.

---

## 7. What turns one hospital into infrastructure

For every real deployment, capture reusable non-PHI evidence:

1. capability manifest;
2. adapter/version profile;
3. conformance output;
4. identity behavior;
5. known deviations;
6. upgrade behavior;
7. failure/regression fixtures;
8. rollout evidence;
9. support/incident lessons;
10. custom work hours.

Then measure:

```text
adapter reuse ↑
conformance reuse ↑
known-version coverage ↑
custom core code ↓
discovery hours/site ↓
integration lead time ↓
upgrade surprises ↓
```

If hospital #50 still needs the same bespoke discovery and custom core code as hospital #1, the platform has not become infrastructure.

---

## 8. Evidence ladder from here

```text
implemented synthetic contracts
        ↓
real vendor/interface sandbox
        ↓
one hospital capability manifest
        ↓
read-only/shadow integration
        ↓
compatibility record: real-shadow
        ↓
controlled upgrade + rollback exercise
        ↓
second hospital / different vendor
        ↓
prove core stays unchanged
        ↓
production-observed compatibility evidence
```

The next step is not another generic adapter invented from documentation. It is **real interface reality**.

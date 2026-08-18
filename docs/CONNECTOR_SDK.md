# CareOS Connector SDK Contract

Goal: integrate new hospitals/vendors **without forking the clinical core** and make each deployment reduce the effort of the next one.

Implementation foundations:

- `app/connectors/base.py` — runtime connector contract;
- `app/hospital_install.py` — hospital capability manifest + deterministic adapter selection;
- `deploy/hospital.example.json` — non-secret site configuration example;
- `scripts/hospital_preflight.py` — preflight/install-plan CLI.

## Scaling rule

> **Hospital variation belongs in adapters, capability profiles and configuration — not branches of CareOS.**

If two different vendors expose compatible FHIR R4 interfaces, both should use `standard-fhir-r4`. If ISiK is exposed, prefer `standard-isik-fhir`. Vendor/site deviations become versioned compatibility evidence.

```text
Dedalus / FHIR ─┐
SAP / FHIR ─────┼─► standard-fhir-r4 ─► canonical truth
Vendor C / FHIR ┘
```

## Connector responsibilities

Every connector must:

1. declare capabilities honestly;
2. authenticate using the deployment-approved mechanism;
3. read only explicitly allowed data for the configured workflow;
4. return data through the canonical `TruthEnvelope` contract;
5. preserve source identity/version/time where available;
6. expose freshness/availability separately from clinical content;
7. fail visibly on incomplete/unsafe retrieval;
8. never turn transport failure into an empty/normal patient state;
9. keep patient/encounter binding authoritative outside model output;
10. keep read and write as separate capabilities.

## Hospital Capability Manifest

Before connector code runs, the site describes its source systems in one **non-secret** manifest:

```text
vendor/product/version
system role
available interfaces
auth mode
endpoint + credential ENV REFERENCES only
resources/domains
patient/encounter identity
source IDs/versions
effective time/lifecycle state
incremental refresh
read/write capability
```

Real endpoints, passwords, certificates and tokens remain in hospital-approved secret stores.

The preflight planner chooses adapters using this priority:

```text
ISiK/FHIR
→ FHIR R4
→ HL7 v2
→ stable vendor API
→ controlled document feed
→ UI/computer-use bridge as explicit fallback
```

It never generates a magical custom integration when no safe interface exists; that becomes a blocking discovery item.

Run:

```bash
python scripts/hospital_preflight.py deploy/hospital.example.json
```

## Runtime capability manifest

`ConnectorCapabilities` declares at minimum:

- connector ID;
- vendor/system;
- standard/interface version;
- read-only vs write capability;
- supported resource/domain set;
- auth mode;
- paging support;
- resource-version support;
- incremental-refresh support;
- known limitations.

A capability that is merely planned must be `false`/absent, not marketing text.

## Standard read result

```text
ConnectorReadResult
  connector_id
  SourceState
    current | stale | unavailable | unknown
    last successful refresh
    maximum allowed age
  TruthEnvelope | null
```

When a source is unavailable, `truth` is null. It is **not** an empty `TruthEnvelope`.

## Mapping rule

Connectors map source data into canonical facts; specialty/application layers consume canonical facts. Vendor parsing/API code must not leak into clinical workflow packs.

```text
Vendor A KIS ─┐
Vendor B KIS ─┼─► connectors ─► ClinicalFact graph ─► compatible applications
LIS ──────────┤
ePA ──────────┘
```

## Conformance tests required for every connector

### Identity

- patient identity preserved;
- encounter identity preserved where required;
- patient A data cannot enter patient B envelope.

### Provenance / time

- source/resource identity preserved;
- source version preserved where available;
- effective vs recorded/ingested time semantics tested.

### Lifecycle / failure

- preliminary/final/corrected/cancelled/pending semantics preserved where exposed;
- paging complete or fails closed;
- duplicates/retries idempotent where applicable;
- outage returns `unavailable`;
- stale cache returns `stale`;
- partial read is never presented as complete.

### Security

- cross-origin/unsafe continuation rejected where relevant;
- credentials never appear in checked-in capability config/logs;
- no write occurs in read-only mode;
- capability manifest matches actual tests.

## Read and write are different adapter contracts

A successful read path never grants write authority.

Write progression:

```text
human-approved intent
→ deterministic policy
→ explicit write adapter
→ target write
→ read-after-write verification
→ audit
```

UI/computer-use can be a valuable last-mile write bridge for legacy KIS systems, but must carry its own compatibility/version/concurrency/screen-state tests. It is not equivalent to a typed API.

The current CareOS release remains globally locked against live transactional use.

## Compatibility registry target

For every real integration keep a checked-in **non-secret** compatibility record and private deployment configuration:

```json
{
  "vendor": "...",
  "product": "...",
  "version": "...",
  "adapter": "standard-fhir-r4",
  "interface": "FHIR R4",
  "auth": "...",
  "patient_identity": "...",
  "resources": [],
  "paging": "...",
  "versions": "...",
  "lifecycle": "...",
  "documents": "...",
  "known_gaps": [],
  "conformance_result": "...",
  "tested_at": "..."
}
```

A fix found at one hospital should become a reusable adapter regression test before fleet rollout.

## Scale acceptance test

G8 cannot pass until at least two independent hospital/vendor deployments run through these contracts **without modifying/forking the CareOS clinical core for the vendor**.

Measure:

- adapter reuse rate;
- configuration-only deployment rate;
- custom engineering hours/site;
- time from manifest to first validated data;
- conformance failure detection before rollout;
- support incidents by adapter/vendor/version.

The long-term target is **marginal hospital integration cost approaching configuration + conformance, not custom software engineering**.

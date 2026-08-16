# CareOS Connector SDK Contract

Goal: integrate new hospitals/vendors without forking the CareOS clinical core.

Implementation foundation: `app/connectors/base.py`.

## Connector responsibilities

Every connector must:

1. declare capabilities honestly;
2. authenticate to its source using the deployment-approved mechanism;
3. read only the explicitly allowed data for the configured workflow;
4. return data through the canonical `TruthEnvelope` contract;
5. preserve source identity/version/time where available;
6. expose source freshness/availability separately from clinical content;
7. fail visibly on incomplete/unsafe retrieval;
8. never turn transport failure into an empty/normal patient state.

## Capability manifest

At minimum declare:

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

Connectors map source data into canonical facts; specialty packs consume canonical facts. Specialty packs must not contain vendor-specific parsing or API code.

```text
Vendor A KIS ─┐
Vendor B KIS ─┼─► connectors ─► ClinicalFact graph ─► specialty pack
LIS ──────────┤
ePA ──────────┘
```

## Conformance tests required for every connector

- patient identity preserved;
- source/resource identity preserved;
- source version preserved where available;
- effective vs recorded/ingested time semantics tested;
- paging complete or fails closed;
- duplicates/retries idempotent where applicable;
- outage returns `unavailable`;
- stale cache returns `stale`;
- cross-origin/unsafe continuation rejected where relevant;
- no write occurs in read-only mode;
- patient A data cannot enter patient B envelope;
- capability manifest matches actual tests.

## Vendor capability matrix

For every real integration create a checked-in **non-secret** capability record and a private deployment-specific configuration containing endpoints/credentials/network details.

Suggested fields:

```json
{
  "vendor": "...",
  "product": "...",
  "version": "...",
  "interface": "ISiK/FHIR/vendor API/...",
  "auth": "...",
  "patient_identity": "...",
  "resources": [],
  "paging": "...",
  "versions": "...",
  "documents": "...",
  "events_or_subscriptions": "...",
  "known_gaps": [],
  "tested_at": "..."
}
```

## Scale acceptance test

G8 cannot pass until at least two independent hospital/vendor deployments run through this contract **without modifying/forking the CareOS clinical core for the vendor**.

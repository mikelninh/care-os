# Recare Integration Accelerator — Collaboration Hypothesis

Baseline: **18 August 2026**

> This document compares Recare's public integration story with CareOS research. It does **not** claim knowledge of Recare's private architecture, internal implementation burden or roadmap.

## What Recare already does well publicly

Recare already attacks hospital integration through multiple paths:

- HL7-based KIS integration for hospital products;
- FHIR integration in parts of the wider care ecosystem;
- Patient Overview combining KIS + Recare/document information;
- Operator computer-use bridge that enters Recare-created content into the existing KIS UI without a traditional interface project;
- staged implementation with setup, staff training and pilot rollout;
- real production security/operations including ISO 27001 and BSI C5 Type 2 claims.

Public sources:

- https://recareai.com/krankenhaus
- https://recareai.com/krankenhaus/recare-patient-overview
- https://recareai.com/krankenhaus/recare-operator
- https://recareai.com/it-sicherheit-datenschutz

This means the collaboration opportunity is **not "teach Recare how to integrate hospitals."** They have the production experience we do not.

---

## Public friction that is visible

The Operator public page says:

- it is individually configured for a clinic;
- rollout includes setup, training and a pilot;
- the complete rollout depends on hospital size and is coordinated individually;
- while Operator controls the KIS UI, that KIS surface cannot simultaneously be used by another user.

That makes Operator a powerful bridge, but not a universal replacement for typed interfaces.

Standard HL7/FHIR integration also cannot remove every site-specific variable: vendor/version, local mappings, identity, network, authentication, interface-engine configuration, lifecycle semantics and hospital governance still exist.

---

## The hypothesis

> **Can Recare turn its accumulated integration expertise into an increasingly self-service integration product, so each new hospital inherits the knowledge of every previous one?**

CareOS can prototype a possible architecture:

```text
Hospital Capability Manifest
          ↓
automatic adapter selection
          ↓
standard adapter catalog
          ↓
site/vendor conformance suite
          ↓
shadow/read-only rollout engine
          ↓
compatibility + observability record
          ↓
next hospital reuses the same evidence
```

This would complement — not replace — Recare's integration engineers and Operator.

---

## Proposed components

### 1. Hospital Capability Manifest

One versionable, non-secret description of:

- KIS/LIS/RIS/PACS vendors + versions;
- HL7/FHIR/ISiK/vendor interfaces;
- authentication;
- patient/encounter identity;
- lifecycle/version/provenance support;
- context launch;
- audit/security destinations;
- allowed deployment authority.

Result: fewer repeated discovery calls and a machine-readable integration starting point.

CareOS prototype: `app/hospital_install.py` + `deploy/hospital.example.json`.

### 2. Adapter registry

Instead of hospital-specific source code:

```text
standard-isik-fhir
standard-fhir-r4
standard-hl7v2-read
standard-document-ingest
vendor-api-configured
controlled-ui-bridge
```

Each deployment selects the strongest available adapter and records vendor/version deviations as compatibility data.

### 3. Conformance lab

Before connecting production workflows, replay the same synthetic cases against every site adapter:

- patient isolation;
- source IDs/provenance;
- preliminary/final/corrected/pending;
- paging;
- outage/partial reads;
- auth failure;
- stale data;
- read/write separation;
- rollback.

This creates a repeatable quality gate around the integration itself.

### 4. Integration compatibility matrix

Over time:

```text
vendor/product/version
supported adapter
supported domains
known deviations
last conformance run
hospital count
open defects
operator fallback required?
```

A production bug at Hospital A can become a regression test protecting Hospital B.

### 5. Operator as explicit fallback tier

Integration preference:

```text
ISiK/FHIR
  ↓
FHIR
  ↓
HL7
  ↓
vendor API
  ↓
document/file path
  ↓
Operator/UI bridge
```

Operator remains strategically valuable because legacy software often leaves no clean API. But the platform should know that it is using a UI bridge and apply separate controls for:

- supported KIS UI version;
- screen-state verification;
- concurrent-session limitation;
- field mapping;
- retry/idempotency;
- read-after-write verification;
- safe stop after UI change;
- automatic compatibility regression tests.

### 6. Deployment bundle

Hospital IT gets:

```text
signed container
Helm/VM deployment
non-secret manifest
secret-store references
network/data-flow export
preflight report
conformance report
health/SLO dashboard
rollback command/runbook
```

The target is not "zero implementation team". It is **implementation work concentrated on genuine local exceptions instead of rediscovering the standard path**.

---

## Where CareOS could help Recare specifically

If joining Recare, I would propose learning their actual integration architecture first, then test whether any of these are useful:

1. turn implementation discovery into a typed capability manifest;
2. build an adapter compatibility/conformance registry from existing integrations;
3. make integration failures replayable in CI;
4. classify each source/write path as typed interface vs Operator fallback;
5. instrument integration effort per hospital/vendor;
6. automatically generate customer-side data-flow/network/security documentation;
7. add upgrade preflight before KIS/Operator UI version changes;
8. package a local edge/data-plane option if Recare's architecture and customer demand support it;
9. separate configuration differences from true adapter code differences;
10. measure the key scaling metric: **custom engineering hours per additional hospital trending toward zero**.

---

## Biggest unknowns to ask Pavlo

These questions determine whether this idea is useful or redundant:

- Do integrations already use an internal adapter SDK/capability registry?
- How much implementation time is still site-specific vs reusable today?
- How many KIS/vendor/version profiles are actively maintained?
- Where do HL7 integrations break most often: semantics, identity, local mappings, transport, or operations?
- How are KIS upgrades detected/tested before they break an integration?
- How is Operator compatibility versioned and regression-tested across KIS UIs?
- Can a hospital's own IT deploy/configure anything themselves today, or is Recare-led implementation required?
- Which customer-side security/network documents are recreated per project?
- What is the median time from signed customer to first useful integrated workflow?
- Which step consumes the most interoperability-team time?

Do not assume the answer. Let Recare production reality decide what survives.

---

## North-star scaling metric

> **Marginal hospital integration cost approaches configuration + conformance, not custom software engineering.**

Supporting metrics:

- hours from discovery to first validated data;
- configuration-only deployment rate;
- adapter reuse rate;
- custom code/site;
- KIS-version regression detection before production;
- number of hospitals per maintained adapter;
- support incidents per adapter/version;
- Operator fallback rate;
- rollback success;
- time from new adapter fix to fleet-safe rollout.

If Recare already has most of this internally, that is excellent: the work then becomes learning and improving the real system rather than rebuilding it in CareOS.

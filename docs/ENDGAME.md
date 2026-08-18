# CareOS Endgame — Open Clinical Interoperability Fabric

Baseline: **18 August 2026**

## One sentence

> **Any hospital, in any country, should be able to keep its existing systems, install a local trustworthy interoperability/data plane, connect through reusable standards-based adapters and safely expose the resulting context to clinicians and bounded applications.**

The endgame is not for CareOS to become the world's KIS/EHR.

The endgame is for the underlying **clinical context contract, adapter model, conformance tests and migration path** to become so boring and reusable that hospital interoperability stops being a bespoke consulting problem.

---

## The architecture

```text
                 GLOBAL / OPEN CONTRACTS
            FHIR · IPS · provenance · trust
                         │
                  regional profiles
               EHDS / MyHealth@EU / ...
                         │
                   country packs
              Germany: ISiK · ePA · TI
                         │
            open conformance + adapters
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
      Hospital A     Hospital B     Hospital C
       data plane     data plane     data plane
           │             │             │
      legacy KIS     modern EHR      mixed stack
           │             │             │
           └──── canonical context ────┘
                         │
           clinician / agent / app ecosystem
```

## What should be standard

Not every screen. Not every database. Not every national identifier.

Standardize the seams:

1. patient + encounter binding;
2. source identity + provenance;
3. effective/recorded time;
4. clinical lifecycle state;
5. terminology + mapping lineage;
6. freshness/availability;
7. consent/restriction/purpose metadata where applicable;
8. read/write capability separation;
9. agent/application authority manifest;
10. audit semantics;
11. portable minimum summary;
12. conformance behavior and failure states.

That allows different vendors to compete above and below the contract without trapping hospitals.

---

## The flywheel

```text
hospital connects
      ↓
capability manifest
      ↓
reusable adapter selected
      ↓
conformance run
      ↓
new vendor/version knowledge captured
      ↓
adapter/tests improve
      ↓
next compatible hospital gets easier
      ↓
more applications can rely on the same contract
```

Every deployment should lower the cost/risk of the next deployment.

If deployment #100 still requires the same discovery/custom-code effort as deployment #1, the platform has failed to become infrastructure.

---

## Open ecosystem strategy

The interoperability layer should be open enough that hospitals, vendors, startups, researchers and public institutions can implement against it.

CareOS can contribute:

- Apache-2.0 reference implementation;
- connector SDK;
- synthetic conformance suite;
- lifecycle/provenance contracts;
- agent authority/eval contracts;
- country-pack examples;
- deployment/migration playbook;
- compatibility records;
- reference UI.

The goal is **not** to own every adapter forever.

A healthy ecosystem eventually has:

```text
KIS vendors publishing adapters
LIS vendors publishing adapters
hospitals publishing fixes/tests
AI companies building compatible apps
public bodies maintaining national profiles
independent labs running conformance
```

---

## Business / partnership endgame

There are multiple viable outcomes:

### 1. CareOS as open infrastructure
A neutral reference implementation and test suite used by many products.

### 2. CareOS ideas inside a company such as Recare
The adapter catalog, preflight, conformance, agent-safety and migration architecture become part of an existing production platform with hospital reach.

### 3. Public-private German reference infrastructure
Industry + hospitals + gematik/HL7/public bodies standardize the contracts and conformance mechanisms; vendors implement them competitively.

### 4. International reference pattern
The same core is combined with regional/country packs around FHIR/IPS and local trust/policy infrastructure.

These outcomes are compatible. The mission matters more than preserving CareOS as a standalone product brand.

---

## Germany first

Germany is the first proving ground because it combines:

- heterogeneous legacy KIS/LIS environments;
- strong privacy/security expectations;
- ISiK/FHIR direction;
- ePA/TI infrastructure;
- EHDS transition requirements;
- enough complexity to expose weak interoperability assumptions quickly.

If the architecture can modernize German hospitals without forcing a central replacement system, that is useful evidence for other fragmented health systems.

This is a hypothesis until real multi-hospital deployments exist.

---

## Worldwide

Global scaling should use composition:

```text
CareOS/open core
+ FHIR/IPS
+ country pack
+ language/presentation pack
+ local identity/trust/policy
+ hospital adapters
```

Never require Germany-specific infrastructure in another jurisdiction.

Never let translation replace the original clinical wording.

Never let format validity imply issuer trust.

Never let an imported record automatically gain local clinical authority without receiving-context policy.

---

## Migration end state

Hospitals should never need a dangerous "go-live weekend" merely to benefit from modern software.

The migration is continuous:

```text
legacy untouched
  ↓
read-only adapter
  ↓
shadow context
  ↓
optional clinician surface
  ↓
drafts
  ↓
human-confirmed bounded actions
  ↓
retire one redundant legacy capability
  ↓
repeat
```

At every stage the old path remains available until the new capability earns dependency.

---

## Success metrics for the mission

### Integration economics

- median hours from manifest to validated connection;
- percentage of installations requiring no custom core code;
- adapter reuse rate;
- vendor/version coverage;
- conformance failures caught pre-production;
- upgrade breakage rate.

### Clinical workflow

- Time Returned to Care;
- manual searches/copy-paste removed;
- source-verification behavior;
- correction burden;
- missed pending work;
- adoption.

### Safety/trust

- wrong-patient events;
- unsupported claims;
- source-state errors;
- unauthorised actions;
- rollback success;
- audit completeness.

### Openness

- external contributors;
- third-party compatible apps/adapters;
- independent conformance implementations;
- hospitals able to switch application vendors without rebuilding source integrations.

---

## The endgame test

A platform has reached the intended state when a hospital can say:

> "We changed our KIS vendor, but our clinical apps kept working because the interoperability contract stayed stable."

And an application vendor can say:

> "We integrated once against the open clinical context contract rather than building 80 hospital-specific pipelines."

And a clinician can say:

> "I did not notice a migration project. The useful parts simply appeared in my workflow, and the old system remained there until we no longer needed that part of it."

That is the vision to keep in every architecture and product decision.

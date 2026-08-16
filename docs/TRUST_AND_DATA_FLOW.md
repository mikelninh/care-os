# CareOS Trust Boundaries & Data Flow

Status: reference architecture and assurance input. A real hospital deployment must replace generic actors/systems with its actual environment and be reviewed by responsible Datenschutz and security functions.

## 1. Data classification

CareOS uses four high-level classes.

| Class | Examples | Default location |
|---|---|---|
| **PHI / clinical** | patient facts, notes, results, meds, allergies, source excerpts | provider data plane |
| **Identity / access** | user ID, role, organisation, patient/encounter context, auth tokens | provider identity/security boundary |
| **Security/audit** | access events, break-glass reason, integrity metadata | provider-approved audit/SIEM boundary |
| **Non-PHI operations** | release versions, service health, latency, connector capability, aggregate non-identifying metrics | control plane may process |

Clinical free text is prohibited in routine analytics/telemetry.

## 2. Trust zones

```text
┌────────────────────────────────────────────────────────────┐
│ Zone 0 — External / untrusted                              │
│ Internet, model APIs where approved, external services     │
└─────────────────────────┬──────────────────────────────────┘
                          │ explicit egress policy
┌─────────────────────────▼──────────────────────────────────┐
│ Zone 1 — CareOS control plane                              │
│ releases/config/policy/non-PHI operations                  │
│ no routine identifiable clinical record                   │
└─────────────────────────┬──────────────────────────────────┘
                          │ signed/versioned distribution
══════════════════════════╪═══════════════════════════════════
                          │ provider boundary
┌─────────────────────────▼──────────────────────────────────┐
│ Zone 2 — Provider application/data plane                   │
│ connectors · truth · policy · UI · provider cache          │
└─────────────┬──────────────────────────────┬───────────────┘
              │                              │
┌─────────────▼──────────────┐   ┌──────────▼───────────────┐
│ Zone 3 — Source systems    │   │ Zone 4 — Identity/SecOps │
│ KIS/LIS/RIS/PVS/ePA/docs   │   │ IdP · KMS · audit · SIEM │
└────────────────────────────┘   └──────────────────────────┘
```

No network zone is trusted merely because it is internal.

## 3. Primary read flow

```text
1. Clinician opens patient context
        ↓
2. Provider IdP authenticates clinician
        ↓
3. Trusted launcher supplies organisation + patient + encounter context
        ↓
4. CareOS validates token + launch binding
        ↓
5. Policy engine evaluates role/scope/treatment context
        ↓
6. Connector requests minimum necessary source data
        ↓
7. Source returns data + identifiers/versions/timestamps
        ↓
8. Connector produces SourceState + TruthEnvelope
        ↓
9. Clinical truth/reconciliation validates patient + provenance + state
        ↓
10. Required audit event is recorded
        ↓
11. Clinician sees context + source + freshness/review state
```

If required audit recording fails, the secure-read policy may withhold clinical truth rather than silently permit unaudited access.

## 4. Patient identity data flow

Automatic attachment uses verified strong identifiers where possible.

Demographic attributes may be processed for review/ambiguity handling but do not independently authorize a silent merge.

```text
launch patient ID
       +
connector patient ID
       +
source identifiers
       ↓
identity policy
   ├─ unique verified match → attach
   ├─ conflict → block
   └─ demographic similarity only → review
```

## 5. Document / model-assisted extraction flow

Document processing is a separate trust boundary because model/parser output is not authoritative.

```text
clinical document
      ↓
approved parser/model boundary
      ↓
untrusted candidate
  fact type + value + exact quote
      ↓
mechanical source verification
      ↓
terminology/unit/temporal policy
      ↓
ClinicalFact candidate
      ↓
reconciliation + review
```

### Model egress policy

A production deployment must explicitly define:

- whether any model call leaves the provider boundary;
- exact data fields sent;
- processing location;
- provider/subprocessor;
- retention/training guarantees;
- encryption;
- access/logging;
- fallback when the model is unavailable;
- whether local/private model execution is required.

The reference architecture does **not** assume that identifiable clinical documents may be sent to a public model API.

## 6. Control-plane flow

```text
CareOS release pipeline
     ↓
signed/versioned artifact
     ↓
provider deployment validates integrity
     ↓
provider applies release under change control
```

Control plane receives only explicitly approved operational metadata.

Forbidden by default:

- patient names;
- identifiers;
- diagnosis/medication/result text;
- document excerpts;
- free-text clinical prompts;
- raw patient-level audit trails.

## 7. Audit flow

```text
clinical access/action
      ↓
structured audit event
      ├─ actor/user
      ├─ organisation
      ├─ patient reference strategy
      ├─ data category/action
      ├─ source/origin
      ├─ timestamp
      └─ break-glass/elevation context
      ↓
provider-controlled protected audit store / SIEM
```

Production audit must support integrity protection and access separation from normal application administration.

## 8. Break-glass flow

Break glass is not a universal bypass.

```text
normal access denied
      ↓
approved emergency condition
      ↓
user selects break-glass + supplies reason
      ↓
elevated policy decision
      ↓
high-signal audit/alert
      ↓
post-event review according to provider policy
```

## 9. Write-back boundary

Current release policy supports no production write-back.

Future write-back, if justified, requires a separate flow:

```text
prepared action/document
     ↓
human review
     ↓
explicit capability authorization
     ↓
source-system optimistic/version check
     ↓
write
     ↓
source acknowledgement/version
     ↓
audit + reconciliation
```

No read connector is implicitly write-capable.

## 10. Failure data flows

### Source unavailable

```text
connector timeout/error
      ↓
SourceState = unavailable
      ↓
UI shows unavailable/degraded state
```

Never converted into an empty/negative result.

### Source stale

```text
last successful source timestamp exceeds policy
      ↓
SourceState = stale
      ↓
clinician sees stale indicator
```

### Partial page failure

The entire logical search may be rejected rather than displaying silently truncated data as complete.

### Audit unavailable

Required audit failure fails closed according to secure-read policy.

### Identity mismatch

Patient truth is withheld.

## 11. Retention design

CareOS should prefer retrieval and short-lived provider-side caching over creating another permanent longitudinal record.

Each deployment must define:

- what is cached;
- why;
- retention period;
- source-of-truth relationship;
- invalidation/version behavior;
- deletion process;
- backup scope;
- audit retention;
- data-subject-rights handling where applicable.

## 12. Encryption and key boundaries

Production target:

- TLS/mTLS where required for transport;
- encryption at rest;
- provider-/tenant-specific key separation;
- managed KMS/HSM-backed key lifecycle where appropriate;
- secrets outside source code;
- rotation/revocation;
- least privilege for services;
- documented recovery process.

## 13. Data-flow review checklist

Before any live deployment, responsible parties should be able to answer:

- Which exact patient data enters CareOS?
- From which source?
- For which purpose?
- Where is it processed?
- Where is it stored/cached?
- For how long?
- Which subprocessors can access it?
- Which model providers can receive it, if any?
- What identity/treatment-context authorizes access?
- Where is every access audited?
- What happens if source/IdP/audit/model is unavailable?
- How is deletion/retention handled?
- How is the deployment disabled/rolled back?

If any answer is implicit, the deployment is not ready for identifiable patient data.

# CareOS Deployment Patterns

Status: target deployment patterns for architecture/procurement discussion. None of these patterns is a claim of a currently approved live hospital deployment.

## Invariants across all patterns

Every supported deployment preserves the same contracts:

- source systems remain authoritative;
- identifiable patient data is not required in the global control plane;
- patient/encounter identity is explicit;
- access is authenticated + authorised + treatment-context aware;
- clinical facts carry provenance;
- stale/unavailable/unknown are distinct states;
- read and write are separate capabilities;
- model output cannot directly become trusted truth;
- audit is mandatory;
- production live-data mode is gate-controlled.

## Pattern A — Provider on-prem / private infrastructure

```text
Hospital network
  ├─ KIS/LIS/RIS/PACS/PVS
  ├─ hospital IdP
  ├─ hospital SIEM/audit
  └─ CareOS data plane
       ├─ connector gateway
       ├─ clinical truth service
       ├─ terminology adapter/cache
       ├─ policy engine
       └─ clinician web UI

CareOS control plane
  └─ signed release/config metadata only
```

### Advantages

- maximum provider control;
- strongest data-locality story;
- simplest answer to organisations that prohibit external PHI processing;
- direct integration with local identity/audit/network controls.

### Trade-offs

- higher hospital operations burden;
- patching/upgrades depend on local deployment process;
- more difficult cross-site observability without carefully designed non-PHI telemetry;
- hardware/capacity planning is provider-specific.

### Suitable for

- security-sensitive hospital pilots;
- institutions with mature private platform teams;
- environments where cloud processing is not currently acceptable.

## Pattern B — Dedicated provider cloud tenant

```text
Provider systems
      │
   secure interface
      ▼
Dedicated provider tenant
  ├─ connector services
  ├─ clinical truth service
  ├─ policy / SSO integration
  ├─ audit forwarding
  └─ CareOS UI/API

Shared CareOS control plane
  └─ no routine identifiable PHI
```

### Advantages

- strong tenant isolation;
- centralised patching/operations;
- better elastic capacity;
- easier managed backup/recovery/monitoring.

### Trade-offs / required controls

- healthcare cloud legal/security requirements apply where applicable;
- C5/current equivalent evidence and customer-side controls must be evaluated under §393 SGB V where relevant;
- provider must approve processing locations, subprocessors, key management, audit and incident processes;
- tenant isolation must be independently tested.

## Pattern C — Federated managed service

Long-term scale pattern.

```text
                     CAREOS CONTROL PLANE
 signed releases · config schemas · policy packs · non-PHI ops
            │              │              │
      ┌─────┘              │              └─────┐
      ▼                    ▼                    ▼
Provider A data plane  Provider B data plane  Provider C data plane
      │                    │                    │
 local KIS/LIS          local KIS/LIS          local PVS/etc.
      │                    │                    │
 clinical truth         clinical truth         clinical truth
 + audit/policy         + audit/policy         + audit/policy
```

### Advantages

- one platform lifecycle without centralising longitudinal PHI;
- provider-specific data sovereignty;
- repeatable connector and specialty-pack deployment;
- central distribution of validated releases and policies;
- strong fit for multi-hospital scaling if contracts remain stable.

### Required maturity

- signed/reproducible release artifacts;
- provider-isolated secrets/keys;
- strong tenant boundary testing;
- provider-specific audit destinations;
- policy/config version control;
- rollback/kill switch per provider;
- no central dependency that turns all providers unsafe when unavailable.

## Browser / clinician access pattern

CareOS should be a thin web experience running in a **supported, patched browser surface**.

Allowed access surfaces may include:

- managed workstation browser;
- Citrix/VDI/RDS published application/browser;
- managed ward tablet;
- supported mobile browser for approved use cases.

An obsolete workstation OS is not made safe by weakening TLS, browser or authentication requirements. Where legacy desktop hardware cannot run a supported client securely, CareOS should be delivered through a managed modern execution surface such as VDI/Citrix or a managed device.

## KIS embedded/context-launch pattern

Preferred clinician workflow:

```text
clinician authenticates once
          ↓
opens patient in KIS/portal
          ↓
trusted launch context
(user + organisation + patient + encounter + treatment context)
          ↓
CareOS validates binding
          ↓
CareOS opens same patient without second manual search
```

Manual patient search may exist in synthetic demos, but it is not the target production workflow.

## Write-back progression

### Stage 0
No integration, synthetic only.

### Stage 1
Read-only sandbox.

### Stage 2
Read-only shadow/live pilot after gates.

### Stage 3
Only if separately justified: constrained human-confirmed write-back for a specific workflow.

### Never implicit
Read access never automatically grants write access. Autonomous clinical write-back is outside the current release boundary.

## Deployment selection record

Every provider deployment should record:

- selected pattern;
- processing locations;
- source systems/connectors;
- identity provider;
- patient-context mechanism;
- audit destination;
- key/secrets owner;
- retention/cache rules;
- subprocessors;
- backup/restore model;
- RPO/RTO;
- support/escalation owner;
- kill-switch owner;
- approved browser/VDI/device surfaces;
- gate evidence and reviewer approvals.

<!-- paos:reviewed=2026-09-01 -->
# Architecture

## System shape

```text
KIS / EHR · LIS · RIS/PACS · documents · ePA
                       ↓
                reusable adapters
                       ↓
          source-linked clinical context
 identity · provenance · time · lifecycle · freshness
                       ↓
       patient-local graph + deterministic policy
               ↙                   ↘
        role-specific UX         bounded agents/apps
               ↘                   ↙
                    HUMAN AUTHORITY
```

## Architecture purpose

CareOS is a context/interoperability/assurance layer beside existing hospital systems, not a replacement system of record. The architecture protects the distinction between source truth, derived context and agent-generated work.

## Core boundaries

- **source systems:** authoritative clinical inputs;
- **adapters:** normalise access while retaining provenance/lifecycle;
- **patient-local graph:** composes context without erasing origin or freshness;
- **deterministic policy:** enforces state/authority rules outside model discretion;
- **bounded agents/apps:** prepare work but do not create trusted clinical truth;
- **human review:** final clinical authority.

## State model

`NORMAL / DEGRADED / OFFLINE / RECOVERY` are product states, not infrastructure trivia. UI and agents must change behaviour accordingly.

## Decision reversibility

### GREEN

- synthetic fixtures and evaluation expansion;
- reversible UX improvements that preserve trust information;
- internal ranking/summarisation experiments behind existing safety gates.

### AMBER

- new hospital/vendor connector;
- changes to freshness/lifecycle semantics;
- new derived artefact type;
- new agent capability within research scope;
- changes to study protocol after preregistration.

### RED

- production PHI processing/write-back;
- patient identity/linkage model;
- clinical authority rules;
- weakening provenance or reconciliation requirements;
- production deployment into a hospital environment;
- claims of clinical/regulatory validation;
- data retention/security boundaries.

## Reuse strategy

Hospital #100 should increasingly reuse adapter, manifest, assurance and safety knowledge learned from hospitals #1–99. Repeatability is an architecture goal, but it remains unproven until multiple real hospitals/vendors supply evidence.

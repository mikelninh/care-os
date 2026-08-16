# CareOS Architecture Decision Records

Architecture decisions are durable constraints. If a future implementation needs to violate one, the change must create a superseding ADR and trigger architecture/safety review.

| ADR | Decision |
|---|---|
| [ADR-001](ADR-001-system-of-record.md) | CareOS is not the clinical system of record |
| [ADR-002](ADR-002-provider-side-phi.md) | Identifiable clinical data stays provider-side by default |
| [ADR-003](ADR-003-provenance-mandatory.md) | Provenance is mandatory for surfaced clinical facts |
| [ADR-004](ADR-004-models-untrusted.md) | AI/models are untrusted proposers, not truth authorities |
| [ADR-005](ADR-005-failure-semantics.md) | Missing, negative, stale, unavailable and unknown are distinct |
| [ADR-006](ADR-006-read-write-separation.md) | Read and write capabilities are separated |
| [ADR-007](ADR-007-patient-identity.md) | Demographic similarity cannot silently merge patients |
| [ADR-008](ADR-008-composition-not-forks.md) | Scale by composition, not hospital/specialty core forks |
| [ADR-009](ADR-009-national-rails-first.md) | Consume national/EU rails before inventing private equivalents |
| [ADR-010](ADR-010-open-connector-contract.md) | Vendor-specific integrations stay behind an open stable connector contract |
| [ADR-011](ADR-011-agents-delegated-principals.md) | Agents are separately identified, narrowly delegated principals, never human-session proxies |

## ADR template

Every new ADR should include:

- status;
- date;
- context;
- decision;
- consequences;
- rejected alternatives;
- evidence/links;
- supersession relationship if any.

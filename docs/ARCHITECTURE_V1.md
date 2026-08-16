# CareOS Architecture V1 — Superseded

**Status:** superseded on 2026-08-16 by [`ARCHITECTURE_V2.md`](ARCHITECTURE_V2.md).

V1 established the core federated architecture decisions that remain valid:

- CareOS is not the clinical system of record;
- CareOS does not become a national central patient database;
- identifiable clinical data stays provider-side by default;
- source provenance is mandatory;
- source failure/staleness/unknown are explicit;
- national standards are preferred over private replacements;
- specialties/countries/audiences compose around one core.

Do not use this file as the current architecture proposal.

Use instead:

1. [`ARCHITECTURE_V2.md`](ARCHITECTURE_V2.md) — canonical technical architecture;
2. [`GOVERNMENT_REFERENCE_ARCHITECTURE.md`](GOVERNMENT_REFERENCE_ARCHITECTURE.md) — German public-sector proposal;
3. [`TRUST_AND_DATA_FLOW.md`](TRUST_AND_DATA_FLOW.md) — trust/data-flow architecture;
4. [`DEPLOYMENT_PATTERNS.md`](DEPLOYMENT_PATTERNS.md) — supported target deployment patterns;
5. [`NATIONAL_INTEGRATION_MAP.md`](NATIONAL_INTEGRATION_MAP.md) — Germany/EU integration map;
6. [`../architecture/reference-architecture.json`](../architecture/reference-architecture.json) — machine-readable architecture manifest;
7. [`GATES.md`](GATES.md) — actual production-readiness status.

Historical architecture decisions are preserved as explicit ADRs under [`adr/`](adr/README.md).

# CareOS — Architecture

## System shape
`source systems → reusable adapters → source-linked clinical context → patient-local graph + deterministic policy → role UX / bounded agents → human authority`

## Hard boundaries
- source truth remains outside the model;
- identity resolution is deterministic/fail-closed;
- derived work carries provenance and lifecycle state;
- stale derived artifacts become review-required after source correction;
- NORMAL / DEGRADED / OFFLINE / RECOVERY states are explicit;
- agent capabilities are bounded and auditable.

## Existing foundation
- FHIR R4 research read path;
- ISiK/FHIR-oriented validation;
- HL7 v2 ADT/ORU parsing;
- source-linked lifecycle/provenance;
- patient-local graph;
- hospital manifest/preflight/review pack;
- deployment scaffolding.

## Hard-to-reverse choices
Identity, source provenance, clinical authority, access control and lifecycle semantics are RED decisions. Presentation details and bounded workflow UX are more reversible.

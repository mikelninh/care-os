# CareOS Terminology Validation

Status: target architecture / evidence policy. CareOS currently does **not** claim full terminology validation.

## Why ISiK validation is not enough

The pinned gematik ISiK5 reference-validator plugin (`isik5-1.0.4`, package `de.gematik.isik#5.1.3`) explicitly ignores terminology validation for several major code systems, including:

- LOINC;
- SNOMED CT;
- ICD-10-GM;
- ATC;
- OPS;
- KDL;
- ISO/IEEE 11073 code system.

It also ignores several value sets requiring SNOMED/OPS expansion.

Therefore a green ISiK profile-validation result must **never** be described by CareOS as proof that all coded clinical content is semantically valid.

Source of truth for the pinned gap list:
`gematik/app-referencevalidator-plugins/valmodule-isik5/src/main/resources/plugin/config.yaml`

## Evidence model

CareOS tracks profile-validation and terminology-validation evidence separately.

```text
FHIR resource
   ├── profile / structure validation → gematik reference validator
   └── coding / value-set validation  → terminology validation service/process
```

For code systems excluded by the reference validator, `app/terminology_policy.py` requires explicit external validation evidence before CareOS may claim terminology validation.

## Target terminology architecture

For a hospital deployment:

1. preserve original code/system/display from the source;
2. validate code-system membership/version using an approved terminology service or authoritative package;
3. validate required value-set membership where applicable;
4. record terminology server/package/version as evidence;
5. keep local hospital codes separate from normalized concepts;
6. treat uncertain mappings as reviewable mappings rather than silently replacing source coding;
7. version all mappings and make them reproducible for incident/audit review.

## Mapping vs validation

These are separate operations:

- **validation** asks whether a supplied code is valid for a system/value set;
- **mapping** links one coding to another coding/concept.

A valid local code is not automatically a valid LOINC/SNOMED mapping. Mapping confidence and review provenance must be stored separately.

## Production blocker

G2 remains PARTIAL until the first real deployment has an agreed terminology-validation path covering the systems used by the selected clinical workflows and evidence that the actual connector outputs pass it.

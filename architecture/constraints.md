# CareOS — Constraints

## Safety / authority
- no autonomous clinical decisions;
- no derived/model output may silently become clinical source truth;
- unsafe ambiguity must escalate rather than smooth over uncertainty.

## Privacy / security
- production identifiable clinical data is blocked until approved environment, access, privacy and security controls exist;
- data minimisation and patient-local access boundaries are preferred;
- audit and source provenance are mandatory for consequential context.

## Evidence / claims
- synthetic engineering proof must be labelled synthetic;
- a green repository cannot imply clinical validation;
- real clinician, hospital, privacy/security and regulatory evidence are external gates.

## Current blocker
The frozen 500-case synthetic clinical-truth holdout preserves precision/provenance but currently has **26.32% recall with 100% review-case burden**. Production G1 remains blocked.

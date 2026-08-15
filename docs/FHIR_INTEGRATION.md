# CareOS FHIR integration proof

This is an integration test path, **not an ISiK certification claim**.

## Local real FHIR server

CareOS uses the HAPI FHIR JPA starter image as a real FHIR R4 REST server for development.

```bash
docker compose -f integration/docker-compose.fhir.yml up -d
python scripts/seed_fhir.py
FHIR_BASE_URL=http://localhost:8080/fhir uvicorn app.main:app --reload
```

Then call:

```bash
curl http://localhost:8000/api/fhir/capability
curl http://localhost:8000/api/fhir/patients/careos-farid/timeline
```

## Adapter contract

FHIR resources are normalized into the CareOS timeline while retaining `resourceType` and `id` as source provenance.

Current development resources:

- Patient
- AllergyIntolerance
- Condition
- Observation
- MedicationStatement
- Task
- DocumentReference

Next Germany-specific step: install/validate the relevant ISiK implementation-guide packages and run profile validation against the concrete hospital use case. The transport adapter intentionally does not claim that plain FHIR R4 equals ISiK conformance.

## Failure behavior

- FHIR server unavailable → explicit `503`, never stale success.
- Empty resource search → empty list, not fabricated facts.
- Every normalized item keeps the upstream FHIR resource identity.
- Write-back remains disabled in this proof path.

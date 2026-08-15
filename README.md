# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

CareOS is a clinician-first healthcare workflow prototype exploring one question:

**Can software give doctors and nurses meaningful administrative time back without increasing safety risk, correction rate, or cognitive load?**

## V8 — Integration + Stress Lab

V8 keeps the calm clinician experience from V7 and adds the engineering evidence needed to move toward a real hospital pilot:

- **real FHIR R4 adapter path** with a local HAPI FHIR server;
- **500-case gold-label dataset** covering allergies, medication, diagnoses, renal function, follow-ups, discharge, contradictions and provenance;
- **two red-team layers**, including a second unseen holdout created *after* the first hardening pass;
- **production-readiness gates** that deliberately refuse to call the default demo “production ready”;
- **guideline source registry + update watcher** with clinical review before any change can affect displayed guidance;
- separate **Platform Lab** for IT/engineering so complexity does not leak into the clinician UI.

## Clinician experience

1. **See what matters now** — only the few facts that deserve attention.
2. **Keep the source visible** — every surfaced fact can be traced back.
3. **Search one patient history** — KIS, ePA, lab, nursing, fax, calls, letters and scans can appear in one timeline.
4. **Document once** — one captured note prepares documentation, handover, tasks and discharge material for human review.
5. **Fail closed on identity ambiguity** — uncertain patient matching never silently attaches a document.
6. **Measure usefulness** — Pilot Mode records real task time, corrections and cognitive effort.

## Stress test — honest current edge

The original synthetic benchmark was too easy and reached 100%, so it is retained only as a warning against benchmark overfitting.

A first red-team holdout then exposed major failures. After hardening specifically against those attacks, that same suite reached 100%.

To avoid fooling ourselves again, V8 creates a **second unseen holdout after hardening**. Current result on 500 synthetic cases:

| Gold field | Exact accuracy |
|---|---:|
| Allergy | **43.2%** |
| Current medication | **45.0%** |
| Relevant diagnoses | **53.8%** |
| Last renal function | **65.8%** |
| Open follow-ups | **71.0%** |
| Discharge | **61.6%** |
| Contradictions | **74.8%** |
| Provenance object | **3.8%** |

**126 silent contradiction misses** remain in this unseen synthetic holdout.

That is not acceptable for clinical deployment — and that is precisely why the benchmark exists.

Compact reports:

- `data/redteam_before_summary.json`
- `data/redteam_after_summary.json`
- `data/redteam_unseen_summary.json`

The repository includes **100 readable gold cases** in `data/stress_gold_sample_100.jsonl`; `benchmark/generate.py` deterministically generates the full **500-case** benchmark used for the reported run.

> These are synthetic software-engineering benchmarks, **not clinical validation**.

## Real FHIR integration path

CareOS V8 includes a real FHIR R4 transport adapter and a local HAPI FHIR JPA development server.

```bash
docker compose -f integration/docker-compose.fhir.yml up -d
python scripts/seed_fhir.py
FHIR_BASE_URL=http://localhost:8080/fhir uvicorn app.main:app --reload
```

Then:

```bash
curl http://localhost:8000/api/fhir/capability
curl http://localhost:8000/api/fhir/patients/careos-farid/timeline
```

FHIR resources are normalized into CareOS while retaining upstream `resourceType` and `id` as provenance.

**FHIR R4 support is not an ISiK certification claim.** The Germany-specific next step is validation against the relevant gematik ISiK profiles/reference validator for the concrete hospital workflow.

See [`docs/FHIR_INTEGRATION.md`](docs/FHIR_INTEGRATION.md).

## Guideline & evidence layer

CareOS does **not** scrape arbitrary web pages and tell a doctor what treatment to choose.

V8 uses a safer architecture:

```text
official publisher source
        ↓
change detector
        ↓
clinical review queue
        ↓
versioned guidance registry
        ↓
local hospital policy / SOP overlay
        ↓
patient-context reference retrieval
```

Initial registry sources include German NVL/AWMF metadata plus international context such as KDIGO, NICE and WHO SMART Guidelines.

A scheduled GitHub Action watches official source pages for changes. A change opens review work; it is **never auto-applied to patient care**.

See [`docs/GUIDELINE_ARCHITECTURE.md`](docs/GUIDELINE_ARCHITECTURE.md).

## Production security / compliance

The default repo must fail the production-readiness gate.

```bash
curl http://localhost:8000/api/security/readiness
```

The gate checks for production configuration such as OIDC/SSO, audience/issuer validation, audit sink, PHI-safe telemetry, region controls, applicable German cloud evidence, TLS and disabled autonomous clinical write-back.

This is a **configuration gate, not certification or legal advice**.

See:

- [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md)
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
- [`SECURITY.md`](SECURITY.md)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- clinician UI: `http://127.0.0.1:8000/`
- integration/stress dashboard: `http://127.0.0.1:8000/platform`
- API docs: `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest -q
python -m benchmark.redteam_unseen
```

Current V8 baseline: **17 automated tests**.

## Clinician pilot

See [`HUONG_CLINICIAN_TEST.md`](HUONG_CLINICIAN_TEST.md).

North-star hypothesis:

> Can CareOS return **30 minutes of administrative time per clinician per shift** without increasing correction rate, safety risk, or cognitive effort?

This is a hypothesis to test — **not a product claim**.

## Safety status

**Prototype only. Synthetic data only. Not for clinical use.**

CareOS V8:

- performs no production KIS/PVS/EHR writes;
- makes no autonomous treatment or diagnosis decisions;
- does not silently merge ambiguous patient identities;
- preserves provenance as a core contract;
- requires human review for prepared documentation;
- exposes benchmark failures instead of hiding them.

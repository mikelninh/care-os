# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

CareOS is a clinician-first healthcare workflow prototype exploring one question:

**Can software give doctors and nurses meaningful administrative time back without increasing safety risk, correction rate, or cognitive load?**

## V9 — Specialty Packs + Global Composition

V9 keeps the calm clinician experience from V7/V8 and adds a scalable composition model:

```text
CareOS Core
  + Specialty Pack
  + Country Pack
  + Language Pack
  + Audience View
```

That means Infectiology, Oncology and Neurology are **not three separate products**. The same patient truth layer, provenance, security and interoperability core can surface different priorities for each specialty.

### Clinician focus

![CareOS clinician focus](docs/screenshots/clinical-focus.svg)

The default experience remains intentionally quiet: what matters now, where it came from, and what still needs a human.

### Infectiology Pack — first executable specialty pack

![CareOS Infectiology Pack](docs/screenshots/infectiology-pack.svg)

For an infectious-disease team, the first view prioritises:

- specimen + collection time + organism;
- preliminary vs final microbiology;
- susceptibility/resistance;
- current anti-infective therapy **as documented**, not automatically recommended;
- isolation / infection-prevention status;
- relevant devices and insertion dates;
- fever/inflammatory-marker trends;
- pending cultures, screens and follow-ups;
- source provenance on every surfaced fact.

Oncology and Neurology implement the same pack contract. See [`docs/SPECIALTY_PACKS.md`](docs/SPECIALTY_PACKS.md).

## Global architecture

Example compositions:

- `Core + Infectiology + Germany + German + Clinician`
- `Core + Oncology + Germany + English + Clinician`
- `Core + Neurology + Vietnam + Vietnamese + Patient/Family` *(planned V10)*

Clinical facts should remain coded/structured where possible; presentation language is a separate layer. High-risk translations retain the original source text one click away.

For cross-border portability, CareOS treats the **International Patient Summary (IPS)** as a baseline portable patient-summary contract, with country packs adding national identity, terminology, consent, infrastructure and regulatory rules.

See [`docs/GLOBAL_ARCHITECTURE.md`](docs/GLOBAL_ARCHITECTURE.md).

## Audience separation

The same data does **not** mean the same screen or access policy.

- **Clinician** — clinical context necessary for care.
- **Patient & Family** — plain-language timeline, medications, appointments, documents and permissioned sharing *(planned V10)*.
- **Payer / Care Coordination** — purpose-limited minimum dataset only; never a default mirror of the clinician record.

See [`docs/PAYER_VIEW.md`](docs/PAYER_VIEW.md) and [`docs/V10_PATIENT_FAMILY.md`](docs/V10_PATIENT_FAMILY.md).

## Ethical Monetization Agent

CareOS includes an explicit commercial-ethics charter at `/api/monetization/ethical-agent`.

Preferred early models:

1. fixed-price hospital workflow pilots → platform/integration fee only after measured usefulness;
2. simple practice/MVZ subscription without metering safety-critical patient access;
3. public-interest/grant pilots when they accelerate evidence and interoperability;
4. later purpose-bound payer care-coordination programmes — **never sale of patient data or unrestricted record access**.

See [`docs/ETHICAL_MONETIZATION_AGENT.md`](docs/ETHICAL_MONETIZATION_AGENT.md).

## Integration evidence

CareOS includes a real FHIR R4 transport adapter and a local HAPI FHIR JPA development server. GitHub CI starts HAPI, waits for a CapabilityStatement, seeds synthetic resources, and reads them through the CareOS adapter with upstream IDs retained as provenance.

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

**FHIR R4 support is not an ISiK certification claim.** The Germany-specific next step is validation against applicable gematik ISiK profiles and one read-only KIS/vendor sandbox.

See [`docs/FHIR_INTEGRATION.md`](docs/FHIR_INTEGRATION.md).

## Stress test — honest current edge

The original synthetic benchmark was too easy and reached 100%, so it is retained as a warning against benchmark overfitting.

V8/V9 retain a frozen **second unseen 500-case holdout** created after the first hardening pass. Current deterministic extraction result:

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

The next extraction architecture prioritises source-native structured data, schema-constrained document extraction, exact evidence spans, temporal reasoning, unit/terminology normalisation, contradiction detection and explicit `unknown/review` output rather than guessing.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Guideline & evidence layer

CareOS does **not** scrape arbitrary webpages and tell a clinician what treatment to choose.

```text
official publisher source
        ↓
change detector
        ↓
clinical review queue
        ↓
versioned evidence registry
        ↓
local hospital SOP overlay
        ↓
patient-context reference retrieval
```

Specialty bindings now include:

- Infectiology → RKI/KRINKO + AWMF + local SOP;
- Oncology → Onkopedia + AWMF/S3 + local tumour-board SOP;
- Neurology → DGN/AWMF + clearly labelled international context;
- global machine-readable direction → WHO SMART Guidelines where applicable.

A source change opens review work; it is **never silently applied to patient care**.

See [`docs/GUIDELINE_ARCHITECTURE.md`](docs/GUIDELINE_ARCHITECTURE.md).

## Production security / compliance

The default repo deliberately fails the production-readiness gate.

```bash
curl http://localhost:8000/api/security/readiness
```

The gate checks for production configuration such as OIDC/SSO, issuer/audience validation, audit sink, PHI-safe telemetry, region controls, applicable German cloud evidence, TLS and disabled autonomous clinical write-back.

This is a **configuration gate, not certification or legal advice**.

See [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) and [`SECURITY.md`](SECURITY.md).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- clinician UI: `http://127.0.0.1:8000/`
- specialty packs: `http://127.0.0.1:8000/specialty`
- integration/stress dashboard: `http://127.0.0.1:8000/platform`
- API docs: `http://127.0.0.1:8000/docs`

Useful APIs:

```text
GET /api/specialties
GET /api/specialties/infectiology
GET /api/architecture/packs
GET /api/global/ips-preview/farid?language=en
GET /api/monetization/ethical-agent
GET /api/guidelines/sources
GET /api/security/readiness
GET /api/stress/latest
```

## Tests

```bash
pytest -q
python -m benchmark.redteam_unseen
```

Current V9 baseline: **23 automated tests passing locally before publication**. GitHub Actions reruns the suite on the public repository.

## Clinician pilot

See [`HUONG_CLINICIAN_TEST.md`](HUONG_CLINICIAN_TEST.md).

North-star hypothesis:

> Can CareOS return **30 minutes of administrative time per clinician per shift** without increasing correction rate, safety risk, or cognitive effort?

This is a hypothesis to test — **not a product claim**.

## Safety status

**Prototype only. Synthetic data only. Not for clinical use.**

CareOS V9:

- performs no production KIS/PVS/EHR writes;
- makes no autonomous treatment or diagnosis decisions;
- does not silently merge ambiguous patient identities;
- preserves provenance as a core contract;
- requires human review for prepared documentation;
- exposes benchmark failures instead of hiding them.

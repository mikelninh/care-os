# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

CareOS is a clinician-first workflow layer for fragmented healthcare systems.

It is designed to sit **beside** existing KIS/PVS/EHR systems, not replace them: bring together the few patient facts that matter now, keep every fact traceable to its source, surface what is missing or contradictory, and prepare documentation / handover for human review.

## Try it

**Clinician demo:** https://mikelninh.github.io/careos/  
**Chefarzt / pilot view:** https://mikelninh.github.io/careos/chef.html

> Public demos use **synthetic data only** and are not for clinical use.

![CareOS clinician focus](docs/screenshots/clinical-focus.svg)

## Why CareOS

A clinician should not have to reconstruct one patient across KIS, lab, microbiology, nursing notes, PDFs, fax and phone calls.

CareOS asks four questions:

1. **What matters right now?**
2. **Where did it come from?**
3. **What is still missing, contradictory or pending?**
4. **Can this documentation be prepared once and reused safely?**

The north-star hypothesis is measurable:

> **Can CareOS return meaningful administrative time to clinicians without increasing correction rate, safety risk or cognitive effort?**

That is a hypothesis to test — not a product claim.

## Infectiology first

The first executable specialty pack is built around infectious-disease workflow.

![CareOS Infectiology Pack](docs/screenshots/infectiology-pack.svg)

The default view prioritises:

- specimen, collection time and organism;
- preliminary vs final microbiology;
- susceptibility / resistance;
- current anti-infective therapy **as documented**, not automatically recommended;
- isolation / infection-prevention status;
- relevant devices and insertion dates;
- fever / inflammatory-marker trends;
- pending cultures, screens and follow-ups;
- provenance for every surfaced fact.

Oncology and Neurology use the same specialty-pack contract rather than becoming separate products.

See [`docs/SPECIALTY_PACKS.md`](docs/SPECIALTY_PACKS.md).

## One core, many contexts

```text
CareOS Core
   + Specialty Pack
   + Country Pack
   + Language Pack
   + Audience View
```

Examples:

- `Core + Infectiology + Germany + German + Clinician`
- `Core + Oncology + Germany + English + Clinician`
- `Core + Neurology + Vietnam + Vietnamese + Patient/Family` *(planned)*

Clinical facts stay structured where possible; presentation language is a separate layer. High-risk translations retain the original source text.

CareOS also treats the **International Patient Summary (IPS)** as a portable baseline, with country packs adding national identity, terminology, consent and infrastructure rules.

See [`docs/GLOBAL_ARCHITECTURE.md`](docs/GLOBAL_ARCHITECTURE.md).

## Different users, different permissions

The same truth layer does **not** mean everyone gets the same screen or access.

- **Clinician** — clinical context necessary for care.
- **Patient & Family** — plain-language timeline, medications, appointments, documents and permissioned sharing *(planned)*.
- **Payer / Care Coordination** — purpose-limited minimum dataset only; never a mirror of the clinician record.

See [`docs/PAYER_VIEW.md`](docs/PAYER_VIEW.md) and [`docs/V10_PATIENT_FAMILY.md`](docs/V10_PATIENT_FAMILY.md).

## Integration strategy

The adoption path is intentionally incremental:

```text
1. Synthetic browser pilot
        ↓
2. Hospital-internal read-only pilot
        ↓
3. FHIR / ISiK / vendor connector
        ↓
4. Governed write-back only much later
```

CareOS includes a real FHIR R4 transport adapter. GitHub CI starts a HAPI FHIR server, waits for its CapabilityStatement, seeds synthetic resources, and reads them back through the CareOS adapter with upstream resource IDs retained as provenance.

```bash
docker compose -f integration/docker-compose.fhir.yml up -d
python scripts/seed_fhir.py
FHIR_BASE_URL=http://localhost:8080/fhir uvicorn app.main:app --reload
```

**FHIR R4 support is not an ISiK certification claim.** The Germany-specific next step is validation against applicable gematik ISiK profiles and a read-only hospital / KIS vendor sandbox.

See [`docs/FHIR_INTEGRATION.md`](docs/FHIR_INTEGRATION.md).

## We actively try to break it

CareOS includes a frozen **500-case unseen adversarial benchmark** covering:

- allergy;
- current medication;
- relevant diagnoses;
- renal function;
- open follow-ups;
- discharge;
- contradictions;
- provenance.

The current deterministic extractor still fails badly on unseen phrasing, including silent contradiction misses. Those failures are public because they are exactly what must be solved **before** clinical deployment.

The next extraction architecture prioritises source-native structured data, schema-constrained document extraction, exact evidence spans, temporal reasoning, unit / terminology normalisation, contradiction detection and explicit `unknown/review` rather than guessing.

See [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Guideline & evidence layer

CareOS does not scrape arbitrary webpages and tell clinicians what treatment to choose.

```text
official publisher
       ↓
change detector
       ↓
clinical review
       ↓
versioned evidence registry
       ↓
local hospital SOP overlay
       ↓
patient-context reference
```

Source updates never silently change patient-specific behaviour.

See [`docs/GUIDELINE_ARCHITECTURE.md`](docs/GUIDELINE_ARCHITECTURE.md).

## Security and hospital deployment

The public demo is deliberately **synthetic only**.

Real patient data requires a separate deployment gate: supported and patched browser surface, hospital identity / SSO, role and treatment-context authorisation, audit trail, PHI-safe telemetry, encryption, retention rules, incident processes and the applicable German privacy / cloud evidence.

CareOS deliberately fails its production-readiness gate in the default repo.

See [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) and [`SECURITY.md`](SECURITY.md).

## Hospital pilot

The first ask is intentionally small:

> **5–10 clinicians, synthetic cases, ~20 minutes, no patient data, no integration.**

Measure whether CareOS actually reduces search effort, clicks, phone/fax chasing and documentation burden. If there is no clear value, stop. If there is, then evaluate a hospital-internal read-only pilot with IT and Datenschutz.

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
- integration / stress dashboard: `http://127.0.0.1:8000/platform`
- API docs: `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest -q
python -m benchmark.redteam_unseen
```

## Safety status

**Prototype only. Synthetic data only. Not for clinical use.**

CareOS currently:

- performs no production KIS/PVS/EHR writes;
- makes no autonomous diagnosis or treatment decisions;
- does not silently merge ambiguous patient identities;
- keeps provenance as a core contract;
- requires human review for prepared documentation;
- exposes benchmark failures instead of hiding them.

---

### Product thesis

**One patient. One understandable story. Every source preserved. Less hunting, less duplicate documentation, more time for care.**

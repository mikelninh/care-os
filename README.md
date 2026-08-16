# CareOS

> **Patient history without the hunt. Document once, reuse safely.**

## About

CareOS is a clinician-first workflow layer for fragmented healthcare systems.

It is designed to sit **beside** existing KIS/PVS/EHR systems, not replace them: bring together the few patient facts that matter now, keep every fact traceable to its source, surface what is missing or contradictory, and prepare documentation / handover for human review.

**Current focus:** Infectiology first, with reusable specialty packs for Oncology and Neurology, plus country, language, patient/family and care-coordination layers.

## Try it

**Clinician demo:** https://mikelninh.github.io/careos/  
**Chefarzt / pilot view:** https://mikelninh.github.io/careos/chef.html

> Public demos use **synthetic data only** and are not for clinical use.

![CareOS clinician focus](docs/screenshots/clinical-focus.svg)

## Production-readiness status

CareOS does **not** call itself production-ready because a demo works.

It graduates through evidence-backed gates:

| Gate | Status |
|---|---|
| Scope & safety boundary | **EXTERNAL REVIEW** |
| Clinical truth | **BLOCKED** |
| German interoperability | **PARTIAL** |
| Privacy & security | **PARTIAL** |
| Production reliability | **PARTIAL** |
| Regulatory & quality | **EXTERNAL REVIEW** |
| Invisible workflow integration | **PARTIAL** |
| Hospital deployment kit | **PARTIAL** |
| Repeatable multi-hospital deployment | **PARTIAL** |
| National / EU scale | **BLOCKED** |

**No gate is marked PASS yet. Identifiable live patient data remains locked.**

The lock is enforced in code: `CAREOS_DATA_MODE=live-readonly` refuses startup while core gates G0–G5 are incomplete; transactional/write-back mode is unsupported by the current release policy.

See [`docs/GATES.md`](docs/GATES.md), [`docs/SAFETY_CASE.md`](docs/SAFETY_CASE.md) and [`docs/ARCHITECTURE_V1.md`](docs/ARCHITECTURE_V1.md).

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

## Clinical truth architecture

Source systems and extractors do not write directly into the clinician UI.

```text
FHIR / KIS / LIS / documents
             ↓
      untrusted/source adapter
             ↓
    ClinicalFact / TruthEnvelope
             ↓
 provenance · time · status · source
             ↓
 contradiction / review / freshness
             ↓
          clinician view
```

Document/model extraction is explicitly untrusted. A proposed document-derived fact must cite exact character offsets and a verbatim source quote; unsupported/paraphrased evidence is rejected before the fact can enter the truth layer. Ambiguous or unknown facts are routed to review rather than silently presented as confirmed.

See [`app/clinical_truth.py`](app/clinical_truth.py), [`app/document_pipeline.py`](app/document_pipeline.py) and [`docs/BENCHMARK.md`](docs/BENCHMARK.md).

## Integration strategy

The adoption path is intentionally incremental:

```text
1. Synthetic browser pilot
        ↓
2. Hospital network / no-PHI integration proof
        ↓
3. Hospital-internal read-only live-data pilot — only after G0–G5 PASS
        ↓
4. Repeat across another vendor/hospital
        ↓
5. Transactional/write-back programme only if separately justified
```

CareOS includes a real FHIR R4 transport adapter. FHIR data are normalized through the canonical truth layer while retaining resource IDs, resource versions where supplied, and effective/recorded time separately.

FHIR search uses bounded same-origin Bundle pagination: pagination loops, cross-origin continuation and max-page truncation fail closed rather than silently returning partial patient truth.

CareOS also runs a pinned gematik reference-validator workflow against a synthetic ISiK5 Patient fixture. The validator/plugin versions and SHA-256 digests are pinned in CI.

**This is ISiK validation evidence, not a gematik certification/confirmation claim.** A real KIS/LIS/vendor read-only sandbox remains a G2 blocker.

See [`docs/FHIR_INTEGRATION.md`](docs/FHIR_INTEGRATION.md) and [`docs/CONNECTOR_SDK.md`](docs/CONNECTOR_SDK.md).

## Security and privacy architecture

The public demo is deliberately **synthetic only**.

Current hardening includes:

- asymmetric OIDC/JWT verification contract with issuer, audience, expiry and signature checks;
- role/scope/treatment-context authorization;
- short-lived identity/organisation/patient-bound context launch;
- elevated break-glass semantics;
- secure read orchestration that withholds patient truth on authorization failure, source failure/staleness, patient mismatch or required audit failure;
- global / connector-specific runtime kill switches;
- provider-controlled data-plane architecture for identifiable clinical data;
- DSFA/DPIA support, AVV requirements, incident and deployment/rollback dossiers.

Still missing before live PHI: real hospital IdP/context integration, immutable production audit, KMS/secrets/encryption deployment, hospital-specific privacy agreements/approval, applicable German cloud evidence, independent penetration test and the remaining G0–G5 evidence.

See [`docs/HOSPITAL_ASSURANCE_PACK.md`](docs/HOSPITAL_ASSURANCE_PACK.md), [`docs/DATA_FLOW_AND_PRIVACY.md`](docs/DATA_FLOW_AND_PRIVACY.md), [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) and [`SECURITY.md`](SECURITY.md).

## We actively try to break it

CareOS keeps a frozen **500-case unseen adversarial benchmark** covering allergy, medication, diagnoses, renal function, follow-ups, discharge, contradictions and provenance.

The legacy deterministic document extractor still fails badly on unseen phrasing, including critical silent contradiction misses. Those failures remain public and are why **G1 is BLOCKED**.

We are not fixing that by tuning more regexes against the frozen holdout. The replacement architecture is structured-first, source-span verified, versioned, uncertainty-aware and evaluated on untouched holdouts.

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

## Hospital pilot

The first ask remains intentionally small:

> **5–10 clinicians, synthetic cases, ~20 minutes, no patient data, no integration.**

If that demonstrates a real workflow benefit, the next step is not “upload patient data.” It is to complete the assurance/integration gates with hospital IT, Datenschutz, Informationssicherheit and clinical leadership.

The eventual live pilot is measured on time-to-fact, searches/calls/faxes avoided, corrections, provenance, unsupported claims, wrong-patient events, contradiction misses, stale-data handling, review burden and cognitive effort—not on AI usage.

See [`docs/PILOT_MEASUREMENT_PROTOCOL.md`](docs/PILOT_MEASUREMENT_PROTOCOL.md).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Useful endpoints:

- clinician UI: `http://127.0.0.1:8000/`
- specialty packs: `http://127.0.0.1:8000/specialty`
- integration / stress dashboard: `http://127.0.0.1:8000/platform`
- API docs: `http://127.0.0.1:8000/docs`
- gate board: `http://127.0.0.1:8000/api/readiness/gates`
- data-mode lock: `http://127.0.0.1:8000/api/readiness/data-mode`

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
- makes provenance part of the clinical-fact contract;
- distinguishes stale/unavailable from clinically absent;
- requires human review for uncertain/prepared outputs;
- exposes benchmark failures instead of hiding them;
- refuses live-data startup while core assurance gates are incomplete.

---

### Product thesis

**One patient. One understandable story. Every source preserved. Less hunting, less duplicate documentation, more time for care.**

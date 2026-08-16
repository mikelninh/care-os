# CareOS × SJK Infektiologie — end-to-end programme

> Product-research programme, not an official hospital plan or endorsement. Until the live-data gate is opened, all product testing uses synthetic or explicitly approved de-identified data only.

## North-star question

**Can CareOS return meaningful clinician time without making patient information less trustworthy, less current, or harder to audit?**

The programme advances only when the previous stage produces evidence. A senior sponsor cannot waive a safety gate.

---

## Stage 0 — Synthetic team test

**Owner:** product + participating infectiology clinicians  
**System access:** none  
**Data:** synthetic only

### Entry
- public browser prototype works on phone and representative desktop browser;
- all cases visibly labelled synthetic;
- no external patient-data input field;
- test tasks and measurement sheet ready.

### Test
5–10 clinicians independently complete repeated tasks:
1. identify what changed;
2. distinguish preliminary/final/pending;
3. find documented anti-infective treatment;
4. identify open follow-up;
5. open the supporting source;
6. prepare a handover.

### Evidence collected
- completion time;
- wrong answers;
- missed pending items;
- source opens;
- navigation/click count;
- corrections;
- perceived effort 1–5;
- would-use-tomorrow yes/no;
- top five facts needed before a typical round;
- current calls/searches/logins/copy-paste that could disappear.

### Exit
Proceed only if clinicians can explain the product without coaching and identify repeated real work it could remove.

### Stop
- users cannot tell pending from negative;
- source/provenance is misunderstood;
- the interface adds more work than it removes;
- the team says the selected workflows are not important.

---

## Stage 1 — Workflow map and sponsor decision

**Owner:** clinical sponsor + product  
**System access:** none  
**Data:** no patient records required

Map one shift end to end:

`morning board -> ward round -> results chase -> microbiology -> orders/tasks -> handover -> day-clinic/ASV/consult continuity`

For each repeated task capture:
- trigger;
- current system/source;
- human steps;
- duplicate entry;
- phone/fax/manual chase;
- latency;
- risk if missed;
- owner;
- candidate CareOS intervention.

### Exit evidence
A one-page workflow baseline and Chefarzt decision:

**YES** to a read-only technical discovery, or **NO** with the reason documented.

No request for clinical production access yet.

---

## Stage 2 — IT / Datenschutz / security discovery

**Owner:** hospital IT/architecture + Informationssicherheit + Datenschutz, with product  
**System access:** architecture/test-environment information only

Resolve the ten questions in `SJK_INTEGRATION_DISCOVERY.md`:
- KIS;
- LIS/microbiology;
- RIS/PACS;
- documents;
- ISiK/FHIR/vendor interfaces;
- IdP/SSO;
- patient/encounter context launch;
- browser/Citrix/VDI reality;
- audit/SIEM/hosting constraints;
- accountable governance owners.

### Required outputs
- hospital-specific data-flow diagram;
- proposed read-only connector;
- authoritative patient/encounter identifiers;
- source freshness/version semantics;
- authentication/authorization design;
- approved test hosting boundary;
- named reviewers;
- pilot stop/rollback path.

### Stop
Do not move forward if patient identity, access context, audit, freshness or processing boundary cannot be made explicit.

---

## Stage 3 — Synthetic/de-identified technical sandbox

**Owner:** interoperability + hospital IT  
**System access:** approved sandbox/test tenant  
**Data:** synthetic, or formally approved de-identified test data

Start with one narrow read slice:
- Patient / Encounter identity;
- microbiology result + lifecycle status;
- selected lab results;
- medication record / documented anti-infectives;
- tasks/pending diagnostics where available;
- document/report references.

### Technical acceptance
- same upstream IDs preserved;
- pagination/partial-state visible;
- source versions/timestamps preserved;
- `pending`, `final`, `corrected`, `stale`, `unavailable` distinguishable;
- patient-context mismatch fails closed;
- no write capability;
- kill switch tested;
- source outage never becomes an empty/normal patient state;
- ISiK/FHIR/profile and terminology evidence kept separate.

### Exit evidence
A reproducible technical run plus failure-injection report.

---

## Stage 4 — Assurance review

**Owner:** independent qualified reviewers + hospital accountable functions

Parallel reviews:

### Clinical safety
- intended use;
- known hazards;
- unsafe ambiguity;
- human-review points;
- stop thresholds.

### Datenschutz
- purpose/legal basis determined by responsible parties;
- data minimisation;
- DSFA/DPIA as required;
- AVV/DPA and subprocessors where applicable;
- retention/deletion;
- rights and transparency process.

### Security
- real SSO/IdP;
- role + treatment-context authorization;
- central protected audit;
- encryption/KMS/secrets;
- vulnerability/SBOM programme;
- independent penetration test;
- backup/restore and incident response.

### Regulatory / quality
- independent MDR/MDSW qualification/classification;
- AI Act/EHDS applicability assessment;
- classification-appropriate quality/risk/change lifecycle.

### Exit
G0–G5 must be evidence-backed PASS before identifiable live-data mode can start.

---

## Stage 5 — Shadow workflow study

**Owner:** clinical lead + evaluation lead  
**Clinical authority:** existing systems/workflows only

CareOS runs without changing care decisions or writing to the KIS. Outputs are compared against the approved source workflow.

### Measure
- fact retrieval accuracy;
- source/provenance correctness;
- freshness;
- critical silent misses;
- review burden;
- time to required information;
- corrections;
- usability/cognitive load.

### Stop thresholds
Immediate stop for:
- wrong-patient attachment;
- unsupported critical clinical claim;
- hidden stale/unavailable source state;
- access-control/audit failure;
- any incident the clinical safety lead judges unacceptable.

---

## Stage 6 — Limited live read-only pilot

**Scope:** one department, named users, narrow workflows, fixed duration.  
**Write-back:** disabled.

The clinician opens the patient in the normal workflow. CareOS should receive trusted patient/encounter context and display source-grounded context without a second patient search.

### Primary endpoint
**Clinician minutes returned per completed target workflow, with no increase in critical errors/corrections.**

### Secondary endpoints
- searches/clicks/logins avoided;
- calls/manual chases avoided;
- pending items successfully surfaced;
- source-open rate;
- review burden;
- effort score;
- weekly active use;
- would-continue-use.

### Exit
Go/no-go based on measured benefit and safety, not enthusiasm.

---

## Stage 7 — Repeatability proof

Deploy the same core into a second independent environment/vendor without forking CareOS clinical truth.

Differences should remain in:
- connector configuration;
- mappings;
- local workflow/SOP overlays;
- permissions;
- specialty pack configuration.

If Hospital B requires a bespoke clinical core, G8 fails.

---

## Stage 8 — Scale

Only after repeatability:
- additional SJK/Joseph Kliniken workflows/departments where appropriate;
- second/third hospitals;
- ambulatory/PVS path;
- ePA/TI/KIM/ISiP interfaces where justified;
- national/EU interoperability obligations;
- independent health-services evaluation;
- payer/public funding based on measured outcomes, never patient-data monetisation.

## Programme scoreboard

| Stage | Current state |
|---|---|
| 0 Synthetic team test | **READY TO RUN** |
| 1 Workflow map / sponsor | **READY AFTER TEAM FEEDBACK** |
| 2 IT/Datenschutz discovery | **PACK READY, PEOPLE NOT YET ENGAGED** |
| 3 Technical sandbox | **BLOCKED ON ACTUAL SJK/VENDOR INTERFACES** |
| 4 Assurance review | **GENERIC PACK READY, EXTERNAL/HOSPITAL REVIEW MISSING** |
| 5 Shadow study | **LOCKED** |
| 6 Live read-only pilot | **LOCKED BY G0–G5** |
| 7 Repeatability | **BLOCKED** |
| 8 Scale | **BLOCKED** |

CareOS graduates by evidence, not by calendar date or version number.

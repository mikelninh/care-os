# Hospital Discovery Workshop — 60 minutes, no PHI

Purpose: create the **first real hospital capability manifest** and expose wrong assumptions before asking for system access.

This is not an approval meeting and not a product demo. Do not request patient data, credentials or secrets.

## Minimum participants

- clinical workflow owner / clinician;
- hospital IT / integration owner;
- privacy or data-protection representative;
- security/CISO representative where feasible;
- optional procurement/operations owner.

## Output

By the end, we should have a non-secret draft containing:

- actual workflow boundary and owner;
- named systems and vendor/product/version where known;
- source types used in the workflow;
- interface types actually available (FHIR/ISiK, HL7 v2, documents, vendor API, other);
- identity/patient-context mechanism;
- read/write boundary;
- network/auth ownership;
- environments that may be available (test/sandbox/deidentified/shadow);
- data-protection/security reviewers and required review artifacts;
- operational owner, stop/rollback expectations;
- unknowns, contradictions and bespoke work.

## Agenda

### 0–10 min — real workflow archaeology

Ask the clinician to narrate one recent normal case without patient-identifying details:

1. What starts the task?
2. Which systems/screens/documents are opened?
3. Where do changed/pending results appear?
4. Where does the clinician manually reconcile information?
5. Which step causes calls/messages/searching/copy-paste?
6. What mistake or missed pending item would be dangerous?
7. What is the real end state of the task?

Do not show CareOS until this baseline is understood.

### 10–25 min — system map

For every source:

| Question | Capture |
|---|---|
| System | product/vendor/name |
| Version | exact if known |
| Owner | team/role |
| Data used | categories, no PHI examples |
| Interface | FHIR/ISiK/HL7v2/API/document/other |
| Patient context | how identity/encounter is selected |
| Lifecycle | preliminary/final/corrected/cancelled available? |
| Availability | normal outages/partial-read behavior |
| Test path | sandbox/deidentified/test environment? |

### 25–35 min — CareOS boundary

Show only the narrow target:

- read-only source-linked context;
- no autonomous diagnosis/treatment;
- no hidden write-back;
- pending/unavailable preserved;
- human remains authority;
- synthetic/deidentified first.

Ask: **Which assumption is wrong in your hospital?**

### 35–50 min — review path

Map actual required reviewers and what each needs:

- Clinical / patient safety
- Datenschutz / DPO
- Security / CISO
- IT integration
- Betriebsrat / workforce where applicable
- Procurement / Legal
- Operations / support
- Regulatory/quality where applicable

For each:

`owner -> question -> evidence needed -> who can verify -> prerequisite -> can run in parallel?`

### 50–60 min — smallest next proof

Choose exactly one:

1. synthetic clinician sessions only;
2. real non-secret capability manifest;
3. approved vendor/test sandbox;
4. deidentified interface sample;
5. governed shadow evaluation preparation.

Do not jump to live identifiable data because the demo is compelling.

## Red flags to record, not solve away

- no reliable patient-context mechanism;
- vendor interface differs from documentation;
- corrected/preliminary lifecycle not available;
- read-only access still exposes excessive data;
- no test environment;
- unclear system owner;
- review path depends on undocumented personal knowledge;
- procurement/licensing forbids intended use;
- workflow benefit disappears after necessary verification;
- critical integration requires write authority.

## Definition of done

The workshop is complete when:

- at least one current workflow is mapped end-to-end;
- system/vendor/version unknowns are explicit;
- no secrets/PHI were captured;
- every blocker has an owner or is explicitly owner-unknown;
- the next smallest safe evidence step is chosen;
- `proof/EVIDENCE_LEDGER.yaml` is updated with supported/falsified/blocked/unknown findings.

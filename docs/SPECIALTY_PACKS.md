# Specialty Packs

CareOS V9 separates clinical specialty logic from the core platform.

```text
CareOS Core
  + Specialty Pack
  + Country Pack
  + Language Pack
  + Audience View
```

A specialty pack controls **priority, vocabulary, questions, workflow templates, evaluation cases and guideline-source bindings**. It does not create a separate patient record and must not silently change treatment.

## Infectiology Pack (first executable pack)

Priorities:
- microbiology specimen + collection time + organism;
- susceptibility / resistance and whether result is preliminary/final;
- current antimicrobials and source;
- infection prevention / isolation state;
- relevant devices and insertion dates;
- fever / inflammatory marker trends;
- pending cultures, screens and follow-ups;
- source provenance on every displayed fact.

Guideline/evidence bindings start with RKI/KRINKO, AWMF and local hospital SOPs.

## Oncology Pack

Priorities include diagnosis/stage, pathology/molecular findings, therapy cycle, toxicity, response, tumor-board dependencies and follow-up. Germany-source candidates include Onkopedia and AWMF/S3 guidance plus local tumor-board SOPs.

## Neurology Pack

Priorities include neurological baseline, change from baseline, imaging, medication context, functional status, cognition/seizures where relevant and unresolved follow-up. Germany-source candidates include DGN/AWMF, with international sources clearly labelled when used.

## Rule

A pack changes **what CareOS surfaces first**, not what exists in the underlying record. Missing or ambiguous safety-critical data is shown as unknown/review rather than guessed.

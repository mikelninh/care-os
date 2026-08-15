# Guideline & evidence architecture

CareOS does **not** scrape arbitrary web pages and then tell a doctor what to do.

```text
official publisher sources
        ↓
source watcher (change detection only)
        ↓
clinical review queue
        ↓
verified, versioned guidance metadata
        ↓
local hospital policy / SOP overlay
        ↓
patient-context retrieval
        ↓
Guideline context with source + version + date
```

For Germany, the source hierarchy is configurable but starts with applicable law/binding rules and local SOPs, then German national/specialty guidance such as NVL/AWMF where applicable, then international specialty guidance such as KDIGO or NICE as transparent context.

A changed publisher page creates a **review event**, not a clinical recommendation. Reviewers confirm version, effective date, changed recommendations and local applicability. Old versions remain immutable for audit and reproducibility. Conflicting current guidance is shown as a conflict; CareOS does not invent a consensus.

V8 displays **reference context** only. Patient-specific diagnosis or treatment recommendations would require a separate intended-purpose, clinical-risk, validation and regulatory assessment.

WHO SMART Guidelines are useful architectural inspiration because they treat digital guideline implementation as structured artifacts rather than just PDFs.

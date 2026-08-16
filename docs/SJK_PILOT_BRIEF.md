# CareOS × SJK Infektiologie — synthetic pilot brief

> Product-research proposal only. Not an official Joseph Kliniken Berlin document or endorsement. No real patient data is required for this stage.

## The ask

Run a short synthetic usability/workflow test with 5–10 people from the infectiology team.

- no patient data
- no KIS access
- no installation
- no clinical decision automation
- browser-based synthetic cases
- 15–20 minutes per participant

The purpose is not to ask whether the interface looks nice. It is to test whether CareOS could remove repeated information hunting from real infectious-disease work.

## What we test

1. **Morning board:** find overnight changes and critical pending items.
2. **Ward round:** reconstruct microbiology + documented anti-infective therapy + organ-function trend + devices + hygiene state.
3. **Result chase:** tell pending/resulted/stale/unavailable apart.
4. **Microbiology story:** reconstruct specimen → organism → preliminary/final → susceptibility over time.
5. **Handover:** create a concise source-linked handover without losing unresolved items.
6. **Day clinic / ASV:** carry relevant prior context into follow-up without duplicate history work.
7. **Consult / hotline:** assemble the minimum useful context for an infectious-disease consult.
8. **AMS review:** reconstruct the documented antimicrobial/microbiology course without autonomous treatment advice.

## What we measure

- task completion time
- clicks/searches
- source opens
- corrections
- missed pending items
- calls/manual chases the clinician believes the workflow would still require
- effort score (1–5)
- would-use-tomorrow (yes/no)

### Initial product bar

These are hypotheses, not validated clinical thresholds:

- clear reduction in retrieval effort across repeated tasks
- no increase in corrections
- no safety-critical item hidden because data was pending/stale/unavailable
- every surfaced clinical claim has provenance
- users understand uncertainty without training

If those are not true, we fix the product before asking IT for integration.

## What the team should challenge

- Which five facts matter before almost every ward round?
- What is missing from the screen?
- What is distracting or too loud?
- Which data can safely be summarized and which must be shown verbatim?
- Which pending result is most dangerous to lose track of?
- Where does the current workflow require a phone call, fax, CD, second login, or manual copy/paste?
- Which local SOP/hygiene context should appear at the point of work?
- What must CareOS never automate?

## If the synthetic test earns a next step

Then — and only then — invite:

- clinical leadership
- representative physicians
- nursing leadership
- hospital IT / architecture
- information security
- Datenschutz
- hygiene/AMS stakeholders where appropriate

The next ask is a **read-only technical discovery**, not production and not write-back.

# CareOS Independent Review Packet

Purpose: invite experts to **find reasons CareOS should not advance yet**.

Reviewer feedback is evidence of critique, not institutional approval unless the reviewer explicitly has that authority.

## Send reviewers only what they need

Start with:

1. `README.md` — 5-minute orientation;
2. `docs/CURRENT_STATUS_AND_GAPS.md` — current truth boundary;
3. `docs/CLAIM_EVIDENCE_MATRIX.md` — falsifiable claims;
4. generated hospital review pack if reviewing a real non-secret manifest;
5. one narrow workflow demo / synthetic study.

Do not overwhelm them with the whole repository.

## Review A — clinician / clinical safety

Ask:

1. Is the intended first workflow clinically meaningful or artificial?
2. Which information/state could CareOS present dangerously even if technically source-linked?
3. Does `pending / unavailable / preliminary / corrected` match clinical mental models?
4. What would make you stop a shadow evaluation immediately?
5. Is our Definition of Done for the first workflow correct?
6. Which error classes are missing?
7. Where could source provenance create false reassurance rather than trust?
8. What must be independently measured before any real workflow use?

Output:

- severity-ranked findings;
- missing safety cases;
- corrected workflow/DoD;
- advance / redesign / stop recommendation for synthetic external study only.

## Review B — privacy + security

Ask:

1. Is the proposed data scope actually minimal for the intended workflow?
2. Which data-flow or processor/subprocessor fact is missing?
3. Which identity/role/treatment-context assumption is unsafe?
4. Could provenance/audit itself leak sensitive data?
5. What evidence would you require before approving a sandbox or shadow evaluation?
6. Which retention/deletion/backup path is underspecified?
7. What attacker/failure mode is missing from the threat model?
8. Is the read-only boundary technically enforceable rather than contractual only?

Output:

- required evidence list;
- unacceptable assumptions;
- minimum controls for next environment;
- explicit non-approval statement unless reviewer is institutionally authorised.

## Review C — hospital IT / integration

Ask:

1. Which source/interface assumptions are unrealistic?
2. Can our capability manifest represent your actual environment without secrets?
3. How is patient/encounter context really resolved?
4. What does FHIR/ISiK expose versus what still comes through HL7v2/documents/vendor-specific paths?
5. How are corrections/retries/outages represented in reality?
6. What work is configuration versus custom engineering?
7. What would be the smallest approved sandbox path?
8. What would make deployment #2 easier than deployment #1 — or why would it not?

Output:

- corrected system map;
- named vendor/version where allowed;
- sandbox candidate;
- bespoke-work estimate;
- top 5 integration risks.

## Review D — regulatory / quality

Only after intended use and deployment context are fixed enough to review.

Ask:

1. Is the intended use stated narrowly enough to classify responsibly?
2. Which claims create medical-device / AI / clinical-safety implications?
3. What quality/risk/change-control evidence is missing?
4. Which human factors/usability evidence is necessary?
5. Which changes would require reassessment?
6. What may CareOS safely claim today, and what wording should be prohibited?

Do not ask the reviewer to “certify” the project informally.

## Finding format

Every finding should become a durable record:

```yaml
id: EXT-001
review_type: clinical_safety
severity: critical | high | medium | low | observation
claim_affected: C1-workflow-useful
finding: "..."
evidence_seen:
  - "..."
recommended_action: "..."
status: open | accepted | disputed | resolved
owner: "role/team"
verification_needed: "what proves resolution"
```

## Advancement rule

A review is valuable when it changes something: a claim weakens/strengthens, a gate opens/closes, a test is added, or an assumption becomes explicitly unknown.

A meeting that ends only with “looks interesting” is not evidence.

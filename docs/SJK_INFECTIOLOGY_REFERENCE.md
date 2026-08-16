# SJK Infektiologie reference environment

> **Status:** synthetic product-research reference only. This is not an official St. Joseph Krankenhaus / Joseph Kliniken Berlin system, endorsement, deployment, or integration. No real patient data belongs in the public demo.

CareOS uses the Klinik für Infektiologie at St. Joseph Krankenhaus Berlin-Tempelhof as the first concrete reference environment for workflow design and later real-world evaluation.

## Publicly documented context

The current Joseph Kliniken Berlin website describes the infectiology service as including:

- Station 21 (inpatient)
- Station 21a / Tagesklinik and ASV-Ambulanz
- a 24/7 physician hotline
- HIV-associated disease/AIDS
- acute infectious diseases
- infective endocarditis
- periprosthetic/device-associated infections
- infections in immunosuppression
- antimicrobial-stewardship interventions

A publicly available historic PJ report describes a ward rhythm containing a morning bed meeting, ward round, review/request of findings and diagnostic planning, followed by case discussion. This is useful product-research evidence, not an authoritative current workflow specification.

## Product hypothesis

The first useful CareOS deployment should not try to solve all hospital work. It should make the repeated reconstruction of an infectious-disease patient's current story substantially faster and safer.

For a typical case, CareOS should help answer:

1. What changed overnight?
2. What microbiology exists, from which specimen and when?
3. Is each result preliminary, final, pending, stale, or unavailable?
4. What antimicrobial treatment is documented as current?
5. What relevant organ-function trend is available?
6. What devices/foci matter?
7. What isolation/hygiene state is documented?
8. What remains unresolved before the next decision or handover?
9. What exact source supports every surfaced statement?

CareOS must not make autonomous treatment recommendations in this reference scope.

## Eight workflows to test

| Workflow | What CareOS should remove | Primary metric |
|---|---|---|
| Morning board | overnight chart reconstruction | time-to-correct-priority |
| Ward round | repeated source hunting | searches/clicks + correction rate |
| Result chase | manual pending-result tracking | calls/faxes/manual chases |
| Microbiology story | chronology reconstruction | time + wrong-source rate |
| Handover | duplicate summary writing | preparation time + omissions |
| Day clinic / ASV | repeated history reconstruction | duplicate documentation |
| Consult / hotline | missing context in referrals | follow-up calls + answer time |
| AMS review | antimicrobial/microbiology reconstruction | source completeness + time |

## First team test

Use only synthetic cases. Give each clinician the same tasks without explaining the UI first.

Record:

- baseline time using their normal mental/workflow model (estimated initially; measured later in an approved environment)
- CareOS completion time
- clicks/searches
- source opens
- corrections
- missed pending items
- perceived effort (1-5)
- "would you use this tomorrow?" yes/no

Then ask:

- Which five facts do you need before almost every ward round?
- Which results are hardest to find or chase?
- Which information is most dangerous when stale or incomplete?
- Which systems/windows do you open for a normal case?
- Which local SOP or hygiene context needs to appear at the point of work?
- What must CareOS never automate?

## Promotion criteria

Do not pursue real-data integration because people say the demo is nice.

The next stage is justified only if the team repeatedly demonstrates that CareOS can reduce information-retrieval/coordination effort while maintaining provenance and without increasing correction burden.

Before any real patient data: G0-G5 remain release gates and the hospital-specific IT, Datenschutz, Informationssicherheit and clinical-safety review must be completed.

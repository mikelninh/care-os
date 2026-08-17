# SJK Infectiology — Synthetic CareOS Agent A/B Study

Status: **synthetic product research only**. No patient data. Not an official SJK study or hospital endorsement.

Public study surface: `https://mikelninh.github.io/careos/sjk/ab.html`

## Question

Does a source-linked CareOS morning-review draft reduce information-reconstruction work **without increasing errors, omissions, automation bias or reduced source verification**?

The study is deliberately designed so **speed alone cannot win**.

## Participants

Start with one clinician as a usability sanity-check, then target **5–10 complete paired clinician sessions** if locally appropriate and voluntarily agreed.

Use pseudonymous participant codes such as `P01`. Do not collect names, real patient information, answer transcripts or free-text clinical cases in the study tool.

## Study design

Each participant completes exactly two rounds:

- `careos`: normal source-linked CareOS synthetic case;
- `careos-agent`: same difficulty family plus an explicitly labelled **untrusted source-linked draft**.

Two synthetic cases (`case-a`, `case-b`) and four deterministic sequences counterbalance:

- condition order;
- case order;
- case × condition assignment.

The participant code is hashed locally to select one of the four sequences. The Python analysis layer independently reproduces the same assignment and rejects mismatched or duplicated rows.

This means incomplete sessions are visible but **never included in the estimated agent effect**.

## Facilitator instruction

Do not teach the interface.

Read only:

> „Beide Fälle sind vollständig synthetisch. Orientiere dich kurz vor der Visite so, wie du es intuitiv tun würdest.“

Then start the page and let the clinician work.

## Tasks in each round

Ask the clinician to identify:

1. microbiology established vs preliminary/pending;
2. documented anti-infective treatment — explicitly **not a recommendation**;
3. current hygiene/isolation status;
4. the most important open/pending items;
5. source(s) supporting the answer;
6. a concise verbal handover.

## Automatically recorded locally

- condition;
- case;
- order position;
- task seconds;
- number of source opens.

## Observer records only structured fields

- wrong answers;
- missed pending items;
- corrections after source review;
- answer/handover accepted without source checking yes/no;
- pending interpreted as negative/complete yes/no;
- documented treatment interpreted as a CareOS recommendation yes/no;
- agent draft confused with source truth yes/no;
- effort 1–5;
- would-use-tomorrow yes/no.

The page intentionally provides **no free-text answer field** and sends **no study result to a server**. The observer explicitly exports JSON or CSV after the session.

## Primary safety/UX metric — verification decay

`verification_decay = unverified acceptance rate with agent - unverified acceptance rate without agent`

Positive verification decay is a warning signal: the draft may be making clinicians less likely to inspect source evidence.

Also report paired `agent - control` deltas for:

- task seconds;
- wrong answers;
- missed pending items;
- source opens;
- corrections;
- effort.

Only complete within-participant pairs contribute to these deltas.

## Hard safety-stop events

Any of the following overrides a favorable time result and produces `evidence_status = safety-stop`:

- pending/unavailable interpreted as negative or complete;
- documented treatment interpreted as a CareOS recommendation;
- agent draft confused with source truth.

Other important redesign signals include increased wrong answers, increased missed pending items, lower source inspection, increased correction burden or increased cognitive effort.

## Aggregate many exported sessions

Each completed browser session exports one participant CSV. Aggregate any number of local exports reproducibly:

```bash
python scripts/summarize_sjk_agent_ab.py \
  pilot/exports/P01.csv \
  pilot/exports/P02.csv \
  pilot/exports/P03.csv \
  pilot/exports/P04.csv \
  pilot/exports/P05.csv \
  --output data/sjk_agent_ab_report.json
```

The summarizer:

- validates required fields and data types;
- independently recomputes the participant's counterbalanced assignment;
- rejects duplicate/extra rounds;
- excludes incomplete participants from paired effects;
- preserves incomplete-session counts as an evidence-quality signal;
- never generates an automatic go decision.

## Evidence status

- `<5` complete pairs → `insufficient-complete-pairs`;
- any hard stop → `safety-stop`;
- `>=5` complete pairs with no hard stop → `ready-for-clinician-review`.

`ready-for-clinician-review` is **not** an automatic success. Quantitative evidence and clinician qualitative feedback must still be reviewed together.

## Six qualitative questions after the full A/B session

Ask verbally; do not enter real clinical material into the tool.

1. Was any statement too confident?
2. What did you verify immediately, and why?
3. What would you never want summarized without opening the source?
4. Where should CareOS abstain rather than help?
5. Would this remove a real call/search/window switch in your morning workflow?
6. What is the biggest risk if this becomes normal routine?

## Decision rule

**Faster is not better if errors, missed pending work, recommendation confusion or unverified acceptance increase.**

Code support:

- `app/agent_study.py`
- `scripts/summarize_sjk_agent_ab.py`
- `share/sjk-infectiology/ab.html`

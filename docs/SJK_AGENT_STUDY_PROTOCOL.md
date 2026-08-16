# SJK Infectiology — Synthetic CareOS Agent A/B Study

Status: synthetic product-research protocol. No patient data. Not an official SJK study or hospital endorsement.

## Question

Does a source-linked CareOS morning-review agent reduce information-reconstruction work **without increasing errors, omissions, automation bias or reduced source verification**?

## Participants

Start with Huong alone for usability sanity-check, then target 5–10 Infectiology clinicians if locally appropriate and voluntarily agreed.

Use participant codes only. Do not collect patient information or free-text clinical cases.

## Conditions

A. CareOS synthetic case without agent-prepared draft.  
B. Same difficulty family with CareOS + source-linked agent draft.

Counterbalance order where possible so learning does not automatically favor B.

## Tasks

For each condition ask the clinician to identify:

1. microbiology established vs preliminary/pending;
2. documented anti-infective treatment (not recommendation);
3. current hygiene/isolation status;
4. the most important open/pending items;
5. source(s) supporting the answer;
6. a concise handover.

Do not teach the interface first beyond saying it is synthetic and not for clinical use.

## Record

- task seconds;
- wrong answers;
- missed pending items;
- number of source opens/checks;
- corrections after source review;
- whether agent output was accepted without source checking;
- effort 1–5;
- would-use-tomorrow yes/no.

## Safety/UX metric: verification decay

`verification_decay = unverified acceptance rate with agent - unverified acceptance rate without agent`

A faster agent is not a success if clinicians inspect sources materially less, errors increase, or pending items are missed.

## Stop signals

Stop/redo the workflow if any clinician:

- interprets pending/unavailable as negative because of the agent;
- believes agent text is a treatment recommendation;
- cannot distinguish agent draft from source truth;
- misses a safety-critical pending item introduced by the agent view;
- reports the interface increases cognitive burden or makes uncertainty less clear.

## Qualitative questions after tasks

- Was any statement too confident?
- What did you verify immediately, and why?
- What would you never want an agent to summarize without opening the source?
- Where should the agent abstain rather than help?
- Would this save a call/search/window switch in your actual morning workflow?
- What is the biggest risk if this becomes normal routine?

## Decision

No automatic pass. Review quantitative and qualitative evidence together with a clinician safety owner before changing the next phase.

Code support: `app/agent_study.py`.

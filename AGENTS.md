# AGENTS.md — CareOS

## Mission
Return time to care without making clinical information less trustworthy. Build source-linked, bounded clinical context tooling for research and synthetic evaluation while keeping clinical truth, patient safety and real-world authority outside the model.

## Start here
1. Read `README.md`.
2. Read `.harness/project.json`.
3. Read `.harness/active-task.json` and `.harness/HANDOFF.md`.
4. For safety-relevant work, read the exact release, gate and agent-security documents that govern the change.

## Source-of-truth map
- Product status and proof boundary: `README.md`
- Current gaps: `docs/CURRENT_STATUS_AND_GAPS.md`
- Release assurance: `docs/RELEASE_ASSURANCE.md`
- Production gates: `docs/GATES.md`
- Claim/evidence mapping: `docs/CLAIM_EVIDENCE_MATRIX.md`
- Agent security: `docs/AGENT_SECURITY_MODEL.md`
- Clinical study protocol: `docs/TIME_RETURNED_TO_CARE_STUDY.md`
- Runtime: `app/`
- Architecture: `architecture/`
- Benchmarks/evidence: `benchmark/`, `proof/`
- Interoperability: `compatibility/`
- Deployment scaffolding: `deploy/`, `Dockerfile`
- Current work state: `.harness/`
- CI truth: `.github/workflows/`

## Contract before work
Every substantial task must define:
- goal
- authoritative sources
- outputs
- constraints
- done criteria
- forbidden actions
- risk class
- retry budget
- next owner

Do not silently redefine a clinical claim, promote a research result, or hide a failing safety metric.

## Roles
- Chief: triage, decompose, route, collect. Does not make clinical decisions.
- Scout: retrieves source evidence, standards and research material. Read-only by default.
- Builder: creates code, mappings, UX and synthetic artefacts in an isolated workspace.
- Verifier: independently checks safety invariants, tests, benchmarks, provenance and claims.
- Operator: performs only approved external/deployment actions after policy gates.

## Action classes
- A0 Observe — read/search/analyse. Automatic.
- A1 Local reversible — draft/test/edit isolated synthetic work. Automatic.
- A2 Shared reversible — branch, PR, preview, issue. Logged; normally automatic.
- A3 Consequential — publish, deploy, send, write to external systems. Human approval required.
- A4 High-impact — identifiable patient-data access/egress, clinical write-back, patient-care actions, destructive production changes, clinical/regulatory claims. Explicit approval plus stronger independent verification; many A4 actions remain forbidden by current project status.

Trust the action class, not the agent personality.

## Four clinical correctness invariants
1. Pending is not negative.
2. Unavailable is not absent.
3. Documented therapy is not an AI recommendation.
4. Agent draft is not source truth.

Treat violations as harness failures, not wording problems.

## Verification
Minimum harness check:
`python scripts/harness_check.py`

Project-specific verification comes from the relevant workflow under `.github/workflows/` plus the safety/release docs above.

Never claim a test, benchmark, compatibility path or clinical metric passed unless it actually ran or was directly observed and its evidence is captured.

## Durable state
The conversation is not the system of record.
Keep current work in `.harness/active-task.json`.
Keep handoff context in `.harness/HANDOFF.md`.
Keep accepted run receipts in `.harness/receipts/`.

Memory may preserve preferences; current patient/context data, evidence, clinical rules, compatibility, holdout results, release gates and deployment state must be re-opened from authoritative sources.

## Handoffs
A handoff must state status, current step, evidence, decisions, failures/uncertainties, open risks, next owner and exact next action.

Safety-relevant work may not be passed as chat-only context.

## Retries
Use bounded local repair loops. Default maximum: 3 attempts.
If the same failure repeats twice, stop and improve the sensor, fixture, source rule, gate or escalation path.

## Failure upgrades
- missing clinical context -> source/provenance requirement
- pending treated as negative -> invariant regression test
- unavailable treated as absent -> availability-state test
- draft treated as truth -> authority/provenance gate
- missed contradiction -> contradiction sensor/gold case
- poor holdout metric -> keep release blocked; improve evidence/system
- repeated loop -> retry cap/escalation
- unsafe action -> permission gate
- lost decision -> durable state
- unknown failure -> trace/evidence capture

Never improve the copy to conceal a blocked gate.

## Hard boundaries
- Research/synthetic evaluation only under current project status; not for clinical use.
- No production clinical write-back under the current release boundary.
- The model may propose structure; it does not create trusted clinical truth.
- Human authority remains outside the model.
- Missing or unavailable evidence must stay explicit.
- The current frozen holdout blocker may not be relabelled as production readiness.
- No named KIS/LIS compatibility claim without approved real-environment evidence.
- Synthetic/deidentified evidence is never identifiable-patient production evidence.
- Identifiable patient data, credentials and secrets never belong in harness state or receipts.

## Definition of done
Work is done only when contract criteria are evidenced, provenance and uncertainty remain visible, relevant safety/release gates still hold, rollback/next step is known, and any required human or independent approval is recorded.

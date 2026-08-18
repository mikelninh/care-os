## What problem does this solve?

Describe the workflow friction, failure mode or contributor need in a few sentences.

## What changed?

Keep this concrete and reviewable.

## Show the evidence

What demonstrates the change?

- [ ] test / regression fixture
- [ ] screenshot or interaction proof, where relevant
- [ ] benchmark / measurement, where relevant
- [ ] documentation updated, where relevant

Links / notes:

## Safety check

Most PRs only need a quick pass here. Check anything this change can affect:

- [ ] patient / encounter binding
- [ ] provenance / source evidence
- [ ] pending / stale / unavailable / contradictory state
- [ ] model / prompt / extraction behaviour
- [ ] agent tool scope / authorization / egress
- [ ] clinical write capability
- [ ] PHI / privacy / logging / telemetry
- [ ] FHIR / ISiK / connector behaviour
- [ ] none of the above

If you checked any safety-sensitive area, explain the failure mode and regression evidence:

## Honest boundary

What does this PR **not** prove?

Examples: synthetic-only, no real hospital integration, formative UX only, no production load evidence.

## Contributor checklist

- [ ] I used synthetic data only.
- [ ] I did not add secrets, credentials or private hospital/vendor material.
- [ ] I did not silently turn missing/unavailable/pending into a reassuring negative state.
- [ ] I did not give the model new authority without deterministic controls.
- [ ] If I changed a clinical/safety invariant, I added a regression test.
- [ ] The claim in the PR matches the evidence.

<details>
<summary><strong>Deeper assurance / gate impact — only if relevant</strong></summary>

### Readiness gates

Does this change evidence or blockers for G0–G9?

- Gate(s):
- Previous status:
- Proposed status:
- Evidence:

> A code change alone is not sufficient to mark an assurance gate PASS.

### High-risk review questions

1. Can this create or hide a wrong-patient fact?
2. Can unavailable/stale data become a reassuring empty state?
3. Can a model-derived claim bypass provenance/evidence verification?
4. Can conflicting sources be silently resolved?
5. Can a read-only deployment reach a write capability?
6. Does any new identifiable data leave the provider boundary?
7. Is the action auditable and reversible?

</details>

Thank you for helping make clinical software calmer, safer and more useful. ❤️

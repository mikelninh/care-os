# Harness handoff

## Status
Ready for independent verification.

## Current step
Run the harness gate and existing CareOS safety/release workflows.

## Evidence
- `AGENTS.md` makes clinical invariants and release boundaries part of the root operating map.
- `.harness/project.json` records the research-only / no-writeback / G1-blocked boundary.
- `scripts/harness_check.py` mechanically rejects malformed tasks, unapproved A3/A4 receipt actions and accidental weakening of the current release-boundary flags.
- `.github/workflows/harness.yml` makes the minimum harness continuously testable.

## Decisions
- CareOS gets a stricter harness because errors can become safety-relevant even before production.
- The current failing holdout/release blocker is a fact to preserve, not a marketing problem to rewrite.
- Builder and Verifier stay separate for clinical logic and release claims.
- Patient data never enters repository harness state.

## Failures / uncertainties
CI evidence is pending.

## Open risks
Harness v0.1 validates process and safety-boundary invariants; it does not provide clinical validation, regulatory approval or real-hospital evidence.

## Next owner
Verifier — run the branch workflows, inspect any failure, and upgrade the sensor/gate rather than weakening the acceptance criterion.

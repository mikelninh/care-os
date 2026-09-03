# Harness handoff

## Status
Verified and accepted for merge.

## Current step
Merge PR #62. The harness gate, existing CareOS tests and CodeQL all passed on the implementation commit.

## Evidence
- Harness workflow `33744829375`: success.
- Test workflow `33744829063`: success.
- CodeQL workflow `33744829056`: success.
- `AGENTS.md` makes clinical invariants and release boundaries part of the root operating map.
- Acceptance receipt: `.harness/receipts/harness-v0.1-adoption.json`.

## Decisions
- CareOS gets a stricter harness because errors can become safety-relevant even before production.
- The current failing holdout/release blocker is a fact to preserve, not a marketing problem to rewrite.
- Builder and Verifier stay separate for clinical logic and release claims.
- Patient data never enters repository harness state.

## Failures / uncertainties
None observed in the harness, repository tests or CodeQL for this change.

## Open risks
Harness v0.1 validates process and safety-boundary invariants; it does not provide clinical validation, regulatory approval or real-hospital evidence.

## Next owner
Operator — merge the verified PR, then use a fresh task contract for the next CareOS change.

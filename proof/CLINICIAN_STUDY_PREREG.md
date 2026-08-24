# Clinician Study Preregistration — Sprint 1

Freeze this document before participant `P001` begins. Changes after first participant must be appended under **Protocol deviations**; do not silently edit the original hypothesis.

## Study type

Internal product/usability evaluation using **synthetic cases only**. It is not clinical validation and does not authorize live patient-data research. If the intent changes to publish generalisable research or use real patient/workflow data, obtain the institutionally appropriate ethics/privacy/governance review first.

## Primary question

For physician morning review + documentation preparation, does CareOS reduce task time/friction while preserving correctness, pending-work detection and source verification?

## Participants

Target: 5–10 clinicians for the first workflow family, with mixed experience levels where feasible.

Use pseudonymous participant IDs only. Do not export participant names, patient data or free-text from real cases.

## Design

Paired, counterbalanced, matched synthetic cases:

- odd participant IDs: baseline A -> CareOS B;
- even participant IDs: CareOS A -> baseline B.

A valid pair must use different matched variants and order positions 1 and 2.

## Primary outcomes

Per observation:

- elapsed task seconds;
- correct task completion;
- missed pending items;
- wrong answers;
- unsupported claims;
- source opens / verification behavior;
- corrections;
- context switches / searches / copy-paste;
- cognitive effort 1–5;
- explicit safety stops.

## Safety gate

Any of the following blocks a positive claim for the affected pair/set:

- wrong patient;
- increased missed pending work;
- unsupported consequential claim;
- stale/preliminary information treated as current/final;
- draft mistaken for clinical recommendation;
- material verification collapse.

Speed never overrides this gate.

## Directional success threshold

Do not publish/highlight a directional result for this workflow until:

- >= 5 complete safe pairs;
- both order directions represented;
- every pair uses distinct matched variants;
- zero safety-stop events in the highlighted set;
- no increase in correction burden that negates the time result;
- individual-pair distribution shown alongside median/aggregate.

Product targets such as >=90% task success, lower median time, median cognitive effort <=2/5 and >=80% willingness-to-reuse are **targets to test**, not prior results.

## Baseline integrity

The baseline condition must be credible enough to represent the current task. If participants say it is unrealistically difficult/easy, record this as a protocol limitation rather than interpreting the CareOS delta as real-world time savings.

## Session script

1. Explain synthetic-only nature in <=20 seconds.
2. Do not teach navigation beyond what a first-time user would reasonably receive.
3. Start timing when the task is visible.
4. Observe; do not rescue unless the participant is blocked beyond useful observation.
5. Record interventions as protocol events.
6. End timing at the predefined task completion point.
7. Ask only the five debrief questions in `CLINICIAN_TEST.md`.

## Analysis

Use the existing aggregator. Report:

- each pair;
- median and range;
- safety/correctness outcomes;
- source-check behavior;
- cognitive effort;
- participant friction themes;
- protocol deviations.

Do not convert a tiny synthetic usability sample into a clinical-effectiveness claim.

## Stop / redesign criteria

Pause the current workflow hypothesis if:

- any repeatable safety misunderstanding appears;
- clinicians cannot identify pending/uncertain state;
- source verification meaningfully drops;
- the baseline comparison is invalid;
- users repeatedly say the task does not reflect real work;
- time savings depend on skipping necessary verification.

## Protocol deviations

None at preregistration.

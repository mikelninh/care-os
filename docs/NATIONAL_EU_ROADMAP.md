# CareOS Germany / EU Scale Roadmap

Status: architecture/programme roadmap. It is not a claim that the listed national/EU integrations are implemented.

## Principle

CareOS should become a high-quality **consumer and orchestration layer of public interoperability rails**, not a private replacement for them.

The national architecture remains federated: provider systems and legally governed patient infrastructure remain authoritative; CareOS turns distributed information into a source-grounded workflow context.

## Germany — hospital lane

Target sequence:

1. applicable ISiK modules/profile validation;
2. real KIS/LIS read-only vendor sandbox;
3. hospital identity/treatment-context integration;
4. source freshness/version reconciliation;
5. repeat across at least two materially different KIS/vendor environments;
6. write capability remains a separate programme.

## Germany — ambulatory lane

After hospital repeatability:

- map PVS integration options and relevant KBV/gematik information models;
- preserve the same `ClinicalFact + SourceState` contract;
- test GP/specialist workflows separately rather than reusing hospital attention priorities;
- avoid requiring a second patient search/login.

## Germany — nursing / care lane

Evaluate applicable ISiP interfaces and care-specific workflow packs independently from ISiK. Do not assume hospital profiles or clinician UX transfer directly into nursing/care settings.

## ePA / TI / KIM lane

For each use case answer before building:

1. Is this information already available through the treatment/provider primary system?
2. What legal/technical basis permits CareOS to access it?
3. Is CareOS acting through a provider primary system, another approved component, or a patient-authorized path?
4. Which source remains authoritative?
5. What identity/patient-presence/treatment-context proof is required?
6. What audit/logging obligations apply?

Do not connect to a national rail merely to claim integration; connect only where it removes a measured workflow gap.

## Patient portability

Use the International Patient Summary as a portable baseline where appropriate, while preserving richer local source/provenance. A portable summary is not a replacement for the full German clinical record.

## EHDS preparation

Maintain an explicit mapping for the then-current European Health Data Space requirements that affect:

- EHR interoperability components;
- logging components;
- priority data categories;
- technical documentation/conformity obligations where CareOS falls in scope;
- patient rights/access flows;
- cross-border exchange.

The mapping must be versioned by law/specification date. G9 does not pass from a conceptual mapping alone; implementation evidence is required where CareOS is in scope.

## National operating model

A Germany-scale deployment would require more than software:

- maintained standards/profile compatibility matrix;
- certified/assured hosting and security operating model as applicable;
- connector/vendor partnership programme;
- clinical safety governance;
- Datenschutz and incident-response capability;
- release/change-control governance;
- support model for hospitals/practices;
- independent outcome evaluation;
- transparent national impact scorecard.

## National impact scorecard

Track verified, auditable outcomes rather than AI usage:

- clinician minutes returned;
- median time to required fact;
- searches/calls/faxes/manual chases avoided;
- duplicate documentation avoided;
- provenance coverage;
- critical silent miss rate;
- wrong-patient rate;
- stale-data misrepresentation;
- false-alert/review burden;
- correction rate;
- availability/freshness;
- adoption by workflow/specialty/site.

National extrapolations must always show the measured base effect, eligible population, adoption assumption and sensitivity range.

## G9 pass condition

G9 can only pass when the relevant national/EU paths used by CareOS are implemented and validated, an operating/governance model exists, and multi-site evidence shows the architecture scales without centralizing unnecessary PHI or bypassing national infrastructure.

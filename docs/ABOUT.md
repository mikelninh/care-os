# CareOS — About

CareOS is a clinician-first workflow layer for fragmented healthcare systems.

It helps care teams answer four questions quickly:

1. What matters for this patient right now?
2. Where did that information come from?
3. What is still missing, contradictory, or pending?
4. Can documentation and handover be prepared once and reused safely?

The current prototype focuses on Infectiology, with specialty packs for Oncology and Neurology, while keeping the core architecture reusable across countries, languages, and audience views.

## Current status

- Browser-based clinician demo
- Mobile-first Infectiology pack
- Synthetic data only in public demos
- Real FHIR R4 integration tested in CI
- 500-case adversarial stress benchmark
- Human review for ambiguous patient identity and derived documentation
- No autonomous diagnosis, treatment recommendation, or production EHR write-back

## Live demo

Clinician demo: https://mikelninh.github.io/careos/

Chefarzt / pilot view: https://mikelninh.github.io/careos/chef.html

## Product thesis

**Patient history without the hunt. Document once, reuse safely.**

CareOS is not intended to replace a KIS/PVS/EHR. It is designed to sit beside existing systems, connect progressively, preserve provenance, and prove whether it actually gives clinicians time back without increasing safety risk or cognitive burden.

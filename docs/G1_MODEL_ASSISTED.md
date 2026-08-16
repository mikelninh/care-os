# G1 next generation — evidence-first model-assisted extraction

Holdout #3 showed the current conservative extractor has the desired **precision/abstention direction** but unacceptable recall/review burden. The next move is not to add rules from that holdout. It is to change the extraction architecture while keeping the same truth firewall.

## Non-negotiable trust boundary

A model is a **proposal engine**, never a clinical truth engine.

`document -> model proposals -> exact evidence resolution -> schema validation -> ClinicalFact -> reconciliation`

The model may propose:
- clinical fact type;
- logical concept key;
- original value;
- exact supporting quote;
- code/system candidate;
- unit label;
- source maturity candidate;
- confidence;
- explicit unknown/review.

The model may **not** directly decide:
- character offsets;
- patient identity;
- clinical effective time from unsupported text;
- which conflicting source wins;
- whether a stale/unavailable source means a negative finding;
- treatment or diagnosis recommendations;
- production write-back.

## Evidence admission

`EvidenceFirstModelExtractor` requires the proposed quote to exist **exactly once** in the immutable source text.

Rejected:
- missing quote;
- paraphrased quote;
- repeated/non-unique quote;
- model-proposed effective date without deterministic temporal normalization;
- unknown/ambiguous assertion without review reason.

Accepted proposals still pass the normal `VerifiedExtractionPipeline` exact source-span verification.

## Model/provider independence

The clinical truth layer must not depend on a specific provider. `ModelProposer` is an interface so deployments can use:
- a hospital-approved local model;
- an approved private-cloud model;
- an approved external provider under the required data-processing controls;
- deterministic extraction for sources that do not need a model.

Changing provider/model does not change reconciliation semantics.

## Fresh-development protocol

Holdout #3 is historical and must not be consulted for feature/rule/prompt selection.

The next development corpus should be designed from **independent source-format dimensions**, for example:
- section/header variation;
- tables vs prose vs key/value;
- multi-document chronology;
- corrected/finalized report lifecycle;
- negation and historical-vs-current language;
- exported document typography;
- clinically equivalent unit variants;
- source duplication/corroboration;
- explicit unresolved/partial documents.

The corpus must be labelled before prompt/model iteration begins.

## Development metrics

Track separately:
- field precision/recall/F1;
- unsupported claims;
- provenance coverage;
- wrong-source rate;
- effective-time accuracy once temporal normalization exists;
- review/abstention rate;
- false-review burden;
- unresolved-source barriers;
- contradiction detected/review/silent;
- latency and cost per document;
- model/schema rejection rate.

## Advancement bar

Do not freeze the next holdout until:
- development recall is high enough that clinicians would not review nearly every case;
- precision/provenance remain close to the safety target;
- prompt/model changes are versioned;
- deterministic reconciliation tests remain green;
- failure cases route to review rather than unsupported certainty.

The next frozen holdout is evaluated once. It is evidence, not a leaderboard.

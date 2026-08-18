# CareOS Claim → Evidence → Next Proof Matrix

Baseline: **18 August 2026**

Purpose: make every important CareOS claim inspectable and falsifiable.

Statuses:

- **TESTED SYNTHETICALLY** — executable code + synthetic tests/evidence exist;
- **IMPLEMENTED CONTRACT** — behavior/interface exists but real environment evidence is missing;
- **RESEARCH HYPOTHESIS** — architecture/product claim to test;
- **EXTERNAL EVIDENCE REQUIRED** — cannot be honestly upgraded from the repository alone;
- **BLOCKED** — known evidence currently fails the target.

> A stronger-looking sentence is not a stronger claim. A claim upgrades only when the next evidence layer exists.

---

| Claim | State today | Evidence today | What would falsify/undermine it | Next proof required |
|---|---|---|---|---|
| Pending is not silently treated as negative | **TESTED SYNTHETICALLY** | clinical truth/lifecycle tests, demos, golden journey | downstream UI/agent collapses pending to no finding | clinician sessions + real-source lifecycle cases |
| Unavailable source is not treated as absence | **TESTED SYNTHETICALLY** | source-state, hospital-runtime, resilience tests | partial/outage response allows reassuring negative conclusion | real source outage/partial-read exercise |
| Patient boundaries fail closed | **TESTED SYNTHETICALLY** | cross-patient truth/graph/runtime/agent denial tests | any connector/agent can return/use another patient's data without hard stop | real identity/context-launch tests + independent security review |
| Model cannot grant itself authority | **TESTED SYNTHETICALLY** | gateway/delegation/tool-proxy/red-team tests | compromised worker can change patient/tool/operation/egress/effect scope | production tool inventory behind deterministic proxy + independent red team |
| Clinical source correction reopens dependent derived work | **TESTED SYNTHETICALLY** | graph + artifact invalidation + golden journey | corrected/superseded fact leaves dependent unsigned draft looking current | real delayed/corrected result shadow observation |
| Recovery reconciles before normal operation | **TESTED SYNTHETICALLY** | resilience/recovery/golden journey tests | reconnect alone restores normal capability before missed-state reconciliation | target-hospital downtime/recovery exercise |
| Signed human records are not silently rewritten | **TESTED SYNTHETICALLY** | artifact invalidation contract/tests | correction mutates signed artifact without governed workflow | real document/EHR integration behavior |
| CareOS patient explanation preserves source truth/state | **TESTED SYNTHETICALLY** | patient view + teach-back contracts | explanation/translation replaces original wording or hides pending state | patient/family usability + governed access integration |
| Cross-provider follow-up is modeled as acknowledged state, not fire-and-forget | **IMPLEMENTED CONTRACT** | care coordination state machine/tests | real transport cannot preserve identity/purpose/status or organisation rejects workflow | real KIM/FHIR/vendor transport pilot |
| FHIR R4 read path exists | **TESTED SYNTHETICALLY** | FHIR connector/runtime + tests | real vendor capability/profile behavior incompatible with assumptions | approved vendor/hospital sandbox |
| ISiK-oriented path exists | **TESTED SYNTHETICALLY / VALIDATION PATH** | FHIR runtime + ISiK-oriented validation CI | real ISiK implementation exposes incompatible profile/behavior | real German hospital/vendor ISiK evidence |
| Trusted MPI/source-ID resolution can be deterministic and fail closed | **TESTED SYNTHETICALLY / IMPLEMENTED CONTRACT** | patient ID resolver + hospital runtime tests | real resolver returns ambiguous/stale mappings CareOS cannot represent safely | approved hospital MPI/EMPI adapter integration |
| CareOS has production-ready generic HL7 v2 integration | **DO NOT CLAIM** | narrow ADT/ORU parser only | transport/profile/network/retry assumptions fail | real interface-engine transport + profile/vendor conformance |
| Narrow HL7 v2 ADT/ORU parsing can preserve lifecycle/source identity | **TESTED SYNTHETICALLY** | `hl7v2_connector.py` tests | malformed/retry/corrected messages produce silent wrong state | real interface-engine/vendor sandbox |
| Hospital capability discovery can be productised | **RESEARCH HYPOTHESIS + IMPLEMENTED SCAFFOLD** | manifest, FHIR discovery, preflight | real deployments require mostly undocumented custom discovery | first two real hospital manifests + measured discovery/custom hours |
| Hospital review documentation can be generated from non-secret configuration | **TESTED SYNTHETICALLY** | review-pack generator + secret-pattern tests | required reviewer information cannot be represented or secrets leak into output | DPO/CISO/hospital IT review feedback |
| Upgrade promotion can be evidence-gated and rolled back | **TESTED SYNTHETICALLY / IMPLEMENTED CONTRACT** | upgrade + rollout controller tests | target platform cannot observe/rollback safely enough | target-environment canary/rollback game day |
| Compatibility knowledge can reduce repeated integration work | **RESEARCH HYPOTHESIS + IMPLEMENTED REGISTRY** | typed evidence classes/version matching | site-to-site differences remain mostly bespoke despite same vendor/version | two+ real compatible deployments; custom-hours/reuse measurement |
| Hospital #N becomes easier than hospital #1 | **EXTERNAL EVIDENCE REQUIRED** | architecture + registry/conformance model only | deployment #N requires similar bespoke core work | second/third real site with measured integration economics |
| CareOS returns time to care | **EXTERNAL EVIDENCE REQUIRED** | study protocol/runner/aggregator + targets only | paired users are not faster, verification drops or safety stops increase | ≥5 safe counterbalanced synthetic pairs for one role/workflow, then governed real study |
| Current physician workflow target is useful | **RESEARCH HYPOTHESIS** | Infectiology demo + synthetic task design | users say it duplicates work, cannot orient, distrust sources or miss pending work | real synthetic physician sessions |
| Clinical truth layer is production-useful | **BLOCKED** | frozen 500-case holdout: precision/provenance strong, recall 26.32%, review 100% | current evidence already shows unusable recall/review burden | fresh development corpus + better frontier + user behavior + real source variation |
| Production PHI security is adequate | **EXTERNAL EVIDENCE REQUIRED** | architecture, locks, reference controls only | provider identity/network/audit/KMS/tenant controls fail review/test | hospital controls + DPIA/DPA where applicable + pentest + operations evidence |
| Production agent reliability is adequate | **EXTERNAL EVIDENCE REQUIRED** | synthetic agent/eval/red-team path | real traffic/model/tool/provider failure modes escape controls | production-grade identity/egress/audit + model/provider traces + incidents/evals |
| CareOS is clinically validated | **DO NOT CLAIM** | none | — | appropriately governed clinical/human-factors evidence for fixed intended use |
| CareOS is regulatory approved/certified | **DO NOT CLAIM** | none | — | formal intended-use classification + required conformity/quality process |
| 24/7 SLA can be offered | **DO NOT CLAIM** | operating-model design only | staffing/target exercises absent | real staffed on-call + target SLO/incident/recovery evidence |
| CareOS can scale nationally | **RESEARCH HYPOTHESIS** | German/EU architecture + open contracts | procurement/governance/vendor/systemic-risk model does not work | multi-site evidence + national institutional participation |
| CareOS/global contract can be open/reversible rather than another lock-in | **RESEARCH HYPOTHESIS** | Apache-2.0 + endgame governance/exit requirements | another implementation cannot replace CareOS without rebuilding everything | independent compatible implementation + real provider exit/migration demonstration |

---

# Evidence ladder

```text
unit/property test
→ composed synthetic regression
→ real synthetic user behavior
→ approved deidentified/vendor sandbox
→ shadow observation
→ bounded read-only use
→ second vendor / second hospital
→ target-environment security/operations evidence
→ independent assurance
→ multi-site operating history
→ exit/migration proof
→ national/cross-border evidence
```

No claim may borrow credibility from a later rung.

---

# Reviewer shortcut

If you want to challenge CareOS, start with the weakest high-value claims:

1. **G1 clinical truth usefulness** — current benchmark is deliberately blocked.
2. **Time Returned to Care** — no participant result should exist before real synthetic sessions.
3. **Real hospital interoperability** — no named KIS/LIS compatibility claim without sandbox evidence.
4. **Repeatability** — no platform-scale claim before hospital B.
5. **Production security/operations** — design is not provider evidence.
6. **Endgame governance** — open-source code is not automatically neutral infrastructure.

A useful review should try to falsify these rather than reward the amount of code.
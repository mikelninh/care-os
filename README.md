# CareOS 🏥

**Return time to care — without making clinical information less trustworthy.**

CareOS is a clinician-first **context, interoperability and assurance layer** that sits beside existing hospital systems. It composes source-linked patient context and makes that context safely usable by people and bounded AI applications.

**[Clinical review demo →](https://mikelninh.github.io/careos/clinical.html)** · **[One patient end to end →](https://mikelninh.github.io/careos/journey.html)** · **[Synthetic study →](https://mikelninh.github.io/careos/study.html)**

**Research / synthetic evaluation only · not for clinical use · no production write-back**

## The problem

Healthcare workers still act as human middleware between KIS/EHR, LIS, RIS/PACS, documents, ePA, calls and messages.

CareOS explores a stable layer above those systems rather than replacing them:

```text
KIS / EHR · LIS · RIS/PACS · documents · ePA
                       ↓
                reusable adapters
                       ↓
          source-linked clinical context
 identity · provenance · time · lifecycle · freshness
                       ↓
       role-specific UX + bounded agents/apps
                       ↓
                    human authority
```

The north star is **Time Returned to Care — safety gated.**

## What to try

1. **Clinical review** — inspect changed, pending and critical context with sources attached.
2. **One patient journey** — follow source → draft → outage → correction → recovery → human review.
3. **Synthetic paired-study surface** — see how the project intends to measure time, errors and verification behaviour.

The intended question is not “is this a nice AI demo?” It is:

> **Can clinicians spend less time hunting, reconciling and copying information without losing provenance, uncertainty or control?**

## Four correctness invariants

1. **Pending ≠ negative.**
2. **Unavailable ≠ absent.**
3. **Documented therapy ≠ AI recommendation.**
4. **Agent draft ≠ source truth.**

The model may propose structure. It does **not** become the authority that creates trusted clinical truth.

## What is implemented

- source-linked clinical lifecycle and provenance
- patient-local graph + stale-artifact invalidation
- bounded agent/tool authority and adversarial scenarios
- NORMAL / DEGRADED / OFFLINE / RECOVERY states
- patient/family source-linked experience
- interactive human clinical review UX
- FHIR R4 research read path
- ISiK/FHIR-oriented validation path
- HL7 v2 ADT/ORU parsing for synthetic/deidentified inputs
- hospital manifest / preflight / review-pack tooling
- Docker/Helm deployment scaffold
- synthetic Time Returned to Care study machinery

## Agent safety model

```text
untrusted model proposal
        ↓
deterministic Agent Gateway
patient · encounter · task · tools · operations · budgets
        ↓
trusted Tool Proxy
        ↓
source-linked result
        ↓
untrusted draft
        ↓
human review
```

The model cannot grant itself a new patient, tool, operation or effect authority.

## The blocker we do not hide

The frozen 500-case synthetic clinical-truth holdout currently preserves precision/provenance but reaches only **26.32% recall with 100% review-case burden**.

Therefore **production G1 remains blocked**.

That means CareOS should not be presented as clinically validated, production-ready or ready to make patient-care decisions. The next step is better external evidence, not stronger copy.

## Real-world proof ladder

```text
synthetic tests
   ↓
real clinicians on synthetic cases
   ↓
independent clinical / privacy / security / IT critique
   ↓
real non-secret hospital capability map
   ↓
approved vendor / deidentified sandbox
   ↓
governed shadow workflow
   ↓
bounded read-only pilot
   ↓
second hospital / second vendor
```

The first workflow to prove is **physician morning review + documentation preparation**.

A speed gain is not a win if source verification, error rate or safety gets worse.

## Integration truth

| Path | Current state |
| --- | --- |
| FHIR R4 read | implemented research runtime |
| ISiK / FHIR read | runtime + validation path |
| HL7 v2 ADT/ORU parsing | synthetic/deidentified connector |
| Real HL7 v2 transport | external evidence required |
| Vendor API | contract only |
| Live transactional/write | blocked by release policy |

No named KIS/LIS compatibility claim is made without a real approved environment.

## What is not proven

CareOS is not currently:

- clinically validated
- approved for identifiable patient-data production use
- proven to save clinician time
- proven interoperable with a named production KIS/LIS
- proven repeatable across hospitals
- regulatory approved/certified
- a 24/7 clinical service

## Deep review

- [Release assurance](docs/RELEASE_ASSURANCE.md)
- [Current status and gaps](docs/CURRENT_STATUS_AND_GAPS.md)
- [Claim → evidence matrix](docs/CLAIM_EVIDENCE_MATRIX.md)
- [Production gates](docs/GATES.md)
- [Agent security model](docs/AGENT_SECURITY_MODEL.md)
- [Real-world proof campaign](proof/README.md)
- [Clinical study protocol](docs/TIME_RETURNED_TO_CARE_STUDY.md)

---

**Keep systems of record. Standardize trustworthy context above them.**

*Models may interpret and propose. Evidence, authority and safety boundaries remain outside the model.*

Built by [Michael Ninh](https://mikelninh.github.io/) in Berlin.

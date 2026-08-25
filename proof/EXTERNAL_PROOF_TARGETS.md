# External Proof Targets — ordered by evidence value

This is a target map, not evidence that any organisation has agreed to participate.

## 1. Real clinicians — synthetic paired sessions

**Ask:** 20–30 minutes, no patient data, complete the same bounded workflow baseline vs CareOS.

**Evidence produced:**
- observed task time;
- correctness/pending detection;
- verification behavior;
- friction/cognitive effort;
- workflow realism;
- falsifiable UX/safety findings.

**Why first:** can start without hospital system access and directly tests the highest-value user claim.

## 2. Charité CEED — clinical usability / proof-of-concept critique

Public service description: https://ceed.charite.de/

CEED publicly describes usability/UX testing, proof-of-concept studies, regulatory support and access to clinical expertise.

**Ask:** critique the CareOS first workflow and advise on the smallest realistic usability/PoC path.

**Evidence sought:**
- professional clinical usability assessment;
- human-factors gaps;
- realistic next study design;
- regulatory/clinical-practice constraints.

## 3. Charité Institute of Medical Informatics / EVIDOC — implementation-science critique

Public project: https://medinfo.charite.de/en/research/ag_clinical_implementation_science_in_digital_health_cidh/evidoc/

EVIDOC studies how AI-supported documentation can be integrated effectively and sustainably into clinical routine, including workflow effects and implementation conditions.

**Ask:** challenge the Time Returned to Care protocol and implementation assumptions; identify what would count as meaningful evidence.

**Evidence sought:**
- study-design critique;
- workflow/implementation factors missing from CareOS;
- external falsification of time-savings assumptions;
- advice on what can/cannot generalise from synthetic paired sessions.

## 4. Production hospital-platform company / integration team

Example target already mapped in this repository: Recare / equivalent hospital integration platform.

**Ask:** 45-minute architecture teardown, not a sales demo.

Questions:
- Which CareOS integration assumptions are naive?
- What is configuration vs custom engineering in real hospitals?
- Which lifecycle/provenance patterns matter in production?
- Where would CareOS duplicate mature infrastructure?
- What would a credible sandbox trace look like?

**Evidence produced:**
- architecture corrections;
- overlap removed;
- real integration bottlenecks;
- candidate vendor/environment for compatibility proof.

## 5. First hospital IT + DPO/CISO discovery workshop

**Ask:** complete a non-secret capability manifest. No patient data, credentials or system access required.

**Evidence produced:**
- named system/vendor/version map where allowed;
- real interface availability;
- identity/context path;
- actual review/approval graph;
- sandbox/deidentified options;
- blockers and owners.

## 6. Vendor / approved sandbox

**Ask:** read-only/deidentified interoperability exercise against a named vendor/version.

**Evidence produced:**
- capability statement;
- auth behavior;
- FHIR/ISiK/profile gaps;
- patient-context behavior;
- partial read / corrected-result behavior;
- measured engineering hours to first useful workflow.

## Advancement order

Do not wait for all channels sequentially. Run independent tracks in parallel where safe:

```text
clinician sessions ---------┐
CEED / usability -----------┤
implementation critique ----┤
production architecture ----┼--> corrected pilot package
hospital discovery ---------┤
                            └--> approved sandbox --> shadow request
```

The next stage is earned by evidence, not calendar time.

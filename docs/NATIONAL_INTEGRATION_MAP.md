# CareOS National / EU Integration Map

Baseline date: **2026-08-16**.

Purpose: make every national/institutional dependency explicit and separate **implemented**, **validated**, **planned**, **external** and **not-applicable** states.

## Status legend

- ✅ **implemented** — code exists in CareOS.
- 🧪 **validated synthetically** — automated/synthetic evidence exists.
- 🟡 **planned / contract defined** — architecture exists, real integration missing.
- 🔒 **external dependency** — needs provider/vendor/government infrastructure or approval.
- ⚪ **scope to determine** — applicability depends on intended use/classification/deployment.

## 1. Hospital primary systems

| Layer | Preferred path | CareOS status | Scale requirement |
|---|---|---:|---|
| KIS/EHR | ISiK/FHIR where applicable, vendor API otherwise | 🧪 FHIR + ISiK structural validation | 🔒 real hospital/vendor read-only integration |
| LIS / microbiology | FHIR/ISiK/vendor interface | 🟡 connector contract + SJK workflow defined | 🔒 actual lifecycle/status mapping |
| RIS/PACS reports | FHIR/ISiK/document reference/vendor | 🟡 | 🔒 real source |
| Medication record | source-native FHIR/ISiK/ePA/vendor | 🟡 | 🔒 real source + terminology |
| Tasks/pending diagnostics | FHIR/vendor | 🟡 | 🔒 capability varies by KIS |
| Documents | source document + evidence firewall | ✅ architecture/code | 🟡 higher-recall extractor still blocked by G1 |

## 2. gematik hospital interoperability — ISiK

Official baseline:
https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik

Current CareOS:

- ✅ generic FHIR transport;
- ✅ bounded same-origin Bundle pagination;
- ✅ partial/truncation failure handling;
- 🧪 pinned gematik reference-validator CI;
- 🧪 pinned ISiK5 plugin structural/profile validation on synthetic Patient;
- ✅ explicit separation of profile validation from terminology validation;
- 🔒 real confirmed/relevant hospital product scope and vendor sandbox;
- 🔒 any formal gematik confirmation process if CareOS is confirmation-relevant.

Government proposal principle:

> CareOS should not define a competing hospital interoperability standard. It should consume applicable ISiK interfaces and publish any additional CareOS connector contracts openly enough to avoid new lock-in.

## 3. Nursing / care — ISiP

Official baseline:
https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isip

Current CareOS:

- 🟡 country/connector architecture supports an ISiP path;
- 🔒 no implemented/validated ISiP connector yet;
- 🔒 scope must be driven by an actual nursing/care workflow before implementation.

## 4. Telematikinfrastruktur / TI access

Official baseline:
https://fachportal.gematik.de/telematikinfrastruktur/ti-zugang

The gematik TI 2.0 direction includes Zero Trust and mTLS-oriented access and preserves heterogeneous primary systems.

CareOS:

- ✅ internal auth architecture follows Zero Trust principles (no trust-by-network);
- 🟡 adapter boundary allows future TI identity/access services;
- 🔒 no production TI access component is implemented;
- 🔒 any product approval/confirmation obligations depend on actual product scope.

## 5. Digital identities

Official baseline:
https://fachportal.gematik.de/telematikinfrastruktur/identitaeten

CareOS:

- ✅ provider OIDC/JWT verifier foundation;
- ✅ organisation/role/treatment-context policy contract;
- ✅ context-launch contract;
- 🟡 designed to consume provider/TI identity assertions rather than create national identity;
- 🔒 real hospital IdP and/or TI identity integration.

## 6. Proof of Patient Presence (PoPP)

Official baseline:
https://fachportal.gematik.de/telematikinfrastruktur/komponenten-dienste/popp

CareOS:

- ✅ treatment-context is part of the authorization model;
- 🟡 PoPP can become one cryptographically grounded context signal where applicable;
- 🔒 no PoPP integration implemented.

Architecture rule:

> CareOS treatment-context policy must be able to consume national context evidence without hard-coding one mechanism as universally available.

## 7. ePA

CareOS treats ePA as an authoritative/authorized information source within the national ecosystem, not as a database to replace.

Target use:

- authorized retrieval of available patient data where applicable;
- preserve source/origin;
- distinguish absence/restriction/unavailability;
- no assumption that ePA contains the full local hospital record.

Status:

- 🟡 architectural path;
- 🔒 no production ePA integration.

## 8. KIM

KIM is treated as a secure communication/document transport path, not as the clinical truth layer itself.

Status:

- 🟡 architectural path;
- 🔒 no KIM integration.

## 9. Terminology

CareOS terminology architecture must support governed use/mapping of relevant systems such as:

- ICD-10-GM;
- SNOMED CT;
- LOINC;
- UCUM;
- ATC;
- OPS;
- local hospital codes.

Status:

- ✅ terminology-policy boundary exists;
- ✅ unit-normalization layer exists for governed cases;
- ✅ ISiK profile validation is not misrepresented as terminology validation;
- 🔒 production terminology service + licensed/current code systems/value sets;
- 🔒 local-code mapping governance.

## 10. Cloud / §393 SGB V / C5

Official law:
https://www.gesetze-im-internet.de/sgb_5/__393.html

Reference implications where applicable:

- approved processing locations and domestic establishment conditions;
- appropriate technical/organizational measures;
- current C5 evidence or legally recognized equivalent;
- implementation of corresponding customer controls;
- hospital security obligations referenced by §393.

CareOS:

- ✅ deployment patterns separate provider data plane/control plane;
- ✅ assurance pack includes C5/customer-controls evidence;
- 🔒 no CareOS production environment currently claims an independent C5 Type 2 attestation;
- 🔒 real hosting provider/processing location/subprocessor matrix required per deployment.

## 11. EHDS — Regulation (EU) 2025/327

Official regulation:
https://eur-lex.europa.eu/eli/reg/2025/327/oj/

EHDS defines, among other things, harmonized EHR interoperability and logging components and technical-documentation/conformity obligations for systems within scope.

CareOS:

- ✅ architecture separates interoperability and logging as first-class components;
- ✅ technical-documentation index maps architecture/evidence to EHDS-style documentation expectations;
- ✅ lifecycle/change-control records are explicit;
- 🟡 European EHR exchange-format pathway is planned;
- ⚪ final EHR-system applicability/classification requires qualified legal/regulatory assessment;
- 🔒 no claim of EHDS conformity.

## 12. International Patient Summary (IPS)

CareOS uses IPS as a portability reference/baseline where appropriate, not as proof of global interoperability.

Status:

- 🟡 IPS-shaped preview exists;
- 🔒 current implementation-guide validation and coded-resource completeness required before conformance claim.

## 13. Open connector / anti-lock-in layer

Regardless of national standard, CareOS defines a vendor-neutral contract:

```text
capabilities
+ source identity
+ data/truth envelope
+ version/freshness
+ failure state
+ read/write capability
```

This is intended to keep vendor-specific implementation behind a stable provider-facing architecture.

## 14. Government-scale implementation sequence

```text
ISiK hospital proof
      ↓
second KIS/vendor proof
      ↓
provider identity/context integration
      ↓
ePA/TI path where useful
      ↓
ISiP / outpatient pathways
      ↓
EHDS interoperability/logging mapping
      ↓
open national connector/fact/failure contracts
```

## 15. What would qualify as national readiness evidence

CareOS should not claim national-scale readiness until there is evidence for:

- multiple hospital/KIS vendors;
- ambulatory/PVS path;
- nursing/care path where in scope;
- national identity/access integration where needed;
- ePA/TI interoperability where valuable;
- terminology governance;
- repeatable provider-isolated deployment;
- government/hospital procurement/security evidence;
- EHDS applicability/conformance path;
- independent multi-site clinical/workflow evaluation.

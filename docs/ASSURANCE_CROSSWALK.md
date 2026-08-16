# CareOS Assurance Crosswalk

Baseline date: **2026-08-16**.

Purpose: map CareOS architecture controls to major German/EU assurance themes without claiming certification or legal compliance.

## Status legend

- ✅ implemented / documented internally
- 🧪 synthetic/CI evidence
- 🟡 architecture prepared, production evidence missing
- 🔒 provider/external evidence required
- ⚪ legal applicability to determine

## Crosswalk

| Assurance theme | External baseline | CareOS control/evidence | Status |
|---|---|---|---:|
| Standard hospital interface | gematik ISiK | FHIR adapter, ISiK5 validator CI, connector contract | 🧪 |
| Care-sector interoperability | gematik ISiP | national integration architecture | 🟡 |
| Zero-trust access | TI 2.0 / ZETA direction | no trust-by-network; OIDC + authorization + context contracts | ✅/🟡 |
| Treatment context | PoPP / provider context | treatment-context policy + context launch | ✅ contract / 🔒 real signal |
| Identity | provider/TI identity | strong patient ID rules + provider OIDC | ✅ contract / 🔒 real IdP |
| Cloud processing | §393 SGB V | provider-data-plane patterns, C5/customer-control requirement in assurance pack | 🟡/🔒 |
| C5 customer controls | §393 SGB V / BSI C5 | shared-responsibility + procurement requirements | ✅ documented / 🔒 evidence |
| Access logging | EHDS-style logging requirements where in scope | structured audit, audit-chain prototype, provider SIEM target | ✅/🔒 |
| EHR interoperability component | EHDS if in scope | connector/fact contracts + national integration map | 🟡/⚪ |
| Technical documentation | EHDS Annex III style if in scope | `TECHNICAL_DOCUMENTATION_INDEX.md` | ✅ mapping / ⚪ applicability |
| Lifecycle/change documentation | EHDS / quality expectations where in scope | risk register + change control + ADRs | ✅ foundation |
| Privacy data flows | GDPR / provider governance | trust/data-flow doc + DSFA/AVV support | ✅ docs / 🔒 provider approval |
| Data minimization | GDPR principle / local governance | provider-side PHI, minimum necessary audience views | ✅ architecture |
| Security testing | GDPR/healthcare security practice | safety CI + dependency audit + future pentest | 🧪/🔒 |
| Dependency vulnerabilities | supply-chain security practice | scheduled pip-audit | 🧪 |
| SBOM | software supply-chain practice | CycloneDX artifact workflow | 🧪 |
| Wrong-patient safety | clinical safety | strong-ID-only auto attach; mismatch fail closed | ✅/🧪 |
| Source traceability | clinical safety/auditability | mandatory provenance/evidence contract | ✅/🧪 |
| Source outage safety | reliability/clinical safety | explicit stale/unavailable/unknown + fail-visible | ✅/🧪 |
| Model hallucination boundary | AI safety | untrusted candidate + exact evidence firewall | ✅/🧪 |
| Clinical decision autonomy | intended purpose | no autonomous diagnosis/treatment/writeback boundary | ✅ documented |
| Production validation | provider/regulatory | shadow/live study required | 🔒 |

## Important interpretation rules

### ISiK validation is not full semantic validation

CareOS deliberately distinguishes structural/profile validation from terminology validation. A green ISiK validator does not prove that every ICD/LOINC/SNOMED/ATC/OPS code or local mapping is semantically correct.

### C5 evidence is not the entire hospital security case

Where §393 SGB V applies, a current C5/equivalent report is only part of the evidence. Corresponding customer controls and provider-side technical/organizational measures still have to be implemented and reviewed.

### EHDS mapping is forward design, not conformity

CareOS maps architecture/documentation to EHDS concepts so future applicability does not require a ground-up rewrite. Formal applicability and conformity remain external/legal questions.

### Internal tests cannot replace independent assurance

CareOS CI can prove deterministic software behavior under controlled test conditions. It cannot self-award:

- hospital security acceptance;
- Datenschutz approval;
- MDR classification;
- EHDS legal scope;
- clinical safety validation;
- production penetration-test clearance.

## Official baseline sources

Checked 2026-08-16:

- ISiK: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik
- ISiK/ISiP confirmation: https://fachportal.gematik.de/shop/bestaetigungsverfahren-isik-isip
- ISiP: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isip
- TI 2.0: https://www.gematik.de/telematikinfrastruktur/ti-2-0
- TI access / Zero Trust: https://fachportal.gematik.de/telematikinfrastruktur/ti-zugang
- PoPP: https://fachportal.gematik.de/telematikinfrastruktur/komponenten-dienste/popp
- identities: https://fachportal.gematik.de/telematikinfrastruktur/identitaeten
- §393 SGB V: https://www.gesetze-im-internet.de/sgb_5/__393.html
- C5-Gleichwertigkeitsverordnung: https://www.gesetze-im-internet.de/c5gleichwv/BJNR05B0A0025.html
- BSI C5:2020: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/c5_node.html
- EHDS Regulation (EU) 2025/327: https://eur-lex.europa.eu/eli/reg/2025/327/oj/

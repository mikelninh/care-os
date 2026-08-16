# SJK Infektiologie — read-only integration discovery

> Do not collect credentials, patient data or screenshots of real records for this discovery. The goal is to learn interfaces and constraints, not bypass hospital governance.

## Ten answers that unlock the technical path

1. **KIS:** product/vendor/version used on Station 21 and in the Tagesklinik/ASV.
2. **LIS / microbiology:** product/vendor and whether microbiology is surfaced through the KIS, separate LIS, or both.
3. **Radiology:** RIS/PACS products and how reports are accessed from the clinical workstation.
4. **Document sources:** where external Arztbriefe, scans, fax/PDF and imported documents appear.
5. **Interoperability:** available FHIR/ISiK endpoints, vendor APIs, HL7 v2 feeds, document interfaces, or export capabilities.
6. **Identity:** hospital SSO/IdP technology, clinician role/group source and session model.
7. **Patient context:** whether the KIS can launch another application with trusted patient + encounter context (e.g. SMART-on-FHIR or vendor context launch).
8. **Desktop reality:** Windows/browser versions, Citrix/RDS/VDI/terminal-server use, managed iPads/tablets, network restrictions.
9. **Security/operations:** audit/SIEM destination, secrets/KMS approach, approved hosting patterns, outbound-network policy.
10. **Governance:** named IT, Informationssicherheit and Datenschutz owners for a read-only pilot.

## Preferred integration order

### Path A — trusted embedded/context launch

Best outcome:

`KIS patient context -> CareOS read-only view -> source links back to originating system`

The clinician should not search/select the patient twice.

### Path B — standards-first read-only API

Use validated ISiK/FHIR resources where the source exposes them. CareOS still validates provenance, freshness, identity and terminology separately.

### Path C — vendor adapter

When standards do not expose a required workflow fact, implement it behind the same CareOS connector contract rather than leaking vendor-specific logic into the clinical core.

### Path D — controlled document ingestion

Only for data not available structurally. Documents pass through the evidence-first extraction firewall; unsupported high-risk content becomes review-required rather than silently absent.

## Minimum first connector

Do not connect everything at once.

For Infectiology, the first useful read-only slice is likely:

- patient/encounter identity
- microbiology results and status
- relevant laboratory values
- medication record / documented anti-infectives
- tasks/pending diagnostics if exposed
- document/report references

Exact scope must be confirmed with clinicians and IT.

## Questions for a 30-minute IT call

- Which interface would you prefer an external read-only clinical app to use?
- Is ISiK already exposed in the production/test environment?
- Is there a vendor sandbox/test tenant with synthetic patients?
- Can an app receive trusted patient/encounter context from the KIS?
- How are microbiology status changes represented (preliminary/final/corrected)?
- Which identifiers are authoritative for patient and encounter matching?
- What source timestamps/version identifiers are available?
- What is the approved authentication flow?
- Where must the application run: hospital network, private cloud, vendor cloud, Citrix/VDI?
- What evidence package is required before a synthetic/read-only pilot is approved?

## Stop conditions

Do not proceed to live data if any of these remain unresolved:

- ambiguous authoritative patient identifier
- no treatment-context authorization model
- no auditable access path
- source freshness cannot be represented
- integration returns partial results without a detectable partial state
- real patient data would leave an approved processing boundary
- pilot cannot be shut down independently of the KIS

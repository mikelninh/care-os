# Global composition architecture

CareOS should scale by composition rather than product forks.

Example deployments:

- `Core + Infectiology + Germany + German + Clinician`
- `Core + Oncology + Germany + English + Clinician`
- `Core + Neurology + Vietnam + Vietnamese + Patient/Family` (future V10)

## International exchange

The International Patient Summary (IPS) is the baseline portable patient-summary contract for cross-border/global interoperability. Country packs add national identity, terminology, consent, infrastructure and regulatory requirements around the same core.

## Languages

Clinical facts remain coded/structured where possible. Human-readable labels are translated separately, preserving original source wording and language. Translation must not silently alter clinical meaning; high-risk translated content keeps original text one click away.

## Audience views

- **Clinician** — necessary clinical context for care.
- **Patient/Family (V10)** — plain-language timeline, documents, appointments, medication list, questions and permissioned sharing.
- **Payer/Care Coordination** — purpose-limited minimum dataset only. No default mirror of the clinical record.

## Portable summary preview

`GET /api/global/ips-preview/{patient_id}?language=en` exposes an **IPS-shaped preview** for development. It is intentionally labelled `preview-not-validated`; actual IPS conformance requires profile validation and correct coded resources/sections.

The portability rule is:

1. preserve structured/coded facts and original source references;
2. translate presentation labels separately;
3. retain original high-risk clinical wording one click away;
4. apply country-specific identity/consent/terminology at the Country Pack boundary;
5. validate against the current IPS implementation guide before claiming conformance.

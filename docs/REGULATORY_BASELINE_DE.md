# German regulatory & interoperability baseline

**Snapshot date: 2026-08-16.**

This file records external constraints that influence CareOS architecture. It is not legal advice and must be re-verified before each live-data deployment or material intended-use change.

## Medical software boundary

The European Commission published **MDCG 2019-11 rev.1** on qualification and classification of software under the MDR/IVDR in June 2025.

CareOS therefore treats intended purpose as a release-controlled artifact. The current prototype boundary is retrieval/context/documentation preparation with human review, not autonomous diagnosis/treatment selection.

Official source:
- https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en

## German hospital interoperability — ISiK

As of this snapshot, gematik states that the process of making **ISiK Stage 5** binding, including determination of the latest binding implementation date, is ongoing. Stage 5 was released 2025-07-01; the binding date is currently shown as TBD. Several Stage 3 modules have been mandatory since 2025-07-01.

CareOS must therefore version-pin the applicable ISiK implementation guides and validators; it must not hard-code a permanent assumption that today's stage is final.

Official sources:
- https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik
- https://fachportal.gematik.de/shop/bestaetigungsverfahren-isik-isip

## Nursing/care interoperability — ISiP

gematik is developing a binding standardized interface for information systems in nursing/care (ISiP). CareOS national-scale architecture keeps this as a separate sector connector path rather than assuming hospital ISiK covers care settings.

Official source:
- https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isip

## German cloud processing — §393 SGB V

For covered health/social data processed through cloud-computing services, §393 SGB V currently requires, among other things:

- permitted processing locations and a domestic establishment of the processing entity;
- state-of-the-art appropriate technical/organizational information-security measures;
- a current C5 attestation or qualifying equivalent route;
- implementation of corresponding customer criteria from the audit report.

From 2025-07-01, the general current C5 route is Type 2. A newly placed-on-market IT system after 2025-06-30 may use a current Type 1 attestation for its first 18 months, then Type 2 from month 19. Equivalent-security standards may be possible under the statutory route and implementing regulation.

Official sources:
- https://www.gesetze-im-internet.de/sgb_5/__393.html
- https://www.gesetze-im-internet.de/c5gleichwv/BJNR05B0A0025.html

## Architecture consequences

CareOS therefore adopts these design rules:

1. Generic FHIR support is never marketed as ISiK conformance.
2. Interoperability profiles and terminology packages are version-pinned and tested in CI.
3. Live PHI cloud deployment is blocked until the actual hosting/processing chain has applicable evidence and customer controls.
4. The provider data plane is preferred for identifiable clinical data; a CareOS control plane should not routinely centralize PHI.
5. Intended-use changes trigger regulatory reassessment rather than silent feature creep.
6. Standards/law snapshot dates are explicit because the German health-IT environment is changing quickly.

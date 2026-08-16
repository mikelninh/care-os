# CareOS — 1-Seiter für öffentliche Entscheider:innen

## Das Problem

Klinische Informationen sind vorhanden, aber im Alltag über KIS, Labor, Mikrobiologie, RIS/PACS, PVS, ePA, Dokumente und Kommunikation verteilt. Ärzt:innen rekonstruieren den Patientenkontext immer wieder manuell.

## Der Vorschlag

**Keine neue nationale Patienten-Datenbank. Kein KIS-Rip-and-Replace.**

CareOS schlägt eine föderierte klinische Kontextschicht oberhalb bestehender Systeme vor:

```text
bestehende Quellsysteme
KIS · LIS · PVS · RIS/PACS · ePA · Dokumente
                 ↓
          CareOS Kontextschicht
                 ↓
relevanter Fakt + Quelle + Aktualität + offene Arbeit + Unsicherheit
                 ↓
             Behandelnde
```

Die autoritativen Daten bleiben in den Quellsystemen. Identifizierbare klinische Daten bleiben grundsätzlich provider-seitig bzw. in einem dedizierten provider-kontrollierten Tenant.

## Warum jetzt

Die nationale/europäische Infrastruktur bewegt sich in dieselbe Richtung:

- gematik ISiK für standardisierten Datenaustausch im Krankenhaus;
- ISiP für Pflege;
- TI 2.0 mit Zero-Trust-/Identitäts-/Versorgungskontextbausteinen;
- ePA/TI als nationale Dateninfrastruktur;
- EHDS mit europäischen Interoperabilitäts- und Logging-Komponenten.

CareOS soll diese Infrastruktur **nutzen**, nicht ersetzen.

## Sicherheitsprinzipien

- keine stille Patienten-Zusammenführung über Name/Geburtsdatum;
- jede klinische Information bleibt zur Quelle rückverfolgbar;
- `nicht verfügbar` ≠ `kein Befund`;
- KI darf Fakten vorschlagen, aber nicht direkt klinische Wahrheit schreiben;
- Login allein gewährt keinen Patientenzugriff;
- Read und Write sind getrennte Fähigkeiten;
- Live-Patientendaten bleiben gesperrt, bis technische und externe Assurance-Gates erfüllt sind.

## Wie wir es beweisen

1. synthetischer Workflow-Test mit Ärzt:innen;
2. ein Fachbereich, ein Krankenhaus;
3. read-only technischer Sandbox-Pilot;
4. unabhängige Datenschutz-/Security-/Regulatory-/Clinical-Safety-Prüfung;
5. Shadow Study;
6. begrenzter read-only Live-Pilot;
7. zweites Krankenhaus mit anderem Hersteller — **ohne Core-Fork**;
8. erst dann nationale Skalierung.

## Was standardisiert werden könnte

Nicht ein bundesweit identisches UI, sondern offene Verträge:

- Clinical Fact Contract;
- Provenance Contract;
- Connector Capability Contract;
- Identity/Context Contract;
- Freshness/Failure Contract;
- Audit Contract;
- Specialty-Pack Contract.

## Erfolgsmessung

Nicht „AI accuracy“ als Nordstern, sondern:

- Minuten klinischer Zeit zurückgewonnen;
- Zeit bis zum benötigten Fakt;
- manuelle Suchen/Logins/Telefon/Fax vermieden;
- Doppeldokumentation vermieden;
- Provenance-Abdeckung;
- kritische stille Fehler;
- falsche Patientenverknüpfungen;
- Review-/False-Alert-Belastung;
- Datenaktualität;
- Wiederholbarkeit über Standorte/Hersteller.

## Konkrete Bitte an einen öffentlichen Partner

Nicht: „Bitte bundesweit ausrollen.“

Sondern:

> **Unterstützen Sie einen kleinen, messbaren, standards-first Referenzpiloten mit einem Krankenhaus und einem realen KIS/LIS-Integrationspfad. Wenn der Nutzen, die Sicherheit und die Wiederholbarkeit nicht belegt werden, stoppen wir. Wenn sie belegt werden, öffnen wir die Verträge für breitere Standardisierung und Skalierung.**

## Aktueller Status

**Reference Architecture / Proposal Package: 10/10 vollständig und reviewbar.**

**Produktionsfreigabe: ausdrücklich noch nicht.** Die aktuellen G0–G9-Gates und Blocker sind transparent im Repository dokumentiert.

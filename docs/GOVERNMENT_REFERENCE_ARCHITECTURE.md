# CareOS — Referenzarchitektur für eine föderierte klinische Kontextschicht

Status: **Vorschlag / Reference Architecture**. Kein Produktivfreigabe-, Zertifizierungs- oder Rollout-Nachweis.

Stand: **16.08.2026**.

## Kurzfassung für öffentliche Entscheider:innen

Deutschland muss nicht jedes Krankenhausinformationssystem, Praxisverwaltungssystem oder Pflegesystem ersetzen, um klinische Informationen besser nutzbar zu machen.

CareOS schlägt eine zusätzliche, standardisierte Ebene **oberhalb bestehender Primärsysteme** vor:

> **Die Quellsysteme bleiben autoritativ. Eine föderierte Kontextschicht macht relevante Informationen, Quellen, Aktualität, Unsicherheit und offene Arbeit für Menschen unmittelbar nutzbar.**

Die Architektur vermeidet einen neuen zentralen nationalen Patientendatensilo. Identifizierbare Behandlungsdaten bleiben grundsätzlich in der Organisation, in der sie verarbeitet werden, oder in einem dedizierten, organisationskontrollierten Mandanten.

## Problem

Versorgung ist sektoren- und systemübergreifend, der Arbeitskontext der Behandelnden aber häufig fragmentiert:

- KIS/EHR;
- Labor/Mikrobiologie;
- RIS/PACS;
- PVS;
- Pflege;
- ePA/TI;
- Dokumente;
- KIM;
- Telefon/Fax/manuelle Übergaben.

Mehr Daten lösen dieses Problem nicht automatisch. Entscheidend ist, dass zur richtigen Zeit klar wird:

1. **Was ist relevant?**
2. **Was ist noch offen?**
3. **Wie aktuell ist die Information?**
4. **Woher stammt sie?**
5. **Was ist widersprüchlich oder unsicher?**
6. **Wer darf sie für welchen Zweck sehen?**

## Zielbild

```text
                    Nationale / EU-Infrastruktur
        TI 2.0 · ePA · ISiK · ISiP · Terminologien · EHDS
                              │
                   Standards und Verträge
                              │
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼
 Krankenhaus A          Krankenhaus B             Praxis C
      │                       │                       │
 KIS/LIS/etc.            KIS/LIS/etc.             PVS/etc.
      │                       │                       │
      ▼                       ▼                       ▼
 provider-lokale          provider-lokale          provider-lokale
 Kontextschicht           Kontextschicht           Kontextschicht
      │                       │                       │
      └───────────────────────┼───────────────────────┘
                              ▼
      gemeinsame Fact-, Provenance-, Identity-, Audit- und
                   Interoperabilitätsverträge
```

## Was bundesweit standardisiert werden sollte

Nicht ein gemeinsames Frontend für alle.

Sondern die **Verträge darunter**:

### 1. Clinical Fact Contract

Ein dargestellter klinischer Fakt hat mindestens:

- Patient-/Fallkontext;
- Originalwert/-text;
- normalisierten Wert nur wo geregelt;
- Quelle und Quellen-ID;
- Version/Zeitstempel wo verfügbar;
- klinische Effektivzeit getrennt von Importzeit;
- Provenance/Evidence;
- Status der Aussage;
- Unsicherheits-/Reviewzustand.

### 2. Connector Contract

Jede Datenquelle meldet zusätzlich zum Inhalt:

- Fähigkeit/Capability;
- Quelle;
- Version;
- Aktualität;
- `current / stale / unavailable / unknown`;
- Vollständigkeit/Partial-State;
- Read-vs-Write-Fähigkeit.

### 3. Identity/Context Contract

Zugriff ist an Identität, Organisation, Rolle, Patient/Fall und legitimen Versorgungskontext gebunden.

### 4. Audit Contract

Jeder Zugriff auf klinischen Kontext ist nachvollziehbar; Routine-Telemetrie enthält keine klinischen Freitexte.

### 5. Failure Contract

Nicht verfügbar, nicht gefunden, unbekannt und negativ sind unterschiedliche Zustände.

## Rolle bestehender nationaler Infrastruktur

CareOS soll bestehende und entstehende nationale Infrastruktur **konsumieren**, nicht konkurrierend neu erfinden.

### ISiK

Für Krankenhäuser ist ISiK der bevorzugte standardisierte Integrationspfad, soweit die benötigten Daten/Workflows abgedeckt sind. Vendor-spezifische Schnittstellen bleiben eine kontrollierte Ergänzung.

### ISiP

Für Pflegesysteme gilt dasselbe Prinzip mit ISiP.

### TI 2.0 / ZETA / digitale Identitäten

Die Architektur ist Zero-Trust-orientiert und soll sich an digitale Identitäten, mTLS/Zero-Trust-Zugang und Versorgungskontextsignale der TI 2.0 anschließen, wenn diese für den jeweiligen Use Case verfügbar und anwendbar sind.

### Proof of Patient Presence

PoPP ist ein Beispiel für einen kryptografisch abgesicherten Versorgungskontext. CareOS sollte solche nationalen Signale verwenden können, ohne eine parallele eigene nationale Infrastruktur dafür zu erfinden.

### ePA / KIM

CareOS behandelt ePA und KIM als Daten-/Kommunikationswege im Gesamtökosystem, nicht als zu ersetzende Produkte.

### EHDS

Die Architektur trennt Interoperabilitäts- und Logging-Komponenten bewusst als eigenständige Verträge, damit künftige EHDS-Pflichten für Systeme im Anwendungsbereich anschlussfähig bleiben.

## Datenschutz- und Souveränitätsmodell

### Grundsatz

**Patientendaten bleiben möglichst nah am Leistungserbringer.**

Das nationale/zentral betriebene Control Plane braucht im Zielbild keine routinemäßige Kopie identifizierbarer Längsschnittakten.

Zentral verteilbar sind u. a.:

- Software-Releases;
- signierte Policy-Bundles;
- Specialty Packs;
- Terminologie-/Guideline-Metadaten;
- Connector-Schemas;
- nicht-patientenbezogene Betriebsmetriken.

Provider-seitig bleiben:

- identifizierbare klinische Fakten;
- Patienten-/Fallkontext;
- klinische Source-Provenance;
- Zugriffsentscheidungen;
- providerseitige Auditdaten;
- ggf. kurzlebige, freigegebene Caches.

## Sicherheitsmodell

Die Referenzarchitektur verlangt mindestens:

- starke Authentisierung;
- organisations-/rollen-/versorgungskontextbasierte Autorisierung;
- Least Privilege;
- Break Glass nur kontrolliert und auditiert;
- getrennte Read-/Write-Berechtigungen;
- verschlüsselte Transport-/Speicherwege;
- verwaltete Schlüssel/Secrets;
- manipulationsgeschützte Auditierung;
- SIEM/Monitoring;
- PHI-freie Standardtelemetrie;
- explizite Degraded Modes;
- Kill Switch und Rollback.

Cloud-Einsatz muss, soweit anwendbar, die Anforderungen des §393 SGB V inklusive aktuellem C5-Nachweis bzw. zugelassener Gleichwertigkeit und den korrespondierenden Kundenmaßnahmen erfüllen.

## KI-Modell

KI ist kein System of Record.

Ein Modell darf **Vorschläge erzeugen**, aber klinische Wahrheit wird durch Verträge und Prüfungen kontrolliert:

```text
Quelle → Modellvorschlag → exakte Evidenzprüfung → strukturierter Fakt
      → Terminologie/Zeit/Identität → Reconciliation → Review → Anzeige
```

Das Modell darf keine Quelle erfinden, widersprüchliche Quellen eigenmächtig auflösen oder ohne Evidenz klinische Fakten erzeugen.

## Einführungsvorschlag für Deutschland

### Phase A — Referenzpilot

- 1 Fachbereich;
- 1 Krankenhaus;
- rein lesend;
- klar definierte Workflows;
- synthetisch/de-identifiziert vor Live-Daten;
- unabhängige Security/Datenschutz/Regulatory Reviews.

### Phase B — Wiederholbarkeit

- zweites Krankenhaus;
- anderer KIS/LIS-Hersteller;
- gleicher CareOS-Core;
- Unterschiede nur in Connector/Mapping/Policy/SOP.

### Phase C — interoperabler Baukasten

Veröffentlichen/standardisieren:

- Connector Capability Contract;
- Clinical Fact Contract;
- Provenance Contract;
- Failure/Freshness Contract;
- Context Launch Contract;
- Audit Contract;
- Specialty-Pack Contract.

### Phase D — nationale Anschlussfähigkeit

- ePA/TI/KIM/ISiP/ambulante Pfade;
- nationale Terminologie-/Identity-Dienste;
- EHDS-Interoperabilität/Logging soweit anwendbar;
- föderiertes Multi-Site-Betriebsmodell.

## Messbare nationale Wirkung

CareOS sollte nicht mit „AI accuracy“ als Hauptkennzahl bewertet werden.

Bundesweite KPIs sollten sein:

- Minuten klinischer Arbeitszeit zurückgewonnen;
- Zeit bis zum benötigten Fakt;
- vermiedene manuelle Suchen/Logins;
- vermiedene Telefon-/Fax-/Nachfragen;
- vermiedene Doppeldokumentation;
- Provenance-Abdeckung;
- falsche Patientenverknüpfungen;
- kritische stille Fehlerrate;
- Review-/False-Alert-Belastung;
- Datenaktualität;
- Korrekturrate;
- Systemverfügbarkeit;
- Wiederverwendbarkeit über Standorte/Hersteller.

## Beschaffungsprinzipien

Eine öffentliche Ausschreibung für eine solche Kontextschicht sollte nicht an ein einzelnes KIS binden, sondern Mindestverträge verlangen:

- offene, dokumentierte APIs;
- standards-first;
- exportierbare Provenance;
- keine proprietäre Patientenidentität als Lock-in;
- getrennte Read/Write-Rechte;
- dokumentierte Degraded Modes;
- auditierbare Zugriffspolitik;
- reproduzierbare Conformance Tests;
- keine versteckten Modellabhängigkeiten;
- Exit-/Portabilitätsplan.

## Was CareOS hier anbietet

CareOS kann heute als **konkreter Referenzimplementierungs- und Pilotvorschlag** dienen.

Nicht behauptet wird:

- dass die Architektur bereits national beschlossen ist;
- dass CareOS bereits alle regulatorischen Klassifikationen abgeschlossen hat;
- dass Live-Patientendaten freigegeben sind;
- dass alle G0–G9-Gates bestanden sind;
- dass bestehende nationale Standards durch CareOS ersetzt werden sollen.

Der Vorschlag ist: **erst eine belastbare föderierte Kontextschicht beweisen, dann offene Verträge standardisieren, dann skalieren.**

## Offizielle Baseline-Quellen

Geprüft am 16.08.2026:

- ISiK: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isik
- ISiP: https://fachportal.gematik.de/zielgruppen/primaersystemhersteller/isip
- ISiK/ISiP Bestätigung: https://fachportal.gematik.de/shop/bestaetigungsverfahren-isik-isip
- TI 2.0: https://www.gematik.de/telematikinfrastruktur/ti-2-0
- TI Zugang: https://fachportal.gematik.de/telematikinfrastruktur/ti-zugang
- PoPP: https://fachportal.gematik.de/telematikinfrastruktur/komponenten-dienste/popp
- §393 SGB V: https://www.gesetze-im-internet.de/sgb_5/__393.html
- EHDS, Regulation (EU) 2025/327: https://eur-lex.europa.eu/eli/reg/2025/327/oj/

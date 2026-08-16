# CareOS × SJK Infektiologie — Entscheidungsbrief für die ärztliche Leitung

> Unverbindlicher Produktforschungs-Vorschlag. Kein offizielles Dokument des Krankenhauses. Die aktuelle Demo verarbeitet ausschließlich synthetische Daten.

## Das Problem

Infektiologische Entscheidungen hängen häufig von Informationen ab, die zeitlich und technisch verteilt sind: Mikrobiologie, finale/vorläufige Befunde, Labor, dokumentierte Antiinfektiva, Hygiene, Devices, externe Dokumente und offene Nachverfolgung.

CareOS will **kein KIS ersetzen**. Die Hypothese ist kleiner:

> **Eine lesende, quellengestützte Kontextschicht kann die Such- und Koordinationsarbeit vor Visite, Befundnachverfolgung und Übergabe reduzieren.**

## Was heute bereits gezeigt werden kann

Ein browserbasierter synthetischer Infektiologie-Prototyp:
- keine Installation;
- keine Patientendaten;
- keine KIS-Verbindung;
- keine Therapieempfehlung;
- Mikrobiologie + Status (`vorläufig / final / ausstehend`);
- dokumentierte Antiinfektiva;
- offene Punkte;
- Quellenzugriff;
- Übergabeentwurf;
- mobiler und einfacher Desktop-Test.

## Der erste Vorschlag

**5–10 Ärzt:innen testen den synthetischen Fall für je 5–15 Minuten.**

Wir messen nicht „Gefällt es?“, sondern:
- Zeit bis zur gesuchten Information;
- Fehler/Missverständnisse;
- übersehene offene Punkte;
- Korrekturen;
- Quellenaufrufe;
- subjektiven Aufwand;
- welche heutigen Suchen/Anrufe/Logins dadurch tatsächlich entfallen könnten.

## Was wir ausdrücklich noch nicht wollen

- keine echten Patientendaten;
- keinen Produktivzugang zum KIS;
- keinen automatischen Write-back;
- keine autonome Diagnose/Therapieentscheidung;
- keinen großen Rollout;
- keine Transformationszusage.

## Entscheidung nach dem Test

### Wenn kein klarer Nutzen entsteht
Projekt stoppen oder neu designen.

### Wenn klarer Nutzen entsteht
Ein **30–60-minütiges technisches Discovery** mit IT/Architektur, Informationssicherheit und Datenschutz, um ausschließlich zu klären:
- welche KIS/LIS-Schnittstellen verfügbar sind;
- ob ISiK/FHIR oder ein Vendor-Testsystem existiert;
- wie SSO + vertrauenswürdiger Patientenkontext funktionieren könnten;
- welche Browser/Citrix/VDI-Umgebung unterstützt werden muss;
- welche Sicherheits-/Datenschutzunterlagen vor einem read-only Test erforderlich wären.

## Sicherheitsprinzip

CareOS soll im Zweifel **weniger anzeigen statt sicher klingende Informationen zu erfinden**.

Der aktuelle synthetische neue Holdout zeigt den Trade-off transparent: keine beobachteten unsupported/wrong-source Claims und keine stillen kritischen Misses in diesem Test, aber nur 26.3% Recall und 100% Review-Belastung unter neuen Dokumentformen. Deshalb ist die Clinical-Truth-Gate weiterhin **BLOCKIERT** und Live-Patientendaten sind im Produktcode gesperrt.

## Die Bitte

> **Erlauben Sie uns, zunächst nur zu prüfen, ob 5–10 Kolleg:innen durch diesen Ansatz messbar weniger Informationssucharbeit hätten. Wenn nein, hören wir auf. Wenn ja, prüfen wir gemeinsam mit IT und Datenschutz einen rein lesenden technischen Test.**

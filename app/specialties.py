SPECIALTY_PACKS = {
    "infectiology": {
        "id": "infectiology",
        "name": "Infektiologie",
        "tagline": "Erreger, Resistenzen, Therapie, Hygiene und offene Mikrobiologie auf einen Blick.",
        "accent": "#1f8b76",
        "priority_sections": [
            "microbiology", "antimicrobials", "resistance", "isolation", "devices", "trend", "pending"
        ],
        "questions": [
            "Welche Blutkulturen sind noch ausstehend?",
            "Welche Erreger und Resistenzen wurden zuletzt nachgewiesen?",
            "Welche antiinfektive Therapie läuft aktuell?",
            "Gibt es einen Isolations- oder Hygienehinweis?",
            "Welche Fremdkörper/Devices sind infektiologisch relevant?",
        ],
        "guideline_sources": ["RKI/KRINKO", "AWMF", "local-sop"],
        "demo": {
            "patient": {"name":"Mara Novak","dob":"12.06.1987","id":"INF-20491","ward":"Infektiologie · Station I2","room":"I2-11"},
            "headline": "Was ändert heute die infektiologische Entscheidung?",
            "cards": [
                {"tone":"danger","label":"Mikrobiologie","value":"Blutkultur: E. coli · 2/2 Flaschen positiv","source":"Mikrobiologie · heute 06:42","detail":"Resistogramm teilweise verfügbar"},
                {"tone":"warning","label":"Resistenz","value":"Ciprofloxacin: R · Ceftriaxon: S","source":"Mikrobiologie · heute 07:05","detail":"Finale Empfindlichkeit noch ausstehend"},
                {"tone":"info","label":"Antiinfektiva","value":"Ceftriaxon 2 g i.v. 1×/Tag","source":"KIS Medikation · seit gestern 19:10","detail":"Keine automatische Therapieempfehlung"},
                {"tone":"warning","label":"Hygiene","value":"Kontaktmaßnahmen bis Klärung MRGN-Screening","source":"Hygieneauftrag · heute 07:22","detail":"lokale SOP verknüpft"},
                {"tone":"info","label":"Device","value":"ZVK seit 4 Tagen","source":"Pflege/KIS · Anlage 11.08.","detail":"Quelle erhalten"},
                {"tone":"success","label":"Verlauf","value":"Temp 39,1 → 37,8 °C · CRP 182 → 121 mg/l","source":"Vitalwerte + Labor","detail":"Trend, nicht Interpretation"},
            ],
            "pending": [
                "Finales Resistogramm Blutkultur",
                "Kontroll-Blutkultur 24 h nach Therapiebeginn",
                "MRGN-Screening",
                "Entscheidung über ZVK nach klinischer Prüfung",
            ],
            "timeline": [
                {"time":"07:22","source":"Hygiene","title":"Kontaktmaßnahmen dokumentiert","summary":"Bis MRGN-Screening abgeschlossen ist.","ref":"Hygiene · Auftrag H-881"},
                {"time":"07:05","source":"Mikrobiologie","title":"Vorläufiges Resistogramm","summary":"E. coli: Ciprofloxacin R, Ceftriaxon S.","ref":"LIS · Kultur BC-1142"},
                {"time":"06:42","source":"Mikrobiologie","title":"Blutkultur positiv","summary":"E. coli in 2/2 Flaschen; finale Empfindlichkeit ausstehend.","ref":"LIS · Kultur BC-1142"},
                {"time":"05:55","source":"Labor","title":"Entzündungswerte","summary":"CRP 121 mg/l, Leukozyten 13,4 G/l.","ref":"LIS · Auftrag 80519"},
                {"time":"Gestern 19:10","source":"KIS","title":"Antiinfektive Medikation","summary":"Ceftriaxon 2 g i.v. begonnen.","ref":"KIS · Medikation 7741"},
                {"time":"11.08.","source":"KIS/Pflege","title":"ZVK angelegt","summary":"Rechts jugulär; Anlage dokumentiert.","ref":"KIS · Prozedur 192"},
            ],
            "handover": "E. coli-Bakteriämie; vorläufig Ceftriaxon-sensibel, Ciprofloxacin-resistent. Finale Empfindlichkeit + MRGN-Screening ausstehend. Ceftriaxon läuft. Kontaktmaßnahmen aktiv. ZVK seit 4 Tagen — weitere Entscheidung klinisch prüfen.",
        }
    },
    "oncology": {
        "id": "oncology",
        "name": "Onkologie",
        "tagline": "Tumorstatus, Therapiezyklus, Pathologie, Toxizität und offene Entscheidungen gebündelt.",
        "accent": "#7557b7",
        "priority_sections": ["diagnosis", "stage", "pathology", "therapy", "toxicity", "response", "pending"],
        "questions": ["Welcher Therapiezyklus läuft?", "Welche Pathologie/Molekularbefunde sind entscheidend?", "Welche Toxizitäten sind offen?", "Was ist für das Tumorboard noch ausstehend?"],
        "guideline_sources": ["Onkopedia", "AWMF/S3", "local-tumorboard-sop"],
        "demo": {
            "patient": {"name":"Leonie Fischer","dob":"03.02.1969","id":"ONC-88012","ward":"Onkologie · Station O3","room":"O3-07"},
            "headline": "Was zählt für den nächsten onkologischen Schritt?",
            "cards": [
                {"tone":"info","label":"Diagnose / Stadium","value":"NSCLC · Stadium IV","source":"Tumorboard · 13.08.","detail":"synthetischer Fall"},
                {"tone":"info","label":"Molekular","value":"EGFR Exon 19 del · PD-L1 20 %","source":"Pathologie · 12.08.","detail":"Befund-ID erhalten"},
                {"tone":"success","label":"Therapie","value":"Zyklus 2 · Tag 8","source":"Onko-Therapieplan","detail":"keine Dosierungsempfehlung"},
                {"tone":"warning","label":"Toxizität","value":"Diarrhö Grad 2 · Hauttoxizität Grad 1","source":"Verlauf · heute 08:10","detail":"ärztliche Bewertung erforderlich"},
                {"tone":"warning","label":"Offen","value":"CT Response + Tumorboard","source":"Plan · morgen","detail":"zwei abhängige Schritte"},
            ],
            "pending":["CT Response-Bewertung","Tumorboard-Freigabe","Toxizitätsverlauf dokumentieren"],
            "timeline":[
                {"time":"Heute 08:10","source":"KIS/Verlauf","title":"Toxizitäten dokumentiert","summary":"Diarrhö Grad 2, Hauttoxizität Grad 1; klinische Bewertung bleibt beim Behandlungsteam.","ref":"KIS · Verlauf ONC-552"},
                {"time":"Gestern 14:30","source":"Onko-Therapieplan","title":"Therapiezyklus dokumentiert","summary":"Zyklus 2, Tag 8 im aktuellen Therapieplan.","ref":"Onko-Plan · OP-2202"},
                {"time":"13.08. 16:00","source":"Tumorboard","title":"Stadium bestätigt","summary":"NSCLC, Stadium IV im synthetischen Tumorboard-Fall dokumentiert.","ref":"Tumorboard · TB-203"},
                {"time":"12.08. 11:18","source":"Pathologie","title":"Molekularbefund","summary":"EGFR Exon 19 del; PD-L1 20 %. Originalbefund bleibt maßgeblich.","ref":"Pathologie · P-8891"},
            ],
            "handover":"NSCLC Stadium IV; Molekularbefund verfügbar. Zyklus 2 Tag 8. Toxizitäten dokumentiert. CT und Tumorboard offen."
        }
    },
    "neurology": {
        "id": "neurology",
        "name": "Neurologie",
        "tagline": "Neurologischer Ausgangsstatus, Verlauf, Bildgebung, Medikation und Funktionsänderungen im Kontext.",
        "accent": "#3977a5",
        "priority_sections": ["baseline", "exam", "imaging", "medication", "function", "cognition", "pending"],
        "questions": ["Was ist der neurologische Ausgangsstatus?", "Was hat sich funktionell geändert?", "Welche Bildgebung ist neu?", "Welche offenen neurologischen Follow-ups gibt es?"],
        "guideline_sources": ["DGN/AWMF", "EAN", "local-sop"],
        "demo": {
            "patient": {"name":"Karin Vogel","dob":"28.09.1958","id":"NEU-11903","ward":"Neurologie · Station N4","room":"N4-03"},
            "headline": "Was hat sich neurologisch wirklich verändert?",
            "cards": [
                {"tone":"info","label":"Baseline","value":"Mobil mit Rollator · Sprache klar","source":"Aufnahme · 14.08.","detail":"Ausgangsstatus"},
                {"tone":"warning","label":"Neu seit heute","value":"Gangunsicherheit deutlich stärker","source":"Pflege + Visite · 07:40","detail":"zeitlich getrennte Quellen"},
                {"tone":"info","label":"Bildgebung","value":"MRT gestern · kein akuter Infarkt","source":"Radiologie · 18:22","detail":"Befund-ID erhalten"},
                {"tone":"warning","label":"Offen","value":"Physio-Reassessment + Orthostase","source":"Plan · heute","detail":"Follow-up"},
            ],
            "pending":["Physio-Reassessment","Orthostase prüfen","Medikationsabgleich"],
            "timeline":[
                {"time":"Heute 07:40","source":"KIS/Pflege + Visite","title":"Gangunsicherheit verstärkt","summary":"Deutlich stärker als der dokumentierte Aufnahme-Baseline; Ursache nicht automatisch interpretiert.","ref":"KIS · Verlauf N-441"},
                {"time":"Gestern 18:22","source":"Radiologie","title":"MRT-Befund","summary":"Kein akuter Infarkt im synthetischen Radiologie-Befund.","ref":"RIS · MR-881"},
                {"time":"14.08. 15:05","source":"KIS/Aufnahme","title":"Neurologischer Ausgangsstatus","summary":"Mobil mit Rollator, Sprache klar.","ref":"KIS · Aufnahme N4-230"},
                {"time":"Heute 08:05","source":"Plan","title":"Reassessment offen","summary":"Physio-Reassessment, Orthostase und Medikationsabgleich ausstehend.","ref":"KIS · Plan N4-992"},
            ],
            "handover":"Baseline mobil mit Rollator, heute deutlich gangunsicherer. MRT ohne akuten Infarkt. Reassessment und Orthostase offen."
        }
    }
}

def list_specialty_packs():
    return [{k:v for k,v in pack.items() if k != "demo"} for pack in SPECIALTY_PACKS.values()]

def specialty_demo(pack_id: str):
    return SPECIALTY_PACKS.get(pack_id)

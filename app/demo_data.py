PATIENTS = [
    {
        "id": "farid", "name": "Farid Rahman", "dob": "02.11.1979", "age": 46,
        "patient_no": "24681357", "sex": "Männlich", "ward": "Station 3A · Innere Medizin",
        "room": "3A-17", "status": "attention", "status_label": "Allergie beachten", "initials": "FR"
    },
    {
        "id": "anna", "name": "Anna Keller", "dob": "14.03.1968", "age": 58,
        "patient_no": "87654321", "sex": "Weiblich", "ward": "Station 2B · Kardiologie",
        "room": "2B-04", "status": "review", "status_label": "1 Punkt offen", "initials": "AK"
    },
    {
        "id": "lena", "name": "Lena Hoffmann", "dob": "21.07.1992", "age": 34,
        "patient_no": "12233344", "sex": "Weiblich", "ward": "Station 5A · Pneumologie",
        "room": "5A-09", "status": "ready", "status_label": "Ruhiger Verlauf", "initials": "LH"
    },
    {
        "id": "michael", "name": "Michael Bauer", "dob": "05.09.1960", "age": 65,
        "patient_no": "99887766", "sex": "Männlich", "ward": "Station 3B · Chirurgie",
        "room": "3B-12", "status": "ready", "status_label": "Postoperativ stabil", "initials": "MB"
    },
]

TIMELINES = {
    "farid": [
        {"id":"f1","day":"Heute","time":"09:15","source":"KIS","source_class":"blue","title":"Entlassungsbrief internistische Station 3A","summary":"Entlassung in stabilem Zustand, Weiterbehandlung empfohlen.","author":"Dr. Julia Berger","kind":"document","source_ref":"KIS · Fall 89214"},
        {"id":"f2","day":"Heute","time":"08:45","source":"Arztbrief","source_class":"mint","title":"Konsiliarbericht Kardiologie","summary":"Sinusrhythmus, EF 55 %, medikamentös stabil.","author":"Dr. S. Müller","kind":"document","source_ref":"Arztbrief · 08:45"},
        {"id":"f3","day":"Heute","time":"08:20","source":"Labor","source_class":"mint","title":"Laborergebnisse","summary":"Krea 1,1 mg/dl · eGFR 76 ml/min · CRP 2,1 mg/l","author":"Laborzentrum Nord","kind":"lab","source_ref":"Labor · Auftrag 4831"},
        {"id":"f4","day":"Heute","time":"07:55","source":"ePA","source_class":"red","title":"Allergien & Unverträglichkeiten","summary":"Penicillin (Hautausschlag), ASS (Urtikaria)","author":"ePA","kind":"warning","source_ref":"ePA · Allergien"},
        {"id":"f5","day":"Heute","time":"07:30","source":"Fax","source_class":"blue","title":"Zuweisung Hausarzt","summary":"Anamnese, Vorbefunde, Medikation — Fax digital erfasst.","author":"Dr. K. Reuter","kind":"fax","source_ref":"Fax · Eingang 07:30 · 3 Seiten"},
        {"id":"f6","day":"Gestern","time":"16:10","source":"Anrufnotiz","source_class":"orange","title":"Rücksprache mit Hausarzt","summary":"Medikationsanpassung besprochen. Rückruf nicht mehr offen.","author":"Dr. M. Neumann","kind":"phone","source_ref":"Anrufnotiz · 16:10"},
        {"id":"f7","day":"Gestern","time":"14:40","source":"Pflege","source_class":"violet","title":"Pflegebericht","summary":"Mobilität verbessert, Schmerz NRS 2.","author":"Station 3A Team","kind":"note","source_ref":"Pflege · Schichtbericht"},
        {"id":"f8","day":"Gestern","time":"11:22","source":"Externer Scan","source_class":"gray","title":"Vorbefunde / MRT Knie","summary":"Externe Bildgebung (PDF), relevante Befunde indexiert.","author":"Extern","kind":"document","source_ref":"PDF · 6 Seiten"},
        {"id":"f9","day":"22.05.2024","time":"14:05","source":"Arztbrief","source_class":"violet","title":"Nephrologischer Konsiliarbericht","summary":"Chronische Niereninsuffizienz Stadium 3b dokumentiert.","author":"Dr. S. Weber","kind":"document","source_ref":"Arztbrief · 22.05.2024"},
        {"id":"f10","day":"10.03.2023","time":"13:12","source":"ePA","source_class":"red","title":"Allergie-Hinweis","summary":"Allergische Reaktion auf Amoxicillin vor zwei Jahren (Exanthem).","author":"ePA","kind":"warning","source_ref":"ePA · Altinformation"},
    ],
    "anna": [
        {"id":"a1","day":"Heute","time":"08:42","source":"KIS","source_class":"blue","title":"Aufnahme Kardiologie","summary":"Schwindel bei Lagewechsel, Orthostaseabklärung geplant.","author":"Dr. Julia Berger","kind":"document","source_ref":"KIS · Aufnahme"},
        {"id":"a2","day":"Heute","time":"08:15","source":"Labor","source_class":"mint","title":"Laborergebnisse","summary":"Hb 12,7 g/dl · K 4,1 mmol/l · Krea 0,9 mg/dl","author":"Laborzentrum Nord","kind":"lab","source_ref":"Labor · Auftrag 4950"},
        {"id":"a3","day":"Heute","time":"07:48","source":"Pflege","source_class":"violet","title":"Pflegebericht","summary":"Beim Aufstehen kurz schwindelig, kein Sturz. RR im Stehen erneut kontrollieren.","author":"Station 2B Team","kind":"note","source_ref":"Pflege · Frühdienst"},
        {"id":"a4","day":"Gestern","time":"17:20","source":"Fax","source_class":"blue","title":"Medikationsplan Hausarzt","summary":"Ramipril 5 mg, Bisoprolol 2,5 mg, keine bekannten Allergien.","author":"Hausarztpraxis","kind":"fax","source_ref":"Fax · 17:20 · 2 Seiten"},
    ],
    "lena": [
        {"id":"l1","day":"Heute","time":"08:29","source":"Pflege","source_class":"violet","title":"Verlauf","summary":"Mobil, keine Luftnot, Temperatur 36,8 °C.","author":"Station 5A Team","kind":"note","source_ref":"Pflege · Frühdienst"},
        {"id":"l2","day":"Heute","time":"07:50","source":"Labor","source_class":"mint","title":"Laborergebnisse","summary":"CRP rückläufig, Leukozyten normalisiert.","author":"Laborzentrum Nord","kind":"lab","source_ref":"Labor · Auftrag 4902"},
        {"id":"l3","day":"Gestern","time":"15:30","source":"Arztbrief","source_class":"mint","title":"Pneumologischer Verlauf","summary":"Klinisch gebessert, Entlassung voraussichtlich morgen.","author":"Dr. M. Schwarz","kind":"document","source_ref":"Arztbrief · gestern"},
    ],
    "michael": [
        {"id":"m1","day":"Heute","time":"07:58","source":"KIS","source_class":"blue","title":"Postoperativer Verlauf","summary":"Wundverhältnisse reizlos, Mobilisation nach Plan.","author":"Dr. T. Lang","kind":"document","source_ref":"KIS · Verlauf"},
        {"id":"m2","day":"Gestern","time":"18:00","source":"Pflege","source_class":"violet","title":"Pflegebericht","summary":"Schmerz NRS 3, selbstständig mobilisiert.","author":"Station 3B Team","kind":"note","source_ref":"Pflege · Spätdienst"},
    ],
}

FOCUS = {
    "farid": {"headline":"3 Dinge, die jetzt zählen","facts":[{"tone":"danger","label":"Allergie","value":"Penicillin · Hautausschlag; ASS · Urtikaria","source":"ePA · heute 07:55","search":"Allerg"},{"tone":"info","label":"Letzte Nierenfunktion","value":"Krea 1,1 mg/dl · eGFR 76 ml/min","source":"Labor · heute 08:20","search":"Krea"},{"tone":"success","label":"Frühere Medikation","value":"Ramipril · Metformin · Atorvastatin","source":"KIS + Hausarzt","search":"Ramipril"}],"next_action":"Keine ungeklärte sicherheitskritische Aufgabe. Allergiehinweis bleibt beim Dokumentieren sichtbar.","next_tone":"safe"},
    "anna": {"headline":"1 Punkt braucht deine Aufmerksamkeit","facts":[{"tone":"warning","label":"Offener Follow-up","value":"RR im Stehen erneut kontrollieren","source":"Pflege · heute 07:48","search":"Stehen"},{"tone":"info","label":"Letztes Labor","value":"Krea 0,9 mg/dl · K 4,1 mmol/l","source":"Labor · heute 08:15","search":"Krea"},{"tone":"success","label":"Hausarzt-Medikation","value":"Ramipril 5 mg · Bisoprolol 2,5 mg","source":"Fax · gestern 17:20","search":"Ramipril"}],"next_action":"Vor Abschluss: Orthostase-Follow-up dokumentieren oder als offen markieren.","next_tone":"warn"},
    "lena": {"headline":"Ruhiger Verlauf","facts":[{"tone":"success","label":"Aktueller Status","value":"Mobil · keine Luftnot · 36,8 °C","source":"Pflege · heute 08:29","search":"Mobil"},{"tone":"success","label":"Entzündung","value":"CRP rückläufig · Leukozyten normalisiert","source":"Labor · heute 07:50","search":"CRP"},{"tone":"info","label":"Plan","value":"Entlassung voraussichtlich morgen","source":"Arztbrief · gestern 15:30","search":"Entlassung"}],"next_action":"Keine offene Warnung im synthetischen Fall.","next_tone":"safe"},
    "michael": {"headline":"Postoperativ stabil","facts":[{"tone":"success","label":"Wunde","value":"Reizlos","source":"KIS · heute 07:58","search":"Wund"},{"tone":"success","label":"Mobilität","value":"Selbstständig mobilisiert","source":"Pflege · gestern 18:00","search":"mobil"},{"tone":"info","label":"Schmerz","value":"NRS 3","source":"Pflege · gestern 18:00","search":"NRS"}],"next_action":"Keine offene Warnung im synthetischen Fall.","next_tone":"safe"},
}

DOCUMENTATION_CASES = {"farid":{"note":"Patient klagt über zunehmende Atemnot bei Belastung. Seit zwei Tagen zunehmend. Leichte Beinödeme beidseits. Gewicht +2 kg. RR 148/90, SpO₂ 93 %. Medikation: Ramipril, Bisoprolol, Furosemid. Plan: Echo veranlassen, Verlauf beobachten und Medikation ärztlich prüfen.","structured":{"Situation":"Zunehmende Belastungsdyspnoe seit zwei Tagen, leichte Beinödeme beidseits.","Background":"Relevante Vorinformationen und Allergien aus dem Patientenverlauf verknüpft.","Assessment":"Gewicht +2 kg · RR 148/90 · SpO₂ 93 %.","Plan":"Echo veranlassen · Verlaufskontrolle · Medikation ärztlich prüfen."},"tasks":["Echo veranlassen","Verlaufskontrolle dokumentieren","Medikation ärztlich prüfen"],"handover":"Farid Rahman: zunehmende Belastungsdyspnoe mit Beinödemen. Relevante Allergien und Vorinformationen im Verlauf verknüpft. Offen: Echo, Verlauf, Medikationsprüfung.","discharge":"Entlassbrief-Vorlage gestartet; keine automatische Freigabe oder klinische Entscheidung."}}

INBOX_ITEMS = [
    {"id":"fax-farid","type":"Fax","received":"Heute · 10:02","sender":"Hausarztpraxis Reuter","subject":"Vorbefunde / Medikationsplan","pages":3,"status":"matched","patient_id":"farid","match_confidence":0.99,"match_reason":"Patienten-ID + Name + Geburtsdatum stimmen überein","preview":"Farid Rahman · 02.11.1979 · Medikation: Ramipril, Metformin, Atorvastatin. Allergie: Penicillin dokumentiert."},
    {"id":"scan-ambiguous","type":"Scan","received":"Heute · 10:11","sender":"Externe Praxis","subject":"Vorbefund Michael Bauer","pages":5,"status":"ambiguous","patient_id":None,"match_confidence":0.62,"match_reason":"Name passt, Geburtsdatum auf Scan teilweise unleserlich","preview":"Michael Bauer · geb. 05.0?.19?0 · postoperativer Verlauf ...","candidates":[{"patient_id":"michael","label":"Michael Bauer · 05.09.1960 · ID 99887766"},{"patient_id":"michael-alt","label":"Michael Bauer · 05.06.1968 · ID 55661209"}]}
]

PILOT_TASKS = [
    {"id":"allergy","title":"Frühere Allergie finden","prompt":"Welche relevante Antibiotika-Reaktion ist in Farids Vorgeschichte dokumentiert?","patient_id":"farid","answer_hint":"Amoxicillin · Exanthem (historischer Eintrag)","baseline_minutes":12,"expected_search":"Amoxicillin","call_avoided":1},
    {"id":"renal","title":"Letzte Nierenfunktion finden","prompt":"Wie lautet Farids letzter dokumentierter Kreatinin-/eGFR-Wert?","patient_id":"farid","answer_hint":"Krea 1,1 mg/dl · eGFR 76 ml/min","baseline_minutes":8,"expected_search":"Krea","call_avoided":0},
    {"id":"orthostasis","title":"Offenen Pflegepunkt finden","prompt":"Welcher konkrete Follow-up-Punkt ist bei Anna offen?","patient_id":"anna","answer_hint":"RR im Stehen erneut kontrollieren","baseline_minutes":7,"expected_search":"Stehen","call_avoided":1},
    {"id":"document","title":"Notiz für Übergabe wiederverwenden","prompt":"Bereite aus einer vorhandenen Notiz strukturierte Doku + Übergabe + Aufgaben vor.","patient_id":"farid","answer_hint":"Dokumentationsansicht öffnen und vorbereiten","baseline_minutes":10,"expected_search":"","call_avoided":0},
    {"id":"fax","title":"Externen Befund sicher zuordnen","prompt":"Prüfe, ob ein eingehender Scan eindeutig einem Patienten zugeordnet werden kann.","patient_id":"michael","answer_hint":"Ambiguität erkennen; keine automatische Zuordnung","baseline_minutes":6,"expected_search":"","call_avoided":0}
]

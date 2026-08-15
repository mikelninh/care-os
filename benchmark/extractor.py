from __future__ import annotations

import re
from typing import Any

MED_NAMES = ["Ramipril", "Bisoprolol", "Metformin", "Atorvastatin", "Furosemid", "Amlodipin", "Pantoprazol", "Apixaban"]
DX_NAMES = ["Arterielle Hypertonie", "Chronische Niereninsuffizienz G3b", "Diabetes mellitus Typ 2", "Herzinsuffizienz", "COPD", "Vorhofflimmern"]
ALLERGENS = ["Penicillin", "Amoxicillin", "Ibuprofen", "ASS", "Kontrastmittel"]
REACTIONS = ["Hautausschlag", "Exanthem", "Urtikaria", "Bronchospasmus", "Juckreiz"]
ALLERGY_HEADINGS = [r"Allergie", r"Unverträglichkeit", r"Bek\.\s*Allergie", r"Allerg\.\s*gg\."]
MED_HEADINGS = [r"Aktuelle Medikation", r"Dauermedikation", r"Med\.\s*aktuell", r"Hausmedikation"]
DX_HEADINGS = [r"Relevante Diagnosen", r"Nebendiagnosen", r"Vorerkrankungen", r"Diagn\."]
FOLLOW_HEADINGS = [r"Offen", r"Noch ausstehend", r"To-do", r"Bitte nachholen"]
CONFLICT_HEADINGS = [r"Neu verordnet", r"Start heute", r"Therapie neu", r"Bitte beginnen mit"]

def _effective_date(doc: dict[str, Any]) -> str:
    m = re.search(r"Befunddatum\s+(\d{4}-\d{2}-\d{2})", doc.get("text", ""), re.I)
    return m.group(1) if m else doc.get("date", "0000-00-00")

def _heading_segment(text: str, headings: list[str]) -> str | None:
    for heading in headings:
        m = re.search(rf"(?:{heading})\s*:\s*([^\.]+)", text, re.I)
        if m: return m.group(1).strip()
    return None

def extract(case: dict[str, Any]) -> dict[str, Any]:
    docs=case["documents"]
    allergies=[]; allergy_doc=None
    for d in sorted(docs,key=lambda d:(d.get("kind")!="allergy",d.get("date",""))):
        seg=_heading_segment(d["text"],ALLERGY_HEADINGS)
        if not seg: continue
        substance=next((x for x in ALLERGENS if re.search(rf"\b{re.escape(x)}\b",seg,re.I)),None)
        reaction=next((x for x in REACTIONS if x.lower() in d["text"].lower()),None)
        if substance:
            allergies=[{"substance":substance,"reaction":reaction}]; allergy_doc=d["id"]; break

    med_doc=None; current_meds=[]
    for d in docs:
        seg=_heading_segment(d["text"],MED_HEADINGS)
        if seg is not None:
            meds=sorted([m for m in MED_NAMES if re.search(rf"\b{re.escape(m)}\b",seg)])
            if meds: med_doc=d; current_meds=meds; break

    dx_doc=None; diagnoses=[]
    for d in docs:
        seg=_heading_segment(d["text"],DX_HEADINGS)
        if seg is not None:
            dx_doc=d; diagnoses=sorted([dx for dx in DX_NAMES if dx.lower() in d["text"].lower()]); break

    renal_candidates=[]
    renal_re=re.compile(r"(?:Krea(?:tinin)?|Kreat\.|Kr€a)\s*([0-9]+[,.][0-9]+)\s*mg/d[lI].*?(?:e\s*GFR|GFR\s*\(CKD-EPI\))\s*([0-9]+)",re.I)
    for d in docs:
        m=renal_re.search(d["text"])
        if m: renal_candidates.append((_effective_date(d),float(m.group(1).replace(",",".")),int(m.group(2)),d["id"]))
    renal_candidates.sort(key=lambda x:x[0],reverse=True); renal=None; renal_source=None
    if renal_candidates:
        dt,creat,egfr,renal_source=renal_candidates[0]; renal={"creatinine_mg_dl":creat,"egfr_ml_min":egfr,"date":dt}

    follow_doc=None; followups=[]
    for d in docs:
        if d.get("kind")!="followup": continue
        seg=_heading_segment(d["text"],FOLLOW_HEADINGS)
        if seg is not None:
            follow_doc=d; followups=sorted([x.strip() for x in seg.rstrip(".").split(";") if x.strip()]); break

    discharge_doc=next((d for d in docs if d.get("kind")=="discharge"),None); discharge={"status":"none","date":None}
    if discharge_doc:
        text=discharge_doc["text"]
        m=re.search(r"(?:Entlassung geplant für|Gepl\.\s*Entl\.)\s*(\d{4}-\d{2}-\d{2})",text,re.I)
        if m: discharge={"status":"planned","date":m.group(1)}
        else:
            m=re.search(r"(?:Entlassen am|Entl\.\s*erfolgt)\s*(\d{4}-\d{2}-\d{2})",text,re.I)
            if m: discharge={"status":"completed","date":m.group(1)}

    contradictions=[]
    if allergies:
        a=allergies[0]["substance"]
        for d in docs:
            seg=_heading_segment(d["text"],CONFLICT_HEADINGS)
            if not seg: continue
            med=seg.strip(); conflict=(a in {"Penicillin","Amoxicillin"} and med=="Amoxicillin") or (a in {"Ibuprofen","ASS"} and med=="Ibuprofen") or (a=="Kontrastmittel" and med=="Kontrastmittel")
            if conflict: contradictions.append({"type":"allergy_medication","allergen":a,"medication":med,"source":d["id"]})

    return {"allergies":allergies,"current_medications":current_meds,"relevant_diagnoses":diagnoses,"last_renal_function":renal,"open_followups":followups,"discharge":discharge,"contradictions":contradictions,"provenance":{"allergy":allergy_doc,"current_medication":med_doc["id"] if med_doc else None,"diagnoses":dx_doc["id"] if dx_doc else None,"last_renal_function":renal_source,"open_followups":follow_doc["id"] if follow_doc else None,"discharge":discharge_doc["id"] if discharge_doc else None}}

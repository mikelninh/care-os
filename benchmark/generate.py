from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Any

FIRST = ["Anna", "Farid", "Lena", "Michael", "Miriam", "Thomas", "Aylin", "Jonas", "Sofia", "Mehmet"]
LAST = ["Keller", "Rahman", "Hoffmann", "Bauer", "Nguyen", "Yilmaz", "Schmidt", "Weber", "Neumann", "Costa"]
ALLERGIES = [("Penicillin", "Hautausschlag"),("Amoxicillin", "Exanthem"),("Ibuprofen", "Urtikaria"),("ASS", "Bronchospasmus"),("Kontrastmittel", "Juckreiz")]
MEDS = ["Ramipril", "Bisoprolol", "Metformin", "Atorvastatin", "Furosemid", "Amlodipin", "Pantoprazol", "Apixaban"]
DIAGNOSES = ["Arterielle Hypertonie", "Chronische Niereninsuffizienz G3b", "Diabetes mellitus Typ 2", "Herzinsuffizienz", "COPD", "Vorhofflimmern"]
FOLLOWUPS = ["RR im Stehen erneut kontrollieren", "Kalium morgen kontrollieren", "Hausarztbrief nachfordern", "Echo-Termin prüfen", "Gewicht morgen dokumentieren"]

def _iso(d: date) -> str: return d.isoformat()
def _doc(doc_id: str, source: str, day: str, text: str, kind: str = "note") -> dict[str, Any]: return {"id":doc_id,"source":source,"date":day,"kind":kind,"text":text}

def generate_case(index: int, rng: random.Random) -> dict[str, Any]:
    patient_id=f"stress-{index:04d}"; name=f"{rng.choice(FIRST)} {rng.choice(LAST)}"
    dob=date(1945+rng.randint(0,55),rng.randint(1,12),rng.randint(1,28)); today=date(2026,8,15)
    allergy,reaction=rng.choice(ALLERGIES); meds=rng.sample(MEDS,rng.randint(2,4)); diagnoses=rng.sample(DIAGNOSES,rng.randint(1,3)); followups=rng.sample(FOLLOWUPS,rng.randint(0,2))
    creat=round(rng.uniform(0.7,3.4),1); egfr=max(12,min(110,int(100/max(0.8,creat)+rng.randint(-6,6)))); renal_date=today-timedelta(days=rng.randint(0,7))
    older_creat=round(max(0.6,creat+rng.uniform(-0.7,0.8)),1); older_egfr=max(10,min(120,int(100/max(0.8,older_creat)))); old_renal_date=renal_date-timedelta(days=rng.randint(10,90))
    discharge_mode=rng.choice(["none","planned","completed"]); discharge_date=None if discharge_mode=="none" else _iso(today+timedelta(days=1 if discharge_mode=="planned" else 0))
    historical=rng.choice([m for m in MEDS if m not in meds]); docs=[]
    docs.append(_doc(f"{patient_id}-epa","ePA",_iso(today-timedelta(days=180)),f"Allergie: {allergy}. Reaktion: {reaction}. Keine weiteren bekannten Arzneimittelallergien.","allergy"))
    docs.append(_doc(f"{patient_id}-med","KIS",_iso(today),f"Aktuelle Medikation: {', '.join(meds)}. {historical} wurde vor 6 Monaten abgesetzt.","medication"))
    docs.append(_doc(f"{patient_id}-dx","Arztbrief",_iso(today-timedelta(days=2)),"Relevante Diagnosen: "+"; ".join(diagnoses)+".","diagnosis"))
    docs.append(_doc(f"{patient_id}-renal-old","Labor",_iso(old_renal_date),f"Kreatinin {older_creat:.1f} mg/dl, eGFR {older_egfr} ml/min/1,73m².","lab"))
    docs.append(_doc(f"{patient_id}-renal","Labor",_iso(renal_date),f"Krea {creat:.1f} mg/dl · eGFR {egfr} ml/min/1,73m².","lab"))
    if followups: docs.append(_doc(f"{patient_id}-follow","Pflege",_iso(today),"Offen: "+"; ".join(followups)+".","followup"))
    if discharge_mode=="planned": docs.append(_doc(f"{patient_id}-discharge","KIS",_iso(today),f"Entlassung geplant für {discharge_date}. Entlassbrief noch nicht freigegeben.","discharge"))
    elif discharge_mode=="completed": docs.append(_doc(f"{patient_id}-discharge","KIS",_iso(today),f"Entlassen am {discharge_date}. Entlassbrief final freigegeben.","discharge"))
    contradictions=[]
    if rng.random()<0.34:
        conflict_med="Amoxicillin" if allergy in {"Penicillin","Amoxicillin"} else ("Ibuprofen" if allergy in {"Ibuprofen","ASS"} else "Kontrastmittel")
        docs.append(_doc(f"{patient_id}-conflict","Anrufnotiz",_iso(today),f"Neu verordnet: {conflict_med}. Bitte heute beginnen.","medication")); contradictions.append({"type":"allergy_medication","allergen":allergy,"medication":conflict_med,"source":f"{patient_id}-conflict"})
    difficulty=rng.choice(["clean","noisy","adversarial"])
    if difficulty in {"noisy","adversarial"}: docs.append(_doc(f"{patient_id}-noise","Fax",_iso(today-timedelta(days=1)),f"Vorbefund: Patient berichtet keine neue Allergie gegen Cefuroxim. Historisch war {allergy} bereits bekannt. Altmedikation {historical}. [Scanqualität mittel]","scan"))
    if difficulty=="adversarial":
        docs.append(_doc(f"{patient_id}-adv","Externer Scan",_iso(old_renal_date),f"Archiv: Krea {older_creat:.1f} mg/dl, eGFR {older_egfr}. Frühere Medikation: {historical}; aktuell nicht mehr eingenommen.","scan"))
        if rng.random()<0.5: docs[-1]["text"]=docs[-1]["text"].replace("Krea","Kr€a")
    rng.shuffle(docs)
    provenance={"allergy":f"{patient_id}-epa","current_medication":f"{patient_id}-med","diagnoses":f"{patient_id}-dx","last_renal_function":f"{patient_id}-renal","open_followups":f"{patient_id}-follow" if followups else None,"discharge":f"{patient_id}-discharge" if discharge_mode!="none" else None}
    return {"case_id":patient_id,"patient":{"name":name,"dob":_iso(dob)},"difficulty":difficulty,"documents":docs,"gold":{"allergies":[{"substance":allergy,"reaction":reaction}],"current_medications":sorted(meds),"relevant_diagnoses":sorted(diagnoses),"last_renal_function":{"creatinine_mg_dl":creat,"egfr_ml_min":egfr,"date":_iso(renal_date)},"open_followups":sorted(followups),"discharge":{"status":discharge_mode,"date":discharge_date},"contradictions":contradictions,"provenance":provenance}}

def generate_dataset(count:int=500,seed:int=20260815)->list[dict[str,Any]]:
    rng=random.Random(seed); return [generate_case(i+1,rng) for i in range(count)]

def write_jsonl(path:Path,count:int=500,seed:int=20260815)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        for case in generate_dataset(count,seed): f.write(json.dumps(case,ensure_ascii=False)+"\n")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--count",type=int,default=500); p.add_argument("--seed",type=int,default=20260815); p.add_argument("--output",default="data/stress_gold_500.jsonl"); a=p.parse_args(); write_jsonl(Path(a.output),a.count,a.seed); print(f"wrote {a.count} cases to {a.output}")

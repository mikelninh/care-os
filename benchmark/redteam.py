from __future__ import annotations

import copy
import json
import random
from pathlib import Path
from typing import Any

from .evaluate import FIELDS, norm
from .extractor import extract
from .generate import generate_dataset


def mutate_case(case: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], list[str]]:
    c=copy.deepcopy(case); attacks=[]; docs=c["documents"]
    def replace_in_kind(kind,old,new,label):
        for d in docs:
            if d.get("kind")==kind and old in d["text"]:
                d["text"]=d["text"].replace(old,new); attacks.append(label); return
    if rng.random()<0.65: replace_in_kind("allergy","Allergie:",rng.choice(["Unverträglichkeit:","Bek. Allergie:","Allerg. gg.:"]),"allergy_heading_variant")
    if rng.random()<0.65: replace_in_kind("medication","Aktuelle Medikation:",rng.choice(["Dauermedikation:","Med. aktuell:","Hausmedikation:"]),"med_heading_variant")
    if rng.random()<0.55: replace_in_kind("diagnosis","Relevante Diagnosen:",rng.choice(["Nebendiagnosen:","Vorerkrankungen:","Diagn.:"]),"diagnosis_heading_variant")
    if rng.random()<0.55: replace_in_kind("followup","Offen:",rng.choice(["Noch ausstehend:","To-do:","Bitte nachholen:"]),"followup_heading_variant")
    for d in docs:
        if d.get("kind")=="lab" and rng.random()<0.7:
            d["text"]=d["text"].replace("Kreatinin","Kreat.").replace("Krea","Kreat."); d["text"]=d["text"].replace("eGFR",rng.choice(["GFR (CKD-EPI)","eGFR","e GFR"])); attacks.append("renal_notation_variant")
    if rng.random()<0.35:
        d=next(x for x in docs if x["id"]==c["gold"]["provenance"]["last_renal_function"]); d["text"]=d["text"].replace("mg/dl","mg/dI"); attacks.append("renal_ocr_unit_damage")
    for d in docs:
        if d.get("kind")=="discharge" and rng.random()<0.7:
            if "Entlassung geplant für" in d["text"]: d["text"]=d["text"].replace("Entlassung geplant für","Gepl. Entl.")
            elif "Entlassen am" in d["text"]: d["text"]=d["text"].replace("Entlassen am","Entl. erfolgt")
            attacks.append("discharge_shorthand")
    for d in docs:
        if d.get("kind")=="medication" and "Neu verordnet:" in d["text"] and rng.random()<0.8:
            d["text"]=d["text"].replace("Neu verordnet:",rng.choice(["Start heute:","Therapie neu:","Bitte beginnen mit:"])); attacks.append("conflict_phrase_variant")
    if rng.random()<0.5:
        allergen=c["gold"]["allergies"][0]["substance"]; c["documents"].append({"id":c["case_id"]+"-neg-bait","source":"Anamnese","date":"2026-08-15","kind":"scan","text":f"Patient verneint neue Unverträglichkeiten. Keine Allergie gegen Ceftriaxon angegeben. Bekannte Altallergie {allergen} siehe ePA."}); attacks.append("negation_bait")
    if rng.random()<0.45:
        gold=c["gold"]["last_renal_function"]; stale_creat=round(float(gold["creatinine_mg_dl"])+1.1,1); stale_egfr=max(8,int(gold["egfr_ml_min"])-22)
        c["documents"].append({"id":c["case_id"]+"-stale-copy","source":"Fax","date":"2026-08-15","kind":"scan","text":f"Heute eingescannt. Befunddatum 2025-11-03: Krea {stale_creat:.1f} mg/dl, eGFR {stale_egfr} ml/min/1,73m²."}); attacks.append("stale_result_reingested_today")
    rng.shuffle(c["documents"]); return c,attacks


def run_redteam(count:int=500,seed:int=99173)->dict[str,Any]:
    base=generate_dataset(count,seed=20260815+77); rng=random.Random(seed); field_ok={f:0 for f in FIELDS}; all_ok=0; attack_failures={}; critical_silent=0; samples=[]
    for case in base:
        attacked,attacks=mutate_case(case,rng); pred=extract(attacked); gold=attacked["gold"]; failed=[]
        for field in FIELDS:
            ok=norm(pred.get(field))==norm(gold.get(field)); field_ok[field]+=int(ok)
            if not ok: failed.append(field)
        all_ok+=int(not failed)
        if gold["contradictions"] and not pred["contradictions"]: critical_silent+=1
        for attack in attacks:
            attack_failures.setdefault(attack,[0,0]); attack_failures[attack][1]+=1; attack_failures[attack][0]+=int(bool(failed))
        if failed and len(samples)<30: samples.append({"case_id":attacked["case_id"],"attacks":attacks,"failed_fields":failed,"gold":gold,"predicted":pred})
    return {"dataset":{"count":count,"synthetic_only":True,"holdout_mutations":True,"seed":seed},"exact_field_accuracy":{f:round(field_ok[f]/count,4) for f in FIELDS},"all_fields_exact":round(all_ok/count,4),"critical_silent_contradiction_misses":critical_silent,"attack_failure_rate":{k:round(v[0]/v[1],4) for k,v in sorted(attack_failures.items())},"sample_failures":samples,"interpretation":"Red-team synthetic holdout. Failures are expected and are used to drive the next engineering iteration; not clinical validation."}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--count",type=int,default=500); p.add_argument("--output",default="data/redteam_report.json"); a=p.parse_args(); report=run_redteam(a.count); Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps({k:v for k,v in report.items() if k!="sample_failures"},ensure_ascii=False,indent=2))

from __future__ import annotations

import copy
import json
import random
from pathlib import Path
from typing import Any

from .evaluate import FIELDS, norm
from .extractor import extract
from .generate import generate_dataset


def mutate_unseen(case: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], list[str]]:
    c=copy.deepcopy(case); attacks=[]; docs=c["documents"]
    for d in docs:
        if d.get("kind")=="allergy" and rng.random()<.55:
            substance=c["gold"]["allergies"][0]["substance"]; reaction=c["gold"]["allergies"][0]["reaction"]
            d["text"]=f"Arzneimittelallergien – {substance} ({reaction}); sonst keine bekannt."; attacks.append("allergy_dash_format")
        if d.get("kind")=="medication" and "Aktuelle Medikation:" in d["text"] and rng.random()<.55:
            meds=", ".join(c["gold"]["current_medications"]); d["text"]=f"Medikationsplan bei Aufnahme | {meds} | frühere Medikation siehe Altakte."; attacks.append("med_table_format")
        if d.get("kind")=="diagnosis" and rng.random()<.45:
            d["text"]=f"Problemliste: {' | '.join(c['gold']['relevant_diagnoses'])}."; attacks.append("problem_list_heading")
        if d.get("kind")=="followup" and rng.random()<.45:
            d["text"]=f"Ausstehend → {'; '.join(c['gold']['open_followups'])}."; attacks.append("followup_arrow_format")
        if d.get("kind")=="discharge" and rng.random()<.55:
            g=c["gold"]["discharge"]
            if g["status"]=="planned": d["text"]=f"vsl. Entlassung {g['date']}; Brief in Arbeit."
            if g["status"]=="completed": d["text"]=f"Patient am {g['date']} nach Hause entlassen; Brief freigegeben."
            attacks.append("discharge_natural_language")
        if d.get("kind")=="medication" and any(x in d["text"] for x in ["Neu verordnet:","Start heute:","Therapie neu:","Bitte beginnen mit:"]) and rng.random()<.6:
            for old in ["Neu verordnet:","Start heute:","Therapie neu:","Bitte beginnen mit:"]: d["text"]=d["text"].replace(old,"Angesetzt wurde")
            attacks.append("conflict_passive_voice")
    if rng.random()<.35:
        rid=c["gold"]["provenance"]["last_renal_function"]; d=next(x for x in docs if x["id"]==rid); creat=float(c["gold"]["last_renal_function"]["creatinine_mg_dl"]); umol=round(creat*88.4); egfr=c["gold"]["last_renal_function"]["egfr_ml_min"]
        d["text"]=f"Kreatinin {umol} µmol/l; eGFR {egfr} ml/min/1,73m²."; attacks.append("renal_unit_umol")
    rng.shuffle(c["documents"]); return c,attacks


def run_unseen(count=500,seed=772331):
    cases=generate_dataset(count,seed=20260815+444); rng=random.Random(seed); field_ok={f:0 for f in FIELDS}; all_ok=0; critical=0; samples=[]; family={}
    for case in cases:
        attacked,attacks=mutate_unseen(case,rng); pred=extract(attacked); gold=attacked["gold"]; failed=[]
        for f in FIELDS:
            ok=norm(pred.get(f))==norm(gold.get(f)); field_ok[f]+=int(ok)
            if not ok: failed.append(f)
        all_ok+=int(not failed)
        if gold["contradictions"] and not pred["contradictions"]: critical+=1
        for a in attacks:
            family.setdefault(a,[0,0]); family[a][1]+=1; family[a][0]+=int(bool(failed))
        if failed and len(samples)<30: samples.append({"case_id":attacked["case_id"],"attacks":attacks,"failed_fields":failed,"gold":gold,"predicted":pred})
    return {"dataset":{"count":count,"synthetic_only":True,"unseen_holdout":True,"seed":seed},"exact_field_accuracy":{f:round(field_ok[f]/count,4) for f in FIELDS},"all_fields_exact":round(all_ok/count,4),"critical_silent_contradiction_misses":critical,"attack_failure_rate":{k:round(v[0]/v[1],4) for k,v in sorted(family.items())},"sample_failures":samples,"interpretation":"Second unseen synthetic holdout created after V8 hardening. This is the honest current edge, not clinical validation."}

if __name__=='__main__':
    r=run_unseen(500); Path('data/redteam_unseen_after_hardening.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps({k:v for k,v in r.items() if k!='sample_failures'},ensure_ascii=False,indent=2))

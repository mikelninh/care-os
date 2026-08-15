from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .extractor import extract
from .generate import generate_dataset

FIELDS = ["allergies", "current_medications", "relevant_diagnoses", "last_renal_function", "open_followups", "discharge", "contradictions", "provenance"]

def norm(value: Any) -> Any:
    if isinstance(value, dict): return {k:norm(v) for k,v in sorted(value.items())}
    if isinstance(value, list): return sorted([norm(v) for v in value],key=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False))
    return value

def evaluate(count:int=500,seed:int=20260815)->dict[str,Any]:
    cases=generate_dataset(count,seed); field_ok=Counter(); tier_ok=Counter(); tier_total=Counter(); failures=[]; critical_silent_miss=0
    for case in cases:
        pred=extract(case); gold=case["gold"]; tier=case["difficulty"]; tier_total[tier]+=1; all_ok=True; per_field={}
        for field in FIELDS:
            ok=norm(pred.get(field))==norm(gold.get(field)); per_field[field]=ok; field_ok[field]+=int(ok); all_ok &= ok
        tier_ok[tier]+=int(all_ok)
        if gold["contradictions"] and not pred["contradictions"]: critical_silent_miss+=1
        if not all_ok and len(failures)<25: failures.append({"case_id":case["case_id"],"difficulty":tier,"failed_fields":[f for f,ok in per_field.items() if not ok],"gold":gold,"predicted":pred})
    return {"dataset":{"count":count,"seed":seed,"synthetic_only":True},"exact_field_accuracy":{f:round(field_ok[f]/count,4) for f in FIELDS},"all_fields_exact":round(sum(tier_ok.values())/count,4),"all_fields_exact_by_difficulty":{t:round(tier_ok[t]/tier_total[t],4) for t in sorted(tier_total)},"critical_silent_contradiction_misses":critical_silent_miss,"sample_failures":failures,"interpretation":"Synthetic adversarial benchmark only. Not clinical validation."}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--count",type=int,default=500); p.add_argument("--seed",type=int,default=20260815); p.add_argument("--output",default="data/stress_report.json"); a=p.parse_args(); report=evaluate(a.count,a.seed); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps({k:v for k,v in report.items() if k!="sample_failures"},indent=2,ensure_ascii=False))

from __future__ import annotations

import copy
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.document_pipeline import DocumentInput
from app.extractors.base import VerifiedExtractionPipeline
from app.extractors.conservative_de import ConservativeGermanExtractor
from benchmark.generate import generate_dataset


def _recorded(day: str) -> datetime:
    return datetime.fromisoformat(day).replace(tzinfo=timezone.utc)


def mutate_dev(case: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], list[str]]:
    """Development-only mutations.

    These forms are intentionally separate from benchmark/redteam_unseen.py. It is
    acceptable to iterate against this corpus; the frozen unseen holdout must not be
    used to add recognition rules.
    """
    c = copy.deepcopy(case)
    attacks: list[str] = []

    for d in c["documents"]:
        kind = d.get("kind")
        if kind == "allergy" and rng.random() < 0.55:
            g = c["gold"]["allergies"][0]
            d["text"] = f"Allergie:\n{g['substance']}\nReaktion:\n{g['reaction']}.\nKeine weiteren bekannten Arzneimittelallergien."
            attacks.append("allergy_multiline")
        elif kind == "medication" and d["id"].endswith("-med") and rng.random() < 0.55:
            meds = "; ".join(c["gold"]["current_medications"])
            d["text"] = f"Aktuelle Medikation:\n{meds}.\nHistorische Medikation siehe Vorbefunde."
            attacks.append("medication_multiline_semicolon")
        elif kind == "diagnosis" and rng.random() < 0.5:
            diagnoses = "; ".join(c["gold"]["relevant_diagnoses"])
            d["text"] = f"Relevante Diagnosen:\n{diagnoses}."
            attacks.append("diagnosis_multiline")
        elif kind == "followup" and rng.random() < 0.5:
            followups = "; ".join(c["gold"]["open_followups"])
            d["text"] = f"Offen:\n{followups}."
            attacks.append("followup_multiline")
        elif kind == "lab" and d["id"].endswith("-renal") and rng.random() < 0.5:
            g = c["gold"]["last_renal_function"]
            creat = str(g["creatinine_mg_dl"]).replace(".", ",")
            d["text"] = f"Krea: {creat} mg/dl\neGFR: {g['egfr_ml_min']} ml/min/1,73m²."
            attacks.append("renal_multiline_colon")
        elif kind == "discharge" and rng.random() < 0.5:
            g = c["gold"]["discharge"]
            if g["status"] == "planned":
                d["text"] = f"Entlassung geplant für: {g['date']}.\nEntlassbrief noch nicht freigegeben."
            elif g["status"] == "completed":
                d["text"] = f"Entlassen am: {g['date']}.\nEntlassbrief final freigegeben."
            attacks.append("discharge_colon_multiline")

    rng.shuffle(c["documents"])
    return c, attacks


def _extract_case(case: dict[str, Any]) -> dict[str, Any]:
    pipeline = VerifiedExtractionPipeline(ConservativeGermanExtractor())
    facts = []
    rejected = 0
    for source in case["documents"]:
        result = pipeline.run(DocumentInput(
            patient_ref=case["case_id"],
            document_id=source["id"],
            source_system=source["source"],
            document_kind=source.get("kind"),
            recorded_time=_recorded(source["date"]),
            text=source["text"],
        ))
        facts.extend(result.truth.facts)
        rejected += len(result.rejected)

    values: dict[str, Any] = {
        "allergies": [],
        "current_medications": [],
        "relevant_diagnoses": [],
        "last_renal_function": None,
        "open_followups": [],
        "discharge": {"status": "none", "date": None},
    }
    provenance: dict[str, str | None] = {
        "allergy": None,
        "current_medication": None,
        "diagnoses": None,
        "last_renal_function": None,
        "open_followups": None,
        "discharge": None,
    }
    review_required = []

    for fact in facts:
        if fact.fact_type == "review_required":
            review_required.append(fact.source.document_id)
        elif fact.fact_type == "allergy":
            values["allergies"] = [fact.value_original]
            provenance["allergy"] = fact.source.document_id
        elif fact.fact_type == "current_medications":
            values["current_medications"] = sorted(fact.value_original)
            provenance["current_medication"] = fact.source.document_id
        elif fact.fact_type == "relevant_diagnoses":
            values["relevant_diagnoses"] = sorted(fact.value_original)
            provenance["diagnoses"] = fact.source.document_id
        elif fact.fact_type == "renal_function":
            if values["last_renal_function"] is None or fact.effective_time > values["last_renal_function"]["_time"]:
                values["last_renal_function"] = {
                    "creatinine_mg_dl": fact.value_original["creatinine"],
                    "egfr_ml_min": fact.value_original["egfr"],
                    "date": fact.effective_time.date().isoformat(),
                    "_time": fact.effective_time,
                }
                provenance["last_renal_function"] = fact.source.document_id
        elif fact.fact_type == "open_followups":
            values["open_followups"] = sorted(fact.value_original)
            provenance["open_followups"] = fact.source.document_id
        elif fact.fact_type == "discharge":
            values["discharge"] = fact.value_original
            provenance["discharge"] = fact.source.document_id

    if values["last_renal_function"] is not None:
        values["last_renal_function"].pop("_time")

    return {
        **values,
        "provenance": provenance,
        "review_required": sorted(set(x for x in review_required if x)),
        "surfaced_fact_count": sum(1 for f in facts if f.safe_default_surface),
        "provenance_coverage": 1.0 if not facts else sum(1 for f in facts if f.provenance_complete) / len(facts),
        "rejected_candidates": rejected,
    }


def run_dev(count: int = 200, seed: int = 90517) -> dict[str, Any]:
    cases = generate_dataset(count, seed=20260815 + 9000)
    rng = random.Random(seed)
    fields = ["allergies", "current_medications", "relevant_diagnoses", "last_renal_function", "open_followups", "discharge", "provenance"]
    correct = {field: 0 for field in fields}
    review_cases = 0
    provenance_min = 1.0
    samples = []

    for case in cases:
        attacked, attacks = mutate_dev(case, rng)
        pred = _extract_case(attacked)
        gold = attacked["gold"]
        failed = []
        for field in fields:
            if pred[field] == gold[field]:
                correct[field] += 1
            else:
                failed.append(field)
        review_cases += int(bool(pred["review_required"]))
        provenance_min = min(provenance_min, pred["provenance_coverage"])
        if failed and len(samples) < 20:
            samples.append({"case_id": case["case_id"], "attacks": attacks, "failed_fields": failed, "review_required": pred["review_required"]})

    return {
        "dataset": {
            "count": count,
            "seed": seed,
            "development_only": True,
            "frozen_unseen_holdout_used_for_tuning": False,
        },
        "exact_field_accuracy": {field: round(correct[field] / count, 4) for field in fields},
        "minimum_provenance_coverage": round(provenance_min, 4),
        "cases_routed_to_review": review_cases,
        "sample_failures": samples,
        "interpretation": "Development corpus only. Not clinical validation and not the frozen unseen holdout.",
    }


if __name__ == "__main__":
    report = run_dev()
    Path("data/g1_dev_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "sample_failures"}, ensure_ascii=False, indent=2))

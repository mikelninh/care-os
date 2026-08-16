from __future__ import annotations

import copy
import json
import random
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.case_projection import project_case
from app.document_pipeline import DocumentInput
from app.extractors.base import VerifiedExtractionPipeline
from app.extractors.conservative_de import ConservativeGermanExtractor
from benchmark.generate import generate_dataset
from benchmark.metrics import aggregate_case_scores, score_case


def _recorded(day: str) -> datetime:
    return datetime.fromisoformat(day).replace(tzinfo=timezone.utc)


def mutate_dev(case: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], list[str]]:
    """Development-only mutations, intentionally separate from frozen holdouts."""
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


def extract_case(case: dict[str, Any]) -> dict[str, Any]:
    """Full G1 path: document -> verified candidates -> envelopes -> reconciliation -> projection."""
    pipeline = VerifiedExtractionPipeline(ConservativeGermanExtractor())
    envelopes = []
    rejected = 0
    all_facts = []

    for source in case["documents"]:
        result = pipeline.run(DocumentInput(
            patient_ref=case["case_id"],
            document_id=source["id"],
            source_system=source["source"],
            document_kind=source.get("kind"),
            recorded_time=_recorded(source["date"]),
            text=source["text"],
        ))
        envelopes.append(result.truth)
        all_facts.extend(result.truth.facts)
        rejected += len(result.rejected)

    projection, reconciled = project_case(envelopes)
    pred = asdict(projection)
    pred.update({
        "surfaced_fact_count": len(reconciled.current),
        "provenance_coverage": reconciled.provenance_coverage,
        "rejected_candidates": rejected,
        "raw_fact_count": len(all_facts),
    })
    return pred


def run_dev(count: int = 200, seed: int = 90517) -> dict[str, Any]:
    cases = generate_dataset(count, seed=20260815 + 9000)
    rng = random.Random(seed)
    exact_fields = [
        "allergies", "current_medications", "relevant_diagnoses",
        "last_renal_function", "open_followups", "discharge", "provenance",
    ]
    correct = {field: 0 for field in exact_fields}
    provenance_min = 1.0
    samples = []
    scored = []

    for case in cases:
        attacked, attacks = mutate_dev(case, rng)
        pred = extract_case(attacked)
        gold = attacked["gold"]
        failed = []
        for field in exact_fields:
            if pred[field] == gold[field]:
                correct[field] += 1
            else:
                failed.append(field)
        provenance_min = min(provenance_min, pred["provenance_coverage"])
        case_score = score_case(pred, gold)
        scored.append(case_score)
        if (failed or pred["review_required"] or pred["reconciliation_issues"]) and len(samples) < 20:
            samples.append({
                "case_id": case["case_id"],
                "attacks": attacks,
                "failed_fields": failed,
                "review_required": pred["review_required"],
                "unknown_fields": pred["unknown_fields"],
                "reconciliation_issues": pred["reconciliation_issues"],
            })

    metrics = aggregate_case_scores(scored)
    return {
        "dataset": {
            "count": count,
            "seed": seed,
            "development_only": True,
            "frozen_unseen_holdout_used_for_tuning": False,
            "pipeline": "verified extraction -> clinical truth -> deterministic reconciliation -> projection",
        },
        "exact_field_accuracy": {field: round(correct[field] / count, 4) for field in exact_fields},
        "precision_recall_f1": metrics,
        "minimum_provenance_coverage": round(provenance_min, 4),
        "cases_routed_to_review": sum(1 for s in scored if s["review_required"]),
        "sample_failures": samples,
        "interpretation": "Development corpus only. Not clinical validation and not a frozen holdout.",
    }


if __name__ == "__main__":
    report = run_dev()
    Path("data/g1_dev_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(json.dumps({k: v for k, v in report.items() if k != "sample_failures"}, ensure_ascii=False, indent=2))

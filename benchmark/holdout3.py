from __future__ import annotations

import copy
import hashlib
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any

from benchmark.g1_dev import extract_case
from benchmark.generate import generate_dataset
from benchmark.metrics import aggregate_case_scores, score_case


HOLDOUT_ID = "g1-holdout3-2026-08-16"
HOLDOUT_SEED = 3160816
BASE_SEED = 20269903
MUTATION_VERSION = "1.0.0"

# Names are intentionally disjoint from benchmark.g1_dev mutation families.
HOLDOUT_FAMILIES = frozenset({
    "allergy_narrative_parenthetical",
    "medication_dash_list",
    "diagnosis_pipe_list",
    "renal_equals_semicolon",
    "followup_todo_slash",
    "discharge_german_date",
    "nonbreaking_space_noise",
})


def _de_date(iso_date: str) -> str:
    return datetime.fromisoformat(iso_date).strftime("%d.%m.%Y")


def mutate_holdout(case: dict[str, Any], rng: random.Random) -> tuple[dict[str, Any], list[str]]:
    """Mutation families not used by the development corpus.

    Do not add parser rules in response to this file's results. Once first evaluated,
    this holdout is historical evidence; further extractor work requires a new dev set
    and a future holdout.
    """

    c = copy.deepcopy(case)
    families: list[str] = []

    for d in c["documents"]:
        kind = d.get("kind")
        if kind == "allergy" and rng.random() < 0.72:
            g = c["gold"]["allergies"][0]
            d["text"] = f"Bekannte Arzneimittelallergie gegen {g['substance']} (dokumentierte Reaktion: {g['reaction']})."
            families.append("allergy_narrative_parenthetical")

        elif kind == "medication" and d["id"].endswith("-med") and rng.random() < 0.72:
            meds = "\n".join(f"- {m}" for m in c["gold"]["current_medications"])
            d["text"] = f"Dauermedikation bei Aufnahme\n{meds}\nHistorische Präparate separat dokumentiert."
            families.append("medication_dash_list")

        elif kind == "diagnosis" and rng.random() < 0.68:
            diagnoses = " | ".join(c["gold"]["relevant_diagnoses"])
            d["text"] = f"Diagnosen (für den aktuellen Aufenthalt relevant): {diagnoses}"
            families.append("diagnosis_pipe_list")

        elif kind == "lab" and d["id"].endswith("-renal") and rng.random() < 0.75:
            g = c["gold"]["last_renal_function"]
            creat = str(g["creatinine_mg_dl"]).replace(".", ",")
            d["text"] = f"Vorläufiger Laborbericht: Kreatinin={creat} mg/dL; eGFR={g['egfr_ml_min']} mL/min/1.73 m2"
            families.append("renal_equals_semicolon")

        elif kind == "followup" and rng.random() < 0.68:
            todo = " / ".join(c["gold"]["open_followups"])
            d["text"] = f"To-do heute: {todo}"
            families.append("followup_todo_slash")

        elif kind == "discharge" and rng.random() < 0.7:
            g = c["gold"]["discharge"]
            when = _de_date(g["date"])
            if g["status"] == "planned":
                d["text"] = f"Entlassung vorgesehen am {when}; Briefstatus: Entwurf."
            else:
                d["text"] = f"Entlassung erfolgt am {when}; Briefstatus: final."
            families.append("discharge_german_date")

        # Apply realistic typography noise independently; this is not OCR corruption
        # that destroys clinical meaning, only spacing variation common in exports.
        if rng.random() < 0.16 and " " in d["text"]:
            d["text"] = d["text"].replace(" ", "\u00a0", 1)
            families.append("nonbreaking_space_noise")

    rng.shuffle(c["documents"])
    return c, sorted(set(families))


def generate_holdout(count: int = 500) -> list[dict[str, Any]]:
    base = generate_dataset(count=count, seed=BASE_SEED)
    rng = random.Random(HOLDOUT_SEED)
    out = []
    for case in base:
        mutated, families = mutate_holdout(case, rng)
        mutated["holdout_families"] = families
        out.append(mutated)
    return out


def fingerprint(cases: list[dict[str, Any]]) -> str:
    payload = "\n".join(json.dumps(case, sort_keys=True, ensure_ascii=False, separators=(",", ":")) for case in cases)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _contradiction_outcome(pred: dict[str, Any], gold: dict[str, Any]) -> tuple[int, int, int]:
    """Return detected, review-routed, silent misses using gold only as benchmark oracle."""

    expected = gold.get("contradictions", [])
    if not expected:
        return 0, 0, 0

    allergy_substances = {
        str(item.get("substance")) for item in pred.get("allergies", []) if isinstance(item, dict)
    }
    orders = set(pred.get("new_medication_orders", []))
    unknown = set(pred.get("unknown_fields", []))

    detected = review = silent = 0
    for item in expected:
        if str(item.get("allergen")) in allergy_substances and str(item.get("medication")) in orders:
            detected += 1
        elif "allergies" in unknown or "current_medications" in unknown:
            review += 1
        else:
            silent += 1
    return detected, review, silent


def evaluate_holdout(count: int = 500) -> dict[str, Any]:
    cases = generate_holdout(count=count)
    case_scores = []
    exact_all = 0
    provenance_min = 1.0
    detected_contradictions = 0
    review_contradictions = 0
    silent_contradictions = 0
    family_counts = {family: 0 for family in HOLDOUT_FAMILIES}
    samples = []

    fields = [
        "allergies", "current_medications", "relevant_diagnoses",
        "last_renal_function", "open_followups", "discharge", "provenance",
    ]

    for case in cases:
        for family in case.get("holdout_families", []):
            family_counts[family] += 1
        pred = extract_case(case)
        gold = case["gold"]
        score = score_case(pred, gold)
        case_scores.append(score)
        provenance_min = min(provenance_min, pred["provenance_coverage"])
        if all(pred.get(field) == gold.get(field) for field in fields):
            exact_all += 1

        detected, review, silent = _contradiction_outcome(pred, gold)
        detected_contradictions += detected
        review_contradictions += review
        silent_contradictions += silent

        if (
            score["silent_misses"]
            or score["wrong_sources"]
            or pred.get("review_required")
            or pred.get("reconciliation_issues")
        ) and len(samples) < 25:
            samples.append({
                "case_id": case["case_id"],
                "families": case.get("holdout_families", []),
                "silent_misses": score["silent_misses"],
                "wrong_sources": score["wrong_sources"],
                "unknown_fields": pred.get("unknown_fields", []),
                "review_required": pred.get("review_required", []),
                "reconciliation_issues": pred.get("reconciliation_issues", []),
            })

    aggregate = aggregate_case_scores(case_scores)
    return {
        "holdout": {
            "id": HOLDOUT_ID,
            "count": count,
            "base_seed": BASE_SEED,
            "holdout_seed": HOLDOUT_SEED,
            "mutation_version": MUTATION_VERSION,
            "fingerprint_sha256": fingerprint(cases),
            "development_tuning_allowed": False,
            "families": sorted(HOLDOUT_FAMILIES),
            "family_counts": family_counts,
        },
        "all_fields_exact_rate": round(exact_all / count, 4),
        "precision_recall_f1": aggregate,
        "minimum_provenance_coverage": round(provenance_min, 4),
        "contradiction_safety": {
            "detected": detected_contradictions,
            "explicit_review": review_contradictions,
            "critical_silent_misses": silent_contradictions,
        },
        "sample_failures": samples,
        "interpretation": (
            "Frozen synthetic holdout. Measures generalization and abstention behavior, "
            "not clinical validity. Do not tune the extractor against these cases."
        ),
    }


if __name__ == "__main__":
    report = evaluate_holdout()
    path = Path("data/g1_holdout3_report.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    public = {k: v for k, v in report.items() if k != "sample_failures"}
    print(json.dumps(public, ensure_ascii=False, indent=2))

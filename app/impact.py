from __future__ import annotations
from statistics import median


def score_pilot_task(task_id: str, baseline_minutes: float, actual_seconds: float, *, clicks: int = 0,
                     searches: int = 0, calls: int = 0, corrections: int = 0,
                     effort: int | None = None, success: bool = True) -> dict:
    if baseline_minutes <= 0:
        raise ValueError("baseline_minutes must be > 0")
    if actual_seconds < 0:
        raise ValueError("actual_seconds must be >= 0")
    if any(x < 0 for x in (clicks, searches, calls, corrections)):
        raise ValueError("counts must be >= 0")
    if effort is not None and not 1 <= effort <= 5:
        raise ValueError("effort must be 1..5")
    actual_minutes = actual_seconds / 60.0
    gross_saved = max(0.0, baseline_minutes - actual_minutes)
    credited_saved = gross_saved if success else 0.0
    reduction = max(0.0, min(100.0, (credited_saved / baseline_minutes) * 100.0))
    return {
        "task_id": task_id,
        "baseline_minutes": round(baseline_minutes, 2),
        "actual_seconds": round(actual_seconds, 2),
        "gross_saved_minutes": round(gross_saved, 2),
        "saved_minutes": round(credited_saved, 2),
        "reduction_percent": round(reduction, 1),
        "clicks": int(clicks), "searches": int(searches), "calls": int(calls),
        "corrections": int(corrections), "effort": effort, "success": bool(success),
    }


def aggregate_results(results: list[dict]) -> dict:
    if not results:
        return {
            "tasks": 0, "completed": 0, "median_seconds": 0.0, "median_saved_minutes": 0.0,
            "total_saved_minutes": 0.0, "calls": 0, "corrections": 0, "median_effort": None,
            "success_rate": 0.0, "failed_tasks_credited_minutes": 0.0,
        }
    successful = [r for r in results if r.get("success", True)]
    failed = [r for r in results if not r.get("success", True)]
    effort = [int(r["effort"]) for r in results if r.get("effort") is not None]
    successful_saved = [float(r.get("saved_minutes", 0)) for r in successful]
    failed_credited = sum(float(r.get("saved_minutes", 0)) for r in failed)
    return {
        "tasks": len(results),
        "completed": len(successful),
        "median_seconds": round(median(float(r.get("actual_seconds", 0)) for r in results), 2),
        "median_saved_minutes": round(median(successful_saved), 2) if successful_saved else 0.0,
        "total_saved_minutes": round(sum(successful_saved), 2),
        "calls": sum(int(r.get("calls", 0)) for r in results),
        "corrections": sum(int(r.get("corrections", 0)) for r in results),
        "median_effort": median(effort) if effort else None,
        "success_rate": round(len(successful) / len(results) * 100.0, 1),
        "failed_tasks_credited_minutes": round(failed_credited, 2),
    }

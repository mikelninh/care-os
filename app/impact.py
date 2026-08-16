from __future__ import annotations
from statistics import median

MAX_BASELINE_MINUTES = 240.0
MAX_ACTUAL_SECONDS = 14_400.0
MAX_COUNT = 10_000


def score_pilot_task(task_id: str, baseline_minutes: float, actual_seconds: float, *, clicks: int = 0,
                     searches: int = 0, calls: int = 0, corrections: int = 0,
                     effort: int | None = None, success: bool = True) -> dict:
    if not task_id or len(str(task_id)) > 100:
        raise ValueError("task_id is required and must be <=100 characters")
    if baseline_minutes <= 0 or baseline_minutes > MAX_BASELINE_MINUTES:
        raise ValueError("baseline_minutes must be > 0 and <= 240")
    if actual_seconds < 0 or actual_seconds > MAX_ACTUAL_SECONDS:
        raise ValueError("actual_seconds must be between 0 and 14400")
    if any(x < 0 or x > MAX_COUNT for x in (clicks, searches, calls, corrections)):
        raise ValueError("counts must be between 0 and 10000")
    if effort is not None and not 1 <= effort <= 5:
        raise ValueError("effort must be 1..5")
    actual_minutes = actual_seconds / 60.0
    gross_saved = max(0.0, baseline_minutes - actual_minutes)
    credited_saved = gross_saved if success else 0.0
    reduction = max(0.0, min(100.0, (credited_saved / baseline_minutes) * 100.0))
    return {
        "task_id": str(task_id),
        "baseline_minutes": round(float(baseline_minutes), 2),
        "actual_seconds": round(float(actual_seconds), 2),
        "gross_saved_minutes": round(gross_saved, 2),
        "saved_minutes": round(credited_saved, 2),
        "reduction_percent": round(reduction, 1),
        "clicks": int(clicks), "searches": int(searches), "calls": int(calls),
        "corrections": int(corrections), "effort": effort, "success": bool(success),
    }


def _rescore_row(row: dict) -> dict:
    """Never trust client-computed savings when producing evidence aggregates."""
    required = {"task_id", "baseline_minutes", "actual_seconds"}
    missing = required - set(row)
    if missing:
        raise ValueError("aggregate row missing raw measurement fields: " + ", ".join(sorted(missing)))
    return score_pilot_task(
        str(row["task_id"]),
        float(row["baseline_minutes"]),
        float(row["actual_seconds"]),
        clicks=int(row.get("clicks", 0)),
        searches=int(row.get("searches", 0)),
        calls=int(row.get("calls", 0)),
        corrections=int(row.get("corrections", 0)),
        effort=int(row["effort"]) if row.get("effort") is not None else None,
        success=bool(row.get("success", True)),
    )


def aggregate_results(results: list[dict]) -> dict:
    if not results:
        return {
            "tasks": 0, "completed": 0, "median_seconds": 0.0, "median_saved_minutes": 0.0,
            "total_saved_minutes": 0.0, "calls": 0, "corrections": 0, "median_effort": None,
            "success_rate": 0.0, "failed_tasks_credited_minutes": 0.0,
        }
    if len(results) > 500:
        raise ValueError("aggregate accepts at most 500 task measurements")

    rescored = [_rescore_row(row) for row in results]
    successful = [r for r in rescored if r["success"]]
    failed = [r for r in rescored if not r["success"]]
    effort = [int(r["effort"]) for r in rescored if r.get("effort") is not None]
    successful_saved = [float(r["saved_minutes"]) for r in successful]
    failed_credited = sum(float(r["saved_minutes"]) for r in failed)
    return {
        "tasks": len(rescored),
        "completed": len(successful),
        "median_seconds": round(median(float(r["actual_seconds"]) for r in rescored), 2),
        "median_saved_minutes": round(median(successful_saved), 2) if successful_saved else 0.0,
        "total_saved_minutes": round(sum(successful_saved), 2),
        "calls": sum(int(r["calls"]) for r in rescored),
        "corrections": sum(int(r["corrections"]) for r in rescored),
        "median_effort": median(effort) if effort else None,
        "success_rate": round(len(successful) / len(rescored) * 100.0, 1),
        "failed_tasks_credited_minutes": round(failed_credited, 2),
    }

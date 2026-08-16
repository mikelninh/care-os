from __future__ import annotations

from statistics import median
from pydantic import BaseModel, Field


class StudyObservation(BaseModel):
    participant_code: str = Field(min_length=1)
    condition: str = Field(pattern="^(careos|careos-agent)$")
    task_seconds: float = Field(ge=0, le=3600)
    wrong_answers: int = Field(default=0, ge=0)
    missed_pending_items: int = Field(default=0, ge=0)
    source_opens: int = Field(default=0, ge=0)
    corrections: int = Field(default=0, ge=0)
    accepted_without_source_check: bool = False
    effort: int = Field(ge=1, le=5)
    would_use_tomorrow: bool = False


def summarize_paired_study(observations: list[StudyObservation]) -> dict:
    by_condition = {"careos": [], "careos-agent": []}
    for item in observations:
        by_condition[item.condition].append(item)

    def summary(items: list[StudyObservation]) -> dict:
        if not items:
            return {"n": 0}
        return {
            "n": len(items),
            "median_task_seconds": median(x.task_seconds for x in items),
            "wrong_answers": sum(x.wrong_answers for x in items),
            "missed_pending_items": sum(x.missed_pending_items for x in items),
            "median_source_opens": median(x.source_opens for x in items),
            "corrections": sum(x.corrections for x in items),
            "accepted_without_source_check_rate": sum(x.accepted_without_source_check for x in items) / len(items),
            "median_effort": median(x.effort for x in items),
            "would_use_tomorrow_rate": sum(x.would_use_tomorrow for x in items) / len(items),
        }

    control = summary(by_condition["careos"])
    agent = summary(by_condition["careos-agent"])
    verification_decay = None
    if control.get("n") and agent.get("n"):
        verification_decay = agent["accepted_without_source_check_rate"] - control["accepted_without_source_check_rate"]

    return {
        "control": control,
        "agent": agent,
        "verification_decay": verification_decay,
        "interpretation_rule": "faster is not better if errors, missed pending items, or unverified acceptance increase",
        "automatic_pass": False,
    }

from __future__ import annotations

import hashlib
from collections import defaultdict
from statistics import median

from pydantic import BaseModel, Field, model_validator


class StudyObservation(BaseModel):
    """One synthetic clinician-study round.

    The record is deliberately structured and contains no participant name, patient
    free text, answer transcript, or clinical note. It is suitable for local export
    from the synthetic study page and for aggregate analysis.
    """

    participant_code: str = Field(min_length=2, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    condition: str = Field(pattern=r"^(careos|careos-agent)$")
    case_id: str = Field(min_length=1, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    order_position: int = Field(ge=1, le=2)
    task_seconds: float = Field(ge=0, le=1800)
    wrong_answers: int = Field(default=0, ge=0, le=20)
    missed_pending_items: int = Field(default=0, ge=0, le=20)
    source_opens: int = Field(default=0, ge=0, le=100)
    corrections: int = Field(default=0, ge=0, le=20)
    accepted_without_source_check: bool = False
    pending_as_negative: bool = False
    recommendation_misread: bool = False
    agent_truth_confusion: bool = False
    effort: int = Field(ge=1, le=5)
    would_use_tomorrow: bool = False

    @model_validator(mode="after")
    def agent_only_confusion(self) -> "StudyObservation":
        if self.condition != "careos-agent" and self.agent_truth_confusion:
            raise ValueError("agent_truth_confusion only applies to careos-agent rounds")
        return self


# Four-sequence Latin-square-style assignment. This balances condition order and
# synthetic case order without collecting participant identity.
_SEQUENCES = (
    (("case-a", "careos"), ("case-b", "careos-agent")),
    (("case-b", "careos-agent"), ("case-a", "careos")),
    (("case-b", "careos"), ("case-a", "careos-agent")),
    (("case-a", "careos-agent"), ("case-b", "careos")),
)


def assignment_for(participant_code: str) -> dict:
    code = participant_code.strip()
    if not code or len(code) > 40 or not all(ch.isalnum() or ch in "_-" for ch in code):
        raise ValueError("participant_code must be 1-40 letters/numbers/_/-")
    bucket = hashlib.sha256(code.lower().encode("utf-8")).digest()[0] % len(_SEQUENCES)
    rounds = [
        {"order_position": index + 1, "case_id": case_id, "condition": condition}
        for index, (case_id, condition) in enumerate(_SEQUENCES[bucket])
    ]
    return {"participant_code": code, "sequence": bucket + 1, "rounds": rounds}


def _condition_summary(items: list[StudyObservation]) -> dict:
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
        "pending_as_negative_count": sum(x.pending_as_negative for x in items),
        "recommendation_misread_count": sum(x.recommendation_misread for x in items),
        "agent_truth_confusion_count": sum(x.agent_truth_confusion for x in items),
        "median_effort": median(x.effort for x in items),
        "would_use_tomorrow_rate": sum(x.would_use_tomorrow for x in items) / len(items),
    }


def summarize_paired_study(observations: list[StudyObservation]) -> dict:
    """Summarize only complete within-participant A/B pairs.

    Incomplete participants remain visible as an evidence-quality signal but can never
    influence the estimated agent effect. Duplicate conditions/order slots are rejected
    instead of silently double-weighting a clinician.
    """

    by_participant: dict[str, list[StudyObservation]] = defaultdict(list)
    for item in observations:
        by_participant[item.participant_code].append(item)

    complete_pairs: list[tuple[StudyObservation, StudyObservation]] = []
    incomplete_codes: list[str] = []
    for code, rows in sorted(by_participant.items()):
        if len(rows) != 2:
            incomplete_codes.append(code)
            continue
        conditions = {row.condition for row in rows}
        positions = {row.order_position for row in rows}
        cases = {row.case_id for row in rows}
        if conditions != {"careos", "careos-agent"} or positions != {1, 2} or len(cases) != 2:
            raise ValueError(f"invalid paired study rows for {code}")
        control = next(row for row in rows if row.condition == "careos")
        agent = next(row for row in rows if row.condition == "careos-agent")
        complete_pairs.append((control, agent))

    controls = [pair[0] for pair in complete_pairs]
    agents = [pair[1] for pair in complete_pairs]
    control_summary = _condition_summary(controls)
    agent_summary = _condition_summary(agents)

    paired_deltas = {
        "median_task_seconds": None,
        "wrong_answers": None,
        "missed_pending_items": None,
        "source_opens": None,
        "corrections": None,
        "effort": None,
    }
    verification_decay = None
    if complete_pairs:
        paired_deltas = {
            "median_task_seconds": median(a.task_seconds - c.task_seconds for c, a in complete_pairs),
            "wrong_answers": median(a.wrong_answers - c.wrong_answers for c, a in complete_pairs),
            "missed_pending_items": median(a.missed_pending_items - c.missed_pending_items for c, a in complete_pairs),
            "source_opens": median(a.source_opens - c.source_opens for c, a in complete_pairs),
            "corrections": median(a.corrections - c.corrections for c, a in complete_pairs),
            "effort": median(a.effort - c.effort for c, a in complete_pairs),
        }
        verification_decay = (
            agent_summary["accepted_without_source_check_rate"]
            - control_summary["accepted_without_source_check_rate"]
        )

    hard_stop_events = []
    for row in observations:
        if row.pending_as_negative:
            hard_stop_events.append({"participant_code": row.participant_code, "condition": row.condition, "event": "pending-as-negative"})
        if row.recommendation_misread:
            hard_stop_events.append({"participant_code": row.participant_code, "condition": row.condition, "event": "documented-treatment-read-as-recommendation"})
        if row.agent_truth_confusion:
            hard_stop_events.append({"participant_code": row.participant_code, "condition": row.condition, "event": "agent-draft-confused-with-source-truth"})

    if hard_stop_events:
        evidence_status = "safety-stop"
    elif len(complete_pairs) < 5:
        evidence_status = "insufficient-complete-pairs"
    else:
        evidence_status = "ready-for-clinician-review"

    return {
        "evidence_status": evidence_status,
        "complete_pairs": len(complete_pairs),
        "incomplete_participants": len(incomplete_codes),
        "incomplete_participant_codes": incomplete_codes,
        "control": control_summary,
        "agent": agent_summary,
        "paired_agent_minus_control": paired_deltas,
        "verification_decay": verification_decay,
        "hard_stop_events": hard_stop_events,
        "interpretation_rule": "faster is not better if errors, missed pending items, recommendation confusion, or unverified acceptance increase",
        "automatic_pass": False,
    }

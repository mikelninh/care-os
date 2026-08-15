from __future__ import annotations


def patient_match_decision(confidence: float, exact_identifiers: bool, candidate_count: int) -> dict:
    """Conservative demo policy: ambiguity blocks automatic attachment."""
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be 0..1")
    if exact_identifiers and confidence >= 0.98 and candidate_count == 1:
        return {"decision": "auto_attach_allowed", "human_confirmation": False}
    return {"decision": "block_and_confirm", "human_confirmation": True}

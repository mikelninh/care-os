from __future__ import annotations

import json
from typing import Any

DIRECT_IDENTIFIER_KEYS = {
    "name",
    "full_name",
    "given_name",
    "family_name",
    "dob",
    "date_of_birth",
    "address",
    "email",
    "phone",
    "telephone",
    "mrn",
    "patient_id",
    "patient_ref",
    "insurance_number",
    "versichertennummer",
}


class ProjectionError(ValueError):
    pass


def _find_forbidden(value: Any, path: str = "$") -> str | None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() in DIRECT_IDENTIFIER_KEYS:
                return f"{path}.{key}"
            found = _find_forbidden(nested, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            found = _find_forbidden(nested, f"{path}[{index}]")
            if found:
                return found
    return None


def project_for_model(
    facts: list[dict[str, Any]],
    *,
    allowed_categories: set[str],
    max_facts: int = 50,
    max_input_facts: int = 10_000,
    max_projected_fact_bytes: int = 8_192,
) -> list[dict[str, Any]]:
    """Create a bounded minimal model-visible projection from admitted CareOS facts.

    The cap applies to *allowed projected facts*, not the first N source facts, so a
    long prefix of undelegated categories cannot starve valid context. Direct patient
    identifier fields are absent from the fixed output shape. This remains an
    application-level minimization control, not a substitute for provider DLP/network
    enforcement or a guarantee that arbitrary clinical free text is de-identified.
    """

    if max_facts < 1 or max_facts > 500:
        raise ProjectionError("invalid model projection fact limit")
    if max_input_facts < max_facts or max_input_facts > 100_000:
        raise ProjectionError("invalid model projection input limit")
    if max_projected_fact_bytes < 256 or max_projected_fact_bytes > 65_536:
        raise ProjectionError("invalid projected fact byte limit")
    if len(facts) > max_input_facts:
        raise ProjectionError("model projection input exceeds configured fact limit")

    projected: list[dict[str, Any]] = []
    for fact in facts:
        category = str(fact.get("category") or "")
        if category not in allowed_categories:
            continue
        source_ref = fact.get("source_ref")
        if not source_ref:
            raise ProjectionError("model-visible fact requires source_ref")

        item = {
            "fact_id": fact.get("fact_id"),
            "category": category,
            "value": fact.get("value"),
            "status": fact.get("status"),
            "effective_time": fact.get("effective_time"),
            "source_ref": source_ref,
        }
        forbidden = _find_forbidden(item)
        if forbidden:
            raise ProjectionError(f"direct identifier in model projection at {forbidden}")
        try:
            encoded = json.dumps(item, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ProjectionError("model-visible fact is not serializable") from exc
        if len(encoded) > max_projected_fact_bytes:
            raise ProjectionError("model-visible fact exceeds configured size limit")
        projected.append(item)
        if len(projected) >= max_facts:
            break

    return projected

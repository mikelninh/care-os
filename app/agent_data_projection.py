from __future__ import annotations

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
) -> list[dict[str, Any]]:
    """Create a minimal model-visible projection from already-admitted CareOS facts.

    The projection intentionally excludes direct patient identifiers and requires
    each fact to declare a category and source reference. It is an application-level
    minimization control, not a substitute for provider network/DLP enforcement.
    """

    if max_facts < 1 or max_facts > 500:
        raise ProjectionError("invalid model projection fact limit")

    projected: list[dict[str, Any]] = []
    for fact in facts[:max_facts]:
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
        projected.append(item)

    return projected

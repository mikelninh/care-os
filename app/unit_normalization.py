from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .clinical_truth import ClinicalFact


@dataclass(frozen=True)
class UnitRule:
    """Governed numeric unit conversion rule.

    CareOS does not guess conversions from labels. Each conversion must be registered
    with a stable ID/version and evidence source. ClinicalFact always preserves the
    original value/unit alongside the normalized representation.
    """

    rule_id: str
    version: str
    fact_type: str
    from_unit: str
    to_unit: str
    multiplier: Decimal
    offset: Decimal = Decimal("0")
    evidence_source: str = ""

    def convert(self, value: int | float | Decimal) -> Decimal:
        return Decimal(str(value)) * self.multiplier + self.offset


class UnitNormalizationError(ValueError):
    pass


class UnitRegistry:
    def __init__(self, rules: list[UnitRule] | None = None):
        self._rules: dict[tuple[str, str, str], UnitRule] = {}
        for rule in rules or []:
            self.register(rule)

    def register(self, rule: UnitRule) -> None:
        key = (rule.fact_type, rule.from_unit, rule.to_unit)
        if key in self._rules:
            raise UnitNormalizationError(f"duplicate unit rule for {key}")
        if not rule.rule_id or not rule.version or not rule.evidence_source:
            raise UnitNormalizationError("unit rules require rule_id, version and evidence_source")
        self._rules[key] = rule

    def normalize(self, fact: ClinicalFact, *, target_unit: str) -> ClinicalFact:
        if fact.unit_original is None:
            raise UnitNormalizationError("fact has no original unit")
        if not isinstance(fact.value_original, (int, float, Decimal)):
            raise UnitNormalizationError("numeric unit normalization requires numeric original value")

        if fact.unit_original == target_unit:
            return fact.model_copy(update={
                "value_normalized": fact.value_original,
                "unit_normalized": target_unit,
            })

        key = (fact.fact_type, fact.unit_original, target_unit)
        rule = self._rules.get(key)
        if rule is None:
            raise UnitNormalizationError(f"no governed conversion rule for {key}")

        normalized = rule.convert(fact.value_original)
        return fact.model_copy(update={
            "value_normalized": normalized,
            "unit_normalized": target_unit,
            "transformer": f"{fact.transformer}+unit:{rule.rule_id}",
            "transformer_version": f"{fact.transformer_version}|{rule.version}",
        })

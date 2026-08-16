from decimal import Decimal

import pytest

from app.clinical_truth import ClinicalFact, SourceKind, SourceRef
from app.unit_normalization import UnitNormalizationError, UnitRegistry, UnitRule


def fact(unit="source-unit", value=5):
    return ClinicalFact(
        fact_id="obs:1",
        patient_ref="p1",
        fact_type="synthetic.measurement",
        value_original=value,
        unit_original=unit,
        source=SourceRef(kind=SourceKind.FHIR, system="FHIR", resource_type="Observation", resource_id="1"),
    )


def registry():
    return UnitRegistry([
        UnitRule(
            rule_id="synthetic-double",
            version="1",
            fact_type="synthetic.measurement",
            from_unit="source-unit",
            to_unit="target-unit",
            multiplier=Decimal("2"),
            evidence_source="urn:careos:test-only",
        )
    ])


def test_normalization_preserves_original_value_and_unit():
    original = fact()
    normalized = registry().normalize(original, target_unit="target-unit")
    assert normalized.value_original == 5
    assert normalized.unit_original == "source-unit"
    assert normalized.value_normalized == Decimal("10")
    assert normalized.unit_normalized == "target-unit"
    assert "synthetic-double" in normalized.transformer


def test_unknown_conversion_fails_instead_of_guessing():
    with pytest.raises(UnitNormalizationError, match="no governed conversion"):
        registry().normalize(fact(), target_unit="mystery-unit")


def test_duplicate_rule_is_rejected():
    r = registry()
    with pytest.raises(UnitNormalizationError, match="duplicate"):
        r.register(UnitRule(
            rule_id="duplicate",
            version="1",
            fact_type="synthetic.measurement",
            from_unit="source-unit",
            to_unit="target-unit",
            multiplier=Decimal("3"),
            evidence_source="urn:careos:test-only",
        ))


def test_rules_without_evidence_source_are_rejected():
    with pytest.raises(UnitNormalizationError, match="evidence_source"):
        UnitRegistry([UnitRule(
            rule_id="bad",
            version="1",
            fact_type="synthetic.measurement",
            from_unit="a",
            to_unit="b",
            multiplier=Decimal("1"),
        )])

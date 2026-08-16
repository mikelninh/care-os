from app.extractors.model_schema import MODEL_EXTRACTION_RULES, ModelCandidate, ModelExtractionResponse


def test_model_schema_requires_quote_but_not_model_offsets():
    item = ModelCandidate(
        fact_type="allergy",
        value_original="Penicillin",
        evidence_quote="Penicillin",
        confidence=0.9,
    )
    assert item.evidence_quote == "Penicillin"
    assert "evidence_start" not in ModelCandidate.model_fields
    assert "evidence_end" not in ModelCandidate.model_fields


def test_empty_response_is_valid_when_model_cannot_support_a_fact():
    response = ModelExtractionResponse()
    assert response.candidates == []


def test_model_rules_forbid_paraphrase_offsets_time_guessing_and_clinical_guessing():
    rules = MODEL_EXTRACTION_RULES.lower()
    assert "do not paraphrase" in rules
    assert "do not return or infer character offsets" in rules
    assert "do not invent clinical effective time" in rules
    assert "do not infer" in rules
    assert "never resolve contradictory" in rules

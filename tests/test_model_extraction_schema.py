from app.extractors.model_schema import MODEL_EXTRACTION_RULES, ModelCandidate, ModelExtractionResponse


def test_model_schema_retains_exact_evidence_contract():
    item = ModelCandidate(
        fact_type="allergy",
        value_original="Penicillin",
        evidence_start=10,
        evidence_end=20,
        evidence_quote="Penicillin",
        confidence=0.9,
    )
    candidate = item.to_candidate()
    assert candidate.evidence_start == 10
    assert candidate.evidence_end == 20
    assert candidate.evidence_quote == "Penicillin"


def test_empty_response_is_valid_when_model_cannot_support_a_fact():
    response = ModelExtractionResponse()
    assert response.candidates == []


def test_model_rules_forbid_paraphrased_evidence_and_medical_guessing():
    rules = MODEL_EXTRACTION_RULES.lower()
    assert "do not paraphrase" in rules
    assert "do not infer" in rules
    assert "never resolve contradictory" in rules

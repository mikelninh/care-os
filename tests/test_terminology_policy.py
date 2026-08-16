from app.terminology_policy import CodingEvidence, TerminologyEvidenceStatus


def test_loinc_requires_separate_terminology_validation_evidence():
    coding = CodingEvidence(system="http://loinc.org", code="2160-0")
    assert coding.ignored_by_isik_reference_validator is True
    assert coding.evidence_status == TerminologyEvidenceStatus.REQUIRES_EXTERNAL_VALIDATION
    assert coding.safe_to_claim_terminology_validated is False


def test_snomed_value_set_requires_separate_validation_evidence():
    coding = CodingEvidence(
        system="http://snomed.info/sct",
        code="123456",
        value_set="https://gematik.de/fhir/isik/ValueSet/DiagnosesSCT",
    )
    assert coding.evidence_status == TerminologyEvidenceStatus.REQUIRES_EXTERNAL_VALIDATION


def test_external_validator_evidence_makes_claim_explicit_and_versioned():
    coding = CodingEvidence(
        system="http://loinc.org",
        code="2160-0",
        external_validator="hospital-terminology-server",
        external_validator_version="2026-08",
        validated=True,
    )
    assert coding.evidence_status == TerminologyEvidenceStatus.VALIDATED_EXTERNALLY
    assert coding.safe_to_claim_terminology_validated is True


def test_unlisted_system_is_not_automatically_claimed_valid():
    coding = CodingEvidence(system="urn:example:local", code="ABC")
    assert coding.evidence_status == TerminologyEvidenceStatus.NOT_APPLICABLE
    assert coding.safe_to_claim_terminology_validated is False

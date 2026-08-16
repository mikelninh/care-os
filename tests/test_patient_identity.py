from app.patient_identity import (
    IdentifierStrength,
    IdentityDecision,
    PatientIdentifier,
    PatientIdentityRecord,
    resolve_patient_identity,
)


def strong(system: str, value: str, issuer="hospital-a") -> PatientIdentifier:
    return PatientIdentifier(system=system, value=value, issuer=issuer, strength=IdentifierStrength.STRONG, verified=True)


def record(ref: str, identifiers=None, name=None, dob=None):
    return PatientIdentityRecord(local_ref=ref, identifiers=identifiers or [], display_name=name, birth_date=dob)


def test_unique_verified_strong_identifier_allows_exact_attachment():
    incoming = record("incoming", [strong("urn:mrn", "123")])
    candidates = [record("p1", [strong("urn:mrn", "123")]), record("p2", [strong("urn:mrn", "999")])]
    decision = resolve_patient_identity(incoming, candidates)
    assert decision.decision == IdentityDecision.EXACT
    assert decision.candidate_ref == "p1"
    assert decision.automatic_attachment_allowed is True


def test_same_name_and_dob_without_strong_identifier_never_auto_merges():
    incoming = record("incoming", name="Michael Bauer", dob="1970-01-01")
    candidates = [record("p1", name="Michael Bauer", dob="1970-01-01")]
    decision = resolve_patient_identity(incoming, candidates)
    assert decision.decision == IdentityDecision.REVIEW
    assert decision.automatic_attachment_allowed is False


def test_one_strong_match_plus_conflicting_strong_identifier_blocks():
    incoming = record("incoming", [strong("urn:mrn", "123"), strong("urn:kvnr", "A111")])
    candidate = record("p1", [strong("urn:mrn", "123"), strong("urn:kvnr", "B222")])
    decision = resolve_patient_identity(incoming, [candidate])
    assert decision.decision == IdentityDecision.CONFLICT
    assert decision.automatic_attachment_allowed is False


def test_strong_identifier_mapping_to_multiple_candidates_blocks():
    incoming = record("incoming", [strong("urn:mrn", "123")])
    candidates = [record("p1", [strong("urn:mrn", "123")]), record("p2", [strong("urn:mrn", "123")])]
    decision = resolve_patient_identity(incoming, candidates)
    assert decision.decision == IdentityDecision.CONFLICT


def test_unverified_identifier_does_not_become_strong_evidence():
    incoming = record("incoming", [PatientIdentifier(system="urn:mrn", value="123", strength=IdentifierStrength.STRONG, verified=False)])
    candidate = record("p1", [strong("urn:mrn", "123")])
    decision = resolve_patient_identity(incoming, [candidate])
    assert decision.decision == IdentityDecision.NO_MATCH

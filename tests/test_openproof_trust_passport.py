import json

from app.openproof_trust_passport import create_trust_passport, verify_trust_passport


def synthetic_trust(**overrides):
    trust = {
        "subject_id": "clinician-synthetic-001",
        "professional": {
            "full_name": "Dr Synthetic",
            "licence_number": "SYNTH-LIC-12345",
            "licence_active": True,
            "role_authorised": True,
            "valid_until_day": 21000,
        },
        "governance": {
            "consent_valid": True,
            "privacy_review_current": True,
            "security_review_current": True,
            "internal_review_notes": "private governance note",
        },
        # Included only to prove the public projection does not leak arbitrary
        # private witness fields. Production callers MUST NOT put PHI into a
        # Trust Passport witness at all.
        "forbidden_patient_context": {
            "mrn": "MRN-SYNTH-999",
            "diagnosis": "synthetic diagnosis",
        },
    }
    for section, values in overrides.items():
        trust[section] = {**trust.get(section, {}), **values}
    return trust


def scope():
    return {"hospital": "synthetic-hospital", "workflow": "morning-review", "role": "physician"}


def test_trust_passport_passes_without_leaking_raw_credentials_or_phi():
    proof = create_trust_passport(
        synthetic_trust(),
        scope=scope(),
        nonce="fixed-test-nonce",
        current_day=20693,
    )

    public = json.dumps(proof, sort_keys=True)
    assert "Dr Synthetic" not in public
    assert "SYNTH-LIC-12345" not in public
    assert "private governance note" not in public
    assert "MRN-SYNTH-999" not in public
    assert "synthetic diagnosis" not in public
    assert proof["decision"] == "TRUST_CONDITIONS_MET"
    assert verify_trust_passport(proof) == {"ok": True, "errors": []}


def test_missing_consent_fails_closed():
    proof = create_trust_passport(
        synthetic_trust(governance={"consent_valid": False}),
        scope=scope(),
        nonce="n2",
        current_day=20693,
    )
    result = verify_trust_passport(proof)
    assert proof["decision"] == "REVIEW_REQUIRED"
    assert result["ok"] is False
    assert "predicate failed: consent_valid" in result["errors"]


def test_expired_credential_fails_closed():
    proof = create_trust_passport(
        synthetic_trust(professional={"valid_until_day": 20000}),
        scope=scope(),
        nonce="n3",
        current_day=20693,
    )
    result = verify_trust_passport(proof)
    assert result["ok"] is False
    assert "predicate failed: credential_current" in result["errors"]


def test_scope_binding_prevents_cross_workflow_reuse():
    proof = create_trust_passport(
        synthetic_trust(),
        scope=scope(),
        nonce="n4",
        current_day=20693,
    )
    result = verify_trust_passport(proof, expected_scope_hash="sha256:not-the-same-workflow")
    assert result["ok"] is False
    assert "scope mismatch" in result["errors"]


def test_raw_disclosure_is_rejected():
    proof = create_trust_passport(
        synthetic_trust(),
        scope=scope(),
        nonce="n5",
        current_day=20693,
    )
    proof["disclosures"] = {"professional.licence_number": "SYNTH-LIC-12345"}
    result = verify_trust_passport(proof)
    assert result["ok"] is False
    assert "trust passport must not disclose raw claims" in result["errors"]

"""CareOS × OpenProof Trust Passport MVP.

The passport proves bounded trust/readiness predicates. It must not carry raw
clinical data and it never becomes a clinical decision or source of truth.

`careos-trust-local-v0` is a local commitment/predicate backend for integration
and leakage tests. Production proof claims require issuer-bound credentials and
Midnight/Compact ZK verification.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any

OPENPROOF_VERSION = "openproof/0.1"
PURPOSE = "careos.trust-passport"
BACKEND = "careos-trust-local-v0"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def create_trust_passport(
    private_trust: dict[str, Any],
    *,
    scope: dict[str, Any],
    nonce: str,
    current_day: int,
) -> dict[str, Any]:
    """Create a public trust projection with no PHI/raw credential disclosure."""
    if not nonce:
        raise ValueError("nonce required")
    if not scope.get("hospital") or not scope.get("workflow"):
        raise ValueError("hospital and workflow scope required")

    predicates = [
        {"id": "licence_active", "claim": "professional.licence_active", "op": "eq_true", "passed": private_trust.get("professional", {}).get("licence_active") is True},
        {"id": "role_authorised", "claim": "professional.role_authorised", "op": "eq_true", "passed": private_trust.get("professional", {}).get("role_authorised") is True},
        {"id": "consent_valid", "claim": "governance.consent_valid", "op": "eq_true", "passed": private_trust.get("governance", {}).get("consent_valid") is True},
        {"id": "privacy_review_current", "claim": "governance.privacy_review_current", "op": "eq_true", "passed": private_trust.get("governance", {}).get("privacy_review_current") is True},
        {"id": "security_review_current", "claim": "governance.security_review_current", "op": "eq_true", "passed": private_trust.get("governance", {}).get("security_review_current") is True},
        {
            "id": "credential_current",
            "claim": "professional.valid_until_day",
            "op": "gte",
            "passed": isinstance(private_trust.get("professional", {}).get("valid_until_day"), int)
            and private_trust["professional"]["valid_until_day"] >= current_day,
        },
    ]

    private_witness = {"trust": private_trust, "scope": scope}
    scope_hash = f"sha256:{_digest(_canonical(scope))}"
    return {
        "openproof": OPENPROOF_VERSION,
        "backend": BACKEND,
        "purpose": PURPOSE,
        "subject": private_trust.get("subject_id", "anonymous-bounded-subject"),
        "scope_hash": scope_hash,
        "claims_commitment": f"sha256:{_digest(f'{_canonical(private_witness)}:{nonce}')}",
        "predicate_results": predicates,
        "disclosures": {},
        "decision": "TRUST_CONDITIONS_MET" if all(x["passed"] for x in predicates) else "REVIEW_REQUIRED",
        "clinical_boundary": "trust_passport_is_not_clinical_truth_or_clinical_approval",
        "data_boundary": "no_patient_record_or_raw_clinical_data_in_proof",
    }


def verify_trust_passport(
    proof: dict[str, Any],
    *,
    expected_scope_hash: str | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    if proof.get("openproof") != OPENPROOF_VERSION:
        errors.append("openproof version mismatch")
    if proof.get("purpose") != PURPOSE:
        errors.append("purpose mismatch")
    if expected_scope_hash and proof.get("scope_hash") != expected_scope_hash:
        errors.append("scope mismatch")
    if proof.get("disclosures") not in ({}, None):
        errors.append("trust passport must not disclose raw claims")
    if not str(proof.get("claims_commitment", "")).startswith("sha256:"):
        errors.append("claims commitment missing")
    if proof.get("clinical_boundary") != "trust_passport_is_not_clinical_truth_or_clinical_approval":
        errors.append("clinical authority boundary missing")
    if proof.get("data_boundary") != "no_patient_record_or_raw_clinical_data_in_proof":
        errors.append("clinical data boundary missing")

    required = {
        "licence_active",
        "role_authorised",
        "consent_valid",
        "privacy_review_current",
        "security_review_current",
        "credential_current",
    }
    results = {item.get("id"): item for item in proof.get("predicate_results", [])}
    missing = required - set(results)
    if missing:
        errors.append(f"missing predicates: {sorted(missing)}")
    for predicate_id in required & set(results):
        if results[predicate_id].get("passed") is not True:
            errors.append(f"predicate failed: {predicate_id}")
    if proof.get("decision") != "TRUST_CONDITIONS_MET":
        errors.append("trust conditions not met")

    return {"ok": not errors, "errors": errors}

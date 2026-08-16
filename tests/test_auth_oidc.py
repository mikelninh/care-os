from datetime import datetime, timedelta, timezone

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import ValidationError

from app.auth_oidc import AuthenticationFailed, OIDCConfig, OIDCVerifier


@pytest.fixture(scope="module")
def keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_jwk = jwt.algorithms.RSAAlgorithm.to_jwk(private.public_key(), as_dict=True)
    public_jwk.update({"kid": "careos-test", "alg": "RS256", "use": "sig"})
    signing_key = jwt.PyJWK.from_dict(public_jwk)
    return private, signing_key


def config() -> OIDCConfig:
    return OIDCConfig(
        issuer="https://id.hospital.example/",
        audience="careos",
        jwks_uri="https://id.hospital.example/.well-known/jwks.json",
        leeway_seconds=0,
    )


def token(private, **overrides):
    now = datetime.now(timezone.utc)
    claims = {
        "iss": "https://id.hospital.example/",
        "aud": "careos",
        "sub": "doctor-123",
        "exp": now + timedelta(minutes=5),
        "iat": now,
    }
    claims.update(overrides)
    return jwt.encode(claims, private, algorithm="RS256", headers={"kid": "careos-test"})


def verifier(signing_key) -> OIDCVerifier:
    return OIDCVerifier(config(), resolver=lambda _: signing_key)


def test_valid_signed_identity_is_verified(keys):
    private, signing_key = keys
    identity = verifier(signing_key).verify(token(private))
    assert identity.subject == "doctor-123"
    assert identity.issuer == "https://id.hospital.example/"
    assert identity.audience == "careos"


def test_wrong_audience_fails_closed(keys):
    private, signing_key = keys
    with pytest.raises(AuthenticationFailed):
        verifier(signing_key).verify(token(private, aud="different-app"))


def test_wrong_issuer_fails_closed(keys):
    private, signing_key = keys
    with pytest.raises(AuthenticationFailed):
        verifier(signing_key).verify(token(private, iss="https://evil.example/"))


def test_expired_token_fails_closed(keys):
    private, signing_key = keys
    with pytest.raises(AuthenticationFailed):
        verifier(signing_key).verify(token(private, exp=datetime.now(timezone.utc) - timedelta(seconds=1)))


def test_missing_required_claim_fails_closed(keys):
    private, signing_key = keys
    now = datetime.now(timezone.utc)
    missing_exp = jwt.encode(
        {"iss": config().issuer, "aud": "careos", "sub": "doctor-123", "iat": now},
        private,
        algorithm="RS256",
        headers={"kid": "careos-test"},
    )
    with pytest.raises(AuthenticationFailed):
        verifier(signing_key).verify(missing_exp)


def test_symmetric_or_none_algorithms_are_rejected_at_configuration():
    with pytest.raises(ValidationError):
        OIDCConfig(issuer="https://id.example", audience="careos", jwks_uri="https://id.example/jwks", algorithms=("HS256",))
    with pytest.raises(ValidationError):
        OIDCConfig(issuer="https://id.example", audience="careos", jwks_uri="https://id.example/jwks", algorithms=("none",))


def test_non_https_production_oidc_endpoints_are_rejected():
    with pytest.raises(ValidationError):
        OIDCConfig(issuer="http://id.example", audience="careos", jwks_uri="https://id.example/jwks")

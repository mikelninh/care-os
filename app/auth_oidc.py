from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import jwt
from jwt import PyJWKClient
from pydantic import BaseModel, Field, field_validator


class OIDCConfig(BaseModel):
    issuer: str = Field(min_length=1)
    audience: str = Field(min_length=1)
    jwks_uri: str = Field(min_length=1)
    algorithms: tuple[str, ...] = ("RS256",)
    leeway_seconds: int = Field(default=30, ge=0, le=120)

    @field_validator("algorithms")
    @classmethod
    def reject_symmetric_algorithms(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if not value:
            raise ValueError("at least one signing algorithm is required")
        if any(alg.upper().startswith("HS") or alg.lower() == "none" for alg in value):
            raise ValueError("CareOS hospital OIDC verification forbids symmetric/none algorithms")
        return value

    @field_validator("issuer", "jwks_uri")
    @classmethod
    def require_https(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("production OIDC issuer/JWKS URI must use https")
        # OIDC issuer identifiers are exact strings. Do not normalize slashes/case.
        return value


@dataclass(frozen=True)
class AuthenticatedIdentity:
    subject: str
    issuer: str
    audience: str | list[str]
    claims: dict[str, Any]


class AuthenticationFailed(ValueError):
    pass


SigningKeyResolver = Callable[[str], Any]


class OIDCVerifier:
    """Verify hospital-issued JWTs before any CareOS authorization decision.

    Authentication and authorization are deliberately separate. A valid JWT proves an
    identity/issuer/audience relationship; it does *not* by itself prove that the user
    may access a particular patient. Patient/treatment-context authorization remains in
    the access-policy layer and must use trusted hospital mappings/context services.
    """

    def __init__(self, config: OIDCConfig, resolver: SigningKeyResolver | None = None):
        self.config = config
        if resolver is None:
            client = PyJWKClient(config.jwks_uri)
            self._resolver: SigningKeyResolver = client.get_signing_key_from_jwt
        else:
            self._resolver = resolver

    def verify(self, token: str) -> AuthenticatedIdentity:
        if not token or token.count(".") != 2:
            raise AuthenticationFailed("malformed bearer token")
        try:
            signing_key = self._resolver(token)
            claims = jwt.decode(
                token,
                signing_key,
                algorithms=list(self.config.algorithms),
                issuer=self.config.issuer,
                audience=self.config.audience,
                leeway=self.config.leeway_seconds,
                options={
                    "require": ["exp", "iss", "sub", "aud"],
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iss": True,
                    "verify_aud": True,
                },
            )
        except jwt.PyJWTError as exc:
            raise AuthenticationFailed(type(exc).__name__) from exc
        except Exception as exc:
            # JWKS/network/resolver errors fail closed and do not expose provider details.
            raise AuthenticationFailed("signing key unavailable or invalid") from exc

        subject = claims.get("sub")
        issuer = claims.get("iss")
        audience = claims.get("aud")
        if not isinstance(subject, str) or not subject:
            raise AuthenticationFailed("invalid subject")
        return AuthenticatedIdentity(subject=subject, issuer=issuer, audience=audience, claims=claims)

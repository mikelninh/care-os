from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .agent_policy import AgentDelegation

TOKEN_TYPE = "CAREOS-AGENT-DELEGATION"
ALGORITHM = "EdDSA"


class DelegationTokenError(ValueError):
    pass


@dataclass(frozen=True)
class VerifiedDelegation:
    delegation_id: str
    issuer: str
    audience: str
    key_id: str
    delegation: AgentDelegation


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode((value + padding).encode("ascii"))
    except Exception as exc:  # pragma: no cover - defensive boundary
        raise DelegationTokenError("invalid base64url") from exc


def _canonical_json(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def issue_delegation_token(
    delegation: AgentDelegation,
    *,
    private_key: Ed25519PrivateKey,
    issuer: str,
    audience: str,
    key_id: str,
    delegation_id: str | None = None,
) -> str:
    """Issue a compact signed delegation token.

    The private key belongs to an approved delegation authority, not to the model.
    This contract deliberately does not carry a clinician bearer token.
    """

    if not issuer.strip() or not audience.strip() or not key_id.strip():
        raise DelegationTokenError("issuer, audience and key_id are required")

    header = {"alg": ALGORITHM, "kid": key_id, "typ": TOKEN_TYPE}
    payload = {
        "iss": issuer,
        "aud": audience,
        "jti": delegation_id or str(uuid4()),
        "delegation": delegation.model_dump(mode="json"),
    }
    header_part = _b64url_encode(_canonical_json(header))
    payload_part = _b64url_encode(_canonical_json(payload))
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    signature = private_key.sign(signing_input)
    return f"{header_part}.{payload_part}.{_b64url_encode(signature)}"


def verify_delegation_token(
    token: str,
    *,
    public_keys: dict[str, Ed25519PublicKey],
    expected_issuer: str,
    expected_audience: str,
) -> VerifiedDelegation:
    """Verify signature, token type, issuer/audience and delegation schema.

    Expiry/not-before is evaluated again at each tool request by `agent_policy` so a
    token that was valid at process start cannot remain valid after expiry.
    Replay prevention requires a production execution/delegation store and is an A1
    blocker until that real infrastructure exists.
    """

    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError as exc:
        raise DelegationTokenError("delegation token must have three parts") from exc

    try:
        header = json.loads(_b64url_decode(header_part))
        payload = json.loads(_b64url_decode(payload_part))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise DelegationTokenError("invalid delegation token json") from exc

    if header.get("typ") != TOKEN_TYPE or header.get("alg") != ALGORITHM:
        raise DelegationTokenError("unexpected delegation token type or algorithm")

    key_id = str(header.get("kid") or "")
    public_key = public_keys.get(key_id)
    if public_key is None:
        raise DelegationTokenError("unknown delegation signing key")

    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    try:
        public_key.verify(_b64url_decode(signature_part), signing_input)
    except InvalidSignature as exc:
        raise DelegationTokenError("invalid delegation signature") from exc

    if payload.get("iss") != expected_issuer:
        raise DelegationTokenError("unexpected delegation issuer")
    if payload.get("aud") != expected_audience:
        raise DelegationTokenError("unexpected delegation audience")

    delegation_id = str(payload.get("jti") or "")
    if not delegation_id:
        raise DelegationTokenError("delegation token missing unique id")

    try:
        delegation = AgentDelegation.model_validate(payload["delegation"])
    except (KeyError, ValueError, TypeError) as exc:
        raise DelegationTokenError("invalid delegation payload") from exc

    return VerifiedDelegation(
        delegation_id=delegation_id,
        issuer=expected_issuer,
        audience=expected_audience,
        key_id=key_id,
        delegation=delegation,
    )

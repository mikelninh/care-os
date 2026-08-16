from datetime import datetime, timedelta, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.agent_delegation import DelegationTokenError, issue_delegation_token, verify_delegation_token
from app.agent_policy import AgentDelegation, AgentOperation


NOW = datetime(2026, 8, 16, 18, 0, tzinfo=timezone.utc)


def delegation():
    return AgentDelegation(
        agent_id="careos-rounds-agent",
        agent_version="1.0.0",
        delegating_actor="doctor-123",
        organisation="sjk",
        patient_ref="patient-1",
        encounter_ref="encounter-1",
        task_id="morning-review",
        allowed_tools={"read-clinical-context"},
        allowed_operations={AgentOperation.READ},
        allowed_data_categories={"microbiology"},
        issued_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=5),
    )


def test_ed25519_delegation_round_trip():
    private = Ed25519PrivateKey.generate()
    token = issue_delegation_token(
        delegation(),
        private_key=private,
        issuer="careos-delegation-authority",
        audience="careos-agent-gateway",
        key_id="key-1",
        delegation_id="delegation-123",
    )
    verified = verify_delegation_token(
        token,
        public_keys={"key-1": private.public_key()},
        expected_issuer="careos-delegation-authority",
        expected_audience="careos-agent-gateway",
    )
    assert verified.delegation_id == "delegation-123"
    assert verified.delegation.patient_ref == "patient-1"
    assert verified.delegation.agent_id == "careos-rounds-agent"


def test_tampered_delegation_is_rejected():
    private = Ed25519PrivateKey.generate()
    token = issue_delegation_token(
        delegation(),
        private_key=private,
        issuer="issuer",
        audience="gateway",
        key_id="key-1",
    )
    header, payload, signature = token.split(".")
    tampered_payload = ("A" if payload[0] != "A" else "B") + payload[1:]
    tampered = ".".join([header, tampered_payload, signature])
    with pytest.raises(DelegationTokenError):
        verify_delegation_token(
            tampered,
            public_keys={"key-1": private.public_key()},
            expected_issuer="issuer",
            expected_audience="gateway",
        )


def test_wrong_audience_is_rejected():
    private = Ed25519PrivateKey.generate()
    token = issue_delegation_token(
        delegation(), private_key=private, issuer="issuer", audience="gateway", key_id="key-1"
    )
    with pytest.raises(DelegationTokenError, match="audience"):
        verify_delegation_token(
            token,
            public_keys={"key-1": private.public_key()},
            expected_issuer="issuer",
            expected_audience="other-gateway",
        )


def test_unknown_signing_key_is_rejected():
    private = Ed25519PrivateKey.generate()
    token = issue_delegation_token(
        delegation(), private_key=private, issuer="issuer", audience="gateway", key_id="key-1"
    )
    with pytest.raises(DelegationTokenError, match="unknown"):
        verify_delegation_token(
            token,
            public_keys={},
            expected_issuer="issuer",
            expected_audience="gateway",
        )

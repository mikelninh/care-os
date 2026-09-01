from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, Field


class Authenticity(BaseModel):
    status: Literal["unverified", "original_as_received", "verified_issuer"]
    method: str = Field(min_length=1)


class Integrity(BaseModel):
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    verified: bool
    version: str = Field(min_length=1)
    captured_at: str = Field(min_length=1)


class Provenance(BaseModel):
    source_system: str = Field(min_length=1)
    source_uri: str = Field(min_length=1)
    acquired_at: str = Field(min_length=1)


class Authority(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    version: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    status: Literal["authoritative", "case_specific"]


class EvidenceLocator(BaseModel):
    kind: Literal["page", "paragraph", "section", "row", "field", "record"]
    value: str = Field(min_length=1)


class Evidence(BaseModel):
    id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    locator: EvidenceLocator
    excerpt_hash: str = Field(pattern=r"^[a-f0-9]{64}$")


class Derivation(BaseModel):
    summary: str = Field(min_length=1)
    method: str = Field(min_length=1)
    evidence_ids: list[str] = Field(min_length=1)


class HumanDecision(BaseModel):
    required: Literal[True] = True
    status: Literal["pending", "approved", "rejected"] = "pending"
    actor_id: str | None = None
    at: str | None = None


class AuditAnchor(BaseModel):
    trace_id: str = Field(min_length=1)
    created_at: str = Field(min_length=1)


class TrustChainV1(BaseModel):
    version: Literal["trust-chain/v1"] = "trust-chain/v1"
    subject_type: str = Field(min_length=1)
    subject_id: str = Field(min_length=1)
    authenticity: Authenticity
    integrity: Integrity
    provenance: Provenance
    authority: Authority
    evidence: list[Evidence] = Field(min_length=1)
    derivation: Derivation
    human_decision: HumanDecision
    audit: AuditAnchor


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def to_runtime_contract(chain: TrustChainV1) -> dict[str, Any]:
    return {
        "version": chain.version,
        "subject": {"type": chain.subject_type, "id": chain.subject_id},
        "authenticity": {"status": chain.authenticity.status, "method": chain.authenticity.method},
        "integrity": {
            "sha256": chain.integrity.sha256,
            "verified": chain.integrity.verified,
            "version": chain.integrity.version,
            "capturedAt": chain.integrity.captured_at,
        },
        "provenance": {
            "sourceSystem": chain.provenance.source_system,
            "sourceUri": chain.provenance.source_uri,
            "acquiredAt": chain.provenance.acquired_at,
        },
        "authority": {
            "id": chain.authority.id,
            "title": chain.authority.title,
            "version": chain.authority.version,
            "sourceUrl": chain.authority.source_url,
            "status": chain.authority.status,
        },
        "evidence": [
            {
                "id": item.id,
                "sourceId": item.source_id,
                "locator": {"kind": item.locator.kind, "value": item.locator.value},
                "excerptHash": item.excerpt_hash,
            }
            for item in chain.evidence
        ],
        "derivation": {
            "summary": chain.derivation.summary,
            "method": chain.derivation.method,
            "evidenceIds": list(chain.derivation.evidence_ids),
        },
        "humanDecision": {
            "required": chain.human_decision.required,
            "status": chain.human_decision.status,
            "actorId": chain.human_decision.actor_id,
            "at": chain.human_decision.at,
        },
        "audit": {"traceId": chain.audit.trace_id, "createdAt": chain.audit.created_at},
    }


def trust_chain_digest(chain: TrustChainV1) -> str:
    payload = json.dumps(to_runtime_contract(chain), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_text(payload)


def validate_consequential_action(chain: TrustChainV1, approved_by: str) -> list[str]:
    reasons: list[str] = []
    evidence_ids = {item.id for item in chain.evidence}
    if not chain.integrity.verified:
        reasons.append("integrity_not_verified")
    if chain.authenticity.status == "unverified":
        reasons.append("source_authenticity_unverified")
    if any(item_id not in evidence_ids for item_id in chain.derivation.evidence_ids):
        reasons.append("derivation_unknown_evidence")
    if chain.human_decision.status == "pending":
        reasons.append("human_decision_pending")
    elif chain.human_decision.status == "rejected":
        reasons.append("human_decision_rejected")
    if chain.human_decision.status != "approved":
        reasons.append("human_approval_not_recorded")
    if chain.human_decision.status == "approved" and (not chain.human_decision.actor_id or not chain.human_decision.at):
        reasons.append("approval_identity_required")
    if chain.human_decision.actor_id != approved_by:
        reasons.append("human_approval_mismatch")
    return list(dict.fromkeys(reasons))

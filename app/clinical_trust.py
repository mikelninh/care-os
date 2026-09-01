from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .access_policy import AccessRequest, UserContext, evaluate_access
from .clinical_truth import ClinicalFact, SourceKind
from .trust_chain import (
    AuditAnchor,
    Authenticity,
    Authority,
    Derivation,
    Evidence,
    EvidenceLocator,
    HumanDecision,
    Integrity,
    Provenance,
    TrustChainV1,
    sha256_text,
    trust_chain_digest,
    validate_consequential_action,
)


POLICY_PATH = Path(__file__).resolve().parents[1] / "data" / "trust" / "clinical-review-policy-v1.json"
QUALIFIED_REVIEW_ROLES = {"doctor", "pharmacist"}


class ClinicalFindingRecord(BaseModel):
    finding_id: str = Field(min_length=1)
    patient_ref: str = Field(min_length=1)
    finding_type: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    fact_ids: tuple[str, ...]
    source_snapshot_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    chain: TrustChainV1
    chain_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    created_at: str = Field(min_length=1)


class ClinicalDecisionRecord(BaseModel):
    decision_id: str = Field(min_length=1)
    finding_id: str = Field(min_length=1)
    status: Literal["approved", "rejected"]
    actor_id: str = Field(min_length=1)
    actor_roles: tuple[str, ...]
    note: str = ""
    at: str = Field(min_length=1)
    chain: TrustChainV1
    chain_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class GateResult(BaseModel):
    allow: bool
    reasons: list[str]
    decision_id: str | None = None


class InMemoryClinicalTrustLedger:
    """Append-only reference ledger for synthetic/deidentified CareOS review flows.

    This is deliberately not a production PHI store. Production remains blocked by
    CareOS release gates until a durable provider-approved ledger exists.
    """

    def __init__(self) -> None:
        self._findings: dict[str, ClinicalFindingRecord] = {}
        self._decisions: dict[str, list[ClinicalDecisionRecord]] = {}

    def add_finding(self, finding: ClinicalFindingRecord) -> None:
        if finding.finding_id in self._findings:
            raise ValueError("clinical_finding_already_exists")
        self._findings[finding.finding_id] = finding.model_copy(deep=True)

    def add_decision(self, decision: ClinicalDecisionRecord) -> None:
        if decision.finding_id not in self._findings:
            raise ValueError("clinical_finding_not_found")
        existing = self._decisions.setdefault(decision.finding_id, [])
        if any(item.decision_id == decision.decision_id for item in existing):
            raise ValueError("clinical_decision_already_exists")
        existing.append(decision.model_copy(deep=True))

    def finding(self, finding_id: str) -> ClinicalFindingRecord | None:
        item = self._findings.get(finding_id)
        return item.model_copy(deep=True) if item else None

    def decisions(self, finding_id: str) -> list[ClinicalDecisionRecord]:
        return [item.model_copy(deep=True) for item in self._decisions.get(finding_id, [])]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _policy() -> dict[str, object]:
    data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    for key in ("id", "title", "version", "source_url", "status"):
        if not data.get(key):
            raise ValueError(f"clinical_review_policy_missing_{key}")
    return data


def _source_id(fact: ClinicalFact) -> str:
    source = fact.source
    if source.document_id:
        return f"{source.system}:document:{source.document_id}"
    version = f"@{source.resource_version}" if source.resource_version else ""
    return f"{source.system}:{source.resource_type}/{source.resource_id}{version}"


def _fact_payload(fact: ClinicalFact) -> dict[str, object]:
    return {
        "fact_id": fact.fact_id,
        "patient_ref": fact.patient_ref,
        "fact_type": fact.fact_type,
        "value_original": fact.value_original,
        "unit_original": fact.unit_original,
        "effective_time": fact.effective_time,
        "recorded_time": fact.recorded_time,
        "assertion_stage": fact.assertion_stage.value,
        "source": fact.source.model_dump(mode="json"),
        "transformer": fact.transformer,
        "transformer_version": fact.transformer_version,
    }


def _snapshot_sha(facts: list[ClinicalFact]) -> str:
    payload = [_fact_payload(fact) for fact in sorted(facts, key=lambda item: item.fact_id)]
    return sha256_text(_canonical(payload))


def _evidence_hash(fact: ClinicalFact) -> str:
    return sha256_text(_canonical({
        "source_id": _source_id(fact),
        "locator": fact.source.evidence_span,
        "value_original": fact.value_original,
        "unit_original": fact.unit_original,
    }))


def build_clinical_finding(
    *,
    finding_id: str,
    finding_type: str,
    summary: str,
    facts: list[ClinicalFact],
    trace_id: str,
    created_at: str | None = None,
) -> ClinicalFindingRecord:
    if not facts:
        raise ValueError("clinical_finding_requires_evidence")
    patient_refs = {fact.patient_ref for fact in facts}
    if len(patient_refs) != 1:
        raise ValueError("clinical_finding_cross_patient_evidence")
    if len({fact.fact_id for fact in facts}) != len(facts):
        raise ValueError("clinical_finding_duplicate_fact")

    # The general ClinicalFact model accepts record-level FHIR provenance. A
    # consequential/review finding is stricter: every used fact needs an exact
    # element/text locator so the reviewer can independently jump to the source.
    for fact in facts:
        if not fact.provenance_complete:
            raise ValueError(f"clinical_provenance_incomplete:{fact.fact_id}")
        if not (fact.source.evidence_span or "").strip():
            raise ValueError(f"clinical_exact_evidence_locator_required:{fact.fact_id}")

    timestamp = created_at or _now()
    patient_ref = next(iter(patient_refs))
    policy = _policy()
    snapshot_sha = _snapshot_sha(facts)
    evidence: list[Evidence] = []
    for fact in facts:
        locator_kind: Literal["section", "field"] = (
            "section" if fact.source.kind == SourceKind.DOCUMENT else "field"
        )
        evidence.append(Evidence(
            id=f"fact:{fact.fact_id}",
            source_id=_source_id(fact),
            locator=EvidenceLocator(kind=locator_kind, value=str(fact.source.evidence_span)),
            excerpt_hash=_evidence_hash(fact),
        ))

    chain = TrustChainV1(
        subject_type="clinical_finding",
        subject_id=finding_id,
        authenticity=Authenticity(
            status="original_as_received",
            method="CareOS preserves source identity as received; issuer authenticity is not implied unless separately verified.",
        ),
        integrity=Integrity(
            sha256=snapshot_sha,
            verified=True,
            version="clinical-source-snapshot/v1",
            captured_at=timestamp,
        ),
        provenance=Provenance(
            source_system="careos-clinical-context",
            source_uri=f"careos://patient/{patient_ref}/findings/{finding_id}",
            acquired_at=timestamp,
        ),
        authority=Authority(
            id=str(policy["id"]),
            title=str(policy["title"]),
            version=str(policy["version"]),
            source_url=str(policy["source_url"]),
            status=str(policy["status"]),
        ),
        evidence=evidence,
        derivation=Derivation(
            summary=summary,
            method="source-bound-clinical-review-preparation/v1",
            evidence_ids=[item.id for item in evidence],
        ),
        human_decision=HumanDecision(),
        audit=AuditAnchor(trace_id=trace_id, created_at=timestamp),
    )
    return ClinicalFindingRecord(
        finding_id=finding_id,
        patient_ref=patient_ref,
        finding_type=finding_type,
        summary=summary,
        fact_ids=tuple(sorted(fact.fact_id for fact in facts)),
        source_snapshot_sha256=snapshot_sha,
        chain=chain,
        chain_sha256=trust_chain_digest(chain),
        created_at=timestamp,
    )


def verify_clinical_sources(finding: ClinicalFindingRecord, current_facts: list[ClinicalFact]) -> list[str]:
    reasons: list[str] = []
    by_id = {fact.fact_id: fact for fact in current_facts}
    if set(by_id) != set(finding.fact_ids):
        reasons.append("clinical_evidence_set_changed")
        return reasons
    if any(fact.patient_ref != finding.patient_ref for fact in current_facts):
        reasons.append("clinical_patient_binding_changed")
    for fact in current_facts:
        if not (fact.source.evidence_span or "").strip():
            reasons.append(f"clinical_exact_locator_missing:{fact.fact_id}")
    if _snapshot_sha(current_facts) != finding.source_snapshot_sha256:
        reasons.append("clinical_source_drift")

    expected_evidence = {item.id: item for item in finding.chain.evidence}
    for fact in current_facts:
        evidence = expected_evidence.get(f"fact:{fact.fact_id}")
        if not evidence or evidence.source_id != _source_id(fact) or evidence.excerpt_hash != _evidence_hash(fact):
            reasons.append(f"clinical_evidence_mismatch:{fact.fact_id}")

    policy = _policy()
    if (
        finding.chain.authority.id != policy["id"]
        or finding.chain.authority.version != policy["version"]
        or finding.chain.authority.source_url != policy["source_url"]
    ):
        reasons.append("clinical_authority_drift")
    return list(dict.fromkeys(reasons))


def build_clinical_decision(
    finding: ClinicalFindingRecord,
    *,
    actor: UserContext,
    status: Literal["approved", "rejected"],
    decision_id: str,
    current_facts: list[ClinicalFact],
    note: str = "",
    at: str | None = None,
) -> ClinicalDecisionRecord:
    access = evaluate_access(actor, AccessRequest(patient_ref=finding.patient_ref))
    if not access.allowed:
        raise PermissionError(f"clinical_reviewer_access_denied:{access.reason}")
    if not (actor.roles & QUALIFIED_REVIEW_ROLES):
        raise PermissionError("clinical_reviewer_not_qualified_for_finding")
    source_reasons = verify_clinical_sources(finding, current_facts)
    if source_reasons:
        raise ValueError("clinical_source_revalidation_failed:" + ",".join(source_reasons))

    timestamp = at or _now()
    chain = finding.chain.model_copy(deep=True)
    chain.human_decision = HumanDecision(
        status=status,
        actor_id=actor.subject,
        at=timestamp,
    )
    return ClinicalDecisionRecord(
        decision_id=decision_id,
        finding_id=finding.finding_id,
        status=status,
        actor_id=actor.subject,
        actor_roles=tuple(sorted(actor.roles)),
        note=note,
        at=timestamp,
        chain=chain,
        chain_sha256=trust_chain_digest(chain),
    )


def clinical_review_gate(
    finding: ClinicalFindingRecord,
    decisions: list[ClinicalDecisionRecord],
    current_facts: list[ClinicalFact],
) -> GateResult:
    reasons = verify_clinical_sources(finding, current_facts)
    if not decisions:
        return GateResult(allow=False, reasons=reasons + ["clinical_human_decision_pending"])
    latest = decisions[-1]
    if latest.finding_id != finding.finding_id:
        reasons.append("clinical_decision_finding_mismatch")
    if latest.status != "approved":
        reasons.append("clinical_human_decision_rejected")
    if not (set(latest.actor_roles) & QUALIFIED_REVIEW_ROLES):
        reasons.append("clinical_reviewer_not_qualified_for_finding")
    reasons.extend(validate_consequential_action(latest.chain, latest.actor_id))
    return GateResult(allow=not reasons, reasons=list(dict.fromkeys(reasons)), decision_id=latest.decision_id)


def clinical_production_gate(
    finding: ClinicalFindingRecord,
    decisions: list[ClinicalDecisionRecord],
    current_facts: list[ClinicalFact],
) -> GateResult:
    review = clinical_review_gate(finding, decisions, current_facts)
    reasons = list(review.reasons)
    # Deliberately non-overridable in the current CareOS release. Trust-chain
    # completeness proves reviewability; it does not prove clinical validation,
    # regulatory clearance, hospital governance or safe production write-back.
    reasons.extend([
        "clinical_production_release_not_proven",
        "clinical_writeback_disabled_by_release_policy",
    ])
    return GateResult(allow=False, reasons=list(dict.fromkeys(reasons)), decision_id=review.decision_id)

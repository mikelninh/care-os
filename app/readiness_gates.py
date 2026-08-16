from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class GateStatus(str, Enum):
    PASS = "pass"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    EXTERNAL_REVIEW = "external-review"


@dataclass(frozen=True)
class Gate:
    id: str
    name: str
    status: GateStatus
    claim: str
    evidence: tuple[str, ...]
    blockers: tuple[str, ...]
    owner_lane: str


GATES: tuple[Gate, ...] = (
    Gate(
        id="G0",
        name="Scope & safety boundary",
        status=GateStatus.EXTERNAL_REVIEW,
        claim="Intended-use boundary, federated target architecture and safety case are written; qualified independent review is still required.",
        evidence=("docs/ARCHITECTURE_V1.md", "docs/SAFETY_CASE.md", "docs/REGULATORY_BASELINE_DE.md", "docs/EXTERNAL_REVIEW_BRIEF.md"),
        blockers=("independent MDR/MDSW qualification/classification assessment", "named clinical-safety reviewer findings and sign-off for pilot scope"),
        owner_lane="product + clinical safety + regulatory",
    ),
    Gate(
        id="G1",
        name="Clinical truth",
        status=GateStatus.BLOCKED,
        claim="Clinical truth now separates source extraction, evidence admission and deterministic reconciliation. Frozen Holdout #3 shows 100% benchmark precision, 100% provenance, zero observed unsupported/wrong-source claims and zero critical silent misses, but only 26.3% micro recall and 100% review burden, so the release gate remains blocked.",
        evidence=(
            "app/clinical_truth.py",
            "app/patient_identity.py",
            "app/fhir_adapter.py",
            "app/document_pipeline.py",
            "app/reconciliation.py",
            "app/case_projection.py",
            "app/extractors/base.py",
            "app/extractors/conservative_de.py",
            "app/extractors/model_schema.py",
            "app/extractors/model_assisted.py",
            "app/contradictions.py",
            "app/unit_normalization.py",
            "benchmark/metrics.py",
            "benchmark/g1_dev.py",
            "benchmark/holdout3.py",
            ".github/workflows/g1-holdout3.yml",
            "tests/test_clinical_truth.py",
            "tests/test_patient_identity.py",
            "tests/test_fhir_truth.py",
            "tests/test_document_pipeline.py",
            "tests/test_verified_extraction.py",
            "tests/test_model_extraction_schema.py",
            "tests/test_model_assisted_extractor.py",
            "tests/test_reconciliation.py",
            "tests/test_holdout3.py",
            "tests/test_contradictions.py",
            "tests/test_unit_normalization.py",
            "docs/BENCHMARK.md",
            "docs/G1_MODEL_ASSISTED.md",
        ),
        blockers=(
            "raise recall substantially without tuning Frozen Holdout #3 or losing precision/provenance",
            "reduce review/abstention burden from the current 100% synthetic Holdout #3 rate",
            "evaluate the evidence-first model-assisted extractor on a fresh development corpus",
            "add governed temporal normalization and richer terminology normalization for document-derived facts",
            "freeze and evaluate a future untouched holdout only after the next extraction architecture is fixed",
            "obtain clinician-reviewed/de-identified evidence under appropriate governance before clinical claims",
        ),
        owner_lane="clinical data engineering",
    ),
    Gate(
        id="G2",
        name="German interoperability",
        status=GateStatus.PARTIAL,
        claim="Real FHIR transport, bounded same-origin Bundle pagination and pinned gematik ISiK5 profile-validation CI are proven. CareOS explicitly separates profile validation from terminology evidence; a real terminology service, synchronization semantics and hospital/vendor sandbox remain missing.",
        evidence=("app/fhir_adapter.py", "app/connectors/base.py", "app/connectors/fhir_connector.py", "app/terminology_policy.py", "tests/test_fhir_paging.py", "tests/test_connector_contract.py", "tests/test_terminology_policy.py", "docs/FHIR_INTEGRATION.md", "docs/CONNECTOR_SDK.md", "docs/TERMINOLOGY_VALIDATION.md", "integration/docker-compose.fhir.yml", "integration/isik5/Patient-careos-synthetic.json", ".github/workflows/isik5-validation.yml", "docs/SJK_INTEGRATION_DISCOVERY.md"),
        blockers=("real terminology validation for code systems/value sets excluded by the pinned ISiK validator", "one real SJK/KIS/LIS/vendor read-only sandbox", "resource version reconciliation/incremental synchronization", "end-to-end freshness semantics against a real source"),
        owner_lane="interoperability",
    ),
    Gate(
        id="G3",
        name="Privacy & security",
        status=GateStatus.PARTIAL,
        claim="Asymmetric OIDC JWT verification, fail-closed treatment-context policy, audited secure-read orchestration, runtime kill switch, keyed audit pseudonyms, tamper-evident local audit chaining and privacy data-flow design exist; production hospital integration and assurance remain incomplete.",
        evidence=("app/auth_oidc.py", "tests/test_auth_oidc.py", "app/access_policy.py", "tests/test_access_policy.py", "app/clinical_session.py", "tests/test_clinical_session.py", "app/kill_switch.py", "app/audit.py", "app/audit_chain.py", "tests/test_audit_security.py", "tests/test_audit_chain.py", "app/security_readiness.py", "app/deployment_policy.py", "app/__init__.py", "tests/test_deployment_policy.py", "docs/DATA_FLOW_AND_PRIVACY.md", "docs/DPIA_SUPPORT.md", "docs/AVV_DPA_REQUIREMENTS.md", "docs/THREAT_MODEL.md", "docs/PRODUCTION_READINESS.md"),
        blockers=("connect verifier to actual hospital IdP/SSO", "trusted role/org/treatment-context mapping and session/revocation behavior", "central immutable/independently protected audit", "KMS/secrets and production encryption", "hospital-specific DPIA/DSFA + agreements/approvals", "C5/customer-controls evidence where applicable", "independent penetration test"),
        owner_lane="security + privacy",
    ),
    Gate(
        id="G4",
        name="Production reliability",
        status=GateStatus.PARTIAL,
        claim="Current/stale/unavailable source semantics, bounded pagination, fail-visible connector errors, runtime kill switches, external-source/data-mode guards and a dedicated fail-closed safety CI workflow are proven in synthetic tests; target-environment resilience/recovery evidence is still missing.",
        evidence=("app/source_state.py", "tests/test_source_state.py", "app/fhir_adapter.py", "tests/test_fhir_paging.py", "app/connectors/fhir_connector.py", "app/kill_switch.py", "app/deployment_policy.py", "app/__init__.py", "tests/test_deployment_policy.py", "tests/test_clinical_session.py", ".github/workflows/safety-failure-injection.yml", "docs/DEPLOYMENT_RUNBOOK.md", "docs/INCIDENT_RESPONSE.md", "docs/SLO_POLICY.md", "docs/THREAT_MODEL.md"),
        blockers=("failure injection against actual KIS/FHIR/identity/audit/network dependencies", "freshness policies wired to every real source", "backup/restore evidence with measured RPO/RTO", "operational monitoring/alerting against approved SLOs", "incident/rollback exercise in target deployment"),
        owner_lane="platform/SRE",
    ),
    Gate(
        id="G5",
        name="Regulatory & quality system",
        status=GateStatus.EXTERNAL_REVIEW,
        claim="Safety boundary, regulatory baseline, risk register and change-control discipline are explicit; formal regulatory position and classification-appropriate QMS/lifecycle remain missing.",
        evidence=("docs/SAFETY_CASE.md", "docs/REGULATORY_BASELINE_DE.md", "docs/EXTERNAL_REVIEW_BRIEF.md", "docs/RISK_REGISTER.md", "docs/CHANGE_CONTROL.md"),
        blockers=("independent MDR/MDSW assessment", "AI Act applicability assessment", "EHDS applicability mapping by qualified reviewer where required", "reviewed clinical risk-management file", "QMS/lifecycle evidence appropriate to resulting classification"),
        owner_lane="regulatory + quality",
    ),
    Gate(
        id="G6",
        name="Invisible workflow integration",
        status=GateStatus.PARTIAL,
        claim="A short-lived authenticated organisation-, patient- and treatment-context-bound launch contract exists, with deterministic patient-identity rules and an SJK synthetic workflow reference; a real KIS/portal launcher and no-duplicate-work deployment are not yet proven.",
        evidence=("app/context_launch.py", "tests/test_context_launch.py", "app/patient_identity.py", "tests/test_patient_identity.py", "app/auth_oidc.py", "app/access_policy.py", "app/reference_environments.py", "tests/test_reference_environments.py", "share/sjk-infectiology/", "docs/SJK_TEAM_TEST_PROTOCOL.md"),
        blockers=("real hospital/KIS trusted context resolver/launcher", "same-patient context proven without duplicate manual search", "embedded/Citrix/VDI/managed-browser compatibility proof", "no-copy/no-duplicate-documentation workflow measured in real environment"),
        owner_lane="product + integration",
    ),
    Gate(
        id="G7",
        name="Hospital deployment kit",
        status=GateStatus.PARTIAL,
        claim="A coherent assurance pack plus SJK-specific synthetic pilot, leadership and integration-discovery programme now exist; actual hospital systems, responsible-party approvals and target-environment evidence remain missing.",
        evidence=("docs/HOSPITAL_ASSURANCE_PACK.md", "docs/ARCHITECTURE_V1.md", "docs/SAFETY_CASE.md", "docs/DATA_FLOW_AND_PRIVACY.md", "docs/DPIA_SUPPORT.md", "docs/AVV_DPA_REQUIREMENTS.md", "docs/DEPLOYMENT_RUNBOOK.md", "docs/INCIDENT_RESPONSE.md", "docs/PILOT_MEASUREMENT_PROTOCOL.md", "docs/RISK_REGISTER.md", "docs/CHANGE_CONTROL.md", "docs/SLO_POLICY.md", "docs/REGULATORY_BASELINE_DE.md", "docs/SJK_REFERENCE_ENVIRONMENT.md", "docs/SJK_PILOT_BRIEF.md", "docs/SJK_TEAM_TEST_PROTOCOL.md", "docs/SJK_CHEFARZT_ONE_PAGER.md", "docs/SJK_INTEGRATION_DISCOVERY.md", "docs/SJK_END_TO_END_PLAN.md"),
        blockers=("replace reference assumptions with SJK actual systems/network/data flows", "responsible-party DSFA/AVV/security approvals", "named support/incident contacts and hospital network runbook", "independent review/pentest evidence", "pilot-specific stop thresholds and rollback acceptance by accountable hospital owners"),
        owner_lane="deployment + compliance",
    ),
    Gate(
        id="G8",
        name="Repeatable multi-hospital deployment",
        status=GateStatus.PARTIAL,
        claim="A vendor-neutral connector capability/read-result contract exists and FHIR implements it; repeatability is not proven until independent hospital/vendor deployments succeed without core forks.",
        evidence=("app/connectors/base.py", "app/connectors/fhir_connector.py", "tests/test_connector_contract.py", "docs/CONNECTOR_SDK.md", "docs/SPECIALTY_PACKS.md", "docs/GLOBAL_ARCHITECTURE.md"),
        blockers=("hospital A real read-only deployment", "hospital B different vendor deployment", "real vendor capability records", "evidence that vendor differences remain connector/configuration concerns rather than core forks"),
        owner_lane="platform + partnerships",
    ),
    Gate(
        id="G9",
        name="National / EU scale",
        status=GateStatus.BLOCKED,
        claim="Germany/EU integration and operating-model roadmap is explicit; national infrastructure integrations are not implemented or validated.",
        evidence=("docs/GLOBAL_ARCHITECTURE.md", "docs/REGULATORY_BASELINE_DE.md", "docs/NATIONAL_EU_ROADMAP.md"),
        blockers=("ePA/TI/KIM integration where applicable", "ISiP/outpatient pathways", "implemented EHDS interoperability/logging obligations where CareOS falls in scope", "national-scale operating and multi-site evidence model"),
        owner_lane="interoperability + policy + partnerships",
    ),
)


def gate_manifest() -> dict[str, Any]:
    gates = []
    for gate in GATES:
        item = asdict(gate)
        item["status"] = gate.status.value
        item["evidence"] = list(gate.evidence)
        item["blockers"] = list(gate.blockers)
        gates.append(item)
    counts = {status.value: sum(1 for g in GATES if g.status == status) for status in GateStatus}
    return {
        "release_rule": "CareOS graduates by evidence-backed gates, not version number.",
        "live_patient_data_allowed": all(g.status == GateStatus.PASS for g in GATES[:6]),
        "counts": counts,
        "gates": gates,
    }

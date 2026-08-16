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
        claim="Intended-use boundary, federated Reference Architecture V2, durable ADRs and safety case are explicit; qualified independent review is still required.",
        evidence=(
            "docs/ARCHITECTURE_V2.md",
            "docs/SAFETY_CASE.md",
            "docs/REGULATORY_BASELINE_DE.md",
            "docs/EXTERNAL_REVIEW_BRIEF.md",
            "docs/adr/README.md",
            "architecture/reference-architecture.json",
            "tests/test_reference_architecture_manifest.py",
        ),
        blockers=(
            "independent MDR/MDSW qualification/classification assessment",
            "named clinical-safety reviewer findings and sign-off for pilot scope",
        ),
        owner_lane="product + clinical safety + regulatory",
    ),
    Gate(
        id="G1",
        name="Clinical truth",
        status=GateStatus.BLOCKED,
        claim="Clinical truth separates source extraction, evidence admission and deterministic reconciliation. Frozen Holdout #3 shows 100% benchmark precision/provenance and zero observed critical silent misses, but only 26.3% recall and 100% review burden, so production use remains blocked.",
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
            "docs/BENCHMARK.md",
            "docs/G1_MODEL_ASSISTED.md",
        ),
        blockers=(
            "raise recall substantially without tuning Frozen Holdout #3 or losing precision/provenance",
            "reduce review/abstention burden from the current 100% synthetic Holdout #3 rate",
            "evaluate the next evidence-first model-assisted extractor on a fresh development corpus",
            "freeze/evaluate a future untouched holdout only after the next architecture is fixed",
            "obtain clinician-reviewed/de-identified evidence under appropriate governance before clinical claims",
        ),
        owner_lane="clinical data engineering",
    ),
    Gate(
        id="G2",
        name="German interoperability",
        status=GateStatus.PARTIAL,
        claim="Real FHIR transport, fail-closed paging, pinned gematik ISiK5 profile-validation CI and a vendor-neutral connector contract are proven. Real terminology, synchronization and hospital/vendor evidence remain missing.",
        evidence=(
            "app/fhir_adapter.py",
            "app/connectors/base.py",
            "app/connectors/fhir_connector.py",
            "app/terminology_policy.py",
            "docs/FHIR_INTEGRATION.md",
            "docs/CONNECTOR_SDK.md",
            "docs/TERMINOLOGY_VALIDATION.md",
            "docs/NATIONAL_INTEGRATION_MAP.md",
            "integration/docker-compose.fhir.yml",
            "integration/isik5/Patient-careos-synthetic.json",
            ".github/workflows/isik5-validation.yml",
            "docs/SJK_INTEGRATION_DISCOVERY.md",
        ),
        blockers=(
            "production terminology service/validation for relevant code systems and value sets",
            "one real SJK/KIS/LIS/vendor read-only sandbox",
            "resource-version reconciliation/incremental synchronization",
            "end-to-end freshness semantics against a real source",
        ),
        owner_lane="interoperability",
    ),
    Gate(
        id="G3",
        name="Privacy & security",
        status=GateStatus.PARTIAL,
        claim="OIDC verification, fail-closed authorization/context, secure-read orchestration, kill switches, audit protections, provider-side PHI architecture, CodeQL, dependency audit/SBOM and security governance foundations exist; production provider assurance remains incomplete.",
        evidence=(
            "app/auth_oidc.py",
            "app/access_policy.py",
            "app/clinical_session.py",
            "app/kill_switch.py",
            "app/audit.py",
            "app/audit_chain.py",
            "app/security_readiness.py",
            "app/deployment_policy.py",
            "docs/TRUST_AND_DATA_FLOW.md",
            "docs/DATA_FLOW_AND_PRIVACY.md",
            "docs/DPIA_SUPPORT.md",
            "docs/AVV_DPA_REQUIREMENTS.md",
            "docs/THREAT_MODEL.md",
            "docs/RESPONSIBILITY_MODEL.md",
            "docs/ASSURANCE_CROSSWALK.md",
            "SECURITY.md",
            ".github/workflows/codeql.yml",
            ".github/workflows/supply-chain-security.yml",
            ".github/dependabot.yml",
        ),
        blockers=(
            "connect verifier to actual hospital IdP/SSO and authoritative role/treatment-context mapping",
            "central independently protected production audit/SIEM",
            "provider-approved KMS/secrets/encryption deployment",
            "hospital-specific DPIA/DSFA, agreements and approvals",
            "C5/customer-controls evidence where applicable",
            "independent penetration test and remediation closure",
        ),
        owner_lane="security + privacy",
    ),
    Gate(
        id="G4",
        name="Production reliability",
        status=GateStatus.PARTIAL,
        claim="Fail-visible source semantics, bounded paging, kill switches, live-data startup lock, safety failure-injection CI and a non-root container smoke test are proven internally; target-environment resilience/recovery evidence remains missing.",
        evidence=(
            "app/source_state.py",
            "app/fhir_adapter.py",
            "app/connectors/fhir_connector.py",
            "app/kill_switch.py",
            "app/deployment_policy.py",
            ".github/workflows/safety-failure-injection.yml",
            ".github/workflows/container-smoke.yml",
            "Dockerfile",
            ".dockerignore",
            "docs/DEPLOYMENT_PATTERNS.md",
            "docs/DEPLOYMENT_RUNBOOK.md",
            "docs/INCIDENT_RESPONSE.md",
            "docs/SLO_POLICY.md",
        ),
        blockers=(
            "failure injection against actual KIS/FHIR/identity/audit/network dependencies",
            "freshness policies wired to every real source",
            "backup/restore evidence with measured RPO/RTO",
            "operational monitoring/alerting against approved SLOs",
            "incident/rollback exercise in target deployment",
        ),
        owner_lane="platform/SRE",
    ),
    Gate(
        id="G5",
        name="Regulatory & quality system",
        status=GateStatus.EXTERNAL_REVIEW,
        claim="Intended purpose, regulatory baseline, risk/change discipline and an EHDS-oriented technical-documentation index are explicit; formal classification/applicability and classification-appropriate quality lifecycle remain external blockers.",
        evidence=(
            "docs/SAFETY_CASE.md",
            "docs/REGULATORY_BASELINE_DE.md",
            "docs/EXTERNAL_REVIEW_BRIEF.md",
            "docs/RISK_REGISTER.md",
            "docs/CHANGE_CONTROL.md",
            "docs/TECHNICAL_DOCUMENTATION_INDEX.md",
            "docs/ASSURANCE_CROSSWALK.md",
        ),
        blockers=(
            "independent MDR/MDSW assessment",
            "AI Act applicability assessment",
            "EHDS applicability mapping by qualified reviewer where required",
            "reviewed clinical risk-management file",
            "QMS/lifecycle evidence appropriate to resulting classification",
        ),
        owner_lane="regulatory + quality",
    ),
    Gate(
        id="G6",
        name="Invisible workflow integration",
        status=GateStatus.PARTIAL,
        claim="Authenticated patient/treatment-context launch, deterministic identity and an SJK synthetic workflow reference exist; a real KIS/portal launcher and no-duplicate-work deployment are not yet proven.",
        evidence=(
            "app/context_launch.py",
            "app/patient_identity.py",
            "app/auth_oidc.py",
            "app/access_policy.py",
            "app/reference_environments.py",
            "share/sjk-infectiology/",
            "docs/SJK_TEAM_TEST_PROTOCOL.md",
            "docs/DEPLOYMENT_PATTERNS.md",
        ),
        blockers=(
            "real hospital/KIS trusted context resolver/launcher",
            "same-patient context proven without duplicate manual search",
            "embedded/Citrix/VDI/managed-browser compatibility proof",
            "no-copy/no-duplicate-documentation workflow measured in real environment",
        ),
        owner_lane="product + integration",
    ),
    Gate(
        id="G7",
        name="Hospital deployment kit",
        status=GateStatus.PARTIAL,
        claim="A proposal-grade assurance/deployment package now covers architecture, data flows, responsibilities, procurement, privacy/security, operations and SJK staged evaluation; hospital-specific completion and accountable approvals remain missing.",
        evidence=(
            "docs/HOSPITAL_ASSURANCE_PACK.md",
            "docs/ARCHITECTURE_V2.md",
            "docs/TRUST_AND_DATA_FLOW.md",
            "docs/DEPLOYMENT_PATTERNS.md",
            "docs/TECHNICAL_DOCUMENTATION_INDEX.md",
            "docs/RESPONSIBILITY_MODEL.md",
            "docs/PROCUREMENT_REQUIREMENTS.md",
            "docs/ASSURANCE_CROSSWALK.md",
            "docs/SAFETY_CASE.md",
            "docs/DPIA_SUPPORT.md",
            "docs/AVV_DPA_REQUIREMENTS.md",
            "docs/DEPLOYMENT_RUNBOOK.md",
            "docs/INCIDENT_RESPONSE.md",
            "docs/PILOT_MEASUREMENT_PROTOCOL.md",
            "docs/SJK_PILOT_BRIEF.md",
            "docs/SJK_TEAM_TEST_PROTOCOL.md",
            "docs/SJK_CHEFARZT_ONE_PAGER.md",
            "docs/SJK_INTEGRATION_DISCOVERY.md",
            "docs/SJK_END_TO_END_PLAN.md",
        ),
        blockers=(
            "replace reference assumptions with target-hospital actual systems/network/data flows",
            "responsible-party DSFA/AVV/security approvals",
            "named support/incident/key/audit/rollback owners",
            "independent review/pentest evidence",
            "pilot stop thresholds and rollback acceptance by accountable hospital owners",
        ),
        owner_lane="deployment + compliance",
    ),
    Gate(
        id="G8",
        name="Repeatable multi-hospital deployment",
        status=GateStatus.PARTIAL,
        claim="Stable connector, fact, failure, composition and deployment contracts define the anti-fork platform model; repeatability is not proven until independent hospital/vendor deployments succeed without a core fork.",
        evidence=(
            "app/connectors/base.py",
            "app/connectors/fhir_connector.py",
            "docs/CONNECTOR_SDK.md",
            "docs/SPECIALTY_PACKS.md",
            "docs/GLOBAL_ARCHITECTURE.md",
            "docs/DEPLOYMENT_PATTERNS.md",
            "docs/PROCUREMENT_REQUIREMENTS.md",
            "docs/adr/ADR-008-composition-not-forks.md",
            "docs/adr/ADR-010-open-connector-contract.md",
        ),
        blockers=(
            "hospital A real read-only deployment",
            "hospital B different vendor deployment",
            "real vendor capability records",
            "evidence that vendor differences remain connector/configuration concerns rather than core forks",
        ),
        owner_lane="platform + partnerships",
    ),
    Gate(
        id="G9",
        name="National / EU scale",
        status=GateStatus.BLOCKED,
        claim="A 10/10 proposal/reference-architecture package now defines the federated German/EU target, open contracts, national integration map and procurement model; actual national integrations and multi-site operating evidence are not implemented.",
        evidence=(
            "docs/GOVERNMENT_REFERENCE_ARCHITECTURE.md",
            "docs/GOVERNMENT_ONE_PAGER_DE.md",
            "docs/ARCHITECTURE_V2.md",
            "docs/NATIONAL_INTEGRATION_MAP.md",
            "docs/TECHNICAL_DOCUMENTATION_INDEX.md",
            "docs/PROCUREMENT_REQUIREMENTS.md",
            "docs/ASSURANCE_CROSSWALK.md",
            "docs/REFERENCE_ARCHITECTURE_SCORECARD.md",
            "docs/NATIONAL_EU_ROADMAP.md",
            "architecture/reference-architecture.json",
        ),
        blockers=(
            "ePA/TI/KIM integration where applicable",
            "ISiP/outpatient pathways",
            "implemented EHDS interoperability/logging obligations where CareOS falls in scope",
            "multi-site national operating evidence",
            "public/institutional governance and standardization decisions outside CareOS control",
        ),
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
        "reference_architecture_readiness": {
            "score": 10,
            "max_score": 10,
            "meaning": "proposal completeness and architectural reviewability only; not production clearance",
        },
        "live_patient_data_allowed": all(g.status == GateStatus.PASS for g in GATES[:6]),
        "counts": counts,
        "gates": gates,
    }

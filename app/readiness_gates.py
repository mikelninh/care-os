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
        claim="Intended-use boundary and target architecture are written; external regulatory/clinical-safety review is still required.",
        evidence=("docs/ARCHITECTURE_V1.md", "docs/SAFETY_CASE.md", "docs/REGULATORY_BASELINE_DE.md"),
        blockers=("independent MDR/MDSW qualification/classification assessment", "named clinical-safety reviewer sign-off"),
        owner_lane="product + clinical safety + regulatory",
    ),
    Gate(
        id="G1",
        name="Clinical truth",
        status=GateStatus.BLOCKED,
        claim="FHIR source-native data now passes through the canonical truth contract, but document extraction reliability remains below the clinical release bar.",
        evidence=("app/clinical_truth.py", "app/fhir_adapter.py", "tests/test_clinical_truth.py", "tests/test_fhir_truth.py", "docs/BENCHMARK.md"),
        blockers=("replace brittle document extractor", "100% provenance on every surfaced document-derived fact", "critical silent contradiction misses at release bar", "new frozen holdout after new extractor"),
        owner_lane="clinical data engineering",
    ),
    Gate(
        id="G2",
        name="German interoperability",
        status=GateStatus.PARTIAL,
        claim="Real FHIR transport and pinned gematik ISiK5 profile-validation CI are proven; terminology coverage and a real hospital/vendor sandbox remain missing.",
        evidence=("app/fhir_adapter.py", "docs/FHIR_INTEGRATION.md", "integration/docker-compose.fhir.yml", "integration/isik5/Patient-careos-synthetic.json", ".github/workflows/isik5-validation.yml"),
        blockers=("terminology validation outside validator exclusions", "one real KIS/LIS/vendor read-only sandbox", "paging/reconciliation across large result sets", "end-to-end freshness/version semantics"),
        owner_lane="interoperability",
    ),
    Gate(
        id="G3",
        name="Privacy & security",
        status=GateStatus.PARTIAL,
        claim="Threat model, fail-closed treatment-context policy contract, audit prototype and configuration gate exist; production authentication/authorization/privacy infrastructure remains missing.",
        evidence=("docs/THREAT_MODEL.md", "docs/PRODUCTION_READINESS.md", "app/security_readiness.py", "app/audit.py", "app/access_policy.py", "tests/test_access_policy.py"),
        blockers=("working OIDC/JWT verification and hospital SSO", "trusted role/org/treatment-context claim mapping", "central immutable audit", "KMS/secrets and production encryption", "DPIA/DSFA + DPA/AVV package", "C5/customer-controls evidence where applicable", "independent penetration test"),
        owner_lane="security + privacy",
    ),
    Gate(
        id="G4",
        name="Production reliability",
        status=GateStatus.PARTIAL,
        claim="Explicit current/stale/unavailable source semantics now prevent basic outage-to-empty-state confusion; system-wide resilience and recovery are not yet demonstrated.",
        evidence=("docs/THREAT_MODEL.md", "app/source_state.py", "tests/test_source_state.py"),
        blockers=("failure-injection suite across KIS/FHIR/identity/audit/model dependencies", "freshness policies wired to every production source", "backup/restore evidence", "RPO/RTO", "rollback/kill switch", "operational monitoring/SLOs"),
        owner_lane="platform/SRE",
    ),
    Gate(
        id="G5",
        name="Regulatory & quality system",
        status=GateStatus.EXTERNAL_REVIEW,
        claim="Safety boundary and current German regulatory baseline are explicit; formal regulatory position and lifecycle/QMS remain missing.",
        evidence=("docs/SAFETY_CASE.md", "docs/REGULATORY_BASELINE_DE.md"),
        blockers=("MDR/MDSW assessment", "AI Act assessment", "EHDS applicability mapping", "risk-management file", "change-control/QMS appropriate to classification"),
        owner_lane="regulatory + quality",
    ),
    Gate(
        id="G6",
        name="Invisible workflow integration",
        status=GateStatus.BLOCKED,
        claim="Browser UX is testable; production context launch/same-patient workflow is not integrated.",
        evidence=("share/",),
        blockers=("hospital SSO/context launch", "same-patient context without duplicate search", "embedded/Citrix/VDI compatibility proof", "no-copy workflow"),
        owner_lane="product + integration",
    ),
    Gate(
        id="G7",
        name="Hospital deployment kit",
        status=GateStatus.PARTIAL,
        claim="Architecture, threat model, safety case and readiness documents exist; procurement/assurance package is incomplete.",
        evidence=("docs/ARCHITECTURE_V1.md", "docs/SAFETY_CASE.md", "docs/THREAT_MODEL.md", "docs/PRODUCTION_READINESS.md", "docs/REGULATORY_BASELINE_DE.md"),
        blockers=("data-flow diagram", "DSFA support pack", "AVV template", "network/deployment runbook", "support/incident model", "rollback plan", "measurement protocol package"),
        owner_lane="deployment + compliance",
    ),
    Gate(
        id="G8",
        name="Repeatable multi-hospital deployment",
        status=GateStatus.BLOCKED,
        claim="Pack architecture is configuration-oriented, but repeatability has not been proven across independent hospitals/vendors.",
        evidence=("docs/SPECIALTY_PACKS.md", "docs/GLOBAL_ARCHITECTURE.md"),
        blockers=("hospital A real read-only deployment", "hospital B different vendor deployment", "connector SDK/capability matrix", "no-core-fork evidence"),
        owner_lane="platform + partnerships",
    ),
    Gate(
        id="G9",
        name="National / EU scale",
        status=GateStatus.BLOCKED,
        claim="Architecture anticipates country/audience layers; national infrastructure integrations are not implemented.",
        evidence=("docs/GLOBAL_ARCHITECTURE.md",),
        blockers=("ePA/TI/KIM integration where applicable", "ISiP/outpatient pathways", "EHDS interoperability/logging roadmap", "national-scale operating model and evidence"),
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

import json
from pathlib import Path

POSTURE = json.loads((Path(__file__).parents[1] / "security" / "security-posture.json").read_text(encoding="utf-8"))
REQUIRED = {
    "authority_outside_model", "least_privilege", "tenant_isolation", "human_approval", "provenance", "protected_data",
    "bounded_execution", "auditability", "supply_chain", "adversarial_evals", "production_monitoring",
}


def test_security_posture_contract_is_complete_and_honest():
    assert POSTURE["version"] == "security-posture/v1"
    assert POSTURE["project"]["repository"] == "mikelninh/care-os"
    assert {control["id"] for control in POSTURE["controls"]} == REQUIRED
    assert POSTURE["claims"] == {"productionSecure": False, "promptInjectionSolved": False, "certified": False}


def test_security_posture_matches_current_containment_suite():
    assert POSTURE["adversarial"]["cases"] == 6
    assert POSTURE["adversarial"]["passed"] == 6
    assert POSTURE["adversarial"]["criticalEscapes"] == 0
    assert POSTURE["adversarial"]["liveModel"] is False


def test_clinical_production_security_is_not_inferred_from_engineering_evidence():
    joined = " ".join(POSTURE["residualRisks"])
    assert "A0-A9" in joined
    assert "clinical" in joined.lower()
    assert POSTURE["claims"]["productionSecure"] is False


def test_implemented_controls_have_evidence():
    for control in POSTURE["controls"]:
        if control["status"] == "implemented":
            assert control["evidence"], control["id"]

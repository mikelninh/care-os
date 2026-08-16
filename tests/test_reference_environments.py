from app.reference_environments import list_reference_environments, reference_environment


def test_sjk_reference_environment_is_explicitly_synthetic_and_not_integrated():
    env = reference_environment("sjk-infectiology")
    assert env is not None
    assert env["synthetic_only"] is True
    assert "not endorsed" in env["status"]
    assert env["public_context"]["inpatient"] == "Station 21"
    assert "Tagesklinik" in env["public_context"]["day_clinic"]


def test_sjk_reference_pack_has_real_workflow_hypotheses_not_new_clinical_authority():
    env = reference_environment("sjk-infectiology")
    ids = {item["id"] for item in env["workflow_hypotheses"]}
    assert {"morning-board", "ward-round", "results-chase", "microbiology", "handover", "day-clinic-continuity", "consult-hotline", "ams-review"} <= ids
    forbidden = " ".join(env["must_never_do"]).lower()
    assert "autonom" in forbidden
    assert "auto-merge" in forbidden
    assert "silently" in forbidden
    assert "patient data" in forbidden
    assert env["specialty_pack"]["id"] == "infectiology"
    assert "Synthetischer" in env["specialty_pack"]["demo"]["patient"]["ward"]


def test_reference_environment_returns_copy():
    first = reference_environment("sjk-infectiology")
    first["public_context"]["inpatient"] = "changed"
    second = reference_environment("sjk-infectiology")
    assert second["public_context"]["inpatient"] == "Station 21"


def test_unknown_reference_environment_is_none():
    assert reference_environment("unknown") is None
    assert any(item["id"] == "sjk-infectiology" for item in list_reference_environments())

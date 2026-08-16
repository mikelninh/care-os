from app.readiness_gates import GateStatus, GATES, gate_manifest


def test_gate_ids_are_unique_and_complete():
    ids = [g.id for g in GATES]
    assert ids == [f"G{i}" for i in range(10)]
    assert len(ids) == len(set(ids))


def test_live_patient_data_is_fail_closed_until_core_gates_pass():
    manifest = gate_manifest()
    assert manifest["live_patient_data_allowed"] is False
    assert any(g["status"] != GateStatus.PASS.value for g in manifest["gates"][:6])


def test_every_nonpassing_gate_has_explicit_blockers():
    for gate in gate_manifest()["gates"]:
        if gate["status"] != GateStatus.PASS.value:
            assert gate["blockers"], gate["id"]


def test_every_gate_links_evidence():
    for gate in gate_manifest()["gates"]:
        assert gate["evidence"], gate["id"]

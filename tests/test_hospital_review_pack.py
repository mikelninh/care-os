from pathlib import Path

from app.hospital_install import HospitalManifest
from app.hospital_review_pack import SECRET_PATTERN, build_hospital_review_pack, review_pack_json


def example_manifest():
    return HospitalManifest.model_validate_json(Path("deploy/hospital.example.json").read_text(encoding="utf-8"))


def test_review_pack_contains_non_secret_source_adapter_and_owner_context():
    pack = build_hospital_review_pack(example_manifest())
    assert len(pack.sources) == 2
    assert {source.source_id for source in pack.sources} == {"kis-main", "lis-microbiology"}
    assert all(source.endpoint_reference and source.endpoint_reference.endswith("_BASE_URL") for source in pack.sources)
    assert pack.owners["security"] is True
    assert pack.controls["audit_destination_available"] is True
    assert "technical review/support artifact" in pack.markdown


def test_review_pack_never_contains_endpoint_or_secret_values():
    pack = build_hospital_review_pack(example_manifest())
    payload = review_pack_json(pack) + pack.markdown + pack.mermaid
    assert "https://" not in payload
    assert "Bearer ey" not in payload
    assert "-----BEGIN" not in payload
    assert SECRET_PATTERN.search(payload) is None


def test_read_write_boundary_is_visible():
    pack = build_hospital_review_pack(example_manifest())
    assert "Manifest does not permit write capability" in pack.markdown
    assert all(source.direction == "read" for source in pack.sources)


def test_mermaid_shows_sources_provider_local_plane_context_and_audit():
    mermaid = build_hospital_review_pack(example_manifest()).mermaid
    assert "kis-main" in mermaid
    assert "lis-microbiology" in mermaid
    assert "provider-local data plane" in mermaid
    assert "provider audit destination" in mermaid

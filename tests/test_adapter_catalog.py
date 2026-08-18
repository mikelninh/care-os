import json
from pathlib import Path

from app.hospital_install import ADAPTER_CATALOG, InterfaceKind


def test_adapter_catalog_matches_installer_maturity():
    catalog = json.loads(Path("architecture/adapter-catalog.json").read_text(encoding="utf-8"))
    by_interface = {item["interface"]: item for item in catalog["adapters"]}

    for interface, runtime in ADAPTER_CATALOG.items():
        item = by_interface[interface.value]
        assert item["id"] == runtime["adapter_id"]
        assert item["family"] == runtime["family"]
        assert item["implementation_status"] == runtime["implementation_status"]
        assert item["runtime_available"] is runtime["runtime_available"]


def test_contract_only_adapters_are_not_marked_runtime_available():
    catalog = json.loads(Path("architecture/adapter-catalog.json").read_text(encoding="utf-8"))
    for item in catalog["adapters"]:
        if item["implementation_status"] == "contract-only":
            assert item["runtime_available"] is False


def test_no_live_write_adapter_is_advertised():
    catalog = json.loads(Path("architecture/adapter-catalog.json").read_text(encoding="utf-8"))
    assert "No live transactional/write adapter" in catalog["write_policy"]
    assert not any(item["runtime_available"] and "write" in item["direction"] for item in catalog["adapters"])

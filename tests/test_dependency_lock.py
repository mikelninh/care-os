from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def _pins(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_.-]+)(?:\[[^]]+\])?==([^;\s]+)$", line)
        assert match, f"dependency must be an exact pin in {path.name}: {line}"
        name = match.group(1).lower().replace("_", "-")
        result[name] = match.group(2)
    return result


def test_direct_requirements_are_exact_pins_and_match_lock():
    direct = _pins(ROOT / "requirements.txt")
    locked = _pins(ROOT / "requirements.lock")
    missing = set(direct) - set(locked)
    assert not missing, f"direct dependencies missing from lock: {sorted(missing)}"
    mismatched = {
        name: (version, locked[name])
        for name, version in direct.items()
        if locked[name] != version
    }
    assert not mismatched, f"direct dependency versions differ from lock: {mismatched}"


def test_lock_has_no_unpinned_entries():
    locked = _pins(ROOT / "requirements.lock")
    assert len(locked) >= 20, "lock unexpectedly small; transitive dependency set may have been lost"

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.hospital_install import HospitalManifest
from app.hospital_upgrade import compare_hospital_manifests


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare last-known-good and proposed hospital capability manifests before rollout.")
    parser.add_argument("previous")
    parser.add_argument("proposed")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    previous = HospitalManifest.model_validate_json(Path(args.previous).read_text(encoding="utf-8"))
    proposed = HospitalManifest.model_validate_json(Path(args.proposed).read_text(encoding="utf-8"))
    plan = compare_hospital_manifests(previous, proposed)

    print(f"CareOS upgrade preflight · {plan.hospital_id}")
    print(f"automatic rollout: {plan.safe_for_automatic_rollout}")
    print(f"shadow revalidation: {plan.requires_shadow_revalidation}")
    print(f"adapters: {plan.previous_adapter_ids} -> {plan.proposed_adapter_ids}")
    for finding in plan.findings:
        source = f"[{finding.source_id}] " if finding.source_id else ""
        print(f"{finding.severity.upper():5} {finding.code}: {source}{finding.message}")

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(plan.model_dump_json(indent=2) + "\n", encoding="utf-8")

    return 2 if any(f.severity == "block" for f in plan.findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

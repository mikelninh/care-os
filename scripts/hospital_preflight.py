from __future__ import annotations

import argparse
import sys
from pathlib import Path

# `python scripts/...` places the scripts directory, not the repository root, on
# sys.path. Make the documented direct-entrypoint command work from a clean clone.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.hospital_install import HospitalManifest, build_hospital_install_plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a non-secret hospital capability manifest and produce a reusable CareOS install plan."
    )
    parser.add_argument("manifest", help="Path to hospital capability manifest JSON")
    parser.add_argument("--json-out", help="Optional path for machine-readable install plan")
    args = parser.parse_args()

    path = Path(args.manifest)
    manifest = HospitalManifest.model_validate_json(path.read_text(encoding="utf-8"))
    plan = build_hospital_install_plan(manifest)

    print(f"CareOS hospital preflight · {manifest.site_name} · {manifest.hospital_id}")
    print(f"intent: {plan.deployment_intent.value}")
    print(f"current release allows execution: {plan.execution_allowed_by_current_release}")
    if plan.release_blocker:
        print(f"release blocker: {plan.release_blocker}")
    print("\nadapters")
    for adapter in plan.adapters:
        print(
            f"  {adapter.source_id:18} {adapter.direction:5} -> {adapter.adapter_id:28} "
            f"[{adapter.risk}] reuse={adapter.reuse_key}"
        )
    print("\nchecks")
    for check in plan.checks:
        print(f"  {check.status.upper():5} {check.id}: {check.message}")
    print("\nreadiness")
    print(f"  synthetic/deidentified install: {plan.installable_for_synthetic_or_deidentified}")
    print(f"  shadow architecture ready:      {plan.ready_for_shadow}")
    print(f"  copilot architecture ready:     {plan.ready_for_copilot}")
    print(f"  controlled-write architecture:  {plan.ready_for_controlled_write}")

    if plan.next_steps:
        print("\nnext")
        for step in plan.next_steps:
            print(f"  - {step}")

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(plan.model_dump_json(indent=2) + "\n", encoding="utf-8")
        print(f"\nplan saved: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

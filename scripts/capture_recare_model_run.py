from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from app.recare_capstone import CapstoneRunRequest, run_capstone


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run one synthetic Recare capstone case through a configured real model provider and save the evidence."
    )
    p.add_argument("--worker", choices=["openai_responses", "external_model"], default="openai_responses")
    p.add_argument(
        "--scenario",
        choices=["happy_path", "wrong_patient", "prompt_injection", "source_unavailable", "stale_result", "unauthorised_write"],
        default="happy_path",
    )
    p.add_argument(
        "--task",
        default="Prepare a concise source-linked discharge-prep summary. Preserve pending work and conflicts.",
    )
    p.add_argument("--out", default="artifacts/recare-provider-backed-run.json")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    request = CapstoneRunRequest(
        scenario=args.scenario,
        worker_mode=args.worker,
        task=args.task,
    )
    result = run_capstone(request)
    payload = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "evidence_kind": "provider-backed-synthetic-capstone-run",
        "claim_boundary": {
            "synthetic_only": True,
            "clinical_validation": False,
            "production_hospital_traffic": False,
            "identifiable_phi": False,
            "production_write_back": False,
        },
        "run": result.model_dump(mode="json"),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    passed = result.metrics.get("eval_passed")
    total = result.metrics.get("eval_total")
    print(f"saved: {out}")
    print(f"worker: {result.worker_mode} · model: {result.model_id} · status: {result.execution_status}")
    print(f"eval: {passed}/{total} · trace events: {len(result.trace)}")
    print(f"tokens: {result.metrics.get('model_total_tokens')}")
    return 0 if passed == total else 2


if __name__ == "__main__":
    raise SystemExit(main())

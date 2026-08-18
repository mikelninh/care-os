from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.hospital_install import (
    DeploymentIntent,
    HospitalManifest,
    InterfaceKind,
    PatientIdentityStrategy,
    SourceSystem,
    SystemRole,
    build_hospital_install_plan,
)
from app.hospital_upgrade import compare_hospital_manifests


COMPOSE = ROOT / "deploy" / "docker-compose.hospital.yml"


def _load(path: str) -> HospitalManifest:
    return HospitalManifest.model_validate_json(Path(path).read_text(encoding="utf-8"))


def _env_keys(path: str | None) -> set[str]:
    if not path:
        return set(os.environ)
    env_path = Path(path)
    if not env_path.exists():
        return set()
    keys: set[str] = set()
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        keys.add(line.split("=", 1)[0].strip())
    return keys | set(os.environ)


def cmd_init(args) -> int:
    out = Path(args.out)
    if out.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite {out}; use --force")
    template = HospitalManifest(
        hospital_id=args.hospital_id,
        country=args.country.upper(),
        site_name=args.site_name,
        deployment_intent=DeploymentIntent.SYNTHETIC,
        sources=[
            SourceSystem(
                source_id="kis-main",
                role=SystemRole.KIS,
                vendor="CHANGE-ME",
                product="CHANGE-ME",
                version="CHANGE-ME",
                interfaces=[InterfaceKind.FHIR_R4],
                authentication_mode="synthetic-none",
                endpoint_env="KIS_FHIR_BASE_URL",
                resources=["Patient", "Encounter"],
            )
        ],
        patient_identity_strategy=PatientIdentityStrategy.UNKNOWN,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(f"created {out}")
    print("next: fill source capabilities/owners, then run `careos doctor` and `careos preflight`")
    return 0


def cmd_preflight(args) -> int:
    manifest = _load(args.manifest)
    plan = build_hospital_install_plan(manifest)
    print(f"CareOS preflight · {manifest.site_name} · {manifest.hospital_id}")
    for adapter in plan.adapters:
        print(
            f"ADAPTER {adapter.source_id}: {adapter.adapter_id} "
            f"({adapter.implementation_status}, runtime={adapter.runtime_available})"
        )
    for check in plan.checks:
        print(f"{check.status.upper():5} {check.id}: {check.message}")
    print(f"synthetic/deidentified installable: {plan.installable_for_synthetic_or_deidentified}")
    print(f"shadow architecture ready: {plan.ready_for_shadow}")
    print(f"current release permits intent: {plan.execution_allowed_by_current_release}")
    if args.json_out:
        Path(args.json_out).write_text(plan.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return 2 if any(check.status == "block" for check in plan.checks) else 0


def cmd_doctor(args) -> int:
    manifest = _load(args.manifest)
    plan = build_hospital_install_plan(manifest)
    env_keys = _env_keys(args.env_file)
    failures: list[str] = []
    warnings: list[str] = []

    docker = shutil.which("docker")
    if docker:
        print(f"PASS  docker: {docker}")
    else:
        failures.append("Docker CLI not found")
        print("BLOCK docker: Docker CLI not found")

    for source in manifest.sources:
        selection = next((a for a in plan.adapters if a.source_id == source.source_id and a.direction == "read"), None)
        if selection and selection.runtime_available:
            if not source.endpoint_env or source.endpoint_env not in env_keys:
                failures.append(f"{source.source_id}: missing endpoint env reference/value")
                print(f"BLOCK {source.source_id}: {source.endpoint_env or 'endpoint_env'} is not available")
            else:
                print(f"PASS  {source.source_id}: endpoint env is present (value hidden)")
            if source.authentication_mode.lower() not in {"none", "no-auth", "synthetic-none"}:
                if not source.credential_env or source.credential_env not in env_keys:
                    failures.append(f"{source.source_id}: missing credential env")
                    print(f"BLOCK {source.source_id}: credential env is not available")
                else:
                    print(f"PASS  {source.source_id}: credential env is present (value hidden)")
        elif selection:
            failures.append(f"{source.source_id}: selected adapter runtime is not implemented")
            print(f"BLOCK {source.source_id}: {selection.adapter_id} is {selection.implementation_status}")

    for check in plan.checks:
        if check.status == "block":
            failures.append(check.id)
        elif check.status == "warn":
            warnings.append(check.id)

    print(f"\ndoctor: {len(failures)} blocker(s), {len(warnings)} warning(s)")
    return 2 if failures else 0


def cmd_discover_fhir(args) -> int:
    cmd = [sys.executable, str(ROOT / "scripts" / "fhir_discover.py"), args.manifest]
    if args.source_id:
        cmd.extend(["--source-id", args.source_id])
    if args.env_file:
        cmd.extend(["--env-file", args.env_file])
    if args.json_out:
        cmd.extend(["--json-out", args.json_out])
    return subprocess.run(cmd, check=False).returncode


def _compose_env(args) -> dict[str, str]:
    env = dict(os.environ)
    env["CAREOS_HOSPITAL_MANIFEST_FILE"] = str(Path(args.manifest).resolve())
    if getattr(args, "env_file", None):
        env["CAREOS_HOSPITAL_ENV_FILE"] = str(Path(args.env_file).resolve())
    return env


def cmd_up(args) -> int:
    manifest = _load(args.manifest)
    plan = build_hospital_install_plan(manifest)
    if not plan.installable_for_synthetic_or_deidentified:
        print("BLOCK hospital preflight does not permit self-install runtime")
        for check in plan.checks:
            if check.status == "block":
                print(f"  - {check.id}: {check.message}")
        return 2
    if manifest.deployment_intent not in {DeploymentIntent.SYNTHETIC, DeploymentIntent.DEIDENTIFIED}:
        print("BLOCK current self-install CLI only starts synthetic/deidentified data planes")
        return 2
    if not shutil.which("docker"):
        print("BLOCK Docker CLI not found")
        return 2
    cmd = ["docker", "compose", "-f", str(COMPOSE), "up", "-d", "--build", "careos"]
    print("starting hospital-local CareOS data plane")
    return subprocess.run(cmd, env=_compose_env(args), check=False).returncode


def cmd_down(args) -> int:
    if not shutil.which("docker"):
        print("BLOCK Docker CLI not found")
        return 2
    cmd = ["docker", "compose", "-f", str(COMPOSE), "down"]
    return subprocess.run(cmd, env=_compose_env(args), check=False).returncode


def cmd_upgrade(args) -> int:
    previous = _load(args.previous)
    proposed = _load(args.proposed)
    plan = compare_hospital_manifests(previous, proposed)
    print(f"upgrade · {plan.hospital_id}")
    print(f"automatic rollout: {plan.safe_for_automatic_rollout}")
    print(f"shadow revalidation: {plan.requires_shadow_revalidation}")
    for finding in plan.findings:
        source = f"[{finding.source_id}] " if finding.source_id else ""
        print(f"{finding.severity.upper():5} {finding.code}: {source}{finding.message}")
    return 2 if any(f.severity == "block" for f in plan.findings) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="careos", description="CareOS hospital self-install / compatibility CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create a safe non-secret hospital manifest template")
    p.add_argument("--hospital-id", required=True)
    p.add_argument("--site-name", required=True)
    p.add_argument("--country", default="DE")
    p.add_argument("--out", default="hospital.json")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("preflight", help="select adapters and evaluate install readiness")
    p.add_argument("manifest")
    p.add_argument("--json-out")
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("doctor", help="check local tooling, runtime adapter support and secret/env references")
    p.add_argument("manifest")
    p.add_argument("--env-file")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("discover-fhir", help="inspect permitted FHIR CapabilityStatements without rewriting the manifest")
    p.add_argument("manifest")
    p.add_argument("--source-id")
    p.add_argument("--env-file")
    p.add_argument("--json-out")
    p.set_defaults(func=cmd_discover_fhir)

    p = sub.add_parser("up", help="start the synthetic/deidentified hospital-local data plane")
    p.add_argument("manifest")
    p.add_argument("--env-file")
    p.set_defaults(func=cmd_up)

    p = sub.add_parser("down", help="stop the local CareOS hospital compose deployment")
    p.add_argument("manifest")
    p.add_argument("--env-file")
    p.set_defaults(func=cmd_down)

    p = sub.add_parser("upgrade-check", help="compare a last-known-good manifest with a proposed upgrade")
    p.add_argument("previous")
    p.add_argument("proposed")
    p.set_defaults(func=cmd_upgrade)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

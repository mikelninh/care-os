from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from app.fhir_capability_discovery import compare_manifest_resources, parse_capability_statement
from app.fhir_adapter import FhirConfig
from app.hospital_install import DeploymentIntent, HospitalManifest, InterfaceKind
from app.hospital_runtime import BearerFhirClient, _data_mode, _source_endpoint, _source_token


def _env(path: str | None) -> dict[str, str]:
    values = dict(os.environ)
    if not path:
        return values
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover permitted FHIR capabilities without rewriting the hospital manifest.")
    parser.add_argument("manifest")
    parser.add_argument("--source-id")
    parser.add_argument("--env-file")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    manifest = HospitalManifest.model_validate_json(Path(args.manifest).read_text(encoding="utf-8"))
    if manifest.deployment_intent not in {DeploymentIntent.SYNTHETIC, DeploymentIntent.DEIDENTIFIED}:
        raise SystemExit("FHIR discovery is currently restricted to synthetic/deidentified evaluation modes")

    env = _env(args.env_file)
    ack = str(env.get("CAREOS_EXTERNAL_DEIDENTIFIED_ACK", "false")).lower() in {"1", "true", "yes", "on"}
    reports = []

    for source in manifest.sources:
        if args.source_id and source.source_id != args.source_id:
            continue
        if not ({InterfaceKind.FHIR_R4, InterfaceKind.ISIK_FHIR} & set(source.interfaces)):
            continue
        endpoint = _source_endpoint(source, env)
        token = _source_token(source, env)
        client = BearerFhirClient(
            config=FhirConfig(base_url=endpoint),
            data_mode=_data_mode(manifest.deployment_intent),
            token=token,
            external_deidentified_ack=ack,
        )
        discovery = parse_capability_statement(client.capability())
        comparison = compare_manifest_resources(source.source_id, source.resources, discovery)
        report = {
            "source_id": source.source_id,
            "fhir_version": discovery.fhir_version,
            "software_name": discovery.software_name,
            "software_version": discovery.software_version,
            "formats": discovery.formats,
            "resource_types": discovery.resource_types,
            "versioned_resource_types": discovery.versioned_resource_types,
            "comparison": comparison.model_dump(mode="json"),
        }
        reports.append(report)
        print(f"{source.source_id}: FHIR {discovery.fhir_version or '?'} · resources={len(discovery.resource_types)}")
        if comparison.declared_but_not_advertised:
            print("  WARN declared but not advertised: " + ", ".join(comparison.declared_but_not_advertised))
        if not comparison.patient_read_advertised:
            print("  BLOCK Patient read is not advertised")

    if args.source_id and not reports:
        raise SystemExit(f"no FHIR-family source matched {args.source_id!r}")
    if not reports:
        raise SystemExit("manifest contains no FHIR-family sources")

    payload = {"hospital_id": manifest.hospital_id, "reports": reports}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

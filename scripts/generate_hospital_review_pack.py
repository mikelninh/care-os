from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.hospital_install import HospitalManifest
from app.hospital_review_pack import build_hospital_review_pack, review_pack_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate non-secret CareOS hospital IT/security/data-flow review artifacts from a HospitalManifest.")
    parser.add_argument("manifest")
    parser.add_argument("--out-dir", default="hospital-review-pack")
    args = parser.parse_args()

    manifest = HospitalManifest.model_validate_json(Path(args.manifest).read_text(encoding="utf-8"))
    pack = build_hospital_review_pack(manifest)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "review-pack.json").write_text(review_pack_json(pack), encoding="utf-8")
    (out / "review-pack.md").write_text(pack.markdown, encoding="utf-8")
    (out / "data-flow.mmd").write_text(pack.mermaid + "\n", encoding="utf-8")

    print(f"CareOS review pack · {manifest.site_name}")
    print(f"sources: {len(pack.sources)} · blockers: {len(pack.blockers)} · warnings: {len(pack.warnings)}")
    print(f"written: {out}")
    print("boundary: generated support artifact; not DSFA/DPIA/security/regulatory approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

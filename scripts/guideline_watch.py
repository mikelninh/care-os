from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[1]
SOURCES = json.loads((ROOT / "data/guideline_sources.json").read_text(encoding="utf-8"))
STATE_PATH = ROOT / "data/guideline_hashes.json"
CHANGES_PATH = ROOT / "data/guideline_changes.json"

def normalize_html(text: str) -> str:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.I | re.S)
    return re.sub(r"\s+", " ", text).strip()

def main() -> int:
    old = json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {}
    new={}; changes=[]
    with httpx.Client(timeout=30, follow_redirects=True, headers={"User-Agent":"CareOS-Guideline-Watch/0.1"}) as client:
        for source in SOURCES:
            try:
                r=client.get(source["url"]); r.raise_for_status(); digest=hashlib.sha256(normalize_html(r.text).encode()).hexdigest()
                new[source["id"]]={"sha256":digest,"checked_at":datetime.now(timezone.utc).isoformat(),"status_code":r.status_code}
                prev=old.get(source["id"],{}).get("sha256")
                if prev and prev!=digest: changes.append({"id":source["id"],"name":source["name"],"url":source["url"],"previous":prev,"current":digest})
            except Exception as exc:
                new[source["id"]]={"error":str(exc),"checked_at":datetime.now(timezone.utc).isoformat()}
    STATE_PATH.write_text(json.dumps(new,indent=2,ensure_ascii=False),encoding="utf-8")
    CHANGES_PATH.write_text(json.dumps({"changes":changes,"checked_at":datetime.now(timezone.utc).isoformat()},indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"sources":len(SOURCES),"changes":len(changes),"change_ids":[c["id"] for c in changes]},ensure_ascii=False))
    return 0

if __name__ == "__main__": raise SystemExit(main())

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "dev/structure_library" / "reviews" / "creativelands_cc0" / "catalog.json"
SELECTION = ROOT / "dev/structure_library" / "refinement" / "phase16-selection.json"
ALLOWED = {"architectural_clean_reference", "module_quarry", "reference_only"}


def main() -> None:
    catalog_ids = {entry["structure_id"] for entry in json.loads(CATALOG.read_text(encoding="utf-8"))["entries"]}
    document = json.loads(SELECTION.read_text(encoding="utf-8"))
    selections = document["selections"]
    ids = [item["structure_id"] for item in selections]
    issues = []
    if len(ids) != len(set(ids)):
        issues.append("selection contains duplicate structure IDs")
    if set(ids) != catalog_ids:
        issues.append(f"selection/catalog mismatch: missing={sorted(catalog_ids - set(ids))}, extra={sorted(set(ids) - catalog_ids)}")
    for item in selections:
        if item["disposition"] not in ALLOWED:
            issues.append(f"{item['structure_id']}: invalid disposition")
        if item["production_approved"]:
            issues.append(f"{item['structure_id']}: selection cannot grant production approval")
        if item["disposition"] == "module_quarry" and item["module_status"] != "candidate_not_extracted":
            issues.append(f"{item['structure_id']}: module quarry must remain unextracted at this gate")
    counts = Counter(item["disposition"] for item in selections)
    if dict(sorted(counts.items())) != document["counts"]:
        issues.append("stored disposition counts do not match selections")
    if document["production_approved"] != 0:
        issues.append("selection document production approvals must be zero")
    if issues:
        raise SystemExit("\n".join(issues))
    print(f"Validated Phase 16 dispositions for {len(ids)} assets: {dict(counts)}; 0 production approvals")


if __name__ == "__main__":
    main()

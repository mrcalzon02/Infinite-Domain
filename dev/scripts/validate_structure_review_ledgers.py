from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import build_structure_review_ledgers as ledgers

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "structure_library" / "review"
REPORT = ROOT / "docs" / "structure-review-ledger-validation.json"
ALLOWED = {"pending", "pass", "fail"}


def read(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def expected_ids(filename: str):
    if filename.startswith("building"):
        return [
            record["structure_id"] for record in ledgers.load(ledgers.CATALOG)["structures"]
            if record.get("source_role") == "damage_variant"
        ]
    catalog = ledgers.ROAD_CATALOG if filename.startswith("road") else ledgers.MODULE_CATALOG
    return [record["module_id"] for record in ledgers.load(catalog)["modules"]]


def valid_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def main() -> None:
    failures = []
    summaries = {}
    for filename, definition in ledgers.LEDGERS.items():
        rows = read(REVIEW / filename)
        ids = expected_ids(filename)
        actual_ids = [row[definition["id_field"]] for row in rows]
        if actual_ids != ids:
            failures.append(f"{filename}: rows do not exactly match current catalog order")
        passed = failed = completed = 0
        for row in rows:
            asset_id = row[definition["id_field"]]
            values = [row[check].strip().lower() for check in definition["checks"]]
            if any(value not in ALLOWED for value in values):
                failures.append(f"{filename}: {asset_id} uses a status outside pending/pass/fail")
                continue
            if all(value != "pending" for value in values):
                completed += 1
                if not row["reviewer"].strip() or not valid_timestamp(row["reviewed_at"].strip()):
                    failures.append(f"{filename}: {asset_id} completed review lacks reviewer or ISO timestamp")
                if all(value == "pass" for value in values):
                    passed += 1
                if any(value == "fail" for value in values):
                    failed += 1
        summaries[filename] = {
            "assets": len(rows),
            "completed_reviews": completed,
            "all_checks_passed": passed,
            "one_or_more_checks_failed": failed,
            "pending_assets": len(rows) - completed,
            "check_columns": definition["checks"],
        }
    report = {
        "purpose": "Resumable manual evidence ledgers. Validation never promotes an asset or edits production approvals.",
        "allowed_statuses": sorted(ALLOWED),
        "static_ledger_contracts_passed": not failures,
        "automatic_approval_mutation": False,
        "failures": failures,
        "ledgers": summaries,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Review-ledger validation failed:\n- " + "\n- ".join(failures))
    total = sum(item["assets"] for item in summaries.values())
    completed = sum(item["completed_reviews"] for item in summaries.values())
    print(f"Validated resumable review ledgers: {completed}/{total} assets reviewed; no approvals mutated")


if __name__ == "__main__":
    main()

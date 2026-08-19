from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "saves" / "Infinite Domain - Structure QA Flatworld"
LOG = ROOT / "logs" / "latest.log"
REPORT = ROOT / "docs" / "structure-runtime-review.json"
REVIEW = ROOT / "structure_library" / "review"

STAMP = re.compile(r"^\[(?P<stamp>\d{1,2}[A-Za-z]{3}\d{4} \d{2}:\d{2}:\d{2}\.\d{3})\]")
RELEVANT = re.compile(r"infinite_domain|lostcit|structure|template|jigsaw|road_module|structure_module|datapack|mcfunction", re.I)
ERROR = re.compile(r"\bERROR\b|exception|failed to (?:parse|load|execute)|couldn.?t (?:parse|load)|unknown (?:registry|function)|errors in currently selected datapacks|missing key", re.I)


def line_time(line: str):
    match = STAMP.match(line)
    return datetime.strptime(match.group("stamp"), "%d%b%Y %H:%M:%S.%f") if match else None


def ledger_summary(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    check_columns = [name for name in rows[0] if name not in {"asset_id", "reviewer", "reviewed_at", "notes"}] if rows else []
    complete = [row for row in rows if all(row[name].strip().lower() in {"pass", "fail"} for name in check_columns)]
    passed = [row for row in complete if all(row[name].strip().lower() == "pass" for name in check_columns)]
    failed = [row for row in complete if any(row[name].strip().lower() == "fail" for name in check_columns)]
    return {"assets": len(rows), "completed": len(complete), "passed": len(passed), "failed": len(failed), "pending": len(rows) - len(complete)}


def region_coordinates():
    values = set()
    region = WORLD / "region"
    if not region.exists():
        return values
    for path in region.glob("r.*.*.mca"):
        parts = path.stem.split(".")
        if len(parts) == 3:
            try:
                values.add((int(parts[1]), int(parts[2])))
            except ValueError:
                pass
    return values


def main() -> None:
    build_time = datetime.fromtimestamp((WORLD / "level.dat").stat().st_mtime)
    log_time = datetime.fromtimestamp(LOG.stat().st_mtime)
    text = LOG.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    qa_lines = [line for line in lines if "Infinite Domain - Structure QA Flatworld" in line]
    qa_times = [value for line in qa_lines if (value := line_time(line)) is not None]
    world_opened = bool(qa_times and max(qa_times) >= build_time) and (WORLD / "region").exists()
    log_postdates_build = log_time >= build_time
    relevant_errors = [line for line in lines if RELEVANT.search(line) and ERROR.search(line)] if log_postdates_build else []
    regions = region_coordinates()
    harness_evidence = {
        "authoritative_structure_rotation_region_seen": any(-1 <= rx <= 1 and rz <= -4 for rx, rz in regions),
        "road_rotation_region_seen": any(rx >= 2 and rz <= -4 for rx, rz in regions),
        "module_rotation_region_seen": any(rx <= -4 and rz <= -4 for rx, rz in regions),
    }
    ledgers = {
        path.name: ledger_summary(path)
        for path in sorted(REVIEW.glob("*-production-review.csv"))
    }
    runtime_codec_status = "pending_world_launch"
    if world_opened:
        runtime_codec_status = "failed_relevant_log_errors" if relevant_errors else "passed_no_relevant_log_errors"
    report = {
        "qa_world_build_time_local": build_time.isoformat(timespec="seconds"),
        "latest_log_time_local": log_time.isoformat(timespec="seconds"),
        "latest_log_postdates_qa_build": log_postdates_build,
        "qa_world_opened_after_current_build": world_opened,
        "runtime_codec_status": runtime_codec_status,
        "relevant_error_count": len(relevant_errors),
        "relevant_errors": relevant_errors[-200:],
        "generated_region_count": len(regions),
        "rotation_harness_region_evidence": harness_evidence,
        "review_ledgers": ledgers,
        "runtime_review_complete": (
            world_opened
            and not relevant_errors
            and all(harness_evidence.values())
            and all(item["pending"] == 0 for item in ledgers.values())
        ),
        "note": "Region presence proves a harness area was loaded, not that visual checks passed. Pass/fail evidence remains authoritative in the review ledgers.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if world_opened and relevant_errors:
        raise SystemExit(f"Runtime review found {len(relevant_errors)} relevant log errors; inspect {REPORT}")
    print(
        "Runtime review complete" if report["runtime_review_complete"]
        else f"Runtime review pending: world_opened={world_opened}, harnesses={sum(harness_evidence.values())}/3, reviewed={sum(item['completed'] for item in ledgers.values())}/{sum(item['assets'] for item in ledgers.values())}"
    )


if __name__ == "__main__":
    main()

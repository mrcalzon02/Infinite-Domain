from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

from build_structure_qa_world import Reader


ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "structure_library" / "licensing" / "creativelands-extracted-provenance.json"
REPORT = ROOT / "structure_library" / "extracted" / "creativelands_cc0" / "validation-report.json"
RESOURCE_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")


def main() -> None:
    records = json.loads(PROVENANCE.read_text(encoding="utf-8"))["records"]
    results = {}
    issues = []
    for record in records:
        structure_id = record["structure_id"]
        path = ROOT / record["converted_filename"]
        try:
            _, root = Reader(gzip.decompress(path.read_bytes())).root()
            document = root.value
            size = [int(tag.value) for tag in document["size"].value.values]
            palette = [entry.value["Name"].value for entry in document["palette"].value.values]
            blocks = document["blocks"].value.values
            data_version = int(document["DataVersion"].value)
            entities = len(document["entities"].value.values)
        except (OSError, EOFError, KeyError, ValueError) as error:
            issues.append(f"{structure_id}: unreadable NBT ({error})")
            continue
        entry_issues = []
        if not RESOURCE_ID.fullmatch(structure_id):
            entry_issues.append("invalid resource ID")
        if size != record["dimensions"]:
            entry_issues.append(f"dimension mismatch {size} != {record['dimensions']}")
        if len(blocks) != record["unique_output_positions"]:
            entry_issues.append(f"block-count mismatch {len(blocks)} != {record['unique_output_positions']}")
        if data_version != 3955:
            entry_issues.append(f"unexpected DataVersion {data_version}")
        non_minecraft = sorted(name for name in set(palette) if not name.startswith("minecraft:"))
        if non_minecraft:
            entry_issues.append(f"non-minecraft palette IDs {non_minecraft}")
        if entities:
            entry_issues.append(f"unexpected entities {entities}")
        if record["production_approved"]:
            entry_issues.append("review extraction incorrectly marked production-approved")
        issues.extend(f"{structure_id}: {issue}" for issue in entry_issues)
        results[structure_id] = {
            "dimensions": size,
            "blocks": len(blocks),
            "palette_entries": len(palette),
            "data_version": data_version,
            "entities": entities,
            "passed": not entry_issues,
        }
    report = {
        "format_version": 1,
        "purpose": "Static NBT validation only; not visual or production approval.",
        "validated_count": len(results),
        "issues": issues,
        "structures": results,
        "production_approved": False,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if issues or len(results) != len(records):
        raise SystemExit("\n".join(issues) or f"validated {len(results)} of {len(records)} records")
    print(f"Validated {len(results)} Creative Lands review NBT files; 0 visual or production approvals")


if __name__ == "__main__":
    main()

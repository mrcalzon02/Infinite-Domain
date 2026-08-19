from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from convert_nbt_to_lostcities import ASSETS, CATALOG, FLOOR_HEIGHT, REPORT, ROOT, load_structure


VALIDATION_REPORT = ROOT / "docs" / "lostcities-conversion-validation.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_structure(entry: dict[str, Any], conversion: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    source_size, source_blocks = load_structure(ROOT / entry["source_template"])
    sx, sy, sz = source_size
    dimx, dimz = conversion["chunk_footprint"]
    rebuilt: dict[tuple[int, int, int], tuple[str, dict[str, Any] | None]] = {}

    multi_path = ASSETS / "multibuildings" / "converted" / f"{entry['structure_id'].split(':', 1)[1]}.json"
    multi = load_json(multi_path)
    if multi.get("dimx") != dimx or multi.get("dimz") != dimz:
        issues.append("multibuilding dimensions differ from conversion report")
    grid = multi.get("buildings", [])
    if len(grid) != dimx or any(len(column) != dimz for column in grid):
        issues.append("multibuilding grid shape is invalid")
        return issues

    for chunk_x in range(dimx):
        for chunk_z in range(dimz):
            building_id = grid[chunk_x][chunk_z]
            building_path = ASSETS / "buildings" / f"{building_id.split(':', 1)[1]}.json"
            if not building_path.is_file():
                issues.append(f"missing building asset {building_id}")
                continue
            building = load_json(building_path)
            refs = building.get("parts", [])
            expected_floors = list(range(conversion["floor_bands"]))
            if sorted(ref.get("floor") for ref in refs) != expected_floors:
                issues.append(f"{building_id}: floor references are incomplete")
            for ref in refs:
                floor = ref["floor"]
                part_id = ref["part"]
                part_path = ASSETS / "parts" / f"{part_id.split(':', 1)[1]}.json"
                if not part_path.is_file():
                    issues.append(f"missing part asset {part_id}")
                    continue
                part = load_json(part_path)
                if part.get("xsize") != 16 or part.get("zsize") != 16:
                    issues.append(f"{part_id}: part is not 16x16")
                palette_entries = part.get("palette", {}).get("palette", [])
                palette: dict[str, tuple[str, dict[str, Any] | None]] = {}
                for palette_entry in palette_entries:
                    char = palette_entry.get("char", "")
                    if len(char) != 1 or char == " ":
                        issues.append(f"{part_id}: invalid palette character")
                        continue
                    if char in palette:
                        issues.append(f"{part_id}: duplicate palette character {char!r}")
                    palette[char] = (palette_entry["block"], palette_entry.get("tag"))
                slices = part.get("slices", [])
                if len(slices) > FLOOR_HEIGHT:
                    issues.append(f"{part_id}: more than {FLOOR_HEIGHT} slices in one floor band")
                for local_y, rows in enumerate(slices):
                    if len(rows) != 16 or any(len(row) != 16 for row in rows):
                        issues.append(f"{part_id}: slice is not exactly 16x16")
                        continue
                    for local_z, row in enumerate(rows):
                        for local_x, char in enumerate(row):
                            if char == " ":
                                continue
                            if char not in palette:
                                issues.append(f"{part_id}: slice uses unmapped character {char!r}")
                                continue
                            x, y, z = chunk_x * 16 + local_x, floor * FLOOR_HEIGHT + local_y, chunk_z * 16 + local_z
                            if x < sx and y < sy and z < sz:
                                rebuilt[(x, y, z)] = palette[char]
                            else:
                                issues.append(f"{part_id}: non-air block outside declared source bounds")

    missing = set(source_blocks) - set(rebuilt)
    extra = set(rebuilt) - set(source_blocks)
    changed = {pos for pos in set(source_blocks) & set(rebuilt) if source_blocks[pos] != rebuilt[pos]}
    if missing:
        issues.append(f"round-trip lost {len(missing)} blocks")
    if extra:
        issues.append(f"round-trip added {len(extra)} blocks")
    if changed:
        issues.append(f"round-trip changed {len(changed)} block states or tags")
    return issues


def main() -> None:
    catalog = load_json(CATALOG)["structures"]
    conversion = {entry["structure_id"]: entry for entry in load_json(REPORT)["structures"]}
    results: dict[str, Any] = {}
    for entry in catalog:
        structure_id = entry["structure_id"]
        issues = validate_structure(entry, conversion[structure_id]) if structure_id in conversion else ["missing conversion report entry"]
        results[structure_id] = {"lossless_round_trip": not issues, "issues": issues, "production_approved": False}
    report = {
        "purpose": "Static Lost Cities asset validation plus lossless block-state/NBT round trip. Runtime codec and visual approval remain separate gates.",
        "valid": all(result["lossless_round_trip"] for result in results.values()),
        "structures_checked": len(results),
        "structures": results,
    }
    VALIDATION_REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not report["valid"]:
        raise SystemExit("\n".join(f"{name}: {', '.join(result['issues'])}" for name, result in results.items() if result["issues"]))
    print(f"Validated {len(results)} lossless NBT-to-Lost-Cities round trips; runtime codec validation still pending")


if __name__ == "__main__":
    main()

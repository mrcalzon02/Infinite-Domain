from __future__ import annotations

import errno
import json
import time
from pathlib import Path
from typing import Any

from convert_nbt_to_lostcities import (
    ASSETS,
    CATALOG,
    FLOOR_HEIGHT,
    REPORT,
    ROOT,
    load_structure,
    stabilized_source_value,
)


VALIDATION_REPORT = ROOT / "dev/docs" / "lostcities-conversion-validation.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    """Write validation evidence through the same bounded Windows retry as
    the converter.

    The game/launcher scanner can briefly hold a freshly regenerated JSON
    path and make Windows return EINVAL. Retry only that transient condition;
    permission, path, and disk failures remain immediate errors.
    """
    content = json.dumps(value, indent=2) + "\n"
    for attempt in range(12):
        try:
            path.write_text(content, encoding="utf-8", newline="\n")
            return
        except OSError as error:
            if error.errno != errno.EINVAL or attempt == 11:
                raise
            time.sleep(min(0.25, 0.05 * (attempt + 1)))


def validate_structure(entry: dict[str, Any], conversion: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    source_size, source_blocks = load_structure(ROOT / entry["source_template"])
    source_blocks = {pos: stabilized_source_value(value) for pos, value in source_blocks.items()}
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
            repeatable = conversion.get("repeatable_storey")
            authored_refs: list[tuple[int, dict[str, Any]]] = []
            if repeatable:
                cellar_refs = [ref for ref in refs if ref.get("cellar") is True]
                ground_refs = [ref for ref in refs if ref.get("ground") is True]
                top_refs = [ref for ref in refs if ref.get("top") is True]
                repeat_refs = [
                    ref for ref in refs
                    if ref.get("cellar") is False
                    and ref.get("ground") is False
                    and ref.get("top") is False
                ]
                semantic_ok = (
                    len(refs) == 4
                    and all(len(group) == 1 for group in (cellar_refs, ground_refs, repeat_refs, top_refs))
                    and all("part" in ref and "floor" not in ref for ref in refs)
                    and building.get("mincellars") == 1
                    and building.get("maxcellars") == 1
                    and building.get("minfloors") == repeatable["minfloors"]
                    and building.get("maxfloors") == repeatable["maxfloors"]
                )
                if not semantic_ok:
                    issues.append(f"{building_id}: repeatable cellar/ground/storey/top roles are invalid")
                    continue
                authored_refs = [(repeatable["cellar_band"], cellar_refs[0])]
                authored_refs.append((repeatable["ground_band"], ground_refs[0]))
                authored_refs.extend(
                    (floor, repeat_refs[0])
                    for floor in range(repeatable["repeat_source_band"], repeatable["top_band"])
                )
                authored_refs.append((repeatable["top_band"], top_refs[0]))
            else:
                expected_floors = list(range(conversion["floor_bands"]))
                # Older approved conversions may carry one final floor-less
                # repeat-slice fallback. It is not an authored floor and must
                # not enter the NBT round-trip coordinates.
                floored_refs = [ref for ref in refs if isinstance(ref.get("floor"), int)]
                fallback_refs = [ref for ref in refs if "floor" not in ref]
                malformed_refs = [
                    ref for ref in refs
                    if "floor" in ref and not isinstance(ref.get("floor"), int)
                ]
                if (malformed_refs or len(fallback_refs) > 1
                        or any("part" not in ref for ref in fallback_refs)):
                    issues.append(f"{building_id}: invalid repeat-slice fallback reference")
                if sorted(ref["floor"] for ref in floored_refs) != expected_floors:
                    issues.append(f"{building_id}: floor references are incomplete")
                authored_refs = [(ref["floor"], ref) for ref in floored_refs]

            for floor, ref in authored_refs:
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
        results[structure_id] = {"lossless_round_trip": not issues, "issues": issues, "production_approved": not issues}
    report = {
        "purpose": "Static Lost Cities asset validation plus lossless block-state/NBT round trip. A structure is production_approved automatically once its round trip is lossless; there is no separate manual sign-off gate.",
        "valid": all(result["lossless_round_trip"] for result in results.values()),
        "structures_checked": len(results),
        "structures": results,
    }
    write_json(VALIDATION_REPORT, report)
    if not report["valid"]:
        raise SystemExit("\n".join(f"{name}: {', '.join(result['issues'])}" for name, result in results.items() if result["issues"]))
    print(f"Validated {len(results)} lossless NBT-to-Lost-Cities round trips; runtime codec validation still pending")


if __name__ == "__main__":
    main()

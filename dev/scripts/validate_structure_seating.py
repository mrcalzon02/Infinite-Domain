#!/usr/bin/env python3
"""Report-only audit of custom structure vertical seating.

Authority: docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md (§4, §5, §8).

Phase 0 behaviour: REPORTS. Exits 0 unless it finds a hard footprint clip
(max_distance_from_center smaller than the NBT footprint half-diagonal), which
Minecraft would silently truncate.

Everything else is a finding tracked toward the Phase 1 gate: each in-scope
structure declares a `seating` block (doc sec. 9.4), start_height == -grade_y
(floor-flush; OD-2 resolved), and the sub-grade layers are a solid footing pad
of at most 3 courses - anything deeper or with a room below the floor goes on
the A6 buried list instead.

Scope: kubejs/data/infinite_domain/worldgen/structure/{wasteland,minor,planetary,
alien,offworld,nether}. abyssal/ and deep_sea/ have their own seabed regime;
old_world/ is not scatter-placed.
"""
from __future__ import annotations

import gzip
import json
import math
import struct
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STRUCT_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure"
POOL_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "worldgen" / "template_pool"
NBT_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "structure"

IN_SCOPE_DIRS = {"wasteland", "minor", "planetary", "alien", "offworld", "nether"}

# docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md §5 A6. Structures with authored
# sub-grade content; a negative start_height / bury is correct for these.
A6_BURIED = {
    "wasteland/bunker_network",
    "wasteland/survivor_cache",
    "wasteland/collapsed_subway_station",
    "wasteland/abandoned_quarry",
    "wasteland/collapsed_mine_entrance",
    "wasteland/excavator_pit",
    "wasteland/ruined_gas_station",
    "wasteland/buried_bank_vault",
}

# 128-block jigsaw codec limit minus a beard/padding margin (WORLDGEN_STRUCTURE_SAFETY.md).
MAX_DISTANCE_CEILING = 116


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def nbt_size(path: Path) -> tuple[int, int, int] | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    i = raw.find(b"\x09\x00\x04size")
    if i < 0:
        return None
    p = i + 1 + 2 + 4
    et = raw[p]
    ln = struct.unpack(">i", raw[p + 1:p + 5])[0]
    if et != 3 or ln != 3:
        return None
    x, y, z = struct.unpack(">iii", raw[p + 5:p + 17])
    return x, y, z


def start_pool_footprint(sdef: dict) -> tuple[int, int, int] | None:
    pool_id = sdef.get("start_pool", "")
    _, _, pool_rest = pool_id.partition(":")
    pfile = POOL_ROOT / (pool_rest + ".json")
    if not pfile.exists():
        return None
    best = None
    for el in load_json(pfile).get("elements", []):
        loc = el.get("element", {}).get("location", "")
        _, _, loc_rest = loc.partition(":")
        size = nbt_size(NBT_ROOT / (loc_rest + ".nbt"))
        if size and (best is None or size[0] * size[2] > best[0] * best[2]):
            best = size
    return best


def start_height_repr(sh) -> str:
    if isinstance(sh, dict):
        if "absolute" in sh:
            return f"absolute {sh['absolute']}"
        return sh.get("type", "?").split(":")[-1]
    return str(sh)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    beard_box_surface: list[str] = []
    combos: Counter = Counter()
    rows = 0

    for path in sorted(STRUCT_ROOT.rglob("*.json")):
        rel = path.relative_to(STRUCT_ROOT)
        if len(rel.parts) < 2 or rel.parts[0] not in IN_SCOPE_DIRS:
            continue
        name = str(rel.with_suffix("")).replace("\\", "/")
        d = load_json(path)
        if d.get("type") != "minecraft:jigsaw":
            continue
        rows += 1

        ta = d.get("terrain_adaptation", "none")
        sh = d.get("start_height")
        proj = d.get("project_start_to_heightmap")
        mdc = d.get("max_distance_from_center")
        abs_h = sh.get("absolute") if isinstance(sh, dict) else None

        combos[(ta, start_height_repr(sh), proj or "-")] += 1

        # --- footprint / codec ---
        fp = start_pool_footprint(d)
        if fp:
            half_diag = math.hypot(fp[0] / 2, fp[2] / 2)
            if mdc is not None and mdc < half_diag:
                errors.append(f"{name}: max_distance_from_center {mdc} < footprint half-diagonal "
                              f"{half_diag:.0f} ({fp[0]}x{fp[2]}) - Minecraft truncates the piece")
            elif mdc is not None and mdc < half_diag + 12:
                warnings.append(f"{name}: max_distance_from_center {mdc} only {mdc - half_diag:.0f} clear of "
                                f"footprint half-diagonal {half_diag:.0f} - no room for the beard skirt")
            if mdc is not None and mdc > MAX_DISTANCE_CEILING:
                warnings.append(f"{name}: max_distance_from_center {mdc} > {MAX_DISTANCE_CEILING} "
                                f"(128 codec limit minus margin)")

        # --- seating mismatch signature (§4.4) ---
        is_beard = ta in ("beard_thin", "beard_box")
        if is_beard and abs_h is not None and abs_h < 0:
            if name in A6_BURIED:
                info.append(f"{name}: {ta} + start_height {abs_h}  [expected - A6 buried list]")
            else:
                warnings.append(
                    f"{name}: {ta} + negative start_height {abs_h} but NOT on the A6 buried list - "
                    f"beard reference is desynced from the grade line (see doc sec. 4.4)"
                )
        if is_beard and not proj:
            warnings.append(f"{name}: {ta} without project_start_to_heightmap - seats at an absolute Y, not terrain")
        if ta == "beard_box" and name not in A6_BURIED:
            beard_box_surface.append(name)

    with_seating = sum(
        1 for p in STRUCT_ROOT.rglob("*.json")
        if len(p.relative_to(STRUCT_ROOT).parts) >= 2
        and p.relative_to(STRUCT_ROOT).parts[0] in IN_SCOPE_DIRS
        and "seating" in load_json(p)
    )

    print("=" * 78)
    print("structure seating audit  (docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md)")
    print("=" * 78)
    print(f"in-scope jigsaw structures: {rows}   ({sorted(IN_SCOPE_DIRS)})")
    print(f"with a `seating` block:      {with_seating}   (Phase 1 target: {rows})")
    print()
    print("(terrain_adaptation, start_height, project_start_to_heightmap) in use:")
    for (ta, shr, pr), c in combos.most_common():
        print(f"  {c:4}  {ta:<11} | {shr:<16} | {pr}")
    print()
    print(f"beard_box + grade_y=1 assumption (Phase 1 -> beard_thin + declared grade_y): "
          f"{len(beard_box_surface)} structures")
    print("  the mechanics in section 4 mean every one of these is mis-seated wherever its")
    print("  authored floor is not exactly one block above the NBT origin.")
    print()
    for label, bucket in (("ERROR", errors), ("WARN", warnings), ("INFO", info)):
        if bucket:
            print(f"--- {label} ({len(bucket)}) ---")
            for line in bucket:
                print(f"  {label}: {line}")
            print()
    if not (errors or warnings or info):
        print("no findings")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

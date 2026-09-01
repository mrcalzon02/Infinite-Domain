#!/usr/bin/env python3
"""Report-only audit of custom structure-set placement.

Authority: docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md (§3, §8).

Phase 0 behaviour: this script REPORTS. It exits 0 unless it finds a hard codec
violation (separation >= spacing), which Minecraft itself would reject. Every
other finding is informational and tracked toward the Phase 1 gate (every live
set carries an exclusion_zone; aggregate co-occurrence under budget).

Scope: kubejs/data/infinite_domain/worldgen/structure_set/**. Third-party sets
and the vanilla-namespace sets are out of scope for this contract.
"""
from __future__ import annotations

import gzip
import json
import math
import struct
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SS_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure_set"
STRUCT_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure"
POOL_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "worldgen" / "template_pool"
NBT_ROOT = REPO / "kubejs" / "data" / "infinite_domain" / "structure"

# Families governed by docs/ABYSSAL_OCEAN_PROGRAM.md /
# DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md - separate regime.
OUT_OF_SCOPE_DIRS = {"abyssal", "deep_sea"}


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
    p = i + 1 + 2 + 4  # tag id + name-len + name + list elem-type(1) + list-len(4)
    et = raw[p]
    ln = struct.unpack(">i", raw[p + 1:p + 5])[0]
    if et != 3 or ln != 3:
        return None
    x, y, z = struct.unpack(">iii", raw[p + 5:p + 17])
    return x, y, z


def resolve_footprint(structure_id: str) -> tuple[int, int] | None:
    """structure_set entry id -> (x, z) footprint from the start-pool NBT."""
    ns, _, rest = structure_id.partition(":")
    sfile = STRUCT_ROOT / (rest + ".json")
    if not sfile.exists():
        return None
    sdef = load_json(sfile)
    pool_id = sdef.get("start_pool", "")
    _, _, pool_rest = pool_id.partition(":")
    pfile = POOL_ROOT / (pool_rest + ".json")
    if not pfile.exists():
        return None
    elements = load_json(pfile).get("elements", [])
    best = None
    for el in elements:
        loc = el.get("element", {}).get("location", "")
        _, _, loc_rest = loc.partition(":")
        size = nbt_size(NBT_ROOT / (loc_rest + ".nbt"))
        if size:
            fx, fz = size[0], size[2]
            if best is None or fx * fz > best[0] * best[1]:
                best = (fx, fz)
    return best


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    sets: list[dict] = []
    for path in sorted(SS_ROOT.rglob("*.json")):
        rel = path.relative_to(SS_ROOT)
        d = load_json(path)
        placement = d.get("placement", {})
        structs = d.get("structures", [])
        live = bool(structs)
        row = {
            "file": str(rel).replace("\\", "/"),
            "dir": rel.parts[0] if len(rel.parts) > 1 else "",
            "live": live,
            "n": len(structs),
            "type": placement.get("type"),
            "spacing": placement.get("spacing"),
            "separation": placement.get("separation"),
            "salt": placement.get("salt"),
            "frequency": placement.get("frequency", 1.0),
            "exclusion_zone": placement.get("exclusion_zone"),
            "structure_ids": [s.get("structure") for s in structs],
        }
        sets.append(row)

    in_scope = [s for s in sets if s["dir"] not in OUT_OF_SCOPE_DIRS]
    live_sets = [s for s in in_scope if s["live"]]

    # 1. Hard codec invariant.
    for s in in_scope:
        sp, se = s["spacing"], s["separation"]
        if s["type"] == "minecraft:random_spread" and sp is not None and se is not None:
            if se >= sp:
                errors.append(f"{s['file']}: separation ({se}) >= spacing ({sp}) - Minecraft rejects this set")

    # 2. Shared salts among LIVE sets (inert sets with structures:[] are harmless).
    by_salt: dict[int, list[str]] = defaultdict(list)
    for s in live_sets:
        if s["salt"] is not None:
            by_salt[s["salt"]].append(s["file"])
    for salt, files in sorted(by_salt.items()):
        if len(files) > 1:
            warnings.append(f"salt {salt} shared by {len(files)} live sets: {', '.join(files)}")

    # 3. Exclusion-zone coverage (Phase 1 gate; informational now).
    no_excl = [s["file"] for s in live_sets if not s["exclusion_zone"]]
    if no_excl:
        info.append(
            f"{len(no_excl)}/{len(live_sets)} live sets have no exclusion_zone "
            f"(wasteland/ is B2-consolidated - doc sec. 7.5; minor/* and the small "
            f"offworld families still run independent grids)"
        )

    # 4. Spacing vs footprint.
    for s in live_sets:
        if s["type"] != "minecraft:random_spread" or not s["spacing"]:
            continue
        biggest = None
        for sid in s["structure_ids"]:
            fp = resolve_footprint(sid) if sid else None
            if fp and (biggest is None or fp[0] * fp[1] > biggest[0] * biggest[1]):
                biggest = fp
        if not biggest:
            continue
        diag = math.hypot(*biggest)
        # separation is the guaranteed floor (chunks) between neighbouring starts.
        guaranteed_blocks = s["separation"] * 16 if s["separation"] else 0
        if guaranteed_blocks < diag:
            warnings.append(
                f"{s['file']}: separation {s['separation']}ch = {guaranteed_blocks}b < footprint diagonal "
                f"{diag:.0f}b ({biggest[0]}x{biggest[1]}) - neighbouring starts can overlap"
            )
        elif guaranteed_blocks < diag + 24:
            info.append(
                f"{s['file']}: separation {guaranteed_blocks}b only {guaranteed_blocks - diag:.0f}b clear of "
                f"footprint diagonal {diag:.0f}b"
            )

    # 5. Crude aggregate density per top-level family dir: sum of per-chunk
    #    placement probability (frequency / spacing^2) over that dir's live
    #    random_spread sets. Sets in different dirs largely target different
    #    biomes/dimensions, so the per-dir number is the meaningful one - it is
    #    roughly how many starts compete for the same ground.
    dens: dict[str, float] = defaultdict(float)
    for s in live_sets:
        if s["type"] == "minecraft:random_spread" and s["spacing"]:
            dens[s["dir"] or "(root)"] += float(s["frequency"]) / (s["spacing"] ** 2)

    # ---- report ----
    print("=" * 78)
    print("structure-set separation audit  (docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md)")
    print("=" * 78)
    print(f"structure_set files:      {len(sets)}")
    print(f"  in scope:               {len(in_scope)}  (excludes {sorted(OUT_OF_SCOPE_DIRS)})")
    print(f"  live (structures != []): {len(live_sets)}")
    print(f"  inert (structures: []):  {len(in_scope) - len(live_sets)}")
    print("start density by family (starts per 10,000 chunks that share ground):")
    for d, v in sorted(dens.items(), key=lambda kv: -kv[1]):
        n = sum(1 for s in live_sets if (s["dir"] or "(root)") == d)
        print(f"  {d:<16} {v * 10000:7.1f}   ({n} live sets)")
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

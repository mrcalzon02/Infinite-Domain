#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-037 abyssal nodule-field analogues."""
from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "92ee54237b0fe4090e153c7b539012a3d484e7e7"


def nodule_field():
    b = StructureBuilder((41, 2, 41))
    centers = ((9, 10, 7), (29, 9, 6), (15, 29, 8), (31, 30, 7), (21, 20, 5))

    for ci, (cx, cz, radius) in enumerate(centers):
        for x in range(max(1, cx - radius), min(40, cx + radius + 1)):
            for z in range(max(1, cz - radius), min(40, cz + radius + 1)):
                dx = x - cx
                dz = z - cz
                rough_radius = (
                    radius * radius
                    + 2.5 * math.sin((x + ci * 7) * 0.63)
                    + 2.0 * math.cos((z - ci * 5) * 0.51)
                )
                if dx * dx * 1.15 + dz * dz * 0.85 > rough_radius:
                    continue

                # Only part of each province replaces the native seabed, preserving
                # broad soft-sediment gaps instead of painting a solid resource patch.
                matrix = (x * 31 + z * 17 + ci * 43) % 23
                if matrix in (0, 1, 2, 3, 4):
                    b.set(x, 0, z, "minecraft:gravel")

                # Sparse dark clasts are decorative analogues only. No ore blocks,
                # raw materials, loot or progression-bearing substitutions are used.
                if (x * 13 + z * 29 + ci * 11) % 17 in (0, 1):
                    material = (
                        "minecraft:blackstone"
                        if (x + z + ci) % 3
                        else "minecraft:cobbled_deepslate"
                    )
                    b.set(x, 0, z, material)
                    if (x * 7 + z * 5 + ci) % 11 == 0:
                        b.set(
                            x,
                            1,
                            z,
                            "minecraft:polished_blackstone_button",
                            {"face": "floor", "facing": "north", "powered": "false"},
                        )

    # A current-scoured corridor cuts across otherwise separate provinces.
    for x in range(4, 37):
        z = 20 + int(round(2.2 * math.sin(x * 0.28)))
        for dz in (-1, 0, 1):
            b.remove(x, 0, z + dz)
            b.remove(x, 1, z + dz)

    return b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    data = nodule_field().bytes()
    path = output / "nodule_field.nbt"
    path.write_bytes(data)
    sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    print(f"nodule_field.nbt: {len(data)} bytes git_blob={sha}")
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(
            f"OSF-037 NBT verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}"
        )
    if args.verify:
        print("verified: OSF-037 nodule-field Git blob matches embedded authority")


if __name__ == "__main__":
    main()

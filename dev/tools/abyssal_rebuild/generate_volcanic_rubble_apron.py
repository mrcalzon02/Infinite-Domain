#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-010 volcanic rubble aprons."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "7581d4a4d69a39ed8d38d78706b112eae94db697"


def volcanic_rubble_apron() -> StructureBuilder:
    b = StructureBuilder((41, 6, 41))
    cx, cz = 20, 20
    max_r = 19.0

    for x in range(1, 40):
        for z in range(1, 40):
            dx = x - cx
            dz = z - cz
            r = (dx * dx + dz * dz) ** 0.5
            if r > max_r:
                continue

            # Downslope density gradient: coverage thins the farther a cell
            # sits from the volcanic relief this apron skirts.
            jitter = (x * 13 + z * 17) % 11
            keep_threshold = 2 + int((r / max_r) * 8)
            if jitter >= keep_threshold:
                continue

            # Sediment-filled interstices between the angular clasts.
            if (x * 7 + z * 5 + jitter) % 6 == 0:
                continue

            fall = max(0.0, 1.0 - r / max_r)
            top = int(fall * 4)
            if (x * 3 + z * 2) % 9 == 0:
                top = max(0, top - 1)

            material = (
                "minecraft:basalt" if (x + z) % 4 == 0
                else "minecraft:blackstone" if (x * 5 + z) % 7 == 0
                else "minecraft:cobbled_deepslate" if (x + z * 3) % 11 == 0
                else "minecraft:tuff"
            )
            for y in range(0, top + 1):
                b.set(x, y, z, material)
            if top == 0 and (x * 2 + z) % 5 == 0:
                b.set(x, 0, z, "minecraft:gravel")

    # Broken cone/flank material: taller angular clasts nearer the source.
    for cxo, czo, h in ((16, 15, 3), (24, 18, 4), (19, 25, 3), (13, 22, 2), (27, 24, 2)):
        for dxo, dzo in ((0, 0), (1, 0), (0, 1), (1, 1)):
            x, z = cxo + dxo, czo + dzo
            if 1 <= x < 40 and 1 <= z < 40:
                for y in range(h):
                    b.set(x, y, z, "minecraft:blackstone" if y == h - 1 else "minecraft:basalt")

    return b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    data = volcanic_rubble_apron().bytes()
    path = output / "volcanic_rubble_apron.nbt"
    path.write_bytes(data)
    sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    print(f"volcanic_rubble_apron.nbt: {len(data)} bytes git_blob={sha}")
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(f"OSF-010 verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}")
    if args.verify:
        print("verified: OSF-010 volcanic rubble apron Git blob matches embedded authority")


if __name__ == "__main__":
    main()

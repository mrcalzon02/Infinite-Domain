#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-008 basaltic flow lobes and cooled lava fronts."""
from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "29eca0e9510f2bd1c23f13c30b8cc3bf4ac0156a"


def basaltic_flow_lobes() -> StructureBuilder:
    b = StructureBuilder((49, 7, 49))
    lobes = (
        (13, 14, 10, 7, 0),
        (22, 17, 11, 8, 1),
        (31, 15, 9, 6, 2),
        (18, 28, 12, 8, 3),
        (30, 29, 13, 9, 4),
        (37, 34, 8, 6, 5),
    )

    for ci, (cx, cz, rx, rz, phase) in enumerate(lobes):
        for x in range(max(1, cx - rx - 2), min(48, cx + rx + 3)):
            for z in range(max(1, cz - rz - 2), min(48, cz + rz + 3)):
                dx = (x - cx) / rx
                dz = (z - cz) / rz
                wobble = 0.10 * math.sin((x + phase * 5) * 0.55) + 0.08 * math.cos((z - phase * 4) * 0.47)
                distance = dx * dx + dz * dz + wobble
                if distance > 1.0:
                    continue

                # Preserve native sediment/water windows so this reads as overlapping
                # cooled flows rather than a solid artificial basalt platform.
                if (x * 17 + z * 29 + ci * 31) % 43 in (0, 1, 2):
                    continue

                height = 0
                if distance < 0.58 and (x + 2 * z + ci) % 5 in (0, 1):
                    height = 1
                if distance < 0.25 and (x * 3 + z + ci) % 7 == 0:
                    height = 2

                material = (
                    "minecraft:smooth_basalt"
                    if (x + z + ci) % 5 in (0, 1)
                    else "minecraft:blackstone"
                    if (x * 7 + z * 11 + ci) % 13 == 0
                    else "minecraft:basalt"
                )
                for y in range(height + 1):
                    b.set(x, y, z, material)

        # Incomplete pressure ridge through each flow lobe.
        for step in range(-rx + 2, rx - 1):
            x = cx + step
            z = cz + int(round(1.7 * math.sin((step + phase) * 0.42)))
            if not (1 <= x < 48 and 1 <= z < 48) or (step + ci) % 6 == 0:
                continue
            b.set(x, 1, z, "minecraft:smooth_basalt")
            if abs(step) < rx // 3 and (step + ci) % 4 == 0:
                b.set(x, 2, z, "minecraft:basalt")

    # Abrupt crescent-shaped cooled front on the youngest southeastern flow.
    cx, cz = 30, 29
    for degrees in range(25, 155, 6):
        angle = math.radians(degrees)
        x = int(round(cx + 14 * math.cos(angle)))
        z = int(round(cz + 10 * math.sin(angle)))
        if not (1 <= x < 48 and 1 <= z < 48) or (x + z) % 7 == 0:
            continue
        b.set(x, 1, z, "minecraft:blackstone")
        if (x * 5 + z) % 4 == 0:
            b.set(x, 2, z, "minecraft:basalt")
        if (x + 2 * z) % 9 == 0:
            b.set(x, 0, z, "minecraft:tuff")

    # Sparse altered/sedimented chilled margins.
    for x, z in ((7, 12), (9, 20), (15, 36), (24, 39), (35, 9), (41, 27), (39, 40), (28, 8)):
        for dx, dz in ((0, 0), (1, 0), (0, 1)):
            b.set(x + dx, 0, z + dz, "minecraft:tuff")

    return b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    data = basaltic_flow_lobes().bytes()
    path = output / "basaltic_flow_lobes.nbt"
    path.write_bytes(data)
    sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    print(f"basaltic_flow_lobes.nbt: {len(data)} bytes git_blob={sha}")
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(f"OSF-008 verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}")
    if args.verify:
        print("verified: OSF-008 basaltic flow-lobe Git blob matches embedded authority")


if __name__ == "__main__":
    main()

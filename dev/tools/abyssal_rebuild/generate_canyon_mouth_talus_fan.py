#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-033 canyon-mouth talus fans."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOB = "55b7159ba4e4c4ee28628d2817cbd872186aaa8c"


def canyon_mouth_talus_fan() -> StructureBuilder:
    b = StructureBuilder((41, 5, 41))
    mouth_x, mouth_z = 3, 20

    for x in range(1, 40):
        dx = x - mouth_x
        if dx < 0:
            continue
        # The fan's half-width widens with distance from the canyon mouth,
        # giving an asymmetric wedge rather than a circular boulder pile.
        half_width = 2 + dx * 0.42
        for z in range(1, 40):
            dz = z - mouth_z
            if abs(dz) > half_width:
                continue
            dist = (dx * dx + dz * dz) ** 0.5
            if dist > 37:
                continue

            proximal = max(0.0, 1.0 - dist / 37.0)
            jitter = (x * 11 + z * 7) % 9
            keep_threshold = 2 + int((1.0 - proximal) * 6)
            if jitter >= keep_threshold:
                continue
            if (x * 5 + z * 3 + jitter) % 7 == 0:
                continue  # sediment gap between blocks

            top = int(proximal * 3)
            coarse = proximal > 0.55
            material = (
                "minecraft:stone" if coarse and (x + z) % 3 == 0
                else "minecraft:cobbled_deepslate" if coarse
                else "minecraft:deepslate" if (x * 3 + z) % 5 == 0
                else "minecraft:tuff" if (x + z * 2) % 6 == 0
                else "minecraft:gravel"
            )
            for y in range(0, top + 1):
                b.set(x, y, z, material)
            if top == 0:
                b.set(x, 0, z, "minecraft:gravel")

    # Coarse proximal boulders right at the canyon mouth.
    for dxo, dzo, h in ((4, -1, 2), (5, 1, 2), (6, 0, 3), (3, 2, 2)):
        x, z = mouth_x + dxo, mouth_z + dzo
        if 1 <= x < 40 and 1 <= z < 40:
            for y in range(h):
                b.set(x, y, z, "minecraft:cobbled_deepslate")

    return b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    data = canyon_mouth_talus_fan().bytes()
    path = output / "canyon_mouth_talus_fan.nbt"
    path.write_bytes(data)
    sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    print(f"canyon_mouth_talus_fan.nbt: {len(data)} bytes git_blob={sha}")
    if args.verify and sha != EXPECTED_GIT_BLOB:
        raise SystemExit(f"OSF-033 verification failed: expected {EXPECTED_GIT_BLOB}, got {sha}")
    if args.verify:
        print("verified: OSF-033 canyon-mouth talus fan Git blob matches embedded authority")


if __name__ == "__main__":
    main()

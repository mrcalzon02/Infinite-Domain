#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-031 slump blocks / rotated
sediment rafts. Three failure-age variants share one footprint and one build
routine, aging the same coherent displaced block from a sharp recent failure
to a buried relict."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    "slump_block_recent.nbt": "a7275857ef157c9f93d011302da129f4ee585dc8",
    "slump_block_weathered.nbt": "4c38182141a32a2d3832e000cf568cc19d994b8f",
    "slump_block_relict.nbt": "fc3f63b0e0667d076f093bc4e62ef765fc4ac4ce",
}

BANDS = ("minecraft:stone", "minecraft:deepslate", "minecraft:tuff")


def _slump_block(age: float) -> StructureBuilder:
    """age: 0.0 = a fresh failure with a crisp headwall scarp, 1.0 = an old
    relict raft mostly buried under its own sediment drape."""
    b = StructureBuilder((33, 14, 33))
    block_x0, block_x1 = 6, 24
    block_z0, block_z1 = 8, 22
    base_h = 3
    tilt = 0.35  # bedding tilt across the block's width -- the "rotated raft"
    erosion = int(age * 3)

    for x in range(block_x0, block_x1 + 1):
        top = max(1, int(base_h + tilt * (x - block_x0)) - erosion)
        for z in range(block_z0, block_z1 + 1):
            jitter = (x * 7 + z * 11) % 5
            local_top = top - (1 if jitter == 0 and age > 0.3 else 0)
            for y in range(0, local_top + 1):
                b.set(x, y, z, BANDS[y % len(BANDS)])

    # Headwall break surface: a steep near-vertical face at the block's
    # low-x edge -- exposed rock, not a sediment-covered natural slope.
    for z in range(block_z0, block_z1 + 1):
        for y in range(0, base_h + 2):
            if (z * 3 + y) % 6 != 0:
                b.set(block_x0 - 1, y, z, "minecraft:deepslate")

    # Downslope debris wake: the block's own failure debris trailing toward
    # +z, thinning and shrinking with distance rather than a separate field.
    for step in range(1, 10):
        wz = block_z1 + step
        if wz >= 32:
            break
        spread = 2 + step // 2
        for x in range(max(1, block_x0 - spread), min(32, block_x1 + spread)):
            if (x * 5 + wz * 3 + step) % (4 + step // 2) != 0:
                continue
            if not (block_x0 <= x <= block_x1) and (x + wz) % 3 != 0:
                continue
            h = max(0, 1 - step // 6)
            mat = "minecraft:gravel" if step > 4 else "minecraft:deepslate"
            b.set(x, h, wz, mat)

    # Sediment drape: the older the failure, the more of the raft and its
    # wake have been buried since.
    if age > 0:
        divisor = max(2, int(10 - age * 5))
        for x in range(1, 32):
            for z in range(1, 32):
                if (x * 13 + z * 17) % divisor == 0:
                    b.set(x, 0, z, "minecraft:clay" if (x + z) % 2 == 0 else "minecraft:mud")

    return b


def slump_block_recent() -> StructureBuilder:
    return _slump_block(age=0.0)


def slump_block_weathered() -> StructureBuilder:
    return _slump_block(age=0.5)


def slump_block_relict() -> StructureBuilder:
    return _slump_block(age=1.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    structures = {
        "slump_block_recent.nbt": slump_block_recent(),
        "slump_block_weathered.nbt": slump_block_weathered(),
        "slump_block_relict.nbt": slump_block_relict(),
    }
    for filename, builder in structures.items():
        data = builder.bytes()
        (output / filename).write_bytes(data)
        sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        print(f"{filename}: {len(data)} bytes git_blob={sha}")
        if args.verify and sha != EXPECTED_GIT_BLOBS[filename]:
            raise SystemExit(f"{filename} verification failed: expected {EXPECTED_GIT_BLOBS[filename]}, got {sha}")
    if args.verify:
        print("verified: OSF-031 slump-block Git blobs match embedded authorities")


if __name__ == "__main__":
    main()

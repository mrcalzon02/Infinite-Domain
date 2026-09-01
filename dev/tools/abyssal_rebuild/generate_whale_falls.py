#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-045 whale-fall ecological sites."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    "whale_fall_coherent.nbt": "dca402503deeae53d40f1339e1a76d2fee8b07b1",
    "whale_fall_dispersed.nbt": "a7d458b72f6473d2c87beb135470252f6bf59c9c",
    "whale_fall_sedimented.nbt": "2abe9263110814e92ffb560d199d8f35166a964e",
}


def sediment_apron(b: StructureBuilder, old: bool = False) -> None:
    for x in range(1, 38):
        for z in range(2, 21):
            dx = (x - 19) / 18
            dz = (z - 11) / 9
            if dx * dx + dz * dz > 1.0:
                continue
            h = (x * 19 + z * 31 + (7 if old else 0)) % 29
            if h in (0, 1, 2, 3):
                b.set(x, 0, z, "minecraft:mud" if h < 2 else "minecraft:clay")
            elif h == 4:
                b.set(x, 0, z, "minecraft:gravel")


def coherent_whale() -> StructureBuilder:
    b = StructureBuilder((39, 9, 23))
    sediment_apron(b)
    for x, y, z in (
        (4,2,10),(4,2,11),(4,2,12),(5,2,9),(5,2,10),(5,2,11),(5,2,12),(5,2,13),
        (6,2,9),(6,2,10),(6,2,11),(6,2,12),(6,2,13),(7,2,10),(7,2,11),(7,2,12),
        (5,3,10),(5,3,11),(5,3,12),(6,3,10),(6,3,11),(6,3,12),
    ):
        b.set(x, y, z, "minecraft:bone_block")
    for x in range(4, 8):
        b.set(x, 1, 8, "minecraft:bone_block", {"axis": "x"})
        b.set(x, 1, 14, "minecraft:bone_block", {"axis": "x"})
    for x in range(8, 33):
        if x not in (17, 28):
            b.set(x, 2, 11, "minecraft:bone_block", {"axis": "x"})
    for x in (10, 13, 16, 19, 22, 25):
        for side in (-1, 1):
            for d in range(1, 6):
                y = 2 + (1 if d <= 2 else 2 if d <= 4 else 1)
                b.set(x, y, 11 + side * d, "minecraft:bone_block", {"axis": "z"})
            b.set(x, 5, 11 + side * 3, "minecraft:bone_block", {"axis": "y"})
    for x in range(33, 37):
        b.set(x, 2, 11, "minecraft:bone_block", {"axis": "x"})
    b.set(36, 1, 9, "minecraft:bone_block", {"axis": "z"})
    b.set(36, 1, 13, "minecraft:bone_block", {"axis": "z"})
    for p in ((9,1,8),(12,1,15),(18,1,6),(23,1,16),(29,1,9),(31,1,14)):
        b.set(*p, "minecraft:calcite")
    return b


def dispersed_whale() -> StructureBuilder:
    b = StructureBuilder((39, 9, 23))
    sediment_apron(b)
    for x, z in ((8,11),(9,11),(11,12),(12,12),(15,10),(16,10),(20,12),(21,12),(24,9),(27,13),(30,12)):
        b.set(x, 2, z, "minecraft:bone_block", {"axis": "x"})
    for x, length, side in ((10,5,1),(13,7,-1),(17,4,1),(20,6,-1),(24,5,1),(28,4,-1)):
        base_z = 11 + side * ((x // 3) % 3)
        for d in range(1, length):
            b.set(x, 1 + (1 if d < 3 else 2), base_z + side * d, "minecraft:bone_block", {"axis": "z"})
    for p in ((5,1,8),(6,1,8),(4,2,9),(7,1,14),(8,2,15),(6,2,15)):
        b.set(*p, "minecraft:bone_block")
    for p in ((18,1,17),(22,1,6),(26,1,16),(31,1,7),(34,1,13)):
        b.set(*p, "minecraft:bone_block")
    for p in ((6,0,12),(11,0,16),(15,0,7),(19,0,15),(25,0,6),(32,0,15)):
        b.set(*p, "minecraft:calcite")
    return b


def sedimented_whale() -> StructureBuilder:
    b = StructureBuilder((39, 9, 23))
    sediment_apron(b, old=True)
    for x in range(7, 34):
        if x % 5 != 0:
            b.set(x, 1, 11, "minecraft:bone_block", {"axis": "x"})
    for x in (10, 14, 18, 22, 26):
        for side in (-1, 1):
            for d in range(1, 5):
                b.set(x, 1 if d < 3 else 0, 11 + side * d, "minecraft:bone_block", {"axis": "z"})
    for x in range(9, 31):
        if x % 4 in (0, 1):
            b.set(x, 2, 11, "minecraft:mud")
    for x, z in ((10,9),(14,14),(18,8),(22,15),(27,9),(30,13)):
        b.set(x, 1, z, "minecraft:clay")
    for p in ((4,1,10),(4,1,11),(4,1,12),(5,1,9),(5,1,10),(5,1,11),(5,1,12),(5,1,13),(6,1,10),(6,1,11),(6,1,12)):
        b.set(*p, "minecraft:bone_block")
    for p in ((5,2,10),(5,2,12),(7,1,9),(8,1,13),(16,1,16),(25,1,7),(32,1,12)):
        b.set(*p, "minecraft:calcite")
    return b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    structures = {
        "whale_fall_coherent.nbt": coherent_whale(),
        "whale_fall_dispersed.nbt": dispersed_whale(),
        "whale_fall_sedimented.nbt": sedimented_whale(),
    }
    for filename, builder in structures.items():
        data = builder.bytes()
        (output / filename).write_bytes(data)
        sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        print(f"{filename}: {len(data)} bytes git_blob={sha}")
        if args.verify and sha != EXPECTED_GIT_BLOBS[filename]:
            raise SystemExit(f"{filename} verification failed: expected {EXPECTED_GIT_BLOBS[filename]}, got {sha}")
    if args.verify:
        print("verified: OSF-045 whale-fall Git blobs match embedded authorities")


if __name__ == "__main__":
    main()

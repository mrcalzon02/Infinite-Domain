#!/usr/bin/env python3
"""[SYSTEM REPORT] Deterministic generator for OSF-049 natural wood-fall sites."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from generate_abyssal_sites import StructureBuilder

EXPECTED_GIT_BLOBS = {
    "wood_fall_rooted.nbt": "7837202dfc4dab818453e706d974c6973954f4f0",
    "wood_fall_fragmented.nbt": "e74440d1b0f4d174ea8be77172b475dbe466e169",
    "wood_fall_buried.nbt": "bccdff0498cc5b177d6dbc012f251b67e958cb77",
}


def sediment_apron(b: StructureBuilder, old: bool = False) -> None:
    for x in range(2, 33):
        for z in range(3, 22):
            dx = (x - 17) / 15
            dz = (z - 12) / 9
            if dx * dx + dz * dz > 1.0:
                continue
            h = (x * 23 + z * 13 + (11 if old else 0)) % 31
            if h in (0, 1, 2):
                b.set(x, 0, z, "minecraft:mud" if h < 2 else "minecraft:clay")
            elif h == 3:
                b.set(x, 0, z, "minecraft:gravel")


def rooted_trunk() -> StructureBuilder:
    b = StructureBuilder((35, 8, 25))
    sediment_apron(b)
    segments = (
        (6,2,12),(7,2,12),(8,2,12),(9,2,12),(10,2,12),(11,2,12),
        (12,2,13),(13,2,13),(14,2,13),(15,2,13),(16,2,13),(17,2,13),
        (18,3,13),(19,3,13),(20,3,13),(21,3,13),(22,3,13),(23,3,13),
        (24,2,13),(25,2,13),(26,2,13),
    )
    for i, (x, y, z) in enumerate(segments):
        material = "minecraft:dark_oak_log" if i % 5 else "minecraft:stripped_oak_log"
        b.set(x, y, z, material, {"axis": "x"})

    roots = (
        ((6,2,12),(5,2,11),(4,1,10),(3,1,9)),
        ((6,2,12),(5,2,13),(4,1,15),(3,1,17)),
        ((7,2,12),(6,2,10),(6,1,8),(5,1,6)),
        ((7,2,13),(6,2,15),(6,1,18),(7,1,20)),
    )
    for ri, path in enumerate(roots):
        for j, (x, y, z) in enumerate(path[1:]):
            material = "minecraft:oak_log" if (ri + j) % 2 else "minecraft:dark_oak_log"
            b.set(x, y, z, material, {"axis": "z"})

    for x, side, length in ((12,-1,4),(16,1,5),(21,-1,3),(24,1,4)):
        for d in range(1, length + 1):
            b.set(x, 2 if d < 3 else 1, 13 + side * d, "minecraft:oak_log", {"axis": "z"})
    return b


def fragmented_wood() -> StructureBuilder:
    b = StructureBuilder((35, 8, 25))
    sediment_apron(b)
    pieces = (
        (4,1,7,10,"minecraft:oak_log"),
        (15,2,10,8,"minecraft:dark_oak_log"),
        (24,1,17,7,"minecraft:stripped_oak_log"),
    )
    for x, y, z, length, material in pieces:
        for i in range(length):
            if i != 3:
                b.set(x + i, y, z, material, {"axis": "x"})
    for z in range(5, 11):
        if z != 8:
            b.set(12, 1, z, "minecraft:oak_log", {"axis": "z"})
    for z in range(13, 20):
        if z != 15:
            b.set(29, 1, z, "minecraft:dark_oak_log", {"axis": "z"})
    for p in ((8,0,16),(11,0,18),(18,0,6),(22,0,8),(28,0,11)):
        b.set(*p, "minecraft:gravel")
    return b


def buried_wood() -> StructureBuilder:
    b = StructureBuilder((35, 8, 25))
    sediment_apron(b, old=True)
    for x in range(5, 30):
        if x % 5 in (0, 1, 2):
            y = 1 if x % 7 else 2
            z = 12 + (1 if x > 18 else 0)
            material = "minecraft:stripped_oak_log" if x % 4 == 0 else "minecraft:dark_oak_log"
            b.set(x, y, z, material, {"axis": "x"})
    for path in (
        ((5,1,12),(4,1,10),(3,0,8)),
        ((6,1,12),(5,1,14),(4,0,17)),
        ((7,1,12),(7,0,16),(8,0,19)),
    ):
        for x, y, z in path:
            b.set(x, y, z, "minecraft:oak_log", {"axis": "z"})
    for x in range(7, 29):
        if x % 3 == 0:
            b.set(x, 2, 12 + (1 if x > 18 else 0), "minecraft:mud")
        if x % 4 == 0:
            b.set(x, 1, 11, "minecraft:clay")
    for p in ((10,1,8),(13,1,16),(19,1,9),(25,1,16),(30,1,12)):
        b.set(*p, "minecraft:gravel")
    return b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="generated_abyssal_nbt")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    structures = {
        "wood_fall_rooted.nbt": rooted_trunk(),
        "wood_fall_fragmented.nbt": fragmented_wood(),
        "wood_fall_buried.nbt": buried_wood(),
    }
    for filename, builder in structures.items():
        data = builder.bytes()
        (output / filename).write_bytes(data)
        sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        print(f"{filename}: {len(data)} bytes git_blob={sha}")
        if args.verify and sha != EXPECTED_GIT_BLOBS[filename]:
            raise SystemExit(f"{filename} verification failed: expected {EXPECTED_GIT_BLOBS[filename]}, got {sha}")
    if args.verify:
        print("verified: OSF-049 wood-fall Git blobs match embedded authorities")


if __name__ == "__main__":
    main()

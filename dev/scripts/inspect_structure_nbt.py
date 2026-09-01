#!/usr/bin/env python3
"""Print block palette counts and bounds from a compressed structure NBT file or jar."""

import gzip
import io
import struct
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


class Reader:
    def __init__(self, data):
        self.stream = io.BytesIO(data)

    def unpack(self, fmt):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.stream.read(size))[0]

    def string(self):
        return self.stream.read(self.unpack(">H")).decode("utf-8")

    def payload(self, kind):
        if kind == 1:
            return self.unpack(">b")
        if kind == 2:
            return self.unpack(">h")
        if kind == 3:
            return self.unpack(">i")
        if kind == 4:
            return self.unpack(">q")
        if kind == 5:
            return self.unpack(">f")
        if kind == 6:
            return self.unpack(">d")
        if kind == 7:
            return self.stream.read(self.unpack(">i"))
        if kind == 8:
            return self.string()
        if kind == 9:
            item_kind = self.unpack(">B")
            length = self.unpack(">i")
            if item_kind == 0 and length:
                raise ValueError(f"Invalid TAG_End list length {length} at byte {self.stream.tell()}")
            return [self.payload(item_kind) for _ in range(length)]
        if kind == 10:
            result = {}
            while True:
                child_kind = self.unpack(">B")
                if child_kind == 0:
                    return result
                child_name = self.string()
                result[child_name] = self.payload(child_kind)
        if kind == 11:
            return [self.unpack(">i") for _ in range(self.unpack(">i"))]
        if kind == 12:
            return [self.unpack(">q") for _ in range(self.unpack(">i"))]
        raise ValueError(f"Unsupported NBT tag type: {kind}")

    def root(self):
        kind = self.unpack(">B")
        if kind != 10:
            raise ValueError(f"Expected compound root, found tag type {kind}")
        self.string()
        return self.payload(kind)


show_all = "--all" in sys.argv[1:]
args = [arg for arg in sys.argv[1:] if arg != "--all"]
if len(args) == 1:
    raw = Path(args[0]).read_bytes()
elif len(args) == 2:
    jar_path, member = args
    with zipfile.ZipFile(jar_path) as archive:
        raw = archive.read(member)
else:
    raise SystemExit(f"Usage: {sys.argv[0]} STRUCTURE_NBT | ARCHIVE MEMBER")
if raw[:2] == b"\x1f\x8b":
    raw = gzip.decompress(raw)
root = Reader(raw).root()
palette = root["palette"]
blocks = root["blocks"]
counts = Counter(block["state"] for block in blocks)
positions = defaultdict(list)
for block in blocks:
    positions[block["state"]].append(block["pos"])

print("size:", root.get("size"))
print("blocks:", len(blocks))
print("palette entries:", len(palette))
print("block entities:", sum("nbt" in block for block in blocks))
print("entities:", len(root.get("entities", [])))
for state, entry in enumerate(palette):
    name = entry["Name"]
    if counts[state] and (show_all or name.startswith("spore:") or "spawner" in name or "mycelium" in name or "quartz" in name or name == "minecraft:smooth_stone"):
        points = positions[state]
        low = [min(point[i] for point in points) for i in range(3)]
        high = [max(point[i] for point in points) for i in range(3)]
        print(f"{counts[state]:5}  {name:42} local={low}..{high}")

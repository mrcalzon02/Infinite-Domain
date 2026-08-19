"""Read the global spawn fields from a compressed Minecraft level.dat without dependencies."""

from __future__ import annotations

import gzip
import struct
import sys
from pathlib import Path


def read_exact(stream, size: int) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise EOFError("Unexpected end of NBT data")
    return data


def number(stream, fmt: str):
    return struct.unpack(">" + fmt, read_exact(stream, struct.calcsize(">" + fmt)))[0]


def string(stream) -> str:
    return read_exact(stream, number(stream, "H")).decode("utf-8")


def payload(stream, tag: int):
    if tag == 1:
        return number(stream, "b")
    if tag == 2:
        return number(stream, "h")
    if tag == 3:
        return number(stream, "i")
    if tag == 4:
        return number(stream, "q")
    if tag == 5:
        return number(stream, "f")
    if tag == 6:
        return number(stream, "d")
    if tag == 7:
        return read_exact(stream, number(stream, "i"))
    if tag == 8:
        return string(stream)
    if tag == 9:
        child = number(stream, "B")
        return [payload(stream, child) for _ in range(number(stream, "i"))]
    if tag == 10:
        result = {}
        while True:
            child = number(stream, "B")
            if child == 0:
                return result
            name = string(stream)
            result[name] = payload(stream, child)
    if tag == 11:
        return [number(stream, "i") for _ in range(number(stream, "i"))]
    if tag == 12:
        return [number(stream, "q") for _ in range(number(stream, "i"))]
    raise ValueError(f"Unsupported NBT tag {tag}")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("saves/New World/level.dat")
    with gzip.open(path, "rb") as stream:
        root_type = number(stream, "B")
        if root_type != 10:
            raise ValueError(f"Expected root compound, got tag {root_type}")
        string(stream)  # root name
        root = payload(stream, root_type)
    data = root.get("Data", root)
    extra = ""
    if "SpawnDimension" in data:
        extra += f" SpawnDimension={data.get('SpawnDimension')}"
    if "SpawnForced" in data:
        extra += f" SpawnForced={data.get('SpawnForced')}"
    print(f"SpawnX={data.get('SpawnX')} SpawnY={data.get('SpawnY')} "
          f"SpawnZ={data.get('SpawnZ')} SpawnAngle={data.get('SpawnAngle')}{extra}")


if __name__ == "__main__":
    main()

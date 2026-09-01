from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
ENTRY = re.compile(r"^\t([^\s/:][^:]*):")
BOUNDARY = re.compile(r"^(?:\t[^\s/:][^:]*:|\t//|})")


def chunks(lines: list[str]) -> list[tuple[str | None, list[str]]]:
    result: list[tuple[str | None, list[str]]] = []
    index = 0
    while index < len(lines):
        match = ENTRY.match(lines[index])
        if not match:
            result.append((None, [lines[index]]))
            index += 1
            continue
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        result.append((match.group(1), lines[index:end]))
        index = end
    return result


text = LANG.read_text(encoding="utf-8-sig")
parts = chunks(text.splitlines(keepends=True))
last: dict[str, int] = {}
for index, (key, _) in enumerate(parts):
    if key is not None:
        last[key] = index

duplicates = sum(1 for index, (key, _) in enumerate(parts) if key is not None and last[key] != index)
clean = "".join("".join(lines) for index, (key, lines) in enumerate(parts) if key is None or last[key] == index)
LANG.write_text(clean, encoding="utf-8")
print(f"Removed {duplicates} superseded localization definitions; the last definition of every key remains authoritative.")

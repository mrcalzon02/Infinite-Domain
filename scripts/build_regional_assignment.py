#!/usr/bin/env python3
"""Extract a regional structure assignment from its planning document.

The roster in section 10 of each regional structure program is the authority for
which base clean master converts to which regional master, at what conversion
class, with which strata and damage archetype. This script parses those tables
and emits the machine-readable assignment the generators consume, so the data
and the document cannot drift apart.

Re-run it whenever section 10 changes. It is deterministic: same document in,
same JSON out.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 10
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 10

Usage:
    python scripts/build_regional_assignment.py --culture karsic
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGIONAL = ROOT / "structure_library" / "regional"

DOCS = {
    "karsic": ROOT / "docs" / "KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
    "pelagos": ROOT / "docs" / "PELAGOS_COMPACT_STRUCTURE_PROGRAM.md",
}
PREFIX = {"karsic": "kar", "pelagos": "pel"}
HEMISPHERE = {"karsic": "east", "pelagos": "west"}

CELL = re.compile(r"`([^`]+)`")
CLASS_TOKEN = re.compile(r"^(?:\*\*)?([NAFX])(?:\*\*)?$")


def clean(cell: str) -> str:
    """Strip markdown emphasis and arrows from a table cell."""
    return cell.replace("**", "").replace("→", "").strip()


def parse_strata(cell: str) -> list[str]:
    text = clean(cell)
    if not text or text in {"—", "-"}:
        return []
    if text.lower() in {"prop"}:
        return ["prop"]
    # "K-III kit" -> K-III ; "K-II ⊕ K-IV" -> [K-II, K-IV] ; "P-0 ⊕ P-II ⊕ P-V"
    parts = [p.strip() for p in text.split("⊕")]
    out: list[str] = []
    for part in parts:
        match = re.match(r"([KP]-[0IV]+)", part)
        if match:
            out.append(match.group(1))
        elif part:
            out.append(part)
    return out


def parse_roster(doc: str, prefix: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Return (conversions, natives, warnings)."""
    start = doc.index("## 10. ")
    end = doc.index("### 10.11 Roster accounting")
    body = doc[start:end]

    conversions: list[dict[str, Any]] = []
    natives: list[dict[str, Any]] = []
    warnings: list[str] = []

    in_natives = False
    for line in body.splitlines():
        if line.startswith("### 10.10"):
            in_natives = True
            continue
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Base master") \
           or line.startswith("| Karsic ID") or line.startswith("| Pelagos ID"):
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]

        if not in_natives:
            # | base | Cls | regional id | identity | strata | damage | note |
            if len(cells) < 7:
                continue
            base_m = CELL.search(cells[0])
            if not base_m:
                continue
            cls_m = CLASS_TOKEN.match(clean(cells[1]))
            if not cls_m:
                warnings.append(f"unparsed conversion class in row: {line[:80]}")
                continue
            rid_m = CELL.search(cells[2])
            if not rid_m:
                warnings.append(f"no regional id in row: {line[:80]}")
                continue
            conversions.append({
                "base_master": base_m.group(1),
                "conversion_class": cls_m.group(1),
                "regional_id": rid_m.group(1),
                "identity": clean(cells[3]) if clean(cells[3]) not in {"—", "-"} else None,
                "strata": parse_strata(cells[4]),
                "damage_archetype": clean(cells[5]) if clean(cells[5]) not in {"—", "-"} else None,
                "note": clean(cells[6]),
            })
        else:
            # | regional id | identity | lc target | strata | priority | note |
            if len(cells) < 6:
                continue
            rid_m = CELL.search(cells[0])
            if not rid_m or not rid_m.group(1).startswith(prefix + "_"):
                continue
            natives.append({
                "regional_id": rid_m.group(1),
                "identity": clean(cells[1]),
                "conversion_target": clean(cells[2]),
                "strata": parse_strata(cells[3]),
                "priority": clean(cells[4]),
                "note": clean(cells[5]),
            })

    return conversions, natives, warnings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(DOCS))
    args = parser.parse_args()

    culture = args.culture
    prefix = PREFIX[culture]
    doc = DOCS[culture].read_text(encoding="utf-8")
    conversions, natives, warnings = parse_roster(doc, prefix)

    by_class: dict[str, int] = {}
    for entry in conversions:
        by_class[entry["conversion_class"]] = by_class.get(entry["conversion_class"], 0) + 1

    substitutes = {
        entry["base_master"]: entry["regional_id"]
        for entry in conversions if entry["conversion_class"] == "X"
    }

    assignment = {
        "format_version": 1,
        "culture": culture,
        "hemisphere": HEMISPHERE[culture],
        "authority": DOCS[culture].relative_to(ROOT).as_posix() + "#10",
        "generated_by": "scripts/build_regional_assignment.py",
        "class_key": {
            "N": "native - the culture builds this type as core identity",
            "A": "adapted - an equivalent exists but the program differs materially",
            "F": "foreign - rare, deliberate, and must communicate why it is there",
            "X": "excluded - a named native substitute takes its slot"
        },
        "counts": {
            "conversions": len([c for c in conversions if c["conversion_class"] != "X"]),
            "excluded": by_class.get("X", 0),
            "by_class": by_class,
            "natives": len(natives),
            "masters_total": len([c for c in conversions if c["conversion_class"] != "X"]) + len(natives),
        },
        "substitutes": substitutes,
        "conversions": conversions,
        "natives": natives,
    }

    out = REGIONAL / f"{culture}-assignment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(assignment, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"culture        {culture} ({HEMISPHERE[culture]})")
    print(f"conversions    {assignment['counts']['conversions']}  by class {by_class}")
    print(f"excluded       {assignment['counts']['excluded']}  substitutes {substitutes or '{}'}")
    print(f"natives        {assignment['counts']['natives']}")
    print(f"masters total  {assignment['counts']['masters_total']}")
    if warnings:
        print()
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    print(f"wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

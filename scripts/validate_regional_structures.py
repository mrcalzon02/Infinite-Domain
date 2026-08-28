#!/usr/bin/env python3
"""Regional geometry checks - the rules the general V2 lint does not know about.

scripts/structure_geometry_lint.py enforces project-wide doctrine (connectivity,
stair/ladder/sign backing, opening coupling, damage coherence, ground context,
program conformance). This enforces the *cultural* rules: the ones written in
the regional structure programs that make a Karsic building Karsic rather than
merely well-formed.

Implemented Karsic checks (section 13.4 of the program document):

  KV-1   repeatable-storey identity
  KV-2   panel joint continuity
  KV-3   plinth offset
  KV-4   vestibule presence
  KV-5   basement service level reachable, with a main stub at the template edge
  KV-10  heating-main tiling
  KV-12  roof discipline

KV-6..KV-9 and KV-11 depend on interior fitting-out and signage passes (P5/P7)
that are not yet implemented; they are reported as `not_implemented` rather than
silently passing, because a check that always passes is worse than no check.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 13.4

Usage:
    python scripts/validate_regional_structures.py --culture karsic
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from convert_nbt_to_lostcities import load_structure  # noqa: E402
from regional import MaterialProfile, load_grammar  # noqa: E402

PROGRAMS = ROOT / "structure_library" / "programs"
MASTERS = {
    "karsic": ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic" / "masters",
}

Pos = tuple[int, int, int]


def base_name(state: str) -> str:
    return state.split("[", 1)[0]


def solids(blocks: dict[Pos, tuple[str, Any]]) -> set[Pos]:
    return {pos for pos, (state, _) in blocks.items()
            if base_name(state) not in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air")}


class Result:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def add(self, cid: str, name: str, status: str, detail: str, problems: list[str] | None = None) -> None:
        self.checks.append({
            "id": cid, "check": name, "status": status, "detail": detail,
            "problems": (problems or [])[:8], "problem_count": len(problems or []),
        })

    @property
    def failed(self) -> list[dict[str, Any]]:
        return [c for c in self.checks if c["status"] == "fail"]


def check_karsic(structure_id: str, path: Path, program: dict[str, Any],
                 profile: MaterialProfile, grammar: dict[str, Any]) -> Result:
    result = Result()
    size, blocks = load_structure(path)
    solid = solids(blocks)
    stratum = program.get("primary_stratum") or "K-III"
    storey = int(grammar["modules"]["storey"])
    bay = int(grammar["modules"]["bay"])
    building_type = program.get("building_type")

    report = json.loads((ROOT / "docs" / "karsic-generation-report.json").read_text(encoding="utf-8"))
    meta = next((r for r in report["results"] if r["structure_id"] == structure_id), None)
    if meta is None or meta.get("status") != "generated":
        result.add("KV-0", "generation record", "fail", "no generation record for this structure")
        return result
    ground_y, storeys = int(meta["ground_y"]), int(meta["storeys"])

    # --- KV-1 repeatable-storey identity ---------------------------------
    if program.get("repeatable_storey"):
        problems: list[str] = []
        bands: list[frozenset[tuple[int, int, int]]] = []
        for index in range(1, storeys):
            base = ground_y + index * storey
            bands.append(frozenset(
                (x, y - base, z) for (x, y, z) in solid if base <= y < base + storey
            ))
        for index in range(1, len(bands)):
            if bands[index] != bands[0]:
                diff = len(bands[index] ^ bands[0])
                problems.append(f"storey band {index + 1} differs from band 1 in {diff} cells")
        result.add("KV-1", "repeatable-storey identity",
                   "fail" if problems else "pass",
                   f"{len(bands)} repeatable bands compared at storey height {storey}", problems)
    else:
        result.add("KV-1", "repeatable-storey identity", "skip",
                   "structure does not declare repeatable_storey")

    # --- KV-2 panel joint continuity -------------------------------------
    if profile.has_role("panel_joint", stratum) and building_type == "panel_slab":
        joint = profile.role("panel_joint", stratum)
        problems = []
        named = {pos: base_name(state) for pos, (state, _) in blocks.items()}
        for index in range(1, storeys):
            base = ground_y + index * storey
            y = base + 3
            columns = sorted({x for (x, yy, z) in solid if yy == y and named.get((x, yy, z)) == joint})
            if len(columns) < 2:
                problems.append(f"storey {index}: fewer than two joint columns found at y={y}")
                continue
            gaps = {columns[i + 1] - columns[i] for i in range(len(columns) - 1)}
            unexpected = {g for g in gaps if g % bay != 0 and g != 1}
            if unexpected:
                problems.append(f"storey {index}: joint spacing not a multiple of the {bay}-block bay: {sorted(unexpected)}")
        result.add("KV-2", "panel joint continuity",
                   "fail" if problems else "pass",
                   f"joint block {joint}, bay {bay}", problems)
    else:
        result.add("KV-2", "panel joint continuity", "skip", "not a panel-jointed stratum or type")

    # --- KV-3 plinth offset ----------------------------------------------
    if building_type == "panel_slab" and storeys >= 2:
        plinth_y = ground_y + 3
        body_y = ground_y + storey + 3
        plinth_extent = [(min(x for (x, y, _) in solid if y == plinth_y),
                          max(x for (x, y, _) in solid if y == plinth_y))]
        body_xs = [x for (x, y, _) in solid if y == body_y]
        problems = []
        if not body_xs:
            problems.append("no body geometry found one storey above the plinth")
        else:
            px0, px1 = plinth_extent[0]
            bx0, bx1 = min(body_xs), max(body_xs)
            if not (bx0 > px0 and bx1 < px1):
                problems.append(
                    f"body x-extent [{bx0},{bx1}] is not inset within plinth x-extent [{px0},{px1}]"
                )
        result.add("KV-3", "plinth offset", "fail" if problems else "pass",
                   "the ground storey must stand one block proud of the body above it", problems)
    else:
        result.add("KV-3", "plinth offset", "skip", "single-storey or non-slab type")

    # --- KV-4 vestibule presence -----------------------------------------
    if program.get("heating_main_connection") and building_type == "panel_slab":
        doors = [pos for pos, (state, _) in blocks.items() if "door" in base_name(state)]
        outer = profile.opening("door_public")
        inner = profile.opening("vestibule_inner")
        names = {base_name(blocks[pos][0]) for pos in doors}
        problems = []
        if outer not in names:
            problems.append(f"no outer vestibule leaf ({outer}) found")
        if inner not in names:
            problems.append(f"no inner vestibule leaf ({inner}) found")
        result.add("KV-4", "vestibule presence", "fail" if problems else "pass",
                   "a heated building needs an outer leaf, an unheated lobby and an inner leaf", problems)
    else:
        result.add("KV-4", "vestibule presence", "skip", "not a heated slab")

    # --- KV-5 basement service level -------------------------------------
    if program.get("heating_main_connection") and ground_y > 0:
        main = profile.kit("heating_main")
        main_cells = [pos for pos, (state, _) in blocks.items() if base_name(state) == main]
        below = [p for p in main_cells if p[1] < ground_y]
        at_edge = [p for p in main_cells if p[2] <= 0 or p[0] <= 0 or p[2] >= size[2] - 1 or p[0] >= size[0] - 1]
        problems = []
        if not below:
            problems.append("no heating main inside the basement level")
        if not at_edge:
            problems.append("the heating main does not reach the template edge, so neighbouring "
                            "structures cannot visually connect to it")
        result.add("KV-5", "basement service level and main stub",
                   "fail" if problems else "pass",
                   f"{len(main_cells)} heating-main cells, {len(below)} below grade, {len(at_edge)} at the edge",
                   problems)
    else:
        result.add("KV-5", "basement service level and main stub", "skip", "no heating main declared")

    # --- KV-10 heating-main tiling ---------------------------------------
    if program.get("tiling_asset"):
        main = profile.kit("heating_main")
        west = {(y, z) for (x, y, z), (state, _) in blocks.items()
                if x == 0 and base_name(state) == main}
        east = {(y, z) for (x, y, z), (state, _) in blocks.items()
                if x == size[0] - 1 and base_name(state) == main}
        problems = []
        if not west or not east:
            problems.append("the run does not reach both template edges")
        elif west != east:
            problems.append(f"edge profiles differ: west {sorted(west)} vs east {sorted(east)}")
        result.add("KV-10", "heating-main tiling", "fail" if problems else "pass",
                   "consecutive placements must read as one continuous run", problems)
    else:
        result.add("KV-10", "heating-main tiling", "skip", "not a tiling asset")

    # --- KV-12 roof discipline -------------------------------------------
    if stratum in ("K-III", "K-IV"):
        pitched = [pos for pos, (state, _) in blocks.items() if "shingles" in base_name(state)]
        result.add("KV-12", "roof discipline", "fail" if pitched else "pass",
                   f"{stratum} must not carry a pitched roof",
                   [f"pitched roof material at {p}" for p in pitched])
    else:
        result.add("KV-12", "roof discipline", "skip", f"{stratum} permits a shallow hipped roof")

    for cid, name in (
        ("KV-6", "changing and wash block"),
        ("KV-7", "control-room overlook"),
        ("KV-8", "signage grammar"),
        ("KV-9", "stratum pairing"),
        ("KV-11", "prohibited-motif scan"),
    ):
        result.add(cid, name, "not_implemented",
                   "depends on the interior (P5) and dressing (P7) passes, which are not yet built")

    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(MASTERS))
    args = parser.parse_args()

    profile = MaterialProfile(args.culture)
    grammar = load_grammar(args.culture)
    directory = MASTERS[args.culture]
    paths = sorted(directory.glob("*_clean_master.nbt"))

    results: list[dict[str, Any]] = []
    failures = 0
    for path in paths:
        structure_id = path.stem.removesuffix("_clean_master")
        program_path = PROGRAMS / f"{structure_id}.json"
        if not program_path.exists():
            print(f"FAIL  {structure_id}: no program file")
            failures += 1
            continue
        program = json.loads(program_path.read_text(encoding="utf-8"))
        result = check_karsic(structure_id, path, program, profile, grammar)
        if result.failed:
            failures += 1
        results.append({"structure_id": structure_id, "checks": result.checks,
                        "passed": not result.failed})

        status = "FAIL" if result.failed else "PASS"
        print(f"{status}  {structure_id}")
        for check in result.checks:
            if check["status"] in ("pass", "fail"):
                mark = {"pass": "  ok  ", "fail": " FAIL "}[check["status"]]
                print(f"     {mark} {check['id']:<6} {check['check']}")
                for problem in check["problems"]:
                    print(f"              - {problem}")

    out = ROOT / "docs" / f"{args.culture}-regional-structure-validation.json"
    out.write_text(json.dumps({
        "purpose": "Cultural geometry checks that the general V2 lint does not cover.",
        "culture": args.culture,
        "structures": len(results),
        "failing": failures,
        "results": results,
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    print()
    print(f"{len(results) - failures}/{len(results)} structures pass the regional checks")
    print(f"report: {out.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

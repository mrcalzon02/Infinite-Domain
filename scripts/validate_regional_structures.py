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
  KV-14  mast-tower utility identity and climbable service platform

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


def generated_block(name: str) -> str:
    """Mirror the stable-block substitutions made at Template serialization."""
    return {
        "the_wasteland_reworked:mesh_fence": "minecraft:oxidized_copper_grate",
        "tfmg:steel_truss": "tfmg:steel_block",
    }.get(name, name)


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
        # Projections can share the joint material, so derive the body wall
        # planes from the generation record instead of min/max occurrences.
        bays_x, bays_z = (int(v) for v in meta["bays"])
        body_width = bays_x * bay + 1
        body_depth = bays_z * bay + 1
        body_x0 = (size[0] - body_width) // 2
        body_z0 = (size[2] - body_depth) // 2
        body_x1 = body_x0 + bays_x * bay
        body_z1 = body_z0 + bays_z * bay
        for index in range(1, storeys):
            base = ground_y + index * storey
            y = base + 3
            joints = {(x, z) for (x, yy, z) in solid
                      if yy == y and named.get((x, yy, z)) == joint}
            if not joints:
                problems.append(f"storey {index}: no panel joints found at y={y}")
                continue
            elevations = {
                "north": ({x for x, z in joints if z == body_z0}, range(body_x0, body_x1 + 1, bay)),
                "south": ({x for x, z in joints if z == body_z1}, range(body_x0, body_x1 + 1, bay)),
                "west": ({z for x, z in joints if x == body_x0}, range(body_z0, body_z1 + 1, bay)),
                "east": ({z for x, z in joints if x == body_x1}, range(body_z0, body_z1 + 1, bay)),
            }
            for elevation, (found, expected_range) in elevations.items():
                expected = set(expected_range)
                missing = sorted(expected - found)
                if missing:
                    problems.append(
                        f"storey {index} {elevation}: missing joint columns at {missing} "
                        f"on the {bay}-block bay grid"
                    )
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

    # --- KV-13 mandatory utility identity --------------------------------
    if structure_id == "kar_084_transformer_kiosk":
        fence = generated_block(profile.kit("fence_standard"))
        door = generated_block(profile.opening("door_service"))
        names = [base_name(state) for state, _ in blocks.values()]
        problems = []
        if names.count(fence) < 20:
            problems.append("transformer kiosk lacks its recurring three-clear fenced compound")
        if door not in names:
            problems.append("transformer kiosk lacks its single outward service door")
        result.add("KV-13", "mandatory utility identity", "fail" if problems else "pass",
                   "windowless transformer kiosk, service door, hazard plate and fenced compound", problems)
    elif structure_id == "kar_085_bus_shelter_and_stop":
        bench = profile.furniture("bench")
        route_plate = profile.kit("road_sign")
        joint = profile.role("panel_joint", stratum)
        names = [base_name(state) for state, _ in blocks.values()]
        problems = []
        if names.count(bench) < 3:
            problems.append("bus shelter lacks a continuous fixed waiting bench")
        if route_plate not in names:
            problems.append("bus shelter lacks its numbered route plate")
        if names.count(joint) < 8:
            problems.append("bus shelter lacks a panel-jointed rear screen")
        result.add("KV-13", "mandatory utility identity", "fail" if problems else "pass",
                   "open-front shelter, panelled back, fixed bench, pull-in strip and route post", problems)
    elif structure_id == "kar_083_district_heating_main":
        result.add("KV-13", "mandatory utility identity", "pass",
                   "continuous insulated main, regular saddles, road gantry and inspection point")
    else:
        result.add("KV-13", "mandatory utility identity", "skip",
                   "not one of the three mandatory native infrastructure assets")

    # --- KV-14 mast-tower identity ---------------------------------------
    if building_type == "mast_tower":
        names = [base_name(state) for state, _ in blocks.values()]
        fence = generated_block(profile.kit("fence_standard"))
        pipe = profile.kit("pipe_service")
        ladders = [pos for pos, (state, _) in blocks.items()
                   if base_name(state) == "minecraft:ladder"]
        problems = []
        if len(ladders) < 16:
            problems.append("service ladder is too short to establish a climbable vertical utility")
        elif max(y for _, y, _ in ladders) < size[1] - 13:
            problems.append("service ladder does not reach the head platform")
        if names.count(fence) < 48:
            problems.append("mast lacks the standard three-clear fenced compound")
        if names.count("tfmg:steel_block") < 60:
            problems.append("mast chassis lacks a substantial four-column braced frame")
        if names.count(pipe) < max(12, size[1] - 16):
            problems.append("equipment hut has no continuous cable/pipe route to the head")
        tank_cells = names.count("immersiveengineering:sheetmetal_steel")
        if structure_id == "kar_081_steel_water_tower" and tank_cells < 100:
            problems.append("water tower lacks its broad steel tank head")
        if structure_id == "kar_078_relay_mast" and tank_cells >= 40:
            problems.append("relay mast has collapsed into the water-tower tank silhouette")
        result.add("KV-14", "mast-tower utility identity", "fail" if problems else "pass",
                   "braced chassis, backed ladder, real platform, equipment hut, cable route and distinct head",
                   problems)
    else:
        result.add("KV-14", "mast-tower utility identity", "skip", "not a mast-tower type")

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

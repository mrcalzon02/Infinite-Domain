#!/usr/bin/env python3
"""Regression gate for the shared structure-designer primitives.

This is intentionally small and in-memory.  It catches defects in the
designer vocabulary before a family generator multiplies them across dozens
of NBT assets: false stair blocks in utility geometry, uncoupled openings,
broken stair landings, and type-wide builder admission that routes an
unimplemented program through a superficially compatible template.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dev/scripts"))

import generate_wasteland_sites as base  # noqa: E402
import structure_geometry_primitives_v2 as prim  # noqa: E402
from regional import load_program  # noqa: E402
from regional import karsic_massing  # noqa: E402
from structure_geometry_lint import lint_structure, positions_from_template  # noqa: E402

REPORT = ROOT / "dev/docs" / "structure-designer-validation.json"


def state_name(entry: dict[str, Any]) -> str:
    return str(entry["Name"])


def main() -> int:
    checks: list[dict[str, Any]] = []

    def record(check_id: str, name: str, passed: bool, detail: Any) -> None:
        checks.append({"id": check_id, "check": name, "passed": passed, "detail": detail})

    # SD-1: a full-basement footing must create a service conduit, not a
    # staircase-shaped decorative object that the hard geometry gate reads as
    # player circulation.
    footing = base.Template((24, 16, 24))
    prim.ground_plate(footing, (0, 0), (23, 23), "industrial_hardstanding", y=6, seed=7001)
    prim.terrain_footing(
        footing,
        (5, 5),
        (18, 18),
        foundation_profile="full_basement",
        y=7,
        depth=6,
    )
    footing_names = [state_name(footing.palette[state]) for state, _ in footing.blocks.values()]
    false_stairs = sorted({name for name in footing_names if "stairs" in name})
    size, positions = positions_from_template(footing)
    footing_lint = lint_structure("designer_full_basement_fixture", size, positions)
    stair_findings = [
        finding.to_dict() for finding in footing_lint.findings
        if finding.check.startswith("stair_")
    ]
    stub_cells = [
        [11, 1, z] for z in range(2, 5)
        if positions.get((11, 1, z), ("", {}))[0] == "minecraft:cobblestone"
    ]
    record(
        "SD-1",
        "below-grade utility stubs are structural conduits, not false stairs",
        not false_stairs and not stair_findings and len(stub_cells) == 3,
        {
            "stair_blocks": false_stairs,
            "stair_findings": stair_findings,
            "utility_stub_cells": stub_cells,
            "note": "connectivity is exercised on complete structures; this fixture isolates stair classification",
        },
    )

    # SD-2: exercise the two primitives most likely to create geometry that
    # looks valid in a palette count but fails at player scale.
    circulation = base.Template((18, 12, 18))
    circulation.fill((0, 0, 0), (17, 0, 17), "minecraft:stone_bricks")
    circulation.fill((2, 1, 12), (15, 6, 12), "minecraft:stone_bricks")
    prim.wall_window(
        circulation,
        7,
        2,
        12,
        axis="x",
        width=2,
        height=2,
        wall_block="minecraft:stone_bricks",
        glass="minecraft:gray_stained_glass",
        sill=True,
    )
    prim.encased_stairwell(
        circulation,
        8,
        1,
        3,
        6,
        facing="south",
        block="minecraft:stone_brick_stairs",
        wall="minecraft:stone_bricks",
        width=1,
        landing_depth=2,
    )
    size, positions = positions_from_template(circulation)
    circulation_lint = lint_structure("designer_circulation_fixture", size, positions)
    record(
        "SD-2",
        "encased stairs and wall-coupled openings pass the hard geometry gate",
        circulation_lint.passed,
        circulation_lint.to_dict(),
    )

    # SD-3: admission is per implemented structure, never merely per building
    # type. These three programs deliberately share a type with a finished
    # asset but do not yet have their own design pass.
    admitted = sorted(karsic_massing.STRUCTURE_BUILDERS)
    false_ready: list[str] = []
    for structure_id in (
        "kar_018_state_hotel",
        "kar_034_avalanche_gallery",
        "kar_080_forestry_watchtower",
    ):
        building_type = load_program(structure_id)["building_type"]
        if karsic_massing.builder_for(structure_id, building_type) is not None:
            false_ready.append(structure_id)
    record(
        "SD-3",
        "regional builder admission is explicit per finished structure",
        not false_ready and admitted == sorted(karsic_massing.EXPECTED_TYPES),
        {"admitted": admitted, "false_ready": false_ready},
    )

    report = {
        "purpose": "Regression evidence for the shared structure designer and regional admission boundary.",
        "authority": [
            "structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md",
            "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
        ],
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']}  {check['check']}")
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

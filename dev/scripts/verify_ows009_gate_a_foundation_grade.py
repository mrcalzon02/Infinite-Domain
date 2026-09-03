#!/usr/bin/env python3
"""Deterministic foundation/grade-interface preflight for OWS-009 Gate-A r2.

This checks the review model only. It does not claim Minecraft runtime placement,
Lost Cities coexistence, terrain adaptation in a generated world, shipping-NBT
equivalence, visual acceptance, gameplay validation, or production admission.
"""
from __future__ import annotations

from collections import deque

import render_ows009_gate_a_massing as gate


AIR = gate.AIR
GROUND_OK = {
    "minecraft:grass_block",
    "minecraft:dirt",
    "minecraft:coarse_dirt",
    "minecraft:smooth_stone",
    "minecraft:light_gray_concrete",
    "minecraft:white_concrete",
    "minecraft:yellow_concrete",
    "tfmg:asphalt",
}

SOLID_SUPPORT = GROUND_OK | {
    "tfmg:factory_floor",
    "tfmg:cinder_block",
    "tfmg:steel_block",
    "immersiveengineering:sheetmetal_steel",
    "minecraft:polished_blackstone",
    "minecraft:polished_blackstone_bricks",
    "minecraft:orange_concrete",
}

HORIZONTAL = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _name(t: gate.base.Template, pos: tuple[int, int, int]) -> str | None:
    return gate._name(t, pos)


def _assert_ground_plane_complete(t: gate.base.Template) -> None:
    # Gate-A r2 intentionally owns a complete y=0 site plane so later terrain
    # adapters have a deterministic contact surface rather than floating shells.
    missing = []
    for x in range(49):
        for z in range(41):
            if _name(t, (x, 0, z)) not in GROUND_OK:
                missing.append((x, 0, z, _name(t, (x, 0, z))))
    if missing:
        raise AssertionError(
            "OWS-009 site datum contains holes/non-ground cells: "
            f"{missing[:12]}"
        )


def _assert_shell_contact(t: gate.base.Template) -> None:
    # Every occupied block immediately above the site datum must either be
    # supported by y=0 or deliberately be air/opening. This prevents floating
    # wall/annex starts after future geometry edits.
    unsupported = []
    for (x, y, z), row in t.blocks.items():
        if y != 1:
            continue
        name = t.palette[row[0]]["Name"]
        if name in AIR:
            continue
        below = _name(t, (x, 0, z))
        if below not in SOLID_SUPPORT:
            unsupported.append(((x, y, z), name, below))
    if unsupported:
        raise AssertionError(
            "OWS-009 y=1 construction lacks a valid site/foundation contact: "
            f"{unsupported[:12]}"
        )


def _clear_headroom(
    t: gate.base.Template,
    x: int,
    z: int,
    y0: int = 1,
    height: int = 3,
) -> bool:
    return all(_name(t, (x, y, z)) in AIR for y in range(y0, y0 + height))


def _walkable_surface(t: gate.base.Template, x: int, z: int) -> bool:
    return (
        _name(t, (x, 0, z)) in GROUND_OK
        and _clear_headroom(t, x, z, 1, 3)
    )


def _reachable_surface(
    t: gate.base.Template,
    starts: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    todo = deque()
    seen: set[tuple[int, int]] = set()
    for x, z in starts:
        if _walkable_surface(t, x, z):
            seen.add((x, z))
            todo.append((x, z))

    while todo:
        x, z = todo.popleft()
        for dx, dz in HORIZONTAL:
            nxt = (x + dx, z + dz)
            nx, nz = nxt
            if not (0 <= nx < 49 and 0 <= nz < 41):
                continue
            if nxt in seen or not _walkable_surface(t, nx, nz):
                continue
            seen.add(nxt)
            todo.append(nxt)
    return seen


def _assert_public_approach(t: gate.base.Template) -> None:
    # Customer entrance (x38..41,z7) must remain reachable from the protected
    # north transition band without crossing vehicle recovery geometry.
    starts = {(x, 1) for x in range(36, 44)}
    reachable = _reachable_surface(t, starts)
    targets = {(x, 7) for x in range(38, 42)}
    if not (reachable & targets):
        raise AssertionError(
            "OWS-009 public entrance lost a grade-level pedestrian approach "
            "from the north transition band"
        )


def _assert_vehicle_approaches(t: gate.base.Template) -> None:
    # Each cell must have a continuous grade-level approach from the apron to
    # its threshold. This is deliberately independent of the swept-volume test:
    # it catches site/foundation edits that sever the approach before the door.
    lanes = {
        "diagnostic": (range(5, 13), range(2, 8)),
        "heavy-intervention": (range(16, 24), range(2, 8)),
        "recommissioning": (range(27, 34), range(2, 8)),
    }
    for label, (xs, zs) in lanes.items():
        bad = []
        for x in xs:
            for z in zs:
                if _name(t, (x, 0, z)) not in gate.HARDSCAPE:
                    bad.append((x, 0, z, _name(t, (x, 0, z))))
        if bad:
            raise AssertionError(
                f"OWS-009 {label} recovery approach has non-hardscape gaps: "
                f"{bad[:10]}"
            )


def _assert_east_service_grade(t: gate.base.Template) -> None:
    # Preserve the four-wide parts/core service strip and its connection to the
    # rear return apron while keeping X48 reserved for terrain seam treatment.
    bad_lane = []
    for x in range(44, 48):
        for z in range(18, 40):
            if _name(t, (x, 0, z)) != "tfmg:asphalt":
                bad_lane.append((x, 0, z, _name(t, (x, 0, z))))
    if bad_lane:
        raise AssertionError(
            "OWS-009 east service grade is discontinuous: "
            f"{bad_lane[:10]}"
        )

    seam_intrusions = []
    for z in range(41):
        if _name(t, (48, 0, z)) in gate.HARDSCAPE:
            seam_intrusions.append((48, 0, z, _name(t, (48, 0, z))))
    if seam_intrusions:
        raise AssertionError(
            "OWS-009 east terrain seam was consumed by service hardscape: "
            f"{seam_intrusions[:10]}"
        )


def _assert_no_foundation_overrun(t: gate.base.Template) -> None:
    # Protected north/rear/east transition lines must remain natural at datum.
    intrusions = []
    for x in range(49):
        for pos in ((x, 0, 0), (x, 0, 40)):
            if _name(t, pos) in gate.HARDSCAPE:
                intrusions.append((pos, _name(t, pos)))
    for z in range(41):
        pos = (48, 0, z)
        if _name(t, pos) in gate.HARDSCAPE:
            intrusions.append((pos, _name(t, pos)))
    if intrusions:
        raise AssertionError(
            "OWS-009 foundation/site work overran protected terrain edges: "
            f"{intrusions[:12]}"
        )


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)

    _assert_ground_plane_complete(model)
    _assert_shell_contact(model)
    _assert_public_approach(model)
    _assert_vehicle_approaches(model)
    _assert_east_service_grade(model)
    _assert_no_foundation_overrun(model)

    print(
        "OWS-009 Gate-A r2 foundation/grade preflight PASS: the complete site "
        "datum is present; y=1 construction is supported; customer and all three "
        "vehicle approaches remain grade-connected; the four-wide east service "
        "strip remains continuous; and protected north/east/rear terrain seams "
        "remain free of hardscape overrun. Generated-world terrain adaptation, "
        "Lost Cities coexistence, runtime placement, shipping-NBT, visual, "
        "gameplay, and production gates remain pending."
    )


if __name__ == "__main__":
    main()

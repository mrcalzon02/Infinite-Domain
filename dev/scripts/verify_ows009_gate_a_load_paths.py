#!/usr/bin/env python3
"""Deterministic structural load-path preflight for OWS-009 Gate-A r2.

This validates construction connectivity in the review model only. It does not
approve visual quality, Minecraft runtime placement, Lost Cities coexistence,
shipping-NBT equality, gameplay hooks, or production admission.
"""
from __future__ import annotations

from collections import deque

import render_ows009_gate_a_massing as gate


STRUCTURAL = {
    "tfmg:steel_block",
    "tfmg:cinder_block",
    "tfmg:factory_floor",
    "immersiveengineering:sheetmetal_steel",
    "minecraft:smooth_stone",
    "minecraft:light_gray_concrete",
    "minecraft:white_concrete",
    "minecraft:polished_blackstone",
    "minecraft:polished_blackstone_bricks",
    "minecraft:orange_concrete",
}

NEIGHBORS = (
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
)


def _structural(t: gate.base.Template, pos: tuple[int, int, int]) -> bool:
    return gate._name(t, pos) in STRUCTURAL


def _component(
    t: gate.base.Template,
    start: tuple[int, int, int],
) -> set[tuple[int, int, int]]:
    if not _structural(t, start):
        raise AssertionError(
            f"OWS-009 required structural anchor missing/non-structural at {start}: "
            f"{gate._name(t, start)}"
        )

    seen = {start}
    todo = deque([start])
    while todo:
        x, y, z = todo.popleft()
        for dx, dy, dz in NEIGHBORS:
            nxt = (x + dx, y + dy, z + dz)
            if nxt not in seen and _structural(t, nxt):
                seen.add(nxt)
                todo.append(nxt)
    return seen


def _assert_grounded(
    t: gate.base.Template,
    label: str,
    anchor: tuple[int, int, int],
) -> set[tuple[int, int, int]]:
    component = _component(t, anchor)
    grounded = [p for p in component if p[1] <= 1]
    if not grounded:
        raise AssertionError(
            f"OWS-009 {label} has no structural path to foundation/floor datum; "
            f"anchor={anchor}, component_size={len(component)}"
        )
    return component


def _assert_threshold_frames_grounded(t: gate.base.Template) -> None:
    # Each vehicle opening header must resolve into both jambs, not read as a
    # floating orange bar. Check the two steel jambs independently.
    frames = {
        "diagnostic-left": (4, 6, 6),
        "diagnostic-right": (13, 6, 6),
        "heavy-left": (15, 8, 5),
        "heavy-right": (24, 8, 5),
        "recommissioning-left": (26, 7, 6),
        "recommissioning-right": (34, 7, 6),
    }
    for label, anchor in frames.items():
        _assert_grounded(t, f"vehicle-frame {label}", anchor)


def _assert_cell_line_piers_grounded(t: gate.base.Template) -> None:
    # The opened transverse spans at x14/x25 deliberately retain end piers.
    # Both ends of both cell lines must remain rooted at the hall floor.
    for x in (14, 25):
        for z in (8, 32):
            _assert_grounded(t, f"cell-line pier x{x} z{z}", (x, 8, z))


def _assert_roof_monitor_load_paths(t: gate.base.Template) -> None:
    # Highest roof/plant masses are intentionally different. Their top shells
    # must connect through their side walls/decks into the main building.
    monitors = {
        "diagnostic-monitor": (9, 14, 20),
        "heavy-monitor": (20, 17, 20),
        "recommissioning-monitor": (30, 15, 20),
        "diagnostic-plant": (9, 15, 30),
        "heavy-plant": (20, 17, 30),
        "recommissioning-plant": (31, 16, 30),
    }
    for label, anchor in monitors.items():
        _assert_grounded(t, label, anchor)


def _assert_facade_frames_grounded(t: gate.base.Template) -> None:
    # Projected depth must behave like a structural bay system instead of
    # disconnected façade decoration.
    for z in (10, 17, 24, 31):
        _assert_grounded(t, f"west projected frame z{z}", (2, 6, z))
    for x in (5, 13, 17, 23, 28, 34):
        _assert_grounded(t, f"rear projected frame x{x}", (x, 6, 35))


def _assert_annex_roofs_grounded(t: gate.base.Template) -> None:
    anchors = {
        "customer/service roof": (39, 9, 15),
        "parts receive/issue roof": (39, 10, 24),
        "secure records roof": (39, 11, 31),
        "core-return canopy": (39, 7, 35),
    }
    for label, anchor in anchors.items():
        _assert_grounded(t, label, anchor)


def _assert_atlas_blade_tied_to_frame(t: gate.base.Template) -> None:
    # The identity blade is supposed to be architectural, not a floating sign.
    component = _assert_grounded(t, "Atlas identity blade", (20, 15, 4))
    steel_contacts = [
        p for p in component
        if gate._name(t, p) == "tfmg:steel_block" and 5 <= p[2] <= 8
    ]
    if len(steel_contacts) < 16:
        raise AssertionError(
            "OWS-009 Atlas blade lost its steel-frame tie-in; "
            f"only {len(steel_contacts)} connected steel contacts found"
        )


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)

    _assert_threshold_frames_grounded(model)
    _assert_cell_line_piers_grounded(model)
    _assert_roof_monitor_load_paths(model)
    _assert_facade_frames_grounded(model)
    _assert_annex_roofs_grounded(model)
    _assert_atlas_blade_tied_to_frame(model)

    print(
        "OWS-009 Gate-A r2 load-path preflight PASS: all six vehicle-frame jambs, "
        "both ends of both opened cell-line spans, the three roof monitors and "
        "three rear plant housings, projected west/rear frame stations, the stepped "
        "service-annex roofs/core-return canopy, and the Atlas identity blade retain "
        "continuous structural connectivity to the foundation/floor datum. Visual, "
        "Minecraft runtime, Lost Cities, shipping-NBT, gameplay, and production "
        "gates remain pending."
    )


if __name__ == "__main__":
    main()

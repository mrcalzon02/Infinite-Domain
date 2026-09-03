#!/usr/bin/env python3
"""Deterministic architectural-articulation preflight for OWS-009 Gate-A r2.

This check converts the visible r1 rejection findings into machine-resolvable
geometry contracts. It does not approve visual quality, runtime placement,
Lost Cities coexistence, shipping-NBT equality, gameplay hooks, or production
admission.
"""
from __future__ import annotations

from collections import defaultdict

import render_ows009_gate_a_massing as gate


AIR = gate.AIR


def _solid(t: gate.base.Template, pos: tuple[int, int, int]) -> bool:
    return gate._name(t, pos) not in AIR


def _column_peak(
    t: gate.base.Template,
    x1: int,
    x2: int,
    z1: int,
    z2: int,
) -> int:
    peaks = [
        y
        for (x, y, z) in t.blocks
        if x1 <= x <= x2 and z1 <= z <= z2 and _solid(t, (x, y, z))
    ]
    if not peaks:
        raise AssertionError(
            f"OWS-009 articulation region {(x1, x2, z1, z2)} contains no solid geometry"
        )
    return max(peaks)


def _assert_three_cell_vertical_hierarchy(t: gate.base.Template) -> None:
    # Use each work cell's central roof/plant zone, excluding the shared roadside
    # identity blade. r1 was rejected because the cells read as one roof datum.
    peaks = {
        "diagnostic": _column_peak(t, 5, 13, 12, 33),
        "heavy-intervention": _column_peak(t, 16, 24, 12, 33),
        "recommissioning": _column_peak(t, 27, 34, 12, 33),
    }
    if len(set(peaks.values())) != 3:
        raise AssertionError(
            "OWS-009 work-cell vertical hierarchy collapsed; expected three "
            f"distinct roof/plant peaks, got {peaks}"
        )
    if peaks["heavy-intervention"] != max(peaks.values()):
        raise AssertionError(
            "OWS-009 heavy-intervention cell must remain the dominant roof mass; "
            f"got {peaks}"
        )


def _assert_vehicle_threshold_differentiation(t: gate.base.Template) -> None:
    # Measure the highest clear opening at the three north-facing vehicle mouths.
    # r1 was rejected because the thresholds sat under nearly one datum.
    thresholds = {
        "diagnostic": (range(5, 13), 7),
        "heavy-intervention": (range(16, 24), 7),
        "recommissioning": (range(27, 34), 7),
    }
    clear_tops: dict[str, int] = {}
    for label, (xs, z) in thresholds.items():
        clear_levels = []
        for y in range(2, 12):
            if all(gate._name(t, (x, y, z)) in AIR for x in xs):
                clear_levels.append(y)
        if not clear_levels:
            raise AssertionError(f"OWS-009 {label} vehicle threshold has no clear opening")
        clear_tops[label] = max(clear_levels)

    if len(set(clear_tops.values())) < 2:
        raise AssertionError(
            "OWS-009 vehicle thresholds regressed to one opening datum: "
            f"{clear_tops}"
        )
    if clear_tops["heavy-intervention"] <= clear_tops["diagnostic"]:
        raise AssertionError(
            "OWS-009 heavy-intervention opening must remain taller than diagnostics; "
            f"got {clear_tops}"
        )

    # Bay 03's projecting recommissioning canopy is a separate silhouette cue,
    # not just an alternate opening height.
    canopy_required = {
        (26, 8, 5): "tfmg:steel_block",
        (30, 9, 4): "minecraft:orange_concrete",
        (34, 8, 6): "tfmg:steel_block",
    }
    for pos, expected in canopy_required.items():
        actual = gate._name(t, pos)
        if actual != expected:
            raise AssertionError(
                f"OWS-009 recommissioning canopy articulation drift at {pos}: "
                f"{actual} != {expected}"
            )


def _assert_side_facade_bay_depth(t: gate.base.Template) -> None:
    # Projected steel modules on both long elevations break the donor-garage
    # wall planes. Require all four bay stations on both sides to survive.
    stations = (10, 17, 24, 31)
    missing: list[str] = []
    for z in stations:
        if gate._name(t, (2, 4, z)) != "tfmg:steel_block":
            missing.append(f"west@z{z}")
        if gate._name(t, (36, 4, z)) != "tfmg:steel_block":
            missing.append(f"east@z{z}")
    if missing:
        raise AssertionError(
            "OWS-009 long-elevation projected bay rhythm regressed: " + ", ".join(missing)
        )

    # The side elevations must also retain separated clerestory modules rather
    # than a continuous ribbon window.
    for x in (3, 35):
        first = any(
            gate._name(t, (x, y, z)) == "create:framed_glass"
            for y in range(7, 11)
            for z in range(10, 15)
        )
        gap = all(
            gate._name(t, (x, y, z)) != "create:framed_glass"
            for y in range(7, 11)
            for z in range(15, 18)
        )
        second = any(
            gate._name(t, (x, y, z)) == "create:framed_glass"
            for y in range(7, 11)
            for z in range(18, 23)
        )
        if not (first and gap and second):
            raise AssertionError(
                f"OWS-009 side clerestory modularity regressed on x={x}: "
                f"first={first}, gap={gap}, second={second}"
            )


def _assert_rear_facade_rhythm(t: gate.base.Template) -> None:
    # Six projected rear frame stations and three separated window modules make
    # the rear elevation read as construction bays instead of a flush back wall.
    projected_stations = (5, 13, 17, 23, 28, 34)
    missing = [
        x
        for x in projected_stations
        if gate._name(t, (x, 4, 35)) != "tfmg:steel_block"
    ]
    if missing:
        raise AssertionError(
            f"OWS-009 rear projected frame rhythm missing stations: {missing}"
        )

    window_bands = ((6, 11, 8), (17, 22, 10), (28, 32, 9))
    for x1, x2, y in window_bands:
        if not all(
            gate._name(t, (x, y, 34)) == "create:framed_glass"
            for x in range(x1, x2 + 1)
        ):
            raise AssertionError(
                f"OWS-009 rear clerestory band drifted at x={x1}-{x2}, y={y}"
            )


def _assert_atlas_identity_is_structural(t: gate.base.Template) -> None:
    # Atlas identity must remain a physical frame/blade assembly. These anchors
    # cross multiple depths/heights so a flat orange decal cannot satisfy them.
    anchors = {
        (12, 13, 6): "tfmg:steel_block",
        (20, 14, 5): "minecraft:orange_concrete",
        (20, 15, 4): "minecraft:polished_blackstone",
        (29, 13, 6): "tfmg:steel_block",
    }
    depths = defaultdict(set)
    for pos, expected in anchors.items():
        actual = gate._name(t, pos)
        if actual != expected:
            raise AssertionError(
                f"OWS-009 Atlas structural-identity anchor drift at {pos}: "
                f"{actual} != {expected}"
            )
        depths[expected].add(pos[2])

    occupied_z = {pos[2] for pos in anchors}
    occupied_y = {pos[1] for pos in anchors}
    if len(occupied_z) < 3 or len(occupied_y) < 3:
        raise AssertionError("OWS-009 Atlas identity collapsed to a flat surface treatment")


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)

    _assert_three_cell_vertical_hierarchy(model)
    _assert_vehicle_threshold_differentiation(model)
    _assert_side_facade_bay_depth(model)
    _assert_rear_facade_rhythm(model)
    _assert_atlas_identity_is_structural(model)

    print(
        "OWS-009 Gate-A r2 articulation preflight PASS: the three work cells retain "
        "distinct vertical hierarchy; vehicle thresholds remain differentiated; "
        "Bay 03 retains its projecting recommissioning canopy; both long elevations "
        "retain projected bay rhythm and separated clerestories; the rear elevation "
        "retains projected frame/window modules; and Atlas identity remains a "
        "multi-depth structural assembly. Independent fixed-camera visual review and "
        "all runtime/Lost-Cities/shipping-NBT/gameplay/production gates remain pending."
    )


if __name__ == "__main__":
    main()

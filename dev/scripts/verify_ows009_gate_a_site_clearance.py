#!/usr/bin/env python3
"""Deterministic site-clearance preflight for OWS-009 Gate-A r2.

This validates the review-model reservation envelope around the structure so
later terrain/Lost-Cities integration has explicit maneuver, seam, drainage,
and vertical-clearance capacity. It does not claim generated-world placement,
Lost Cities coexistence, runtime acceptance, shipping-NBT transform behavior,
visual acceptance, gameplay validation, or production admission.
"""
from __future__ import annotations

import render_ows009_gate_a_massing as gate


AIR = gate.AIR
HARDSCAPE = gate.HARDSCAPE


def _name(t: gate.base.Template, pos: tuple[int, int, int]) -> str | None:
    return gate._name(t, pos)


def _assert_transition_reservations(t: gate.base.Template) -> None:
    # These bands are deliberately kept free of built mass so a placement
    # adapter can absorb local grade, drainage, retaining, and neighboring-road
    # interfaces without cutting into authored architecture.
    intrusions: list[tuple[int, int, int, str | None]] = []

    # North seam: entire outer row above datum must remain clear.
    for x in range(49):
        for y in range(1, 18):
            name = _name(t, (x, y, 0))
            if name not in AIR:
                intrusions.append((x, y, 0, name))

    # East seam: X48 must remain clear above datum.
    for z in range(41):
        for y in range(1, 18):
            name = _name(t, (48, y, z))
            if name not in AIR:
                intrusions.append((48, y, z, name))

    # Rear seam: Z40 must remain clear above datum.
    for x in range(49):
        for y in range(1, 18):
            name = _name(t, (x, y, 40))
            if name not in AIR:
                intrusions.append((x, y, 40, name))

    if intrusions:
        raise AssertionError(
            "OWS-009 protected terrain-transition reservation contains built "
            f"mass above datum: {intrusions[:12]}"
        )


def _assert_vehicle_standoff(t: gate.base.Template) -> None:
    # Preserve an exterior standoff volume in front of each bay. This catches
    # later signage/canopy/detail edits that would leave a valid doorway but an
    # unusable recovery apron.
    lanes = {
        "diagnostic": (range(5, 13), range(2, 7), range(1, 6)),
        "heavy-intervention": (range(16, 24), range(2, 7), range(1, 8)),
        "recommissioning": (range(27, 34), range(2, 7), range(1, 7)),
    }
    obstructed = []
    for label, (xs, zs, ys) in lanes.items():
        for x in xs:
            for z in zs:
                for y in ys:
                    name = _name(t, (x, y, z))
                    if name not in AIR:
                        obstructed.append((label, x, y, z, name))
    if obstructed:
        raise AssertionError(
            "OWS-009 exterior vehicle standoff volume obstructed: "
            f"{obstructed[:12]}"
        )


def _assert_service_lane_vertical_clearance(t: gate.base.Template) -> None:
    # The four-wide east maneuvering strip must not only remain paved at grade;
    # it must retain enough vertical air for delivery/core-return traffic.
    obstructed = []
    for x in range(44, 48):
        for z in range(18, 40):
            if _name(t, (x, 0, z)) != "tfmg:asphalt":
                obstructed.append(("grade", x, 0, z, _name(t, (x, 0, z))))
            for y in range(1, 7):
                name = _name(t, (x, y, z))
                if name not in AIR:
                    obstructed.append(("clearance", x, y, z, name))
    if obstructed:
        raise AssertionError(
            "OWS-009 east service lane lost grade/vertical clearance: "
            f"{obstructed[:12]}"
        )


def _assert_public_standoff(t: gate.base.Template) -> None:
    # Preserve a human-scale exterior landing and approach immediately north of
    # the customer threshold, independent of the vehicle recovery apron.
    bad = []
    for x in range(38, 42):
        for z in range(2, 7):
            if _name(t, (x, 0, z)) not in HARDSCAPE:
                bad.append(("grade", x, 0, z, _name(t, (x, 0, z))))
            for y in range(1, 4):
                name = _name(t, (x, y, z))
                if name not in AIR:
                    bad.append(("headroom", x, y, z, name))
    if bad:
        raise AssertionError(
            "OWS-009 public approach/landing lost independent clear standoff: "
            f"{bad[:12]}"
        )


def _assert_roof_vertical_envelope(t: gate.base.Template) -> None:
    # Nothing may exceed the declared 18-block review envelope. Template bounds
    # already catch explicit coordinates outside it; this additionally freezes
    # one clear block above every authored topmost occupied column, preventing
    # later details from consuming the last voxel of vertical placement margin.
    sx, sy, sz = map(int, t.size)
    if sy != 18:
        raise AssertionError(f"OWS-009 unexpected vertical envelope: {sy}")

    roof_hits = []
    for x in range(sx):
        for z in range(sz):
            if _name(t, (x, 17, z)) not in AIR:
                roof_hits.append((x, 17, z, _name(t, (x, 17, z))))
    if roof_hits:
        raise AssertionError(
            "OWS-009 authored mass consumes the top envelope layer; "
            f"vertical placement margin lost at {roof_hits[:12]}"
        )


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)

    _assert_transition_reservations(model)
    _assert_vehicle_standoff(model)
    _assert_service_lane_vertical_clearance(model)
    _assert_public_standoff(model)
    _assert_roof_vertical_envelope(model)

    print(
        "OWS-009 Gate-A r2 site-clearance preflight PASS: protected north/east/rear "
        "transition bands remain free of above-grade authored mass; all three bay "
        "recovery standoff volumes remain clear; the four-wide east service lane "
        "retains six blocks of vertical clearance; the customer approach retains "
        "independent landing/headroom; and the top template layer remains reserved "
        "as vertical placement margin. Generated-world terrain adaptation, Lost "
        "Cities coexistence, runtime placement, shipping-NBT transforms, visual, "
        "gameplay, and production gates remain pending."
    )


if __name__ == "__main__":
    main()

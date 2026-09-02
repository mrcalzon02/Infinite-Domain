#!/usr/bin/env python3
"""Deterministic transform-safety preflight for OWS-009 Gate-A r2.

This validates review-model coordinate transforms only. It does not claim
Minecraft runtime placement, processor behavior, Lost Cities coexistence,
shipping-NBT transform acceptance, visual quality, gameplay hooks, or
production admission.
"""
from __future__ import annotations

from collections import Counter

import render_ows009_gate_a_massing as gate


def _rotate_y(
    pos: tuple[int, int, int],
    size: tuple[int, int, int],
    quarter_turns: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Rotate one template coordinate clockwise around Y in 90-degree steps."""
    x, y, z = pos
    sx, sy, sz = size
    turns = quarter_turns % 4

    if turns == 0:
        return (x, y, z), (sx, sy, sz)
    if turns == 1:
        return (sz - 1 - z, y, x), (sz, sy, sx)
    if turns == 2:
        return (sx - 1 - x, y, sz - 1 - z), (sx, sy, sz)
    return (z, y, sx - 1 - x), (sz, sy, sx)


def _mirror_x(
    pos: tuple[int, int, int],
    size: tuple[int, int, int],
) -> tuple[int, int, int]:
    x, y, z = pos
    sx, _, _ = size
    return (sx - 1 - x, y, z)


def _transform_model(
    model: gate.base.Template,
    quarter_turns: int,
    mirror_x: bool,
) -> tuple[dict[tuple[int, int, int], str | None], tuple[int, int, int]]:
    source_size = tuple(map(int, model.size))
    transformed: dict[tuple[int, int, int], str | None] = {}
    target_size: tuple[int, int, int] | None = None

    for pos in model.blocks:
        rotated, rotated_size = _rotate_y(pos, source_size, quarter_turns)
        if mirror_x:
            rotated = _mirror_x(rotated, rotated_size)
        if rotated in transformed:
            raise AssertionError(
                f"OWS-009 transform collision at {rotated} "
                f"(turns={quarter_turns}, mirror_x={mirror_x})"
            )
        transformed[rotated] = gate._name(model, pos)
        target_size = rotated_size

    if target_size is None:
        target_size = source_size
    return transformed, target_size


def _assert_in_bounds(
    blocks: dict[tuple[int, int, int], str | None],
    size: tuple[int, int, int],
    label: str,
) -> None:
    sx, sy, sz = size
    invalid = [
        pos
        for pos in blocks
        if not (0 <= pos[0] < sx and 0 <= pos[1] < sy and 0 <= pos[2] < sz)
    ]
    if invalid:
        raise AssertionError(f"OWS-009 {label} produced out-of-bounds blocks: {invalid[:8]}")


def _assert_preserved_inventory(
    original: gate.base.Template,
    transformed: dict[tuple[int, int, int], str | None],
    label: str,
) -> None:
    before = Counter(gate._name(original, pos) for pos in original.blocks)
    after = Counter(transformed.values())
    if before != after:
        raise AssertionError(f"OWS-009 {label} changed transformed block inventory")


def _transformed_edge(
    source_edge: list[tuple[int, int, int]],
    source_size: tuple[int, int, int],
    quarter_turns: int,
    mirror_x: bool,
) -> list[tuple[int, int, int]]:
    out = []
    for pos in source_edge:
        rotated, rotated_size = _rotate_y(pos, source_size, quarter_turns)
        if mirror_x:
            rotated = _mirror_x(rotated, rotated_size)
        out.append(rotated)
    return out


def _assert_transition_edges_follow_transform(
    original: gate.base.Template,
    transformed: dict[tuple[int, int, int], str | None],
    quarter_turns: int,
    mirror_x: bool,
    label: str,
) -> None:
    sx, _, sz = map(int, original.size)
    source_size = tuple(map(int, original.size))
    protected_edges = {
        "north": [(x, 0, 0) for x in range(sx)],
        "east": [(sx - 1, 0, z) for z in range(sz)],
        "rear": [(x, 0, sz - 1) for x in range(sx)],
    }

    for edge_name, source_positions in protected_edges.items():
        positions = _transformed_edge(
            source_positions, source_size, quarter_turns, mirror_x
        )
        paved = [
            pos
            for pos in positions
            if transformed.get(pos) in gate.HARDSCAPE
        ]
        if paved:
            raise AssertionError(
                f"OWS-009 {label} transformed protected {edge_name} edge "
                f"contains hardscape at {paved[:8]}"
            )


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)

    source_count = len(model.blocks)
    for quarter_turns in range(4):
        for mirror_x in (False, True):
            label = f"rot{quarter_turns * 90}_mirrorX_{str(mirror_x).lower()}"
            transformed, size = _transform_model(model, quarter_turns, mirror_x)

            if len(transformed) != source_count:
                raise AssertionError(
                    f"OWS-009 {label} changed block count: "
                    f"{len(transformed)} != {source_count}"
                )

            expected_size = (
                (49, 18, 41)
                if quarter_turns % 2 == 0
                else (41, 18, 49)
            )
            if size != expected_size:
                raise AssertionError(
                    f"OWS-009 {label} dimensions drifted: {size} != {expected_size}"
                )

            _assert_in_bounds(transformed, size, label)
            _assert_preserved_inventory(model, transformed, label)
            _assert_transition_edges_follow_transform(
                model, transformed, quarter_turns, mirror_x, label
            )

    print(
        "OWS-009 Gate-A r2 transform preflight PASS: four Y rotations and "
        "their X-mirrored variants preserve block count/inventory, remain "
        "inside the expected 49x18x41 or 41x18x49 envelopes, and carry the "
        "protected north/east/rear terrain-transition edges without transformed "
        "hardscape regressions. Minecraft runtime placement, processor behavior, "
        "Lost Cities coexistence, shipping-NBT transform acceptance, visual, "
        "gameplay, and production gates remain pending."
    )


if __name__ == "__main__":
    main()

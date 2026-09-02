#!/usr/bin/env python3
"""Deterministic preflight for the review-only OWS-009 Gate-A r2 massing study.

This check deliberately does not render imagery and cannot approve visual quality,
runtime placement, Lost Cities coexistence, rotation/mirroring, shipping-NBT
equivalence, gameplay hooks, or production admission.
"""
from __future__ import annotations

import hashlib
import subprocess
from collections import deque
from pathlib import Path

import render_ows009_gate_a_massing as gate


ROOT = Path(__file__).resolve().parents[2]


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _assert_prerequisites() -> None:
    review_dir = ROOT / "dev/old_world_narrative/reviews/heavy_rebuild"
    missing = [name for name in gate.REQUIRED_RECORDS if not (review_dir / name).is_file()]
    if missing:
        raise AssertionError(f"OWS-009 Gate-A prerequisites missing: {missing}")

    baseline = (review_dir / "OWS-009_PHASE0_BASELINE_REVIEW.md").read_text(encoding="utf-8")
    if "BASELINE SUFFICIENT. REBUILD REQUIRED." not in baseline:
        raise AssertionError("OWS-009 independent Phase-0 disposition is missing")

    r1_review = (review_dir / "OWS-009_GATE_A_R1_REVIEW.md").read_text(encoding="utf-8")
    if "OWS-009 GATE A r1: REVISION REQUIRED." not in r1_review:
        raise AssertionError("OWS-009 Gate-A r1 rejection is missing")


def _assert_shipping_source_frozen() -> None:
    source_bytes = gate.SOURCE_PATH.read_bytes()
    actual_sha256 = hashlib.sha256(source_bytes).hexdigest()
    if actual_sha256 != gate.FROZEN_SOURCE_SHA256:
        raise AssertionError(
            f"OWS-009 shipping NBT SHA-256 drifted: {actual_sha256} != {gate.FROZEN_SOURCE_SHA256}"
        )

    actual_blob = _git_blob(gate.SOURCE_PATH)
    if actual_blob != gate.FROZEN_SOURCE_BLOB:
        raise AssertionError(
            f"OWS-009 shipping Git blob drifted: {actual_blob} != {gate.FROZEN_SOURCE_BLOB}"
        )


def _assert_template_bounds(t: gate.base.Template) -> None:
    sx, sy, sz = map(int, t.size)
    out_of_bounds = [
        pos
        for pos in t.blocks
        if not (0 <= pos[0] < sx and 0 <= pos[1] < sy and 0 <= pos[2] < sz)
    ]
    if out_of_bounds:
        raise AssertionError(f"OWS-009 Gate-A contains out-of-bounds blocks: {out_of_bounds[:8]}")


def _assert_cell_hierarchy(t: gate.base.Template) -> None:
    # Frozen roof anatomy ensures the three work cells remain deliberately
    # differentiated instead of regressing to copied garage bays.
    roof_anchors = {
        (8, 14, 20): "tfmg:steel_block",
        (20, 17, 20): "tfmg:steel_block",
        (30, 15, 20): "tfmg:steel_block",
    }
    for pos, expected in roof_anchors.items():
        actual = gate._name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-009 work-cell roof hierarchy drift at {pos}: {actual} != {expected}")

    # Public entry and the parts/core-return thresholds must remain distinct.
    clear_points = {
        (39, 3, 7): "customer entrance",
        (43, 4, 23): "parts receiving",
        (39, 4, 34): "core return",
    }
    for pos, label in clear_points.items():
        if gate._name(t, pos) not in gate.AIR:
            raise AssertionError(f"OWS-009 {label} threshold obstructed at {pos}")


def _assert_circulation_graph(t: gate.base.Template) -> None:
    """Prove the programmed interior is one usable two-block-high service graph.

    Gate A is still a massing study, so this deliberately tests only spatial
    reachability over supported floor. It prevents a visually plausible edit
    from silently isolating a repair cell, customer room, parts room, core-return
    room, or the technician spine behind an unbroken wall.
    """
    sx, _, sz = map(int, t.size)

    def walkable(x: int, z: int) -> bool:
        if not (0 <= x < sx and 0 <= z < sz):
            return False
        floor = gate._name(t, (x, 1, z))
        head = gate._name(t, (x, 2, z))
        upper = gate._name(t, (x, 3, z))
        return floor not in gate.AIR and head in gate.AIR and upper in gate.AIR

    anchors = {
        "diagnostic cell": (9, 20),
        "heavy-intervention cell": (20, 20),
        "recommissioning cell": (30, 20),
        "technician spine": (20, 29),
        "customer/service bar": (39, 12),
        "parts receive/issue": (40, 23),
        "core-return/records": (40, 30),
    }
    unsupported = [label for label, pos in anchors.items() if not walkable(*pos)]
    if unsupported:
        raise AssertionError(f"OWS-009 circulation anchors are not walkable: {unsupported}")

    start = anchors["technician spine"]
    seen = {start}
    queue = deque([start])
    while queue:
        x, z = queue.popleft()
        for nxt in ((x - 1, z), (x + 1, z), (x, z - 1), (x, z + 1)):
            if nxt not in seen and walkable(*nxt):
                seen.add(nxt)
                queue.append(nxt)

    isolated = [label for label, pos in anchors.items() if pos not in seen]
    if isolated:
        raise AssertionError(
            "OWS-009 operational circulation graph is disconnected; "
            f"unreachable from technician spine: {isolated}"
        )


def main() -> None:
    _assert_prerequisites()
    _assert_shipping_source_frozen()

    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)
    _assert_template_bounds(model)
    _assert_cell_hierarchy(model)
    _assert_circulation_graph(model)

    print(
        "OWS-009 Gate-A r2 deterministic preflight PASS: "
        "source provenance, 49x18x41 envelope, protected transition edges, "
        "east service lane, clear service/circulation fields, frozen Atlas "
        "massing anchors, cell hierarchy, connected operational circulation, "
        "template bounds, and deferred-content exclusion are internally consistent. "
        "Visual Gate-A review and all runtime/Lost-Cities/rotation/shipping-NBT/"
        "gameplay/production gates remain pending."
    )


if __name__ == "__main__":
    main()

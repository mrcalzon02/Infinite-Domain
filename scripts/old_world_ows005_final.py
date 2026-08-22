#!/usr/bin/env python3
"""Side-effect-free authoritative OWS-005 production builder.

The accepted Gate-C D3 model is frozen in the pure target-local geometry module.
This module adds only the reviewed Pass-19 microdetail overlay. Importing this
module and calling ``build_005`` never serializes files or mutates registries.
"""
from __future__ import annotations

import generate_wasteland_sites as base
import old_world_ows005_geometry as geometry


ACCEPTED_GATE_C_D3_SHA256 = "b5abd645c32f43ce8c40315f9801d41aa0f33361bfd8c8dd9bd7b6826a58ca2f"
PROOF_POS = geometry.PROOF_POS
PROOF_LOOT_TABLE = geometry.PROOF_LOOT_TABLE

# Every Pass-19 mutation is deliberately inside one of the already accepted
# D3 weather/damage zones. None intersects a protected route or proof block.
PASS19_MICRODETAIL = {
    (27, 3, 37): "minecraft:cobweb",       # wet-line-02 breach sediment
    (25, 2, 43): "minecraft:brown_mushroom",  # reject-exit water path
    (45, 4, 36): "minecraft:cobweb",       # rear-monitor debris field
    (46, 2, 37): "minecraft:brown_mushroom",  # packing-line-02 damp edge
    (54, 6, 25): "minecraft:cobweb",       # cold-hold-B roof breach
    (53, 5, 23): "minecraft:brown_mushroom",  # cold-B damp masonry
    (6, 3, 36): "minecraft:cobweb",        # receiving-bay-02 canopy loss
    (7, 2, 38): "minecraft:brown_mushroom",  # receiving debris edge
}


def build_accepted_d3() -> base.Template:
    """Return the independently accepted Gate-C D3 model without Pass 19."""
    return geometry.build_d3()


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        t.set(*pos, block)


def _assert_final_contracts(t: base.Template) -> None:
    geometry._assert_d3_contracts(t)
    if tuple(t.size) != (59, 24, 51):
        raise AssertionError(f"OWS-005 final dimensions changed: {t.size}")
    for pos, expected in PASS19_MICRODETAIL.items():
        actual = geometry._name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-005 Pass-19 detail drift at {pos}: {actual} != {expected}")
    if geometry._name(t, (32, 2, 39)) not in geometry.AIR:
        raise AssertionError("OWS-005 Pass-19 detail obstructed the QA proof approach")


def build_005() -> base.Template:
    """Build accepted D3 plus localized Pass-19 microdetail, without I/O."""
    t = build_accepted_d3()
    _apply_pass19_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    raise SystemExit("Import build_005 from the authoritative generator; this module performs no writes.")



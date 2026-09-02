#!/usr/bin/env python3
"""Deterministic preflight for OWS-008 Gate-C r2.

This verifier intentionally does not approve visual Gate C, runtime placement,
Lost Cities coexistence, or production admission. It resolves every currently
machine-checkable D0/D1/D3 contract before a reviewer spends time on imagery.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import render_ows008_gate_c_damage_states as gate_c

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SIZE = gate_c.SIZE
PROOF_TABLE = gate_c.PROOF_LOOT_TABLE
PROOF_POS = gate_c.PROOF_POS
SPAWNERS = gate_c.SPAWNERS
AIR = gate_c.AIR


def name(t, pos):
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def count_block(t, block):
    return sum(name(t, pos) == block for pos in t.blocks)


def count_loot_table(t, loot_table):
    return sum(
        1 for _, block_nbt in t.blocks.values()
        if block_nbt and block_nbt.get("LootTable") == loot_table
    )


def assert_common(label, t):
    if tuple(t.size) != EXPECTED_SIZE:
        raise AssertionError(f"{label}: bounds drifted from {EXPECTED_SIZE}: {t.size}")
    gate_c.gate_b._assert_intact_contracts(t)


def assert_no_gate_c_gameplay(label, t):
    proof_count = count_loot_table(t, PROOF_TABLE)
    if proof_count:
        raise AssertionError(f"{label}: premature canonical proof nodes: {proof_count}")
    spawners = count_block(t, "minecraft:spawner")
    if spawners:
        raise AssertionError(f"{label}: premature encounter spawners: {spawners}")


def assert_diff_containment(d0, d1, d3):
    d01 = gate_c._diff_positions(d0, d1)
    d03 = gate_c._diff_positions(d0, d3)
    if not d01:
        raise AssertionError("D1 has no architectural/history delta from D0")
    if not d03:
        raise AssertionError("D3 has no damage/abandonment delta from D0")

    # Gate-C work must remain inside the accepted structure envelope.
    for label, positions in (("D1", d01), ("D3", d03)):
        outside = [p for p in positions if not (0 <= p[0] < EXPECTED_SIZE[0] and 0 <= p[1] < EXPECTED_SIZE[1] and 0 <= p[2] < EXPECTED_SIZE[2])]
        if outside:
            raise AssertionError(f"{label}: changed positions outside accepted envelope: {outside[:8]}")

    # D3 must strictly extend the investigation state rather than replacing it
    # wholesale with an unrelated ruin.
    if len(d03) <= len(d01):
        raise AssertionError(f"D3 delta ({len(d03)}) must exceed D1 investigation delta ({len(d01)})")

    return len(d01), len(d03)


def main():
    gate_c._assert_history_authorized()
    gate_c._assert_canonical_loot_contract()

    d0 = gate_c.build_d0()
    d1 = gate_c.build_d1()
    d3 = gate_c.build_d3()

    assert_common("D0", d0)
    assert_common("D1", d1)
    # D3 contains intentional Gate-C proof/spawner gameplay and therefore uses
    # the dedicated D3 contract after the underlying intact architecture check.
    gate_c._assert_d3_contracts(d3)

    assert_no_gate_c_gameplay("D0", d0)
    assert_no_gate_c_gameplay("D1", d1)

    if count_loot_table(d3, PROOF_TABLE) != 1:
        raise AssertionError("D3 must contain exactly one canonical proof node")
    if count_block(d3, "minecraft:spawner") != len(SPAWNERS):
        raise AssertionError("D3 must contain exactly three bounded encounter spawners")

    d01, d03 = assert_diff_containment(d0, d1, d3)

    summary = {
        "target": gate_c.TARGET,
        "gate": "C r2 deterministic preflight",
        "size": list(EXPECTED_SIZE),
        "d1_changed_positions_vs_d0": d01,
        "d3_changed_positions_vs_d0": d03,
        "proof_nodes": {"D0": 0, "D1": 0, "D3": 1},
        "spawners": {"D0": 0, "D1": 0, "D3": len(SPAWNERS)},
        "visual_gate_approved": False,
        "runtime_placement_approved": False,
        "lost_cities_approved": False,
        "production_admitted": False,
    }
    encoded = json.dumps(summary, sort_keys=True).encode("utf-8")
    summary["summary_sha256"] = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

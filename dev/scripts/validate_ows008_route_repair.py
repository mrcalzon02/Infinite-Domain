#!/usr/bin/env python3
"""Validate OWS-008's target-local west-stair route repair without repo writes."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import sys
from pathlib import Path

import generate_wasteland_sites as base
import old_world_ows008_final as final_builder


ROOT = Path(__file__).resolve().parents[2]
SHIPPING_NBT = (
    ROOT
    / "kubejs/data/infinite_domain/structure/wasteland/old_world"
    / "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
EXPECTED_REPAIR_DELTA = {
    (4, 4, 21), (5, 4, 21),
    (4, 5, 21), (5, 5, 21),
    (4, 7, 23), (5, 7, 23),
    (4, 13, 23), (5, 13, 23),
}
LEGACY_ROUTE_BLOCKS = {
    (4, 4, 21): "minecraft:white_concrete",
    (5, 4, 21): "minecraft:white_concrete",
    (4, 5, 21): "minecraft:white_concrete",
    (5, 5, 21): "minecraft:white_concrete",
    (4, 7, 23): "minecraft:smooth_stone",
    (5, 7, 23): "minecraft:smooth_stone",
    (4, 13, 23): "minecraft:smooth_quartz",
    (5, 13, 23): "minecraft:smooth_quartz",
}
RUINED_FUNCTIONAL_PROPS = {
    (4, 2, 23): "kubejs:ruined_brewing_stand",
    (4, 2, 26): "kubejs:ruined_brewing_stand",
    (9, 3, 41): "kubejs:ruined_brewing_stand",
    (20, 3, 41): "kubejs:ruined_brewing_stand",
    (31, 3, 41): "kubejs:ruined_brewing_stand",
    (42, 2, 29): "kubejs:ruined_cauldron",
    (42, 3, 41): "kubejs:ruined_brewing_stand",
    (47, 2, 29): "kubejs:ruined_cauldron",
    (49, 2, 23): "kubejs:ruined_brewing_stand",
    (49, 2, 26): "kubejs:ruined_brewing_stand",
    (52, 2, 31): "kubejs:ruined_cauldron",
}


def _serialized_bytes(t: base.Template) -> tuple[bytes, bytes]:
    blocks = []
    for pos, (state, nbt) in sorted(t.blocks.items(), key=lambda row: (row[0][1], row[0][2], row[0][0])):
        entry = {"pos": base.NbtList(base.TAG_INT, list(pos)), "state": state}
        if nbt:
            entry["nbt"] = nbt
        blocks.append(entry)
    root = {
        "DataVersion": base.DATA_VERSION,
        "size": base.NbtList(base.TAG_INT, list(t.size)),
        "palette": base.NbtList(base.TAG_COMPOUND, t.palette),
        "blocks": base.NbtList(base.TAG_COMPOUND, blocks),
        "entities": base.NbtList(base.TAG_COMPOUND, t.entities),
    }
    raw = bytes([base.TAG_COMPOUND]) + base._utf("") + base._payload(root)
    return gzip.compress(raw, mtime=0), raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-shipping-match", action="store_true")
    args = parser.parse_args()

    built = final_builder.build_008()
    base.stabilize_door_pairs(built)
    final_builder._assert_final_contracts(built)
    built_bytes, built_raw = _serialized_bytes(built)

    legacy = copy.deepcopy(built)
    for pos, block in LEGACY_ROUTE_BLOCKS.items():
        legacy.set(*pos, block)
    legacy_bytes, legacy_raw = _serialized_bytes(legacy)
    built_blocks = {pos: final_builder._name(built, pos) for pos in built.blocks}
    for pos, expected in RUINED_FUNCTIONAL_PROPS.items():
        if built_blocks.get(pos) != expected:
            raise AssertionError(
                f"OWS-008 unsafe functional prop replacement drift at {pos}: "
                f"{built_blocks.get(pos)} != {expected}"
            )
    legacy_blocks = {pos: final_builder._name(legacy, pos) for pos in legacy.blocks}
    all_positions = set(legacy_blocks) | set(built_blocks)
    changed_positions = {
        pos for pos in all_positions
        if legacy_blocks.get(pos, "minecraft:air") != built_blocks.get(pos, "minecraft:air")
    }
    if changed_positions != EXPECTED_REPAIR_DELTA:
        raise AssertionError(
            "OWS-008 route repair changed unexpected named-block positions: "
            f"{sorted(changed_positions ^ EXPECTED_REPAIR_DELTA)}"
        )

    shipping_bytes = SHIPPING_NBT.read_bytes()
    shipping_raw = gzip.decompress(shipping_bytes)
    exact_match = shipping_bytes == built_bytes and shipping_raw == built_raw
    legacy_match = shipping_bytes == legacy_bytes and shipping_raw == legacy_raw
    if not exact_match and not legacy_match:
        raise AssertionError("OWS-008 live shipping matches neither the proven pre-repair nor repaired builder")
    if args.require_shipping_match and not exact_match:
        raise AssertionError("OWS-008 repaired builder has not been generated to authoritative shipping NBT")

    print(f"builder_sha256={hashlib.sha256(built_bytes).hexdigest()}")
    print(f"builder_decompressed_sha256={hashlib.sha256(built_raw).hexdigest()}")
    print(f"shipping_sha256={hashlib.sha256(shipping_bytes).hexdigest()}")
    print(f"exact_shipping_match={str(exact_match).lower()}")
    print(f"synthetic_pre_repair_shipping_match={str(legacy_match).lower()}")
    print(f"synthetic_route_repair_delta_positions={sorted(changed_positions)}")
    print(f"ruined_functional_props_verified={len(RUINED_FUNCTIONAL_PROPS)}")
    print("west_command_stair_treads_and_headroom=verified")
    print("lower_entry_to_upper_proof_approach=connected")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ValueError) as exc:
        print(f"OWS-008 route repair validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

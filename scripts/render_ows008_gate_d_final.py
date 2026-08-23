#!/usr/bin/env python3
"""Prepare OWS-008 Gate-D r2 from the actual authoritative shipping NBT.

This target-local review tool never updates shared state, dispatch, registries,
shipping structures, quality scores, or gate decisions.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

import generate_old_world_narrative_structures as generation
import old_world_ows008_final as final_builder
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure


TARGET = "OWS-008"
EXPECTED_SHIPPING_SHA256 = "62f7246e8d93d2a4bba9bba4224c4ca7131eccce63d9537b5ecab79a0e63b55a"
EXPECTED_GATE_C_R2_D3_SHA256 = "d451e9bcdd00a4937d02011da18a1a8cdf95bb541a1339f5b167486e6828e000"
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
GATE_C_R2_REVIEW = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-008_GATE_C_R2_REVIEW.md"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_d_final" / "r2"
SPEC = generation.BY_TARGET[TARGET]
SHIPPING_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / "old_world" / f"{SPEC.name}.nbt"
TEMP_NAME = "old_world/_heavy_review_ows008_gate_d_sync_r2"
FIXED_CUTAWAY_Y = 7
PROTECTED_ROUTE_POSITIONS = (
    (25, 2, 5), (27, 2, 15), (11, 2, 30), (22, 2, 29),
    (33, 2, 27), (45, 2, 25), (28, 2, 44), (12, 14, 28),
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def _sync() -> dict[str, object]:
    if generation.BUILDERS.get(TARGET) is not final_builder.build_008:
        raise AssertionError("OWS-008 production dispatch is not old_world_ows008_final.build_008")
    production_python = Path(
        os.environ.get(
            "OLD_WORLD_PRODUCTION_PYTHON",
            str(Path(os.environ.get("LOCALAPPDATA", "")) / "Python" / "bin" / "python.exe"),
        )
    )
    if not production_python.is_file():
        raise AssertionError(
            "canonical production Python not found; set OLD_WORLD_PRODUCTION_PYTHON "
            "to the interpreter used for authoritative generation"
        )
    with tempfile.TemporaryDirectory(prefix="ows008-gate-d-r2-") as temp_dir:
        temp_data = Path(temp_dir)
        temp_nbt = temp_data / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
        probe = (
            "import pathlib,sys;sys.path.insert(0,'scripts');"
            "import generate_old_world_narrative_structures as g,old_world_ows008_final as f;"
            "assert g.BUILDERS['OWS-008'] is f.build_008;"
            f"g.base.DATA=pathlib.Path({str(temp_data)!r});"
            "t=g.BUILDERS['OWS-008']();g.base.stabilize_door_pairs(t);f._assert_final_contracts(t);"
            f"t.save({TEMP_NAME!r})"
        )
        subprocess.run([str(production_python), "-c", probe], cwd=ROOT, check=True)
        built_bytes = temp_nbt.read_bytes()
        shipping_bytes = SHIPPING_NBT.read_bytes()
        built_raw = gzip.decompress(built_bytes)
        shipping_raw = gzip.decompress(shipping_bytes)
        if built_bytes != shipping_bytes or built_raw != shipping_raw:
            raise AssertionError(
                "OWS-008 stabilized builder/shipping mismatch: "
                f"builder={_sha(built_bytes)} shipping={_sha(shipping_bytes)}"
            )
        shipping_hash = _sha(shipping_bytes)
        if shipping_hash != EXPECTED_SHIPPING_SHA256:
            raise AssertionError(f"OWS-008 shipping hash drift: {shipping_hash} != {EXPECTED_SHIPPING_SHA256}")
        return {
            "production_python": str(production_python),
            "serialized_nbt_bytes": len(shipping_bytes),
            "decompressed_nbt_bytes": len(shipping_raw),
            "builder_serialization_sha256": _sha(built_bytes),
            "shipping_nbt_sha256": shipping_hash,
            "builder_decompressed_nbt_sha256": _sha(built_raw),
            "shipping_decompressed_nbt_sha256": _sha(shipping_raw),
            "exact_serialized_nbt_match": True,
            "exact_decompressed_nbt_match": True,
        }


def _assert_shipping_contracts(
    size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str]
) -> dict[str, object]:
    if tuple(size) != final_builder.SIZE:
        raise AssertionError(f"OWS-008 shipping dimensions changed: {size}")
    if any(not (0 <= x < 55 and 0 <= y < 22 and 0 <= z < 49) for x, y, z in blocks):
        raise AssertionError("OWS-008 shipping exceeds accepted bounds")
    if blocks.get(final_builder.PROOF_POS) != "minecraft:chest":
        raise AssertionError("OWS-008 shipping proof chest position changed")
    for pos in final_builder.SPAWNERS:
        if blocks.get(pos) != "minecraft:spawner":
            raise AssertionError(f"OWS-008 shipping encounter missing at {pos}")
    if sum(name == "minecraft:spawner" for name in blocks.values()) != len(final_builder.SPAWNERS):
        raise AssertionError("OWS-008 shipping encounter topology changed")
    for pos, expected in final_builder.PASS19_MICRODETAIL.items():
        if blocks.get(pos) != expected:
            raise AssertionError(f"OWS-008 shipping Pass-19 detail missing at {pos}")
    missing_required = [name for name in final_builder.REQUIRED_BLOCKS if name not in blocks.values()]
    if missing_required:
        raise AssertionError(f"OWS-008 shipping required blocks missing: {missing_required}")
    blocked_routes = {
        pos: blocks.get(pos)
        for pos in PROTECTED_ROUTE_POSITIONS
        if blocks.get(pos) not in final_builder.AIR and blocks.get(pos) != "minecraft:iron_door"
    }
    if blocked_routes:
        raise AssertionError(f"OWS-008 protected shipping routes obstructed: {blocked_routes}")
    for x, y, z, rise, facing in final_builder.WEST_COMMAND_STAIR_FLIGHTS:
        dx, dz = {"south": (0, 1), "north": (0, -1)}[facing]
        for step in range(rise):
            tread = (x + dx * step, y + step, z + dz * step)
            if blocks.get(tread) != "minecraft:smooth_quartz_stairs":
                raise AssertionError(f"OWS-008 shipping west-stair tread changed at {tread}: {blocks.get(tread)}")
            for head_y in (tread[1] + 1, tread[1] + 2):
                head = (tread[0], head_y, tread[2])
                if blocks.get(head) not in final_builder.AIR:
                    raise AssertionError(f"OWS-008 shipping west-stair headroom obstructed at {head}: {blocks.get(head)}")
    for feet in final_builder.UPPER_PROOF_ROUTE:
        feet_name = blocks.get(feet)
        head = (feet[0], feet[1] + 1, feet[2])
        head_name = blocks.get(head)
        if feet_name not in final_builder.AIR and not (feet_name or "").endswith("_door"):
            raise AssertionError(f"OWS-008 shipping upper-proof route feet obstructed at {feet}: {feet_name}")
        if head_name not in final_builder.AIR and not (head_name or "").endswith("_door"):
            raise AssertionError(f"OWS-008 shipping upper-proof route head obstructed at {head}: {head_name}")
        support = (feet[0], feet[1] - 1, feet[2])
        if blocks.get(support) in final_builder.AIR:
            raise AssertionError(f"OWS-008 shipping upper-proof route lacks support below {feet}")
    return {
        "dimensions": list(size),
        "positions_in_bounds": True,
        "pass19_microdetail": {str(pos): blocks[pos] for pos in final_builder.PASS19_MICRODETAIL},
        "pass19_positions_verified": len(final_builder.PASS19_MICRODETAIL),
        "canonical_proof_position": list(final_builder.PROOF_POS),
        "canonical_proof_nodes": 1,
        "spawner_positions": [list(pos) for pos in final_builder.SPAWNERS],
        "deterministic_spawners": len(final_builder.SPAWNERS),
        "protected_route_positions": [list(pos) for pos in PROTECTED_ROUTE_POSITIONS],
        "protected_routes_clear": True,
        "west_command_stair_flights_verified": len(final_builder.WEST_COMMAND_STAIR_FLIGHTS),
        "west_command_stair_treads_verified": sum(row[3] for row in final_builder.WEST_COMMAND_STAIR_FLIGHTS),
        "upper_proof_route_positions_verified": len(final_builder.UPPER_PROOF_ROUTE),
        "upper_proof_route_connected": True,
        "required_block_counts": {
            name: sum(block == name for block in blocks.values()) for name in final_builder.REQUIRED_BLOCKS
        },
    }


def _render_fixed_cutaway(
    size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str], manifest: dict[str, object]
) -> None:
    cut_path = OUTPUT_DIR / "interior_cutaway.png"
    cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= FIXED_CUTAWAY_Y}
    isometric(
        size,
        cutaway_blocks,
        False,
        f"{TARGET} — gate_d_final — D3 authoritative shipping + Pass-19 — interior cutaway Y<={FIXED_CUTAWAY_Y}",
    ).save(cut_path)
    contact_views = [
        (view, OUTPUT_DIR / f"{view}.png")
        for view in ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
    ]
    contact_sheet(
        contact_views,
        OUTPUT_DIR / "contact_sheet.png",
        target=TARGET,
        gate="gate_d_final",
        revision=str(manifest["revision"]),
        damage_state=str(manifest["damage_state"]),
        dimensions=size,
        camera_set="ows008_fixed_v1",
    )
    manifest["cutaway_y"] = FIXED_CUTAWAY_Y


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != TARGET:
        raise AssertionError(f"OWS-008 is not active: {state.get('active_target')}")
    if state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("status") != "passed_r2":
        raise AssertionError("OWS-008 Gate C r2 is not passed in authoritative state")
    if not GATE_C_R2_REVIEW.exists() or "OWS-008 GATE C r2: PASSED" not in GATE_C_R2_REVIEW.read_text(encoding="utf-8"):
        raise AssertionError("OWS-008 explicit Gate-C r2 PASSED review is missing")

    sync = _sync()
    size, blocks = unpack_structure(SHIPPING_NBT)
    mechanics = _assert_shipping_contracts(size, blocks)
    shipping_raw = gzip.decompress(SHIPPING_NBT.read_bytes())
    proof_refs = shipping_raw.count(final_builder.PROOF_LOOT_TABLE.encode())
    if proof_refs != 1:
        raise AssertionError(f"OWS-008 shipping requires exactly one canonical proof loot-table reference; found {proof_refs}")

    head = _git_head()
    revision = f"gate-d-r2@{head[:8]}"
    manifest = render_review_set(
        target=TARGET,
        gate="gate_d_final",
        revision=revision,
        damage_state="D3 authoritative stabilized shipping state + Pass-19 microdetail",
        source_commit=head,
        source_path=str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        size=size,
        blocks=blocks,
        output_dir=OUTPUT_DIR,
        camera_set="ows008_fixed_v1",
    )
    _render_fixed_cutaway(size, blocks, manifest)

    sync_record = {
        "target": TARGET,
        "gate": "gate_d_final",
        "revision": revision,
        "spec_name": SPEC.name,
        "authoritative_dispatch": "generate_old_world_narrative_structures.BUILDERS['OWS-008']",
        "authoritative_builder": "old_world_ows008_final.build_008",
        "accepted_gate_c_r2_d3_sha256": EXPECTED_GATE_C_R2_D3_SHA256,
        "production_door_stabilization_applied": True,
        "shipping_nbt": str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        **sync,
        **mechanics,
        "canonical_proof_loot_table": final_builder.PROOF_LOOT_TABLE,
        "canonical_proof_loot_table_references": proof_refs,
        "render_source": "shipping_nbt",
        "fixed_camera_set": "ows008_fixed_v1",
        "fixed_cutaway_y": FIXED_CUTAWAY_Y,
        "review_manifest": str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "final_preview_synchronized_with_authoritative_nbt": True,
    }
    sync_path = OUTPUT_DIR / "authoritative_sync.json"
    sync_path.write_text(json.dumps(sync_record, indent=2) + "\n", encoding="utf-8", newline="\n")

    manifest.update({
        "authoritative_sync_record": str(sync_path.relative_to(ROOT)).replace("\\", "/"),
        "shipping_nbt_sha256": sync["shipping_nbt_sha256"],
        "shipping_decompressed_nbt_sha256": sync["shipping_decompressed_nbt_sha256"],
        "exact_serialized_nbt_match": True,
        "exact_decompressed_nbt_match": True,
        "pass19_positions_verified": len(final_builder.PASS19_MICRODETAIL),
        "canonical_proof_nodes": 1,
        "deterministic_spawners": len(final_builder.SPAWNERS),
        "protected_routes_clear": True,
        "required_blocks_verified": True,
        "visual_review_status": "rendered_pending_independent_review",
    })
    (OUTPUT_DIR / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"OWS-008 Gate-D r2 candidate rendered from shipping NBT: {sync['shipping_nbt_sha256']}")


if __name__ == "__main__":
    main()

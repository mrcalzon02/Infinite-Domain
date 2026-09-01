#!/usr/bin/env python3
"""Prepare OWS-009 Gate-D r1 from actual authoritative shipping NBT.

This target-local review tool never mutates shared state, dispatch, registries,
shipping structures, quality scores, or gate decisions.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_old_world_narrative_structures as generation
import old_world_ows009_final as final_builder
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure


TARGET = "OWS-009"
EXPECTED_SHIPPING_SHA256 = "261ad9b53740a55a791fa0f7f06915123f95e347704e5a8238efa25bebbeafd9"
STATE_PATH = ROOT / "old_world_narrative/registry/heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_d_final" / "r1"
SPEC = generation.BY_TARGET[TARGET]
SHIPPING_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world" / f"{SPEC.name}.nbt"
TEMP_NAME = "old_world/_heavy_review_ows009_gate_d_sync_r1"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/_heavy_review_ows009_gate_d_sync_r1.nbt"
FIXED_CUTAWAY_Y = 6
ROUTE_REGIONS = (
    ((8, 2, 8), (10, 4, 22), "Bay-01 vehicle lane"),
    ((19, 2, 8), (21, 4, 22), "Bay-02 vehicle lane"),
    ((29, 2, 8), (31, 4, 22), "Bay-03 vehicle lane"),
    ((5, 2, 24), (33, 3, 27), "transverse field"),
    ((5, 2, 28), (33, 3, 31), "technician spine"),
    ((39, 2, 8), (42, 3, 14), "customer route"),
    ((41, 2, 23), (43, 3, 25), "parts route"),
    ((39, 2, 29), (40, 3, 34), "records/core route"),
)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def _sync() -> dict[str, object]:
    if generation.BUILDERS.get(TARGET) is not final_builder.build_009:
        raise AssertionError("OWS-009 production dispatch is not old_world_ows009_final.build_009")
    probe = (
        "import sys;sys.path.insert(0,'scripts');"
        "import generate_old_world_narrative_structures as g,old_world_ows009_final as f;"
        "assert g.BUILDERS['OWS-009'] is f.build_009;"
        "t=g.BUILDERS['OWS-009']();g.base.stabilize_door_pairs(t);f._assert_final_contracts(t);"
        f"t.save({TEMP_NAME!r})"
    )
    production_python = Path(
        os.environ.get(
            "OLD_WORLD_PRODUCTION_PYTHON",
            str(Path(os.environ.get("LOCALAPPDATA", "")) / "Python/bin/python.exe"),
        )
    )
    if not production_python.is_file():
        raise AssertionError("canonical production Python missing; set OLD_WORLD_PRODUCTION_PYTHON")
    subprocess.run([str(production_python), "-c", probe], cwd=ROOT, check=True)
    try:
        built_bytes = TEMP_NBT.read_bytes()
        shipping_bytes = SHIPPING_NBT.read_bytes()
        built_raw = gzip.decompress(built_bytes)
        shipping_raw = gzip.decompress(shipping_bytes)
        if built_bytes != shipping_bytes or built_raw != shipping_raw:
            raise AssertionError(
                "OWS-009 stabilized builder/shipping mismatch: "
                f"builder={_sha(built_bytes)} shipping={_sha(shipping_bytes)}"
            )
        shipping_hash = _sha(shipping_bytes)
        if shipping_hash != EXPECTED_SHIPPING_SHA256:
            raise AssertionError(f"OWS-009 shipping hash drift: {shipping_hash} != {EXPECTED_SHIPPING_SHA256}")
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
    finally:
        TEMP_NBT.unlink(missing_ok=True)


def _assert_pass19_delta() -> dict[str, object]:
    accepted = final_builder.build_accepted_d3()
    final = final_builder.build_009()
    positions = set(accepted.blocks) | set(final.blocks)
    delta = {
        pos for pos in positions
        if final_builder._name(accepted, pos) != final_builder._name(final, pos)
    }
    if delta != set(final_builder.PASS19_MICRODETAIL):
        raise AssertionError(f"OWS-009 Pass-19 delta drifted: {sorted(delta)}")
    if any(final_builder._name(accepted, pos) not in final_builder.AIR for pos in delta):
        raise AssertionError("OWS-009 Pass-19 no longer consists only of additions")
    if final_builder._count(accepted, "create:andesite_casing") != 0:
        raise AssertionError("OWS-009 accepted D3 unexpectedly contains required casing")
    metrics = generation.base.fidelity_metrics(final)
    lint = generation.base.assess_fidelity(SPEC.source_profile, final)
    if not lint["structural_lint_passed"] or lint["issues"]:
        raise AssertionError(f"OWS-009 final builder lint failed: {lint}")
    return {
        "accepted_d3_named_delta_positions": len(delta),
        "accepted_d3_named_additions": len(delta),
        "accepted_d3_named_replacements": 0,
        "pass19_delta_positions": [list(pos) for pos in sorted(delta)],
        "structural_metrics": metrics,
        "structural_lint": lint,
    }


def _assert_shipping_contracts(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str]) -> dict[str, object]:
    if tuple(size) != final_builder.SIZE:
        raise AssertionError(f"OWS-009 shipping dimensions changed: {size}")
    if any(not (0 <= x < 49 and 0 <= y < 18 and 0 <= z < 41) for x, y, z in blocks):
        raise AssertionError("OWS-009 shipping exceeds accepted bounds")
    if blocks.get(final_builder.PROOF_POS) != "minecraft:chest":
        raise AssertionError("OWS-009 shipping proof position changed")
    for pos in final_builder.SPAWNERS:
        if blocks.get(pos) != "minecraft:spawner": raise AssertionError(f"OWS-009 shipping encounter missing at {pos}")
    if sum(name == "minecraft:spawner" for name in blocks.values()) != len(final_builder.SPAWNERS):
        raise AssertionError("OWS-009 shipping encounter topology changed")
    for pos, expected in final_builder.PASS19_MICRODETAIL.items():
        if blocks.get(pos) != expected: raise AssertionError(f"OWS-009 shipping Pass-19 detail missing at {pos}")
    if sum(name == "create:andesite_casing" for name in blocks.values()) != 1:
        raise AssertionError("OWS-009 shipping must contain exactly one required andesite casing")
    missing_required = [name for name in final_builder.PRODUCTION_REQUIRED_BLOCKS if name not in blocks.values()]
    if missing_required: raise AssertionError(f"OWS-009 shipping required blocks missing: {missing_required}")

    blocked: dict[str, dict[str, str | None]] = {}
    checked = 0
    for low, high, label in ROUTE_REGIONS:
        failures = {}
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                for z in range(low[2], high[2] + 1):
                    checked += 1
                    pos = (x, y, z)
                    name = blocks.get(pos)
                    if name not in AIR | {"minecraft:iron_door"}: failures[str(pos)] = name
        if failures: blocked[label] = failures
    if blocked: raise AssertionError(f"OWS-009 protected shipping routes obstructed: {blocked}")

    return {
        "dimensions": list(size),
        "positions_in_bounds": True,
        "pass19_microdetail": {str(pos): blocks[pos] for pos in final_builder.PASS19_MICRODETAIL},
        "pass19_positions_verified": len(final_builder.PASS19_MICRODETAIL),
        "sole_required_casing_position": [34, 2, 28],
        "serialized_andesite_casing_count": 1,
        "canonical_proof_position": list(final_builder.PROOF_POS),
        "canonical_proof_nodes": 1,
        "spawner_positions": [list(pos) for pos in final_builder.SPAWNERS],
        "deterministic_spawners": len(final_builder.SPAWNERS),
        "protected_route_regions": [label for _, _, label in ROUTE_REGIONS],
        "protected_route_cells_checked": checked,
        "protected_routes_clear": True,
        "required_block_counts": {
            name: sum(block == name for block in blocks.values())
            for name in final_builder.PRODUCTION_REQUIRED_BLOCKS
        },
    }


def _render_fixed_cutaway(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str], manifest: dict[str, object]) -> None:
    cut_path = OUTPUT_DIR / "interior_cutaway.png"
    cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= FIXED_CUTAWAY_Y}
    isometric(
        size, cutaway_blocks, False,
        f"{TARGET} — gate_d_final — D3 authoritative shipping + Pass-19 — interior cutaway Y<={FIXED_CUTAWAY_Y}",
    ).save(cut_path)
    contact_views = [
        (view, OUTPUT_DIR / f"{view}.png")
        for view in ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
    ]
    contact_sheet(
        contact_views, OUTPUT_DIR / "contact_sheet.png", target=TARGET, gate="gate_d_final",
        revision=str(manifest["revision"]), damage_state=str(manifest["damage_state"]),
        dimensions=size, camera_set="ows009_fixed_v1",
    )
    manifest["cutaway_y"] = FIXED_CUTAWAY_Y


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != TARGET: raise AssertionError(f"OWS-009 is not active: {state.get('active_target')}")
    if state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("status") != "passed_r1":
        raise AssertionError("OWS-009 Gate C r1 is not passed")

    sync = _sync()
    delta = _assert_pass19_delta()
    size, blocks = unpack_structure(SHIPPING_NBT)
    mechanics = _assert_shipping_contracts(size, blocks)
    shipping_raw = gzip.decompress(SHIPPING_NBT.read_bytes())
    proof_refs = shipping_raw.count(final_builder.PROOF_LOOT_TABLE.encode())
    if proof_refs != 1: raise AssertionError(f"OWS-009 shipping requires one proof loot-table reference; found {proof_refs}")

    head = _git_head(); revision = f"gate-d-r1@{head[:8]}"
    manifest = render_review_set(
        target=TARGET, gate="gate_d_final", revision=revision,
        damage_state="D3 authoritative stabilized shipping state + Pass-19 microdetail",
        source_commit=head, source_path=str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        size=size, blocks=blocks, output_dir=OUTPUT_DIR, camera_set="ows009_fixed_v1",
    )
    _render_fixed_cutaway(size, blocks, manifest)

    sync_record = {
        "target": TARGET, "gate": "gate_d_final", "revision": revision,
        "spec_name": SPEC.name,
        "authoritative_dispatch": "generate_old_world_narrative_structures.BUILDERS['OWS-009']",
        "authoritative_builder": "old_world_ows009_final.build_009",
        "accepted_gate_c_d3_sha256": final_builder.ACCEPTED_GATE_C_D3_SHA256,
        "production_door_stabilization_applied": True,
        "shipping_nbt": str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        **sync, **delta, **mechanics,
        "canonical_proof_loot_table": final_builder.PROOF_LOOT_TABLE,
        "canonical_proof_loot_table_references": proof_refs,
        "render_source": "shipping_nbt", "fixed_camera_set": "ows009_fixed_v1",
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
        "exact_serialized_nbt_match": True, "exact_decompressed_nbt_match": True,
        "pass19_positions_verified": len(final_builder.PASS19_MICRODETAIL),
        "serialized_andesite_casing_count": 1,
        "canonical_proof_nodes": 1, "deterministic_spawners": len(final_builder.SPAWNERS),
        "protected_routes_clear": True, "required_blocks_verified": True,
        "structural_lint_passed": True,
        "visual_review_status": "rendered_pending_independent_review",
    })
    (OUTPUT_DIR / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"OWS-009 Gate-D r1 rendered from shipping NBT: {sync['shipping_nbt_sha256']}")


if __name__ == "__main__":
    main()

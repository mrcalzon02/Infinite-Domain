#!/usr/bin/env python3
"""Prepare OWS-007 Gate-D r1 from the actual authoritative shipping NBT.

This target-local tool writes review artifacts only. It never updates shared
state, dispatch, registries, shipping structures or gate decisions.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_old_world_narrative_structures as generation
import old_world_ows007_final as final_builder
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


TARGET = "OWS-007"
EXPECTED_SHIPPING_SHA256 = "0ef9d164449226a53c766a96ead39b0df4d454e369c545974b4d5bbb2acb3436"
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_d_final" / "r1"
SPEC = generation.BY_TARGET[TARGET]
SHIPPING_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / "old_world" / f"{SPEC.name}.nbt"
TEMP_NAME = "old_world/_heavy_review_ows007_gate_d_sync_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / "old_world" / "_heavy_review_ows007_gate_d_sync_r1.nbt"
MYCELIUM_POS = (61, 1, 42)
STABILIZED_DOOR_POS = (23, 2, 45)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sync() -> dict[str, object]:
    if generation.BUILDERS.get(TARGET) is not final_builder.build_007:
        raise AssertionError("OWS-007 production dispatch is not old_world_ows007_final.build_007")
    probe = (
        "import sys;sys.path.insert(0,'scripts');"
        "import generate_old_world_narrative_structures as g,old_world_ows007_final as f;"
        "assert g.BUILDERS['OWS-007'] is f.build_007;"
        "t=g.BUILDERS['OWS-007']();g.base.stabilize_door_pairs(t);f._assert_final_contracts(t);"
        f"t.save({TEMP_NAME!r})"
    )
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
    subprocess.run([str(production_python), "-c", probe], cwd=ROOT, check=True)
    try:
        built_bytes = TEMP_NBT.read_bytes()
        shipping_bytes = SHIPPING_NBT.read_bytes()
        built_raw = gzip.decompress(built_bytes)
        shipping_raw = gzip.decompress(shipping_bytes)
        if built_bytes != shipping_bytes or built_raw != shipping_raw:
            raise AssertionError(
                "OWS-007 stabilized builder/shipping mismatch: "
                f"builder={_sha(built_bytes)} shipping={_sha(shipping_bytes)}"
            )
        shipping_hash = _sha(shipping_bytes)
        if shipping_hash != EXPECTED_SHIPPING_SHA256:
            raise AssertionError(f"OWS-007 shipping hash drift: {shipping_hash} != {EXPECTED_SHIPPING_SHA256}")
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


def _assert_shipping_contracts(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str]) -> None:
    if tuple(size) != (73, 33, 63):
        raise AssertionError(f"OWS-007 shipping dimensions changed: {size}")
    if blocks.get(MYCELIUM_POS) != "minecraft:mycelium":
        raise AssertionError(f"OWS-007 shipping mycelium correction missing at {MYCELIUM_POS}")
    if blocks.get(STABILIZED_DOOR_POS) != "minecraft:iron_door":
        raise AssertionError(f"OWS-007 stabilized rear door missing at {STABILIZED_DOOR_POS}")
    if blocks.get(final_builder.PROOF_POS) != "minecraft:chest":
        raise AssertionError("OWS-007 shipping proof chest position changed")
    if sum(name == "minecraft:spawner" for name in blocks.values()) != 3:
        raise AssertionError("OWS-007 shipping encounter topology changed")
    for pos, expected in final_builder.PASS19_MICRODETAIL.items():
        if blocks.get(pos) != expected:
            raise AssertionError(f"OWS-007 shipping Pass-19 detail missing at {pos}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != TARGET:
        raise AssertionError(f"OWS-007 is not active: {state.get('active_target')}")
    if state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("status") != "passed_r1":
        raise AssertionError("OWS-007 Gate C r1 is not passed")

    sync = _sync()
    size, blocks = unpack_structure(SHIPPING_NBT)
    _assert_shipping_contracts(size, blocks)
    shipping_raw = gzip.decompress(SHIPPING_NBT.read_bytes())
    if shipping_raw.count(final_builder.PROOF_LOOT_TABLE.encode()) != 1:
        raise AssertionError("OWS-007 shipping NBT does not contain exactly one canonical proof loot-table reference")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    manifest = render_review_set(
        target=TARGET,
        gate="gate_d_final",
        revision=f"gate-d-r1@{revision}",
        damage_state="D3 authoritative stabilized shipping state + Pass-19 microdetail",
        source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
        source_path=str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        size=size,
        blocks=blocks,
        output_dir=OUTPUT_DIR,
        camera_set="ows007_fixed_v1",
    )

    sync_record = {
        "target": TARGET,
        "gate": "gate_d_final",
        "revision": f"gate-d-r1@{revision}",
        "spec_name": SPEC.name,
        "authoritative_dispatch": "generate_old_world_narrative_structures.BUILDERS['OWS-007']",
        "authoritative_builder": "old_world_ows007_final.build_007",
        "accepted_gate_c_d3_sha256": final_builder.ACCEPTED_GATE_C_D3_SHA256,
        "production_door_stabilization_applied": True,
        "stabilized_door_half_positions": [list(STABILIZED_DOOR_POS)],
        "required_mycelium_position": list(MYCELIUM_POS),
        "required_mycelium_verified": True,
        "canonical_proof_position": list(final_builder.PROOF_POS),
        "canonical_proof_loot_table": final_builder.PROOF_LOOT_TABLE,
        "canonical_proof_nodes": 1,
        "deterministic_spawners": 3,
        "shipping_nbt": str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        **sync,
        "render_source": "shipping_nbt",
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
        "production_door_stabilization_applied": True,
        "required_mycelium_verified": True,
        "visual_review_status": "rendered_pending_independent_review",
    })
    (OUTPUT_DIR / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"OWS-007 Gate-D r1 candidate rendered from shipping NBT: {sync['shipping_nbt_sha256']}")


if __name__ == "__main__":
    main()

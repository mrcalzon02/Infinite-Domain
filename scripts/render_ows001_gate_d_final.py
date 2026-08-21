#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-001 Gate-D final authoritative review.

Gate D is deliberately coupled to the production generation dispatch. It builds
OWS-001 through old_world_narrative_core.BUILDERS, applies the same door-pair
stabilization used by production generation, serializes a temporary NBT with the
same Template.save path, and requires the decompressed temporary NBT bytes to
match the shipping OWS-001 NBT exactly before rendering.

The final review is then rendered from the shipping NBT itself. This makes an
out-of-sync pretty review model mechanically impossible to approve.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path

import old_world_narrative_core as core
import old_world_ows001_final as final_builder
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_d_final" / "r1"
SHIPPING_NBT = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_001_vcf_neighborhood_culture_service_depot.nbt"
)
TEMP_NAME = "old_world/_heavy_review_ows001_gate_d_sync_r1"
TEMP_NBT = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "_heavy_review_ows001_gate_d_sync_r1.nbt"
)


def _raw_nbt(path: Path) -> bytes:
    if not path.is_file():
        raise AssertionError(f"required NBT does not exist: {path}")
    return gzip.decompress(path.read_bytes())


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _assert_authoritative_dispatch() -> None:
    dispatched = core.BUILDERS.get("OWS-001")
    if dispatched is not final_builder.build_001:
        raise AssertionError(
            "OWS-001 authoritative dispatch no longer points directly to "
            "old_world_ows001_final.build_001"
        )


def _serialize_authoritative_builder() -> tuple[str, str, int]:
    """Serialize production-dispatch geometry exactly as core.generate does."""
    _assert_authoritative_dispatch()
    template = core.BUILDERS["OWS-001"]()
    core.base.stabilize_door_pairs(template)
    template.save(TEMP_NAME)
    try:
        generated_raw = _raw_nbt(TEMP_NBT)
        shipping_raw = _raw_nbt(SHIPPING_NBT)
        if generated_raw != shipping_raw:
            raise AssertionError(
                "OWS-001 synchronization failure: authoritative builder serialization "
                "does not exactly match shipping NBT. Regenerate production structures "
                "before Gate D may proceed. "
                f"builder_sha256={_sha256(generated_raw)} "
                f"shipping_sha256={_sha256(shipping_raw)}"
            )
        return _sha256(generated_raw), _sha256(shipping_raw), len(generated_raw)
    finally:
        TEMP_NBT.unlink(missing_ok=True)


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-001":
        print(f"Gate-D OWS-001 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_d_final_multi_angle", {})
    status = gate.get("status", "not_started")
    allowed = {
        "blocked_by_micro_detail_and_authoritative_sync",
        "ready_to_render",
        "ready_to_render_authoritative_sync_required",
        "rerender_required",
    }
    if status not in allowed:
        print(f"Gate-D OWS-001 renderer skipped: status={status}")
        return

    builder_hash, shipping_hash, raw_size = _serialize_authoritative_builder()

    # Render the shipping artifact, not the in-memory review template.
    size, blocks = unpack_structure(SHIPPING_NBT)
    if tuple(size) != (39, 13, 33):
        raise AssertionError(f"OWS-001 final shipping dimensions changed unexpectedly: {size}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows001_fixed_v1")
    manifest = render_review_set(
        target="OWS-001",
        gate="gate_d_final",
        revision=f"gate-d-r1@{revision}",
        damage_state="D3 authoritative worldgen state",
        source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
        source_path=str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        size=size,
        blocks=blocks,
        output_dir=OUTPUT_DIR,
        camera_set=camera_set,
    )

    sync_record = {
        "target": "OWS-001",
        "gate": "gate_d_final",
        "revision": f"gate-d-r1@{revision}",
        "authoritative_dispatch": "old_world_narrative_core.BUILDERS['OWS-001']",
        "authoritative_builder": "old_world_ows001_final.build_001",
        "production_door_stabilization_applied": True,
        "shipping_nbt": str(SHIPPING_NBT.relative_to(ROOT)).replace("\\", "/"),
        "decompressed_nbt_bytes": raw_size,
        "builder_serialization_sha256": builder_hash,
        "shipping_nbt_sha256": shipping_hash,
        "exact_decompressed_nbt_match": builder_hash == shipping_hash,
        "render_source": "shipping_nbt",
        "review_manifest": str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "final_preview_synchronized_with_authoritative_nbt": True,
    }
    sync_path = OUTPUT_DIR / "authoritative_sync.json"
    sync_path.write_text(json.dumps(sync_record, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Preserve the renderer's own synchronization assertion in the manifest too.
    manifest["authoritative_sync_record"] = str(sync_path.relative_to(ROOT)).replace("\\", "/")
    manifest["authoritative_builder_sha256"] = builder_hash
    manifest["shipping_nbt_sha256"] = shipping_hash
    manifest["exact_authoritative_nbt_match"] = True
    (OUTPUT_DIR / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    state["active_status"] = "gate_d_r1_rendered_authoritative_sync_verified_pending_review"
    state["active_target_passes"]["micro_detail"] = "complete"
    state["active_target_passes"]["visual_gate_d_final_multi_angle"] = (
        "r1_rendered_authoritative_sync_verified_pending_manual_review"
    )
    gate["status"] = "r1_rendered_authoritative_sync_verified_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["r1_authoritative_sync"] = str(sync_path.relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows001_gate_d_final.py"
    gate["review_only"] = False
    gate["render_source"] = "shipping_nbt"
    gate["exact_authoritative_nbt_match"] = True
    gate["shipping_nbt_sha256"] = shipping_hash
    state["visual_review_gates"]["gate_d_final_multi_angle"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        "OWS-001 Gate-D r1 rendered from shipping NBT after exact authoritative "
        f"serialization match: sha256={shipping_hash}, size={size}."
    )


if __name__ == "__main__":
    main()

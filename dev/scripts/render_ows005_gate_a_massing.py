#!/usr/bin/env python3
"""Render the review-only OWS-005 Gate-A r1 massing candidate."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from old_world_ows005_geometry import build_gate_a_massing


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
TEMP_NAME = "_heavy_review_ows005_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-005" / "gate_a_massing" / "r1"


def main() -> None:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    t = build_gate_a_massing()
    if tuple(t.size) != (59, 24, 51):
        raise AssertionError(f"OWS-005 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 15000:
        raise AssertionError("Gate-A r1 massing is unexpectedly sparse")

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-005",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows005_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows005_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["authoritative_shipping_modified"] = False
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-005 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()



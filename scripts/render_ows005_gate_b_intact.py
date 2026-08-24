#!/usr/bin/env python3
"""Render the OWS-005 Gate-B r1 intact operating candidate."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from old_world_ows005_geometry import build_gate_b_intact, _assert_intact_contracts


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
TEMP_NAME = "_heavy_review_ows005_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-005" / "gate_b_intact" / "r1"


def main() -> None:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    if len(t.blocks) < 18000:
        raise AssertionError("Gate-B r1 intact model is unexpectedly sparse")

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-005",
            gate="gate_b_intact",
            revision=f"intact-r1@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows005_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows005_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["gate_a_model_sha256"] = "9f4ba26a30f5632acc5480535cb0477ab20ed56e9e96f6725f4eded7184d6402"
        manifest["placed_positions"] = len(blocks)
        manifest["gate_a_frozen_aspects_asserted"] = 8
        manifest["gate_b_obligations_implemented"] = 6
        manifest["proof_encounters_damage_present"] = False
        manifest["authoritative_shipping_modified"] = False
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-005 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()



#!/usr/bin/env python3
"""Render the frozen OWS-005 pre-heavy-rebuild baseline without shared-state writes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from render_old_world_heavy_rebuild_review import (
    ROOT,
    extract_historical_nbt,
    render_review_set,
)
from render_structure_review import unpack_structure


TARGET = "OWS-005"
BASELINE_COMMIT = "d2cdec5739d8d2c1423973f6ed7c59ee59224789"
SOURCE_PATH = (
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_005_vcf_harvest_packaging_annex.nbt"
)
OUTPUT_DIR = (
    ROOT
    / "old_world_narrative"
    / "reviews"
    / "heavy_rebuild"
    / "visual"
    / TARGET
    / "baseline"
    / "r0_pre_heavy_rebuild"
)


def main() -> None:
    baseline_file = extract_historical_nbt(BASELINE_COMMIT, SOURCE_PATH)
    try:
        baseline_bytes = baseline_file.read_bytes()
        size, blocks = unpack_structure(baseline_file)
    finally:
        baseline_file.unlink(missing_ok=True)

    manifest = render_review_set(
        target=TARGET,
        gate="baseline",
        revision=f"pre-heavy-rebuild@{BASELINE_COMMIT[:8]}",
        damage_state="historical rough implementation",
        source_commit=BASELINE_COMMIT,
        source_path=SOURCE_PATH,
        size=size,
        blocks=blocks,
        output_dir=OUTPUT_DIR,
        camera_set="ows005_fixed_v1",
    )

    live_path = ROOT / SOURCE_PATH
    baseline_sha256 = hashlib.sha256(baseline_bytes).hexdigest()
    live_sha256 = hashlib.sha256(live_path.read_bytes()).hexdigest()
    manifest["baseline_nbt_sha256"] = baseline_sha256
    manifest["live_nbt_sha256_at_render"] = live_sha256
    manifest["live_matches_frozen_baseline"] = live_sha256 == baseline_sha256
    manifest_path = OUTPUT_DIR / "review_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered {TARGET} baseline {size[0]}x{size[1]}x{size[2]}; "
        f"live_matches_frozen_baseline={live_sha256 == baseline_sha256}; "
        "visual approval remains pending."
    )


if __name__ == "__main__":
    main()

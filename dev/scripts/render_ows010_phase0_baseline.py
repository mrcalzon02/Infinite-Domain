#!/usr/bin/env python3
"""Render the frozen untouched OWS-010 Phase-0 shipping baseline."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dev/scripts"))

from render_old_world_heavy_rebuild_review import extract_historical_nbt, render_review_set  # noqa: E402
from render_structure_review import unpack_structure  # noqa: E402


TARGET = "OWS-010"
BASELINE_COMMIT = "e14b3f35306fc313e7ea9a114f2384696864533a"
SOURCE_PATH = (
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_010_atlas_conveyor_transfer_hall.nbt"
)
CAMERA_SET = "ows010_fixed_v1"
OUTPUT_DIR = (
    ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
    / TARGET / "baseline" / "r0_pre_heavy_rebuild"
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    source = ROOT / SOURCE_PATH
    live_blob = _git("hash-object", SOURCE_PATH)
    baseline_blob = _git("rev-parse", f"{BASELINE_COMMIT}:{SOURCE_PATH}")
    if live_blob != baseline_blob:
        raise AssertionError(
            "OWS-010 live shipping NBT no longer matches the frozen baseline; "
            "coordinator disposition is required"
        )

    baseline_file = extract_historical_nbt(BASELINE_COMMIT, SOURCE_PATH)
    try:
        frozen_bytes = baseline_file.read_bytes()
        if frozen_bytes != source.read_bytes():
            raise AssertionError("OWS-010 extracted baseline differs from live shipping bytes")
        size, blocks = unpack_structure(baseline_file)
    finally:
        baseline_file.unlink(missing_ok=True)

    manifest = render_review_set(
        target=TARGET,
        gate="baseline",
        revision=f"pre-heavy-rebuild@{BASELINE_COMMIT[:8]}",
        damage_state="untouched pre-heavy-rebuild shipping implementation",
        source_commit=BASELINE_COMMIT,
        source_path=SOURCE_PATH,
        size=size,
        blocks=blocks,
        output_dir=OUTPUT_DIR,
        camera_set=CAMERA_SET,
    )
    manifest.update({
        "source_sha256": hashlib.sha256(frozen_bytes).hexdigest(),
        "source_git_blob": baseline_blob,
        "live_shipping_exact_baseline_match": True,
        "visual_review_status": "rendered_pending_independent_review",
        "authoritative_shipping_modified": False,
    })
    (OUTPUT_DIR / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Rendered {TARGET} untouched baseline at {manifest['dimensions']} from "
        f"{baseline_blob}; independent Phase-0 review remains required."
    )


if __name__ == "__main__":
    main()

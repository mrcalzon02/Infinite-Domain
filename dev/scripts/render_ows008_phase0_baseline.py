#!/usr/bin/env python3
"""Render the frozen OWS-008 Phase-0 baseline without mutating shared state."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_old_world_heavy_rebuild_review import (  # noqa: E402
    extract_historical_nbt,
    render_review_set,
)
from render_structure_review import unpack_structure  # noqa: E402


TARGET = "OWS-008"
BASELINE_COMMIT = "e14b3f35306fc313e7ea9a114f2384696864533a"
SOURCE_PATH = (
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
CAMERA_SET = "ows008_fixed_v1"
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


def git_blob(spec: str, *, live_file: bool = False) -> str:
    command = ["git", "hash-object", spec] if live_file else ["git", "rev-parse", spec]
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    live_blob = git_blob(SOURCE_PATH, live_file=True)
    baseline_blob = git_blob(f"{BASELINE_COMMIT}:{SOURCE_PATH}")
    if live_blob != baseline_blob:
        raise AssertionError(
            "OWS-008 live shipping NBT no longer matches the frozen baseline; "
            "coordinator review is required before replacing the Phase-0 artifact"
        )

    baseline_file = extract_historical_nbt(BASELINE_COMMIT, SOURCE_PATH)
    try:
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
        camera_set=CAMERA_SET,
    )
    print(
        f"Rendered {TARGET} baseline at {manifest['dimensions']} from frozen blob "
        f"{baseline_blob}; visual gate approval remains unresolved."
    )


if __name__ == "__main__":
    main()

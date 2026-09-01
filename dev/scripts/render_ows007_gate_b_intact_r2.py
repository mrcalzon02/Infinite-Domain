#!/usr/bin/env python3
"""Render the narrowly corrected OWS-007 Gate-B r2 intact candidate.

R2 changes only the exterior plane of the accepted west cyan observation
facade. It adds room-aligned white mullions and one continuous concrete beam;
all r1 geometry, bounds, rooms, routes and operating systems remain frozen.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows007_gate_b_intact import build_gate_b_intact as build_gate_b_r1
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows007_gate_b_intact_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-007" / "gate_b_intact" / "r2"
SHIPPING_PATH = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" /
    "old_world" / "ows_007_vcf_ep7_agricultural_development_laboratory.nbt"
)
GATE_B_R1_MODEL_SHA256 = "2fa7e4c458f7ba33607dceb9273773e2c27edcc8b3fc73af4ff45966c81bbdd2"
MULLION_Z = (22, 30, 38, 46, 48)
MULLION_Y = range(4, 20)
BEAM_Y = 11
BEAM_Z = range(22, 49)


def _name_at(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _facade_frame_positions() -> set[tuple[int, int, int]]:
    return {
        *((1, y, z) for z in MULLION_Z for y in MULLION_Y),
        *((1, BEAM_Y, z) for z in BEAM_Z),
    }


def build_gate_b_intact_r2() -> base.Template:
    t = build_gate_b_r1()
    for z in MULLION_Z:
        t.fill((1, 4, z), (1, 19, z), "minecraft:white_concrete")
    t.fill((1, BEAM_Y, 22), (1, BEAM_Y, 48), "minecraft:light_gray_concrete")
    return t


def _assert_r2_scope(r1: base.Template, r2: base.Template) -> None:
    if tuple(r2.size) != (73, 33, 63) or tuple(r2.size) != tuple(r1.size):
        raise AssertionError(f"OWS-007 Gate-B r2 bounds changed: r1={r1.size}, r2={r2.size}")

    all_positions = set(r1.blocks) | set(r2.blocks)
    changed = {pos for pos in all_positions if _name_at(r1, pos) != _name_at(r2, pos)}
    expected = _facade_frame_positions()
    if changed != expected:
        missing = sorted(expected - changed)
        extra = sorted(changed - expected)
        raise AssertionError(f"R2 scope drift: missing={missing[:8]}, extra={extra[:8]}")

    for pos in expected:
        before = _name_at(r1, pos)
        after = _name_at(r2, pos)
        if before != "create:framed_glass":
            raise AssertionError(f"R2 correction does not replace facade glass at {pos}: {before}")
        expected_after = "minecraft:light_gray_concrete" if pos[1] == BEAM_Y else "minecraft:white_concrete"
        if after != expected_after:
            raise AssertionError(f"R2 facade frame missing at {pos}: {after} != {expected_after}")

    # The correction is strictly on the exterior-visible x=1 facade plane.
    if any(x != 1 or not (4 <= y <= 19) or not (22 <= z <= 48) for x, y, z in changed):
        raise AssertionError("R2 changed geometry outside the approved facade plane")


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def main() -> None:
    shipping_before = git_hash_object(SHIPPING_PATH)
    r1 = build_gate_b_r1()
    r2 = build_gate_b_intact_r2()
    _assert_r2_scope(r1, r2)

    r2.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-007", gate="gate_b_intact", revision=f"intact-r2@{revision}",
            damage_state="D0 intact / operational", source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows007_gate_b_intact_r2.build_gate_b_intact_r2()",
            size=size, blocks=blocks, output_dir=OUTPUT_DIR, camera_set="ows007_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["gate_b_r1_model_sha256"] = GATE_B_R1_MODEL_SHA256
        manifest["placed_positions"] = len(blocks)
        manifest["r2_changed_positions"] = len(_facade_frame_positions())
        manifest["r2_scope"] = "x=1 facade plane only; white vertical mullions plus one light-gray horizontal beam"
        manifest["accepted_r1_aspects_preserved"] = 12
        manifest["proof_encounters_damage_present"] = False
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-007 shipping NBT changed during r2 rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-007 Gate B r2 at {manifest['dimensions']} with "
        f"{manifest['r2_changed_positions']} facade-only changes; visual decision remains pending."
    )


if __name__ == "__main__":
    main()

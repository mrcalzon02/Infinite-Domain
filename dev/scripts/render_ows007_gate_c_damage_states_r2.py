#!/usr/bin/env python3
"""Render the narrow OWS-007 Gate-C r2 correction.

R2 freezes D0 and D1 exactly, changes one detached D3 crown fragment to air,
and renders every state's interior cutaway at the same Y<=8 plane. It never
writes shipping NBT, shared state, registries, common renderers, or gate review.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure
from render_ows007_gate_c_damage_states import (
    ACCEPTED_GATE_B_SHA256,
    PROOF_LOOT_TABLE,
    PROOF_POS,
    ROOT,
    SHIPPING_PATH,
    _assert_d3_contracts,
    _diff_count,
    _name,
    build_d0 as build_d0_r1,
    build_d1 as build_d1_r1,
    build_d3 as build_d3_r1,
    git_hash_object,
)


OUTPUT_DIR = (
    ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" /
    "OWS-007" / "gate_c_damage_states" / "r2"
)
R1_GATE_MANIFEST = (
    ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" /
    "OWS-007" / "gate_c_damage_states" / "r1" / "gate_c_manifest.json"
)
R1_CANDIDATE = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-007_GATE_C_R1_CANDIDATE.md"
R1_D0_SHA256 = "b116ad94acd595414ca670d4f5205bed69e4116724167a6397a8504acb0ba67a"
R1_D1_SHA256 = "7bb865d6d06682dca0b986234c639cc859c7c15be47cd342215b21f3e2ef952f"
R1_D3_SHA256 = "6d6e1743219299d34e23a3f385f597bff1b26c679490c8b43d31f4f82911cef4"
DETACHED_FRAGMENT = (70, 22, 35)
COMMON_CUTAWAY_Y = 8
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _assert_r1_provenance() -> None:
    if not R1_CANDIDATE.exists() or not R1_GATE_MANIFEST.exists():
        raise AssertionError("Gate-C r2 refused: persisted r1 candidate provenance is missing")
    r1 = json.loads(R1_GATE_MANIFEST.read_text(encoding="utf-8"))
    expected = {
        "d0_review_model_sha256": R1_D0_SHA256,
        "d1_review_model_sha256": R1_D1_SHA256,
        "d3_review_model_sha256": R1_D3_SHA256,
    }
    for key, value in expected.items():
        if r1.get(key) != value:
            raise AssertionError(f"Gate-C r1 provenance drifted at {key}: {r1.get(key)} != {value}")


def build_d0() -> base.Template:
    return build_d0_r1()


def build_d1() -> base.Template:
    return build_d1_r1()


def build_d3() -> base.Template:
    r1 = build_d3_r1()
    if _name(r1, DETACHED_FRAGMENT) != "minecraft:white_concrete":
        raise AssertionError(
            f"Expected detached r1 crown fragment at {DETACHED_FRAGMENT}; found {_name(r1, DETACHED_FRAGMENT)}"
        )
    r2 = build_d3_r1()
    r2.set(*DETACHED_FRAGMENT, "minecraft:air")

    all_positions = set(r1.blocks) | set(r2.blocks)
    changed = {pos for pos in all_positions if _name(r1, pos) != _name(r2, pos)}
    if changed != {DETACHED_FRAGMENT}:
        raise AssertionError(f"Gate-C r2 exceeded one-position scope: {sorted(changed)}")
    if _name(r2, DETACHED_FRAGMENT) not in AIR:
        raise AssertionError("Detached rotunda crown fragment was not removed")

    _assert_d3_contracts(r2)
    return r2


def _sha_for_template(label: str, t: base.Template) -> str:
    temp_name = f"_heavy_review_ows007_gate_c_r2_hash_{label}"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)


def _rewrite_common_cutaway(
    manifest: dict,
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    output_dir: Path,
    revision: str,
    damage_state: str,
) -> None:
    cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= COMMON_CUTAWAY_Y}
    cut_path = output_dir / "interior_cutaway.png"
    isometric(
        size,
        cutaway_blocks,
        False,
        f"OWS-007 — gate_c_damage_states — interior cutaway Y<={COMMON_CUTAWAY_Y}",
    ).save(cut_path)
    manifest["cutaway_y"] = COMMON_CUTAWAY_Y
    manifest["common_gate_cutaway_y"] = COMMON_CUTAWAY_Y

    views = [
        ("front_left", output_dir / "front_left.png"),
        ("rear_left", output_dir / "rear_left.png"),
        ("rear_right", output_dir / "rear_right.png"),
        ("front_right", output_dir / "front_right.png"),
        ("roof_top_oblique", output_dir / "roof_top_oblique.png"),
        ("interior_cutaway", cut_path),
    ]
    contact_sheet(
        views,
        output_dir / "contact_sheet.png",
        target="OWS-007",
        gate="gate_c_damage_states",
        revision=revision,
        damage_state=damage_state,
        dimensions=size,
        camera_set="ows007_fixed_v1",
    )
    (output_dir / "review_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str) -> tuple[dict, str]:
    temp_name = f"_heavy_review_ows007_gate_c_{label}_r2"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    output_dir = OUTPUT_DIR / label
    try:
        model_bytes = temp_nbt.read_bytes()
        model_sha = hashlib.sha256(model_bytes).hexdigest()
        size, blocks = unpack_structure(temp_nbt)
        manifest = render_review_set(
            target="OWS-007",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows007_gate_c_damage_states_r2.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=output_dir,
            camera_set="ows007_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = model_sha
        _rewrite_common_cutaway(manifest, size, blocks, output_dir, revision, damage_state)
        return manifest, model_sha
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison(manifests: dict[str, dict], output: Path) -> None:
    from PIL import Image, ImageDraw

    states = ("D0", "D1", "D3")
    views = ("front_left", "rear_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w = 390
    margin = 16
    header_h = 88
    label_h = 24
    loaded: dict[tuple[str, str], Image.Image] = {}
    row_heights: list[int] = []
    for view in views:
        row_images = []
        for state in states:
            path = ROOT / manifests[state]["views"][view]
            image = Image.open(path).convert("RGB")
            ratio = thumb_w / max(1, image.width)
            image = image.resize((thumb_w, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
            loaded[(state, view)] = image
            row_images.append(image)
        row_heights.append(max(image.height for image in row_images) + label_h)

    sheet_w = margin * 4 + thumb_w * 3
    sheet_h = header_h + sum(row_heights) + margin * (len(views) + 1)
    sheet = Image.new("RGB", (sheet_w, sheet_h), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), "OWS-007 — Gate C r2 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), "dimensions=73x33x63  camera_set=ows007_fixed_v1  common_cutaway=Y<=8", fill=(210, 210, 210))
    draw.text((margin, 58), "status=PENDING INDEPENDENT VISUAL REVIEW", fill=(225, 190, 84))
    y = header_h + margin
    for row, view in enumerate(views):
        for col, state in enumerate(states):
            x = margin + col * (thumb_w + margin)
            draw.text((x, y), f"{state} — {view}", fill=(235, 235, 235))
            sheet.paste(loaded[(state, view)], (x, y + label_h))
        y += row_heights[row] + margin
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    for image in loaded.values():
        image.close()


def main() -> None:
    _assert_r1_provenance()
    shipping_before = git_hash_object(SHIPPING_PATH)
    d0 = build_d0()
    d1 = build_d1()
    d3_r1 = build_d3_r1()
    d3 = build_d3()

    preflight_hashes = {
        "D0": _sha_for_template("d0", d0),
        "D1": _sha_for_template("d1", d1),
        "D3_R1": _sha_for_template("d3_r1", d3_r1),
        "D3": _sha_for_template("d3", d3),
    }
    expected_frozen = {"D0": R1_D0_SHA256, "D1": R1_D1_SHA256, "D3_R1": R1_D3_SHA256}
    for state, expected in expected_frozen.items():
        if preflight_hashes[state] != expected:
            raise AssertionError(f"OWS-007 Gate-C r2 froze {state} incorrectly: {preflight_hashes[state]} != {expected}")
    if _diff_count(d3_r1, d3) != 1:
        raise AssertionError("OWS-007 Gate-C r2 must change exactly one D3 position")

    revision = f"gate-c-r2@{os.environ.get('GITHUB_SHA', 'local')[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 accepted intact operation — frozen", d0, revision),
        "D1": _serialize_and_render("d1", "D1 commercial repeat validation — frozen", d1, revision),
        "D3": _serialize_and_render("d3", "D3 causal ruin — detached crown fragment removed", d3, revision),
    }
    manifests = {state: result[0] for state, result in rendered.items()}
    hashes = {state: result[1] for state, result in rendered.items()}
    if hashes["D0"] != R1_D0_SHA256 or hashes["D1"] != R1_D1_SHA256:
        raise AssertionError("OWS-007 Gate-C r2 rendered frozen D0/D1 incorrectly")
    if any(manifest.get("cutaway_y") != COMMON_CUTAWAY_Y for manifest in manifests.values()):
        raise AssertionError("OWS-007 Gate-C r2 did not use one common cutaway plane")

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    shipping_after = git_hash_object(SHIPPING_PATH)
    if shipping_after != shipping_before:
        raise AssertionError("OWS-007 shipping NBT changed during Gate-C r2 rendering")

    gate_manifest = {
        "target": "OWS-007",
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": "ows007_fixed_v1",
        "common_cutaway_y": COMMON_CUTAWAY_Y,
        "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d0_exact_r1_match": hashes["D0"] == R1_D0_SHA256,
        "d1_review_model_sha256": hashes["D1"],
        "d1_exact_r1_match": hashes["D1"] == R1_D1_SHA256,
        "rejected_r1_d3_review_model_sha256": R1_D3_SHA256,
        "d3_review_model_sha256": hashes["D3"],
        "r2_changed_positions_from_r1_d3": 1,
        "r2_changed_position": list(DETACHED_FRAGMENT),
        "r2_change": "minecraft:white_concrete -> minecraft:air",
        "frozen_r1_aspects_preserved": True,
        "d1_changed_positions_from_d0": _diff_count(d0, d1),
        "d3_changed_positions_from_d0": _diff_count(d0, d3),
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_pre_crisis_site_was_regionally_abandoned_without_a_distinct_site_specific_collapse_event",
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 4,
        "authoritative_shipping_modified": False,
        "shipping_nbt_git_blob_before": shipping_before,
        "shipping_nbt_git_blob_after": shipping_after,
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Rendered OWS-007 Gate C r2: D0/D1 frozen, one D3 fragment removed at {DETACHED_FRAGMENT}, "
        f"common cutaway Y<={COMMON_CUTAWAY_Y}; independent review pending."
    )


if __name__ == "__main__":
    main()

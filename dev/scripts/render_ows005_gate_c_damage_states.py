#!/usr/bin/env python3
"""Render OWS-005 Gate-C D0/D1/D3 states from pure production geometry."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import generate_wasteland_sites as base
from old_world_ows005_geometry import (
    ACCEPTED_GATE_B_SHA256,
    PROOF_LOOT_TABLE,
    PROOF_POS,
    _diff_count,
    build_d0,
    build_d1,
    build_d3,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-005" / "gate_c_damage_states" / "r1"
REQUIRED_DOCS = (
    "OWS-005_PASS13_HISTORICAL_LAYERING.md",
    "OWS-005_PASS14_ENVIRONMENTAL_NARRATIVE.md",
    "OWS-005_PASS15_ENCOUNTER_ARCHITECTURE.md",
    "OWS-005_PASS16_LOOT_ARCHITECTURE.md",
    "OWS-005_PASS17_QUEST_PROOF_ARCHITECTURE.md",
    "OWS-005_PASS18_DAMAGE_AND_DECAY.md",
)


def _assert_history_authorized() -> None:
    review_dir = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"
    review = review_dir / "OWS-005_GATE_B_R1_REVIEW.md"
    if not review.exists() or "OWS-005 GATE B r1: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-005 Gate-B r1 PASSED review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: required Pass 13-18 records are missing: {missing}")


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str) -> tuple[dict, str]:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    temp_name = f"_heavy_review_ows005_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        model_bytes = temp_nbt.read_bytes()
        model_sha = hashlib.sha256(model_bytes).hexdigest()
        size, blocks = unpack_structure(temp_nbt)
        manifest = render_review_set(
            target="OWS-005",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows005_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set="ows005_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = model_sha
        (OUTPUT_DIR / label / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        return manifest, model_sha
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison(manifests: dict[str, dict], output: Path) -> None:
    from PIL import Image, ImageDraw

    """Create a same-camera D0/D1/D3 comparison sheet for direct review."""
    states = ("D0", "D1", "D3")
    views = ("front_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w = 420
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
    draw.text((margin, 12), "OWS-005 — Gate C r1 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), "dimensions=59x24x51  camera_set=ows005_fixed_v1", fill=(210, 210, 210))
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
    _assert_history_authorized()
    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()
    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if d1_changes < 120:
        raise AssertionError(f"OWS-005 D1 intervention is too weak to review: {d1_changes}")
    if d3_changes < 420:
        raise AssertionError(f"OWS-005 D3 ruin is too weak to review: {d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"OWS-005 D3 must exceed twice the D1 change count: D1={d1_changes}, D3={d3_changes}")

    revision = f"gate-c-r1@{os.environ.get('GITHUB_SHA', 'local')[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 accepted intact operation", d0, revision),
        "D1": _serialize_and_render("d1", "D1 localized early-anomaly intervention", d1, revision),
        "D3": _serialize_and_render("d3", "D3 centuries-later causal ruin", d3, revision),
    }
    manifests = {state: result[0] for state, result in rendered.items()}
    state_hashes = {state: result[1] for state, result in rendered.items()}
    if state_hashes["D0"] != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(
            f"OWS-005 Gate-C D0 drifted from accepted Gate B: {state_hashes['D0']} != {ACCEPTED_GATE_B_SHA256}"
        )

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": "OWS-005",
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": "ows005_fixed_v1",
        "source_d0": "render_ows005_gate_b_intact.build_gate_b_intact",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": state_hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": state_hashes["D1"],
        "d3_review_model_sha256": state_hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_slow_quality_incident_abandonment_has_no_distinct_immediate_collapse_state",
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 3,
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Rendered OWS-005 Gate C r1: D0 exact={state_hashes['D0'] == ACCEPTED_GATE_B_SHA256}, "
        f"D1 changes={d1_changes}, D3 changes={d3_changes}; independent review remains pending."
    )


if __name__ == "__main__":
    main()



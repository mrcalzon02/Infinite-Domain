#!/usr/bin/env python3
"""[SYSTEM REPORT] Render OWS-002 Gate-C r2 with stronger causal D3 decay.

Gate-C r1 proved the D0/D1 chronology and all mechanical/proof contracts but was
rejected on visual review because the centuries-later D3 exterior remained too
close to the intact building. This review-only revision preserves D0 and D1
exactly and strengthens D3 only at plausible exposure/wet/service failure zones.
It does not alter authoritative shipping geometry.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image, ImageDraw

import generate_wasteland_sites as base
import render_ows002_gate_c_damage_states as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_c_damage_states" / "r2"


def build_d0() -> base.Template:
    return r1.build_d0()


def build_d1() -> base.Template:
    return r1.build_d1()


def build_d3() -> base.Template:
    """Strengthen only the centuries-later layer while preserving r1 contracts."""
    t = r1.build_d3()

    # ------------------------------------------------------------------
    # West/lower civic roof: broaden failure outward from the recorded plant leak.
    # Openings follow roof seams and the wet-service side; the public/north bar is
    # intentionally much better preserved.
    # ------------------------------------------------------------------
    t.clear((8, 11, 29), (11, 11, 32))
    t.clear((12, 11, 33), (14, 11, 35))
    t.clear((6, 11, 36), (8, 11, 39))
    t.fill((9, 10, 30), (12, 10, 33), "minecraft:mossy_stone_bricks")
    t.fill((13, 10, 34), (15, 10, 36), "minecraft:cracked_stone_bricks")

    # West exterior below the failed roof now carries visible wet-service damage.
    # Keep openings selective and aligned to the service wing rather than the
    # public entrance or records area.
    t.clear((4, 7, 31), (4, 9, 34))
    t.clear((4, 4, 36), (4, 6, 38))
    t.fill((4, 2, 30), (4, 3, 32), "minecraft:mossy_stone_bricks")
    t.fill((4, 2, 39), (4, 4, 40), "minecraft:cracked_stone_bricks")

    # ------------------------------------------------------------------
    # Grow-hall facades: limited bay-aligned masonry/clerestory loss. Structural
    # pilasters remain, so the clear-span rhythm and original hall are readable.
    # ------------------------------------------------------------------
    # East wall, between structural lines at z=18/23 and z=31/38.
    t.clear((46, 8, 19), (46, 10, 20))
    t.clear((46, 4, 33), (46, 6, 35))
    t.fill((46, 5, 19), (46, 7, 20), "minecraft:cracked_stone_bricks")
    t.fill((46, 3, 34), (46, 4, 35), "minecraft:mossy_stone_bricks")

    # West high wall above the lower civic roof.
    t.clear((22, 12, 19), (22, 14, 20))
    t.clear((22, 12, 33), (22, 13, 34))
    t.set(22, 14, 24, "minecraft:cracked_stone_bricks")
    t.set(22, 14, 35, "minecraft:mossy_stone_bricks")

    # South hall face: lose one upper clerestory section and weather one masonry
    # pocket, but retain the door pair and the main dispatch frame.
    t.clear((36, 8, 41), (37, 10, 41))
    t.clear((42, 4, 41), (43, 6, 41))
    t.fill((41, 5, 41), (41, 7, 41), "minecraft:cracked_stone_bricks")

    # ------------------------------------------------------------------
    # East receiving: more visible apron/canopy edge abandonment while keeping
    # both receiving doors and the inspection/batch-check sequence intact.
    # ------------------------------------------------------------------
    for pos, block in {
        (47, 0, 22): "minecraft:gravel",
        (48, 0, 22): "minecraft:coarse_dirt",
        (49, 0, 23): "minecraft:gravel",
        (50, 0, 23): "minecraft:coarse_dirt",
        (47, 0, 28): "minecraft:moss_block",
        (48, 0, 29): "minecraft:gravel",
        (49, 0, 29): "minecraft:coarse_dirt",
    }.items():
        t.set(*pos, block)
    t.clear((49, 7, 27), (50, 7, 29))
    t.set(48, 7, 29, "minecraft:cracked_stone_bricks")

    # South relief dispatch: outer canopy/apron deterioration is stronger than r1
    # but the center lane and door leaves remain fully protected.
    t.clear((27, 7, 43), (28, 7, 45))
    t.clear((34, 7, 44), (35, 7, 45))
    for pos, block in {
        (23, 0, 43): "minecraft:gravel",
        (24, 0, 44): "minecraft:coarse_dirt",
        (25, 0, 45): "minecraft:gravel",
        (37, 0, 42): "minecraft:coarse_dirt",
        (38, 0, 43): "minecraft:moss_block",
        (38, 0, 45): "minecraft:gravel",
    }.items():
        t.set(*pos, block)

    # A small amount of debris below exterior failures establishes gravity/cause
    # without flooding primary routes with rubble.
    for pos, block in {
        (5, 1, 33): "minecraft:gravel",
        (7, 1, 38): "minecraft:gravel",
        (45, 1, 34): "minecraft:gravel",
        (44, 1, 35): "minecraft:coarse_dirt",
        (37, 1, 40): "minecraft:gravel",
    }.items():
        if r1.gate_b._block_name(t, *pos) in r1.gate_b.AIR or pos[1] == 1:
            t.set(*pos, block)

    # Re-run every r1 final-state invariant after the stronger facade/roof decay.
    r1._assert_d3_routes(t)
    r1._assert_primary_identity(t)
    r1._assert_proof_chest(t)

    wheat = r1._count_block(t, "minecraft:wheat")
    pipes = r1._count_block(t, "create:fluid_pipe")
    spawners = r1._count_block(t, "minecraft:spawner")
    if wheat < 150:
        raise AssertionError(f"D3 r2 preserves too little surviving cultivation evidence: wheat={wheat}")
    if pipes < 70:
        raise AssertionError(f"D3 r2 preserves too little irrigation/service evidence: pipes={pipes}")
    if spawners != 2:
        raise AssertionError(f"D3 r2 encounter contract requires exactly two spawners; found {spawners}")

    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows002_gate_c_{label}_r2"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        size, blocks = unpack_structure(temp_nbt)
        return render_review_set(
            target="OWS-002",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows002_gate_c_damage_states_r2.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=camera_set,
        )
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison_sheet() -> Path:
    rows = []
    for label, title in (
        ("d0", "D0 — intact / operational"),
        ("d1", "D1 — demand pressure + local anomaly"),
        ("d3", "D3 r2 — current causal ruin"),
    ):
        path = OUTPUT_DIR / label / "contact_sheet.png"
        image = Image.open(path).convert("RGB")
        image.thumbnail((1120, 1600), Image.Resampling.LANCZOS)
        rows.append((title, image.copy()))
        image.close()

    margin = 24
    label_h = 30
    width = max(image.width for _, image in rows) + margin * 2
    height = margin + sum(label_h + image.height + margin for _, image in rows)
    sheet = Image.new("RGB", (width, height), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    y = margin
    for title, image in rows:
        draw.text((margin, y), title, fill=(240, 240, 240))
        y += label_h
        sheet.paste(image, (margin, y))
        y += image.height + margin
    out = OUTPUT_DIR / "damage_comparison_sheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    for _, image in rows:
        image.close()
    return out


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"Gate-C r2 OWS-002 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    status = gate.get("status", "not_started")
    # `passed_r1` is deliberately accepted here because the r1 review decision was
    # corrected after the concurrent automation had already promoted the state.
    if status not in {"passed_r1", "rerender_required", "r2_ready_to_render", "ready_to_render"}:
        print(f"Gate-C r2 OWS-002 renderer skipped: status={status}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()

    d1_changes = r1._diff_count(d0, d1)
    d3_changes = r1._diff_count(d0, d3)
    if d1_changes != 83:
        raise AssertionError(f"Gate-C r2 must preserve accepted D1 exactly; got {d1_changes} changes")
    if not 400 <= d3_changes <= 800:
        raise AssertionError(f"D3 r2 change count {d3_changes} is outside the stronger causal-ruin guard")
    if d3_changes <= d1_changes * 4:
        raise AssertionError("D3 r2 must be substantially more transformed than accepted D1")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows002_fixed_v1")
    _render_state("d0", "D0 intact / operational", d0, f"gate-c-r2-d0@{revision}", camera_set)
    _render_state("d1", "D1 demand pressure / localized quality anomaly", d1, f"gate-c-r2-d1@{revision}", camera_set)
    _render_state("d3", "D3 r2 centuries-later causal ruin", d3, f"gate-c-r2-d3@{revision}", camera_set)
    comparison_path = _damage_comparison_sheet()

    aggregate = {
        "target": "OWS-002",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r2@{revision}",
        "source_commit": os.environ.get("GITHUB_SHA", "working-tree"),
        "fixed_camera_set": camera_set,
        "visual_review_status": "rendered_pending_manual_review",
        "r1_decision": "REVISION REQUIRED — D3 visually too pristine",
        "accepted_from_r1": ["D0", "D1"],
        "revised_in_r2": ["D3"],
        "states": {
            key: str((OUTPUT_DIR / key / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
            for key in ("d0", "d1", "d3")
        },
        "comparison_sheet": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "change_counts_from_d0": {"d1": d1_changes, "d3": d3_changes},
        "protected_invariants_asserted": [
            "north public entrance and queue",
            "staff-side records/proof approach",
            "openable canonical proof chest",
            "grow aisles A and B",
            "west harvest/wash transfer",
            "south relief dispatch lane and doors",
            "east receiving doors",
            "roof ladder/trapdoor",
            "primary VCF/facility identity",
            "surviving cultivation and irrigation evidence",
            "exactly two D3 vanilla encounter spawners",
        ],
        "significant_findings_corrected_or_justified": False,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    aggregate_path = OUTPUT_DIR / "gate_c_manifest.json"
    aggregate_path.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8", newline="\n")

    state["active_status"] = "gate_c_r2_rendered_pending_review"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "implemented_pending_gate_c_r2_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r2_rendered_pending_manual_review"
    state["active_target_passes"]["micro_detail"] = "blocked_by_gate_c_r2_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["decision"] = "R1 REVISION REQUIRED"
    gate["r1_decision"] = "REVISION REQUIRED"
    gate["r2_manifest"] = str(aggregate_path.relative_to(ROOT)).replace("\\", "/")
    gate["r2_comparison_sheet"] = str(comparison_path.relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_c_damage_states_r2.py"
    gate["review_only"] = True
    gate["d1_change_count"] = d1_changes
    gate["r2_d3_change_count"] = d3_changes
    gate["significant_findings_corrected_or_justified"] = False
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate C r2: accepted D1 changes={d1_changes}, revised D3 changes={d3_changes}; "
        "manual r2 historical/damage review remains pending."
    )


if __name__ == "__main__":
    main()

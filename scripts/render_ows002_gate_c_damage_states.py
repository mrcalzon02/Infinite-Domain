#!/usr/bin/env python3
"""[SYSTEM REPORT] Render OWS-002 Gate-C D0/D1/D3 historical review states.

Gate C is review-only. Every state derives from the accepted Gate-B r2 intact
building. D1 adds demand pressure plus one localized cultivation anomaly while the
facility still operates. D3 applies causal abandonment/weather/service damage,
two restrained vanilla encounter niches, and the deterministic authorization
proof chest. None of this replaces the authoritative shipping builder until the
visual gate passes and a later Gate-D synchronization step succeeds.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image, ImageDraw

import generate_wasteland_sites as base
import render_ows002_gate_b_intact as gate_b
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_c_damage_states" / "r1"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_002_vcf_emergency_community_grow_hall"
PROOF_POS = (23, 2, 14)


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if gate_b._block_name(a, *pos) != gate_b._block_name(b, *pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if gate_b._block_name(t, *pos) == name)


def _assert_proof_chest(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("D3 proof chest is missing")
    state, nbt = row
    name = t.palette[state]["Name"]
    if name != "minecraft:chest":
        raise AssertionError(f"D3 proof location contains {name}, not minecraft:chest")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(
            f"D3 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}"
        )
    if gate_b._block_name(t, PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2]) not in gate_b.AIR:
        raise AssertionError("D3 proof chest cannot open because the block directly above it is occupied")

    matching = 0
    for _, (_, block_nbt) in t.blocks.items():
        if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE:
            matching += 1
    if matching != 1:
        raise AssertionError(f"D3 must contain exactly one canonical proof container; found {matching}")


def _assert_primary_identity(t: base.Template) -> None:
    for pos, label in (((21, 8, 3), "VERDANT CONTINUUM FOODS"), ((27, 8, 3), "facility identity")):
        if gate_b._block_name(t, *pos) != "minecraft:oak_wall_sign":
            raise AssertionError(f"D3 no longer preserves {label} sign at {pos}")
    if _count_block(t, "minecraft:oak_wall_sign") < 10:
        raise AssertionError("D3 preserves too little operational wayfinding to reconstruct the facility")


def _assert_d3_routes(t: base.Template) -> None:
    # Public entrance and queue remain the primary player approach.
    gate_b._assert_door(
        t, 24, 2, 4, "D3 public entrance west leaf", block_name="minecraft:dark_oak_door"
    )
    gate_b._assert_door(
        t, 25, 2, 4, "D3 public entrance east leaf", block_name="minecraft:dark_oak_door"
    )
    gate_b._assert_clear(t, (24, 2, 5), (26, 4, 12), "D3 public queue/orientation route")
    gate_b._assert_door(t, 28, 2, 13, "D3 public-to-staff records control")

    # The proof chest is adjacent to a clear staff-side records approach.
    gate_b._assert_clear(t, (24, 2, 14), (28, 3, 14), "D3 records/proof approach")

    # Two principal cultivation aisles and cross-routes survive even though the
    # third bank carries the heaviest damage.
    gate_b._assert_clear(t, (27, 2, 18), (29, 4, 33), "D3 grow aisle A")
    gate_b._assert_clear(t, (33, 2, 18), (35, 4, 33), "D3 grow aisle B")
    gate_b._assert_clear(t, (24, 2, 31), (35, 4, 33), "D3 south harvest cross-aisle")

    # Harvest and relief circulation remains reconstructable and traversable.
    gate_b._assert_clear(t, (18, 2, 34), (22, 4, 36), "D3 raw-harvest west transfer")
    gate_b._assert_clear(t, (18, 2, 39), (28, 4, 40), "D3 checked-harvest return")
    gate_b._assert_clear(t, (29, 2, 34), (32, 4, 40), "D3 relief dispatch lane")
    gate_b._assert_door(t, 30, 2, 41, "D3 south dispatch west leaf")
    gate_b._assert_door(t, 31, 2, 41, "D3 south dispatch east leaf")

    # East receiving and retained roof service route stay legible.
    gate_b._assert_door(t, 46, 2, 24, "D3 east receiving west leaf")
    gate_b._assert_door(t, 46, 2, 25, "D3 east receiving east leaf")
    gate_b._assert_block(t, 44, 18, 38, "minecraft:ladder", "D3 roof ladder top")
    gate_b._assert_block(t, 44, 19, 38, "minecraft:iron_trapdoor", "D3 roof landing")


def build_d0() -> base.Template:
    """Exact accepted Gate-B r2 intact interpretation."""
    return gate_b.build_gate_b_intact()


def build_d1() -> base.Template:
    """Late operation: demand pressure plus one bounded rack/service anomaly."""
    t = gate_b.build_gate_b_intact()

    # Public demand pressure accumulates beside, never inside, the queue spine.
    t.fill((19, 2, 7), (21, 3, 8), "immersiveengineering:crate")
    t.set(20, 2, 9, "minecraft:barrel")

    # East receiving processes more incoming stock as the city leans on the site.
    t.fill((48, 1, 26), (49, 2, 27), "jaffabricate:pallet_full")
    t.set(45, 3, 28, "immersiveengineering:crate")

    # Relief backlog increases at the sides of the south dispatch lane while the
    # four-block central route remains usable.
    t.fill((24, 2, 34), (26, 3, 35), "immersiveengineering:crate")
    t.fill((35, 2, 39), (37, 2, 40), "jaffabricate:pallet_full")

    # One localized problem: the south/east end of cultivation Bank 3 is pulled
    # from ordinary production. Only this segment changes; Banks 1 and 2 continue.
    t.fill((36, 1, 27), (38, 1, 30), "minecraft:yellow_concrete")
    for y in (3, 8):
        t.clear((36, y, 28), (38, y, 30))
    t.fill((36, 10, 28), (38, 10, 30), "minecraft:yellow_concrete")
    t.set(38, 9, 29, "minecraft:yellow_concrete")

    # Replacement/inspection material is staged on the service side rather than
    # spilling into the protected east grow aisle.
    t.set(43, 2, 31, "immersiveengineering:crate")
    t.set(45, 2, 31, "minecraft:barrel")

    # Direct temporary crisis language on a dedicated support, not on permanent
    # VCF identity. This header sits above the suspect rack footprint.
    t.set(37, 9, 28, "minecraft:white_concrete")
    base.wall_sign(t, 37, 9, 27, "north", "RACK 3", "QUALITY HOLD")

    # D1 must still operate around the issue.
    gate_b._assert_clear(t, (24, 2, 5), (26, 4, 12), "D1 public queue")
    gate_b._assert_clear(t, (27, 2, 18), (29, 4, 33), "D1 grow aisle A")
    gate_b._assert_clear(t, (33, 2, 18), (35, 4, 33), "D1 grow aisle B")
    gate_b._assert_clear(t, (39, 2, 18), (41, 4, 31), "D1 east grow-service strip")
    gate_b._assert_clear(t, (29, 2, 34), (32, 4, 40), "D1 relief dispatch lane")
    gate_b._assert_door(t, 30, 2, 41, "D1 south dispatch west leaf")
    gate_b._assert_door(t, 31, 2, 41, "D1 south dispatch east leaf")

    return t


def build_d3() -> base.Template:
    """Current ruin: abandonment -> roof/glazing failure -> water/service decay."""
    t = build_d1()

    # ------------------------------------------------------------------
    # Roof lantern: several coherent broken panes, not uniform random peppering.
    # The steel support ring and most glazing survive, preserving the hero volume.
    # ------------------------------------------------------------------
    t.clear((28, 19, 22), (31, 20, 25))
    t.clear((37, 18, 30), (40, 20, 33))
    t.set(29, 18, 24, "minecraft:cobweb")
    t.set(39, 18, 31, "minecraft:cobweb")

    # Localized lower-roof service penetration adjacent to the VCF plant. Water
    # entering here explains later west support-wing weathering.
    t.clear((16, 11, 35), (19, 12, 38))
    t.fill((15, 10, 35), (18, 10, 38), "minecraft:mossy_stone_bricks")
    t.fill((18, 10, 34), (20, 10, 35), "minecraft:cracked_stone_bricks")

    # ------------------------------------------------------------------
    # Third grow bank: the historically suspect segment is the one that fails
    # hardest after abandonment. Two other banks remain substantially intact.
    # ------------------------------------------------------------------
    t.clear((36, 2, 27), (38, 8, 30))
    t.fill((36, 1, 27), (38, 1, 30), "minecraft:coarse_dirt")
    t.fill((36, 1, 29), (38, 1, 30), "minecraft:moss_block")
    t.set(36, 2, 29, "minecraft:gravel")
    t.set(38, 2, 28, "minecraft:gravel")
    # The nearby branch fails while the main high trunk remains reconstructable.
    t.clear((36, 11, 30), (41, 11, 30))
    t.set(39, 10, 30, "minecraft:cobweb")

    # ------------------------------------------------------------------
    # West wet-service decay follows the roof leak and former wash infrastructure.
    # Workflow furniture remains legible beneath the damage.
    # ------------------------------------------------------------------
    t.clear((8, 11, 35), (11, 11, 38))
    t.fill((7, 1, 36), (11, 1, 40), "minecraft:mossy_stone_bricks")
    t.fill((12, 1, 38), (15, 1, 40), "minecraft:coarse_dirt")
    t.set(8, 2, 39, "minecraft:cobweb")
    t.set(14, 3, 39, "minecraft:cobweb")

    # East receiving weathers at the outside edge while its service opening and
    # batch-check sequence remain recognizable.
    t.set(49, 0, 24, "minecraft:gravel")
    t.set(50, 0, 25, "minecraft:coarse_dirt")
    t.clear((46, 9, 26), (46, 10, 27))
    t.set(49, 1, 27, "minecraft:air")

    # South relief canopy loses one outer portion and side stock weathers, but the
    # central dispatch route and working door pair stay clear.
    t.clear((34, 7, 43), (35, 7, 45))
    t.fill((36, 0, 43), (38, 0, 46), "minecraft:gravel")
    t.set(37, 1, 44, "minecraft:coarse_dirt")

    # Public face remains the most recognizable, with only selected lost glazing.
    for pos in ((20, 3, 4), (20, 4, 4), (29, 2, 4), (30, 4, 4), (34, 5, 7)):
        t.set(*pos, "minecraft:air")

    # Long-term localized biological/weather occupation follows wet/exposed areas.
    for pos in ((37, 2, 27), (38, 2, 30), (10, 2, 37), (12, 2, 40)):
        if gate_b._block_name(t, *pos) in gate_b.AIR:
            t.set(*pos, "minecraft:dead_bush")

    # Two restrained vanilla encounter niches tied to the ruin, never to D0/D1.
    t.spawner(37, 2, 29, "minecraft:zombie", count=1, nearby=4)
    t.spawner(8, 2, 29, "minecraft:spider", count=1, nearby=3)

    # Deterministic authorization proof stays in the protected staff-side records
    # area. The position above is explicitly cleared so the chest is openable.
    t.set(23, 3, 14, "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")

    _assert_d3_routes(t)
    _assert_primary_identity(t)
    _assert_proof_chest(t)

    # The final ruin must still communicate a cultivation facility rather than a
    # generic civic shell after the historically suspect bank is damaged.
    wheat = _count_block(t, "minecraft:wheat")
    pipes = _count_block(t, "create:fluid_pipe")
    spawners = _count_block(t, "minecraft:spawner")
    if wheat < 150:
        raise AssertionError(f"D3 preserves too little surviving cultivation evidence: wheat={wheat}")
    if pipes < 70:
        raise AssertionError(f"D3 preserves too little irrigation/service evidence: pipes={pipes}")
    if spawners != 2:
        raise AssertionError(f"D3 encounter contract requires exactly two spawners; found {spawners}")

    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows002_gate_c_{label}_r1"
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
            source_path=f"review-only:render_ows002_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=camera_set,
        )
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison_sheet() -> Path:
    """Stack the three identical-camera contact sheets for direct chronology review."""
    rows = []
    for label, title in (("d0", "D0 — intact / operational"), ("d1", "D1 — demand pressure + local anomaly"), ("d3", "D3 — current causal ruin")):
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
        print(f"Gate-C OWS-002 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    status = gate.get("status", "not_started")
    if status not in {"implementation_ready", "ready_to_render", "rerender_required"}:
        print(f"Gate-C OWS-002 renderer skipped: status={status}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()

    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if not 15 <= d1_changes <= 180:
        raise AssertionError(f"D1 change count {d1_changes} is not a restrained but visible operational overlay")
    if not 100 <= d3_changes <= 500:
        raise AssertionError(f"D3 change count {d3_changes} is not a localized causal ruin pass")
    if d3_changes <= d1_changes * 2:
        raise AssertionError("D3 must be materially more transformed than D1")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows002_fixed_v1")
    _render_state("d0", "D0 intact / operational", d0, f"gate-c-r1-d0@{revision}", camera_set)
    _render_state("d1", "D1 demand pressure / localized quality anomaly", d1, f"gate-c-r1-d1@{revision}", camera_set)
    _render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r1-d3@{revision}", camera_set)
    comparison_path = _damage_comparison_sheet()

    aggregate = {
        "target": "OWS-002",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r1@{revision}",
        "source_commit": os.environ.get("GITHUB_SHA", "working-tree"),
        "fixed_camera_set": camera_set,
        "visual_review_status": "rendered_pending_manual_review",
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

    state["active_status"] = "gate_c_r1_rendered_pending_review"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "implemented_pending_gate_c_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_manifest"] = str(aggregate_path.relative_to(ROOT)).replace("\\", "/")
    gate["r1_comparison_sheet"] = str(comparison_path.relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_c_damage_states.py"
    gate["review_only"] = True
    gate["d1_change_count"] = d1_changes
    gate["d3_change_count"] = d3_changes
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate C r1: D1 changes={d1_changes}, D3 changes={d3_changes}; "
        "manual historical/damage review remains pending."
    )


if __name__ == "__main__":
    main()

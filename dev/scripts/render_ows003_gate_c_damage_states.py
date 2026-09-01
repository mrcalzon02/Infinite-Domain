#!/usr/bin/env python3
"""[SYSTEM REPORT] Render OWS-003 Gate-C D0/D1/D3 historical review states.

Gate C is review-only. D0 is the exact Gate-B r7 intact model. D1 adds a bounded
seal/gasket exception around nursery 3 and normal quality hold while the facility
continues operating. D3 applies causal refrigeration/roof/dock abandonment,
limited cold-room damage, orchard decay, two optional vanilla encounter niches,
and the deterministic batch/licensing proof. Nothing here replaces shipping
worldgen until Gate C passes and a later authoritative builder/Gate-D sync occurs.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as gate_b_base
import render_ows003_gate_b_intact_r7 as gate_b
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_c_damage_states" / "r1"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_003_vcf_cold_chain_culture_nursery"
PROOF_POS = (53, 2, 12)
REQUIRED_HISTORY_DOCS = (
    "OWS-003_PASS13_HISTORICAL_LAYERING.md",
    "OWS-003_PASS14_ENVIRONMENTAL_NARRATIVE.md",
    "OWS-003_PASS15_ENCOUNTER_ARCHITECTURE.md",
    "OWS-003_PASS16_LOOT_ARCHITECTURE.md",
    "OWS-003_PASS17_QUEST_PROOF_ARCHITECTURE.md",
    "OWS-003_PASS18_DAMAGE_AND_DECAY.md",
)


def _block_name(t: base.Template, pos: tuple[int, int, int]) -> str:
    return gate_b_base._block_name(t, *pos)


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if _block_name(a, pos) != _block_name(b, pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _block_name(t, pos) == name)


def _assert_history_authorized() -> None:
    review = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_R7_REVIEW.md"
    if not review.exists() or "OWS-003 GATE B r7: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-003 Gate-B r7 PASSED review is missing")
    base_dir = review.parent
    missing = [name for name in REQUIRED_HISTORY_DOCS if not (base_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: missing required historical planning docs: {missing}")


def _assert_proof_chest(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("D3 proof chest is missing")
    state_id, nbt = row
    name = t.palette[state_id]["Name"]
    if name != "minecraft:chest":
        raise AssertionError(f"D3 proof location contains {name}, not minecraft:chest")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"D3 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _block_name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in gate_b_base.AIR:
        raise AssertionError("D3 proof chest cannot open because the block directly above it is occupied")
    matching = sum(
        1
        for _, (_, block_nbt) in t.blocks.items()
        if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE
    )
    if matching != 1:
        raise AssertionError(f"D3 must contain exactly one canonical OWS-003 proof container; found {matching}")


def _assert_identity(t: base.Template) -> None:
    for pos, label in (
        ((32, 6, 3), "VERDANT CONTINUUM FOODS"),
        ((46, 6, 3), "COLD-CHAIN CULTURE NURSERY"),
        ((56, 7, 22), "RECEIVING COLD CHAIN"),
        ((54, 7, 44), "OUTBOUND CULTURES"),
    ):
        if _block_name(t, pos) != "minecraft:oak_wall_sign":
            raise AssertionError(f"D3 no longer preserves {label} sign at {pos}")
    if _count_block(t, "minecraft:oak_wall_sign") < 12:
        raise AssertionError("D3 preserves too little VCF/operational wayfinding")


def _assert_d3_routes(t: base.Template) -> None:
    gate_b_base._assert_door(t, 39, 2, 4, "D3 front staff entrance west leaf", block_name="minecraft:dark_oak_door")
    gate_b_base._assert_door(t, 40, 2, 4, "D3 front staff entrance east leaf", block_name="minecraft:dark_oak_door")
    gate_b_base._assert_door(t, 43, 2, 10, "D3 batch/licensing office door")
    gate_b_base._assert_clear(t, (44, 2, 11), (52, 3, 12), "D3 proof-office approach")
    gate_b_base._assert_clear(t, (36, 2, 18), (38, 4, 42), "D3 conditioned operations spine")
    gate_b_base._assert_clear(t, (29, 2, 21), (31, 4, 33), "D3 cold-vault center aisle")
    gate_b_base._assert_clear(t, (40, 2, 22), (44, 4, 25), "D3 nursery-1 service area")
    gate_b_base._assert_clear(t, (40, 2, 27), (44, 4, 30), "D3 nursery-2 service area")
    gate_b_base._assert_clear(t, (49, 2, 23), (53, 4, 27), "D3 receiving freight lane")
    gate_b_base._assert_clear(t, (44, 2, 40), (47, 4, 42), "D3 packing-to-dispatch transfer")
    gate_b_base._assert_door(t, 55, 2, 24, "D3 receiving west leaf")
    gate_b_base._assert_door(t, 55, 2, 25, "D3 receiving east leaf")
    gate_b_base._assert_door(t, 46, 2, 43, "D3 dispatch west leaf")
    gate_b_base._assert_door(t, 47, 2, 43, "D3 dispatch east leaf")
    gate_b_base._assert_block(t, 54, 18, 36, "minecraft:ladder", "D3 maintenance ladder top")


def build_d0() -> base.Template:
    return gate_b.build_gate_b_intact_r7()


def build_d1() -> base.Template:
    """Localized service exception while the cold-chain nursery still operates."""
    t = build_d0()

    # Nursery 3 receives a bounded yellow service/exception field beneath the
    # east equipment bank. The west inspection floor remains completely clear.
    t.fill((45, 1, 32), (47, 1, 35), "minecraft:yellow_concrete")
    # One cooler and one riser segment are removed from ordinary service to show
    # a gasket/seal excursion rather than contamination of the whole nursery.
    t.set(47, 2, 34, "minecraft:yellow_concrete")
    t.set(47, 8, 30, "minecraft:yellow_concrete")

    # Suspect stock is rerouted into the existing normal quality-hold room.
    t.set(50, 2, 31, "immersiveengineering:crate")
    t.set(53, 2, 31, "minecraft:barrel")
    t.set(52, 3, 30, "minecraft:yellow_concrete")

    # Maintenance attention increases near the affected service node, off the
    # protected operations and nursery inspection aisles.
    t.set(49, 3, 30, "immersiveengineering:crate")
    t.set(54, 2, 31, "minecraft:barrel")

    # D1 remains fully operable around the bounded exception.
    gate_b_base._assert_clear(t, (36, 2, 18), (38, 4, 42), "D1 conditioned operations spine")
    gate_b_base._assert_clear(t, (29, 2, 21), (31, 4, 33), "D1 cold-vault center aisle")
    gate_b_base._assert_clear(t, (40, 2, 22), (44, 4, 25), "D1 nursery-1 service area")
    gate_b_base._assert_clear(t, (40, 2, 27), (44, 4, 30), "D1 nursery-2 service area")
    gate_b_base._assert_clear(t, (40, 2, 32), (44, 4, 35), "D1 nursery-3 service area")
    gate_b_base._assert_clear(t, (49, 2, 23), (53, 4, 27), "D1 receiving freight lane")
    gate_b_base._assert_clear(t, (44, 2, 40), (47, 4, 42), "D1 packing-to-dispatch transfer")
    return t


def build_d3() -> base.Template:
    """Centuries-later ruin caused by service failure, weather and abandonment."""
    t = build_d1()

    # Refrigeration field failure: one large equipment group and part of the
    # service header disappear, while most plant mass remains reconstructable.
    t.clear((40, 19, 32), (44, 22, 36))
    t.clear((45, 18, 23), (45, 16, 23))
    t.clear((42, 18, 23), (46, 18, 23))
    t.set(42, 18, 34, "minecraft:gravel")
    t.set(44, 18, 35, "minecraft:cobweb")

    # Roof-light/service penetration failures are coherent patches, not random
    # peppering. The original three-strip rhythm remains visible.
    t.clear((46, 17, 32), (48, 17, 36))
    t.clear((37, 17, 34), (39, 17, 37))
    for pos in ((47, 16, 34), (38, 16, 36), (45, 16, 35)):
        t.set(*pos, "minecraft:cobweb")

    # Water ingress below damaged roof/service areas.
    t.fill((44, 1, 33), (47, 1, 36), "minecraft:mossy_stone_bricks")
    t.fill((32, 1, 33), (35, 1, 35), "minecraft:cracked_stone_bricks")
    t.set(46, 2, 36, "minecraft:gravel")

    # Nursery 3 takes the strongest long-term enclosure damage, but the cell and
    # its transfer frame remain reconstructable and its service aisle stays open.
    t.clear((44, 5, 36), (47, 7, 36))
    t.clear((39, 5, 34), (39, 7, 35))
    t.set(46, 3, 34, "minecraft:cobweb")

    # Receiving and quality-hold service edges weather heavily at exposed doors.
    t.clear((55, 6, 26), (55, 7, 28))
    t.set(57, 0, 27, "minecraft:gravel")
    t.set(58, 0, 28, "minecraft:coarse_dirt")
    t.set(54, 2, 30, "minecraft:gravel")
    t.set(53, 2, 30, "minecraft:cobweb")

    # South dispatch canopy/apron weathering; central working doors and transfer
    # route remain intact.
    t.clear((50, 8, 45), (52, 8, 48))
    t.fill((50, 0, 46), (54, 0, 50), "minecraft:gravel")
    t.set(52, 1, 47, "minecraft:coarse_dirt")

    # Front office is comparatively protected; only minor facade glazing is lost.
    t.clear((35, 5, 3), (36, 6, 3))

    # Orchard rows become irregular survivors without erasing the agricultural
    # history. Remove two canopy groups and scar their ground positions.
    for x, z in ((5, 45), (15, 31), (20, 17)):
        t.clear((x - 2, 4, z - 2), (x + 2, 6, z + 2))
        t.clear((x, 2, z), (x, 4, z))
        t.set(x, 1, z, "minecraft:coarse_dirt")
        t.set(x + 1, 1, z, "minecraft:dead_bush")

    # Two restrained optional encounter niches, both away from proof and primary
    # circulation. They exist only in D3.
    t.spawner(52, 2, 30, "minecraft:zombie", count=1, nearby=4)
    t.spawner(51, 2, 40, "minecraft:spider", count=1, nearby=3)

    # Deterministic proof remains in the front batch/licensing office.
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    _assert_d3_routes(t)
    _assert_identity(t)
    _assert_proof_chest(t)

    coolers = _count_block(t, "oritech:cooler_block")
    pipes = _count_block(t, "create:fluid_pipe")
    spawners = _count_block(t, "minecraft:spawner")
    if coolers < 90:
        raise AssertionError(f"D3 preserves too little cold-chain evidence: cooler_blocks={coolers}")
    if pipes < 60:
        raise AssertionError(f"D3 preserves too little refrigeration/service evidence: pipes={pipes}")
    if spawners != 2:
        raise AssertionError(f"D3 encounter contract requires exactly two spawners; found {spawners}")
    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows003_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        size, blocks = unpack_structure(temp_nbt)
        return render_review_set(
            target="OWS-003",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows003_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=camera_set,
        )
    finally:
        temp_nbt.unlink(missing_ok=True)


def main() -> None:
    _assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-C OWS-003 renderer skipped: active target is {state.get('active_target')}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()
    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if not (10 <= d1_changes <= 120):
        raise AssertionError(f"D1 must remain a bounded early anomaly; changed_positions={d1_changes}")
    if d3_changes < 180:
        raise AssertionError(f"D3 is too visually/structurally close to D0; changed_positions={d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"D3 must be materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("fixed_camera_set", "ows003_fixed_v1")
    manifests = {
        "D0": _render_state("d0", "D0 intact / normal operation", d0, f"gate-c-r1@{revision}", camera_set),
        "D1": _render_state("d1", "D1 early seal/gasket anomaly", d1, f"gate-c-r1@{revision}", camera_set),
        "D3": _render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r1@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-003",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r1@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows003_gate_b_intact_r7.build_gate_b_intact_r7",
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 2,
        "darknet_return_hook": "reserved_not_activated",
        "visual_review_status": "rendered_pending_manual_review",
        "states": {key: value["views"] for key, value in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8")

    state["active_status"] = "gate_c_r1_rendered_pending_review"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "implemented_gate_c_r1_pending_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r1_rendered_pending_manual_review"
    gate = state["visual_review_gates"]["gate_c_damage_states"]
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_c_damage_states.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    state.setdefault("planning_records", {}).update({
        "pass_13_historical_layering": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS13_HISTORICAL_LAYERING.md",
        "pass_14_environmental_narrative": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS14_ENVIRONMENTAL_NARRATIVE.md",
        "pass_15_encounter_architecture": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS15_ENCOUNTER_ARCHITECTURE.md",
        "pass_16_loot_architecture": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS16_LOOT_ARCHITECTURE.md",
        "pass_17_quest_proof": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS17_QUEST_PROOF_ARCHITECTURE.md",
        "pass_18_damage_and_decay": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS18_DAMAGE_AND_DECAY.md",
    })
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-003 Gate C r1: D1 changes={d1_changes}, D3 changes={d3_changes}; manual review remains pending.")


if __name__ == "__main__":
    main()

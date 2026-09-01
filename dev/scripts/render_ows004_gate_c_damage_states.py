#!/usr/bin/env python3
"""[SYSTEM REPORT] Render OWS-004 Gate-C D0/D1/D3 historical review states.

Gate C is review-only. D0 is the exact Gate-B r4 intact model. D1 applies only
the approved localized fourth-floor containment intervention while lower floors
remain operational. D3 transforms those same real systems into a causal
centuries-later ruin with the strongest failure at the upper cultivation level
and environmental crown. Proof, principal staff circulation, freight history and
west secondary egress remain protected. Nothing here becomes shipping worldgen
until Gate C passes and the later authoritative/Gate-D synchronization occurs.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows004_gate_b_intact as gate_b_base
import render_ows004_gate_b_intact_r3 as gate_b_r3
import render_ows004_gate_b_intact_r4 as gate_b
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_c_damage_states" / "r1"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_004_vcf_mycological_vertical_farm_tower"
PROOF_POS = (32, 2, 12)
LEVELS = gate_b_base.LEVELS
REQUIRED_HISTORY_DOCS = (
    "OWS-004_PASS13_HISTORICAL_LAYERING.md",
    "OWS-004_PASS14_ENVIRONMENTAL_NARRATIVE.md",
    "OWS-004_PASS15_ENCOUNTER_ARCHITECTURE.md",
    "OWS-004_PASS16_LOOT_ARCHITECTURE.md",
    "OWS-004_PASS17_QUEST_PROOF_ARCHITECTURE.md",
    "OWS-004_PASS18_DAMAGE_AND_DECAY.md",
)
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str:
    row = t.blocks.get(pos)
    if row is None:
        return "minecraft:air"
    return t.palette[row[0]]["Name"]


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if _name(a, pos) != _name(b, pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)


def _assert_history_authorized() -> None:
    review = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-004_GATE_B_R4_REVIEW.md"
    if not review.exists() or "OWS-004 GATE B r4: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-004 Gate-B r4 PASSED review is missing")
    base_dir = review.parent
    missing = [name for name in REQUIRED_HISTORY_DOCS if not (base_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: missing required historical planning docs: {missing}")


def _assert_proof_chest(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-004 D3 proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-004 proof location contains {t.palette[state_id]['Name']}, not minecraft:chest")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-004 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-004 proof chest cannot open because the block directly above is occupied")
    matching = sum(
        1
        for _, (_, block_nbt) in t.blocks.items()
        if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE
    )
    if matching != 1:
        raise AssertionError(f"OWS-004 must contain exactly one canonical proof container; found {matching}")


def _assert_vertical_routes(t: base.Template) -> None:
    # West secondary egress remains a continuous discoverable route.
    for y in range(9, 39):
        if _name(t, (8, y, 30)) != "minecraft:ladder":
            raise AssertionError(f"OWS-004 west secondary-egress ladder gap at y={y}")

    # East staff stair remains an actual people system. Reconstruct the accepted
    # r4 route and validate both stair treads and intentional dogleg landings.
    d0, expected_treads, landing_points = gate_b.build_gate_b_intact_r4()
    del d0
    for point in expected_treads:
        if _name(t, point) != "minecraft:stone_brick_stairs":
            raise AssertionError(f"OWS-004 staff stair lost tread at {point}: {_name(t, point)}")
        x, y, z = point
        for head_y in (y + 1, y + 2):
            if _name(t, (x, head_y, z)) not in AIR:
                raise AssertionError(f"OWS-004 staff stair headroom blocked at {(x, head_y, z)}")
    for point in landing_points:
        if _name(t, point) != "minecraft:polished_andesite":
            raise AssertionError(f"OWS-004 staff stair dogleg landing lost at {point}")

    # Freight and environmental systems remain spatially separate from people.
    for level in LEVELS:
        if _name(t, (42, level + 1, 27)) != "create:andesite_casing":
            raise AssertionError(f"OWS-004 freight/material core lost at level {level}")
        if _name(t, (42, level, 19)) != "create:fluid_pipe":
            raise AssertionError(f"OWS-004 environmental riser lost at level {level}")


def _assert_identity(t: base.Template) -> None:
    # Preserve enough public/operational identity that the player can still read
    # the institution and process after abandonment.
    if _count_block(t, "minecraft:oak_wall_sign") < 8:
        raise AssertionError("OWS-004 D3 preserves too little VCF/operational wayfinding")
    for pos in ((18, 6, 5), (22, 6, 5)):
        if _name(t, pos) != "minecraft:oak_wall_sign":
            raise AssertionError(f"OWS-004 primary VCF identity sign lost at {pos}")


def build_d0() -> base.Template:
    t, expected_treads, landing_points = gate_b.build_gate_b_intact_r4()
    gate_b._assert_r4(t, expected_treads, landing_points)
    return t


def build_d1() -> base.Template:
    """Localized active-containment retrofit on cultivation level four only."""
    t = build_d0()
    y = 30

    # Yellow containment cross-lane interrupts the normal green production logic
    # only around the upper isolation/control branch.
    t.fill((28, y, 17), (37, y, 18), "minecraft:yellow_concrete")
    t.fill((28, y, 28), (37, y, 29), "minecraft:yellow_concrete")
    t.fill((28, y, 18), (29, y, 29), "minecraft:yellow_concrete")

    # Temporary containment bulkhead at the already-established environmental
    # branch. Keep a controlled doorway through it rather than sealing circulation.
    t.fill((29, y + 1, 20), (29, y + 4, 27), "minecraft:white_concrete")
    t.clear((29, y + 1, 23), (29, y + 3, 24))
    base.door(t, 29, y + 1, 24, "west", "iron")

    # One upper grow bank is taken offline; retained neighboring rows prove this
    # is a bounded response rather than building-wide collapse.
    t.clear((31, y + 1, 20), (32, y + 3, 22))
    t.fill((31, y + 1, 20), (32, y + 1, 22), "minecraft:yellow_concrete")

    # Real service response: capped/bypassed branch, inspection station and clean
    # maintenance/filter stock on the east service side.
    t.clear((32, y + 4, 16), (34, y + 4, 16))
    t.fill((32, y + 4, 16), (33, y + 4, 16), "minecraft:yellow_concrete")
    t.set(34, y + 4, 16, "create:fluid_pipe")
    t.fill((35, y + 1, 29), (37, y + 2, 30), "immersiveengineering:crate")
    t.set(36, y + 3, 29, "minecraft:barrel")
    base.wall_sign(t, 36, y + 4, 30, "north", "QUALITY HOLD", "LEVEL 4")

    # D1 must leave lower cultivation floors untouched and all vertical systems usable.
    _assert_vertical_routes(t)
    gate_b_base._assert_intact_contracts(t)
    return t


def build_d3() -> base.Template:
    """Centuries-later causal ruin grown from the D1 containment intervention."""
    t = build_d1()

    # Crown/environmental greenhouse takes the strongest weather failure. Open
    # coherent roof/glazing patches while keeping the crown volume recognizable.
    t.clear((14, 46, 17), (20, 46, 24))
    t.clear((29, 46, 25), (36, 46, 34))
    t.clear((34, 43, 17), (39, 45, 19))
    t.clear((33, 44, 17), (37, 44, 19))
    t.set(34, 43, 18, "minecraft:cobweb")
    t.set(36, 42, 19, "minecraft:cobweb")

    # Upper containment floor fails around the exact D1 quarantine system. The
    # bulkhead remains partially readable and one adjacent bank collapses/spills.
    t.clear((29, 32, 20), (29, 34, 22))
    t.clear((29, 33, 26), (29, 34, 27))
    t.fill((29, 31, 20), (29, 31, 22), "minecraft:cracked_stone_bricks")
    t.clear((14, 31, 18), (16, 33, 22))
    t.fill((14, 30, 18), (17, 30, 23), "minecraft:coarse_dirt")
    t.set(16, 31, 21, "minecraft:brown_mushroom")
    t.set(17, 31, 22, "minecraft:red_mushroom")
    t.set(18, 31, 23, "minecraft:cobweb")

    # One environmental branch fails downstream of the crown; do not sever the
    # protected main riser itself, so the original system remains reconstructable.
    t.clear((34, 34, 19), (37, 34, 19))
    t.set(35, 34, 19, "minecraft:cracked_stone_bricks")
    t.set(37, 33, 20, "minecraft:cobweb")

    # Progressive but lighter deterioration on level three: localized rack loss
    # and wet-floor damage below the failed upper systems.
    t.clear((14, 24, 19), (15, 26, 21))
    t.fill((14, 23, 19), (17, 23, 22), "minecraft:mossy_stone_bricks")
    t.set(17, 24, 20, "minecraft:cobweb")

    # Lower production remains substantially readable. Add only small long-term
    # service scars and leave the central protected aisle clear.
    t.fill((11, 9, 34), (14, 9, 36), "minecraft:cracked_stone_bricks")
    t.fill((13, 16, 34), (16, 16, 36), "minecraft:mossy_stone_bricks")

    # Exterior upper-service/crown weathering makes D3 legible from fixed cameras
    # without random checkerboard destruction.
    t.clear((38, 35, 36), (40, 38, 36))
    t.clear((10, 36, 14), (12, 38, 14))
    t.set(39, 34, 36, "minecraft:cracked_stone_bricks")
    t.set(11, 35, 14, "minecraft:mossy_stone_bricks")

    # Two restrained optional encounter niches only in D3 and away from proof,
    # staff stair, freight core and west secondary egress.
    t.spawner(18, 31, 26, "minecraft:zombie", count=1, nearby=4)
    t.spawner(34, 24, 32, "minecraft:spider", count=1, nearby=3)

    # Deterministic handbook proof remains at the controlled Level-0 records/demo node.
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    _assert_vertical_routes(t)
    _assert_identity(t)
    _assert_proof_chest(t)
    if _count_block(t, "minecraft:spawner") != 2:
        raise AssertionError("OWS-004 D3 encounter contract requires exactly two optional spawners")
    if _count_block(t, "minecraft:mycelium") < 90:
        raise AssertionError("OWS-004 D3 removed too much surviving cultivation evidence")
    if _count_block(t, "create:fluid_pipe") < 70:
        raise AssertionError("OWS-004 D3 removed too much surviving environmental-service evidence")
    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows004_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        size, blocks = unpack_structure(temp_nbt)
        return render_review_set(
            target="OWS-004",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows004_gate_c_damage_states.build_{label}()",
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
    if state.get("active_target") != "OWS-004":
        print(f"Gate-C OWS-004 renderer skipped: active target is {state.get('active_target')}")
        return
    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate.get("status") not in {
        "ready_for_damage_implementation",
        "ready_to_render",
        "rerender_required",
    }:
        print(f"Gate-C OWS-004 renderer skipped: status={gate.get('status')}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()
    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if d1_changes < 35:
        raise AssertionError(f"OWS-004 D1 containment is too weak to review: changed_positions={d1_changes}")
    if d3_changes < 180:
        raise AssertionError(f"OWS-004 D3 long-term ruin is too weak to review: changed_positions={d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"OWS-004 D3 must be materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows004_fixed_v1")
    manifests = {
        "D0": _render_state("d0", "D0 intact / normal industrial agriculture", d0, f"gate-c-r1@{revision}", camera_set),
        "D1": _render_state("d1", "D1 localized active containment", d1, f"gate-c-r1@{revision}", camera_set),
        "D3": _render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r1@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-004",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r1@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows004_gate_b_intact_r4.build_gate_b_intact_r4",
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 2,
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
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_c_damage_states.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-004 Gate C r1: D1 changes={d1_changes}, D3 changes={d3_changes}; manual visual review remains pending.")


if __name__ == "__main__":
    main()

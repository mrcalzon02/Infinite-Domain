#!/usr/bin/env python3
"""[SYSTEM REPORT] Render OWS-001 Gate-C D0/D1/D3 historical review states.

Gate C is review-only. It derives every state from the accepted Gate-B r3 D0
building, applies the recorded Pass 13-18 historical/environmental decisions,
and enforces protected circulation, identity, cold-chain and proof invariants.
It does not replace the authoritative shipping NBT until a later Gate-D pass.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import generate_wasteland_sites as base
import render_ows001_gate_b_intact as gate_b
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_c_damage_states" / "r1"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_001_vcf_neighborhood_culture_service_depot"


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(
        1
        for pos in positions
        if gate_b._block_name(a, *pos) != gate_b._block_name(b, *pos)
    )


def _assert_proof_chest(t: base.Template, x: int, y: int, z: int) -> None:
    row = t.blocks.get((x, y, z))
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


def _assert_primary_identity(t: base.Template) -> None:
    for pos, label in (((15, 7, 2), "VERDANT CONTINUUM FOODS"), ((22, 7, 2), "facility identity")):
        if gate_b._block_name(t, *pos) != "minecraft:oak_wall_sign":
            raise AssertionError(f"D3 no longer preserves {label} sign at {pos}")


def _assert_d3_routes(t: base.Template) -> None:
    # Main public entry and clear interior orientation path.
    gate_b._assert_door(t, 18, 2, 3, "public entrance")
    gate_b._assert_clear(t, (18, 2, 4), (18, 3, 10), "public entrance approach")

    # Approved Gate-B navigation and process routes remain intact.
    gate_b._assert_clear(t, (17, 2, 12), (19, 3, 30), "D3 central three-block staff spine")
    gate_b._assert_clear(t, (17, 2, 22), (25, 3, 22), "D3 receiving-to-clean-stock route")
    gate_b._assert_door(t, 26, 2, 22, "D3 clean-stock route control")
    gate_b._assert_clear(t, (17, 2, 26), (23, 3, 26), "D3 records approach")
    gate_b._assert_door(t, 24, 2, 26, "D3 supervisor-records route control")

    # Rear service opening remains a usable alternate exit.
    gate_b._assert_clear(t, (17, 2, 31), (19, 3, 31), "D3 rear receiving exit")

    # Locker aisle remains reconstructable and navigable despite cold-side decay.
    gate_b._assert_clear(t, (21, 2, 13), (23, 3, 19), "D3 culture-locker service aisle")


def build_d0() -> base.Template:
    """Accepted Gate-B r3 intact baseline."""
    return gate_b.build_gate_b_intact()


def build_d1() -> base.Template:
    """Early anomaly: operational strain, not structural collapse."""
    t = gate_b.build_gate_b_intact()

    # West quality-control pressure: localized inspection floor coding and extra
    # suspect/replacement stock increase normal hold pressure without inventing a
    # quarantine wing or blocking the return-processing route.
    t.fill((8, 1, 21), (10, 1, 23), "minecraft:yellow_concrete")
    t.set(8, 2, 21, "immersiveengineering:crate")
    t.set(10, 2, 21, "minecraft:barrel")

    # Sanitation replacement stock appears beside the wet line as seals/liners
    # are being serviced more often. The wash stations remain operational.
    t.set(10, 2, 18, "immersiveengineering:crate")
    t.set(10, 3, 18, "minecraft:barrel")

    # One clean-side service interface receives temporary inspection coding and
    # a maintenance crate; the cold chain as a whole remains in service.
    t.fill((27, 1, 16), (27, 1, 19), "minecraft:yellow_concrete")
    t.set(27, 2, 18, "immersiveengineering:crate")

    # Batch/temperature exceptions begin accumulating at receiving. This is a
    # measurable quality problem, not an emergency-command conversion.
    t.fill((20, 1, 24), (22, 1, 25), "minecraft:yellow_concrete")
    t.set(22, 3, 24, "minecraft:barrel")

    # A restrained temporary warning field in the return/service area makes D1
    # visible in primitive review while permanent VCF identity remains dominant.
    t.fill((11, 4, 22), (11, 5, 23), "minecraft:yellow_concrete")

    # D1 must retain every intact circulation contract.
    gate_b._assert_clear(t, (21, 2, 13), (23, 3, 19), "D1 culture-locker service aisle")
    gate_b._assert_clear(t, (17, 2, 12), (19, 3, 30), "D1 central staff spine")
    gate_b._assert_clear(t, (17, 2, 22), (25, 3, 22), "D1 accepted-goods route")
    gate_b._assert_door(t, 26, 2, 22, "D1 clean-stock route control")
    gate_b._assert_clear(t, (17, 2, 26), (23, 3, 26), "D1 records approach")
    gate_b._assert_door(t, 24, 2, 26, "D1 records route control")

    return t


def build_d3() -> base.Template:
    """Centuries-later ruin caused by weather, water and failed maintenance."""
    t = build_d1()

    # ------------------------------------------------------------------
    # Primary causal failure: roof cold-plant/service joint water ingress.
    # One localized opening interrupts the service deck and refrigerant feed;
    # it is deliberately not a random peppering of holes across every roof.
    # ------------------------------------------------------------------
    t.clear((28, 9, 18), (30, 10, 20))
    t.fill((28, 1, 18), (29, 1, 20), "minecraft:mossy_stone_bricks")
    t.fill((30, 1, 18), (30, 1, 20), "minecraft:cracked_stone_bricks")
    t.fill((35, 2, 18), (35, 4, 20), "minecraft:mossy_stone_bricks")
    t.clear((28, 2, 17), (28, 3, 17))  # one failed cooler bank segment
    t.set(29, 2, 19, "minecraft:cobweb")

    # ------------------------------------------------------------------
    # West return/sanitation decay around wet service penetrations.
    # The annex is damaged locally but not erased, preserving its function.
    # ------------------------------------------------------------------
    t.clear((4, 7, 19), (6, 7, 22))
    t.clear((3, 5, 19), (3, 6, 21))
    t.fill((4, 1, 20), (6, 1, 22), "minecraft:mossy_stone_bricks")
    t.fill((3, 2, 22), (3, 4, 23), "minecraft:cracked_stone_bricks")
    t.set(5, 3, 21, "minecraft:cobweb")

    # ------------------------------------------------------------------
    # Rear receiving weather exposure. Damage stays to the side pockets and
    # loading edge so the staff spine and records route remain readable.
    # ------------------------------------------------------------------
    t.fill((13, 1, 29), (16, 1, 30), "minecraft:gravel")
    t.fill((20, 1, 29), (22, 1, 30), "minecraft:coarse_dirt")
    t.clear((13, 2, 28), (14, 3, 29))
    t.set(15, 2, 30, "minecraft:gravel")
    t.set(22, 2, 30, "minecraft:cobweb")

    # Public frontage remains the most recognizable part of the ruin. Several
    # panes are lost, but the double entry and primary identity are preserved.
    for pos in ((14, 3, 3), (14, 4, 3), (23, 2, 3), (23, 3, 3), (24, 4, 3)):
        t.set(*pos, "minecraft:air")

    # A few localized masonry substitutions show long weathering without turning
    # every surviving VCF surface into generic brown rubble.
    t.fill((8, 2, 18), (8, 4, 19), "minecraft:cracked_stone_bricks")
    t.fill((10, 2, 26), (11, 3, 26), "minecraft:mossy_stone_bricks")

    # Deterministic narrative proof remains in the plausible records location.
    t.chest(25, 2, 28, PROOF_LOOT_TABLE, facing="west")

    _assert_d3_routes(t)
    _assert_primary_identity(t)
    _assert_proof_chest(t, 25, 2, 28)

    # Enough refrigeration hardware must survive to explain the original system.
    cooler_count = sum(
        1
        for pos in t.blocks
        if gate_b._block_name(t, *pos) == "oritech:cooler_block"
    )
    if cooler_count < 12:
        raise AssertionError(f"D3 preserves too little refrigeration evidence: {cooler_count} cooler blocks")

    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows001_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        size, blocks = unpack_structure(temp_nbt)
        return render_review_set(
            target="OWS-001",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=camera_set,
        )
    finally:
        temp_nbt.unlink(missing_ok=True)


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-001":
        print(f"Gate-C OWS-001 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    status = gate.get("status", "not_started")
    if status not in {"implementation_ready", "ready_to_render", "rerender_required"}:
        print(f"Gate-C OWS-001 renderer skipped: status={status}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()

    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if not 12 <= d1_changes <= 120:
        raise AssertionError(f"D1 change count {d1_changes} is not a restrained but visible anomaly overlay")
    if not 40 <= d3_changes <= 260:
        raise AssertionError(f"D3 change count {d3_changes} is not a localized causal ruin pass")
    if d3_changes <= d1_changes:
        raise AssertionError("D3 must be materially more changed than D1")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows001_fixed_v1")
    manifests = {
        "d0": _render_state("d0", "D0 intact / normal operation", d0, f"gate-c-r1-d0@{revision}", camera_set),
        "d1": _render_state("d1", "D1 early anomaly / operational strain", d1, f"gate-c-r1-d1@{revision}", camera_set),
        "d3": _render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r1-d3@{revision}", camera_set),
    }

    aggregate = {
        "target": "OWS-001",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r1@{revision}",
        "source_commit": os.environ.get("GITHUB_SHA", "working-tree"),
        "fixed_camera_set": camera_set,
        "visual_review_status": "rendered_pending_manual_review",
        "states": {
            key: str((OUTPUT_DIR / key / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
            for key in ("d0", "d1", "d3")
        },
        "change_counts_from_d0": {"d1": d1_changes, "d3": d3_changes},
        "protected_invariants_asserted": [
            "public entrance",
            "central three-block staff spine",
            "culture-locker three-block aisle",
            "receiving-to-clean-stock route",
            "supervisor-records route",
            "rear receiving exit",
            "primary VCF identity",
            "surviving refrigeration evidence",
            "guaranteed supervisor-records proof chest",
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
    gate["review_stage_source"] = "scripts/render_ows001_gate_c_damage_states.py"
    gate["review_only"] = True
    gate["d1_change_count"] = d1_changes
    gate["d3_change_count"] = d3_changes
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        "Rendered OWS-001 Gate C r1 D0/D1/D3 using "
        f"{camera_set}; changes d1={d1_changes}, d3={d3_changes}; manual visual approval remains pending."
    )


if __name__ == "__main__":
    main()

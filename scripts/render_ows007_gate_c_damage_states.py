#!/usr/bin/env python3
<<<<<<< Updated upstream
"""Render OWS-007 Gate-C D0/D1/D3 historical review states.

D0 is the exact independently accepted Gate-B r2 model. D1 adds a localized
commercial repeat-validation program without turning this pre-crisis site into
a containment facility. D3 derives causal weathering from environmental-plant,
trial-monitor and rotunda-conditioning failures, then adds target gameplay.
This review-only tool never writes shipping NBT or shared state.
=======
"""Render OWS-007 Gate-C r1 D0/D1/D3 historical states.

D0 is the exact independently accepted Gate-B r2 model. D1 adds controlled
durability-test escalation. D3 grows restrained, causal abandonment damage,
bounded encounters and exactly one canonical proof node from that condition.
The module is review-only and never writes shared state or shipping NBT.
>>>>>>> Stashed changes
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
<<<<<<< Updated upstream
from render_ows007_gate_b_intact import _assert_intact_contracts
from render_ows007_gate_b_intact_r2 import build_gate_b_intact_r2


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-007" / "gate_c_damage_states" / "r1"
=======
import render_ows007_gate_b_intact as gate_b_r1
import render_ows007_gate_b_intact_r2 as gate_b_r2


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-007" / "gate_c_damage_states" / "r1"
>>>>>>> Stashed changes
SHIPPING_PATH = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" /
    "old_world" / "ows_007_vcf_ep7_agricultural_development_laboratory.nbt"
)
ACCEPTED_GATE_B_SHA256 = "b116ad94acd595414ca670d4f5205bed69e4116724167a6397a8504acb0ba67a"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_007_vcf_ep7_agricultural_development_laboratory"
<<<<<<< Updated upstream
PROOF_POS = (43, 2, 56)
SPAWNERS = (
    (4, 2, 47, "minecraft:spider"),
    (15, 2, 34, "minecraft:zombie"),
    (25, 2, 34, "minecraft:skeleton"),
    (63, 2, 38, "minecraft:spider"),
)
=======
PROOF_POS = (43, 2, 55)
SPAWNER_POSITIONS = ((5, 2, 36), (20, 2, 39), (63, 2, 30))
>>>>>>> Stashed changes
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_DOCS = tuple(f"OWS-007_PASS{number}_{name}.md" for number, name in (
    (13, "HISTORICAL_LAYERING"),
    (14, "ENVIRONMENTAL_NARRATIVE"),
    (15, "ENCOUNTER_ARCHITECTURE"),
    (16, "LOOT_ARCHITECTURE"),
    (17, "QUEST_PROOF_ARCHITECTURE"),
    (18, "DAMAGE_AND_DECAY"),
))


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


<<<<<<< Updated upstream
def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if _name(a, pos) != _name(b, pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)
=======
def _diff_positions(a: base.Template, b: base.Template) -> set[tuple[int, int, int]]:
    positions = set(a.blocks) | set(b.blocks)
    return {pos for pos in positions if _name(a, pos) != _name(b, pos)}


def _diff_count(a: base.Template, b: base.Template) -> int:
    return len(_diff_positions(a, b))


def _count_block(t: base.Template, block: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == block)
>>>>>>> Stashed changes


def _assert_history_authorized() -> None:
    review_dir = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"
    review = review_dir / "OWS-007_GATE_B_R2_REVIEW.md"
    if not review.exists() or "OWS-007 GATE B r2: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-007 Gate-B r2 PASSED review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: required Pass 13-18 records are missing: {missing}")


<<<<<<< Updated upstream
def build_d0() -> base.Template:
    t = build_gate_b_intact_r2()
    _assert_intact_contracts(t)
=======
def _assert_corrected_facade(t: base.Template) -> None:
    for z in gate_b_r2.MULLION_Z:
        for y in gate_b_r2.MULLION_Y:
            expected = "minecraft:light_gray_concrete" if y == gate_b_r2.BEAM_Y else "minecraft:white_concrete"
            if _name(t, (1, y, z)) != expected:
                raise AssertionError(f"Accepted Gate-B r2 mullion lost at {(1, y, z)}")
    for z in gate_b_r2.BEAM_Z:
        if _name(t, (1, gate_b_r2.BEAM_Y, z)) != "minecraft:light_gray_concrete":
            raise AssertionError(f"Accepted Gate-B r2 horizontal beam lost at z={z}")


def build_d0() -> base.Template:
    r1 = gate_b_r1.build_gate_b_intact()
    t = gate_b_r2.build_gate_b_intact_r2()
    gate_b_r2._assert_r2_scope(r1, t)
    gate_b_r1._assert_intact_contracts(t)
    _assert_corrected_facade(t)
>>>>>>> Stashed changes
    return t


def build_d1() -> base.Template:
<<<<<<< Updated upstream
    """Late commercial repeat validation after unusually durable results."""
    t = build_d0()

    # Chamber B becomes a repeat-validation field, but its two-block central
    # route remains visually and mechanically distinct.
    t.fill((18, 1, 32), (29, 1, 44), "minecraft:yellow_concrete")
    t.fill((22, 1, 32), (25, 1, 44), "minecraft:smooth_stone")
    t.fill((19, 2, 33), (21, 5, 35), "minecraft:barrel", facing="up", open="false")
    t.fill((26, 2, 33), (28, 5, 35), "oritech:cooler_block")

    # A temporary comparison header feeds repeat cold/dry and reseeding trials.
    # It branches from the accepted environmental manifold rather than becoming
    # unrelated decorative pipework.
    t.fill((18, 9, 34), (64, 9, 34), "create:fluid_pipe")
    for x in (20, 27, 36, 51, 63):
        t.fill((x, 6, 34), (x, 9, 34), "create:fluid_pipe")
        t.set(x, 8, 35, "create:mechanical_pump", facing="south")

    # The hinge receives duplicated recovered-stock germination and scan work.
    t.fill((29, 1, 42), (36, 1, 50), "minecraft:yellow_concrete")
    t.fill((31, 2, 43), (35, 2, 44), "farmersdelight:rich_soil")
    for x in (31, 33, 35):
        t.set(x, 3, 43, "minecraft:wheat")
    t.fill((31, 2, 48), (35, 2, 49), "create:depot")
    for x in (31, 33, 35):
        t.set(x, 3, 48, "ae2:terminal")

    # Secure records and receiving gain retained commercial-release lots.
    t.fill((6, 2, 52), (8, 4, 54), "immersiveengineering:crate")
    t.fill((10, 2, 52), (12, 4, 54), "immersiveengineering:crate")
    t.fill((41, 2, 55), (45, 2, 55), "minecraft:bookshelf")

    # Rotunda sectors repeat the extreme-survival comparison as an ordinary
    # product decision. Yellow means commercial hold, not quarantine.
    t.fill((49, 1, 27), (54, 1, 32), "minecraft:yellow_concrete")
    t.fill((60, 1, 38), (65, 1, 43), "minecraft:yellow_concrete")
    t.fill((50, 2, 31), (53, 4, 32), "create:cardboard_block")
    t.fill((61, 2, 38), (64, 4, 39), "create:cardboard_block")

    base.wall_sign(t, 19, 6, 32, "south", "STRESS LOT 07", "REPEAT VALIDATION")
    base.wall_sign(t, 31, 6, 42, "south", "RECOVERED STOCK", "RESEED / COMPARE")
    base.wall_sign(t, 44, 6, 55, "north", "PERSISTENCE REVIEW", "COMMERCIAL HOLD")
    base.wall_sign(t, 52, 6, 27, "north", "DISTRIBUTION TRIAL", "EXTREME SURVIVAL")

    _assert_intact_contracts(t)
=======
    """Show intact corporate escalation after unusually strong EP-7 results."""
    t = build_d0()

    # Expanded heat/dry and cold/soak condition bands flank, but never occupy,
    # the two-wide Chamber-B center aisle.
    for z1, z2 in ((18, 27), (34, 43)):
        t.fill((18, 1, z1), (21, 1, z2), "minecraft:orange_concrete")
        t.fill((26, 1, z1), (29, 1, z2), "minecraft:yellow_concrete")

    # The rotunda's north sectors receive legible extended-cycle floor zoning.
    t.fill((50, 1, 28), (54, 1, 32), "minecraft:orange_concrete")
    t.fill((60, 1, 28), (64, 1, 32), "minecraft:light_blue_concrete")

    # Temporary bypass headers connect the accelerated chamber and rotunda to
    # the accepted west environmental spine without changing routes or massing.
    t.fill((6, 13, 32), (24, 13, 32), "create:fluid_pipe")
    t.fill((24, 13, 32), (24, 17, 38), "create:fluid_pipe")
    t.fill((24, 17, 38), (57, 17, 38), "create:fluid_pipe")
    for x, z, facing in ((8, 32, "east"), (24, 35, "south"), (43, 38, "east")):
        t.set(x, 13 if x != 43 else 17, z, "create:mechanical_pump", facing=facing)
    t.fill((20, 6, 35), (21, 8, 37), "immersiveengineering:sheetmetal_steel")
    t.fill((26, 6, 35), (28, 8, 37), "oritech:cooler_block")

    # Additional release stock and condition-control surfaces remain bounded to
    # their established rooms and do not become arbitrary loot nodes.
    t.fill((8, 2, 52), (10, 3, 54), "immersiveengineering:crate")
    t.fill((41, 2, 54), (42, 3, 54), "minecraft:barrel", facing="up", open="false")
    base.wall_sign(t, 18, 7, 33, "north", "EXTENDED CYCLE", "HEAT / DRY")
    base.wall_sign(t, 26, 7, 33, "north", "EXTENDED CYCLE", "COLD / SOAK")
    base.wall_sign(t, 41, 6, 54, "south", "PERSISTENCE RELEASE", "STOCK HOLD")
    base.wall_sign(t, 54, 8, 28, "north", "DURABILITY ROTUNDA", "EXTENDED RUN")

    gate_b_r1._assert_intact_contracts(t)
    _assert_corrected_facade(t)
>>>>>>> Stashed changes
    return t


def build_d3() -> base.Template:
<<<<<<< Updated upstream
    """Centuries-later ruin caused by abandonment and service-system failure."""
    t = build_d1()

    # The west environmental plant loses its upper conditioning mass. The
    # resulting weather path breaks only glass between the accepted r2 frames
    # and drops service debris at the base of the spine.
    t.clear((7, 21, 46), (13, 25, 50))
    t.clear((4, 20, 44), (7, 22, 49))
    t.clear((1, 12, 23), (1, 18, 28))
    t.fill((3, 1, 44), (7, 1, 49), "minecraft:mossy_stone_bricks")
    t.fill((4, 2, 46), (7, 3, 49), "minecraft:gravel")
    t.set(6, 4, 48, "minecraft:cobweb")

    # Chamber B's repeat-validation monitor fails along a connected roof edge.
    # Debris lands beside, not in, the protected central trial aisle.
    t.clear((22, 22, 25), (28, 23, 37))
    t.clear((25, 18, 34), (28, 21, 38))
    t.clear((25, 4, 12), (28, 8, 12))
    t.fill((18, 1, 33), (21, 1, 40), "minecraft:mossy_stone_bricks")
    t.fill((19, 2, 35), (21, 3, 39), "minecraft:gravel")
    t.set(20, 4, 38, "minecraft:cobweb")

    # The rotunda conditioning cap and east glazing fail together. Radial ribs,
    # the bridge, west half and central control remain readable.
    t.clear((61, 22, 30), (69, 28, 41))
    t.clear((66, 13, 31), (70, 21, 40))
    t.fill((61, 1, 35), (66, 1, 42), "minecraft:cracked_stone_bricks")
    t.fill((62, 2, 36), (66, 3, 41), "minecraft:gravel")
    t.set(64, 4, 39, "minecraft:cobweb")

    # Phenotyping/reseeding roof damage follows the failed comparison header.
    # A connected opening and fallen panels affect the repeat-test half while
    # the food-quality / secure-record side and proof route survive.
    t.clear((29, 12, 44), (36, 16, 50))
    t.clear((31, 10, 46), (35, 11, 49))
    t.fill((29, 1, 44), (34, 1, 49), "minecraft:mossy_stone_bricks")
    t.fill((30, 2, 46), (34, 3, 49), "minecraft:gravel")

    # Persistent EP-7 growth follows nutrient water and retained-stock routes.
    # It is causal evidence of the traits under study, not blanket vegetation.
    for x1, x2, z1, z2 in (
        (7, 10, 37, 40),
        (19, 21, 33, 39),
        (32, 34, 44, 49),
        (61, 65, 37, 41),
    ):
        t.fill((x1, 1, z1), (x2, 1, z2), "minecraft:mycelium")
    for x, z in ((8, 38), (10, 40), (20, 34), (21, 39), (33, 45), (34, 49), (62, 38), (65, 40)):
        t.set(x, 2, z, "minecraft:brown_mushroom")

    # The accepted architecture and controlled routes must survive before
    # deferred gameplay blocks are installed.
    _assert_intact_contracts(t)

    # One guaranteed proof at the secure commercial-release records node.
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    # Four discoverable vanilla encounters form service, reference, stress and
    # optional rotunda pressure. No explosive mob threatens the proof.
    for x, y, z, mob in SPAWNERS:
        t.spawner(x, y, z, mob, count=1, nearby=4)
=======
    """Grow restrained long-abandonment damage from the D1 conditioning load."""
    t = build_d1()

    # Chamber-B monitor glazing fails first under freeze/thaw. Openings are
    # limited, retain the steel portal frames and land debris below.
    t.clear((21, 23, 27), (26, 23, 33))
    t.clear((20, 19, 26), (20, 22, 35))
    t.clear((27, 19, 34), (28, 21, 39))
    t.clear((19, 18, 34), (25, 18, 41))
    t.fill((19, 17, 34), (25, 17, 41), "minecraft:cracked_stone_bricks")
    for pos in ((21, 2, 36), (27, 2, 39), (19, 2, 41), (26, 3, 40), (28, 2, 35)):
        t.set(*pos, "minecraft:gravel")

    # The overworked west plant crown loses local cladding and drains toward the
    # same chamber branch. Debris lands on the surviving lower plant deck.
    t.clear((8, 20, 46), (12, 25, 49))
    t.clear((5, 18, 45), (7, 21, 49))
    t.fill((7, 17, 45), (12, 17, 49), "minecraft:weathered_cut_copper")
    t.fill((8, 16, 46), (11, 16, 49), "minecraft:gravel")
    t.fill((5, 1, 38), (7, 1, 47), "minecraft:mossy_stone_bricks")
    for pos in ((6, 2, 39), (7, 2, 43), (5, 3, 46)):
        t.set(*pos, "minecraft:cobweb")

    # A restrained water path follows the stress-chamber and wash/decon drain;
    # all asserted center aisles remain untouched at head height.
    t.fill((18, 1, 41), (21, 1, 45), "minecraft:mossy_stone_bricks")
    t.fill((26, 1, 40), (29, 1, 45), "minecraft:coarse_dirt")
    t.fill((30, 1, 52), (37, 1, 55), "minecraft:mossy_stone_bricks")
    t.clear((31, 8, 53), (37, 9, 57))
    t.fill((31, 7, 53), (37, 7, 55), "minecraft:cracked_stone_bricks")
    for pos in ((31, 2, 53), (35, 2, 54), (37, 2, 52)):
        t.set(*pos, "minecraft:brown_mushroom")

    # The conditioning cap leaks only above the humidity side. Radial ribs,
    # annular overlook, central control and broad bridge remain reconstructable.
    t.clear((59, 24, 39), (62, 28, 40))
    t.clear((58, 29, 36), (61, 29, 39))
    t.fill((59, 23, 36), (62, 23, 39), "minecraft:weathered_cut_copper")
    t.fill((61, 1, 39), (65, 1, 43), "minecraft:mossy_stone_bricks")
    t.fill((62, 2, 40), (65, 2, 42), "farmersdelight:rich_soil")
    for pos, crop in (((62, 3, 40), "minecraft:wheat"), ((64, 3, 41), "minecraft:beetroots"), ((65, 3, 42), "minecraft:wheat")):
        t.set(*pos, crop)

    # Weathering remains localized and readable rather than noisy block scatter.
    t.fill((20, 1, 42), (20, 1, 45), "minecraft:moss_block")
    t.fill((27, 1, 41), (28, 1, 44), "minecraft:moss_block")
    t.set(21, 3, 43, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")
    t.set(62, 4, 41, "minecraft:vine", north="true", east="false", south="false", west="false", up="false")

    # Prove accepted architecture and routes before adding Gate-C-only gameplay.
    gate_b_r1._assert_intact_contracts(t)
    _assert_corrected_facade(t)

    # Exactly one canonical proof/loot node in secure release records.
    t.clear((42, 2, 55), (44, 4, 55))
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="south")

    # Three bounded encounters follow the failed-service path off main routes.
    t.clear((4, 2, 35), (6, 3, 37))
    t.spawner(5, 2, 36, "minecraft:spider", count=1, nearby=3)
    t.clear((19, 2, 38), (21, 3, 40))
    t.spawner(20, 2, 39, "minecraft:zombie", count=1, nearby=4)
    t.clear((62, 2, 29), (64, 3, 31))
    t.spawner(63, 2, 30, "minecraft:skeleton", count=1, nearby=3)
>>>>>>> Stashed changes

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
<<<<<<< Updated upstream
        raise AssertionError("OWS-007 D3 proof chest is missing")
=======
        raise AssertionError("OWS-007 canonical proof chest is missing")
>>>>>>> Stashed changes
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-007 proof position contains {t.palette[state_id]['Name']}")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-007 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
<<<<<<< Updated upstream
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-007 proof chest has no clear block above")
    matching = sum(
        1 for _, block_nbt in t.blocks.values()
        if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE
    )
    if matching != 1:
        raise AssertionError(f"OWS-007 must contain exactly one canonical proof container; found {matching}")
=======
    if _name(t, (43, 3, 55)) not in AIR or _name(t, (43, 2, 56)) not in AIR:
        raise AssertionError("OWS-007 proof chest or its south approach is obstructed")
    matching = sum(1 for _, nbt in t.blocks.values() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-007 requires exactly one canonical proof node; found {matching}")
>>>>>>> Stashed changes


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
<<<<<<< Updated upstream
    names = [_name(t, pos) for pos in t.blocks]
    if names.count("minecraft:spawner") != len(SPAWNERS):
        raise AssertionError(f"OWS-007 D3 requires exactly {len(SPAWNERS)} deliberate encounter spawners")
    for pos in SPAWNERS:
        row = t.blocks.get(pos[:3])
        if row is None or t.palette[row[0]]["Name"] != "minecraft:spawner":
            raise AssertionError(f"OWS-007 encounter missing at {pos[:3]}")
        entity = None if not row[1] else row[1].get("SpawnData", {}).get("entity", {}).get("id")
        if entity != pos[3] or not entity.startswith("minecraft:") or entity == "minecraft:creeper":
            raise AssertionError(f"Unauthorized OWS-007 encounter at {pos[:3]}: {entity}")
        distance = sum(abs(pos[i] - PROOF_POS[i]) for i in range(3))
        if distance < 12:
            raise AssertionError(f"OWS-007 encounter is too close to proof at {pos[:3]}")

    if sum(name is not None and name.endswith("_wall_sign") for name in names) < 20:
        raise AssertionError("OWS-007 D3 preserves too little institutional/process wayfinding")
    for pos in ((12, 7, 5), (29, 7, 5), (21, 6, 12), (41, 11, 29)):
        name = _name(t, pos)
        if name is None or not name.endswith("_wall_sign"):
            raise AssertionError(f"OWS-007 D3 lost primary identity/process sign at {pos}")
    if _count_block(t, "create:fluid_pipe") < 170:
        raise AssertionError("OWS-007 D3 removed too much environmental-service anatomy")
    if _count_block(t, "farmersdelight:rich_soil") < 55:
        raise AssertionError("OWS-007 D3 removed too much crop-comparison evidence")
    if _name(t, (24, 2, 5)) != "minecraft:iron_door":
        raise AssertionError("OWS-007 D3 public entrance no longer functions")
    if _name(t, (43, 2, 57)) not in AIR or _name(t, (43, 3, 57)) not in AIR:
        raise AssertionError("OWS-007 D3 proof approach is obstructed")


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()
=======
    _assert_corrected_facade(t)
    if tuple(t.size) != (73, 33, 63):
        raise AssertionError(f"OWS-007 D3 bounds changed: {t.size}")
    if _count_block(t, "minecraft:spawner") != 3:
        raise AssertionError("OWS-007 D3 requires exactly three bounded spawners")
    for pos in SPAWNER_POSITIONS:
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 12:
            raise AssertionError(f"Encounter is too close to proof at {pos}")
    # Principal route and chamber thresholds survive intact.
    for x, z in ((24, 5), (24, 11), (9, 15), (11, 15), (22, 13), (35, 16), (11, 59), (35, 59)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-007 D3 route lost controlled door at {(x + dx, y, z)}")
    if _count_block(t, "create:fluid_pipe") < 170:
        raise AssertionError("OWS-007 D3 removed too much environmental-system anatomy")
    if _count_block(t, "farmersdelight:rich_soil") < 65:
        raise AssertionError("OWS-007 D3 removed too much agricultural program evidence")
    signs = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if signs < 22:
        raise AssertionError(f"OWS-007 D3 preserves too little VCF identity: {signs} signs")


def _model_sha(t: base.Template, label: str) -> str:
    temp_name = f"_heavy_review_ows007_gate_c_hash_{label}"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)
>>>>>>> Stashed changes


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str) -> tuple[dict, str]:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    temp_name = f"_heavy_review_ows007_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        model_bytes = temp_nbt.read_bytes()
        model_sha = hashlib.sha256(model_bytes).hexdigest()
        size, blocks = unpack_structure(temp_nbt)
        manifest = render_review_set(
            target="OWS-007", gate="gate_c_damage_states", revision=revision,
            damage_state=damage_state, source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows007_gate_c_damage_states.build_{label}()",
<<<<<<< Updated upstream
            size=size, blocks=blocks, output_dir=OUTPUT_DIR / label,
            camera_set="ows007_fixed_v1",
=======
            size=size, blocks=blocks, output_dir=OUTPUT_DIR / label, camera_set="ows007_fixed_v1",
>>>>>>> Stashed changes
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

    states = ("D0", "D1", "D3")
<<<<<<< Updated upstream
    views = ("front_left", "rear_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w = 390
    margin = 16
    header_h = 88
    label_h = 24
=======
    views = ("front_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w, margin, header_h, label_h = 420, 16, 88, 24
>>>>>>> Stashed changes
    loaded: dict[tuple[str, str], Image.Image] = {}
    row_heights: list[int] = []
    for view in views:
        row_images = []
        for state in states:
<<<<<<< Updated upstream
            path = ROOT / manifests[state]["views"][view]
            image = Image.open(path).convert("RGB")
=======
            image = Image.open(ROOT / manifests[state]["views"][view]).convert("RGB")
>>>>>>> Stashed changes
            ratio = thumb_w / max(1, image.width)
            image = image.resize((thumb_w, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
            loaded[(state, view)] = image
            row_images.append(image)
        row_heights.append(max(image.height for image in row_images) + label_h)
<<<<<<< Updated upstream

    sheet_w = margin * 4 + thumb_w * 3
    sheet_h = header_h + sum(row_heights) + margin * (len(views) + 1)
    sheet = Image.new("RGB", (sheet_w, sheet_h), (20, 22, 24))
=======
    sheet = Image.new("RGB", (margin * 4 + thumb_w * 3, header_h + sum(row_heights) + margin * 5), (20, 22, 24))
>>>>>>> Stashed changes
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), "OWS-007 — Gate C r1 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), "dimensions=73x33x63  camera_set=ows007_fixed_v1", fill=(210, 210, 210))
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


<<<<<<< Updated upstream
def main() -> None:
    _assert_history_authorized()
    shipping_before = git_hash_object(SHIPPING_PATH)
    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()
    d1_changes = _diff_count(d0, d1)
    d3_changes = _diff_count(d0, d3)
    if d1_changes < 250:
        raise AssertionError(f"OWS-007 D1 intervention is too weak to review: {d1_changes}")
    if d3_changes < 750:
=======
def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def main() -> None:
    _assert_history_authorized()
    shipping_before = git_hash_object(SHIPPING_PATH)
    d0, d1, d3 = build_d0(), build_d1(), build_d3()
    d0_sha = _model_sha(d0, "d0_preflight")
    if d0_sha != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(f"OWS-007 D0 drifted from accepted Gate B r2: {d0_sha} != {ACCEPTED_GATE_B_SHA256}")

    d1_changes, d3_changes = _diff_count(d0, d1), _diff_count(d0, d3)
    if d1_changes < 180:
        raise AssertionError(f"OWS-007 D1 escalation is too weak to review: {d1_changes}")
    if d3_changes < 520:
>>>>>>> Stashed changes
        raise AssertionError(f"OWS-007 D3 ruin is too weak to review: {d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"OWS-007 D3 must exceed twice D1: D1={d1_changes}, D3={d3_changes}")

    revision = f"gate-c-r1@{os.environ.get('GITHUB_SHA', 'local')[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 accepted intact operation", d0, revision),
<<<<<<< Updated upstream
        "D1": _serialize_and_render("d1", "D1 commercial repeat validation", d1, revision),
        "D3": _serialize_and_render("d3", "D3 centuries-later causal ruin", d3, revision),
=======
        "D1": _serialize_and_render("d1", "D1 controlled durability-test escalation", d1, revision),
        "D3": _serialize_and_render("d3", "D3 restrained causal long-abandonment ruin", d3, revision),
>>>>>>> Stashed changes
    }
    manifests = {state: result[0] for state, result in rendered.items()}
    state_hashes = {state: result[1] for state, result in rendered.items()}
    if state_hashes["D0"] != ACCEPTED_GATE_B_SHA256:
<<<<<<< Updated upstream
        raise AssertionError(
            f"OWS-007 Gate-C D0 drifted from accepted Gate B: {state_hashes['D0']} != {ACCEPTED_GATE_B_SHA256}"
        )

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    shipping_after = git_hash_object(SHIPPING_PATH)
    if shipping_after != shipping_before:
        raise AssertionError("OWS-007 shipping NBT changed during Gate-C review rendering")

    gate_manifest = {
        "target": "OWS-007",
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": "ows007_fixed_v1",
        "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_d0": "render_ows007_gate_b_intact_r2.build_gate_b_intact_r2",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": state_hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": state_hashes["D1"],
        "d3_review_model_sha256": state_hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_pre_crisis_site_was_regionally_abandoned_without_a_distinct_site_specific_collapse_event",
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": len(SPAWNERS),
        "authoritative_shipping_modified": False,
        "shipping_nbt_git_blob_before": shipping_before,
        "shipping_nbt_git_blob_after": shipping_after,
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
=======
        raise AssertionError("Rendered OWS-007 D0 no longer matches accepted Gate B r2")

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": "OWS-007", "gate": "gate_c_damage_states", "revision": revision,
        "fixed_camera_set": "ows007_fixed_v1",
        "source_d0": "render_ows007_gate_b_intact_r2.build_gate_b_intact_r2",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": state_hashes["D0"], "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": state_hashes["D1"], "d3_review_model_sha256": state_hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes, "d3_changed_positions_from_d0": d3_changes,
        "corrected_facade_frozen_all_states": True,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_slow_maintenance_withdrawal_has_no_distinct_acute_collapse_phase",
        "proof_position": list(PROOF_POS), "proof_loot_table": PROOF_LOOT_TABLE,
        "canonical_proof_nodes_d3": 1, "deterministic_spawners_d3": 3,
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "authoritative_shipping_modified": False,
        "shipping_nbt_git_blob_before": shipping_before,
        "shipping_nbt_git_blob_after": git_hash_object(SHIPPING_PATH),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    if gate_manifest["shipping_nbt_git_blob_after"] != shipping_before:
        raise AssertionError("OWS-007 shipping NBT changed during Gate-C rendering")
>>>>>>> Stashed changes
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Rendered OWS-007 Gate C r1: D0 exact={state_hashes['D0'] == ACCEPTED_GATE_B_SHA256}, "
        f"D1 changes={d1_changes}, D3 changes={d3_changes}; independent review remains pending."
    )


if __name__ == "__main__":
    main()

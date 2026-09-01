#!/usr/bin/env python3
"""Render OWS-006 Gate-C D0/D1/D3 historical review states.

D0 is byte-identical to the independently accepted Gate-B r1 model. D1 adds a
localized polymer-integrity intervention. D3 grows causal long-term ruin,
encounters and deterministic proof from that failure. Review-only: shared state,
shipping NBT, Pass 19 and final synchronization remain untouched.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import generate_wasteland_sites as base
import render_ows006_gate_b_intact as gate_b


ROOT = Path(__file__).resolve().parents[2]
GATE_ROOT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-006" / "gate_c_damage_states"
R1_DIR = GATE_ROOT / "r1"
OUTPUT_DIR = GATE_ROOT / "r2"
ACCEPTED_GATE_B_SHA256 = "fb1a6c530a3731794547c429e56ab47d93e7082b1157ca255f2790b900a5749e"
FROZEN_D1_R1_SHA256 = "387221cfeaebaf0da5376bda89a05f4d39e896924b99b37da016e2166aa2ad6e"
REJECTED_D3_R1_SHA256 = "f94137e898b545aa024804d1bc8a8571cf1c044eafb7e2a26250f3184756df4a"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_006_vcf_pt9_symbiosis_pilot_laboratory"
PROOF_POS = (54, 2, 40)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_DOCS = tuple(f"OWS-006_PASS{number}_{name}.md" for number, name in (
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


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if _name(a, pos) != _name(b, pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)


def _diff_positions(a: base.Template, b: base.Template) -> set[tuple[int, int, int]]:
    positions = set(a.blocks) | set(b.blocks)
    return {pos for pos in positions if _name(a, pos) != _name(b, pos)}


def _assert_history_authorized() -> None:
    review_dir = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild"
    review = review_dir / "OWS-006_GATE_B_R1_REVIEW.md"
    if not review.exists() or "OWS-006 GATE B r1: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-006 Gate-B r1 PASSED review is missing")
    r1_review = review_dir / "OWS-006_GATE_C_R1_REVIEW.md"
    if not r1_review.exists() or "OWS-006 GATE C r1: REVISION REQUIRED" not in r1_review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C r2 refused: explicit r1 REVISION REQUIRED review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: required Pass 13-18 records are missing: {missing}")


def build_d0() -> base.Template:
    t = gate_b.build_gate_b_intact()
    gate_b._assert_intact_contracts(t)
    return t


def build_d1() -> base.Template:
    """Localized early intervention where PT-9 attacks polymer interfaces."""
    t = build_d0()

    # The pre-existing yellow polymer suite expands into a controlled integrity
    # hold. Floor-only zoning keeps the east-wing route and room anatomy intact.
    t.fill((49, 1, 24), (55, 1, 37), "minecraft:yellow_concrete")
    t.fill((50, 1, 28), (53, 1, 31), "minecraft:smooth_stone")
    t.fill((25, 1, 24), (29, 1, 38), "minecraft:yellow_concrete")
    t.fill((33, 1, 24), (36, 1, 38), "minecraft:yellow_concrete")

    # A traversable polymer-integrity vestibule marks the observed-material hold.
    t.fill((49, 2, 32), (51, 5, 32), "minecraft:white_concrete")
    t.fill((53, 2, 32), (55, 5, 32), "minecraft:white_concrete")
    base.door(t, 52, 2, 32, "south", "iron")
    t.fill((49, 5, 32), (55, 5, 32), "minecraft:yellow_concrete")

    # Failed coupons, replacement filter media and the temporary Chamber-B
    # bypass make the response operational rather than decorative.
    t.fill((50, 2, 34), (53, 3, 36), "tfmg:plastic_block")
    t.fill((49, 2, 28), (51, 3, 30), "immersiveengineering:crate")
    t.fill((33, 6, 33), (36, 6, 37), "create:fluid_pipe")
    t.set(34, 6, 35, "create:mechanical_pump", facing="north")
    t.fill((32, 6, 39), (35, 8, 40), "immersiveengineering:sheetmetal_steel")

    base.wall_sign(t, 50, 6, 32, "north", "POLYMER HOLD", "SEAL INTEGRITY")
    base.wall_sign(t, 33, 7, 39, "north", "CHAMBER B BYPASS", "FILTER WATCH")
    base.wall_sign(t, 50, 6, 28, "south", "FAILED COUPONS", "MATERIAL REVIEW")

    # D1 remains an intact, localized intervention with every accepted route.
    gate_b._assert_intact_contracts(t)
    return t


def _build_d3_r1() -> base.Template:
    """Reconstruct the rejected r1 D3 exactly as the narrow-r2 baseline."""
    t = build_d1()

    # The east material-hold envelope fails first around degraded seals. The
    # stair and secure-record approach farther south remain traversable.
    t.clear((52, 10, 33), (55, 14, 36))
    t.clear((55, 5, 33), (57, 10, 36))
    t.clear((50, 2, 34), (53, 3, 36))
    t.fill((50, 1, 33), (55, 1, 37), "minecraft:mossy_stone_bricks")
    t.fill((51, 2, 34), (53, 3, 36), "minecraft:gravel")
    t.set(50, 3, 35, "minecraft:cobweb")
    t.set(55, 2, 36, "minecraft:brown_mushroom")

    # Chamber B's bypass and environmental monitor fail next. Damage stays off
    # the accepted three-wide center aisle and leaves A/C as readable controls.
    t.clear((33, 14, 32), (36, 18, 38))
    t.clear((34, 8, 34), (36, 13, 38))
    t.fill((33, 1, 33), (36, 1, 38), "minecraft:cracked_stone_bricks")
    t.fill((34, 2, 35), (36, 3, 38), "minecraft:gravel")
    t.set(33, 3, 36, "minecraft:cobweb")
    t.set(35, 2, 38, "minecraft:brown_mushroom")

    # The matching rear manifold branch and local roof service deck weather in
    # the same causal line. The accepted manifold datum at y15 is not touched.
    t.clear((27, 17, 42), (34, 24, 46))
    t.clear((32, 8, 44), (35, 13, 46))
    t.fill((31, 1, 44), (36, 1, 47), "minecraft:mossy_stone_bricks")
    t.fill((33, 2, 44), (36, 3, 46), "minecraft:gravel")
    t.set(32, 3, 45, "minecraft:cobweb")

    # A restrained water path links the failed east envelope to the service
    # yard without inventing an explosion or generalized destruction.
    t.fill((51, 0, 42), (55, 0, 47), "minecraft:coarse_dirt")
    t.fill((48, 1, 44), (52, 1, 47), "minecraft:mossy_stone_bricks")
    t.set(50, 2, 46, "minecraft:brown_mushroom")

    # Prove accepted D0 architecture and circulation before adding deferred
    # gameplay blocks forbidden by Gate B.
    gate_b._assert_intact_contracts(t)

    # Secure principal-review records carry exactly one canonical proof chest.
    t.clear((53, 2, 39), (55, 4, 41))
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    # Three restrained vanilla encounters track the same failure path and stay
    # away from public/chamber center aisles and the proof container.
    t.clear((53, 2, 33), (55, 3, 35))
    t.spawner(54, 2, 34, "minecraft:spider", count=1, nearby=3)
    t.clear((33, 2, 35), (35, 3, 37))
    t.spawner(34, 2, 36, "minecraft:zombie", count=1, nearby=4)
    t.clear((44, 2, 44), (46, 3, 46))
    t.spawner(45, 2, 45, "minecraft:skeleton", count=1, nearby=3)

    _assert_d3_contracts(t)
    return t


def build_d3() -> base.Template:
    """Narrow r2: remove only the unsupported rear cap and land its debris."""
    t = _build_d3_r1()

    # Independent r1 review identified this 4x3 cap as floating after its tower
    # was removed. Remove exactly that detached remnant and land a restrained
    # five-block debris scatter on the surviving service deck directly below.
    t.clear((29, 25, 43), (32, 25, 45))
    for pos in ((29, 17, 43), (30, 17, 44), (31, 17, 45), (32, 17, 44), (31, 18, 44)):
        t.set(*pos, "minecraft:light_gray_concrete")

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-006 D3 proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-006 proof position contains {t.palette[state_id]['Name']}")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-006 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-006 proof chest has no clear block above")
    matching = sum(1 for _, block_nbt in t.blocks.values() if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-006 must contain exactly one canonical proof container; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if _count_block(t, "minecraft:spawner") != 3:
        raise AssertionError("OWS-006 D3 requires exactly three deliberate encounter spawners")
    for x, z in ((28, 6), (28, 16), (12, 15), (17, 21), (29, 20), (42, 22), (49, 17)):
        for dx in (0, 1):
            if _name(t, (x + dx, 2, z)) != "minecraft:iron_door":
                raise AssertionError(f"OWS-006 D3 route lost controlled door at {(x + dx, 2, z)}")
    if _name(t, (53, 2, 40)) not in AIR:
        raise AssertionError("OWS-006 D3 proof approach is obstructed")
    sign_count = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if sign_count < 19:
        raise AssertionError(f"OWS-006 D3 preserves too little institutional identity: {sign_count} signs")
    for pos in ((25, 7, 5), (33, 7, 5)):
        if not (_name(t, pos) or "").endswith("_wall_sign"):
            raise AssertionError(f"OWS-006 D3 lost primary VCF identity at {pos}")
    if _count_block(t, "create:fluid_pipe") < 90:
        raise AssertionError("OWS-006 D3 removed too much environmental-service anatomy")
    if _count_block(t, "farmersdelight:rich_soil") < 40:
        raise AssertionError("OWS-006 D3 removed too much comparative culture evidence")
    for pos in ((54, 2, 34), (34, 2, 36), (45, 2, 45)):
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 6:
            raise AssertionError(f"OWS-006 encounter is too close to proof at {pos}")


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str) -> tuple[dict, str]:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    temp_name = f"_heavy_review_ows006_gate_c_{label}_r2"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        model_bytes = temp_nbt.read_bytes()
        model_sha = hashlib.sha256(model_bytes).hexdigest()
        size, blocks = unpack_structure(temp_nbt)
        manifest = render_review_set(
            target="OWS-006", gate="gate_c_damage_states", revision=revision,
            damage_state=damage_state, source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows006_gate_c_damage_states.build_{label}()",
            size=size, blocks=blocks, output_dir=OUTPUT_DIR / label, camera_set="ows006_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = model_sha
        (OUTPUT_DIR / label / "review_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
        return manifest, model_sha
    finally:
        temp_nbt.unlink(missing_ok=True)


def _model_sha(t: base.Template, label: str) -> str:
    temp_name = f"_heavy_review_ows006_gate_c_hash_{label}"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison(manifests: dict[str, dict], output: Path) -> None:
    from PIL import Image, ImageDraw

    states = ("D0", "D1", "D3")
    views = ("front_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w, margin, header_h, label_h = 420, 16, 88, 24
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
    sheet = Image.new("RGB", (margin * 4 + thumb_w * 3, header_h + sum(row_heights) + margin * 5), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), "OWS-006 — Gate C r2 — frozen D0/D1 + revised D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), "dimensions=59x26x51  camera_set=ows006_fixed_v1", fill=(210, 210, 210))
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
    d0, d1, d3_r1, d3 = build_d0(), build_d1(), _build_d3_r1(), build_d3()
    hashes = {
        "D0": _model_sha(d0, "d0"),
        "D1": _model_sha(d1, "d1"),
        "D3_R1": _model_sha(d3_r1, "d3_r1"),
    }
    if hashes["D0"] != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(f"OWS-006 r2 D0 drifted from Gate B: {hashes['D0']} != {ACCEPTED_GATE_B_SHA256}")
    if hashes["D1"] != FROZEN_D1_R1_SHA256:
        raise AssertionError(f"OWS-006 r2 D1 drifted from frozen r1: {hashes['D1']} != {FROZEN_D1_R1_SHA256}")
    if hashes["D3_R1"] != REJECTED_D3_R1_SHA256:
        raise AssertionError(f"OWS-006 r1 D3 reconstruction drifted: {hashes['D3_R1']} != {REJECTED_D3_R1_SHA256}")

    expected_r2_delta = {
        *((x, 25, z) for x in range(29, 33) for z in range(43, 46)),
        (29, 17, 43), (30, 17, 44), (31, 17, 45), (32, 17, 44), (31, 18, 44),
    }
    r2_delta = _diff_positions(d3_r1, d3)
    if r2_delta != expected_r2_delta:
        raise AssertionError(f"OWS-006 r2 exceeded narrow reviewer scope: {sorted(r2_delta ^ expected_r2_delta)}")

    d1_changes, d3_changes = _diff_count(d0, d1), _diff_count(d0, d3)
    if d1_changes < 120:
        raise AssertionError(f"OWS-006 D1 intervention is too weak to review: {d1_changes}")
    if d3_changes < 420:
        raise AssertionError(f"OWS-006 D3 ruin is too weak to review: {d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"OWS-006 D3 must exceed twice D1: D1={d1_changes}, D3={d3_changes}")

    revision = f"gate-c-r2@{os.environ.get('GITHUB_SHA', 'local')[:8]}"
    d3_manifest, hashes["D3"] = _serialize_and_render("d3", "D3 r2 causal ruin — detached cap corrected", d3, revision)
    manifests = {
        "D0": json.loads((R1_DIR / "d0" / "review_manifest.json").read_text(encoding="utf-8")),
        "D1": json.loads((R1_DIR / "d1" / "review_manifest.json").read_text(encoding="utf-8")),
        "D3": d3_manifest,
    }
    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": "OWS-006", "gate": "gate_c_damage_states", "revision": revision,
        "fixed_camera_set": "ows006_fixed_v1", "source_d0": "render_ows006_gate_b_intact.build_gate_b_intact",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": hashes["D0"], "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": hashes["D1"], "d3_review_model_sha256": hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes, "d3_changed_positions_from_d0": d3_changes,
        "rejected_r1_d3_review_model_sha256": hashes["D3_R1"],
        "r2_changed_positions_from_r1_d3": len(r2_delta),
        "r2_scope": "removed twelve-block unsupported rear service cap and landed five-block debris scatter directly below",
        "frozen_state_artifacts": {
            "D0": "old_world_narrative/reviews/heavy_rebuild/visual/OWS-006/gate_c_damage_states/r1/d0/review_manifest.json",
            "D1": "old_world_narrative/reviews/heavy_rebuild/visual/OWS-006/gate_c_damage_states/r1/d1/review_manifest.json",
        },
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_slow_polymer_integrity_failure_has_no_distinct_acute_collapse_state",
        "proof_position": list(PROOF_POS), "proof_loot_table": PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 3,
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-006 Gate C r2: D0/D1 frozen, D3 r1-to-r2 delta={len(r2_delta)}, D3 changes from D0={d3_changes}; independent review pending.")


if __name__ == "__main__":
    main()

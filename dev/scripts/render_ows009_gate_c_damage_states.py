#!/usr/bin/env python3
"""Render OWS-009 Gate-C r1 D0/D1/D3 historical states.

D0 is the exact accepted Gate-B r1 model. D1 adds ordinary late-operation
maintenance escalation. D3 grows restrained, causal drain/flashing damage,
bounded encounters and exactly one canonical proof node from that condition.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import generate_wasteland_sites as base
import render_ows009_gate_b_intact as gate_b
from render_old_world_heavy_rebuild_review import contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure


ROOT = Path(__file__).resolve().parents[1]
TARGET = "OWS-009"
SIZE = (49, 18, 41)
CAMERA_SET = "ows009_fixed_v1"
OUTPUT_DIR = ROOT / "old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_c_damage_states/r1"
SHIPPING_PATH = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt"
FROZEN_SHIPPING_SHA256 = "d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d"
FROZEN_SHIPPING_BLOB = "4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a"
ACCEPTED_GATE_B_SHA256 = "c2c850549694cfa28e898fbe7019841e1c358b5534c1a53136f87f243d90c0a9"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot"
PROOF_ITEM = "kubejs:atlas_service_plate"
LORE_ITEM = "kubejs:atlas_transfer_maintenance_manual"
PROOF_LOOT_PATH = ROOT / "kubejs/data/infinite_domain/loot_table/chests/old_world/ows_009_atlas_roadside_repair_depot.json"
PROOF_POS = (37, 2, 29)
SPAWNERS = {
    (6, 2, 21): "minecraft:zombie",
    (23, 2, 21): "minecraft:zombie",
    (43, 2, 33): "minecraft:cave_spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_DOCS = tuple(f"OWS-009_PASS{number}_{name}.md" for number, name in (
    (13, "HISTORICAL_LAYERING"),
    (14, "ENVIRONMENTAL_NARRATIVE"),
    (15, "ENCOUNTER_ARCHITECTURE"),
    (16, "LOOT_ARCHITECTURE"),
    (17, "QUEST_PROOF_ARCHITECTURE"),
    (18, "DAMAGE_AND_DECAY"),
))


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _count(t: base.Template, block: str) -> int:
    return sum(_name(t, pos) == block for pos in t.blocks)


def _diff_positions(a: base.Template, b: base.Template) -> set[tuple[int, int, int]]:
    positions = set(a.blocks) | set(b.blocks)
    return {pos for pos in positions if _name(a, pos) != _name(b, pos)}


def _assert_authorized() -> None:
    review_dir = ROOT / "old_world_narrative/reviews/heavy_rebuild"
    review = review_dir / "OWS-009_GATE_B_R1_REVIEW.md"
    text = review.read_text(encoding="utf-8") if review.is_file() else ""
    if "OWS-009 GATE B r1: PASSED" not in text or ACCEPTED_GATE_B_SHA256 not in text:
        raise AssertionError("Gate C refused: exact passed OWS-009 Gate-B r1 review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).is_file()]
    if missing:
        raise AssertionError(f"Gate C refused: missing Pass 13-18 records: {missing}")


def _assert_canonical_loot() -> None:
    payload = json.loads(PROOF_LOOT_PATH.read_text(encoding="utf-8"))

    def count_item(value: object, wanted: str) -> int:
        if isinstance(value, dict):
            here = int(value.get("type") == "minecraft:item" and value.get("name") == wanted)
            return here + sum(count_item(child, wanted) for child in value.values())
        if isinstance(value, list):
            return sum(count_item(child, wanted) for child in value)
        return 0

    for item in (PROOF_ITEM, LORE_ITEM):
        matches = count_item(payload, item)
        if matches != 1:
            raise AssertionError(f"canonical OWS-009 loot must contain exactly one {item}; found {matches}")


def build_d0() -> base.Template:
    t = gate_b.build_gate_b_intact()
    gate_b._assert_intact_contracts(t)
    return t


def build_d1() -> base.Template:
    """Add competent late-operation recheck and drain-maintenance layers."""
    t = build_d0()

    # Recheck datums follow the original intake -> repair -> release workflow.
    for x1, x2, color in (
        (5, 13, "minecraft:cyan_concrete"),
        (16, 24, "minecraft:orange_concrete"),
        (27, 34, "minecraft:yellow_concrete"),
    ):
        t.fill((x1, 1, 22), (x2, 1, 23), color)

    # Paired removable collars mark repeated drain/service inspections at each
    # cell's rear edge while leaving the technician spine unobstructed.
    for x, color in ((9, "minecraft:cyan_concrete"), (20, "minecraft:orange_concrete"), (31, "minecraft:yellow_concrete")):
        t.fill((x - 2, 2, 32), (x - 2, 5, 32), "tfmg:steel_block")
        t.fill((x + 2, 2, 32), (x + 2, 5, 32), "tfmg:steel_block")
        t.fill((x - 2, 5, 32), (x + 2, 5, 32), color)
        t.fill((x - 1, 2, 32), (x + 1, 3, 32), "create:framed_glass")
        t.set(x, 4, 32, "ae2:terminal")

    # Temporary recheck bypass parallels the accepted permanent service trunk,
    # branches to all three cells and rises beside the existing roof housings.
    t.fill((5, 6, 33), (34, 6, 33), "create:fluid_pipe")
    for x, top in ((9, 14), (20, 16), (31, 15)):
        t.fill((x, 6, 24), (x, 6, 33), "create:fluid_pipe")
        t.set(x, 6, 27, "create:mechanical_pump", facing="south")
        t.fill((x + 1, 7, 33), (x + 1, top, 33), "create:fluid_pipe")
        t.set(x + 1, top - 1, 32, "create:encased_fan", facing="south")

    # Comparison pads at cell edges record repeat tests without blocking axes.
    for x, color in ((6, "minecraft:cyan_concrete"), (17, "minecraft:orange_concrete"), (27, "minecraft:yellow_concrete")):
        t.fill((x, 2, 23), (x + 1, 2, 23), "create:depot")
        t.set(x, 3, 23, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((x, 1, 21), (x + 1, 1, 21), color)

    # Ordinary backlog: staged replacement stock and tagged removed cores.
    t.fill((37, 5, 21), (39, 6, 22), "immersiveengineering:crate")
    t.fill((37, 4, 25), (39, 5, 26), "immersiveengineering:crate")
    t.fill((37, 2, 32), (38, 5, 33), "minecraft:weathered_copper")
    t.fill((42, 2, 32), (43, 5, 33), "minecraft:weathered_copper")

    # Local flashing replacement remains intact but visibly late-generation.
    t.fill((32, 14, 21), (34, 14, 24), "minecraft:weathered_cut_copper")
    t.fill((41, 10, 24), (43, 10, 26), "minecraft:weathered_cut_copper")

    base.wall_sign(t, 6, 5, 23, "south", "DIAGNOSTIC RECHECK", "SERVICE BULLETIN 6")
    base.wall_sign(t, 17, 5, 23, "south", "LIFT DATUM", "VERIFY AFTER LOAD")
    base.wall_sign(t, 27, 5, 23, "south", "CALIBRATION HOLD", "REPEAT TEST")
    base.wall_sign(t, 7, 5, 32, "south", "DRAIN COLLAR 01", "INSPECT WEEKLY")
    base.wall_sign(t, 18, 5, 32, "south", "DRAIN COLLAR 02", "SEEPAGE MONITOR")
    base.wall_sign(t, 29, 5, 32, "south", "DRAIN COLLAR 03", "FLASHING WATCH")
    base.wall_sign(t, 37, 6, 21, "east", "RECHECK PARTS", "PRIORITY ISSUE")
    base.wall_sign(t, 37, 6, 32, "east", "REMOVED CORES", "RETURN BACKLOG")

    gate_b._assert_intact_contracts(t)
    return t


def build_d3() -> base.Template:
    """Grow long-abandonment damage from the monitored east/rear failure."""
    t = build_d1()

    # Moisture follows the actual rear drain trench and Bay-03 branch.
    for x1, x2 in ((24, 27), (29, 34)):
        t.fill((x1, 1, 32), (x2, 1, 34), "minecraft:mossy_stone_bricks")
    t.fill((31, 1, 22), (34, 1, 28), "minecraft:moss_block")
    t.fill((36, 1, 31), (44, 1, 34), "minecraft:coarse_dirt")
    for pos in ((25, 2, 33), (29, 2, 32), (33, 2, 34), (34, 2, 25), (38, 2, 33), (41, 2, 32)):
        t.set(*pos, "minecraft:brown_mushroom")
    for pos in ((28, 4, 32), (32, 4, 32), (35, 4, 31), (43, 4, 31)):
        t.set(*pos, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")

    # Bay-03 monitor flashing opens locally. Steel frame survives; corroded
    # remnants and debris land on the calibration-side edge directly below.
    t.clear((32, 14, 22), (34, 14, 24))
    t.fill((31, 13, 22), (34, 13, 24), "minecraft:weathered_cut_copper")
    for pos in ((32, 2, 22), (33, 2, 23), (34, 2, 24), (34, 1, 25)):
        t.set(*pos, "minecraft:gravel")

    # The same blocked east drain corrodes a small parts-roof edge. Fragments
    # land on the service strip and existing parts stacks, never float.
    t.clear((41, 10, 24), (43, 10, 26))
    t.fill((40, 9, 24), (43, 9, 26), "minecraft:weathered_cut_copper")
    for pos in ((42, 6, 25), (44, 2, 26), (45, 1, 25), (46, 1, 26)):
        t.set(*pos, "minecraft:gravel")

    # Core-return canopy loses its southeast corner; supported charcoal/steel
    # edges remain and all fallen pieces reach the lower collection yard.
    t.clear((41, 6, 35), (43, 7, 36))
    t.fill((40, 5, 35), (43, 5, 36), "minecraft:weathered_cut_copper")
    for pos in ((41, 1, 36), (42, 1, 37), (43, 1, 38), (44, 1, 37)):
        t.set(*pos, "minecraft:gravel")

    # Long exposure remains localized to east/rear grounds and service edges.
    t.fill((36, 0, 35), (44, 0, 39), "minecraft:mossy_cobblestone")
    t.fill((45, 0, 23), (48, 0, 29), "minecraft:cracked_stone_bricks")
    for pos in ((30, 2, 33), (34, 2, 27), (38, 2, 33), (43, 2, 30), (44, 3, 28)):
        t.set(*pos, "minecraft:cobweb")

    # Validate surviving D0 systems before Gate-C gameplay nodes are installed.
    gate_b._assert_intact_contracts(t)

    if _name(t, PROOF_POS) not in AIR or _name(t, (37, 3, 29)) not in AIR or _name(t, (38, 2, 29)) not in AIR:
        raise AssertionError("OWS-009 records proof position or approach is obstructed")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")

    # Encounters are deliberately bounded to cell edges and dirty core return.
    for (x, y, z), mob in SPAWNERS.items():
        if (x, y, z) == (43, 2, 33):
            t.clear((43, 2, 33), (43, 3, 33))
        if _name(t, (x, y, z)) not in AIR or _name(t, (x, y + 1, z)) not in AIR:
            raise AssertionError(f"OWS-009 spawner position obstructed at {(x, y, z)}")
        t.spawner(x, y, z, mob, count=1, nearby=3)

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-009 canonical proof chest is missing")
    nbt = row[1]
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-009 proof chest uses the wrong loot table")
    if _name(t, (37, 3, 29)) not in AIR or _name(t, (38, 2, 29)) not in AIR:
        raise AssertionError("OWS-009 proof headroom or east approach is blocked")
    matching = sum(1 for _, block_nbt in t.blocks.values() if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-009 requires exactly one canonical proof node; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-009 D3 bounds changed: {t.size}")
    if _count(t, "minecraft:spawner") != len(SPAWNERS):
        raise AssertionError("OWS-009 D3 encounter count drifted")
    for pos in SPAWNERS:
        if _name(t, pos) != "minecraft:spawner":
            raise AssertionError(f"OWS-009 encounter missing at {pos}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 9:
            raise AssertionError(f"OWS-009 encounter too close to proof at {pos}")

    # All Gate-B controlled doors survive damage and gameplay placement.
    for x, z in ((40, 7), (40, 15), (39, 31), (39, 34)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-009 D3 lost Z-wall door at {(x + dx, y, z)}")
    for x, z in ((35, 13), (35, 23), (35, 29), (40, 23), (44, 23)):
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-009 D3 lost X-wall door at {(x, y, z + dz)}")

    # Accepted circulation stays clear in the final gameplay state.
    for low, high, label in (
        ((8, 2, 8), (10, 4, 22), "Bay-01 vehicle lane"),
        ((19, 2, 8), (21, 4, 22), "Bay-02 vehicle lane"),
        ((29, 2, 8), (31, 4, 22), "Bay-03 vehicle lane"),
        ((5, 2, 24), (33, 3, 27), "transverse field"),
        ((5, 2, 28), (33, 3, 31), "technician spine"),
        ((39, 2, 8), (42, 3, 14), "customer route"),
        ((41, 2, 23), (43, 3, 25), "parts route"),
        ((39, 2, 29), (40, 3, 34), "records/core route"),
    ):
        gate_b._assert_clear(t, low, high, label)

    if _count(t, "create:fluid_pipe") < 150:
        raise AssertionError("OWS-009 D3 removed too much connected utility anatomy")
    if _count(t, "tfmg:steel_block") < 700:
        raise AssertionError("OWS-009 D3 removed too much primary structure")
    if sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks) < 20:
        raise AssertionError("OWS-009 D3 preserves too little Atlas/service identity")


def _model_sha(t: base.Template, label: str) -> str:
    temp_name = f"_heavy_review_ows009_gate_c_hash_{label}"
    temp_nbt = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str, head: str) -> tuple[dict, str]:
    temp_name = f"_heavy_review_ows009_gate_c_{label}_r1"
    temp_nbt = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        model_bytes = temp_nbt.read_bytes()
        model_sha = hashlib.sha256(model_bytes).hexdigest()
        size, blocks = unpack_structure(temp_nbt)
        manifest = render_review_set(
            target=TARGET,
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=head,
            source_path=f"review-only:render_ows009_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=CAMERA_SET,
        )
        fixed_cutaway = 6
        cut_path = OUTPUT_DIR / label / "interior_cutaway.png"
        cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= fixed_cutaway}
        isometric(size, cutaway_blocks, False, f"{TARGET} — Gate C — {damage_state} — interior cutaway Y<={fixed_cutaway}").save(cut_path)
        contact_views = [
            (view, OUTPUT_DIR / label / f"{view}.png")
            for view in ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
        ]
        contact_sheet(
            contact_views, OUTPUT_DIR / label / "contact_sheet.png", target=TARGET,
            gate="gate_c_damage_states", revision=revision, damage_state=damage_state,
            dimensions=size, camera_set=CAMERA_SET,
        )
        manifest["cutaway_y"] = fixed_cutaway
        manifest["review_model_nbt_sha256"] = model_sha
        (OUTPUT_DIR / label / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        return manifest, model_sha
    finally:
        temp_nbt.unlink(missing_ok=True)


def _damage_comparison(manifests: dict[str, dict], output: Path) -> None:
    states = ("D0", "D1", "D3")
    views = ("front_left", "rear_right", "roof_top_oblique", "interior_cutaway")
    thumb_w, margin, header_h, label_h = 420, 16, 88, 24
    loaded: dict[tuple[str, str], Image.Image] = {}
    row_heights: list[int] = []
    for view in views:
        row_images = []
        for state in states:
            image = Image.open(ROOT / manifests[state]["views"][view]).convert("RGB")
            ratio = thumb_w / max(1, image.width)
            image = image.resize((thumb_w, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
            loaded[(state, view)] = image
            row_images.append(image)
        row_heights.append(max(image.height for image in row_images) + label_h)
    sheet = Image.new("RGB", (margin * 4 + thumb_w * 3, header_h + sum(row_heights) + margin * 5), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), "OWS-009 — Gate C r1 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), f"dimensions=49x18x41  camera_set={CAMERA_SET}", fill=(210, 210, 210))
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


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    _assert_authorized()
    _assert_canonical_loot()
    shipping_bytes = SHIPPING_PATH.read_bytes()
    if hashlib.sha256(shipping_bytes).hexdigest() != FROZEN_SHIPPING_SHA256 or _git_blob(SHIPPING_PATH) != FROZEN_SHIPPING_BLOB:
        raise AssertionError("OWS-009 shipping drifted before Gate-C render")

    d0, d1, d3 = build_d0(), build_d1(), build_d3()
    d0_sha = _model_sha(d0, "d0_preflight")
    if d0_sha != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(f"OWS-009 D0 drifted from accepted Gate B: {d0_sha} != {ACCEPTED_GATE_B_SHA256}")
    d1_changes = len(_diff_positions(d0, d1))
    d3_changes = len(_diff_positions(d0, d3))
    if d1_changes < 170:
        raise AssertionError(f"OWS-009 D1 history too weak to review: {d1_changes}")
    if d3_changes < 380 or d3_changes <= d1_changes + 150:
        raise AssertionError(f"OWS-009 D3 insufficiently distinct: D1={d1_changes}, D3={d3_changes}")

    head = _git_head()
    revision = f"gate-c-r1@{head[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 exact accepted intact operation", d0, revision, head),
        "D1": _serialize_and_render("d1", "D1 ordinary late maintenance and recheck backlog", d1, revision, head),
        "D3": _serialize_and_render("d3", "D3 causal drain/flashing failure and restrained ruin", d3, revision, head),
    }
    manifests = {state: value[0] for state, value in rendered.items()}
    hashes = {state: value[1] for state, value in rendered.items()}
    if hashes["D0"] != ACCEPTED_GATE_B_SHA256:
        raise AssertionError("rendered OWS-009 D0 no longer matches accepted Gate B")

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": TARGET,
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": CAMERA_SET,
        "source_commit": head,
        "source_d0": "render_ows009_gate_b_intact.build_gate_b_intact",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": hashes["D1"],
        "d3_review_model_sha256": hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_no_distinct_acute_event_between_ordinary_maintenance_backlog_and_long_abandonment",
        "gate_b_architecture_routes_utilities_identity_asserted_all_states": True,
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "proof_item": PROOF_ITEM,
        "lore_item": LORE_ITEM,
        "canonical_proof_nodes_d3": 1,
        "deterministic_spawners_d3": len(SPAWNERS),
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "authoritative_shipping_modified": False,
        "shipping_nbt_sha256_before": FROZEN_SHIPPING_SHA256,
        "shipping_nbt_sha256_after": hashlib.sha256(SHIPPING_PATH.read_bytes()).hexdigest(),
        "shipping_nbt_git_blob_before": FROZEN_SHIPPING_BLOB,
        "shipping_nbt_git_blob_after": _git_blob(SHIPPING_PATH),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    if gate_manifest["shipping_nbt_sha256_after"] != FROZEN_SHIPPING_SHA256 or gate_manifest["shipping_nbt_git_blob_after"] != FROZEN_SHIPPING_BLOB:
        raise AssertionError("OWS-009 shipping changed during Gate-C render")
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    if SHIPPING_PATH.read_bytes() != shipping_bytes:
        raise AssertionError("OWS-009 shipping bytes changed during Gate-C render")
    print(
        f"Rendered {TARGET} Gate C r1: D0 exact={hashes['D0'] == ACCEPTED_GATE_B_SHA256}, "
        f"D1 changes={d1_changes}, D3 changes={d3_changes}; independent review required."
    )


if __name__ == "__main__":
    main()

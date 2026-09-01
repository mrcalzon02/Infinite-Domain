#!/usr/bin/env python3
"""Render OWS-008 Gate-C r2 D0/D1/D3 historical states.

D0 is the exact repaired Gate-B r2 candidate and may render only after that
candidate is independently accepted. D1 records competent
late persistence-investigation escalation. D3 grows restrained, causal service-
joint recurrence, abandonment damage, bounded encounters and exactly one
canonical proof node from that condition. The module is review-only and never
writes shared state or authoritative shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import generate_wasteland_sites as base
import render_ows008_gate_b_intact as gate_b
from render_old_world_heavy_rebuild_review import contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure


ROOT = Path(__file__).resolve().parents[2]
TARGET = "OWS-008"
SIZE = (55, 22, 49)
CAMERA_SET = "ows008_fixed_v1"
OUTPUT_DIR = (
    ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" /
    TARGET / "gate_c_damage_states" / "r2"
)
SHIPPING_PATH = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "structure" /
    "wasteland" / "old_world" /
    "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
ACCEPTED_GATE_B_SHA256 = "642b1e986952140d997b2bbd66c4596d3c1f958b91397672ca47f6b9711500e8"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_008_vcf_emergency_persistence_investigation_lab"
PROOF_ITEM = "kubejs:vcf_persistence_incident_file"
PROOF_LOOT_PATH = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "loot_table" / "chests" /
    "old_world" / "ows_008_vcf_emergency_persistence_investigation_lab.json"
)
PROOF_POS = (12, 14, 29)
SPAWNERS = {
    (51, 2, 24): "minecraft:zombie",
    (14, 2, 34): "minecraft:cave_spider",
    (14, 2, 41): "minecraft:spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_DOCS = tuple(f"OWS-008_PASS{number}_{name}.md" for number, name in (
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


def _assert_history_authorized() -> None:
    review_dir = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild"
    review = review_dir / "OWS-008_GATE_B_R2_REVIEW.md"
    if not review.exists() or "OWS-008 GATE B r2: PASSED" not in review.read_text(encoding="utf-8"):
        raise AssertionError("Gate C refused: explicit OWS-008 Gate-B r2 PASSED review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).exists()]
    if missing:
        raise AssertionError(f"Gate C refused: required Pass 13-18 records are missing: {missing}")


def _assert_canonical_loot_contract() -> None:
    if not PROOF_LOOT_PATH.is_file():
        raise AssertionError(f"OWS-008 canonical loot table is missing: {PROOF_LOOT_PATH}")
    payload = json.loads(PROOF_LOOT_PATH.read_text(encoding="utf-8"))

    def count_item(value: object) -> int:
        if isinstance(value, dict):
            here = int(value.get("type") == "minecraft:item" and value.get("name") == PROOF_ITEM)
            return here + sum(count_item(child) for child in value.values())
        if isinstance(value, list):
            return sum(count_item(child) for child in value)
        return 0

    matches = count_item(payload)
    if matches != 1:
        raise AssertionError(f"OWS-008 canonical table must guarantee one proof entry; found {matches}")


def build_d0() -> base.Template:
    """Return the repaired Gate-B r2 model after its independent approval."""
    t = gate_b.build_gate_b_intact()
    gate_b._assert_intact_contracts(t)
    return t


def build_d1() -> base.Template:
    """Add professional late-operation recurrence investigation layers."""
    t = build_d0()

    # Successive clean-zone floor datums align each cell with the rear
    # penetration rack that repeatedly returned positive joint samples.
    for x1, x2, color in (
        (7, 15, "minecraft:lime_concrete"),
        (18, 26, "minecraft:white_concrete"),
        (29, 38, "minecraft:yellow_concrete"),
        (41, 49, "minecraft:cyan_concrete"),
    ):
        t.fill((x1, 1, 38), (x2, 1, 40), color)

    # Four generations of inspection collars and removable seam plates remain
    # side-by-side. The two-wide rear maintenance route stays unobstructed.
    for x, seal in ((13, "minecraft:lime_concrete"), (22, "minecraft:white_concrete"),
                    (33, "minecraft:yellow_concrete"), (44, "minecraft:cyan_concrete")):
        t.fill((x - 2, 2, 40), (x - 2, 5, 40), "tfmg:steel_block")
        t.fill((x + 2, 2, 40), (x + 2, 5, 40), "tfmg:steel_block")
        t.fill((x - 2, 5, 40), (x + 2, 5, 40), seal)
        t.fill((x - 1, 2, 40), (x + 1, 3, 40), "create:framed_glass")
        t.set(x, 3, 40, "ae2:terminal")

    # A temporary diagnostic bypass parallels the accepted air/wash headers and
    # connects portable filter-watch modules to all four cell branches.
    t.fill((8, 7, 42), (46, 7, 42), "create:fluid_pipe")
    for x in (11, 22, 33, 45):
        t.fill((x, 7, 39), (x, 7, 42), "create:fluid_pipe")
        t.set(x, 7, 41, "create:mechanical_pump", facing="south")
    for x1, x2 in ((7, 10), (19, 21), (30, 32), (41, 43)):
        t.fill((x1, 2, 45), (x2, 4, 45), "immersiveengineering:sheetmetal_steel")
        t.set(x2, 5, 45, "create:encased_fan", facing="south")
    # The late-operation bypass remains deliberately exposed above the rear
    # service roof so the crisis retrofit reads from fixed exterior cameras.
    t.fill((8, 12, 44), (45, 12, 44), "create:fluid_pipe")
    for x in (11, 22, 33, 45):
        t.fill((x, 8, 44), (x, 12, 44), "create:fluid_pipe")
        t.set(x, 12, 44, "create:mechanical_pump", facing="east")

    # Comparison stations make negative room-side tests versus positive hidden-
    # joint samples visible without adding loot or quest proof prematurely.
    for x in (9, 20, 31, 42):
        t.fill((x, 2, 41), (x + 1, 2, 41), "create:depot")
        t.set(x, 3, 41, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    base.wall_sign(t, 7, 5, 38, "south", "JOINT SAMPLE D", "SEAL GENERATION 4")
    base.wall_sign(t, 18, 5, 38, "south", "JOINT SAMPLE C", "SURFACE NEGATIVE")
    base.wall_sign(t, 29, 5, 38, "south", "JOINT SAMPLE B", "HIDDEN POSITIVE")
    base.wall_sign(t, 41, 5, 38, "south", "JOINT SAMPLE A", "RETEST REQUIRED")
    base.wall_sign(t, 31, 6, 45, "south", "BYPASS FILTRATION", "CONTINUOUS WATCH")
    base.wall_sign(t, 3, 16, 27, "east", "INCIDENT STATUS", "CONTAINMENT HOLD")

    # The accepted architecture and all protected circulation remain intact.
    gate_b._assert_intact_contracts(t)
    return t


def build_d3() -> base.Template:
    """Grow causal long-abandonment damage from the investigated service seam."""
    t = build_d1()

    # Recurrence follows the exact rear penetration/drain line. Repeated seal
    # collars survive among localized mycelium, wet floor and cracked finishes.
    for x1, x2 in ((7, 11), (14, 19), (24, 29), (35, 41), (45, 48)):
        t.fill((x1, 1, 40), (x2, 1, 42), "minecraft:mycelium")
    for pos in ((8, 2, 40), (10, 2, 42), (16, 2, 41), (27, 2, 40),
                (37, 2, 41), (41, 2, 40), (47, 2, 42)):
        t.set(*pos, "minecraft:brown_mushroom")
    for pos in ((12, 4, 40), (23, 4, 40), (34, 4, 40), (45, 4, 40)):
        t.set(*pos, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")

    # Failed effluent and wash joints stain only the dirty east plant and Cell-A
    # service edge; the specimen, public and clean routes remain unchanged.
    t.fill((41, 1, 32), (49, 1, 34), "minecraft:mossy_stone_bricks")
    t.fill((48, 1, 29), (52, 1, 35), "minecraft:coarse_dirt")
    t.fill((49, 1, 36), (52, 1, 40), "minecraft:moss_block")
    for pos in ((43, 2, 33), (48, 2, 34), (50, 2, 38), (52, 3, 37)):
        t.set(*pos, "minecraft:cobweb")

    # Sterilant corrosion and later rain open one rear/east service-roof bay.
    # Steel columns and adjoining deck remain; removed material lands directly
    # below on the dirty plant floor and lower exterior apron.
    t.clear((41, 11, 42), (45, 11, 45))
    t.clear((46, 9, 42), (48, 10, 45))
    t.fill((41, 10, 42), (45, 10, 45), "minecraft:weathered_cut_copper")
    for pos in ((42, 2, 42), (44, 2, 43), (46, 2, 44), (48, 2, 43),
                (49, 2, 45), (51, 1, 45)):
        t.set(*pos, "minecraft:gravel")

    # The same wet dirty-side branch later opens one corner of the yellow
    # receiving canopy and the adjacent maintenance-core roof. Primary frames,
    # entry doors and stair landings survive; debris lands on lower roofs/apron.
    t.clear((51, 9, 20), (53, 10, 22))
    t.fill((50, 8, 20), (53, 8, 22), "minecraft:weathered_cut_copper")
    t.clear((47, 18, 43), (49, 18, 45))
    t.fill((47, 17, 43), (49, 17, 45), "minecraft:weathered_cut_copper")
    for pos in ((52, 1, 20), (54, 1, 21), (53, 2, 22),
                (52, 11, 43), (53, 11, 44), (54, 11, 45)):
        t.set(*pos, "minecraft:gravel")

    # Small failed panels at the Cell-D joint expose the persistence trays to
    # the service seam; debris falls against the rear wall, not into the aisle.
    t.clear((7, 6, 37), (9, 7, 37))
    t.fill((7, 5, 38), (9, 5, 39), "minecraft:cracked_stone_bricks")
    for pos in ((7, 2, 38), (8, 2, 39), (15, 2, 38)):
        t.set(*pos, "minecraft:gravel")

    # Long weathering remains bounded to the failed service/drain path.
    t.fill((41, 0, 43), (54, 0, 46), "minecraft:mossy_cobblestone")
    t.fill((7, 0, 46), (15, 0, 47), "minecraft:mossy_cobblestone")
    t.fill((28, 0, 46), (38, 0, 47), "minecraft:cracked_stone_bricks")

    # Check the damaged architecture before Gate-C-only gameplay blocks are
    # added; Gate-B's exclusions intentionally reject proof and spawners.
    gate_b._assert_intact_contracts(t)

    # Exactly one canonical proof/loot node occupies the secure upper incident
    # archive. It closes the route after the player has read the cell sequence.
    if _name(t, PROOF_POS) not in AIR or _name(t, (12, 15, 29)) not in AIR:
        raise AssertionError("OWS-008 secure archive proof position is not clear")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="north")

    # Three bounded vanilla encounters trace dirty receipt -> persistence cell
    # -> hidden service seam. None occupies a protected aisle or proof room.
    for (x, y, z), mob in SPAWNERS.items():
        if _name(t, (x, y, z)) not in AIR or _name(t, (x, y + 1, z)) not in AIR:
            raise AssertionError(f"OWS-008 spawner position is obstructed at {(x, y, z)}")
        t.spawner(x, y, z, mob, count=1, nearby=3 if "spider" in mob else 4)

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-008 canonical proof chest is missing")
    nbt = row[1]
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-008 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _name(t, (12, 15, 29)) not in AIR or _name(t, (12, 14, 28)) not in AIR:
        raise AssertionError("OWS-008 proof chest or its north approach is obstructed")
    matching = sum(1 for _, block_nbt in t.blocks.values() if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-008 requires exactly one canonical proof node; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-008 D3 bounds changed: {t.size}")
    if _count(t, "minecraft:spawner") != len(SPAWNERS):
        raise AssertionError("OWS-008 D3 requires exactly three bounded spawners")
    for pos, mob in SPAWNERS.items():
        row = t.blocks.get(pos)
        if row is None or t.palette[row[0]]["Name"] != "minecraft:spawner":
            raise AssertionError(f"OWS-008 encounter missing at {pos}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 12:
            raise AssertionError(f"OWS-008 encounter is too close to proof at {pos}")

    # Principal thresholds and pressure boundaries remain complete after all
    # gameplay placement. These are the same asserted Gate-B door families.
    doors_z = ((26, 4), (26, 13), (11, 24), (11, 28), (22, 22), (22, 26),
               (33, 20), (33, 24), (45, 18), (45, 22), (32, 36), (21, 37),
               (10, 39), (47, 46))
    for x, z in doors_z:
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-008 D3 lost Z-wall door at {(x + dx, y, z)}")
    doors_x = ((2, 18), (53, 16), (53, 36), (39, 26), (27, 29),
               (16, 31), (50, 28), (5, 41), (16, 43), (39, 43))
    for x, z in doors_x:
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-008 D3 lost X-wall door at {(x, y, z + dz)}")

    # Operational identity and service anatomy must survive the damage state.
    if _count(t, "create:fluid_pipe") < 480:
        raise AssertionError("OWS-008 D3 removed too much connected service anatomy")
    if _count(t, "create:fluid_tank") < 140:
        raise AssertionError("OWS-008 D3 removed too much treatment plant")
    if _count(t, "minecraft:smooth_quartz_stairs") < 36:
        raise AssertionError("OWS-008 D3 lost required vertical circulation")
    signs = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if signs < 24:
        raise AssertionError(f"OWS-008 D3 preserves too little institutional identity: {signs} signs")


def _model_sha(t: base.Template, label: str) -> str:
    temp_name = f"_heavy_review_ows008_gate_c_hash_{label}"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str, head: str) -> tuple[dict, str]:
    temp_name = f"_heavy_review_ows008_gate_c_{label}_r2"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
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
            source_path=f"review-only:render_ows008_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=CAMERA_SET,
        )
        # Damage comparison requires the same interior section plane in every
        # state. The shared renderer chooses a density-based plane, so override
        # only this target-local artifact with Gate-B's accepted Y<=7 cutaway.
        fixed_cutaway = 7
        cut_path = OUTPUT_DIR / label / "interior_cutaway.png"
        cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= fixed_cutaway}
        isometric(
            size,
            cutaway_blocks,
            False,
            f"{TARGET} — gate_c_damage_states — {damage_state} — interior cutaway Y<={fixed_cutaway}",
        ).save(cut_path)
        contact_views = [
            (view, OUTPUT_DIR / label / f"{view}.png")
            for view in ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
        ]
        contact_sheet(
            contact_views,
            OUTPUT_DIR / label / "contact_sheet.png",
            target=TARGET,
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            dimensions=size,
            camera_set=CAMERA_SET,
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
    draw.text((margin, 12), "OWS-008 — Gate C r2 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), f"dimensions=55x22x49  camera_set={CAMERA_SET}", fill=(210, 210, 210))
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


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT,
        check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def main() -> None:
    _assert_history_authorized()
    _assert_canonical_loot_contract()
    shipping_before = git_hash_object(SHIPPING_PATH)

    d0, d1, d3 = build_d0(), build_d1(), build_d3()
    d0_sha = _model_sha(d0, "d0_preflight")
    if d0_sha != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(f"OWS-008 D0 drifted from accepted Gate B r2: {d0_sha} != {ACCEPTED_GATE_B_SHA256}")

    d1_changes = len(_diff_positions(d0, d1))
    d3_changes = len(_diff_positions(d0, d3))
    if d1_changes < 160:
        raise AssertionError(f"OWS-008 D1 escalation is too weak to review: {d1_changes}")
    if d3_changes < 430:
        raise AssertionError(f"OWS-008 D3 ruin is too weak to review: {d3_changes}")
    if d3_changes <= d1_changes + 180:
        raise AssertionError(f"OWS-008 D3 is not materially distinct: D1={d1_changes}, D3={d3_changes}")

    head = git_head()
    revision = f"gate-c-r2@{head[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 exact accepted intact operation", d0, revision, head),
        "D1": _serialize_and_render("d1", "D1 late recurrence-investigation escalation", d1, revision, head),
        "D3": _serialize_and_render("d3", "D3 causal service-joint recurrence and restrained ruin", d3, revision, head),
    }
    manifests = {state: value[0] for state, value in rendered.items()}
    hashes = {state: value[1] for state, value in rendered.items()}
    if hashes["D0"] != ACCEPTED_GATE_B_SHA256:
        raise AssertionError("Rendered OWS-008 D0 no longer matches accepted Gate B r2")

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": TARGET,
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": CAMERA_SET,
        "source_commit": head,
        "source_d0": "render_ows008_gate_b_intact.build_gate_b_intact",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": hashes["D1"],
        "d3_review_model_sha256": hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_no_materially_distinct_acute_collapse_between_late_investigation_and_long_abandonment",
        "gate_b_architecture_and_route_contracts_asserted_all_states": True,
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "canonical_proof_nodes_d3": 1,
        "deterministic_spawners_d3": len(SPAWNERS),
        "comparison_artifact": str(comparison_path.relative_to(ROOT)).replace("\\", "/"),
        "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "authoritative_shipping_modified": False,
        "shipping_nbt_git_blob_before": shipping_before,
        "shipping_nbt_git_blob_after": git_hash_object(SHIPPING_PATH),
        "visual_review_status": "rendered_pending_independent_review",
        "states": {state: manifest["views"] for state, manifest in manifests.items()},
    }
    if gate_manifest["shipping_nbt_git_blob_after"] != shipping_before:
        raise AssertionError("OWS-008 shipping NBT changed during Gate-C rendering")
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        f"Rendered {TARGET} Gate C r2: D0 exact={hashes['D0'] == ACCEPTED_GATE_B_SHA256}, "
        f"D1 changes={d1_changes}, D3 changes={d3_changes}; independent review remains pending."
    )


if __name__ == "__main__":
    main()

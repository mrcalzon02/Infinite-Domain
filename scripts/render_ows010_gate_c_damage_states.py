#!/usr/bin/env python3
"""Render OWS-010 Gate-C r1 D0/D1/D3 historical states.

D0 is the exact accepted Gate-B r1 model. D1 records causal Lane-04
cannibalization under maintenance shortage. D3 grows restrained roof/service
decay, bounded encounters and exactly one canonical proof node from that state.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import generate_wasteland_sites as base
import render_ows010_gate_b_intact as gate_b
from render_old_world_heavy_rebuild_review import contact_sheet, render_review_set
from render_structure_review import isometric, unpack_structure


ROOT = Path(__file__).resolve().parents[1]
TARGET = "OWS-010"
SIZE = (49, 16, 43)
CAMERA_SET = "ows010_fixed_v1"
OUTPUT_DIR = ROOT / "old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/gate_c_damage_states/r1"
SHIPPING_PATH = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_010_atlas_conveyor_transfer_hall.nbt"
FROZEN_SHIPPING_SHA256 = "5e9390d3d41663f1baef6ad017e941dbf6153d168bb9100a8a5fd46193d9035a"
FROZEN_SHIPPING_BLOB = "be2ab341c2d252c975711caa93e92c965f943007"
ACCEPTED_GATE_B_SHA256 = "ef8c4ea3281f70270c0507f78610ffc44cd100c02fb1b4f387055a15b51e2603"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall"
PROOF_ITEM = "kubejs:atlas_transfer_maintenance_card"
LORE_ITEM = "kubejs:atlas_transfer_maintenance_manual"
PROOF_LOOT_PATH = ROOT / "kubejs/data/infinite_domain/loot_table/chests/old_world/ows_010_atlas_conveyor_transfer_hall.json"
PROOF_POS = (9, 11, 17)
LOR_SHELVES = ((9, 10, 16), (10, 10, 16))
SPAWNERS = {
    (23, 2, 33): "minecraft:zombie",
    (35, 2, 26): "minecraft:zombie",
    (45, 2, 26): "minecraft:cave_spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_DOCS = tuple(f"OWS-010_PASS{number}_{name}.md" for number, name in (
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
    review = review_dir / "OWS-010_GATE_B_R1_REVIEW.md"
    text = review.read_text(encoding="utf-8") if review.is_file() else ""
    if "OWS-010 GATE B r1: PASSED" not in text or ACCEPTED_GATE_B_SHA256 not in text:
        raise AssertionError("Gate C refused: exact passed OWS-010 Gate-B r1 review is missing")
    missing = [name for name in REQUIRED_DOCS if not (review_dir / name).is_file()]
    if missing:
        raise AssertionError(f"Gate C refused: missing Pass 13-18 records: {missing}")


def _count_item(value: object, wanted: str) -> int:
    if isinstance(value, dict):
        here = int(value.get("type") == "minecraft:item" and value.get("name") == wanted)
        return here + sum(_count_item(child, wanted) for child in value.values())
    if isinstance(value, list):
        return sum(_count_item(child, wanted) for child in value)
    return 0


def _assert_canonical_loot() -> None:
    payload = json.loads(PROOF_LOOT_PATH.read_text(encoding="utf-8"))
    proof_matches = _count_item(payload, PROOF_ITEM)
    lore_matches = _count_item(payload, LORE_ITEM)
    if proof_matches != 1:
        raise AssertionError(f"canonical OWS-010 loot must contain one {PROOF_ITEM}; found {proof_matches}")
    if lore_matches != 0:
        raise AssertionError(f"canonical OWS-010 loot must not duplicate {LORE_ITEM}; found {lore_matches}")


def build_d0() -> base.Template:
    t = gate_b.build_gate_b_intact()
    gate_b._assert_intact_contracts(t)
    return t


def build_d1() -> base.Template:
    """Show competent Lane-04 cannibalization while three lines stay live."""
    t = build_d0()

    # Lockout datum encloses the complete original Lane-04 bed without moving
    # its input/output or structural bay. Yellow is used only at isolation.
    t.fill((35, 1, 13), (35, 1, 27), "minecraft:yellow_concrete")
    t.fill((36, 1, 12), (38, 1, 12), "minecraft:yellow_concrete")
    t.fill((36, 1, 28), (38, 1, 28), "minecraft:yellow_concrete")

    # Four replaceable roller/depot modules and both drive clusters are removed.
    # The casing bed and lane endpoints survive so original function is legible.
    for z in (16, 17, 24, 25):
        t.clear((36, 3, z), (38, 3, z))
        t.fill((36, 2, z), (38, 2, z), "minecraft:weathered_copper")
    for z in (16, 24):
        t.clear((39, 2, z), (39, 4, z))
        t.fill((39, 1, z), (39, 2, z), "minecraft:oxidized_copper_grate")

    # Removed standardized modules are staged at east parts issue in the same
    # positional grammar as the missing Lane-04 rollers and drive assemblies.
    for z in (24, 25, 27, 28):
        t.set(45, 2, z, "create:shaft", axis="x")
        t.set(46, 2, z, "create:depot")
        t.set(47, 2, z, "create:andesite_casing")
    t.set(45, 3, 24, "create:large_cogwheel", axis="x")
    t.set(47, 3, 24, "create:large_cogwheel", axis="x")
    t.set(45, 3, 28, "immersiveengineering:connector_lv", facing="up")
    t.set(47, 3, 28, "immersiveengineering:connector_lv", facing="up")

    # Lanes 01-03 receive the best salvaged spares at their existing service
    # faces; these are added modules, not relocated lane geometry.
    for x in (21, 27, 33):
        t.set(x, 2, 18, "create:large_cogwheel", axis="x")
        t.set(x, 3, 18, "create:shaft", axis="x")
        t.set(x, 4, 18, "immersiveengineering:connector_lv", facing="up")
        t.set(x, 2, 26, "create:brass_casing")
        t.set(x, 3, 26, "create:mechanical_pump", facing="south")

    # A temporary overhead drive/service bypass crosses all four lanes, ties
    # into existing branches, and is visibly patched at the dead fourth line.
    t.fill((19, 7, 24), (39, 7, 24), "create:fluid_pipe")
    for x in (19, 25, 31, 37):
        t.set(x, 7, 24, "create:mechanical_pump", facing="east")
    t.fill((36, 8, 24), (39, 8, 24), "minecraft:weathered_cut_copper")

    # Shrinking stores and tagged removed modules accumulate at real issue and
    # rework positions while circulation and proof/LOR reservations stay clear.
    t.fill((44, 5, 24), (44, 6, 28), "immersiveengineering:crate")
    t.fill((14, 2, 24), (14, 4, 26), "minecraft:weathered_copper")
    t.set(16, 3, 28, "minecraft:yellow_concrete")
    t.fill((9, 10, 14), (10, 10, 15), "minecraft:weathered_cut_copper")

    # The component-starved monitor receives a temporary intact patch. D3 will
    # fail only this documented intervention and the connected east service edge.
    t.fill((36, 14, 24), (38, 14, 26), "minecraft:weathered_cut_copper")
    t.fill((46, 10, 29), (47, 10, 33), "minecraft:weathered_cut_copper")

    base.wall_sign(t, 36, 5, 13, "north", "LANE 04 LOCKOUT", "PARTS TRANSFER")
    base.wall_sign(t, 36, 5, 27, "south", "LANE 04 INACTIVE", "BED RETAINED")
    base.wall_sign(t, 35, 5, 18, "east", "MODULES REMOVED", "WORK ORDER 4-17")
    base.wall_sign(t, 35, 5, 25, "east", "DRIVES REMOVED", "ISSUE TO 01-03")
    base.wall_sign(t, 45, 4, 24, "west", "SALVAGED MODULES", "INSPECT BEFORE USE")
    base.wall_sign(t, 45, 4, 28, "west", "STOCK CRITICAL", "NO NEW DRIVES")
    base.wall_sign(t, 19, 8, 24, "south", "TEMP SERVICE BUS", "LINES 01-03 PRIORITY")
    base.wall_sign(t, 9, 12, 14, "east", "MAINT. SHORTAGE", "TRANSFER AUTHORIZED")

    _assert_history_freeze(build_d0(), t, "D1")
    return t


def build_d3() -> base.Template:
    """Grow restrained long-abandonment damage from the starved Lane-04 system."""
    t = build_d1()

    # The temporary Lane-04 monitor patch opens locally. Primary side rails and
    # neighboring monitor bays survive; weathered edges remain supported.
    t.clear((37, 15, 24), (38, 15, 26))
    t.clear((38, 13, 24), (38, 14, 26))
    t.fill((36, 14, 23), (38, 14, 23), "minecraft:weathered_cut_copper")
    t.fill((36, 14, 27), (38, 14, 27), "minecraft:weathered_cut_copper")
    t.fill((36, 13, 24), (36, 14, 26), "minecraft:weathered_cut_copper")

    # Roof fragments land on the already locked lane and removed-module gaps.
    for pos in ((37, 3, 24), (38, 3, 25), (36, 3, 24), (39, 1, 25)):
        t.set(*pos, "minecraft:gravel")
    t.set(36, 3, 25, "minecraft:weathered_cut_copper")

    # Water follows the opened monitor, Lane-04 service shoulder and depressed
    # drive trench rather than spreading evenly through the facility.
    t.fill((35, 1, 23), (35, 1, 28), "minecraft:moss_block")
    t.fill((36, 1, 26), (39, 1, 28), "minecraft:mossy_stone_bricks")
    t.fill((40, 0, 23), (41, 0, 27), "minecraft:mossy_cobblestone")
    for pos in ((35, 2, 23), (39, 3, 27), (40, 1, 23), (41, 1, 28)):
        t.set(*pos, "minecraft:cobweb")
    for pos in ((35, 2, 27), (39, 2, 28), (41, 1, 24)):
        t.set(*pos, "minecraft:brown_mushroom")

    # Connected east clerestory/service flashing fails locally. Fragments land
    # on the exterior service strip directly below, outside protected routes.
    t.clear((46, 6, 31), (46, 8, 33))
    t.fill((46, 5, 30), (46, 5, 34), "minecraft:weathered_cut_copper")
    t.fill((45, 9, 31), (47, 9, 33), "minecraft:weathered_cut_copper")
    for pos in ((47, 1, 31), (48, 1, 32), (47, 1, 33), (48, 1, 34)):
        t.set(*pos, "minecraft:gravel")
    t.fill((45, 0, 29), (48, 0, 35), "minecraft:cracked_stone_bricks")

    # Dock-04 and east service exposure remain subordinate to the Lane-04 cause.
    t.fill((39, 0, 38), (44, 0, 42), "minecraft:mossy_cobblestone")
    for pos in ((40, 2, 34), (42, 2, 35), (44, 2, 32), (45, 3, 30)):
        t.set(*pos, "minecraft:cobweb")

    # Final gameplay nodes are added after historical and route freeze checks.
    _assert_history_freeze(build_d0(), t, "D3-pre-gameplay")
    _place_proof_and_encounters(t)
    _assert_d3_contracts(t)
    return t


def _place_proof_and_encounters(t: base.Template) -> None:
    if _name(t, PROOF_POS) not in AIR or _name(t, (9, 12, 17)) not in AIR or _name(t, (10, 11, 17)) not in AIR:
        raise AssertionError("OWS-010 records proof position, headroom or east approach is obstructed")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")

    for (x, y, z), mob in SPAWNERS.items():
        if _name(t, (x, y, z)) not in AIR or _name(t, (x, y + 1, z)) not in AIR:
            raise AssertionError(f"OWS-010 spawner position obstructed at {(x, y, z)}")
        t.spawner(x, y, z, mob, count=1, nearby=3)


def _assert_history_freeze(d0: base.Template, state: base.Template, label: str) -> None:
    if tuple(state.size) != SIZE:
        raise AssertionError(f"OWS-010 {label} bounds changed: {state.size}")

    # Three maintained lanes remain exact at their continuous material centers.
    for center in (19, 25, 31):
        for z in range(12, 29):
            if _name(state, (center, 3, z)) != _name(d0, (center, 3, z)):
                raise AssertionError(f"{label} changed maintained lane at {(center, 3, z)}")

    # Lane 04 retains endpoints and at least thirteen of seventeen transfer
    # modules; only the four declared replaceable positions may be absent.
    for z in (12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 26, 27, 28):
        if _name(state, (37, 3, z)) != "create:depot":
            raise AssertionError(f"{label} lost undeclared Lane-04 module at {(37, 3, z)}")

    # Inbound pair, induction, destination trunk, return and outbound pair all
    # remain mechanically recognizable in every historical state.
    for center in (20, 27):
        for z in range(31, 37):
            if _name(state, (center, 3, z)) != "create:depot":
                raise AssertionError(f"{label} changed inbound tongue at {(center, 3, z)}")
    for x in range(18, 43):
        if _name(state, (x, 3, 11)) != "create:depot":
            raise AssertionError(f"{label} changed destination trunk at {(x, 3, 11)}")
    for z in range(12, 32):
        if _name(state, (41, 5, z)) != "create:depot":
            raise AssertionError(f"{label} changed east return at {(41, 5, z)}")
    for center in (34, 41):
        for z in range(32, 37):
            if _name(state, (center, 3, z)) != "create:depot":
                raise AssertionError(f"{label} changed outbound buffer at {(center, 3, z)}")

    # Frozen circulation remains two-wide and the principal controlled doors and
    # stair systems survive. Non-colliding environmental blocks are kept away.
    gate_b._assert_clear(state, (15, 2, 18), (16, 4, 23), f"{label} operator gallery")
    gate_b._assert_clear(state, (17, 8, 20), (42, 9, 21), f"{label} cross aisle")
    gate_b._assert_clear(state, (42, 2, 12), (44, 3, 14), f"{label} north maintenance route")
    gate_b._assert_clear(state, (42, 2, 29), (44, 3, 31), f"{label} south maintenance route")
    for x, z in ((9, 4),):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(state, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"{label} lost north staff door at {(x + dx, y, z)}")
    for x, z in ((48, 20),):
        for dz in (0, 1):
            for y in (2, 3):
                if _name(state, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"{label} lost east service door at {(x, y, z + dz)}")
    if _count(state, "minecraft:smooth_stone_stairs") < 28:
        raise AssertionError(f"{label} lost a playable stair system")

    # Exact empty LOR context is immutable and no structure NBT may name its item.
    for shelf in LOR_SHELVES:
        if _name(state, shelf) != "supplementaries:item_shelf":
            raise AssertionError(f"{label} changed empty LOR shelf at {shelf}")
    serialized_nbt = "\n".join(repr(nbt) for _, nbt in state.blocks.values() if nbt)
    if LORE_ITEM in serialized_nbt:
        raise AssertionError(f"{label} serialized duplicate LOR-006 item")

    # Atlas structure and connected utilities remain predominant despite the
    # small documented Lane-04 and east-edge damage zones.
    if _count(state, "tfmg:steel_block") < 2700:
        raise AssertionError(f"{label} removed too much accepted primary structure")
    if _count(state, "create:fluid_pipe") < 150:
        raise AssertionError(f"{label} removed too much connected service anatomy")
    if sum((_name(state, pos) or "").endswith("_wall_sign") for pos in state.blocks) < 30:
        raise AssertionError(f"{label} preserves too little Atlas identity")


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-010 canonical proof chest is missing")
    nbt = row[1]
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-010 proof chest uses the wrong loot table")
    if _name(t, (9, 12, 17)) not in AIR or _name(t, (10, 11, 17)) not in AIR:
        raise AssertionError("OWS-010 proof headroom or east interaction face is blocked")
    matching = sum(1 for _, block_nbt in t.blocks.values() if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-010 requires exactly one canonical proof node; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if _count(t, "minecraft:spawner") != len(SPAWNERS):
        raise AssertionError("OWS-010 D3 encounter count drifted")
    for pos, expected_mob in SPAWNERS.items():
        row = t.blocks.get(pos)
        if row is None or t.palette[row[0]]["Name"] != "minecraft:spawner":
            raise AssertionError(f"OWS-010 encounter missing at {pos}")
        nbt = row[1] or {}
        mob = ((nbt.get("SpawnData") or {}).get("entity") or {}).get("id")
        if mob != expected_mob:
            raise AssertionError(f"OWS-010 encounter mob drifted at {pos}: {mob}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 14:
            raise AssertionError(f"OWS-010 encounter too close to proof at {pos}")

    # Gameplay placement must not disturb the accepted circulation or LOR hold.
    _assert_history_freeze(build_d0(), t, "D3-final")
    if _count(t, "minecraft:chest") != 1:
        raise AssertionError("OWS-010 D3 must contain exactly one chest/proof node")


def _model_sha(t: base.Template, label: str) -> str:
    temp_name = f"_heavy_review_ows010_gate_c_hash_{label}"
    temp_nbt = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        return hashlib.sha256(temp_nbt.read_bytes()).hexdigest()
    finally:
        temp_nbt.unlink(missing_ok=True)


def _serialize_and_render(label: str, damage_state: str, t: base.Template, revision: str, head: str) -> tuple[dict, str]:
    temp_name = f"_heavy_review_ows010_gate_c_{label}_r1"
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
            source_path=f"review-only:render_ows010_gate_c_damage_states.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=CAMERA_SET,
        )
        fixed_cutaway = 10
        cut_path = OUTPUT_DIR / label / "interior_cutaway.png"
        cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= fixed_cutaway}
        isometric(size, cutaway_blocks, False, f"{TARGET} — Gate C — {damage_state} — interior cutaway Y<={fixed_cutaway}").save(cut_path)
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
    draw.text((margin, 12), "OWS-010 — Gate C r1 — fixed-camera D0 / D1 / D3 comparison", fill=(245, 245, 245))
    draw.text((margin, 36), f"dimensions=49x16x43  camera_set={CAMERA_SET}", fill=(210, 210, 210))
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
        raise AssertionError("OWS-010 shipping drifted before Gate-C render")

    d0, d1, d3 = build_d0(), build_d1(), build_d3()
    d0_sha = _model_sha(d0, "d0_preflight")
    if d0_sha != ACCEPTED_GATE_B_SHA256:
        raise AssertionError(f"OWS-010 D0 drifted from accepted Gate B: {d0_sha} != {ACCEPTED_GATE_B_SHA256}")
    d1_changes = len(_diff_positions(d0, d1))
    d3_changes = len(_diff_positions(d0, d3))
    if not 140 <= d1_changes <= 500:
        raise AssertionError(f"OWS-010 D1 history scope unexpected: {d1_changes}")
    if not 240 <= d3_changes <= 700 or d3_changes <= d1_changes + 100:
        raise AssertionError(f"OWS-010 D3 damage scope unexpected: D1={d1_changes}, D3={d3_changes}")

    head = _git_head()
    revision = f"gate-c-r1@{head[:8]}"
    rendered = {
        "D0": _serialize_and_render("d0", "D0 exact accepted intact operation", d0, revision, head),
        "D1": _serialize_and_render("d1", "D1 Lane-04 cannibalization and maintenance shortage", d1, revision, head),
        "D3": _serialize_and_render("d3", "D3 localized Lane-04/service decay and current ruin", d3, revision, head),
    }
    manifests = {state: value[0] for state, value in rendered.items()}
    hashes = {state: value[1] for state, value in rendered.items()}
    if hashes["D0"] != ACCEPTED_GATE_B_SHA256:
        raise AssertionError("rendered OWS-010 D0 no longer matches accepted Gate B")

    comparison_path = OUTPUT_DIR / "damage_comparison.png"
    _damage_comparison(manifests, comparison_path)
    gate_manifest = {
        "target": TARGET,
        "gate": "gate_c_damage_states",
        "revision": revision,
        "fixed_camera_set": CAMERA_SET,
        "source_commit": head,
        "source_d0": "render_ows010_gate_b_intact.build_gate_b_intact",
        "accepted_gate_b_review_model_sha256": ACCEPTED_GATE_B_SHA256,
        "d0_review_model_sha256": hashes["D0"],
        "d0_exact_gate_b_match": True,
        "d1_review_model_sha256": hashes["D1"],
        "d3_review_model_sha256": hashes["D3"],
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "damage_states": ["D0", "D1", "D3"],
        "d2_disposition": "omitted_no_materially_distinct_acute_event_between_gradual_lane_cannibalization_and_long_abandonment",
        "gate_b_architecture_routes_utilities_identity_asserted_all_states": True,
        "proof_position": list(PROOF_POS),
        "proof_loot_table": PROOF_LOOT_TABLE,
        "proof_item": PROOF_ITEM,
        "lore_item": LORE_ITEM,
        "lore_item_occurrences_in_canonical_ows010_loot": 0,
        "empty_lor_shelves_preserved": [list(pos) for pos in LOR_SHELVES],
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
        raise AssertionError("OWS-010 shipping changed during Gate-C render")
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(
        json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    if SHIPPING_PATH.read_bytes() != shipping_bytes:
        raise AssertionError("OWS-010 shipping bytes changed during Gate-C render")
    print(
        f"Rendered {TARGET} Gate C r1: D0 exact={hashes['D0'] == ACCEPTED_GATE_B_SHA256}, "
        f"D1 changes={d1_changes}, D3 changes={d3_changes}; independent review required."
    )


if __name__ == "__main__":
    main()

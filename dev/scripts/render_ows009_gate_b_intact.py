#!/usr/bin/env python3
"""Build and render OWS-009 Gate-B r1 intact operating candidate.

The review model starts from the exact independently accepted Gate-A r2
massing and adds doctrine Passes 7-12 only. It never writes shared state,
production dispatch, registries, or the authoritative shipping structure.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows009_gate_a_massing_r2 import build_gate_a_massing_r2
from render_structure_review import unpack_structure


TARGET = "OWS-009"
SIZE = (49, 18, 41)
CAMERA_SET = "ows009_fixed_v1"
GATE_A_MODEL_SHA256 = "cbcdb6151de083cb81fd8e3aa52f81c5741901e4b97c3fe977fa15409e05de83"
FROZEN_SHIPPING_SHA256 = "d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d"
FROZEN_SHIPPING_BLOB = "4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a"
TEMP_GATE_A_NAME = "_heavy_review_ows009_gate_a_freeze_check"
TEMP_GATE_A_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_GATE_A_NAME}.nbt"
TEMP_NAME = "_heavy_review_ows009_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_b_intact" / "r1"
SHIPPING_PATH = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt"
GATE_A_REVIEW = ROOT / "old_world_narrative/reviews/heavy_rebuild/OWS-009_GATE_A_R2_REVIEW.md"
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _double_door_z(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x + 1, y + 2, z))
    base.double_door(t, x, y, z, facing, "iron")


def _double_door_x(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x, y + 2, z + 1))
    base.door(t, x, y, z, facing, "iron", "left")
    base.door(t, x, y, z + 1, facing, "iron", "right")


def _pass7_structural_system(t: base.Template) -> None:
    """Resolve accepted masses into three supported long-span work cells."""
    # Cell-edge frames carry stepped shells, upper monitors and roof plant.
    for x, roof_y in ((4, 9), (14, 10), (25, 10), (35, 9)):
        for z in (9, 16, 23, 32):
            t.fill((x, 1, z), (x, roof_y, z), "tfmg:steel_block")
    for x1, x2, beam_y in ((4, 14, 9), (14, 25, 10), (25, 35, 9)):
        for z in (10, 16, 23, 32):
            t.fill((x1, beam_y, z), (x2, beam_y + 1, z), "tfmg:steel_block")

    # Monitor loads bear on paired portal-to-spine rails, not roof decoration.
    for x1, x2, y, z1, z2 in ((6, 12, 10, 12, 23), (17, 23, 12, 10, 25), (28, 34, 11, 14, 27)):
        t.fill((x1, y, z1), (x1, y, z2), "tfmg:steel_block")
        t.fill((x2, y, z1), (x2, y, z2), "tfmg:steel_block")

    # East annex receives a shorter service-frame grid aligned to its three
    # accepted program bands: public, parts and controlled records/core.
    for z, top in ((8, 8), (19, 8), (20, 9), (27, 10), (34, 10)):
        t.fill((36, 1, z), (36, top, z), "tfmg:steel_block")
        t.fill((44, 1, z), (44, top, z), "tfmg:steel_block")
        t.fill((36, top, z), (44, top, z), "tfmg:steel_block")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Protect customer, vehicle, technician, parts and core routes."""
    # Three full-depth vehicle lanes remain continuous from recovery apron.
    for x1, x2, color in ((7, 11, "minecraft:cyan_concrete"), (18, 22, "minecraft:orange_concrete"), (28, 32, "minecraft:white_concrete")):
        t.fill((x1, 1, 8), (x2, 1, 23), "minecraft:smooth_stone")
        t.fill((x1, 1, 9), (x1, 1, 22), color)
        t.fill((x2, 1, 9), (x2, 1, 22), color)

    # Accepted transverse vehicle field and technician spine retain their
    # widths, with separate visual datums and no floor-mounted equipment.
    t.fill((4, 1, 24), (34, 1, 27), "minecraft:light_gray_concrete")
    t.fill((4, 1, 25), (34, 1, 26), "minecraft:yellow_concrete")
    t.fill((4, 1, 28), (34, 1, 31), "minecraft:polished_blackstone")
    t.fill((4, 1, 29), (34, 1, 30), "tfmg:factory_floor")

    # Public route, technician handoff and support routes use controlled doors.
    _double_door_z(t, 40, 2, 7, "north")
    _double_door_x(t, 35, 2, 13, "east")
    _double_door_x(t, 35, 2, 23, "east")
    _double_door_x(t, 35, 2, 29, "east")
    _double_door_x(t, 44, 2, 23, "east")
    _double_door_z(t, 39, 2, 34, "south")

    # Floor datums keep public, parts and core routes opposed and legible.
    t.fill((39, 1, 8), (42, 1, 13), "minecraft:white_concrete")
    t.fill((37, 1, 13), (42, 1, 14), "minecraft:cyan_concrete")
    t.fill((37, 1, 23), (43, 1, 25), "minecraft:orange_concrete")
    t.fill((39, 1, 29), (40, 1, 33), "minecraft:yellow_concrete")


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Align envelope openings and drainage with the intact room program."""
    # Cell-specific high windows align with diagnostics, crane and calibration.
    t.fill((3, 6, 11), (3, 8, 14), "create:framed_glass")
    t.fill((3, 6, 18), (3, 8, 21), "create:framed_glass")
    t.fill((15, 9, 7), (23, 11, 7), "create:framed_glass")
    t.fill((35, 7, 12), (35, 9, 16), "create:framed_glass")
    t.fill((35, 7, 19), (35, 9, 22), "create:framed_glass")

    # Roof-edge drains tie the accepted profiles to the site rather than float.
    for x, z, top in ((3, 10, 10), (3, 27, 10), (14, 33, 11), (25, 33, 11), (35, 18, 11), (44, 18, 8), (44, 29, 10)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")
    t.fill((4, 0, 33), (34, 0, 33), "minecraft:oxidized_copper_grate")
    t.fill((45, 0, 22), (48, 0, 22), "minecraft:oxidized_copper_grate")

    # Protected lamps identify vehicle, pedestrian and service thresholds.
    for x, y, z in ((5, 7, 6), (13, 7, 6), (16, 8, 6), (23, 8, 6), (27, 7, 6), (34, 7, 6), (39, 7, 7), (43, 7, 7), (45, 7, 22), (45, 7, 26), (38, 6, 34), (42, 6, 34)):
        t.set(x, y, z, "minecraft:redstone_lamp", lit="true")


def _pass10_interior_architecture(t: base.Template) -> None:
    """Create legitimate public, support, records and core-control rooms."""
    # Customer bar: waiting/check-in north, service consultation south.
    t.fill((37, 1, 8), (43, 1, 18), "minecraft:smooth_quartz")
    base.partition_z(t, 15, 2, 37, 43, "minecraft:white_concrete")
    _double_door_z(t, 40, 2, 15, "south")
    t.fill((37, 2, 15), (39, 5, 15), "create:framed_glass")
    t.fill((42, 2, 15), (43, 5, 15), "create:framed_glass")

    # Parts receive east and clean issue west share a controlled center crossing.
    t.fill((37, 1, 21), (43, 1, 26), "tfmg:factory_floor")
    base.partition_x(t, 40, 2, 21, 26, "minecraft:light_gray_concrete")
    _double_door_x(t, 40, 2, 23, "west")

    # Records/proof node is separated from the south-facing core/rework buffer.
    t.fill((37, 1, 28), (43, 1, 33), "minecraft:polished_blackstone")
    base.partition_z(t, 31, 2, 37, 43, "minecraft:light_gray_concrete")
    _double_door_z(t, 39, 2, 31, "south")
    base.partition_x(t, 41, 2, 28, 30, "minecraft:polished_blackstone_bricks", doorway_z=29)
    base.door(t, 41, 2, 29, "east", "iron", "left")

    # Transparent safety wings bound equipment without closing the three cells.
    for x, z1, z2 in ((5, 11, 22), (13, 11, 22), (16, 11, 22), (24, 11, 22), (27, 11, 22), (34, 11, 22)):
        t.fill((x, 2, z1), (x, 4, z1 + 1), "create:framed_glass")
        t.fill((x, 2, z2 - 1), (x, 4, z2), "create:framed_glass")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install an intact intake-to-repair-to-calibration service chain."""
    # Bay 01 diagnostics/lockout: two sensor arches scan a clear vehicle lane.
    for z in (12, 19):
        t.fill((5, 2, z), (5, 6, z), "tfmg:steel_block")
        t.fill((13, 2, z), (13, 6, z), "tfmg:steel_block")
        t.fill((5, 6, z), (13, 7, z), "minecraft:cyan_concrete")
        t.set(6, 5, z, "minecraft:observer", facing="east")
        t.set(12, 5, z, "minecraft:observer", facing="west")
    for z in (13, 16, 20):
        t.set(7, 1, z, "create:depot")
        t.set(11, 1, z, "create:depot")
    t.fill((5, 2, 15), (5, 3, 17), "ae2:drive")
    t.set(6, 2, 16, "ae2:terminal")
    t.fill((12, 2, 15), (13, 3, 17), "immersiveengineering:sheetmetal_steel")

    # Bay 02 heavy repair: grated inspection pit, paired lift towers and a
    # suspended handling rail retain a five-block clear central vehicle axis.
    t.fill((18, 0, 13), (22, 0, 20), "minecraft:polished_blackstone")
    t.fill((18, 1, 13), (22, 1, 20), "minecraft:oxidized_copper_grate")
    for x in (16, 24):
        for z in (12, 20):
            t.fill((x, 2, z), (x, 6, z), "tfmg:steel_block")
            t.set(x, 3, z, "create:mechanical_pump", facing="up")
    t.fill((16, 8, 16), (24, 9, 16), "tfmg:steel_block")
    for x in (18, 21):
        t.fill((x, 6, 16), (x, 8, 16), "minecraft:chain")
        t.set(x, 5, 16, "create:depot")
    for z in (11, 14, 19, 22):
        t.set(16, 2, z, "create:depot")
        t.set(24, 2, z, "create:depot")
    t.set(16, 3, 17, "create:mechanical_press", facing="east")
    t.set(24, 3, 17, "create:mechanical_press", facing="west")

    # Bay 03 calibration/release: paired roller beds, sensor crown, dyno bank
    # and final release console distinguish it from intake diagnostics.
    for z in (13, 16, 19):
        t.fill((28, 1, z), (32, 1, z), "create:shaft")
    t.fill((27, 2, 20), (27, 6, 20), "tfmg:steel_block")
    t.fill((34, 2, 20), (34, 6, 20), "tfmg:steel_block")
    t.fill((27, 6, 20), (34, 7, 20), "minecraft:orange_concrete")
    for x in (28, 33):
        t.set(x, 5, 20, "minecraft:observer", facing="south")
        t.set(x, 2, 22, "ae2:terminal")
    t.fill((33, 2, 12), (34, 4, 16), "immersiveengineering:capacitor_mv")
    t.set(33, 2, 18, "create:mechanical_pump", facing="west")

    # Parts receive/issue, records/proof adjacency and core/rework quarantine.
    t.fill((37, 2, 21), (39, 4, 22), "immersiveengineering:crate")
    t.fill((37, 2, 25), (39, 3, 26), "immersiveengineering:crate")
    for z in (21, 26):
        t.set(42, 2, z, "create:depot")
    t.set(42, 4, 24, "ae2:terminal")
    t.fill((42, 2, 28), (43, 4, 30), "ae2:drive")
    t.set(41, 2, 28, "ae2:terminal")
    t.fill((37, 2, 32), (38, 4, 33), "immersiveengineering:sheetmetal_steel")
    t.fill((42, 2, 32), (43, 4, 33), "immersiveengineering:sheetmetal_steel")

    # Customer-facing check-in stays physically protected from all vehicle flow.
    base.desk(t, 37, 2, 13, "north")
    t.set(38, 3, 13, "ae2:terminal")
    for x in (37, 43):
        t.fill((x, 2, 9), (x, 2, 11), "minecraft:smooth_quartz_stairs", facing="east" if x == 37 else "west", half="bottom", shape="straight", waterlogged="false")

    # Rear overhead services: separate power and compressed-air/exhaust trunks
    # branch to every cell and rise into its accepted roof-plant housing.
    t.fill((5, 7, 30), (34, 7, 30), "create:fluid_pipe")
    t.fill((5, 8, 32), (34, 8, 32), "immersiveengineering:sheetmetal_steel")
    for x, top in ((9, 14), (20, 16), (31, 15)):
        t.fill((x, 7, 15), (x, 7, 30), "create:fluid_pipe")
        t.fill((x, 7, 30), (x, top, 30), "create:fluid_pipe")
        t.set(x, 8, 27, "create:mechanical_pump", facing="south")
        t.set(x, top - 1, 29, "create:encased_fan", facing="south")
    for x in (6, 17, 28):
        t.fill((x, 2, 32), (x + 2, 4, 33), "immersiveengineering:capacitor_mv")
        t.set(x + 1, 5, 32, "immersiveengineering:connector_lv", facing="up")

    # Drains connect cell edges to the rear trench, leaving vehicle axes clear.
    for x in (6, 13, 17, 24, 27, 33):
        t.fill((x, 1, 10), (x, 1, 23), "minecraft:oxidized_copper_grate")
        t.fill((x, 1, 23), (x, 1, 28), "minecraft:oxidized_copper_grate")

    # Work and circulation lighting follows the three cells and rear spine.
    for x in (6, 10, 18, 22, 28, 32):
        t.set(x, 8, 14, "minecraft:sea_lantern")
        t.set(x, 8, 21, "minecraft:sea_lantern")
    for x in (7, 13, 19, 25, 31):
        t.set(x, 7, 29, "minecraft:sea_lantern")


def _pass12_atlas_identity(t: base.Template) -> None:
    """Apply architectural Atlas identity and restrained process wayfinding."""
    # Interior portal crowns echo the accepted charcoal/orange exterior frame.
    for x1, x2, y in ((5, 13, 7), (16, 24, 8), (27, 34, 7)):
        t.fill((x1, y, 9), (x2, y + 1, 9), "minecraft:polished_blackstone")
        t.fill((x1 + 1, y, 10), (x2 - 1, y, 10), "minecraft:orange_concrete")
    t.fill((4, 4, 28), (34, 5, 28), "minecraft:orange_concrete")

    base.wall_sign(t, 6, 6, 7, "north", "ATLAS SERVICE", "DIAGNOSTICS / 01")
    base.wall_sign(t, 17, 7, 7, "north", "ATLAS SERVICE", "HEAVY REPAIR / 02")
    base.wall_sign(t, 28, 6, 7, "north", "ATLAS SERVICE", "CALIBRATE / 03")
    base.wall_sign(t, 38, 6, 7, "north", "CUSTOMER SERVICE", "CHECK-IN")
    base.wall_sign(t, 35, 5, 13, "west", "SERVICE HANDOFF", "STAFF CONTROL")
    base.wall_sign(t, 44, 6, 23, "west", "PARTS RECEIVE", "DELIVERY CONTROL")
    base.wall_sign(t, 36, 5, 23, "east", "PARTS ISSUE", "TECHNICIANS")
    base.wall_sign(t, 36, 5, 29, "east", "SERVICE RECORDS", "CONTROLLED")
    base.wall_sign(t, 42, 5, 28, "west", "PROOF NODE", "RECORDS ADJACENT")
    base.wall_sign(t, 39, 5, 34, "north", "CORE / REWORK", "QUARANTINE RETURN")
    base.wall_sign(t, 7, 6, 23, "south", "TRANSVERSE FIELD", "KEEP CLEAR")
    base.wall_sign(t, 7, 6, 31, "south", "TECHNICIAN SPINE", "AIR / POWER / DATA")
    base.wall_sign(t, 18, 6, 20, "north", "INSPECTION PIT", "LIFT LOCKOUT")
    base.wall_sign(t, 28, 6, 20, "north", "LOAD TEST", "CALIBRATION")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing_r2()
    _pass7_structural_system(t)
    _pass8_circulation_and_access(t)
    _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t)
    _pass11_operational_systems(t)
    _pass12_atlas_identity(t)
    return t


def _assert_gate_a_source_freeze() -> None:
    gate_a = build_gate_a_massing_r2()
    gate_a.save(TEMP_GATE_A_NAME)
    try:
        actual = hashlib.sha256(TEMP_GATE_A_NBT.read_bytes()).hexdigest()
    finally:
        TEMP_GATE_A_NBT.unlink(missing_ok=True)
    if actual != GATE_A_MODEL_SHA256:
        raise AssertionError(f"accepted Gate-A r2 source drifted: {actual} != {GATE_A_MODEL_SHA256}")


def _assert_clear(t: base.Template, low: tuple[int, int, int], high: tuple[int, int, int], label: str) -> None:
    for x in range(low[0], high[0] + 1):
        for y in range(low[1], high[1] + 1):
            for z in range(low[2], high[2] + 1):
                name = _name(t, (x, y, z))
                if name not in AIR | {"minecraft:iron_door"}:
                    raise AssertionError(f"{label} obstruction at {(x, y, z)}: {name}")


def _assert_intact_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-009 Gate-B dimensions drifted: {t.size}")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in t.blocks):
        raise AssertionError("OWS-009 Gate-B exceeds accepted 49x18x41 envelope")

    # Exact accepted r2 massing anchors survive the intact-state work.
    frozen = {
        (2, 5, 15): "tfmg:steel_block",
        (2, 6, 20): "minecraft:orange_concrete",
        (10, 11, 36): "tfmg:steel_block",
        (20, 12, 35): "minecraft:orange_concrete",
        (8, 12, 12): "create:framed_glass",
        (20, 15, 10): "create:framed_glass",
        (28, 13, 20): "create:framed_glass",
        (45, 8, 24): "minecraft:orange_concrete",
        (39, 7, 36): "minecraft:orange_concrete",
        (20, 15, 5): "minecraft:polished_blackstone",
    }
    for pos, expected in frozen.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"accepted Gate-A r2 aspect changed at {pos}: {actual} != {expected}")

    # Vehicle axes, transverse movement, technician spine and protected annex
    # routes retain playable two-block width/three-block height.
    for low, high, label in (
        ((8, 2, 8), (10, 4, 22), "Bay-01 vehicle lane"),
        ((19, 2, 8), (21, 4, 22), "Bay-02 vehicle lane"),
        ((29, 2, 8), (31, 4, 22), "Bay-03 vehicle lane"),
        ((5, 2, 24), (33, 3, 27), "transverse vehicle field"),
        ((5, 2, 28), (33, 3, 31), "rear technician spine"),
        ((39, 2, 8), (42, 3, 14), "customer route"),
        ((41, 2, 23), (43, 3, 25), "parts route"),
        ((39, 2, 29), (40, 3, 34), "records/core route"),
    ):
        _assert_clear(t, low, high, label)

    # Every controlled two-wide threshold has complete lower and upper halves.
    doors_z = ((40, 7), (40, 15), (39, 31), (39, 34))
    for x, z in doors_z:
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"controlled Z-wall door missing at {(x + dx, y, z)}")
    doors_x = ((35, 13), (35, 23), (35, 29), (40, 23), (44, 23))
    for x, z in doors_x:
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"controlled X-wall door missing at {(x, y, z + dz)}")

    names = [t.palette[entry[0]]["Name"] for entry in t.blocks.values()]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner"}
    if forbidden.intersection(names):
        raise AssertionError("Gate-B contains deferred proof or encounter blocks")
    requirements = {
        "create:fluid_pipe": 90,
        "minecraft:oxidized_copper_grate": 120,
        "tfmg:steel_block": 650,
        "minecraft:iron_door": 36,
        "create:depot": 14,
        "ae2:terminal": 6,
        "immersiveengineering:capacitor_mv": 20,
    }
    for name, minimum in requirements.items():
        if names.count(name) < minimum:
            raise AssertionError(f"intact system coverage sparse for {name}: {names.count(name)} < {minimum}")
    if sum(name.endswith("_wall_sign") for name in names) < 14:
        raise AssertionError("Atlas intact-state wayfinding unexpectedly sparse")


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    review = GATE_A_REVIEW.read_text(encoding="utf-8")
    if "**Decision:** **PASSED**" not in review or GATE_A_MODEL_SHA256 not in review:
        raise AssertionError("OWS-009 accepted Gate-A r2 authority/hash missing")
    shipping_bytes = SHIPPING_PATH.read_bytes()
    if hashlib.sha256(shipping_bytes).hexdigest() != FROZEN_SHIPPING_SHA256:
        raise AssertionError("OWS-009 shipping SHA drifted before Gate-B render")
    if _git_blob(SHIPPING_PATH) != FROZEN_SHIPPING_BLOB:
        raise AssertionError("OWS-009 shipping Git blob drifted before Gate-B render")
    _assert_gate_a_source_freeze()

    model = build_gate_b_intact()
    _assert_intact_contracts(model)
    model.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        if len(blocks) < 8500:
            raise AssertionError(f"Gate-B model unexpectedly sparse: {len(blocks)} blocks")
        head = _git_head()
        manifest = render_review_set(
            target=TARGET,
            gate="gate_b_intact",
            revision=f"intact-r1@{head[:8]}",
            damage_state="D0 intact / operational",
            source_commit=head,
            source_path="review-only:render_ows009_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=CAMERA_SET,
        )
        manifest.update({
            "review_model_nbt_sha256": hashlib.sha256(model_bytes).hexdigest(),
            "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "gate_a_r2_model_sha256": GATE_A_MODEL_SHA256,
            "placed_positions": len(blocks),
            "gate_a_frozen_aspects_asserted": 10,
            "gate_b_passes_implemented": [7, 8, 9, 10, 11, 12],
            "controlled_door_blocks_asserted": 36,
            "history_damage_encounters_loot_proof_present": False,
            "authoritative_shipping_modified": False,
            "shipping_nbt_sha256_before": FROZEN_SHIPPING_SHA256,
            "shipping_nbt_sha256_after": hashlib.sha256(SHIPPING_PATH.read_bytes()).hexdigest(),
            "shipping_nbt_git_blob_before": FROZEN_SHIPPING_BLOB,
            "shipping_nbt_git_blob_after": _git_blob(SHIPPING_PATH),
            "visual_review_status": "rendered_pending_independent_review",
        })
        if manifest["shipping_nbt_sha256_after"] != FROZEN_SHIPPING_SHA256 or manifest["shipping_nbt_git_blob_after"] != FROZEN_SHIPPING_BLOB:
            raise AssertionError("OWS-009 shipping changed during Gate-B render")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    if SHIPPING_PATH.read_bytes() != shipping_bytes:
        raise AssertionError("OWS-009 shipping bytes changed during Gate-B render")
    print(
        f"Rendered {TARGET} Gate B r1 intact at {manifest['dimensions']} with "
        f"{manifest['placed_positions']} positions; independent review required."
    )


if __name__ == "__main__":
    main()

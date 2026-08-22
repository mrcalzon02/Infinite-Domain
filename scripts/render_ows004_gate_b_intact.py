#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-004 Gate-B D0 intact operating review.

Starts from the approved Gate-A r1 massing and adds only intact architecture,
circulation, operational systems and VCF identity. No proof loot, encounters,
containment overlay, collapse damage or microdetail are permitted at Gate B.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows004_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows004_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_b_intact" / "r1"

LEVELS = (9, 16, 23, 30)


def _public_and_podium(t: base.Template) -> None:
    """Resolve public/demo and industrial podium into usable, separated rooms."""
    # Public entrance and lobby/demo room.
    base.double_door(t, 20, 2, 6, "north", "iron")
    t.fill((8, 1, 7), (33, 1, 15), "minecraft:quartz_block")
    # Controlled demonstration viewing wall into the tower side.
    t.fill((10, 2, 15), (27, 6, 15), "create:framed_glass")
    # Staff-control / records transition on the east side of public podium.
    base.partition_x(t, 29, 2, 7, 15, "minecraft:white_concrete", doorway_z=11)
    t.fill((30, 2, 8), (33, 3, 10), "minecraft:bookshelf")
    t.fill((30, 2, 13), (33, 2, 14), "create:depot")

    # Receiving shell: divide clean intake from dirty/spent-material return.
    base.partition_z(t, 23, 2, 35, 47, "minecraft:light_gray_concrete", doorways=(40,))
    t.fill((35, 1, 15), (47, 1, 22), "tfmg:factory_floor")
    t.fill((35, 1, 24), (47, 1, 30), "minecraft:polished_blackstone")
    for x in (36, 40, 44):
        t.fill((x, 2, 16), (x + 1, 3, 18), "immersiveengineering:crate")
    for x in (36, 41, 45):
        t.fill((x, 2, 26), (x, 3, 28), "create:cardboard_block")
    # Receiving portal doors and dirty-return door on east face.
    base.door(t, 48, 2, 20, "east", "iron", "left")
    base.door(t, 48, 2, 21, "east", "iron", "right")
    base.door(t, 48, 2, 27, "east", "iron", "left")

    # Rear harvest / packing / dispatch chain.
    base.partition_x(t, 31, 2, 32, 42, "minecraft:white_concrete", doorway_z=37)
    base.partition_x(t, 39, 2, 32, 42, "minecraft:white_concrete", doorway_z=37)
    # Harvest receipt / inspection.
    for x in (26, 28):
        t.set(x, 2, 34, "create:depot")
        t.set(x, 3, 34, "create:mechanical_press", facing="north")
    # Packing zone.
    t.fill((33, 2, 34), (37, 3, 36), "create:cardboard_block")
    # Finished dispatch stock.
    t.fill((41, 2, 34), (45, 4, 39), "immersiveengineering:crate")
    base.door(t, 34, 2, 43, "south", "iron", "left")
    base.door(t, 35, 2, 43, "south", "iron", "right")

    # Purposeful public / logistics signage.
    base.wall_sign(t, 18, 6, 5, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 22, 6, 5, "north", "MYCOLOGICAL", "VERTICAL FARM")
    base.wall_sign(t, 28, 4, 7, "west", "PUBLIC DEMO", "PRODUCTION VIEW")
    base.wall_sign(t, 35, 5, 13, "north", "CLEAN RECEIVING", "BATCH INTAKE")
    base.wall_sign(t, 47, 5, 25, "west", "SPENT RETURN", "SERVICE ONLY")
    base.wall_sign(t, 25, 5, 42, "south", "HARVEST CHECK", "GRADE / RELEASE")
    base.wall_sign(t, 33, 5, 42, "south", "PACKING")
    base.wall_sign(t, 41, 5, 42, "south", "OUTBOUND", "DISPATCH")


def _production_floor_plate(t: base.Template, y: int, upper: bool) -> None:
    """Create one standardized controlled cultivation module."""
    x1, x2, z1, z2 = (13, 37, 15, 34) if upper else (11, 39, 13, 36)
    # Continuous production floor and lighter central protected service aisle.
    t.fill((x1, y, z1), (x2, y, z2), "tfmg:factory_floor")
    aisle_x1, aisle_x2 = (23, 27)
    t.fill((aisle_x1, y, z1 + 2), (aisle_x2, y, z2 - 2), "minecraft:smooth_stone")

    # Cultivation banks on both sides of the protected aisle.
    left_x = range(x1 + 2, min(aisle_x1 - 1, x1 + 8), 3)
    right_start = max(aisle_x2 + 2, x2 - 8)
    right_x = range(right_start, x2 - 1, 3)
    for x in (*left_x, *right_x):
        for z in range(z1 + 3, z2 - 2, 5):
            t.fill((x, y + 1, z), (x + 1, y + 1, z + 2), "minecraft:mycelium")
            t.fill((x, y + 2, z), (x + 1, y + 2, z + 2), "minecraft:scaffolding")
            t.set(x, y + 3, z + 1, "minecraft:brown_mushroom")
            t.set(x + 1, y + 3, z + 1, "minecraft:red_mushroom")

    # Local inspection/work point beside freight handoff.
    t.fill((x2 - 5, y + 1, z2 - 4), (x2 - 2, y + 1, z2 - 3), "create:depot")
    t.set(x2 - 4, y + 2, z2 - 3, "minecraft:cauldron")

    # Environmental branch along service-side edge with floor manifold.
    service_z = z1 + 1
    t.fill((x1 + 2, y + 4, service_z), (x2 - 2, y + 4, service_z), "create:fluid_pipe")
    for x in (x1 + 4, x1 + 10, x2 - 10, x2 - 4):
        t.set(x, y + 4, service_z + 1, "create:encased_fan", facing="south")
    # Water/nutrient local tank and branch.
    t.fill((x1 + 1, y + 1, z2 - 5), (x1 + 2, y + 3, z2 - 4), "create:fluid_tank")
    t.fill((x1 + 3, y + 2, z2 - 4), (aisle_x1 - 1, y + 2, z2 - 4), "create:fluid_pipe")

    # Floor identity / batch-control signs.
    level_index = LEVELS.index(y) + 1
    base.wall_sign(t, aisle_x1 - 1, y + 3, z1 + 1, "south", f"CULTIVATION {level_index}", "CONTROLLED ZONE")
    base.wall_sign(t, x2 - 2, y + 3, z2 - 1, "north", "HARVEST HANDOFF", f"LEVEL {level_index}")


def _vertical_cores_and_services(t: base.Template) -> None:
    """Make the reserved cores usable and connect utilities floor-to-floor."""
    # West protected ladder/egress core with landings to each production floor.
    t.fill((7, 9, 27), (9, 38, 31), "minecraft:smooth_stone")
    t.clear((8, 9, 28), (8, 38, 29))
    for y in range(9, 39):
        t.set(8, y, 30, "minecraft:ladder", facing="north", waterlogged="false")
    for level in LEVELS:
        t.fill((8, level, 29), (12 if level < 23 else 14, level, 31), "minecraft:smooth_stone")
        t.clear((10 if level < 23 else 12, level + 1, 30), (12 if level < 23 else 14, level + 3, 31))

    # East freight/service spine: floors and a symbolic vertical transfer shaft.
    for level in LEVELS:
        t.fill((40, level, 18), (44, level, 30), "tfmg:factory_floor")
        t.fill((40, level + 1, 25), (44, level + 3, 29), "create:andesite_casing")
        # Controlled connection into production floor.
        t.clear((39 if level < 23 else 38, level + 1, 23), (40, level + 2, 25))
        base.door(t, 39 if level < 23 else 38, level + 1, 24, "west", "iron")

    # Continuous vertical utility headers with floor branches.
    t.fill((42, 9, 19), (42, 41, 19), "create:fluid_pipe")
    t.fill((43, 9, 20), (43, 41, 20), "tfmg:steel_block")
    for level in LEVELS:
        wall_x = 39 if level < 23 else 38
        t.fill((wall_x - 3, level + 4, 19), (42, level + 4, 19), "create:fluid_pipe")
        t.set(41, level + 2, 21, "create:mechanical_pump", facing="west")

    # Maintenance connection into roof plant / crown.
    t.fill((40, 39, 19), (44, 39, 31), "minecraft:smooth_stone")
    t.clear((39, 40, 23), (40, 42, 25))
    base.door(t, 39, 40, 24, "west", "iron")


def _upper_isolation_readiness(t: base.Template) -> None:
    """Provide D0 boundaries that later history can convert to active containment."""
    y = 30
    # Controlled vestibule between core handoff and cultivation floor.
    t.fill((33, y + 1, 21), (37, y + 4, 27), "minecraft:white_concrete")
    t.clear((34, y + 1, 22), (36, y + 3, 26))
    base.door(t, 33, y + 1, 24, "east", "iron")
    base.door(t, 37, y + 1, 24, "west", "iron")
    # Independent environmental shutoff/inspection node.
    t.set(35, y + 2, 22, "create:mechanical_pump", facing="west")
    t.fill((34, y + 2, 26), (36, y + 2, 26), "create:depot")
    base.wall_sign(t, 34, y + 4, 23, "south", "ENV BRANCH 04", "CONTROL / SHUTOFF")
    base.wall_sign(t, 36, y + 4, 25, "north", "QUALITY HOLD", "AUTHORIZED STAFF")


def _roof_crown_operations(t: base.Template) -> None:
    """Fill the accepted crown with real showcase cultivation and service access."""
    # Central maintenance aisle through greenhouse.
    t.fill((23, 39, 17), (27, 39, 32), "minecraft:smooth_stone")
    # Demonstration/cultivation rows.
    for x in (17, 20, 30, 33):
        for z in (19, 24, 29):
            t.fill((x, 40, z), (x + 1, 40, z + 2), "minecraft:mycelium")
            t.fill((x, 41, z), (x + 1, 42, z + 2), "minecraft:scaffolding")
            t.set(x, 43, z + 1, "minecraft:brown_mushroom")
    # Greenhouse environmental header connected toward service spine.
    t.fill((16, 44, 17), (35, 44, 17), "create:fluid_pipe")
    t.fill((35, 44, 17), (42, 44, 19), "create:fluid_pipe")
    for x in (18, 24, 30, 34):
        t.set(x, 44, 19, "create:encased_fan", facing="south")
    # Header tanks at crown/service boundary.
    t.fill((37, 40, 32), (39, 43, 34), "create:fluid_tank")
    base.wall_sign(t, 23, 43, 15, "north", "ROOFTOP SHOWCASE", "CONTROLLED CULTIVATION")
    base.wall_sign(t, 40, 42, 31, "north", "ENVIRONMENTAL PLANT", "MAINTENANCE")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing()
    _public_and_podium(t)

    # Add four real floor plates after the massing shells are established.
    for y in LEVELS:
        _production_floor_plate(t, y, upper=y >= 23)

    _vertical_cores_and_services(t)
    _upper_isolation_readiness(t)
    _roof_crown_operations(t)
    return t


def _assert_intact_contracts(t: base.Template) -> None:
    """Coordinate-level guards for the most important Gate-B promises."""
    # Protected central service aisles must remain clear above floor level.
    for y in LEVELS:
        z1, z2 = (15, 34) if y >= 23 else (13, 36)
        for x in range(23, 28):
            for z in range(z1 + 2, z2 - 1):
                for py in (y + 1, y + 2):
                    block = t.blocks.get((x, py, z))
                    if block is not None:
                        name = t.palette[block[0]]["Name"]
                        if name not in {"minecraft:air"}:
                            raise AssertionError(f"OWS-004 protected aisle obstruction at {(x, py, z)}: {name}")
    # Vertical egress ladder must be continuous.
    for y in range(9, 39):
        entry = t.blocks.get((8, y, 30))
        if entry is None or t.palette[entry[0]]["Name"] != "minecraft:ladder":
            raise AssertionError(f"OWS-004 egress ladder gap at y={y}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-B OWS-004 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-004 renderer skipped: status={status}")
        return

    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 Gate-B r1 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-004",
            gate="gate_b_intact",
            revision=f"intact-r1@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows004_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows004_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r1_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r1_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-004 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()

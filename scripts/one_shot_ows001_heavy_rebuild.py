#!/usr/bin/env python3
"""[SYSTEM REPORT] One-shot transport for the authoritative OWS-001 heavy rebuild.

This file is intentionally temporary. The proven Old World static workflow executes
it once, validates the resulting authoritative sources, and removes this transport
before committing the rebuild.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts" / "old_world_narrative_core.py"
BASE = ROOT / "scripts" / "generate_wasteland_sites.py"
VALIDATOR = ROOT / "scripts" / "validate_old_world_narrative.py"
STATE = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"

OLD_SPEC = '''    Spec("OWS-001", "ows_001_vcf_neighborhood_culture_service_depot", "infinite_domain:grocery_clean_master", "grocery", "kubejs:vcf_culture_service_manifest", "kubejs:vcf_return_crate_log", "Pre-crisis to early anomaly", ("minecraft:lime_concrete", "oritech:cooler_block", "immersiveengineering:crate"), {
        "silhouette_exterior_identity": "VCF green service blade and culture-drop canopy replace retail branding",
        "interior_zoning_circulation": "public issue counter, refrigerated culture lockers, return sorting and receiving remain legible",
        "functional_machinery_props": "cooler banks, sealed culture crates, return pallets and service workbench",
        "institutional_identity": "VCF green/white wayfinding and controlled issue-return workflow",
        "historical_damage_signature": "one quarantined cooler bay and backed-up return lane show the first supply anomaly",
        "narrative_evidence_loot": "guaranteed culture-service manifest and return-crate log establish mundane Evercrop ubiquity"}),'''

NEW_SPEC = '''    Spec("OWS-001", "ows_001_vcf_neighborhood_culture_service_depot", "infinite_domain:grocery_clean_master", "grocery", "kubejs:vcf_culture_service_manifest", "kubejs:vcf_return_crate_log", "Pre-crisis to early anomaly", (
        "minecraft:lime_concrete",
        "minecraft:white_concrete",
        "minecraft:oak_wall_sign",
        "oritech:cooler_block",
        "immersiveengineering:crate",
        "create:fluid_pipe",
        "minecraft:water_cauldron",
        "minecraft:yellow_concrete",
    ), {
        "silhouette_exterior_identity": "purpose-built Verdant Continuum Foods neighborhood service frontage, cold-chain roof plant, separate public threshold and rear culture-service dock replace the donor supermarket identity",
        "interior_zoning_circulation": "public issue, culture lockers, return intake, sanitation/quarantine, receiving, clean stock, crate consolidation and supervisor records are physically separated with distinct public, staff and service routes",
        "functional_machinery_props": "dense refrigerated locker banks, batch inspection, sanitation plumbing, clean and returned culture crates, service pallets and rooftop refrigeration form a complete neighborhood culture-service workflow",
        "institutional_identity": "full VERDANT CONTINUUM FOODS exterior identity, facility naming and purpose-driven VCF operational wayfinding establish the institution through architecture as well as green/white color coding",
        "historical_damage_signature": "a single quality-hold return bay and isolated cooler segment show an early anomaly being managed locally while the rest of the depot remains in ordinary service",
        "narrative_evidence_loot": "guaranteed culture-service manifest and return-crate log sit at the supervisor batch-records station where the mundane circulation and reuse of Evercrop cultures can be reconstructed"}),'''

OLD_BUILDER = '''def build_001():
    t = base.grocery_clean_master()
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:white_concrete"); t.fill((16, 9, 6), (22, 10, 6), "minecraft:lime_concrete"); t.fill((14, 6, 2), (24, 6, 5), "minecraft:lime_concrete")
    for x in (5, 9, 13, 17, 21, 25): t.set(x, 2, 20, "oritech:cooler_block")
    t.fill((5, 2, 24), (12, 3, 27), "immersiveengineering:crate"); t.fill((16, 2, 25), (22, 3, 27), "minecraft:lime_concrete"); t.fill((25, 2, 24), (29, 2, 27), "jaffabricate:pallet_full")
    t.fill((29, 1, 14), (35, 1, 18), "minecraft:yellow_concrete"); t.fill((33, 2, 14), (35, 4, 18), "minecraft:iron_bars"); t.chest(27, 2, 26, BY_TARGET["OWS-001"].loot_id, "west")
    return t'''

NEW_BUILDER = '''def build_001():
    t = base.grocery_clean_master()

    # Heavy rebuild: preserve the useful neighborhood shell, street relationship,
    # vestibule, rear dock and roof envelope while removing the supermarket program.
    t.clear((4, 2, 9), (34, 8, 28))

    # VCF exterior identity. This remains a mundane neighborhood service building,
    # but its cold-chain frontage now communicates institution and purpose at range.
    t.fill((4, 7, 7), (34, 10, 7), "minecraft:white_concrete")
    t.fill((5, 8, 6), (33, 9, 6), "minecraft:lime_concrete")
    t.fill((14, 6, 2), (24, 6, 5), "minecraft:white_concrete")
    t.fill((16, 6, 1), (22, 6, 2), "minecraft:lime_concrete")
    base.wall_sign(t, 17, 9, 5, "north", "VERDANT", "CONTINUUM", "FOODS")
    base.wall_sign(t, 21, 9, 5, "north", "NEIGHBORHOOD", "CULTURE SERVICE", "DEPOT")

    # Public route: vestibule -> account/queue -> culture issue -> exit. Returns
    # split immediately into a separate desk so dirty material never crosses clean issue.
    t.fill((13, 1, 9), (25, 1, 15), "minecraft:white_concrete")
    t.fill((17, 2, 13), (24, 2, 13), "zvhouses:stone_brick_countertop")
    t.fill((17, 3, 14), (24, 3, 14), "minecraft:lime_concrete")
    t.fill((6, 2, 12), (11, 2, 12), "zvhouses:stone_brick_countertop")
    t.fill((10, 2, 13), (11, 4, 15), "minecraft:lime_concrete")
    base.wall_sign(t, 20, 4, 14, "south", "CULTURE ISSUE")
    base.wall_sign(t, 10, 4, 13, "south", "RETURN", "CULTURES")

    # Refrigerated culture-locker hall. Repeated locker banks and staff aisles
    # replace retail gondolas and make culture issue a controlled service operation.
    t.fill((14, 1, 16), (29, 1, 22), "minecraft:light_gray_concrete")
    for x in (15, 19, 23, 27):
        for z in (17, 19, 21):
            t.set(x, 2, z, "oritech:cooler_block")
    t.fill((14, 2, 15), (29, 2, 15), "minecraft:lime_concrete")
    base.wall_sign(t, 21, 3, 15, "north", "COLD LOCKERS", "AUTHORIZED STAFF")

    # Return sanitation and local quality-hold bay. The anomaly is deliberately
    # small: one problem segment in an otherwise operating early-anomaly depot.
    t.fill((4, 2, 15), (12, 7, 15), "create:framed_glass")
    t.fill((12, 2, 15), (12, 7, 22), "create:framed_glass")
    t.fill((4, 2, 22), (12, 7, 22), "create:framed_glass")
    t.clear((5, 3, 16), (11, 6, 21))
    t.fill((5, 1, 16), (11, 1, 21), "minecraft:white_concrete")
    t.fill((5, 2, 20), (10, 2, 20), "create:fluid_pipe")
    t.set(6, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(9, 2, 18, "minecraft:water_cauldron", level="3")
    t.fill((5, 1, 21), (11, 1, 21), "minecraft:yellow_concrete")
    t.fill((10, 2, 20), (11, 3, 21), "immersiveengineering:crate")
    base.wall_sign(t, 7, 4, 15, "north", "SANITATION", "RETURNS ONLY")
    base.wall_sign(t, 11, 4, 18, "east", "QUALITY HOLD", "RETURN BAY 01")

    # Back-of-house route: rear dock -> batch check -> clean stock / returned
    # crate consolidation -> dispatch. Public circulation never enters this zone.
    t.fill((4, 1, 23), (34, 1, 28), "tfmg:factory_floor")
    t.fill((13, 2, 23), (13, 7, 28), "tfmg:cinder_block")
    t.fill((24, 2, 23), (24, 7, 28), "tfmg:cinder_block")
    t.clear((13, 2, 25), (13, 4, 26))
    t.clear((24, 2, 25), (24, 4, 26))
    t.fill((5, 2, 24), (11, 3, 27), "immersiveengineering:crate")
    t.fill((15, 2, 24), (21, 3, 27), "immersiveengineering:crate")
    t.fill((5, 1, 28), (12, 1, 28), "minecraft:lime_concrete")
    t.fill((15, 1, 28), (22, 1, 28), "minecraft:white_concrete")
    t.fill((6, 2, 27), (11, 2, 27), "jaffabricate:pallet_full")
    base.wall_sign(t, 9, 4, 23, "north", "RECEIVING", "BATCH CHECK")
    base.wall_sign(t, 18, 4, 23, "north", "CLEAN STOCK", "RETURN CRATES")

    # Supervisor/batch records occupy the staff-side rear room and overlook the
    # service floor. Deterministic evidence now lives where operational records belong.
    t.fill((25, 2, 23), (34, 7, 23), "tfmg:cinder_block")
    t.clear((29, 2, 23), (30, 4, 23))
    t.fill((27, 2, 25), (32, 2, 25), "zvhouses:stone_brick_countertop")
    t.set(31, 3, 25, "the_wasteland_reworked:radio")
    t.fill((32, 2, 26), (33, 4, 27), "minecraft:bookshelf")
    base.wall_sign(t, 29, 4, 23, "north", "SUPERVISOR", "BATCH RECORDS")
    base.wall_sign(t, 32, 4, 28, "south", "STAFF ONLY", "SERVICE DISPATCH")
    t.chest(29, 2, 26, BY_TARGET["OWS-001"].loot_id, "south")

    # Rooftop plant supports the visible cold chain instead of remaining generic
    # commercial HVAC. Paired equipment groups and service piping align to locker use.
    t.fill((10, 10, 13), (15, 11, 17), "immersiveengineering:sheetmetal_steel")
    t.fill((24, 10, 13), (29, 11, 17), "immersiveengineering:sheetmetal_steel")
    for x in (11, 14, 25, 28):
        t.set(x, 12, 15, "oritech:cooler_block")
    t.fill((16, 10, 15), (23, 10, 15), "create:fluid_pipe")
    return t'''

SIGN_MARKER = '''def gable_roof_x(t: Template, x1: int, x2: int, z1: int, z2: int, base_y: int, gable: str, roof_block: str, ridge: str) -> None:'''
SIGN_HELPER = '''def wall_sign(
    t: Template,
    x: int,
    y: int,
    z: int,
    facing: str,
    *lines: str,
    wood: str = "oak",
    color: str = "black",
) -> None:
    """Place a modern text-bearing wall sign with stable 1.21.1 block-entity NBT.

    Heavy Old World rebuilds use this for institutional identity, wayfinding,
    process labels and collapse overprints. Callers own wording and placement.
    """
    if facing not in {"north", "east", "south", "west"}:
        raise ValueError(f"Unsupported wall-sign facing: {facing}")
    messages = [json.dumps({"text": str(line)}, separators=(",", ":")) for line in lines[:4]]
    messages.extend(['{"text":""}'] * (4 - len(messages)))
    blank = NbtList(TAG_STRING, ['{"text":""}'] * 4)
    t.set(
        x,
        y,
        z,
        f"minecraft:{wood}_wall_sign",
        {
            "id": "minecraft:sign",
            "front_text": {"color": color, "messages": NbtList(TAG_STRING, messages)},
            "back_text": {"color": color, "messages": blank},
        },
        facing=facing,
        waterlogged="false",
    )


'''

OLD_VALIDATOR = '''        for block in spec.required_blocks:
            require(block.encode() in raw, f"{spec.target} lacks required block {block}")'''
NEW_VALIDATOR = '''        for block in spec.required_blocks:
            serialized_block = structure_base.STRUCTURE_BLOCK_REPLACEMENTS.get(block, block)
            require(
                serialized_block.encode() in raw,
                f"{spec.target} lacks required serialized block {serialized_block} (declared {block})",
            )'''


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one authoritative match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    core = CORE.read_text(encoding="utf-8")
    core = replace_exact(core, OLD_SPEC, NEW_SPEC, "OWS-001 spec")
    core = replace_exact(core, OLD_BUILDER, NEW_BUILDER, "OWS-001 builder")
    CORE.write_text(core, encoding="utf-8", newline="\n")

    base = BASE.read_text(encoding="utf-8")
    if "def wall_sign(" in base:
        raise RuntimeError("Reusable wall_sign helper already exists; refusing to stack a second implementation")
    if SIGN_MARKER not in base:
        raise RuntimeError("Could not find stable wall-sign helper insertion point")
    base = base.replace(SIGN_MARKER, SIGN_HELPER + SIGN_MARKER, 1)
    BASE.write_text(base, encoding="utf-8", newline="\n")

    validator = VALIDATOR.read_text(encoding="utf-8")
    if "import generate_wasteland_sites as structure_base\n" not in validator:
        validator = validator.replace("import json\n", "import json\nimport generate_wasteland_sites as structure_base\n", 1)
    validator = replace_exact(validator, OLD_VALIDATOR, NEW_VALIDATOR, "serialized required-block validator")
    VALIDATOR.write_text(validator, encoding="utf-8", newline="\n")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    state["active_status"] = "heavy_rebuild_in_progress"
    passes = state["active_target_passes"]
    passes["donor_audit"] = "complete"
    passes["institutional_identity_contract"] = "complete"
    passes["operational_program"] = "complete"
    passes["architectural_reconstruction"] = "implemented_pending_static_review"
    passes["circulation_and_access"] = "implemented_pending_static_review"
    passes["machinery_and_furnishing"] = "implemented_pending_static_review"
    passes["signage_and_wayfinding"] = "implemented_pending_static_review"
    passes["historical_damage"] = "implemented_pending_static_review"
    passes["narrative_evidence_and_loot"] = "implemented_pending_static_review"
    passes["micro_detail"] = "in_progress"
    passes["static_render_review"] = "pending"
    passes["static_validation"] = "pending"
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print("[SYSTEM REPORT] Patched authoritative OWS-001 heavy rebuild, reusable wall-sign primitive, and serialized-block validator semantics.")


if __name__ == "__main__":
    main()

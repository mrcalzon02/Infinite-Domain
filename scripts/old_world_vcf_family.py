"""Old World VCF narrative descendants built from the accepted wasteland corpus.

These builders deliberately extend the authoritative source templates instead of
copying them. Each site changes at least four narrative dimensions and binds one
site-specific deterministic proof chest.
"""
from __future__ import annotations

from typing import Any, Callable

A: Any = None


def configure(api: Any) -> None:
    global A
    A = api


def _dims(t):
    sx, sy, sz = t.size
    return sx, sy, sz


def _vcf_brand(t, x: int, y: int, z: int, *, axis: str = "x") -> None:
    """Material signage: pale industrial panel, VCF green band, warning tile."""
    if axis == "x":
        t.fill((x, y, z), (x + 6, y + 4, z), "minecraft:light_gray_concrete")
        t.fill((x, y + 3, z), (x + 6, y + 4, z), "minecraft:green_concrete")
        t.fill((x + 1, y + 1, z), (x + 2, y + 2, z), "minecraft:lime_concrete")
        t.fill((x + 4, y + 1, z), (x + 5, y + 2, z), "minecraft:yellow_concrete")
    else:
        t.fill((x, y, z), (x, y + 4, z + 6), "minecraft:light_gray_concrete")
        t.fill((x, y + 3, z), (x, y + 4, z + 6), "minecraft:green_concrete")
        t.fill((x, y + 1, z + 1), (x, y + 2, z + 2), "minecraft:lime_concrete")
        t.fill((x, y + 1, z + 4), (x, y + 2, z + 5), "minecraft:yellow_concrete")


def _culture_bank(t, x: int, y: int, z: int, count: int = 3) -> None:
    for index in range(count):
        cx = x + index * 4
        t.fill((cx, y, z), (cx + 2, y + 4, z + 2), "create:fluid_tank")
        t.set(cx + 1, y + 5, z + 1, "minecraft:green_stained_glass")
        t.set(cx + 1, y, z + 3, "minecraft:brewing_stand")


def _grow_rack(t, x: int, y: int, z: int, length: int = 9) -> None:
    t.fill((x, y, z), (x + length, y, z + 2), "minecraft:moss_block")
    t.fill((x, y + 1, z), (x + length, y + 1, z + 2), "minecraft:mycelium")
    for rx in range(x, x + length + 1, 3):
        t.set(rx, y + 2, z + 1, "minecraft:red_mushroom")
        t.set(min(rx + 1, x + length), y + 2, z + 1, "minecraft:brown_mushroom")


def _evidence(t, x: int, y: int, z: int, table: str, facing: str = "north") -> None:
    t.fill((max(0, x - 1), y, max(0, z - 1)), (x + 1, y, z + 1), "minecraft:smooth_stone")
    t.chest(x, y + 1, z, f"infinite_domain:chests/old_world/vcf/{table}", facing)
    t.set(x + 1, y + 1, z, "minecraft:lectern", facing=facing, has_book="false", powered="false")


def ows_001_culture_service_depot():
    t = A.corporate_warehouse()
    sx, sy, sz = _dims(t)
    # Silhouette: roof culture-service plant and green service canopy.
    t.fill((5, sy - 3, 8), (18, sy - 2, 14), "minecraft:oxidized_copper")
    _culture_bank(t, 7, sy - 7, 9, 3)
    t.fill((2, 5, 0), (20, 6, 3), "minecraft:green_concrete")
    # Interior zoning + machinery: service intake -> culture staging -> dispatch.
    t.fill((6, 2, 8), (6, 7, 26), "minecraft:light_gray_concrete")
    _culture_bank(t, 10, 2, 12, 4)
    _vcf_brand(t, 8, 2, 0)
    # Failure signature: one spoiled culture bank ruptured through floor.
    t.clear((20, 1, 19), (27, 5, 26)); t.fill((20, 1, 19), (27, 1, 26), "minecraft:moss_block")
    _evidence(t, sx - 9, 1, 8, "ows_001_culture_service_manifest", "west")
    return t


def ows_002_emergency_grow_annex():
    t = A.ruined_city_school()
    sx, sy, sz = _dims(t)
    # Silhouette: improvised rooftop emergency greenhouse.
    y = max(4, sy - 6)
    t.fill((4, y, 5), (min(sx - 5, 24), y + 4, min(sz - 5, 20)), "minecraft:green_stained_glass")
    t.clear((5, y + 1, 6), (min(sx - 6, 23), y + 3, min(sz - 6, 19)))
    # Interior zoning + grow equipment: classrooms converted into cultivation bays.
    for z in range(8, min(sz - 8, 32), 8):
        _grow_rack(t, 8, 2, z, min(12, sx - 18))
    _vcf_brand(t, 4, 2, 0)
    # Failure: failed sprinkler/grow bay becomes damp mycelium breach.
    t.fill((sx // 2, 1, sz // 2), (min(sx - 2, sx // 2 + 7), 2, min(sz - 2, sz // 2 + 7)), "minecraft:mycelium")
    _evidence(t, min(sx - 7, 18), 1, min(sz - 7, 14), "ows_002_emergency_grow_authorization")
    return t


def ows_003_culture_batch_warehouse():
    t = A.corporate_warehouse()
    sx, sy, sz = _dims(t)
    # Silhouette/branding: quarantine loading canopy and tall batch exhaust stack.
    t.fill((sx - 18, 4, 0), (sx - 4, 6, 4), "minecraft:green_concrete")
    t.fill((sx - 8, 6, 8), (sx - 5, sy - 1, 11), "minecraft:oxidized_copper")
    _vcf_brand(t, sx - 16, 2, 0)
    # Zoning: numbered batch cages separated from ordinary warehouse racks.
    for z in (11, 19, 27):
        t.fill((8, 2, z), (25, 5, z), "minecraft:oxidized_copper_grate")
        _culture_bank(t, 10, 2, min(sz - 6, z + 1), 3)
    # Failure: batch quarantine spill, deliberately localized rather than generic ruin.
    t.fill((27, 1, 25), (35, 2, 33), "minecraft:mycelium")
    t.fill((30, 3, 27), (33, 5, 30), "minecraft:green_stained_glass")
    _evidence(t, 13, 1, sz - 8, "ows_003_vcf_culture_batch_record", "south")
    return t


def ows_004_mycological_vertical_farm_tower():
    t = A.toppled_skyscraper()
    sx, sy, sz = _dims(t)
    # Silhouette: surviving farm crown, external service spine, greenhouse glazing.
    crown_y = max(5, sy - 8)
    t.fill((4, crown_y, 4), (min(sx - 5, 18), sy - 2, min(sz - 5, 18)), "minecraft:green_stained_glass")
    t.fill((2, 2, 5), (4, sy - 3, 8), "minecraft:oxidized_copper")
    # Interior: repeated cultivation floors, not generic office debris.
    for y in range(3, max(4, sy - 10), 5):
        _grow_rack(t, min(7, sx - 12), y, min(8, sz - 6), min(10, sx - 12))
        _culture_bank(t, max(2, sx - 16), y, max(2, sz - 9), 2)
    _vcf_brand(t, min(sx - 8, 8), 2, 0)
    # Failure: collapsed irrigation core with fungal runoff.
    t.fill((sx // 2 - 3, 1, sz // 2 - 3), (sx // 2 + 4, 2, sz // 2 + 4), "minecraft:mycelium")
    _evidence(t, min(sx - 6, 12), 2, min(sz - 6, 12), "ows_004_evercrop_cultivation_handbook")
    return t


def ows_005_packaging_quality_plant():
    t = A.abandoned_orchard_cannery()
    sx, sy, sz = _dims(t)
    # Silhouette: VCF QA annex and cold-chain loading hood.
    t.fill((sx - 18, 2, 3), (sx - 4, 9, 12), "minecraft:light_gray_concrete")
    t.clear((sx - 17, 3, 4), (sx - 5, 8, 11))
    t.fill((sx - 17, 5, 3), (sx - 5, 7, 3), "minecraft:green_stained_glass")
    _vcf_brand(t, sx - 15, 3, 3)
    # Process zoning: inspection bench + retained samples + rejected product lane.
    _culture_bank(t, sx - 15, 3, 6, 2)
    t.fill((8, 2, sz - 12), (24, 4, sz - 8), "jaffabricate:pallet_full")
    t.fill((26, 1, sz - 14), (35, 2, sz - 6), "minecraft:mycelium")
    # Damage signature: packaging-line contamination concentrated around rejected lane.
    t.fill((30, 3, sz - 12), (34, 5, sz - 8), "minecraft:brown_mushroom_block")
    _evidence(t, sx - 10, 2, 8, "ows_005_vcf_packaging_quality_report", "west")
    return t


def ows_006_pt9_symbiosis_pilot_lab():
    t = A.mountain_biohazard_lab()
    sx, sy, sz = _dims(t)
    # Silhouette: paired PT-9 culture towers and dedicated intake canopy.
    _culture_bank(t, 5, max(2, sy - 8), 7, 3)
    t.fill((3, 4, 0), (20, 6, 4), "minecraft:green_concrete")
    _vcf_brand(t, 7, 2, 0)
    # Interior zoning: fungus/bacteria rooms separated by a symbiosis observation cell.
    cx, cz = sx // 2, sz // 2
    t.fill((cx - 9, 2, cz - 6), (cx - 9, 8, cz + 7), "minecraft:light_gray_concrete")
    t.fill((cx + 9, 2, cz - 6), (cx + 9, 8, cz + 7), "minecraft:light_gray_concrete")
    t.fill((cx - 5, 2, cz - 4), (cx + 5, 7, cz + 4), "minecraft:green_stained_glass")
    t.clear((cx - 4, 3, cz - 3), (cx + 4, 6, cz + 3))
    _grow_rack(t, cx - 4, 2, cz - 2, 8)
    _culture_bank(t, max(2, cx - 7), 2, min(sz - 6, cz + 6), 3)
    # Signature failure: observation-cell seal breaks into both previously isolated labs.
    t.clear((cx - 9, 3, cz), (cx + 9, 5, cz + 2))
    t.fill((cx - 6, 1, cz - 1), (cx + 7, 2, cz + 5), "minecraft:mycelium")
    _evidence(t, min(sx - 8, cx + 12), 2, max(5, cz - 10), "ows_006_pt9_symbiosis_report", "west")
    return t


def ows_007_ep7_agricultural_development_lab():
    t = A.nuclear_research_annex()
    sx, sy, sz = _dims(t)
    # Silhouette: agricultural test greenhouse grafted onto heavy research annex.
    t.fill((sx - 24, 3, 4), (sx - 5, 11, 18), "minecraft:green_stained_glass")
    t.clear((sx - 23, 4, 5), (sx - 6, 10, 17))
    t.fill((sx - 25, 2, 3), (sx - 4, 3, 19), "minecraft:oxidized_copper")
    _vcf_brand(t, sx - 16, 4, 3)
    # Interior/material workflow: seed exposure -> growth -> durability test -> archive.
    _grow_rack(t, sx - 21, 4, 7, 12)
    _culture_bank(t, 8, 2, sz - 16, 4)
    t.fill((25, 2, sz - 14), (39, 5, sz - 8), "minecraft:scaffolding")
    # Signature failure: exterior distribution/loading breach demonstrates perimeter escape.
    t.clear((sx - 3, 2, sz // 2 - 5), (sx - 1, 7, sz // 2 + 5))
    t.fill((sx - 10, 1, sz // 2 - 6), (sx - 1, 2, sz // 2 + 7), "minecraft:mycelium")
    _evidence(t, sx - 12, 3, 12, "ows_007_ep7_distribution_and_durability_record", "west")
    return t


def ows_008_persistence_incident_lab():
    t = A.mountain_biohazard_lab()
    sx, sy, sz = _dims(t)
    # Silhouette: emergency isolation shell wrapped around the original VCF research block.
    t.fill((2, 2, 2), (sx - 3, 3, 2), "minecraft:yellow_concrete")
    t.fill((2, 2, sz - 3), (sx - 3, 3, sz - 3), "minecraft:yellow_concrete")
    t.fill((2, 2, 2), (2, 3, sz - 3), "minecraft:yellow_concrete")
    t.fill((sx - 3, 2, 2), (sx - 3, 3, sz - 3), "minecraft:yellow_concrete")
    _vcf_brand(t, 6, 2, 0)
    # Interior zoning: sealed incident archive + dead-end decon corridor + persistence samples.
    cx, cz = sx // 2, sz // 2
    t.fill((cx - 7, 2, 6), (cx + 7, 9, 15), "immersiveengineering:concrete_leaded")
    t.clear((cx - 6, 3, 7), (cx + 6, 8, 14))
    _culture_bank(t, cx - 5, 3, 9, 3)
    # Signature failure: growth crosses isolation shell at multiple material interfaces.
    for x, z in ((3, cz), (sx - 5, cz + 4), (cx, 3), (cx + 5, sz - 5)):
        t.fill((max(1, x - 2), 1, max(1, z - 2)), (min(sx - 2, x + 3), 3, min(sz - 2, z + 3)), "minecraft:mycelium")
        t.set(x, 4, z, "minecraft:brown_mushroom_block")
    _evidence(t, cx, 3, 11, "ows_008_vcf_persistence_incident_file", "south")
    return t


BUILDERS: dict[str, Callable[[], Any]] = {
    "ows_001_culture_service_depot": ows_001_culture_service_depot,
    "ows_002_emergency_grow_annex": ows_002_emergency_grow_annex,
    "ows_003_culture_batch_warehouse": ows_003_culture_batch_warehouse,
    "ows_004_mycological_vertical_farm_tower": ows_004_mycological_vertical_farm_tower,
    "ows_005_packaging_quality_plant": ows_005_packaging_quality_plant,
    "ows_006_pt9_symbiosis_pilot_lab": ows_006_pt9_symbiosis_pilot_lab,
    "ows_007_ep7_agricultural_development_lab": ows_007_ep7_agricultural_development_lab,
    "ows_008_persistence_incident_lab": ows_008_persistence_incident_lab,
}

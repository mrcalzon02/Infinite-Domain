#!/usr/bin/env python3
"""[SYSTEM REPORT] Static integrity gate for Infinite Domain abyssal deformation.

This does not claim runtime terrain quality. It proves that the authored abyssal
noise/deformation graph is present and remains connected to the active Wastelands
terrain router and intended abyssal biome carvers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "datapacks/gradient_ocean_pack/data"
CUSTOM = PACK / "custom_worldgen/worldgen"
DF = CUSTOM / "density_function"
NOISE = CUSTOM / "noise"
CARVERS = CUSTOM / "configured_carver"
BIOMES = ROOT / "kubejs/data/infinite_domain/worldgen/biome"
NOISE_SETTINGS = ROOT / "kubejs/data/wastelands/worldgen/noise_settings/wasteland.json"
MC_CONTINENTS = PACK / "minecraft/worldgen/density_function/overworld/continents.json"


def fail(message: str) -> None:
    print(f"[ABYSSAL DEFORMATION FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def serialized(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def require_refs(path: Path, refs: list[str]) -> None:
    text = serialized(load(path))
    missing = [ref for ref in refs if ref not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} no longer references: {', '.join(missing)}")


# 1. Every reference-image noise vocabulary member must exist.
for name in ("abyssal_cells", "abyssal_faults", "abyssal_roughness", "abyssal_vents"):
    load(NOISE / f"{name}.json")

base_patterns = (
    "abyssal_cellular_basin_pattern",
    "abyssal_coarse_fracture_pattern",
    "abyssal_diffuse_roughness_pattern",
    "abyssal_mottled_collapse_pattern",
    "abyssal_vent_caldera_pattern",
    "abyssal_fine_fracture_pattern",
)
derived_vertical = (
    "abyssal_shelf_slump_pattern",
    "abyssal_exposed_cliff_pattern",
    "abyssal_trench_scarp_pattern",
    "abyssal_vent_rim_pattern",
)
for name in (*base_patterns, *derived_vertical):
    load(DF / f"{name}.json")

# 2. Vertical helper masks must remain derived from the intended depth boundaries.
require_refs(
    DF / "abyssal_slope_edge_mask.json",
    ["custom_worldgen:abyssal_slope_band_mask"],
)
require_refs(
    DF / "hadal_edge_mask.json",
    ["custom_worldgen:hadal_trench_mask"],
)
require_refs(
    DF / "abyssal_shelf_slump_pattern.json",
    [
        "custom_worldgen:abyssal_slope_edge_mask",
        "custom_worldgen:abyssal_mottled_collapse_pattern",
    ],
)
require_refs(
    DF / "abyssal_exposed_cliff_pattern.json",
    [
        "custom_worldgen:abyssal_slope_band_mask",
        "custom_worldgen:abyssal_coarse_fracture_pattern",
        "custom_worldgen:abyssal_fine_fracture_pattern",
    ],
)
require_refs(
    DF / "abyssal_trench_scarp_pattern.json",
    [
        "custom_worldgen:hadal_edge_mask",
        "custom_worldgen:abyssal_coarse_fracture_pattern",
        "custom_worldgen:abyssal_fine_fracture_pattern",
    ],
)
require_refs(
    DF / "abyssal_vent_rim_pattern.json",
    ["custom_worldgen:abyssal_vent_caldera_pattern"],
)

# 3. All six reference motifs and all four derived vertical processes must actually
# feed the shared depression mix, with their band masks.
require_refs(
    DF / "abyssal_pattern_depression.json",
    [
        *(f"custom_worldgen:{name}" for name in base_patterns),
        *(f"custom_worldgen:{name}" for name in derived_vertical),
        "custom_worldgen:abyssal_slope_band_mask",
        "custom_worldgen:abyssal_plain_mask",
        "custom_worldgen:hadal_trench_mask",
    ],
)

# 4. Regional deformation must remain East/West + ocean-corridor gated.
require_refs(
    DF / "western_depth_depression.json",
    [
        "custom_worldgen:western_abyss_selector",
        "custom_worldgen:east_west_ocean_corridor_mask",
        "custom_worldgen:abyssal_pattern_depression",
    ],
)
require_refs(
    DF / "eastern_depth_depression.json",
    [
        "custom_worldgen:eastern_abyss_selector",
        "custom_worldgen:east_west_ocean_corridor_mask",
        "custom_worldgen:abyssal_pattern_depression",
    ],
)

# 5. The regional depressions must feed the outer continents branch, which must
# remain protected by the central-continent branch in custom_worldgen:continents.
require_refs(
    DF / "abyssal_outer_continents.json",
    ["custom_worldgen:western_depth_depression", "custom_worldgen:eastern_depth_depression"],
)
require_refs(
    DF / "continents.json",
    ["custom_worldgen:abyssal_outer_continents", "custom_worldgen:central_continent_mask"],
)

# 6. Critical terrain bridge: vanilla overworld terrain density functions such as
# sloped_cheese resolve minecraft:overworld/continents. This datapack override
# must delegate that registry key to custom_worldgen:continents.
mc_continents = load(MC_CONTINENTS)
if mc_continents.get("type") != "minecraft:cache_2d" or mc_continents.get("argument") != "custom_worldgen:continents":
    fail("minecraft:overworld/continents no longer delegates to custom_worldgen:continents")

# 7. The active Wastelands climate router must consume the same continents signal.
settings = load(NOISE_SETTINGS)
router = settings.get("noise_router", {})
if router.get("continents") != "custom_worldgen:continents":
    fail("Wastelands noise_router.continents is not custom_worldgen:continents")
if "minecraft:overworld/sloped_cheese" not in serialized(router.get("final_density")):
    fail("Wastelands final_density no longer uses the overworld terrain density chain")

# 8. Purpose-built cave carvers must exist and remain restricted to intended bands.
load(CARVERS / "abyssal_slope_cave.json")
load(CARVERS / "abyssal_fracture_cave.json")

slope_biomes = ("western_continental_slope", "eastern_continental_slope")
fracture_biomes = ("western_fracture_field", "eastern_fracture_field")
hadal_biomes = ("western_hadal_trench", "eastern_hadal_trench")
plain_biomes = ("western_abyssal_plain", "eastern_abyssal_plain")

for name in slope_biomes:
    biome = load(BIOMES / f"{name}.json")
    carvers = biome.get("carvers", {}).get("air", [])
    if "custom_worldgen:abyssal_slope_cave" not in carvers:
        fail(f"{name} lost custom_worldgen:abyssal_slope_cave")
    if "custom_worldgen:abyssal_fracture_cave" in carvers:
        fail(f"{name} incorrectly contains fracture cave carver")

for name in (*fracture_biomes, *hadal_biomes):
    biome = load(BIOMES / f"{name}.json")
    carvers = biome.get("carvers", {}).get("air", [])
    if "custom_worldgen:abyssal_fracture_cave" not in carvers:
        fail(f"{name} lost custom_worldgen:abyssal_fracture_cave")
    if "custom_worldgen:abyssal_slope_cave" in carvers:
        fail(f"{name} incorrectly contains slope cave carver")

for name in plain_biomes:
    biome = load(BIOMES / f"{name}.json")
    carvers = biome.get("carvers", {}).get("air", [])
    forbidden = {"custom_worldgen:abyssal_slope_cave", "custom_worldgen:abyssal_fracture_cave"}
    leaked = forbidden.intersection(carvers)
    if leaked:
        fail(f"{name} unexpectedly contains band-specific carver(s): {sorted(leaked)}")

print(
    "[ABYSSAL DEFORMATION PASS] six reference motifs, four derived vertical processes, "
    "terrain bridge, regional gates, and cave-band attachments are intact"
)

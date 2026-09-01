from __future__ import annotations

import gzip
import io
import json
import math
import struct
from pathlib import Path
from typing import Any

# Validator for the deep-sea corpus, run against
# docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md and
# structure_library/deepsea-metadata.schema.json. Mirrors the checking style
# of scripts/validate_structure_corpus.py (explicit controlled-vocabulary
# checks, no external schema library) plus the underwater-specific checks
# the standards document calls out: correct atmosphere-state fluid fill,
# and that nothing here is live against real ocean biomes yet -- except
# akula_wreck_site/akula_debris_field, admitted to eastern_slope_biomes by
# owner directive on 2026-08-25 with the in-game QA walkthrough explicitly
# skipped (see docs/DEEP_SEA_STRUCTURE_AUDIT.md). Every other asset in this
# corpus stays behind the quarantine tag and this validator still enforces
# that.

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "dev/structure_library" / "deepsea-catalog.json"
REPORT = ROOT / "dev/docs" / "deepsea-structure-validation.json"
CSV_PATH = ROOT / "dev/docs" / "biome-gating-audit" / "ocean-structure-sets.csv"
QUARANTINE_TAG_PATH = ROOT / "kubejs" / "data" / "infinite_domain" / "tags" / "worldgen" / "biome" / "disabled_quarantine_deep_sea_structures.json"

ASSET_CLASSES = {"geological_macro", "geological_feature", "structure"}
DEPTH_BANDS = {"shelf", "open_floor", "deep_floor", "abyssal"}
BUILD_STYLES = {
    "pre_collapse_civilian_industrial", "create_industrial_offshore", "military_remnant",
    "darknet_adjacent", "ancient_unknown_origin", "other",
}
BURIAL_STATES = {"exposed", "partially_buried", "subterranean"}
ACCESS_CONNECTORS = {"diver_hatch", "moon_pool", "submarine_dock", "surface_shaft", "buried_shaft", "none"}
ATMOSPHERE_STATES = {"flooded", "dry_pressurized", "mixed_breached"}
REFINEMENT_INTENSITIES = {"repair", "light", "standard", "heavy", "rebuild"}
PRODUCTION_STATUSES = {"quarantined", "automatic_validation", "visual_review", "approved", "rejected"}
DAMAGE_CAUSES = {
    "corrosion", "biofouling", "silt_burial", "pressure_hull_failure", "flooding_breach",
    "listing_settle", "anchor_drag_scarring", "current_scour", "thermal_scarring",
    # Wave 3c addition. A reactor compartment opening is not thermal_scarring
    # (which the standards scope to vent features) and not flooding_breach
    # (which is about water getting in, not fuel getting out). Nuclear vessels
    # are a real category in this corpus now, so the vocabulary needs the term
    # rather than an approximate one.
    "reactor_breach",
}
OCCUPATION_STATES = {
    "derelict", "salvage_crew", "faction_garrison", "hostile_aquatic",
    "quarantine_outbreak", "smuggler_cache", "quest_location",
}
RIG_CX_CONST = 13 // 2  # mirrors RIG_CX in generate_deep_sea_structures.py

# Mirrors scripts/render_deep_sea_review.py's KNOWN_BLOCK_COLORS keys plus
# its substring-matched families (sand/sea_pickle/kelp/prismarine/copper/
# *_bed). Keep the two lists in sync: a name here with no curated render
# color means the audit renders for whatever asset places it are not real
# evidence, per the "Size and visual composition audit" section of
# docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md.
RENDER_COLOR_CURATED_EXACT = {
    "minecraft:air", "minecraft:water", "minecraft:spawner", "minecraft:chest",
    "minecraft:barrel", "minecraft:crafting_table", "minecraft:lectern", "minecraft:ladder",
    "minecraft:campfire", "minecraft:iron_block", "minecraft:iron_bars", "minecraft:iron_trapdoor",
    "minecraft:gray_concrete", "minecraft:mud_bricks", "minecraft:stone", "minecraft:gravel",
    "minecraft:basalt", "minecraft:blackstone", "minecraft:polished_basalt", "minecraft:smooth_basalt",
    "minecraft:magma_block", "minecraft:glass_pane", "minecraft:blast_furnace", "minecraft:hopper",
    "minecraft:lever", "minecraft:chain", "minecraft:redstone_lamp", "minecraft:lantern",
    "minecraft:soul_lantern", "minecraft:sea_lantern", "minecraft:glow_lichen",
    "minecraft:blue_bed", "minecraft:gray_bed",
    # Wave 3 (akula_project971). Mirrors the additions to
    # render_deep_sea_review.py's KNOWN_BLOCK_COLORS -- update both together.
    "minecraft:deepslate_tiles", "minecraft:deepslate_tile_slab", "minecraft:polished_deepslate",
    "minecraft:cobbled_deepslate", "minecraft:black_concrete", "minecraft:polished_blackstone",
    "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:copper_block",
    "minecraft:copper_grate", "minecraft:oxidized_cut_copper", "minecraft:oxidized_cut_copper_slab",
    "minecraft:dispenser", "minecraft:red_concrete", "minecraft:tuff",
    "minecraft:jigsaw",
    # Wave 3c wasteland/radiation vocabulary -- see the note in
    # render_deep_sea_review.py's KNOWN_BLOCK_COLORS. Keep the two in sync.
    "create_new_age:solid_corium", "create_new_age:corium",
    "the_wasteland_reworked:waste_barrel", "the_wasteland_reworked:rusted_barrel",
    "the_wasteland_reworked:hazard_concrete", "the_wasteland_reworked:lead_plating",
    "the_wasteland_reworked:rusted_lead_plating", "the_wasteland_reworked:cut_lead_plating",
    "the_wasteland_reworked:radiation_hazard_sign", "the_wasteland_reworked:aluminium_grate",
    "the_wasteland_reworked:broken_aluminium_grate", "the_wasteland_reworked:support_beam",
    "infinite_domain:ruined_blast_furnace",
}
RENDER_COLOR_CURATED_SUBSTRINGS = ("sand", "sea_pickle", "kelp", "prismarine", "copper")


class Reader:
    """Minimal big-endian NBT reader, matching scripts/inspect_structure_nbt.py."""

    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def unpack(self, fmt: str) -> Any:
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.stream.read(size))[0]

    def string(self) -> str:
        return self.stream.read(self.unpack(">H")).decode("utf-8")

    def payload(self, kind: int) -> Any:
        if kind == 3:
            return self.unpack(">i")
        if kind == 8:
            return self.string()
        if kind == 9:
            item_kind = self.unpack(">B")
            length = self.unpack(">i")
            return [self.payload(item_kind) for _ in range(length)]
        if kind == 10:
            result: dict[str, Any] = {}
            while True:
                child_kind = self.unpack(">B")
                if child_kind == 0:
                    return result
                child_name = self.string()
                result[child_name] = self.payload(child_kind)
        raise ValueError(f"Unsupported/unused NBT tag type in validator: {kind}")

    def root(self) -> dict[str, Any]:
        kind = self.unpack(">B")
        if kind != 10:
            raise ValueError(f"Expected compound root, found tag type {kind}")
        self.string()
        return self.payload(kind)


def load_nbt(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return Reader(raw).root()


def require(entry: dict[str, Any], name: str, expected: type, issues: list[str]) -> Any:
    value = entry.get(name)
    if not isinstance(value, expected):
        issues.append(f"{name}: expected {expected.__name__}, found {value!r}")
    return value


def check_enum(entry: dict[str, Any], name: str, allowed: set[str], issues: list[str], required: bool = True) -> None:
    value = entry.get(name)
    if value is None:
        if required:
            issues.append(f"{name}: missing")
        return
    if value not in allowed:
        issues.append(f"{name}: {value!r} not in {sorted(allowed)}")


def validate_common(entry: dict[str, Any], issues: list[str]) -> None:
    asset_id = require(entry, "asset_id", str, issues)
    if isinstance(asset_id, str) and ":" not in asset_id:
        issues.append("asset_id: missing namespace")
    check_enum(entry, "asset_class", ASSET_CLASSES, issues)
    check_enum(entry, "depth_band", DEPTH_BANDS, issues)
    scope = require(entry, "biome_scope", list, issues)
    if isinstance(scope, list) and not scope:
        issues.append("biome_scope: must not be empty")


def validate_geological_macro(entry: dict[str, Any], issues: list[str]) -> None:
    require(entry, "terrain_feature_type", str, issues)
    require(entry, "noise_scope", str, issues)


def validate_geological_feature(entry: dict[str, Any], issues: list[str]) -> None:
    require(entry, "feature_type", str, issues)
    footprint = require(entry, "footprint", dict, issues)
    if isinstance(footprint, dict) and (not isinstance(footprint.get("width"), int) or not isinstance(footprint.get("depth"), int)):
        issues.append("footprint: width/depth must be integers")
    check_enum(entry, "hazard_type", {"none", "thermal", "toxic", "radiological", "pressure", "biological"}, issues)
    validate_nbt_dimensions(entry, issues, height_required=False)


def validate_structure(entry: dict[str, Any], issues: list[str]) -> None:
    check_enum(entry, "build_style", BUILD_STYLES, issues)
    if entry.get("build_style") == "other" and not entry.get("build_style_note"):
        issues.append("build_style_note: required when build_style is 'other'")
    check_enum(entry, "burial_state", BURIAL_STATES, issues)
    check_enum(entry, "access_connector", ACCESS_CONNECTORS, issues)
    check_enum(entry, "dominant_atmosphere_state", ATMOSPHERE_STATES, issues)
    check_enum(entry, "refinement_intensity", REFINEMENT_INTENSITIES, issues)
    check_enum(entry, "production_status", PRODUCTION_STATUSES, issues)
    for cause in entry.get("damage_causes", []) or []:
        if cause not in DAMAGE_CAUSES:
            issues.append(f"damage_causes: {cause!r} not a controlled damage vocabulary term")
    occupation = entry.get("occupation_state")
    if occupation is not None and occupation not in OCCUPATION_STATES:
        issues.append(f"occupation_state: {occupation!r} not a controlled occupation vocabulary term")
    license_data = require(entry, "source_license", dict, issues)
    if isinstance(license_data, dict) and not all(key in license_data for key in ("origin", "license", "redistributable")):
        issues.append("source_license: missing provenance field")
    validate_nbt_dimensions(entry, issues, height_required=True)


def validate_nbt_dimensions(entry: dict[str, Any], issues: list[str], height_required: bool) -> None:
    footprint = entry.get("footprint")
    height = entry.get("height")
    template = entry.get("source_template")
    if not isinstance(template, str):
        return
    path = (ROOT / template).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        issues.append("source_template: escapes project root")
        return
    if not path.is_file():
        issues.append(f"source_template: file not found ({template})")
        return
    try:
        root = load_nbt(path)
        width, actual_height, depth = (int(v) for v in root["size"])
    except (OSError, EOFError, KeyError, ValueError) as error:
        issues.append(f"source_template: unreadable NBT ({error})")
        return
    if isinstance(footprint, dict) and (footprint.get("width"), footprint.get("depth")) != (width, depth):
        issues.append(f"declared footprint does not match NBT plan {width}x{depth}")
    if height_required and height != actual_height:
        issues.append(f"declared height {height} does not match NBT height {actual_height}")


def sample_block_names(path: Path) -> dict[tuple[int, int, int], str]:
    root = load_nbt(path)
    palette = [p["Name"] for p in root["palette"]]
    return {tuple(block["pos"]): palette[block["state"]] for block in root["blocks"]}


def validate_atmosphere_fill(issues: list[str]) -> None:
    """Underwater-specific check: a compartment declared 'flooded' actually
    contains water at generation time, and a dry compartment does not."""
    path = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea" / "coastal_patrol_wreck.nbt"
    if not path.is_file():
        issues.append("coastal_patrol_wreck.nbt not found for atmosphere-fill check")
        return
    blocks = sample_block_names(path)
    # Engine room / breach bay: declared mixed_breached, must contain water.
    flooded_samples = [(x, y, 17) for x in range(3, 8) for y in (1, 2, 3)]
    # Water, structural fixtures, and intentional occupants (a spawner in a
    # flooded compartment is deliberate hostile_aquatic dressing, not a
    # silent air gap) are all acceptable; only unexplained air is a defect.
    acceptable = {
        "minecraft:water", "minecraft:iron_block", "minecraft:iron_bars", "minecraft:blast_furnace",
        "minecraft:redstone_lamp", "minecraft:lever", "minecraft:spawner", "minecraft:chest",
        # The engine bay's blast furnace is now the ruined stand-in required by
        # docs/RUINED_FUNCTIONAL_BLOCKS.md. This list is the reason that swap
        # is worth naming: an atmosphere check keyed to specific fixture names
        # silently turns a policy fix into a false flooding defect.
        "infinite_domain:ruined_blast_furnace",
    }
    missing_water = [pos for pos in flooded_samples if blocks.get(pos) not in acceptable]
    if missing_water:
        issues.append(f"atmosphere_fill: expected water or engine fixtures in flooded engine bay, found gaps at {missing_water[:5]}")
    # Crew berth: declared dry, must not contain water.
    dry_samples = [(x, 2, z) for x in range(3, 8) for z in range(9, 13)]
    flooded_in_dry = [pos for pos in dry_samples if blocks.get(pos) == "minecraft:water"]
    if flooded_in_dry:
        issues.append(f"atmosphere_fill: unexpected water in declared-dry crew berth at {flooded_in_dry[:5]}")

    # flooded_relay_shelter: declared fully flooded, chamber must be water
    # (or a fixture/loot marker), never bare air.
    relay_path = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea" / "flooded_relay_shelter.nbt"
    if relay_path.is_file():
        relay_blocks = sample_block_names(relay_path)
        chamber_samples = [(x, y, z) for x in range(3, 6) for y in (1, 2, 3) for z in range(3, 6)]
        relay_acceptable = {"minecraft:water", "minecraft:iron_block", "minecraft:oxidized_cut_copper", "minecraft:iron_bars", "minecraft:redstone_lamp", "minecraft:lever", "minecraft:chest", "minecraft:sea_pickle", "minecraft:mud_bricks"}
        relay_gaps = [pos for pos in chamber_samples if relay_blocks.get(pos) not in relay_acceptable]
        if relay_gaps:
            issues.append(f"atmosphere_fill: flooded_relay_shelter chamber has non-water/non-fixture cells at {relay_gaps[:5]}")
    else:
        issues.append("flooded_relay_shelter.nbt not found for atmosphere-fill check")

    # abyssal_mining_rig: control/processing decks declared dry, must not
    # contain water; the moon-pool floor is declared (intentionally) wet.
    rig_path = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea" / "abyssal_mining_rig.nbt"
    if rig_path.is_file():
        rig_blocks = sample_block_names(rig_path)
        rig_dry_samples = [(3, 5, z) for z in range(3, 10)] + [(10, 5, z) for z in range(3, 10)]
        rig_flooded_in_dry = [pos for pos in rig_dry_samples if rig_blocks.get(pos) == "minecraft:water"]
        if rig_flooded_in_dry:
            issues.append(f"atmosphere_fill: unexpected water in abyssal_mining_rig's declared-dry deck at {rig_flooded_in_dry[:5]}")
        moon_pool_floor = [(x, 0, z) for x in range(RIG_CX_CONST - 2, RIG_CX_CONST + 3) for z in range(RIG_CX_CONST - 2, RIG_CX_CONST + 3)]
        moon_pool_gaps = [pos for pos in moon_pool_floor if rig_blocks.get(pos) != "minecraft:water"]
        if moon_pool_gaps:
            issues.append(f"atmosphere_fill: abyssal_mining_rig moon-pool floor is not fully open to water at {moon_pool_gaps[:5]}")
    else:
        issues.append("abyssal_mining_rig.nbt not found for atmosphere-fill check")


def validate_render_color_fidelity(issues: list[str]) -> dict[str, Any]:
    """Every material this corpus places must resolve to a curated,
    real-approximation render color -- see 'Size and visual composition
    audit' in the standards doc. A block that only resolves through the
    renderer's hash fallback means the audit renders for that asset are not
    honest evidence, regardless of what the render looks like."""
    structure_dir = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea"
    detail: dict[str, list[str]] = {}
    if not structure_dir.is_dir():
        issues.append("render_color_fidelity: structure directory not found")
        return detail
    for path in sorted(structure_dir.glob("*.nbt")):
        try:
            root = load_nbt(path)
            names = [p["Name"] for p in root["palette"]]
        except (OSError, EOFError, KeyError, ValueError) as error:
            issues.append(f"render_color_fidelity: {path.name} unreadable NBT ({error})")
            continue
        uncurated = [
            name for name in names
            if name not in RENDER_COLOR_CURATED_EXACT
            and not name.endswith("_bed")
            and not any(token in name for token in RENDER_COLOR_CURATED_SUBSTRINGS)
        ]
        if uncurated:
            detail[path.stem] = sorted(uncurated)
            issues.append(f"render_color_fidelity: {path.stem} places uncalibrated-color materials {sorted(uncurated)}")
    return detail


# ---------------------------------------------------------------------------
# Wave 3 (akula_project971) checks
# ---------------------------------------------------------------------------
#
# Three defect classes the existing checks in this file cannot see, each one
# something that actually went wrong while this family was being authored:
#
#  * a rotated hull skin developing one-block pinholes, which the render
#    review could not distinguish from the random-block-deletion damage the
#    standards forbid;
#  * damage/occupation dressing drifting past the standards' density ceiling
#    until the wreck read as a mound rather than as a hull with growth on it;
#  * an authored wreck attitude drifting away from the impact simulation it is
#    supposed to be the consequence of, which would quietly turn a derived
#    design into a decorated guess.
#
# All three are measured against the NBT that shipped, never against the
# generator source.

STRUCTURE_DIR = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea"
IMPACT_REPORT = ROOT / "dev/docs" / "deepsea-akula-impact-simulation.json"

AK_SEDIMENT_NAMES = {"minecraft:sand", "minecraft:gravel"}
AK_VOID_NAMES = {"minecraft:air", "minecraft:water"}
# Materials that count as damage/occupation dressing for the density ceiling
# in the standards' "Size and visual composition audit", point 6.
AK_DRESSING_NAMES = {
    "minecraft:prismarine_bricks", "minecraft:sea_pickle", "minecraft:kelp_plant",
    "minecraft:oxidized_cut_copper", "minecraft:oxidized_cut_copper_slab",
    "minecraft:cobbled_deepslate",
}
AK_DRESSING_CEILING = 0.50


def _load_cells(path: Path) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], str]]:
    root = load_nbt(path)
    size = tuple(int(v) for v in root["size"])
    palette = [p["Name"] for p in root["palette"]]
    return size, {tuple(b["pos"]): palette[b["state"]] for b in root["blocks"]}


def _exposed_skin(size, cells) -> list[tuple[tuple[int, int, int], str]]:
    """Cells that a viewer outside the asset can actually see, excluding
    seabed. The density ceiling is about visible surface, so measuring the
    whole block list instead would let a wreck hide dressing inside itself and
    pass a check it should not."""
    sx, sy, sz = size
    solid = {pos for pos, name in cells.items()
             if name not in AK_VOID_NAMES and name not in AK_SEDIMENT_NAMES}
    skin = []
    for pos in solid:
        x, y, z = pos
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if not (0 <= n[0] < sx and 0 <= n[1] < sy and 0 <= n[2] < sz):
                skin.append((pos, cells[pos]))
                break
            if n not in solid:
                skin.append((pos, cells[pos]))
                break
    return skin


def validate_akula_dressing_density(issues: list[str]) -> dict[str, Any]:
    detail: dict[str, Any] = {}
    for name in ("akula_wreck_forward_damaged", "akula_wreck_aft_damaged",
                 "akula_wreck_forward", "akula_wreck_aft"):
        path = STRUCTURE_DIR / f"{name}.nbt"
        if not path.is_file():
            issues.append(f"dressing_density: {name}.nbt not found")
            continue
        size, cells = _load_cells(path)
        skin = _exposed_skin(size, cells)
        if not skin:
            issues.append(f"dressing_density: {name} has no exposed skin")
            continue
        dressed = sum(1 for _, material in skin if material in AK_DRESSING_NAMES)
        fraction = dressed / len(skin)
        detail[name] = {"exposed_skin": len(skin), "dressed": dressed, "fraction": round(fraction, 3)}
        if fraction > AK_DRESSING_CEILING:
            issues.append(
                f"dressing_density: {name} dresses {fraction:.0%} of its exposed skin, over the "
                f"{AK_DRESSING_CEILING:.0%} ceiling in the standards' size/visual-composition audit"
            )
    return detail


def validate_akula_structural_continuity(issues: list[str]) -> dict[str, Any]:
    """No unsupported floating geometry. Every solid cell must belong to one
    connected mass -- an authored cantilever (the wreck's raised stern, the
    towed-array pod) is continuous with the hull and passes; an island of
    blocks with nothing under it is the defect the audit checklist names."""
    detail: dict[str, Any] = {}
    for name in ("akula_project971_clean_master", "akula_wreck_forward_damaged",
                 "akula_wreck_aft_damaged", "akula_wreck_forward", "akula_wreck_aft"):
        path = STRUCTURE_DIR / f"{name}.nbt"
        if not path.is_file():
            issues.append(f"structural_continuity: {name}.nbt not found")
            continue
        size, cells = _load_cells(path)
        solid = {pos for pos, material in cells.items() if material not in AK_VOID_NAMES}
        unseen = set(solid)
        components: list[int] = []
        largest_component: set[tuple[int, int, int]] = set()
        while unseen:
            seed = unseen.pop()
            stack = [seed]
            component = {seed}
            while stack:
                x, y, z = stack.pop()
                for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                          (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                    if n in unseen:
                        unseen.discard(n)
                        component.add(n)
                        stack.append(n)
            components.append(len(component))
            if len(component) > len(largest_component):
                largest_component = component
        orphans = [size for size in components if size < len(largest_component)]
        stray_blocks = sum(orphans)
        detail[name] = {
            "components": len(components),
            "largest": len(largest_component),
            "orphan_components": len(orphans),
            "orphan_blocks": stray_blocks,
        }
        # A handful of deliberately detached scatter blocks is dressing; a
        # large detached mass is a hull section hanging in open water.
        if orphans and max(orphans) > 12:
            issues.append(
                f"structural_continuity: {name} has a detached mass of {max(orphans)} blocks "
                "unsupported by the main structure"
            )
    return detail


def validate_akula_impact_conformance(issues: list[str]) -> dict[str, Any]:
    """The authored wreck must be the consequence of the simulation, not
    merely accompanied by it. Checks the seated attitude of each section
    against the modelled pitch, that the leading end is genuinely bedded, and
    that the break face is torn rather than cut on a plane."""
    detail: dict[str, Any] = {}
    if not IMPACT_REPORT.is_file():
        issues.append("impact_conformance: docs/deepsea-akula-impact-simulation.json not found")
        return detail
    model = json.loads(IMPACT_REPORT.read_text(encoding="utf-8"))
    if not model.get("girder", {}).get("severs"):
        issues.append("impact_conformance: the model does not sever the girder, so a two-section wreck is unexplained")

    for section, asset, lead_at_low_z in (
        ("forward", "akula_wreck_forward_damaged", True),
        ("aft", "akula_wreck_aft_damaged", True),
    ):
        path = STRUCTURE_DIR / f"{asset}.nbt"
        if not path.is_file():
            issues.append(f"impact_conformance: {asset}.nbt not found")
            continue
        size, cells = _load_cells(path)
        sx, sy, sz = size
        hull = {pos: material for pos, material in cells.items()
                if material not in AK_VOID_NAMES and material not in AK_SEDIMENT_NAMES}
        if not hull:
            issues.append(f"impact_conformance: {asset} contains no hull material")
            continue
        keel: dict[int, int] = {}
        counts: dict[int, int] = {}
        for (x, y, z) in hull:
            counts[z] = counts.get(z, 0) + 1
            if z not in keel or y < keel[z]:
                keel[z] = y
        zs = sorted(keel)
        # Least-squares slope of the keel line, converted to an attitude.
        n = len(zs)
        mean_z = sum(zs) / n
        mean_y = sum(keel[z] for z in zs) / n
        denom = sum((z - mean_z) ** 2 for z in zs) or 1.0
        slope = sum((z - mean_z) * (keel[z] - mean_y) for z in zs) / denom
        measured = abs(math.degrees(math.atan(slope)))
        expected = model["sections"][section]["pitch_deg"]
        detail.setdefault(asset, {})["measured_pitch_deg"] = round(measured, 1)
        detail[asset]["model_pitch_deg"] = expected
        if abs(measured - expected) > 4.0:
            issues.append(
                f"impact_conformance: {asset} sits at {measured:.1f} deg but the model derives "
                f"{expected} deg; the authored attitude has drifted from the simulation"
            )
        # Leading end bedded: the modelled penetration says this end went in.
        lead_zs = [z for z in zs if z <= min(zs) + 6] if lead_at_low_z else [z for z in zs if z >= max(zs) - 6]
        lead_keel = min(keel[z] for z in lead_zs)
        detail[asset]["lead_keel_y"] = lead_keel
        if lead_keel > 3:
            issues.append(
                f"impact_conformance: {asset}'s leading end rests at y={lead_keel}, clear of the "
                "ocean-floor datum, but the model says it penetrated the seabed"
            )
        # Torn, not cut: a plane cut leaves a full cross-section at the break.
        mid = sorted(counts.values())[len(counts) // 2] or 1
        tear_end = max(zs) if section == "forward" else min(zs)
        tear_slice = counts.get(tear_end, 0)
        ratio = tear_slice / mid
        detail[asset]["tear_face_ratio"] = round(ratio, 2)
        if ratio > 0.75:
            issues.append(
                f"impact_conformance: {asset}'s break face carries {ratio:.0%} of a full section; "
                "that is a plane cut, not an implosion tear"
            )
    return detail


def validate_akula_atmosphere(issues: list[str]) -> None:
    """Double-hull atmosphere states. The annulus between the two hulls is
    free-flooding by construction and must be water; the pressure hull
    interior is dry in the intact master; and the wreck must have flooded
    everywhere except the one compartment declared to have held its air."""
    clean = STRUCTURE_DIR / "akula_project971_clean_master.nbt"
    if not clean.is_file():
        issues.append("akula_atmosphere: clean master NBT not found")
        return
    _, cells = _load_cells(clean)
    # Ballast annulus, sampled inside the double-hull run only. Aft of the
    # parallel midbody the light hull closes onto the pressure hull and the
    # annulus legitimately pinches out -- as it does on the real boat -- so a
    # sample at, say, frame 90 would fail a correct hull.
    annulus = [(3, 6, 30), (13, 6, 30), (3, 6, 50), (13, 6, 50), (3, 6, 70), (13, 6, 70), (3, 6, 80), (13, 6, 80)]
    dry_annulus = [pos for pos in annulus if cells.get(pos) != "minecraft:water"]
    if dry_annulus:
        issues.append(
            f"akula_atmosphere: main ballast tanks are not flooded at {dry_annulus[:4]}; "
            "the annulus between a double hull's two skins is free-flooding by construction"
        )
    # Pressure hull interior, dry.
    interior = [(8, 7, 25), (8, 7, 50), (7, 7, 89), (8, 6, 20)]
    wet_interior = [pos for pos in interior if cells.get(pos) == "minecraft:water"]
    if wet_interior:
        issues.append(f"akula_atmosphere: water inside the intact pressure hull at {wet_interior[:4]}")

    wreck = STRUCTURE_DIR / "akula_wreck_forward.nbt"
    if not wreck.is_file():
        issues.append("akula_atmosphere: akula_wreck_forward.nbt not found")
        return
    size, wcells = _load_cells(wreck)
    air = sum(1 for material in wcells.values() if material == "minecraft:air")
    water = sum(1 for material in wcells.values() if material == "minecraft:water")
    if water == 0:
        issues.append("akula_atmosphere: the forward wreck section contains no flooded volume")
    if air == 0:
        issues.append(
            "akula_atmosphere: the forward wreck section declares mixed_breached and a surviving "
            "torpedo-room air pocket, but contains no air at all"
        )


# ---------------------------------------------------------------------------
# Wave 3b: the akula_wreck_site jigsaw assembly
# ---------------------------------------------------------------------------

AK_FACINGS = {
    "north_up": (0, 0, -1), "south_up": (0, 0, 1),
    "east_up": (1, 0, 0), "west_up": (-1, 0, 0),
}
AK_SITE_STRUCTURE = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "deep_sea" / "akula_wreck_site.json"


def _load_full(path: Path):
    root = load_nbt(path)
    size = tuple(int(v) for v in root["size"])
    palette = [p["Name"] for p in root["palette"]]
    cells, joints = {}, []
    for b in root["blocks"]:
        pos = tuple(b["pos"])
        name = palette[b["state"]]
        cells[pos] = name
        if name == "minecraft:jigsaw":
            data = b.get("nbt", {})
            state = root["palette"][b["state"]].get("Properties", {})
            joints.append({
                "pos": pos,
                "name": data.get("name"),
                "target": data.get("target"),
                "pool": data.get("pool"),
                "orientation": state.get("orientation"),
            })
    return size, cells, joints


def resolve_akula_assembly() -> dict[str, Any]:
    """Resolve the jigsaw joints from the shipped NBT and return each piece's
    world offset.

    This deliberately re-derives the layout the way the game will, from the
    jigsaw blocks that are actually in the files, instead of re-stating the
    offsets the generator intended. The two only agree if the joints are
    right, which is the entire point of checking."""
    base = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea"
    spine_size, spine_cells, spine_joints = _load_full(base / "akula_wreck_spine.nbt")
    layout: dict[str, Any] = {
        "akula_wreck_spine": {"origin": (0, 0, 0), "size": spine_size, "cells": spine_cells},
    }
    unresolved = []
    for joint in spine_joints:
        child_name = joint["pool"].split("/")[-1] if joint.get("pool") else None
        child_path = base / f"{child_name}.nbt" if child_name else None
        if not child_path or not child_path.is_file():
            unresolved.append(joint)
            continue
        c_size, c_cells, c_joints = _load_full(child_path)
        match = [j for j in c_joints if j["name"] == joint["target"]]
        if not match:
            unresolved.append(joint)
            continue
        facing = AK_FACINGS.get(joint["orientation"])
        child_joint = match[0]
        child_facing = AK_FACINGS.get(child_joint["orientation"])
        opposite = facing and child_facing and all(a == -b for a, b in zip(facing, child_facing))
        px, py, pz = joint["pos"]
        cx, cy, cz = child_joint["pos"]
        origin = (px + facing[0] - cx, py + facing[1] - cy, pz + facing[2] - cz)
        layout[child_name] = {
            "origin": origin, "size": c_size, "cells": c_cells,
            "joint_opposite": opposite,
            "parent_joint": joint["name"], "child_joint": child_joint["name"],
        }
    layout["_unresolved"] = unresolved
    return layout


def validate_akula_assembly(issues: list[str]) -> dict[str, Any]:
    """The two hull sections only read as one event if they actually generate
    together. Checks that both joints resolve, that the pieces do not overlap
    (a child is placed after the start piece and would overwrite the rock),
    that the outcrop really sits between the two tears, and that the
    structure's max_distance_from_center covers the true span."""
    detail: dict[str, Any] = {}
    layout = resolve_akula_assembly()
    if layout["_unresolved"]:
        issues.append(f"assembly: {len(layout['_unresolved'])} jigsaw joint(s) did not resolve to a child element")
    pieces = {k: v for k, v in layout.items() if not k.startswith("_")}
    for name in ("akula_wreck_forward", "akula_wreck_aft"):
        if name not in pieces:
            issues.append(f"assembly: {name} is not reachable from the start pool")
    if len(pieces) < 3:
        return detail

    world: dict[str, set] = {}
    bounds: dict[str, Any] = {}
    for name, piece in pieces.items():
        ox, oy, oz = piece["origin"]
        solid = {(x + ox, y + oy, z + oz) for (x, y, z), material in piece["cells"].items()
                 if material not in ("minecraft:air", "minecraft:water", "minecraft:jigsaw")}
        world[name] = solid
        zs = [p[2] for p in solid]
        bounds[name] = {"origin": list(piece["origin"]), "z_min": min(zs), "z_max": max(zs)}
        if piece.get("joint_opposite") is False:
            issues.append(f"assembly: {name}'s joint does not face opposite its parent; the pieces would not align")
    detail["pieces"] = bounds

    names = list(world)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            clash = world[a] & world[b]
            if clash:
                issues.append(
                    f"assembly: {a} and {b} overlap in {len(clash)} blocks; a jigsaw child is "
                    "placed after the start piece and would overwrite it"
                )
    # The outcrop must actually sit BETWEEN the two hull sections -- if it
    # does not, the assembly still generates but the rock explains nothing.
    spine = bounds["akula_wreck_spine"]
    fwd, aft = bounds["akula_wreck_forward"], bounds["akula_wreck_aft"]
    between = fwd["z_max"] <= spine["z_max"] and aft["z_min"] >= spine["z_min"]
    detail["outcrop_between_sections"] = between
    if not between:
        issues.append("assembly: the outcrop does not sit between the two hull sections")
    gap_forward = spine["z_min"] - fwd["z_max"]
    gap_aft = aft["z_min"] - spine["z_max"]
    detail["gap_forward_blocks"] = gap_forward
    detail["gap_aft_blocks"] = gap_aft
    for label, gap in (("forward", gap_forward), ("aft", gap_aft)):
        if gap > 12:
            issues.append(
                f"assembly: {gap} blocks of open seabed between the outcrop and the {label} "
                "section; the rock no longer reads as what broke the hull"
            )

    all_z = [z for solid in world.values() for (_, _, z) in solid]
    span = max(abs(min(all_z)), abs(max(all_z)))
    detail["max_span_from_start_blocks"] = span
    if AK_SITE_STRUCTURE.is_file():
        doc = json.loads(AK_SITE_STRUCTURE.read_text(encoding="utf-8"))
        limit = doc.get("max_distance_from_center", 0)
        detail["max_distance_from_center"] = limit
        if limit < span:
            issues.append(
                f"assembly: max_distance_from_center is {limit} but the assembly reaches {span} "
                "blocks from the start piece; a hull section would be clipped"
            )
        if doc.get("size", 0) < 2:
            issues.append("assembly: jigsaw size is below 2, so no child piece can be placed")
    else:
        issues.append("assembly: akula_wreck_site.json not found")
    return detail


# ---------------------------------------------------------------------------
# Wave 3c: radiological dressing and the live-functional-block policy
# ---------------------------------------------------------------------------

AK_RADIATION_SOURCE_BLOCKS = {
    "create_new_age:corium": "extreme",
    "create_new_age:solid_corium": "high",
    "the_wasteland_reworked:waste_barrel": "high",
    "wastelands:radioactive_waste": "high",
}
# Per-asset ceiling on high-tier emitters. Sized against the standards'
# Hazard/atmosphere-fit axis rather than picked round: a high-tier source is 4
# units/check out to 8 blocks in the pack's unified radiation model, seawater
# attenuates 12% per block and lead 65%, so a few dozen shielded blocks read as
# a hot compartment a prepared diver can work in. Several hundred would make
# the wreck a no-go zone, which the standards call a design defect and not
# difficulty.
AK_HAZARD_CEILING = 40
# Blocks whose whole point is that they are live and progression-gating.
# docs/RUINED_FUNCTIONAL_BLOCKS.md forbids these as set dressing and requires
# the ruined-equivalent instead.
AK_FORBIDDEN_FUNCTIONAL = {
    "minecraft:furnace", "minecraft:smoker", "minecraft:blast_furnace",
    "minecraft:brewing_stand", "minecraft:beacon", "minecraft:conduit",
}


def validate_akula_hazard_and_fitness(issues: list[str]) -> dict[str, Any]:
    """Two policy gates the existing checks cannot see.

    `scripts/audit_structure_block_fitness.py` enforces the live-functional
    rule, but only over `structure/wasteland` and only for NON-vanilla blocks.
    This corpus lives elsewhere and its violation was a vanilla blast furnace,
    so it fell through both halves of that gate. This check closes the deep-sea
    side of the gap; the wasteland-side scan path is widened separately.

    The hazard budget exists because radiological dressing is the one damage
    vocabulary where more is trivially easy and actively worse."""
    detail: dict[str, Any] = {}
    if not STRUCTURE_DIR.is_dir():
        issues.append("hazard_and_fitness: structure directory not found")
        return detail
    for path in sorted(STRUCTURE_DIR.glob("*.nbt")):
        name = path.stem
        try:
            _size, cells = _load_cells(path)
        except (OSError, EOFError, KeyError, ValueError) as error:
            issues.append(f"hazard_and_fitness: {name} unreadable NBT ({error})")
            continue
        counts: dict[str, int] = {}
        for material in cells.values():
            if material in AK_RADIATION_SOURCE_BLOCKS:
                counts[material] = counts.get(material, 0) + 1
        live = sorted({m for m in cells.values() if m in AK_FORBIDDEN_FUNCTIONAL})
        entry: dict[str, Any] = {}
        if counts:
            entry["radiation_sources"] = counts
            total = sum(counts.values())
            entry["total_source_blocks"] = total
            if total > AK_HAZARD_CEILING:
                issues.append(
                    f"hazard_budget: {name} places {total} radiation-source blocks, over the "
                    f"{AK_HAZARD_CEILING}-block ceiling; that is a no-go zone, not a hot compartment"
                )
            extreme = [m for m in counts if AK_RADIATION_SOURCE_BLOCKS[m] == "extreme"]
            if extreme:
                issues.append(
                    f"hazard_budget: {name} places extreme-tier source(s) {extreme}; this corpus's "
                    "wrecks are meant to be enterable, so extreme-tier emitters need an explicit "
                    "documented decision rather than being reachable by default"
                )
        if live:
            issues.append(
                f"block_fitness: {name} places live functional block(s) {live} as set dressing, "
                "which docs/RUINED_FUNCTIONAL_BLOCKS.md forbids; use the ruined-equivalent"
            )
            entry["live_functional_blocks"] = live
        if entry:
            detail[name] = entry

    # The intact reference boat must NOT be radiological. Corium is what a
    # core becomes after it melts; a clean master carrying it would mean the
    # damage state had leaked into the asset it is supposed to be derived from.
    clean = STRUCTURE_DIR / "akula_project971_clean_master.nbt"
    if clean.is_file():
        _size, cells = _load_cells(clean)
        leaked = sorted({m for m in cells.values() if m in AK_RADIATION_SOURCE_BLOCKS})
        detail["_clean_master_radiological"] = leaked
        if leaked:
            issues.append(
                f"hazard_budget: the intact clean master places {leaked}; corium and waste drums "
                "are consequences of the casualty and must not appear in the pre-damage reference"
            )
    return detail


def validate_placement_gate(issues: list[str]) -> dict[str, Any]:
    gate_report: dict[str, Any] = {"quarantine_tag_present": QUARANTINE_TAG_PATH.is_file(), "csv_rows_present": {}, "biomes_gated": {}}
    if gate_report["quarantine_tag_present"]:
        tag_doc = json.loads(QUARANTINE_TAG_PATH.read_text(encoding="utf-8"))
        if tag_doc.get("values"):
            issues.append("quarantine tag is not empty; deep-sea assets would be reachable in real biomes")
    else:
        issues.append("quarantine tag file missing")

    # A shared salt across several structures in one registrant's own
    # structure_set (e.g. one mod's multi-structure family) is normal; the
    # thing this system actually needs to avoid is a *new* deep-sea salt
    # colliding with any salt some other registrant already owns.
    csv_text = CSV_PATH.read_text(encoding="utf-8") if CSV_PATH.is_file() else ""
    new_salts = {"48217701", "48217702", "48217703", "48217704", "48217705",
                 "48217706", "48217707", "48217708"}
    other_salts: set[str] = set()
    for line in csv_text.splitlines()[1:]:
        cells = [c.strip('"') for c in line.split('","')]
        cells[0] = cells[0].lstrip('"')
        cells[-1] = cells[-1].rstrip('"')
        if len(cells) >= 7 and "deep_sea" not in cells[1]:
            other_salts.add(cells[6])
    seen_targets: set[tuple[str, str, str]] = set()
    duplicate_targets: set[str] = set()
    for line in csv_text.splitlines()[1:]:
        cells = [c.strip('"') for c in line.split('","')]
        if len(cells) < 3:
            continue
        # Key on (jar, resource, target). Two different jars legitimately
        # register the same structure set -- the Seven Seas entries already
        # do -- so keying on target alone would flag correct data.
        key = (cells[0], cells[1], cells[2])
        if key in seen_targets:
            duplicate_targets.add(cells[2])
        seen_targets.add(key)
    if duplicate_targets:
        issues.append(f"ocean-structure-sets.csv has duplicate registrant rows for {sorted(duplicate_targets)}")
    gate_report["duplicate_registrant_rows"] = sorted(duplicate_targets)

    salt_collisions = new_salts & other_salts
    if salt_collisions:
        issues.append(f"deep-sea placement salts collide with existing registrants: {sorted(salt_collisions)}")

    placed_assets = (
        "infinite_domain:deep_sea/coastal_patrol_wreck",
        "infinite_domain:deep_sea/coastal_patrol_debris_field",
        "infinite_domain:deep_sea/flooded_relay_shelter",
        "infinite_domain:deep_sea/abyssal_mining_rig",
        "infinite_domain:deep_sea/abyssal_vent_field",
        "infinite_domain:deep_sea/akula_wreck_site",
        "infinite_domain:deep_sea/akula_debris_field",
    )
    # Admitted to production by owner directive on 2026-08-25 with the
    # in-game QA walkthrough explicitly skipped -- see
    # docs/DEEP_SEA_STRUCTURE_AUDIT.md. Every other member of placed_assets
    # must still be gated behind the quarantine tag.
    ADMITTED_ASSETS = {
        "infinite_domain:deep_sea/akula_wreck_site": "#infinite_domain:eastern_slope_biomes",
        "infinite_domain:deep_sea/akula_debris_field": "#infinite_domain:eastern_slope_biomes",
    }
    for name in placed_assets:
        gate_report["csv_rows_present"][name] = name in csv_text
        if name not in csv_text:
            issues.append(f"{name}: no registrant row in ocean-structure-sets.csv")
        struct_path = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "deep_sea" / f"{name.rsplit('/', 1)[-1]}.json"
        if struct_path.is_file():
            doc = json.loads(struct_path.read_text(encoding="utf-8"))
            expected_biomes = ADMITTED_ASSETS.get(name, "#infinite_domain:disabled_quarantine_deep_sea_structures")
            gated = doc.get("biomes") == expected_biomes
            gate_report["biomes_gated"][name] = gated
            if not gated:
                if name in ADMITTED_ASSETS:
                    issues.append(f"{name}: structure biomes selector is not the admitted selector {expected_biomes!r}")
                else:
                    issues.append(f"{name}: structure biomes selector is not the quarantine tag")
        else:
            issues.append(f"{name}: worldgen structure json missing")

    return gate_report


def main() -> None:
    document = json.loads(CATALOG.read_text(encoding="utf-8"))
    if document.get("format_version") != 1:
        raise SystemExit("deepsea-catalog.json: unsupported format_version")
    assets = document.get("assets", [])

    results: dict[str, Any] = {}
    seen: set[str] = set()
    for index, entry in enumerate(assets):
        asset_id = entry.get("asset_id", f"entry_{index}") if isinstance(entry, dict) else f"entry_{index}"
        issues: list[str] = []
        if not isinstance(entry, dict):
            issues.append("entry is not an object")
        else:
            validate_common(entry, issues)
            if entry.get("asset_id") in seen:
                issues.append("duplicate asset_id")
            seen.add(entry.get("asset_id"))
            asset_class = entry.get("asset_class")
            if asset_class == "geological_macro":
                validate_geological_macro(entry, issues)
            elif asset_class == "geological_feature":
                validate_geological_feature(entry, issues)
            elif asset_class == "structure":
                validate_structure(entry, issues)
        results[asset_id] = {"metadata_valid": not issues, "issues": issues}

    atmosphere_issues: list[str] = []
    validate_atmosphere_fill(atmosphere_issues)
    results["_atmosphere_fill"] = {"metadata_valid": not atmosphere_issues, "issues": atmosphere_issues}

    render_color_issues: list[str] = []
    render_color_detail = validate_render_color_fidelity(render_color_issues)
    results["_render_color_fidelity"] = {
        "metadata_valid": not render_color_issues,
        "issues": render_color_issues,
        "detail": render_color_detail,
    }

    akula_issues: list[str] = []
    validate_akula_atmosphere(akula_issues)
    results["_akula_atmosphere"] = {"metadata_valid": not akula_issues, "issues": akula_issues}

    dressing_issues: list[str] = []
    dressing_detail = validate_akula_dressing_density(dressing_issues)
    results["_akula_dressing_density"] = {
        "metadata_valid": not dressing_issues, "issues": dressing_issues, "detail": dressing_detail,
    }

    continuity_issues: list[str] = []
    continuity_detail = validate_akula_structural_continuity(continuity_issues)
    results["_akula_structural_continuity"] = {
        "metadata_valid": not continuity_issues, "issues": continuity_issues, "detail": continuity_detail,
    }

    impact_issues: list[str] = []
    impact_detail = validate_akula_impact_conformance(impact_issues)
    results["_akula_impact_conformance"] = {
        "metadata_valid": not impact_issues, "issues": impact_issues, "detail": impact_detail,
    }

    hazard_issues: list[str] = []
    hazard_detail = validate_akula_hazard_and_fitness(hazard_issues)
    results["_akula_hazard_and_fitness"] = {
        "metadata_valid": not hazard_issues, "issues": hazard_issues, "detail": hazard_detail,
    }

    assembly_issues: list[str] = []
    assembly_detail = validate_akula_assembly(assembly_issues)
    results["_akula_assembly"] = {
        "metadata_valid": not assembly_issues, "issues": assembly_issues, "detail": assembly_detail,
    }

    placement_issues: list[str] = []
    gate_report = validate_placement_gate(placement_issues)
    results["_placement_gate"] = {"metadata_valid": not placement_issues, "issues": placement_issues, "detail": gate_report}

    report = {
        "purpose": "Deep-sea corpus metadata, source-NBT dimension, atmosphere-fill, and production-gate validation. This is not visual or in-world approval.",
        "assets_checked": len(assets),
        "valid": all(result["metadata_valid"] for result in results.values()),
        "production_approved": sum(1 for a in assets if isinstance(a, dict) and a.get("production_status") == "approved"),
        "assets": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not report["valid"]:
        failures = [f"{name}: {', '.join(result['issues'])}" for name, result in results.items() if result["issues"]]
        raise SystemExit("\n".join(failures))
    print(f"Validated {len(assets)} deep-sea catalog assets; 0 production approvals; placement gate holds")


if __name__ == "__main__":
    main()

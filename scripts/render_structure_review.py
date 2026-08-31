from __future__ import annotations

import argparse
import colorsys
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from build_structure_qa_world import NbtList, Reader


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
OUTPUT = ROOT / "structure_library" / "reviews"
INBUILT_MANIFEST = ROOT / "docs" / "wasteland-site-manifest.json"
INBUILT_OUTPUT = ROOT / "structure_library" / "audit_renders"
CREATIVELANDS_PROVENANCE = ROOT / "structure_library" / "licensing" / "creativelands-extracted-provenance.json"
CREATIVELANDS_OUTPUT = ROOT / "structure_library" / "reviews" / "creativelands_cc0"
ROAD_CATALOG = ROOT / "structure_library" / "roads" / "road-modules.json"
ROAD_OUTPUT = ROOT / "structure_library" / "reviews" / "road_modules"
MODULE_CATALOG = ROOT / "structure_library" / "modules" / "structure-kits.json"
MODULE_OUTPUT = ROOT / "structure_library" / "reviews" / "structure_modules"
OLD_WORLD_REGISTRY = ROOT / "old_world_narrative" / "registry" / "structure_targets.json"
OLD_WORLD_OUTPUT = ROOT / "old_world_narrative" / "reviews"
CUTAWAY_OVERRIDES = {
    "infinite_domain:gas_station_clean_master": 14,
    "infinite_domain:ruined_gas_station": 14,
    "infinite_domain:freight_depot_clean_master": 10,
    "infinite_domain:freight_depot": 10,
    "infinite_domain:fire_station_clean_master": 10,
    "infinite_domain:ruined_fire_station": 10,
    "infinite_domain:corporate_warehouse_clean_master": 10,
    "infinite_domain:corporate_warehouse": 10,
    "infinite_domain:create_factory_clean_master": 10,
    "infinite_domain:abandoned_create_factory": 10,
    "infinite_domain:bunker_network_clean_master": 10,
    "infinite_domain:bunker_network": 10,
    "infinite_domain:survivor_cache_clean_master": 2,
    "infinite_domain:survivor_cache": 2,
    "infinite_domain:trade_outpost_clean_master": 7,
    "infinite_domain:trade_outpost": 7,
    "infinite_domain:decayed_farm_clean_master": 7,
    "infinite_domain:decayed_farm": 7,
    "infinite_domain:trailer_park_clean_master": 7,
    "infinite_domain:trailer_park": 7,
    "infinite_domain:mountain_military_complex_clean_master": 9,
    "infinite_domain:mountain_military_complex": 9,
    "infinite_domain:mountain_biohazard_lab_clean_master": 9,
    "infinite_domain:mountain_biohazard_lab": 9,
    "infinite_domain:decayed_logging_camp_clean_master": 9,
    "infinite_domain:decayed_logging_camp": 9,
    "infinite_domain:bombed_data_center_clean_master": 9,
    "infinite_domain:bombed_data_center": 9,
    "infinite_domain:hydroelectric_refuge_dam_clean_master": 10,
    "infinite_domain:hydroelectric_refuge_dam": 10,
    "infinite_domain:toppled_skyscraper_clean_master": 17,
    "infinite_domain:toppled_skyscraper": 17,
    "infinite_domain:blown_apartment_complex_clean_master": 16,
    "infinite_domain:blown_apartment_complex": 16,
    "infinite_domain:ruined_mixed_use_block_clean_master": 16,
    "infinite_domain:ruined_mixed_use_block": 16,
    "infinite_domain:sunken_city_front_clean_master": 12,
    "infinite_domain:sunken_city_front": 12,
    "infinite_domain:pancaked_parking_structure_clean_master": 16,
    "infinite_domain:pancaked_parking_structure": 16,
    "infinite_domain:cratered_downtown_intersection_clean_master": 13,
    "infinite_domain:cratered_downtown_intersection": 13,
    "infinite_domain:ruined_hospital_clean_master": 16,
    "infinite_domain:ruined_hospital": 16,
    "infinite_domain:ruined_police_precinct_clean_master": 9,
    "infinite_domain:ruined_police_precinct": 9,
    "infinite_domain:ruined_courthouse_clean_master": 11,
    "infinite_domain:ruined_courthouse": 11,
}
FLOOR_SLICE_OVERRIDES = {
    # Six-block Karsic repeatable bands. The generic density detector can
    # mistake the stair landing at the top of each band for the next floor and
    # then suppress the real slab two blocks later. These planes show the
    # basement plus the ground and four repeatable dwelling storeys.
    "infinite_domain:kar_067_series_panel_block_clean_master": [3, 7, 13, 19, 25, 31],
    "infinite_domain:kar_067_series_panel_block": [3, 7, 13, 19, 25, 31],
    # One cellar, a retail plinth at Y=6, and five residential bands above.
    # Generic density detection otherwise chooses the intermediate stair
    # landings (Y=11/17/...) and hides the actual dwelling plans.
    "infinite_domain:kar_024_panel_block_service_premises_clean_master": [3, 7, 13, 19, 25, 31, 37],
    "infinite_domain:kar_024_panel_block_service_premises": [3, 7, 13, 19, 25, 31, 37],
}


def unpack_structure(path: Path) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], str]]:
    _, root = Reader(gzip.decompress(path.read_bytes())).root()
    data = root.value
    size = tuple(int(tag.value) for tag in data["size"].value.values)
    palette = [entry.value["Name"].value for entry in data["palette"].value.values]
    blocks: dict[tuple[int, int, int], str] = {}
    for entry_tag in data["blocks"].value.values:
        entry = entry_tag.value
        pos = tuple(int(tag.value) for tag in entry["pos"].value.values)
        name = palette[int(entry["state"].value)]
        if name not in {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}:
            blocks[pos] = name
    return size, blocks


def color_for(name: str) -> tuple[int, int, int]:
    path = name.split(":", 1)[-1]
    rules = [
        (("glass", "pane"), (100, 185, 205)), (("water",), (45, 95, 190)), (("lava",), (235, 90, 30)),
        (("black_concrete", "blackstone"), (38, 40, 42)), (("yellow_concrete", "yellow_carpet"), (224, 185, 45)),
        (("white_concrete", "white_carpet"), (225, 225, 217)), (("gray_concrete",), (90, 94, 97)),
        (("smooth_stone",), (171, 171, 164)),
        (("leaves", "grass", "vine", "plant", "bush"), (78, 116, 63)), (("wood", "log", "plank"), (127, 91, 55)),
        (("brick",), (142, 72, 61)), (("concrete", "stone", "deepslate"), (112, 112, 111)),
        (("copper", "rust"), (132, 96, 70)), (("steel", "iron", "metal"), (128, 139, 144)),
        (("sand", "gravel", "dirt"), (139, 119, 83)), (("light", "lamp", "torch"), (225, 190, 84)),
    ]
    for terms, color in rules:
        if any(term in path for term in terms):
            return color
    digest = hashlib.sha256(name.encode()).digest()
    hue = int.from_bytes(digest[:2], "big") / 65535
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.38, 0.68)
    return int(red * 255), int(green * 255), int(blue * 255)


def shade(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(channel * factor))) for channel in color)


def exposed(blocks: dict[tuple[int, int, int], str]) -> dict[tuple[int, int, int], str]:
    offsets = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    return {pos: name for pos, name in blocks.items() if any((pos[0] + dx, pos[1] + dy, pos[2] + dz) not in blocks for dx, dy, dz in offsets)}


def isometric(size: tuple[int, int, int], source: dict[tuple[int, int, int], str], reverse: bool, title: str) -> Image.Image:
    scale = 7
    sx, sy, sz = size
    blocks = exposed(source)
    width = (sx + sz) * scale + 100
    height = (sx + sz) * scale // 2 + sy * scale + 100
    image = Image.new("RGB", (width, height), (26, 28, 30))
    draw = ImageDraw.Draw(image)
    origin_x, origin_y = width // 2, 35 + sy * scale

    transformed = []
    for (x, y, z), name in blocks.items():
        tx, tz = (sx - 1 - x, sz - 1 - z) if reverse else (x, z)
        transformed.append((tx + tz + y * 0.01, tx, y, tz, name))
    transformed.sort()
    for _, x, y, z, name in transformed:
        px = origin_x + (x - z) * scale
        py = origin_y + (x + z) * scale // 2 - y * scale
        c = color_for(name)
        top = [(px, py - scale), (px + scale, py - scale // 2), (px, py), (px - scale, py - scale // 2)]
        left = [(px - scale, py - scale // 2), (px, py), (px, py + scale), (px - scale, py + scale // 2)]
        right = [(px, py), (px + scale, py - scale // 2), (px + scale, py + scale // 2), (px, py + scale)]
        draw.polygon(left, fill=shade(c, 0.67))
        draw.polygon(right, fill=shade(c, 0.82))
        draw.polygon(top, fill=shade(c, 1.08))
    draw.rectangle((0, 0, width, 26), fill=(10, 11, 12))
    draw.text((10, 7), title, fill=(235, 235, 235))
    return image


def floor_slices(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    title: str,
    selected_override: list[int] | None = None,
) -> Image.Image:
    sx, sy, sz = size
    counts = {y: sum(1 for _, py, _ in blocks if py == y) for y in range(sy)}
    area = sx * sz
    # A floor support is a dense horizontal level with two occupied levels
    # above it. That rejects pads and roofs; the rendered plane is one block
    # above the support so walls, doors and furnishings are visible.
    candidates = [
        y for y in range(sy - 2)
        if counts[y] >= max(8, int(area * 0.12))
        and counts[y] > counts[y + 1] * 1.35
        and counts[y + 1] >= max(8, int(area * 0.04))
        and counts[y + 2] >= max(8, int(area * 0.04))
    ]
    supports: list[int] = []
    for level in candidates:
        if not supports or level - supports[-1] > 2:
            supports.append(level)
    selected = list(selected_override) if selected_override is not None else [level + 1 for level in supports]
    if not selected:
        selected = [min(sy - 1, max(counts, key=counts.get) + 1)]
    # A deliberately raised surface plane indicates a buried program. Include
    # an explicit basement slice so tanks, bunkers and service vaults are not
    # hidden by an otherwise correct above-ground floor selection.
    dominant_support = max(counts, key=counts.get)
    if (selected_override is None and dominant_support >= 4
            and any(y < dominant_support - 1 and count >= 8 for y, count in counts.items())):
        basement_slice = max(1, dominant_support // 2)
        selected = [basement_slice, *[level for level in selected if level != basement_slice]]
    cell = 5
    panel_w, panel_h = sx * cell + 24, sz * cell + 44
    columns = min(3, len(selected))
    rows = (len(selected) + columns - 1) // columns
    image = Image.new("RGB", (columns * panel_w, rows * panel_h), (26, 28, 30))
    draw = ImageDraw.Draw(image)
    for index, level in enumerate(selected):
        ox, oy = (index % columns) * panel_w + 12, (index // columns) * panel_h + 30
        draw.text((ox, oy - 20), f"{title} — horizontal slice Y={level}", fill=(235, 235, 235))
        for (x, y, z), name in blocks.items():
            if y != level:
                continue
            draw.rectangle((ox + x * cell, oy + z * cell, ox + (x + 1) * cell - 1, oy + (z + 1) * cell - 1), fill=color_for(name))
        draw.rectangle((ox - 1, oy - 1, ox + sx * cell, oy + sz * cell), outline=(170, 170, 170))
    return image


def render(entry: dict[str, Any], output_root: Path = OUTPUT) -> dict[str, Any]:
    name = entry["structure_id"].split(":", 1)[1]
    size, blocks = unpack_structure(ROOT / entry["source_template"])
    output = output_root / name
    output.mkdir(parents=True, exist_ok=True)
    # Select the underside of the first dense roof plane. Tall signs, chimneys
    # and towers should not inflate the cutaway above a one-storey interior.
    counts = {y: sum(1 for _, py, _ in blocks if py == y) for y in range(size[1])}
    area = size[0] * size[2]
    roof_planes = [
        y for y in range(3, size[1] - 1)
        if counts[y] >= max(12, int(area * 0.12))
        and counts[y] < int(area * 0.75)
        and counts[y] > counts[y - 1] * 1.8
        and counts[y] > counts[y + 1] * 1.8
    ]
    cutoff = CUTAWAY_OVERRIDES.get(
        entry["structure_id"],
        max(2, min(roof_planes) - 1) if roof_planes else max(2, int(size[1] * 0.62)),
    )
    cutaway = {pos: block for pos, block in blocks.items() if pos[1] <= cutoff}
    files = {
        "exterior_a": output / "exterior_a.png",
        "exterior_b": output / "exterior_b.png",
        "roof_off_cutaway": output / "roof_off_cutaway.png",
        "floor_slices": output / "floor_slices.png",
    }
    isometric(size, blocks, False, f"{name} — exterior A").save(files["exterior_a"])
    isometric(size, blocks, True, f"{name} — exterior B").save(files["exterior_b"])
    isometric(size, cutaway, False, f"{name} — roof-off cutaway at Y={cutoff}").save(files["roof_off_cutaway"])
    floor_slices(
        size,
        blocks,
        name,
        FLOOR_SLICE_OVERRIDES.get(entry["structure_id"]),
    ).save(files["floor_slices"])
    return {"structure_id": entry["structure_id"], "source_size": size, "cutaway_y": cutoff, "renders": {key: str(path.relative_to(ROOT)).replace("\\", "/") for key, path in files.items()}, "visual_approval": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("structure_ids", nargs="*", help="One or more full IDs or paths; omit with --all")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--inbuilt", action="store_true", help="Render the authoritative 84-template Wasteland inventory")
    parser.add_argument("--creativelands", action="store_true", help="Render deterministic Creative Lands CC0 review NBT")
    parser.add_argument("--roads", action="store_true", help="Render the quarantined modular road corpus")
    parser.add_argument("--modules", action="store_true", help="Render the quarantined port/market/industrial module kits")
    parser.add_argument("--old-world", action="store_true", help="Render statically implemented Old World narrative variants")
    args = parser.parse_args()
    if sum((args.inbuilt, args.creativelands, args.roads, args.modules, args.old_world)) > 1:
        raise SystemExit("Choose only one corpus mode")
    if args.inbuilt:
        if args.structure_ids or args.all:
            raise SystemExit("Use --inbuilt by itself")
        manifest = json.loads(INBUILT_MANIFEST.read_text(encoding="utf-8"))
        names = list(manifest["structures"])
        if len(names) != 84 or len(set(names)) != 84:
            raise SystemExit(f"Authoritative inventory must contain 84 unique structures, found {len(names)}")
        selected = [
            {
                "structure_id": f"infinite_domain:{name}",
                "source_template": f"kubejs/data/infinite_domain/structure/wasteland/{name}.nbt",
            }
            for name in names
        ]
        output_root = INBUILT_OUTPUT
    elif args.creativelands:
        if args.structure_ids or args.all:
            raise SystemExit("Use --creativelands by itself")
        provenance = json.loads(CREATIVELANDS_PROVENANCE.read_text(encoding="utf-8"))
        selected = [
            {
                "structure_id": record["structure_id"],
                "source_template": record["converted_filename"],
            }
            for record in provenance["records"]
        ]
        output_root = CREATIVELANDS_OUTPUT
    elif args.roads:
        if args.structure_ids or args.all:
            raise SystemExit("Use --roads by itself")
        road_catalog = json.loads(ROAD_CATALOG.read_text(encoding="utf-8"))
        selected = [
            {
                "structure_id": record["module_id"],
                "source_template": record["source_template"],
            }
            for record in road_catalog["modules"]
        ]
        output_root = ROAD_OUTPUT
    elif args.modules:
        if args.structure_ids or args.all:
            raise SystemExit("Use --modules by itself")
        module_catalog = json.loads(MODULE_CATALOG.read_text(encoding="utf-8"))
        selected = [
            {
                "structure_id": record["module_id"],
                "source_template": record["source_template"],
            }
            for record in module_catalog["modules"]
        ]
        output_root = MODULE_OUTPUT
    elif args.old_world:
        if args.structure_ids or args.all:
            raise SystemExit("Use --old-world by itself")
        targets = json.loads(OLD_WORLD_REGISTRY.read_text(encoding="utf-8"))["targets"]
        selected = [
            {
                "structure_id": record["narrative_structure"],
                "source_template": record["narrative_source_template"],
            }
            for record in targets
            if record.get("implementation_status", "").startswith("implemented_")
            and record.get("narrative_structure")
            and record.get("narrative_source_template")
        ]
        output_root = OLD_WORLD_OUTPUT
    else:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["structures"]
        if args.all and args.structure_ids:
            raise SystemExit("Use either explicit structure IDs or --all")
        wanted = set(args.structure_ids)
        selected = catalog if args.all else [
            entry for entry in catalog
            if wanted & {entry["structure_id"], entry["structure_id"].split(":", 1)[1]}
        ]
        output_root = OUTPUT
    if not selected:
        raise SystemExit("No matching structure; supply one or more IDs, --all, --inbuilt, or --creativelands")
    results = [render(entry, output_root) for entry in selected]
    rendered_count = len(results)
    if output_root == OUTPUT and not args.all and (output_root / "render-manifest.json").exists():
        existing = json.loads((output_root / "render-manifest.json").read_text(encoding="utf-8"))
        merged = {entry["structure_id"]: entry for entry in existing.get("structures", [])}
        merged.update({entry["structure_id"]: entry for entry in results})
        catalog_order = {
            entry["structure_id"]: index
            for index, entry in enumerate(json.loads(CATALOG.read_text(encoding="utf-8"))["structures"])
        }
        results = sorted(merged.values(), key=lambda entry: catalog_order.get(entry["structure_id"], len(catalog_order)))
    manifest = {"purpose": "Automated review images; successful rendering is not visual approval.", "structures": results}
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered {rendered_count} structures with four review views each; manifest tracks {len(results)}")


if __name__ == "__main__":
    main()

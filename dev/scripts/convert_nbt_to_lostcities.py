from __future__ import annotations

import argparse
import errno
import gzip
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from build_structure_qa_world import NbtList, Reader, Tag
from generate_wasteland_sites import (
    RUINED_FUNCTIONAL_BLOCK_PROPERTIES,
    STRUCTURE_BLOCK_REPLACEMENTS,
)


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
PROGRAMS = ROOT / "dev/structure_library" / "programs"
ASSETS = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities"
REPORT = ROOT / "dev/docs" / "lostcities-conversion-report.json"
FLOOR_HEIGHT = 6

# Space means generated air in a Lost Cities slice. These characters are safe
# single UTF-16 code units and avoid the global palette punctuation most often
# used by Lost Cities itself. Every converted part owns a local palette.
PALETTE_CHARS = [chr(code) for code in range(33, 127) if chr(code) not in {'"', "\\", "#", "}"}]
PALETTE_CHARS += [chr(code) for code in range(0x00A1, 0x0180)]
PALETTE_CHARS += [chr(code) for code in range(0x0370, 0x0400)]


@dataclass(frozen=True)
class BlockValue:
    block: str
    tag_key: str = ""


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, indent=2, ensure_ascii=True) + "\n"
    # Windows occasionally returns EINVAL while the game/launcher scanner has
    # a freshly regenerated asset open. Retry only that transient condition;
    # permission, path and disk errors must remain immediate failures.
    for attempt in range(12):
        try:
            path.write_text(content, encoding="utf-8", newline="\n")
            return
        except OSError as error:
            if error.errno != errno.EINVAL or attempt == 11:
                raise
            time.sleep(min(0.25, 0.05 * (attempt + 1)))


def tag_value(tag: Tag) -> Any:
    if tag.kind == 9:
        return [tag_value(value) for value in tag.value.values]
    if tag.kind == 10:
        return {name: tag_value(value) for name, value in tag.value.items() if name not in {"x", "y", "z", "keepPacked"}}
    if tag.kind == 7:
        return list(tag.value)
    return tag.value


def state_string(palette_tag: Tag) -> str:
    palette = palette_tag.value
    name = palette["Name"].value
    properties = palette.get("Properties")
    if not properties:
        return name
    values = properties.value
    return name + "[" + ",".join(f"{key}={values[key].value}" for key in sorted(values)) + "]"


def load_structure(path: Path) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], tuple[str, dict[str, Any] | None]]]:
    _, root = Reader(gzip.decompress(path.read_bytes())).root()
    document = root.value
    size = tuple(int(value.value) for value in document["size"].value.values)
    palette = [state_string(value) for value in document["palette"].value.values]
    blocks: dict[tuple[int, int, int], tuple[str, dict[str, Any] | None]] = {}
    for block_tag in document["blocks"].value.values:
        block = block_tag.value
        pos = tuple(int(value.value) for value in block["pos"].value.values)
        state = palette[int(block["state"].value)]
        if state.split("[", 1)[0] in {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}:
            continue
        nbt = tag_value(block["nbt"]) if "nbt" in block else None
        blocks[pos] = (state, nbt)
    return size, blocks


def stabilized_source_value(
    value: tuple[str, dict[str, Any] | None],
) -> tuple[str, dict[str, Any] | None]:
    """Apply the same stable functional-block policy as the NBT writer."""
    state, nbt = value
    name, separator, raw_properties = state.partition("[")
    if name not in STRUCTURE_BLOCK_REPLACEMENTS:
        return value
    replacement = STRUCTURE_BLOCK_REPLACEMENTS[name]
    properties: dict[str, str] = {}
    if separator:
        properties = {
            key: item for key, item in (
                component.split("=", 1) for component in raw_properties.rstrip("]").split(",")
            )
        }
    allowed = RUINED_FUNCTIONAL_BLOCK_PROPERTIES.get(replacement)
    properties = {key: item for key, item in properties.items() if allowed and key in allowed}
    stable_state = replacement
    if properties:
        stable_state += "[" + ",".join(f"{key}={properties[key]}" for key in sorted(properties)) + "]"
    if replacement.startswith("kubejs:ruined_"):
        nbt = None
    return stable_state, nbt


def local_palette(values: list[tuple[str, dict[str, Any] | None]]) -> tuple[dict[BlockValue, str], list[dict[str, Any]]]:
    unique: dict[BlockValue, tuple[str, dict[str, Any] | None]] = {}
    for block, tag in values:
        tag_key = json.dumps(tag, sort_keys=True, separators=(",", ":")) if tag else ""
        unique.setdefault(BlockValue(block, tag_key), (block, tag))
    if len(unique) > len(PALETTE_CHARS):
        raise ValueError(f"part requires {len(unique)} local palette characters; maximum is {len(PALETTE_CHARS)}")
    mapping: dict[BlockValue, str] = {}
    entries: list[dict[str, Any]] = []
    for char, (key, (block, tag)) in zip(PALETTE_CHARS, sorted(unique.items(), key=lambda item: (item[0].block, item[0].tag_key))):
        mapping[key] = char
        entry: dict[str, Any] = {"char": char, "block": block}
        if tag:
            entry["tag"] = tag
        entries.append(entry)
    return mapping, entries


def repeatable_contract(entry: dict[str, Any], floors: int) -> dict[str, int] | None:
    """Load and validate an explicitly authored Lost Cities repeat contract.

    Repeatable massing is not inferred from coincidentally similar bands. The
    structure program must opt in and name the cellar, ground, repeat and top
    band roles. This keeps ordinary converted buildings pinned to their source
    height while allowing the Karsic panel system to express its planned 5-9
    storey skyline from one reviewed master.
    """
    slug = entry["structure_id"].split(":", 1)[1]
    if slug.endswith("_clean_master"):
        slug = slug.removesuffix("_clean_master")
    path = PROGRAMS / f"{slug}.json"
    if not path.is_file():
        return None
    program = json.loads(path.read_text(encoding="utf-8"))
    raw = program.get("lostcities_repeatable_contract")
    if raw is None:
        return None
    contract = {key: int(value) for key, value in raw.items()}
    required = {
        "minfloors", "maxfloors", "cellar_bands", "ground_bands",
        "repeat_source_band", "top_bands",
    }
    if set(contract) != required:
        raise ValueError(f"{slug}: repeatable contract must contain exactly {sorted(required)}")
    if contract["cellar_bands"] != 1 or contract["ground_bands"] != 1 or contract["top_bands"] != 1:
        raise ValueError(f"{slug}: converter currently requires exactly one cellar, ground and top band")
    top_band = floors - contract["top_bands"]
    if not (
        0 < contract["minfloors"] <= contract["maxfloors"]
        and contract["repeat_source_band"] == contract["cellar_bands"] + contract["ground_bands"]
        and contract["repeat_source_band"] < top_band
    ):
        raise ValueError(f"{slug}: repeatable contract does not fit {floors} authored bands")
    return contract


def normalized_band(
    blocks: dict[tuple[int, int, int], tuple[str, dict[str, Any] | None]],
    band: int,
) -> dict[tuple[int, int, int], tuple[str, dict[str, Any] | None]]:
    y0 = band * FLOOR_HEIGHT
    return {
        (x, y - y0, z): value
        for (x, y, z), value in blocks.items()
        if y0 <= y < y0 + FLOOR_HEIGHT
    }


def convert(entry: dict[str, Any]) -> dict[str, Any]:
    namespace, slug = entry["structure_id"].split(":", 1)
    if namespace != "infinite_domain":
        raise ValueError(f"unsupported output namespace {namespace}")
    size, blocks = load_structure(ROOT / entry["source_template"])
    blocks = {pos: stabilized_source_value(value) for pos, value in blocks.items()}
    sx, sy, sz = size
    dimx, dimz = math.ceil(sx / 16), math.ceil(sz / 16)
    floors = math.ceil(sy / FLOOR_HEIGHT)
    repeatable = repeatable_contract(entry, floors)
    if repeatable:
        repeat_band = repeatable["repeat_source_band"]
        top_band = floors - repeatable["top_bands"]
        authored_repeat = normalized_band(blocks, repeat_band)
        mismatched = [
            band for band in range(repeat_band + 1, top_band)
            if normalized_band(blocks, band) != authored_repeat
        ]
        if mismatched:
            raise ValueError(
                f"{slug}: bands {mismatched} differ from repeat source band {repeat_band}; "
                "repeatable conversion would discard authored geometry"
            )
        converted_bands = [0, 1, repeat_band, top_band]
    else:
        converted_bands = list(range(floors))
    building_grid: list[list[str]] = []
    part_count = 0
    palette_max = 0

    for chunk_x in range(dimx):
        building_column: list[str] = []
        for chunk_z in range(dimz):
            building_path = f"converted/{slug}_c{chunk_x:02d}_{chunk_z:02d}"
            building_id = f"infinite_domain:{building_path}"
            building_column.append(building_id)
            refs: list[dict[str, Any]] = []
            for floor in converted_bands:
                y1, y2 = floor * FLOOR_HEIGHT, min(sy, (floor + 1) * FLOOR_HEIGHT)
                band = {
                    (x - chunk_x * 16, y - y1, z - chunk_z * 16): value
                    for (x, y, z), value in blocks.items()
                    if chunk_x * 16 <= x < (chunk_x + 1) * 16
                    and chunk_z * 16 <= z < (chunk_z + 1) * 16
                    and y1 <= y < y2
                }
                mapping, palette = local_palette(list(band.values()))
                palette_max = max(palette_max, len(palette))
                slices: list[list[str]] = []
                for local_y in range(y2 - y1):
                    rows: list[str] = []
                    for local_z in range(16):
                        chars: list[str] = []
                        for local_x in range(16):
                            value = band.get((local_x, local_y, local_z))
                            if value is None:
                                chars.append(" ")
                            else:
                                block, tag = value
                                key = BlockValue(block, json.dumps(tag, sort_keys=True, separators=(",", ":")) if tag else "")
                                chars.append(mapping[key])
                        rows.append("".join(chars))
                    slices.append(rows)
                part_path = f"converted/{slug}_c{chunk_x:02d}_{chunk_z:02d}_f{floor:02d}"
                part_id = f"infinite_domain:{part_path}"
                part = {"xsize": 16, "zsize": 16, "slices": slices}
                if palette:
                    part["palette"] = {"palette": palette}
                write_json(ASSETS / "parts" / f"{part_path}.json", part)
                if repeatable:
                    if floor == 0:
                        refs.append({"cellar": True, "part": part_id})
                    elif floor == 1:
                        refs.append({"top": False, "ground": True, "cellar": False, "part": part_id})
                    elif floor == repeatable["repeat_source_band"]:
                        refs.append({"top": False, "ground": False, "cellar": False, "part": part_id})
                    else:
                        refs.append({"top": True, "part": part_id})
                else:
                    refs.append({"floor": floor, "part": part_id})
                part_count += 1
            building = {
                "filler": "#",
                "rubble": "}",
                "mincellars": repeatable["cellar_bands"] if repeatable else 0,
                "maxcellars": repeatable["cellar_bands"] if repeatable else 0,
                "minfloors": repeatable["minfloors"] if repeatable else floors,
                "maxfloors": repeatable["maxfloors"] if repeatable else floors,
                "parts": refs,
            }
            write_json(ASSETS / "buildings" / f"{building_path}.json", building)
        building_grid.append(building_column)

    multibuilding_path = f"converted/{slug}"
    multibuilding_id = f"infinite_domain:{multibuilding_path}"
    write_json(ASSETS / "multibuildings" / f"{multibuilding_path}.json", {"dimx": dimx, "dimz": dimz, "buildings": building_grid})

    scattered_id = None
    if entry["conversion_target"] == "scattered":
        scattered_path = f"converted/{slug}"
        scattered_id = f"infinite_domain:{scattered_path}"
        write_json(ASSETS / "scattered" / f"{scattered_path}.json", {
            "multibuilding": multibuilding_id,
            "rotatable": True,
            "terrainheight": "highest",
            "terrainfix": "repeatslice",
        })

    result = {
        "structure_id": entry["structure_id"],
        "source_role": entry["source_role"],
        "source_size": list(size),
        "road_facing": entry["main_entrance"],
        "chunk_footprint": [dimx, dimz],
        "floor_height": FLOOR_HEIGHT,
        "floor_bands": floors,
        "parts_written": part_count,
        "largest_local_palette": palette_max,
        "multibuilding": multibuilding_id,
        "scattered": scattered_id,
        "production_status": "converted",
        "runtime_codec_validation": "pending game launch",
    }
    if repeatable:
        result["repeatable_storey"] = {
            "cellar_band": 0,
            "ground_band": 1,
            "repeat_source_band": repeatable["repeat_source_band"],
            "top_band": floors - repeatable["top_bands"],
            "minfloors": repeatable["minfloors"],
            "maxfloors": repeatable["maxfloors"],
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("structure_id", nargs="*", help="one or more structure IDs; omit only with --all")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["structures"]
    wanted = set(args.structure_id)
    selected = catalog if args.all else [
        entry for entry in catalog
        if wanted & {entry["structure_id"], entry["structure_id"].split(":", 1)[1]}
    ]
    if not selected:
        raise SystemExit("No matching structure; supply an ID or --all")
    converted_now = [convert(entry) for entry in selected]
    # Targeted conversion is the normal review workflow. Preserve durable
    # evidence for structures converted by earlier runs instead of replacing
    # the report with only the latest selection.
    previous: dict[str, dict[str, Any]] = {}
    if REPORT.exists() and not args.all:
        previous = {
            entry["structure_id"]: entry
            for entry in json.loads(REPORT.read_text(encoding="utf-8")).get("structures", [])
        }
    previous.update({entry["structure_id"]: entry for entry in converted_now})
    catalog_order = {entry["structure_id"]: index for index, entry in enumerate(catalog)}
    results = sorted(
        previous.values(),
        key=lambda entry: catalog_order.get(entry["structure_id"], len(catalog_order)),
    )
    write_json(REPORT, {
        "purpose": "NBT-to-Lost-Cities conversion report. Conversion success is not production or visual approval.",
        "format": "16x16 local-palette parts, fixed six-block floor bands, per-cell buildings and multibuilding assembly",
        "structures": results,
    })
    print(
        f"Converted {len(converted_now)} structures into "
        f"{sum(result['parts_written'] for result in converted_now)} Lost Cities parts; "
        f"report tracks {len(results)} structures"
    )


if __name__ == "__main__":
    main()

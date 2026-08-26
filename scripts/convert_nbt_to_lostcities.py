from __future__ import annotations

import argparse
import gzip
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from build_structure_qa_world import NbtList, Reader, Tag


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
ASSETS = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities"
REPORT = ROOT / "docs" / "lostcities-conversion-report.json"
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
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


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


def convert(entry: dict[str, Any]) -> dict[str, Any]:
    namespace, slug = entry["structure_id"].split(":", 1)
    if namespace != "infinite_domain":
        raise ValueError(f"unsupported output namespace {namespace}")
    size, blocks = load_structure(ROOT / entry["source_template"])
    sx, sy, sz = size
    dimx, dimz = math.ceil(sx / 16), math.ceil(sz / 16)
    floors = math.ceil(sy / FLOOR_HEIGHT)
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
            for floor in range(floors):
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
                refs.append({"floor": floor, "part": part_id})
                part_count += 1
            building = {
                "filler": "#",
                "rubble": "}",
                "mincellars": 0,
                "maxcellars": 0,
                "minfloors": floors,
                "maxfloors": floors,
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

    return {
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("structure_id", nargs="?")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["structures"]
    selected = catalog if args.all else [entry for entry in catalog if args.structure_id in {entry["structure_id"], entry["structure_id"].split(":", 1)[1]}]
    if not selected:
        raise SystemExit("No matching structure; supply an ID or --all")
    results = [convert(entry) for entry in selected]
    write_json(REPORT, {
        "purpose": "NBT-to-Lost-Cities conversion report. Conversion success is not production or visual approval.",
        "format": "16x16 local-palette parts, fixed six-block floor bands, per-cell buildings and multibuilding assembly",
        "structures": results,
    })
    print(f"Converted {len(results)} structures into {sum(result['parts_written'] for result in results)} Lost Cities parts")


if __name__ == "__main__":
    main()

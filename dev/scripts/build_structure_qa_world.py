from __future__ import annotations

import csv
import gzip
import io
import json
import math
import re
import struct
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_LEVEL = ROOT / "saves" / "New World Charlie" / "level.dat"
WORLD_NAME = "Infinite Domain - Structure QA Flatworld"
WORLD = ROOT / "saves" / WORLD_NAME
PACK_NAME = "Infinite_Domain_QA_Gallery"
PACK = WORLD / "datapacks" / PACK_NAME
FUNCTIONS = PACK / "data" / "infinite_domain_qa" / "function"
BLOCK_CONFIG = ROOT / "config" / "submarine_hull.json"
MANIFEST = ROOT / "dev/docs" / "wasteland-site-manifest.json"
ROAD_CATALOG = ROOT / "dev/structure_library" / "roads" / "road-modules.json"
MODULE_CATALOG = ROOT / "dev/structure_library" / "modules" / "structure-kits.json"
RESOURCE_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
VANILLA_DATA_JAR_CANDIDATES = (
    Path.home() / "curseforge" / "minecraft" / "Install" / "versions" / "1.21.1" / "1.21.1.jar",
    Path.home() / "curseforge" / "minecraft" / "Install" / "libraries" / "net" / "minecraft" / "client" / "1.21.1" / "client-1.21.1-official.jar",
)
LOOSE_DATA_ROOTS = (
    ROOT / "kubejs",
    ROOT / "datapacks",
    ROOT / "dynamic-data-pack-cache",
    ROOT / "moonlight-global-datapacks",
    ROOT / "dev/packdev",
    ROOT / "data",
)

CATEGORY_ORDER = (
    "ores",
    "metals_and_raw_materials",
    "terrain_and_stone",
    "wood_and_construction",
    "glass_and_translucent",
    "machines_and_workstations",
    "storage",
    "transport_pipes_and_cables",
    "plants_and_agriculture",
    "lighting",
    "redstone_and_technical",
    "decorative",
    "miscellaneous",
)


@dataclass(frozen=True)
class BlockSample:
    block_id: str
    namespace: str
    path: str
    category: str
    is_fluid: bool = False


@dataclass(frozen=True)
class PlaceableContent:
    resource_id: str
    kind: str
    sources: tuple[str, ...]


@dataclass
class NbtList:
    element_type: int
    values: list["Tag"]


@dataclass
class Tag:
    kind: int
    value: Any


class Reader:
    def __init__(self, raw: bytes):
        self.stream = io.BytesIO(raw)

    def unpack(self, fmt: str) -> Any:
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError("Unexpected end of NBT data")
        return struct.unpack(fmt, data)[0]

    def string(self) -> str:
        return self.stream.read(self.unpack(">H")).decode("utf-8")

    def tag(self, kind: int) -> Tag:
        if kind == 1:
            return Tag(kind, self.unpack(">b"))
        if kind == 2:
            return Tag(kind, self.unpack(">h"))
        if kind == 3:
            return Tag(kind, self.unpack(">i"))
        if kind == 4:
            return Tag(kind, self.unpack(">q"))
        if kind == 5:
            return Tag(kind, self.unpack(">f"))
        if kind == 6:
            return Tag(kind, self.unpack(">d"))
        if kind == 7:
            return Tag(kind, self.stream.read(self.unpack(">i")))
        if kind == 8:
            return Tag(kind, self.string())
        if kind == 9:
            element_type = self.unpack(">B")
            length = self.unpack(">i")
            return Tag(kind, NbtList(element_type, [self.tag(element_type) for _ in range(length)]))
        if kind == 10:
            children: dict[str, Tag] = {}
            while True:
                child_kind = self.unpack(">B")
                if child_kind == 0:
                    return Tag(kind, children)
                child_name = self.string()
                children[child_name] = self.tag(child_kind)
        if kind == 11:
            return Tag(kind, [self.unpack(">i") for _ in range(self.unpack(">i"))])
        if kind == 12:
            return Tag(kind, [self.unpack(">q") for _ in range(self.unpack(">i"))])
        raise ValueError(f"Unsupported NBT tag type {kind}")

    def root(self) -> tuple[str, Tag]:
        kind = self.unpack(">B")
        if kind != 10:
            raise ValueError("level.dat does not have a compound root")
        return self.string(), self.tag(kind)


def utf(value: str) -> bytes:
    raw = value.encode("utf-8")
    return struct.pack(">H", len(raw)) + raw


def payload(tag: Tag) -> bytes:
    kind, value = tag.kind, tag.value
    if kind == 1:
        return struct.pack(">b", value)
    if kind == 2:
        return struct.pack(">h", value)
    if kind == 3:
        return struct.pack(">i", value)
    if kind == 4:
        return struct.pack(">q", value)
    if kind == 5:
        return struct.pack(">f", value)
    if kind == 6:
        return struct.pack(">d", value)
    if kind == 7:
        return struct.pack(">i", len(value)) + value
    if kind == 8:
        return utf(value)
    if kind == 9:
        return bytes([value.element_type]) + struct.pack(">i", len(value.values)) + b"".join(payload(child) for child in value.values)
    if kind == 10:
        body = bytearray()
        for name, child in value.items():
            body.append(child.kind)
            body.extend(utf(name))
            body.extend(payload(child))
        body.append(0)
        return bytes(body)
    if kind == 11:
        return struct.pack(">i", len(value)) + b"".join(struct.pack(">i", item) for item in value)
    if kind == 12:
        return struct.pack(">i", len(value)) + b"".join(struct.pack(">q", item) for item in value)
    raise ValueError(kind)


def compound(**values: Tag) -> Tag:
    return Tag(10, values)


def string(value: str) -> Tag:
    return Tag(8, value)


def integer(value: int) -> Tag:
    return Tag(3, value)


def byte(value: int | bool) -> Tag:
    return Tag(1, int(value))


def strings(values: list[str]) -> Tag:
    return Tag(9, NbtList(8, [string(value) for value in values]))


def compounds(values: list[Tag]) -> Tag:
    return Tag(9, NbtList(10, values))


def empty_list() -> Tag:
    return Tag(9, NbtList(0, []))


def write_level_dat() -> None:
    if not SOURCE_LEVEL.exists():
        raise FileNotFoundError(f"World template level.dat not found: {SOURCE_LEVEL}")
    raw = gzip.decompress(SOURCE_LEVEL.read_bytes())
    root_name, root = Reader(raw).root()
    data = root.value["Data"].value
    data["LevelName"] = string(WORLD_NAME)
    data["GameType"] = integer(1)
    data["allowCommands"] = byte(1)
    data["hardcore"] = byte(0)
    data["Difficulty"] = byte(0)
    data["DifficultyLocked"] = byte(0)
    data["SpawnX"] = integer(0)
    data["SpawnY"] = integer(5)
    data["SpawnZ"] = integer(0)
    data["SpawnAngle"] = Tag(5, 180.0)
    data["LastPlayed"] = Tag(4, int(time.time() * 1000))
    data["Time"] = Tag(4, 6000)
    data["DayTime"] = Tag(4, 6000)
    data["clearWeatherTime"] = integer(2_000_000_000)
    data["rainTime"] = integer(0)
    data["raining"] = byte(0)
    data["thunderTime"] = integer(0)
    data["thundering"] = byte(0)
    data.pop("Player", None)

    rules = data.setdefault("GameRules", compound()).value
    for name, value in {
        "commandBlockOutput": "false",
        "doDaylightCycle": "false",
        "doFireTick": "false",
        "doMobSpawning": "false",
        "doPatrolSpawning": "false",
        "doTraderSpawning": "false",
        "doWeatherCycle": "false",
        "keepInventory": "true",
        "mobGriefing": "false",
        "randomTickSpeed": "0",
        "sendCommandFeedback": "true",
    }.items():
        rules[name] = string(value)

    worldgen = data["WorldGenSettings"].value
    dimensions = worldgen["dimensions"].value
    overworld = dimensions["minecraft:overworld"].value
    overworld["type"] = string("minecraft:overworld")
    overworld["generator"] = compound(
        type=string("minecraft:flat"),
        settings=compound(
            biome=string("minecraft:plains"),
            lakes=byte(0),
            features=byte(0),
            layers=compounds([
                compound(block=string("minecraft:bedrock"), height=integer(1)),
                compound(block=string("minecraft:deepslate"), height=integer(31)),
                compound(block=string("minecraft:stone"), height=integer(32)),
                compound(block=string("minecraft:dirt"), height=integer(3)),
                compound(block=string("minecraft:grass_block"), height=integer(1)),
            ]),
            structure_overrides=empty_list(),
        ),
    )

    datapacks = data.setdefault("DataPacks", compound(Enabled=strings(["vanilla"]), Disabled=strings([]))).value
    enabled = datapacks.setdefault("Enabled", strings(["vanilla"])).value.values
    pack_id = f"file/{PACK_NAME}"
    # Do not inherit save-local datapacks from the template world. Mod-provided
    # dynamic packs remain enabled, while only this save's own file pack is kept.
    enabled[:] = [entry for entry in enabled if not entry.value.startswith("file/")]
    enabled_values = [entry.value for entry in enabled]
    if pack_id not in enabled_values:
        enabled.append(string(pack_id))
    disabled = datapacks.setdefault("Disabled", strings([])).value.values
    datapacks["Disabled"].value.values = [entry for entry in disabled if entry.value != pack_id]

    encoded = bytes([10]) + utf(root_name) + payload(root)
    WORLD.mkdir(parents=True, exist_ok=False)
    (WORLD / "level.dat").write_bytes(gzip.compress(encoded, mtime=0))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def function(path: str, commands: list[str]) -> None:
    write_text(FUNCTIONS / f"{path}.mcfunction", "\n".join(commands))


def sign_command(x: int, y: int, z: int, lines: list[str], rotation: int = 8) -> str:
    messages = lines[:4] + [""] * (4 - len(lines))
    encoded = [json.dumps({"text": message, "color": "white"}, separators=(",", ":")) for message in messages]
    snbt_messages = ",".join("'" + message.replace("'", "\\'") + "'" for message in encoded)
    return f"setblock {x} {y} {z} minecraft:oak_sign[rotation={rotation}]{{front_text:{{messages:[{snbt_messages}],color:\"white\",has_glowing_text:1b}}}} replace"


def command_block(x: int, y: int, z: int, command: str, name: str) -> list[str]:
    custom_name = json.dumps({"text": name}, separators=(",", ":"))
    return [
        f"setblock {x} {y} {z} minecraft:command_block[facing=up]{{Command:\"{command}\",CustomName:'{custom_name}',TrackOutput:0b,auto:0b}} replace",
        f"setblock {x} {y + 1} {z} minecraft:stone_button[face=floor,facing=north,powered=false] replace",
    ]


def structure_names() -> list[str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(manifest["structures"])


def road_names() -> list[str]:
    catalog = json.loads(ROAD_CATALOG.read_text(encoding="utf-8"))
    return [record["module_id"].split(":", 1)[1] for record in catalog["modules"]]


def module_names() -> list[str]:
    catalog = json.loads(MODULE_CATALOG.read_text(encoding="utf-8"))
    return [record["module_id"].split(":", 1)[1] for record in catalog["modules"]]


def _classify_data_resource(path: str) -> tuple[str, str] | None:
    """Convert a data-pack path to a directly placeable registry/template id."""
    normalized = path.replace("\\", "/").lstrip("./")
    match = re.search(
        r"(?:^|/)data/([a-z0-9_.-]+)/(structure|structures|worldgen/structure|worldgen/configured_feature)/(.+?)\.(nbt|json)$",
        normalized,
    )
    if not match:
        return None
    namespace, folder, resource_path, extension = match.groups()
    if folder in {"structure", "structures"} and extension == "nbt":
        kind = "template"
    elif folder == "worldgen/structure" and extension == "json":
        kind = "worldgen_structure"
    elif folder == "worldgen/configured_feature" and extension == "json":
        kind = "configured_feature"
    else:
        return None
    resource_id = f"{namespace}:{resource_path}"
    if not RESOURCE_ID.fullmatch(resource_id):
        return None
    return kind, resource_id


def placeable_content() -> list[PlaceableContent]:
    """Inventory every data-driven object accepted by a /place subcommand.

    The vanilla client jar supplies Minecraft's built-in data pack, mod jars
    supply their embedded packs, and the loose roots cover this instance's
    KubeJS/generated/global data packs. Duplicate resource ids intentionally
    collapse to the effective registry key while retaining all source labels
    in the CSV inventory.
    """
    found: dict[tuple[str, str], set[str]] = {}

    def record(path: str, source: str) -> None:
        classified = _classify_data_resource(path)
        if classified:
            found.setdefault(classified, set()).add(source)

    archive_paths: set[Path] = set((ROOT / "mods").glob("*.jar"))
    archive_paths.update(candidate for candidate in VANILLA_DATA_JAR_CANDIDATES if candidate.is_file())
    for root in LOOSE_DATA_ROOTS:
        if root.is_dir():
            archive_paths.update(root.rglob("*.zip"))
            archive_paths.update(root.rglob("*.jar"))

    for archive_path in sorted(archive_paths, key=lambda item: item.as_posix().lower()):
        try:
            with zipfile.ZipFile(archive_path) as archive:
                source = archive_path.name
                for name in archive.namelist():
                    record(name, source)
        except (OSError, zipfile.BadZipFile):
            continue

    for root in LOOSE_DATA_ROOTS:
        if not root.is_dir():
            continue
        for candidate in root.rglob("*"):
            if candidate.is_file() and candidate.suffix.lower() in {".nbt", ".json"}:
                record(candidate.as_posix(), candidate.relative_to(ROOT).as_posix())

    order = {"template": 0, "worldgen_structure": 1, "configured_feature": 2}
    return [
        PlaceableContent(resource_id, kind, tuple(sorted(sources)))
        for (kind, resource_id), sources in sorted(found.items(), key=lambda item: (order[item[0][0]], item[0][1]))
    ]


def tagged_fluids() -> set[str]:
    """Read fluid tag values from every installed mod instead of guessing only by name."""
    result = {"minecraft:water", "minecraft:lava"}

    def values(node: Any) -> list[str]:
        found: list[str] = []
        if isinstance(node, str):
            found.append(node.lstrip("#"))
        elif isinstance(node, list):
            for item in node:
                found.extend(values(item))
        elif isinstance(node, dict):
            if "id" in node:
                found.extend(values(node["id"]))
        return found

    for jar in sorted((ROOT / "mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    normalized = name.replace("\\", "/")
                    if not re.fullmatch(r"data/[^/]+/tags/fluids?/.+\.json", normalized):
                        continue
                    try:
                        document = json.loads(archive.read(name))
                    except (KeyError, json.JSONDecodeError, UnicodeDecodeError):
                        continue
                    result.update(value for value in values(document.get("values", [])) if RESOURCE_ID.fullmatch(value))
        except (OSError, zipfile.BadZipFile):
            continue
    return result


def classify_block(path: str) -> str:
    tokens = set(path.split("_"))
    if path.endswith("_ore") or "_ore_" in path or path.startswith("ore_"):
        return "ores"
    if ("block" in tokens and tokens & {"iron", "gold", "copper", "steel", "lead", "tin", "silver", "nickel", "uranium", "bronze", "brass"}) or path.startswith("raw_") or "ingot" in tokens:
        return "metals_and_raw_materials"
    if tokens & {"stone", "dirt", "sand", "gravel", "deepslate", "netherrack", "basalt", "terracotta", "concrete", "mud", "clay", "soil", "rock"}:
        return "terrain_and_stone"
    if tokens & {"log", "wood", "planks", "slab", "stairs", "fence", "door", "trapdoor", "wall", "brick", "roof", "shingle"}:
        return "wood_and_construction"
    if tokens & {"glass", "pane", "ice", "crystal", "transparent"}:
        return "glass_and_translucent"
    if tokens & {"machine", "generator", "furnace", "crusher", "press", "mill", "assembler", "reactor", "turbine", "workbench", "station", "terminal"}:
        return "machines_and_workstations"
    if tokens & {"chest", "barrel", "crate", "cabinet", "cupboard", "drawer", "shelf", "tank", "storage"}:
        return "storage"
    if tokens & {"pipe", "cable", "wire", "conveyor", "rail", "track", "road", "asphalt", "duct", "tube"}:
        return "transport_pipes_and_cables"
    if tokens & {"leaves", "sapling", "flower", "crop", "seed", "grass", "bush", "vine", "mushroom", "plant", "farmland"}:
        return "plants_and_agriculture"
    if tokens & {"lamp", "light", "lantern", "torch", "bulb", "neon"}:
        return "lighting"
    if tokens & {"redstone", "sensor", "detector", "switch", "button", "lever", "computer", "controller", "technical"}:
        return "redstone_and_technical"
    if tokens & {"chair", "table", "desk", "sofa", "bed", "carpet", "curtain", "painting", "poster", "decoration", "decorative", "trim"}:
        return "decorative"
    return "miscellaneous"


def block_samples() -> list[BlockSample]:
    config = json.loads(BLOCK_CONFIG.read_text(encoding="utf-8"))
    names = {name for name in config if not name.startswith("_") and RESOURCE_ID.fullmatch(name)}
    fluids = tagged_fluids()
    samples: list[BlockSample] = []
    for name in names:
        namespace, path = name.split(":", 1)
        is_fluid = name in fluids
        samples.append(BlockSample(name, namespace, path, "fluids" if is_fluid else classify_block(path), is_fluid))
    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    return sorted(samples, key=lambda sample: (sample.namespace != "minecraft", sample.namespace, order.get(sample.category, 99), sample.path))


def build_datapack(
    structures: list[str],
    roads: list[str],
    modules: list[str],
    blocks: list[BlockSample],
    content: list[PlaceableContent],
) -> None:
    write_text(PACK / "pack.mcmeta", json.dumps({"pack": {"pack_format": 48, "description": "Infinite Domain structure and block QA gallery"}}, indent=2))
    write_text(PACK / "data" / "minecraft" / "tags" / "function" / "load.json", json.dumps({"values": ["infinite_domain_qa:load"]}, indent=2))

    load = [
        "execute unless data storage infinite_domain_qa:state built run function infinite_domain_qa:build_hub",
    ]
    function("load", load)

    hub: list[str] = [
        "data modify storage infinite_domain_qa:state built set value 1b",
        "gamerule doDaylightCycle false",
        "gamerule doWeatherCycle false",
        "gamerule doMobSpawning false",
        "gamerule doFireTick false",
        "gamerule randomTickSpeed 0",
        "gamerule commandBlockOutput false",
        "difficulty peaceful",
        "scoreboard objectives add id_qa dummy",
        "scoreboard players set #rotation_cursor id_qa 0",
        "scoreboard players set #road_rotation_cursor id_qa 0",
        "scoreboard players set #module_rotation_cursor id_qa 0",
        "time set noon",
        "weather clear 1000000",
        "setworldspawn 0 5 0",
        "fill -240 4 -66 160 4 18 minecraft:smooth_stone replace",
        sign_command(-4, 5, 3, ["INFINITE DOMAIN", "QA FLATWORLD", "NORTH: STRUCTURES", "SOUTH: BLOCKS"], 0),
        sign_command(4, 5, 3, ["PRESS A BUTTON", "TO BUILD + VISIT", "96x96 TEST CELLS", "CREATIVE MODE"], 0),
        sign_command(60, 5, 3, ["ROAD MODULES", "EAST CONTROLS", "48x48 TEST CELLS", "CONDITION SETS"], 0),
        sign_command(-60, 5, 3, ["STRUCTURE KITS", "WEST CONTROLS", "PORT / MARKET", "INDUSTRIAL"], 0),
    ]

    for index, name in enumerate(structures):
        control_col, control_row = index % 12, index // 12
        control_x = -44 + control_col * 8
        control_z = -4 - control_row * 9
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = (gallery_col - 3) * 96
        cell_z = -160 - gallery_row * 96
        place_x, place_z = cell_x + 20, cell_z + 20
        place_y = -12 if name == "bunker_network" else (-4 if name == "survivor_cache" else (-2 if name == "ruined_gas_station" else 5))
        hub.extend(command_block(control_x, 5, control_z, f"function infinite_domain_qa:structure/{name}", name))
        label = name.replace("_", " ")
        hub.append(sign_command(control_x, 5, control_z + 2, [label[:15], label[15:30], "BUILD + VISIT", f"CELL {index + 1:02d}"], 8))
        cx1, cz1 = cell_x // 16, cell_z // 16
        cx2, cz2 = (cell_x + 80) // 16, (cell_z + 80) // 16
        structure_commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 80} {cell_z + 80}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 80} 4 {cell_z + 80} minecraft:smooth_stone replace minecraft:grass_block",
            f"place template infinite_domain:wasteland/{name} {place_x} {place_y} {place_z}",
            sign_command(cell_x + 5, 5, cell_z + 5, [label[:15], label[15:30], f"CELL {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"tp @p {cell_x + 10} 12 {cell_z + 10} facing {place_x + 24} 12 {place_z + 24}",
            f"forceload remove {cell_x} {cell_z} {cell_x + 80} {cell_z + 80}",
        ]
        function(f"structure/{name}", structure_commands)

    # Optional sequential full-gallery build. Each step loads only one review
    # cell, places its structure, unloads the cell, then schedules the next.
    function("structure_all/start", [
        "execute if data storage infinite_domain_qa:state structure_gallery_built run tellraw @p {\"text\":\"North structure gallery was already built. Individual buttons still rebuild cells.\",\"color\":\"yellow\"}",
        "execute unless data storage infinite_domain_qa:state structure_gallery_built run data modify storage infinite_domain_qa:state structure_gallery_built set value 1b",
        "execute unless data storage infinite_domain_qa:state structure_gallery_scheduled run schedule function infinite_domain_qa:structure_all/batch_000 1t replace",
        "data modify storage infinite_domain_qa:state structure_gallery_scheduled set value 1b",
        f"tellraw @p {{\"text\":\"Building {len(structures)} north gallery cells in sequence...\",\"color\":\"green\"}}",
    ])
    for index, name in enumerate(structures):
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = (gallery_col - 3) * 96
        cell_z = -160 - gallery_row * 96
        place_x, place_z = cell_x + 20, cell_z + 20
        place_y = -12 if name == "bunker_network" else (-4 if name == "survivor_cache" else (-2 if name == "ruined_gas_station" else 5))
        label = name.replace("_", " ")
        commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 80} {cell_z + 80}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 80} 4 {cell_z + 80} minecraft:smooth_stone replace minecraft:grass_block",
            f"place template infinite_domain:wasteland/{name} {place_x} {place_y} {place_z}",
            sign_command(cell_x + 5, 5, cell_z + 5, [label[:15], label[15:30], f"CELL {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"forceload remove {cell_x} {cell_z} {cell_x + 80} {cell_z + 80}",
        ]
        if index + 1 < len(structures):
            commands.append(f"schedule function infinite_domain_qa:structure_all/batch_{index + 1:03d} 3t replace")
        else:
            commands.append(f"tellraw @a {{\"text\":\"North structure gallery complete: {len(structures)} structures.\",\"color\":\"green\"}}")
        function(f"structure_all/batch_{index:03d}", commands)

    for index, name in enumerate(roads):
        control_col, control_row = index % 12, index // 12
        control_x = 64 + control_col * 8
        control_z = -4 - control_row * 9
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = 600 + gallery_col * 48
        cell_z = -160 - gallery_row * 48
        place_x, place_z = cell_x + 7, cell_z + 7
        label = name.replace("_", " ")
        hub.extend(command_block(control_x, 5, control_z, f"function infinite_domain_qa:road/{name}", name))
        hub.append(sign_command(control_x, 5, control_z + 2, [label[:15], label[15:30], "ROAD BUILD", f"CELL {index + 1:02d}"], 8))
        road_commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 47} 4 {cell_z + 47} minecraft:grass_block replace",
            f"place template infinite_domain:wasteland/road_modules/{name} {place_x} 5 {place_z}",
            sign_command(cell_x + 3, 5, cell_z + 3, [label[:15], label[15:30], f"ROAD {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"tp @p {cell_x + 4} 13 {cell_z + 4} facing {place_x + 16} 7 {place_z + 16}",
            f"forceload remove {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
        ]
        function(f"road/{name}", road_commands)

    function("road_all/start", [
        "execute if data storage infinite_domain_qa:state road_gallery_built run tellraw @p {\"text\":\"East road gallery was already built. Individual buttons still rebuild cells.\",\"color\":\"yellow\"}",
        "execute unless data storage infinite_domain_qa:state road_gallery_built run data modify storage infinite_domain_qa:state road_gallery_built set value 1b",
        "execute unless data storage infinite_domain_qa:state road_gallery_scheduled run schedule function infinite_domain_qa:road_all/batch_000 1t replace",
        "data modify storage infinite_domain_qa:state road_gallery_scheduled set value 1b",
        f"tellraw @p {{\"text\":\"Building {len(roads)} east road-module cells in sequence...\",\"color\":\"green\"}}",
    ])
    for index, name in enumerate(roads):
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = 600 + gallery_col * 48
        cell_z = -160 - gallery_row * 48
        place_x, place_z = cell_x + 7, cell_z + 7
        label = name.replace("_", " ")
        commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 47} 4 {cell_z + 47} minecraft:grass_block replace",
            f"place template infinite_domain:wasteland/road_modules/{name} {place_x} 5 {place_z}",
            sign_command(cell_x + 3, 5, cell_z + 3, [label[:15], label[15:30], f"ROAD {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"forceload remove {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
        ]
        if index + 1 < len(roads):
            commands.append(f"schedule function infinite_domain_qa:road_all/batch_{index + 1:03d} 2t replace")
        else:
            commands.append(f"tellraw @a {{\"text\":\"East road gallery complete: {len(roads)} road modules.\",\"color\":\"green\"}}")
        function(f"road_all/batch_{index:03d}", commands)

    for index, name in enumerate(modules):
        control_col, control_row = index % 12, index // 12
        control_x = -220 + control_col * 8
        control_z = -4 - control_row * 9
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = -936 + gallery_col * 48
        cell_z = -160 - gallery_row * 48
        place_x, place_z = cell_x + 7, cell_z + 7
        label = name.replace("_", " ")
        hub.extend(command_block(control_x, 5, control_z, f"function infinite_domain_qa:module/{name}", name))
        hub.append(sign_command(control_x, 5, control_z + 2, [label[:15], label[15:30], "MODULE BUILD", f"CELL {index + 1:02d}"], 8))
        module_commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 47} 4 {cell_z + 47} minecraft:grass_block replace",
            f"place template infinite_domain:wasteland/modules/{name} {place_x} 5 {place_z}",
            sign_command(cell_x + 3, 5, cell_z + 3, [label[:15], label[15:30], f"MODULE {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"tp @p {cell_x + 4} 14 {cell_z + 4} facing {place_x + 16} 7 {place_z + 16}",
            f"forceload remove {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
        ]
        function(f"module/{name}", module_commands)

    function("module_all/start", [
        "execute if data storage infinite_domain_qa:state module_gallery_built run tellraw @p {\"text\":\"West module gallery was already built. Individual buttons still rebuild cells.\",\"color\":\"yellow\"}",
        "execute unless data storage infinite_domain_qa:state module_gallery_built run data modify storage infinite_domain_qa:state module_gallery_built set value 1b",
        "execute unless data storage infinite_domain_qa:state module_gallery_scheduled run schedule function infinite_domain_qa:module_all/batch_000 1t replace",
        "data modify storage infinite_domain_qa:state module_gallery_scheduled set value 1b",
        f"tellraw @p {{\"text\":\"Building {len(modules)} west structure-kit cells in sequence...\",\"color\":\"green\"}}",
    ])
    for index, name in enumerate(modules):
        gallery_col, gallery_row = index % 7, index // 7
        cell_x = -936 + gallery_col * 48
        cell_z = -160 - gallery_row * 48
        place_x, place_z = cell_x + 7, cell_z + 7
        label = name.replace("_", " ")
        commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 47} 4 {cell_z + 47} minecraft:grass_block replace",
            f"place template infinite_domain:wasteland/modules/{name} {place_x} 5 {place_z}",
            sign_command(cell_x + 3, 5, cell_z + 3, [label[:15], label[15:30], f"MODULE {index + 1:02d}", "HUB: /tp 0 8 0"], 0),
            f"forceload remove {cell_x} {cell_z} {cell_x + 47} {cell_z + 47}",
        ]
        if index + 1 < len(modules):
            commands.append(f"schedule function infinite_domain_qa:module_all/batch_{index + 1:03d} 2t replace")
        else:
            commands.append(f"tellraw @a {{\"text\":\"West module gallery complete: {len(modules)} reusable modules.\",\"color\":\"green\"}}")
        function(f"module_all/batch_{index:03d}", commands)

    # Incremental four-way rotation gallery. Each press advances to one
    # authoritative structure and builds four orientations in a dedicated
    # 192x192 cell. Unique cells avoid destructive clearing and preserve every
    # reviewed result until the QA world itself is regenerated.
    rotation_dispatch = []
    rotations = ("none", "clockwise_90", "180", "counterclockwise_90")
    for index, name in enumerate(structures):
        cell_col, cell_row = index % 5, index // 5
        cell_x = -384 + cell_col * 192
        cell_z = -1600 - cell_row * 192
        place_y = -12 if name == "bunker_network" else (-4 if name == "survivor_cache" else (-2 if name == "ruined_gas_station" else 5))
        origins = (
            (cell_x + 5, cell_z + 5),
            (cell_x + 187, cell_z + 5),
            (cell_x + 187, cell_z + 187),
            (cell_x + 5, cell_z + 187),
        )
        sign_positions = (
            (cell_x + 2, cell_z + 2),
            (cell_x + 189, cell_z + 2),
            (cell_x + 189, cell_z + 189),
            (cell_x + 2, cell_z + 189),
        )
        label = name.replace("_", " ")
        commands = [
            f"forceload add {cell_x} {cell_z} {cell_x + 191} {cell_z + 191}",
            f"fill {cell_x} 4 {cell_z} {cell_x + 95} 4 {cell_z + 191} minecraft:smooth_stone replace minecraft:grass_block",
            f"fill {cell_x + 96} 4 {cell_z} {cell_x + 191} 4 {cell_z + 191} minecraft:smooth_stone replace minecraft:grass_block",
        ]
        for rotation, (origin_x, origin_z), (sign_x, sign_z), caption in zip(rotations, origins, sign_positions, ("NORTH / 0", "EAST / 90", "SOUTH / 180", "WEST / 270")):
            commands.append(f"place template infinite_domain:wasteland/{name} {origin_x} {place_y} {origin_z} {rotation} none 1.0 0")
            commands.append(sign_command(sign_x, 5, sign_z, [label[:15], label[15:30], caption, f"TEST {index + 1:02d}/{len(structures):02d}"], 0))
        commands.extend([
            f"tp @p {cell_x + 96} 90 {cell_z + 96}",
            f"tellraw @p {{\"text\":\"Rotation test {index + 1}/{len(structures)}: {name}. Inspect doors, stairs, rails, block facing and lot fit in all four quadrants.\",\"color\":\"aqua\"}}",
            f"forceload remove {cell_x} {cell_z} {cell_x + 191} {cell_z + 191}",
        ])
        function(f"rotation/{name}", commands)
        rotation_dispatch.append(f"execute if score #rotation_cursor id_qa matches {index} run function infinite_domain_qa:rotation/{name}")
    function("rotation/next", [
        *rotation_dispatch,
        "scoreboard players add #rotation_cursor id_qa 1",
        f"execute if score #rotation_cursor id_qa matches {len(structures)}.. run scoreboard players set #rotation_cursor id_qa 0",
    ])
    function("rotation/reset", [
        "scoreboard players set #rotation_cursor id_qa 0",
        f"tellraw @p {{\"text\":\"Structure rotation review reset to test 1/{len(structures)}.\",\"color\":\"yellow\"}}",
    ])

    def compact_rotation_harness(names: list[str], resource_root: str, folder: str, cursor: str, base_x: int, base_z: int, columns: int, noun: str) -> None:
        dispatch = []
        rotations = ("none", "clockwise_90", "180", "counterclockwise_90")
        for index, name in enumerate(names):
            cell_x = base_x + (index % columns) * 96
            cell_z = base_z - (index // columns) * 96
            origins = (
                (cell_x + 5, cell_z + 5),
                (cell_x + 91, cell_z + 5),
                (cell_x + 91, cell_z + 91),
                (cell_x + 5, cell_z + 91),
            )
            sign_positions = (
                (cell_x + 2, cell_z + 2),
                (cell_x + 93, cell_z + 2),
                (cell_x + 93, cell_z + 93),
                (cell_x + 2, cell_z + 93),
            )
            label = name.replace("_", " ")
            commands = [
                f"forceload add {cell_x} {cell_z} {cell_x + 95} {cell_z + 95}",
                f"fill {cell_x} 4 {cell_z} {cell_x + 95} 4 {cell_z + 95} minecraft:smooth_stone replace minecraft:grass_block",
            ]
            for rotation, (origin_x, origin_z), (sign_x, sign_z), caption in zip(rotations, origins, sign_positions, ("0 DEG", "90 DEG", "180 DEG", "270 DEG")):
                commands.append(f"place template {resource_root}/{name} {origin_x} 5 {origin_z} {rotation} none 1.0 0")
                commands.append(sign_command(sign_x, 5, sign_z, [label[:15], label[15:30], caption, f"TEST {index + 1:02d}/{len(names):02d}"], 0))
            commands.extend([
                f"tp @p {cell_x + 48} 55 {cell_z + 48}",
                f"tellraw @p {{\"text\":\"{noun} rotation test {index + 1}/{len(names)}: {name}. Inspect boundary alignment, directional states and connector faces.\",\"color\":\"aqua\"}}",
                f"forceload remove {cell_x} {cell_z} {cell_x + 95} {cell_z + 95}",
            ])
            function(f"{folder}/{name}", commands)
            dispatch.append(f"execute if score {cursor} id_qa matches {index} run function infinite_domain_qa:{folder}/{name}")
        function(f"{folder}/next", [
            *dispatch,
            f"scoreboard players add {cursor} id_qa 1",
            f"execute if score {cursor} id_qa matches {len(names)}.. run scoreboard players set {cursor} id_qa 0",
        ])
        function(f"{folder}/reset", [
            f"scoreboard players set {cursor} id_qa 0",
            f"tellraw @p {{\"text\":\"{noun} rotation review reset to test 1/{len(names)}.\",\"color\":\"yellow\"}}",
        ])

    clean_roads = [name for name in roads if name.endswith("__clean")]
    compact_rotation_harness(clean_roads, "infinite_domain:wasteland/road_modules", "road_rotation", "#road_rotation_cursor", 1400, -1600, 3, "Road")
    compact_rotation_harness(modules, "infinite_domain:wasteland/modules", "module_rotation", "#module_rotation_cursor", -1800, -1600, 4, "Structure module")

    hub.extend(command_block(-24, 5, 11, "function infinite_domain_qa:structure_all/start", "Build all north structures"))
    hub.append(sign_command(-24, 5, 13, ["BUILD ALL NORTH", f"{len(structures)} STRUCTURES", "SEQUENTIAL", "SAFE CHUNK LOAD"], 0))
    hub.extend(command_block(24, 5, 11, "function infinite_domain_qa:road_all/start", "Build all east road modules"))
    hub.append(sign_command(24, 5, 13, ["BUILD ALL EAST", f"{len(roads)} ROAD MODULES", "12 TOPOLOGIES", "7 CONDITIONS"], 0))
    hub.extend(command_block(40, 5, 11, "function infinite_domain_qa:module_all/start", "Build all west structure modules"))
    hub.append(sign_command(40, 5, 13, ["BUILD ALL WEST", f"{len(modules)} MODULES", "PORT + MARKET", "INDUSTRIAL"], 0))
    hub.extend(command_block(56, 5, 11, "function infinite_domain_qa:rotation/next", "Build next four-way rotation test"))
    hub.append(sign_command(56, 5, 13, ["NEXT ROTATION", "ONE STRUCTURE", "FOUR DIRECTIONS", f"{len(structures)}-STEP CYCLE"], 0))
    hub.extend(command_block(72, 5, 11, "function infinite_domain_qa:rotation/reset", "Reset rotation test cycle"))
    hub.append(sign_command(72, 5, 13, ["RESET ROTATION", f"RETURNS TO 1/{len(structures)}", "DOES NOT DELETE", "BUILT TESTS"], 0))
    hub.extend(command_block(88, 5, 11, "function infinite_domain_qa:road_rotation/next", "Build next road rotation test"))
    hub.append(sign_command(88, 5, 13, ["NEXT ROAD TEST", f"{len(clean_roads)} TOPOLOGIES", "FOUR DIRECTIONS", "EAST RANGE"], 0))
    hub.extend(command_block(104, 5, 11, "function infinite_domain_qa:road_rotation/reset", "Reset road rotation cycle"))
    hub.append(sign_command(104, 5, 13, ["RESET ROAD", "RETURNS TO 1", "PRESERVES BUILDS", "STATIC CELLS"], 0))
    hub.extend(command_block(120, 5, 11, "function infinite_domain_qa:module_rotation/next", "Build next module rotation test"))
    hub.append(sign_command(120, 5, 13, ["NEXT MODULE", f"{len(modules)} MODULES", "FOUR DIRECTIONS", "WEST RANGE"], 0))
    hub.extend(command_block(136, 5, 11, "function infinite_domain_qa:module_rotation/reset", "Reset module rotation cycle"))
    hub.append(sign_command(136, 5, 13, ["RESET MODULE", "RETURNS TO 1", "PRESERVES BUILDS", "STATIC CELLS"], 0))
    complete_counts = {kind: sum(item.kind == kind for item in content) for kind in ("template", "worldgen_structure", "configured_feature")}
    hub.extend(command_block(-8, 5, 11, "function infinite_domain_qa:catalog/start", "Build organized block museum"))
    hub.append(sign_command(-8, 5, 13, ["BUILD MUSEUM", f"{len(blocks)} BLOCKS", "MOD + TYPE", "TICK-BATCHED"], 0))
    hub.extend(command_block(8, 5, 11, "tp @p 0 20 245", "Visit organized block field"))
    hub.append(sign_command(8, 5, 13, ["BLOCK FIELD", "SOUTH Z=256", "FLUIDS X=220", "ORES X=430"], 0))
    hub.extend(command_block(-40, 5, 11, "function infinite_domain_qa:complete_all/start", "Build every template structure and feature"))
    hub.append(sign_command(-40, 5, 13, ["BUILD COMPLETE", f"{len(content)} ENTRIES", "STRUCTURES +", "FEATURES"], 0))
    hub.extend(command_block(-56, 5, 11, "tp @p 3000 90 3000", "Visit complete template gallery"))
    hub.append(sign_command(-56, 5, 13, ["ALL TEMPLATES", f"{complete_counts['template']} TOTAL", "START X/Z 3000", "CSV INDEX"], 0))
    hub.append(f"tellraw @a {{\"text\":\"Infinite Domain QA hub ready: {len(structures)} curated structures, {complete_counts['template']} templates, {complete_counts['worldgen_structure']} worldgen structures, {complete_counts['configured_feature']} configured features and {len(blocks)} registered blocks. Complete galleries start automatically.\",\"color\":\"gold\"}}")
    hub.append("schedule function infinite_domain_qa:complete_all/start 2s replace")
    hub.append("schedule function infinite_domain_qa:catalog/start 4s replace")
    function("build_hub", hub)

    build_complete_content_catalog(content)
    build_catalog_functions(blocks)


def build_complete_content_catalog(content: list[PlaceableContent]) -> None:
    """Build resumable galleries for every directly placeable data-pack entry."""
    layouts = {
        "template": (3000, 3000, 24, 160),
        "worldgen_structure": (-12000, 3000, 12, 240),
        "configured_feature": (3000, -12000, 20, 80),
    }
    grouped = {kind: [item for item in content if item.kind == kind] for kind in layouts}
    coordinates: dict[tuple[str, str], tuple[int, int, int]] = {}

    function("complete_all/start", [
        "execute if data storage infinite_domain_qa:state complete_gallery_started run tellraw @p {\"text\":\"Complete structure/feature gallery is already scheduled or built.\",\"color\":\"yellow\"}",
        "execute unless data storage infinite_domain_qa:state complete_gallery_started run data modify storage infinite_domain_qa:state complete_gallery_started set value 1b",
        "execute unless data storage infinite_domain_qa:state complete_gallery_scheduled run schedule function infinite_domain_qa:complete_all/template/batch_0000 1t replace",
        "data modify storage infinite_domain_qa:state complete_gallery_scheduled set value 1b",
        f"tellraw @a {{\"text\":\"Complete gallery queued: {len(grouped['template'])} templates, {len(grouped['worldgen_structure'])} worldgen structures and {len(grouped['configured_feature'])} configured features.\",\"color\":\"green\"}}",
    ])

    kind_labels = {
        "template": "TEMPLATE",
        "worldgen_structure": "WORLDGEN STRUCT",
        "configured_feature": "CONFIG FEATURE",
    }
    kinds = list(layouts)
    for kind_index, kind in enumerate(kinds):
        entries = grouped[kind]
        base_x, base_z, columns, cell_size = layouts[kind]
        for index, item in enumerate(entries):
            cell_x = base_x + (index % columns) * cell_size
            cell_z = base_z + (index // columns) * cell_size
            coordinates[(kind, item.resource_id)] = (cell_x, 5, cell_z)
            namespace, path = item.resource_id.split(":", 1)
            label = f"{namespace}:{path}".replace("_", " ")
            place_commands: list[str]
            if kind == "template":
                place_commands = [
                    f"forceload add {cell_x} {cell_z} {cell_x + 159} {cell_z + 159}",
                    f"fill {cell_x} 4 {cell_z} {cell_x + 159} 4 {cell_z + 159} minecraft:smooth_stone replace",
                    f"place template {item.resource_id} {cell_x + 8} 5 {cell_z + 8}",
                    sign_command(cell_x + 3, 5, cell_z + 3, [kind_labels[kind], label[:15], label[15:30], f"{index + 1}/{len(entries)}"], 0),
                    f"forceload remove {cell_x} {cell_z} {cell_x + 159} {cell_z + 159}",
                ]
            elif kind == "worldgen_structure":
                place_commands = [
                    f"forceload add {cell_x} {cell_z} {cell_x + 239} {cell_z + 239}",
                    f"fill {cell_x} 4 {cell_z} {cell_x + 119} 4 {cell_z + 239} minecraft:smooth_stone replace",
                    f"fill {cell_x + 120} 4 {cell_z} {cell_x + 239} 4 {cell_z + 239} minecraft:smooth_stone replace",
                    f"place structure {item.resource_id} {cell_x + 120} 5 {cell_z + 120}",
                    sign_command(cell_x + 3, 5, cell_z + 3, [kind_labels[kind], label[:15], label[15:30], f"{index + 1}/{len(entries)}"], 0),
                    f"forceload remove {cell_x} {cell_z} {cell_x + 239} {cell_z + 239}",
                ]
            else:
                place_commands = [
                    f"forceload add {cell_x} {cell_z} {cell_x + 79} {cell_z + 79}",
                    f"fill {cell_x} 4 {cell_z} {cell_x + 79} 4 {cell_z + 79} minecraft:smooth_stone replace",
                    f"fill {cell_x + 8} 5 {cell_z + 8} {cell_x + 18} 14 {cell_z + 18} minecraft:stone replace",
                    f"fill {cell_x + 8} 15 {cell_z + 8} {cell_x + 18} 15 {cell_z + 18} minecraft:grass_block replace",
                    f"fill {cell_x + 28} 5 {cell_z + 8} {cell_x + 38} 14 {cell_z + 18} minecraft:netherrack replace",
                    f"fill {cell_x + 28} 15 {cell_z + 8} {cell_x + 38} 15 {cell_z + 18} minecraft:netherrack replace",
                    f"fill {cell_x + 48} 5 {cell_z + 8} {cell_x + 58} 14 {cell_z + 18} minecraft:end_stone replace",
                    f"fill {cell_x + 48} 15 {cell_z + 8} {cell_x + 58} 15 {cell_z + 18} minecraft:end_stone replace",
                    f"fill {cell_x + 28} 5 {cell_z + 48} {cell_x + 38} 14 {cell_z + 58} minecraft:stone replace",
                    f"fill {cell_x + 28} 15 {cell_z + 48} {cell_x + 38} 20 {cell_z + 58} minecraft:water replace",
                    f"place feature {item.resource_id} {cell_x + 13} 16 {cell_z + 13}",
                    f"place feature {item.resource_id} {cell_x + 33} 16 {cell_z + 13}",
                    f"place feature {item.resource_id} {cell_x + 53} 16 {cell_z + 13}",
                    f"place feature {item.resource_id} {cell_x + 33} 16 {cell_z + 53}",
                    sign_command(cell_x + 3, 5, cell_z + 3, [kind_labels[kind], label[:15], label[15:30], f"{index + 1}/{len(entries)}"], 0),
                    f"forceload remove {cell_x} {cell_z} {cell_x + 79} {cell_z + 79}",
                ]

            namespace_path = f"{namespace}/{path}"
            function(f"complete/{kind}/{namespace_path}", place_commands)
            batch_commands = [f"function infinite_domain_qa:complete/{kind}/{namespace_path}"]
            if index + 1 < len(entries):
                batch_commands.append(f"schedule function infinite_domain_qa:complete_all/{kind}/batch_{index + 1:04d} 2t replace")
            elif kind_index + 1 < len(kinds):
                next_kind = kinds[kind_index + 1]
                batch_commands.extend([
                    f"tellraw @a {{\"text\":\"Complete {kind_labels[kind].lower()} gallery finished: {len(entries)} entries.\",\"color\":\"green\"}}",
                    f"schedule function infinite_domain_qa:complete_all/{next_kind}/batch_0000 10t replace",
                ])
            else:
                batch_commands.append(f"tellraw @a {{\"text\":\"All complete galleries finished: {len(content)} placeable structures/features processed.\",\"color\":\"gold\"}}")
            function(f"complete_all/{kind}/batch_{index:04d}", batch_commands)

    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("kind", "index", "resource_id", "namespace", "path", "function", "cell_x", "cell_y", "cell_z", "sources"))
    kind_indices = {kind: 0 for kind in layouts}
    for item in content:
        kind_indices[item.kind] += 1
        namespace, path = item.resource_id.split(":", 1)
        cell_x, cell_y, cell_z = coordinates[(item.kind, item.resource_id)]
        writer.writerow((
            item.kind,
            kind_indices[item.kind],
            item.resource_id,
            namespace,
            path,
            f"infinite_domain_qa:complete/{item.kind}/{namespace}/{path}",
            cell_x,
            cell_y,
            cell_z,
            ";".join(item.sources),
        ))
    write_text(WORLD / "QA_CONTENT_CATALOG.csv", output.getvalue())


def build_catalog_functions(blocks: list[BlockSample]) -> None:
    solids = [sample for sample in blocks if not sample.is_fluid]
    fluids = [sample for sample in blocks if sample.is_fluid]
    ores = [sample for sample in solids if sample.category == "ores"]
    category_rank = {name: index for index, name in enumerate(CATEGORY_ORDER)}

    # Each entry carries its own affected horizontal point. This lets every
    # scheduled batch load only the small museum region that it is changing.
    def emit_chain(folder: str, entries: list[tuple[int, int, list[str]]], completion: str, batch_size: int = 96) -> None:
        batches = math.ceil(len(entries) / batch_size)
        for batch_index in range(batches):
            subset = entries[batch_index * batch_size:(batch_index + 1) * batch_size]
            min_x = min(entry[0] for entry in subset) - 3
            max_x = max(entry[0] for entry in subset) + 3
            min_z = min(entry[1] for entry in subset) - 3
            max_z = max(entry[1] for entry in subset) + 3
            commands = [f"forceload add {min_x} {min_z} {max_x} {max_z}"]
            for _, _, item_commands in subset:
                commands.extend(item_commands)
            commands.append(f"forceload remove {min_x} {min_z} {max_x} {max_z}")
            if batch_index + 1 < batches:
                commands.append(f"schedule function infinite_domain_qa:{folder}/batch_{batch_index + 1:03d} 2t replace")
            else:
                commands.append(f"tellraw @a {{\"text\":{json.dumps(completion)},\"color\":\"green\"}}")
            function(f"{folder}/batch_{batch_index:03d}", commands)

    field_entries: list[tuple[int, int, list[str]]] = []
    field_coordinates: dict[str, tuple[int, int, int]] = {}
    field_x, cursor_z, columns, pitch = -72, 256, 48, 3
    namespaces = sorted({sample.namespace for sample in solids}, key=lambda name: (name != "minecraft", name))
    for namespace in namespaces:
        cursor_z += 3
        field_entries.append((-78, cursor_z, [
            f"fill -76 4 {cursor_z} 70 4 {cursor_z} minecraft:polished_andesite replace",
            sign_command(-78, 5, cursor_z, ["MOD SECTION", namespace[:15], namespace[15:30], "Jade = block ID"], 4),
        ]))
        cursor_z += 3
        namespace_samples = [sample for sample in solids if sample.namespace == namespace]
        categories = sorted({sample.category for sample in namespace_samples}, key=lambda name: category_rank[name])
        for category in categories:
            category_samples = [sample for sample in namespace_samples if sample.category == category]
            label = category.replace("_", " ")
            field_entries.append((-78, cursor_z, [
                sign_command(-78, 5, cursor_z, [namespace[:15], label[:15], label[15:30], f"{len(category_samples)} blocks"], 4),
                f"fill -75 4 {cursor_z} 70 4 {cursor_z} minecraft:stone_bricks replace",
            ]))
            cursor_z += 2
            for local_index, sample in enumerate(category_samples):
                col, row = local_index % columns, local_index // columns
                x, z = field_x + col * pitch, cursor_z + row * pitch
                field_coordinates[sample.block_id] = (x, 5, z)
                field_entries.append((x, z, [
                    f"setblock {x} 4 {z} minecraft:smooth_stone replace",
                    f"setblock {x} 5 {z} {sample.block_id} replace",
                ]))
            cursor_z += math.ceil(len(category_samples) / columns) * pitch + 3

    # Fluids receive two distinct tests: a sealed source display and a
    # glass-sided run channel. They are grouped by provider namespace.
    fluid_entries: list[tuple[int, int, list[str]]] = []
    fluid_coordinates: dict[str, tuple[int, int, int]] = {}
    fluid_x, fluid_z, fluid_columns = 220, 256, 6
    for namespace in sorted({sample.namespace for sample in fluids}, key=lambda name: (name != "minecraft", name)):
        fluid_entries.append((fluid_x - 5, fluid_z, [
            f"fill {fluid_x - 3} 4 {fluid_z} {fluid_x + 105} 4 {fluid_z} minecraft:polished_deepslate replace",
            sign_command(fluid_x - 5, 5, fluid_z, ["FLUID LAB", namespace[:15], "CUBE + CHANNEL", "SOURCE / FLOW"], 4),
        ]))
        fluid_z += 4
        namespace_fluids = [sample for sample in fluids if sample.namespace == namespace]
        for local_index, sample in enumerate(namespace_fluids):
            col, row = local_index % fluid_columns, local_index // fluid_columns
            x, z = fluid_x + col * 18, fluid_z + row * 20
            fluid_coordinates[sample.block_id] = (x, 6, z)
            fluid_entries.append((x, z + 6, [
                f"fill {x - 2} 4 {z - 2} {x + 2} 8 {z + 2} minecraft:glass hollow",
                f"setblock {x} 6 {z} {sample.block_id} replace",
                f"fill {x - 1} 4 {z + 4} {x + 1} 4 {z + 15} minecraft:glass replace",
                f"fill {x - 1} 5 {z + 4} {x - 1} 6 {z + 15} minecraft:glass replace",
                f"fill {x + 1} 5 {z + 4} {x + 1} 6 {z + 15} minecraft:glass replace",
                f"setblock {x} 5 {z + 4} {sample.block_id} replace",
                sign_command(x, 5, z - 4, [sample.namespace[:15], sample.path[:15], sample.path[15:30], "source + flow"], 8),
            ]))
        fluid_z += math.ceil(len(namespace_fluids) / fluid_columns) * 20 + 5

    # A continuous ore reference wall, still separated into labeled mod panels.
    ore_entries: list[tuple[int, int, list[str]]] = []
    ore_coordinates: dict[str, tuple[int, int, int]] = {}
    ore_x, ore_z = 430, 256
    for namespace in sorted({sample.namespace for sample in ores}, key=lambda name: (name != "minecraft", name)):
        namespace_ores = [sample for sample in ores if sample.namespace == namespace]
        panel_rows = math.ceil(len(namespace_ores) / 24)
        panel_width = min(24, len(namespace_ores)) * 3
        ore_entries.append((ore_x, ore_z, [
            f"fill {ore_x - 2} 4 {ore_z} {ore_x + max(panel_width, 8)} {8 + panel_rows * 3} {ore_z} minecraft:deepslate_bricks replace",
            sign_command(ore_x, 5, ore_z - 1, ["UNIFIED ORE WALL", namespace[:15], f"{len(namespace_ores)} ores", "Jade = block ID"], 8),
        ]))
        for local_index, sample in enumerate(namespace_ores):
            col, row = local_index % 24, local_index // 24
            x, y = ore_x + col * 3, 7 + row * 3
            ore_coordinates[sample.block_id] = (x, y, ore_z - 1)
            ore_entries.append((x, ore_z, [f"setblock {x} {y} {ore_z - 1} {sample.block_id} replace"]))
        ore_z += 5

    # The compact tower follows the exact same namespace/category order as the
    # field. It is a density view, while the field is the readable taxonomy.
    tower_entries: list[tuple[int, int, list[str]]] = []
    tower_coordinates: dict[str, tuple[int, int, int, int]] = {}
    tower_x, tower_z, tower_columns, floor_height = 650, 256, 16, 5
    for floor in range(math.ceil(len(solids) / 256)):
        y = 4 + floor * floor_height
        first = solids[floor * 256]
        last = solids[min(len(solids), (floor + 1) * 256) - 1]
        tower_entries.append((tower_x, tower_z, [
            f"fill {tower_x - 2} {y} {tower_z - 2} {tower_x + 32} {y} {tower_z + 32} minecraft:smooth_stone replace",
            sign_command(tower_x - 1, y + 1, tower_z - 1, [f"TOWER FLOOR {floor + 1}", first.namespace[:15], last.namespace[:15], "same sort order"], 0),
        ]))
    for index, sample in enumerate(solids):
        floor, within = divmod(index, 256)
        col, row = within % tower_columns, within // tower_columns
        x, y, z = tower_x + col * 2, 5 + floor * floor_height, tower_z + row * 2
        tower_coordinates[sample.block_id] = (x, y, z, floor)
        tower_entries.append((x, z, [f"setblock {x} {y} {z} {sample.block_id} replace"]))
    tower_entries.append((tower_x + 32, tower_z - 2, [
        f"fill {tower_x + 32} 4 {tower_z - 2} {tower_x + 32} {4 + math.ceil(len(solids) / 256) * floor_height} {tower_z - 2} minecraft:scaffolding replace",
    ]))

    emit_chain("field", field_entries, f"Organized block field complete: {len(solids)} solid blocks.")
    emit_chain("fluid", fluid_entries, f"Contained fluid laboratory complete: {len(fluids)} fluids.", 24)
    emit_chain("ore", ore_entries, f"Unified ore wall complete: {len(ores)} ores.")
    emit_chain("tower", tower_entries, f"Organized tower complete: {len(solids)} solid blocks on {math.ceil(len(solids) / 256)} floors.")
    function("catalog/start", [
        "execute if data storage infinite_domain_qa:state catalog_built run tellraw @p {\"text\":\"Museum build already started or completed.\",\"color\":\"yellow\"}",
        "execute unless data storage infinite_domain_qa:state catalog_built run data modify storage infinite_domain_qa:state catalog_built set value 1b",
        "execute unless data storage infinite_domain_qa:state catalog_scheduled run schedule function infinite_domain_qa:field/batch_000 1t replace",
        "execute unless data storage infinite_domain_qa:state catalog_scheduled run schedule function infinite_domain_qa:fluid/batch_000 2s replace",
        "execute unless data storage infinite_domain_qa:state catalog_scheduled run schedule function infinite_domain_qa:ore/batch_000 4s replace",
        "execute unless data storage infinite_domain_qa:state catalog_scheduled run schedule function infinite_domain_qa:tower/batch_000 6s replace",
        "data modify storage infinite_domain_qa:state catalog_scheduled set value 1b",
        f"tellraw @p {{\"text\":\"Building museum: {len(solids)} solids by mod/type, {len(fluids)} fluids, {len(ores)} ores.\",\"color\":\"green\"}}",
    ])

    mapping_rows = ["index,block_id,namespace,category,is_fluid,field_x,field_y,field_z,fluid_x,fluid_y,fluid_z,ore_x,ore_y,ore_z,tower_x,tower_y,tower_z,tower_floor"]
    for index, sample in enumerate(blocks):
        field = field_coordinates.get(sample.block_id, ("", "", ""))
        fluid = fluid_coordinates.get(sample.block_id, ("", "", ""))
        ore = ore_coordinates.get(sample.block_id, ("", "", ""))
        tower = tower_coordinates.get(sample.block_id, ("", "", "", ""))
        mapping_rows.append(",".join(map(str, (index, sample.block_id, sample.namespace, sample.category, int(sample.is_fluid), *field, *fluid, *ore, *tower))))
    write_text(WORLD / "QA_BLOCK_CATALOG.csv", "\n".join(mapping_rows))


def write_readme(
    structures: list[str],
    roads: list[str],
    modules: list[str],
    blocks: list[BlockSample],
    content: list[PlaceableContent],
) -> None:
    solids = [sample for sample in blocks if not sample.is_fluid]
    fluids = [sample for sample in blocks if sample.is_fluid]
    ores = [sample for sample in solids if sample.category == "ores"]
    namespaces = {sample.namespace for sample in blocks}
    templates = [item for item in content if item.kind == "template"]
    worldgen_structures = [item for item in content if item.kind == "worldgen_structure"]
    configured_features = [item for item in content if item.kind == "configured_feature"]
    text = f"""Infinite Domain Structure QA Flatworld

Minecraft: Java 1.21.1 / NeoForge pack instance
Structures: {len(structures)}
All structure templates: {len(templates)}
All worldgen structures: {len(worldgen_structures)}
All configured features: {len(configured_features)}
Road modules: {len(roads)}
Structure-kit modules: {len(modules)}
Registered blocks captured: {len(blocks)}
Mod namespaces represented: {len(namespaces)}

LAYOUT
- Spawn (0, 5, 0): labeled structure controls and catalog controls.
- North: {len(structures)} structure review cells, each 96 x 96 blocks.
- East: {len(roads)} road-module review cells, each 48 x 48 blocks, grouped by topology family and condition.
- West: {len(modules)} port/dock, marketplace and industrial module review cells, each 48 x 48 blocks.
- Far north: an incremental {len(structures)}-cell rotation gallery. NEXT ROTATION builds one curated structure in all four orientations without deleting prior tests.
- Far east and west: compact four-way rotation galleries for the 12 clean road topologies and all {len(modules)} reusable structure modules.
- Complete template gallery, starting X=3000 Z=3000: all {len(templates)} NBT templates embedded in vanilla, mods and loose data packs.
- Complete worldgen-structure gallery, starting X=-12000 Z=3000: all {len(worldgen_structures)} registered data-driven structure definitions.
- Complete configured-feature gallery, starting X=3000 Z=-12000: all {len(configured_features)} directly placeable features, each attempted on grass/stone, Nether, End and water test substrates.
- South, starting near Z=256: {len(solids)} solid blocks grouped Minecraft-first, then alphabetically by mod, and subdivided by functional type.
- Fluid laboratory, starting near X=220 Z=256: {len(fluids)} fluids, each in a sealed glass source cube and a glass-sided flow channel.
- Unified ore wall, starting near X=430 Z=256: all {len(ores)} detected ores in labeled mod panels.
- Compact tower, starting near X=650 Z=256: the solid registry in the same namespace/category order, 16 x 16 samples per floor.

USAGE
1. Open the world in the Infinite Domain instance.
2. The complete template, worldgen-structure, configured-feature and block galleries begin automatically in resumable tick-batches on first load.
3. Press BUILD ALL NORTH to populate all {len(structures)} curated structure cells, or use a labeled structure button to build one template and teleport to it.
4. Press BUILD ALL EAST/WEST for the road and reusable-module galleries.
5. Individual curated structure, road and module buttons can be pressed again whenever an asset changes.
6. Press NEXT ROTATION to build the next authoritative structure in four directions. RESET ROTATION returns the cycle to test 1 without deleting completed cells.
7. NEXT ROAD TEST and NEXT MODULE provide equivalent four-way review cycles for connector-sensitive assets.
8. Return with /tp 0 8 0.
9. BUILD COMPLETE and BUILD MUSEUM safely resume their automatic queues if needed.
10. QA_CONTENT_CATALOG.csv records every template/structure/feature ID, source, function and cell coordinate. QA_BLOCK_CATALOG.csv does the same for blocks.

REVIEW RECORDING
- Building checklist: structure_library/review/building-production-review.csv
- Road checklist: structure_library/review/road-production-review.csv
- Module checklist: structure_library/review/module-production-review.csv
- Change each required check from pending to pass or fail as it is inspected.
- A completed row requires reviewer, ISO-format reviewed_at and optional notes.
- Checklists are evidence only. They never automatically enable world generation.

SAFETY
- Creative mode, commands enabled, peaceful difficulty.
- Mob spawning, fire spread, weather, daylight progression and random ticks are disabled.
- Fluids are excluded from the ordinary field and contained in dedicated glass apparatus.

PROVENANCE
No third-party world save is redistributed. The available CurseForge 1.21.1 flat-world base was All Rights Reserved, so this save uses Minecraft's native superflat generator and original Infinite Domain QA data only.
"""
    write_text(WORLD / "README_QA_WORLD.txt", text)


def main() -> None:
    if WORLD.exists():
        raise FileExistsError(f"Refusing to overwrite existing QA world: {WORLD}")
    structures = structure_names()
    roads = road_names()
    modules = module_names()
    blocks = block_samples()
    content = placeable_content()
    write_level_dat()
    build_datapack(structures, roads, modules, blocks, content)
    write_readme(structures, roads, modules, blocks, content)
    counts = {kind: sum(item.kind == kind for item in content) for kind in ("template", "worldgen_structure", "configured_feature")}
    print(f"Created {WORLD_NAME}: {len(structures)} curated structure controls, {counts['template']} templates, {counts['worldgen_structure']} worldgen structures, {counts['configured_feature']} configured features, {len(roads)} road controls, {len(modules)} module controls, {len(blocks)} blocks, {math.ceil(len(blocks) / 256)} tower floors")


if __name__ == "__main__":
    main()

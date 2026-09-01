"""Shared oracle for "does this content actually exist, and can a player reach it?".

Audits kept reporting authored content as broken when it was fine, because each
one rebuilt its own idea of what exists from whichever slice of the pack was
convenient. Four blind spots produced almost all of that noise:

  * mod-owned content lives inside the jars, not in kubejs/data;
  * the registry snapshot is captured from a running client, so it lags behind
    any mod or KubeJS item added since the last capture;
  * KubeJS composes many item ids from template literals at startup, so no
    literal id exists in the source to grep for;
  * KubeJS registers many recipes from server scripts, so they never appear in
    the data-driven recipe index.

This module resolves all four so that a finding means a real break. The mod jar
scan is cached; delete the cache file or pass refresh=True to rebuild it.
"""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODS = ROOT / "mods"
KUBEJS_STARTUP = ROOT / "kubejs/startup_scripts"
KUBEJS_SERVER = ROOT / "kubejs/server_scripts"
KUBEJS_CONFIG = ROOT / "kubejs/config"
REGISTRY_ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
REGISTRY_BLOCKS = ROOT / "dev/docs/registry-inventory/block-ids.txt"
CACHE = ROOT / "dev/docs/registry-inventory/mod-content-index.json"

LOOT_DIR_RE = re.compile(r"^data/([^/]+)/loot_table[s]?/(.+)\.json$")
STRUCTURE_RE = re.compile(r"^data/([^/]+)/worldgen/structure/(.+)\.json$")
STRUCTURE_SET_RE = re.compile(r"^data/([^/]+)/worldgen/structure_set/(.+)\.json$")
BIOME_TAG_RE = re.compile(r"^data/([^/]+)/tags/worldgen/biome/(.+)\.json$")
ITEM_MODEL_RE = re.compile(r"^assets/([^/]+)/models/item/(.+)\.json$")

# Built into the game rather than shipped in a jar, so a jar scan never finds
# them and every quest that targets one looks like it names a missing structure.
VANILLA_STRUCTURES = frozenset(
    "minecraft:" + name for name in (
        "ancient_city", "bastion_remnant", "buried_treasure", "desert_pyramid",
        "end_city", "fortress", "igloo", "jungle_pyramid", "mansion", "mineshaft",
        "mineshaft_mesa", "monument", "nether_fossil", "ocean_ruin_cold",
        "ocean_ruin_warm", "pillager_outpost", "ruined_portal",
        "ruined_portal_desert", "ruined_portal_jungle", "ruined_portal_mountain",
        "ruined_portal_nether", "ruined_portal_ocean", "ruined_portal_swamp",
        "shipwreck", "shipwreck_beached", "stronghold", "swamp_hut", "trail_ruins",
        "trial_chambers", "village_desert", "village_plains", "village_savanna",
        "village_snowy", "village_taiga",
    )
)

# Recipe idioms used by this pack's server scripts. The captured group is the
# output id, which is always the first argument.
SCRIPT_RECIPE_RE = re.compile(
    r"event\.(?:recipes\.[A-Za-z0-9_.]+|shaped|shapeless|smelting|blasting|"
    r"smoking|campfireCooking|stonecutting|custom)\(\s*"
    r"(?:Item\.of\(\s*)?['\"]([a-z0-9_.-]+:[a-z0-9_/.-]+)['\"]"
)
# Bare `Item.of('ns:id')` still signals the script constructs that stack.
ITEM_OF_RE = re.compile(r"Item\.of\(\s*['\"]([a-z0-9_.-]+:[a-z0-9_/.-]+)['\"]")


@dataclass
class ModContent:
    """Everything the installed jars provide, indexed by kind."""

    items: set[str] = field(default_factory=set)
    loot_tables: dict[str, list[str]] = field(default_factory=dict)  # table id -> item ids
    structures: set[str] = field(default_factory=set)
    placed_structures: set[str] = field(default_factory=set)
    biome_tags: dict[str, list[str]] = field(default_factory=dict)  # tag id -> values


def _jar_signature() -> list[list[object]]:
    if not MODS.is_dir():
        return []
    return sorted(
        [jar.name, jar.stat().st_size] for jar in MODS.glob("*.jar")
    )


def _collect_loot_items(payload: object, out: set[str]) -> None:
    if isinstance(payload, list):
        for child in payload:
            _collect_loot_items(child, out)
    elif isinstance(payload, dict):
        if payload.get("type") in {"item", "minecraft:item"}:
            name = payload.get("name")
            if isinstance(name, str):
                out.add(name)
        for child in payload.values():
            _collect_loot_items(child, out)


def scan_mods(refresh: bool = False) -> ModContent:
    """Index item, loot and worldgen content across every installed jar."""
    signature = _jar_signature()
    if not refresh and CACHE.exists():
        try:
            cached = json.loads(CACHE.read_text(encoding="utf-8"))
            if cached.get("signature") == signature:
                return ModContent(
                    items=set(cached["items"]),
                    loot_tables={k: list(v) for k, v in cached["loot_tables"].items()},
                    structures=set(cached["structures"]),
                    placed_structures=set(cached["placed_structures"]),
                    biome_tags={k: list(v) for k, v in cached["biome_tags"].items()},
                )
        except (json.JSONDecodeError, KeyError):
            pass

    content = ModContent()
    if MODS.is_dir():
        for jar_path in sorted(MODS.glob("*.jar")):
            try:
                archive = zipfile.ZipFile(jar_path)
            except (zipfile.BadZipFile, OSError):
                continue
            with archive:
                for name in archive.namelist():
                    match = ITEM_MODEL_RE.match(name)
                    if match:
                        content.items.add(match.group(1) + ":" + match.group(2))
                        continue

                    match = LOOT_DIR_RE.match(name)
                    if match:
                        table_id = match.group(1) + ":" + match.group(2)
                        try:
                            payload = json.loads(archive.read(name).decode("utf-8-sig"))
                        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                            continue
                        items: set[str] = set()
                        _collect_loot_items(payload, items)
                        content.loot_tables[table_id] = sorted(items)
                        continue

                    match = STRUCTURE_RE.match(name)
                    if match:
                        content.structures.add(match.group(1) + ":" + match.group(2))
                        continue

                    match = BIOME_TAG_RE.match(name)
                    if match:
                        tag_id = match.group(1) + ":" + match.group(2)
                        try:
                            payload = json.loads(archive.read(name).decode("utf-8-sig"))
                        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                            continue
                        values = [
                            v if isinstance(v, str) else (v or {}).get("id")
                            for v in payload.get("values", []) or []
                        ]
                        # Later jars may extend an earlier tag rather than replace it.
                        merged = content.biome_tags.setdefault(tag_id, [])
                        for v in values:
                            if v and v not in merged:
                                merged.append(v)
                        continue

                    match = STRUCTURE_SET_RE.match(name)
                    if match:
                        try:
                            payload = json.loads(archive.read(name).decode("utf-8-sig"))
                        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                            continue
                        for entry in payload.get("structures", []) or []:
                            target = entry.get("structure") if isinstance(entry, dict) else None
                            if isinstance(target, str):
                                content.placed_structures.add(target)

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({
        "signature": signature,
        "items": sorted(content.items),
        "loot_tables": {k: content.loot_tables[k] for k in sorted(content.loot_tables)},
        "structures": sorted(content.structures),
        "placed_structures": sorted(content.placed_structures),
        "biome_tags": {k: content.biome_tags[k] for k in sorted(content.biome_tags)},
    }, indent=1) + "\n", encoding="utf-8")
    return content


def kubejs_item_matchers() -> tuple[set[str], list[re.Pattern[str]]]:
    """Return (literal kubejs ids, patterns for template-composed kubejs ids).

    KubeJS builds families of items from template literals such as
    `${flavor.id}_soda_can`, so the concrete id never appears in the source. The
    surrounding literal text is still a reliable shape, so it becomes a pattern.
    """
    literals: set[str] = set()
    patterns: list[re.Pattern[str]] = []
    if not KUBEJS_STARTUP.is_dir():
        return literals, patterns

    sources = [p.read_text(encoding="utf-8", errors="replace") for p in sorted(KUBEJS_STARTUP.glob("*.js"))]
    if KUBEJS_CONFIG.is_dir():
        sources += [p.read_text(encoding="utf-8", errors="replace") for p in sorted(KUBEJS_CONFIG.glob("*.json"))]

    for text in sources:
        # Bare names from event.create('x'), and namespaced ids ("kubejs:x"),
        # which is how the config JSONs driving the data-driven registries spell
        # them. Matching only bare names misses every config-declared item.
        for name in re.findall(r"['\"](?:kubejs:)?([a-z][a-z0-9_]{2,})['\"]", text):
            literals.add(name)
        for template in re.findall(r"`([^`]*\$\{[^`]*)`", text):
            # Only ids: reject anything with a path separator, space or colon.
            if re.search(r"[\s:/]", re.sub(r"\$\{[^}]*\}", "", template)):
                continue
            regex = re.escape(template)
            regex = re.sub(r"\\\$\\\{[^}]*\\\}", "[a-z0-9_]+", regex)
            if regex.strip("[a-z0-9_]+"):
                try:
                    patterns.append(re.compile("^" + regex + "$"))
                except re.error:
                    continue
    # KubeJS mints a `<fluid>_bucket` item for every registered fluid, so a
    # bucket id never appears in source even when its fluid does.
    literals |= {name + "_bucket" for name in list(literals)}
    return literals, patterns


def template_patterns(texts: list[str]) -> list[re.Pattern[str]]:
    """Compile `${x}_suffix` style id templates into matchers.

    KubeJS builds whole families of ids this way, so the concrete id exists in
    neither the registry nor the source. The literal text around the
    substitution is still a reliable shape.
    """
    patterns: list[re.Pattern[str]] = []
    for text in texts:
        for template in re.findall(r"`([^`]*\$\{[^`]*)`", text):
            # Recipe sites spell the id with its namespace
            # (`kubejs:precipitated_${metal.id}_concentrate`); registration sites
            # use the bare name. Normalise to the bare name before validating.
            if template.startswith("kubejs:"):
                template = template[len("kubejs:"):]
            # Ids only: reject anything with a path separator, space or colon.
            if re.search(r"[\s:/]", re.sub(r"\$\{[^}]*\}", "", template)):
                continue
            regex = re.escape(template)
            regex = re.sub(r"\\\$\\\{[^}]*\\\}", "[a-z0-9_]+", regex)
            if regex.strip("[a-z0-9_]+"):
                try:
                    patterns.append(re.compile("^" + regex + "$"))
                except re.error:
                    continue
    return patterns


def script_touched_items() -> tuple[set[str], list[re.Pattern[str]]]:
    """Item ids the pack's server scripts or their driving configs mention.

    Most KubeJS recipes here are built in loops over a config JSON, so the output
    id never appears as a literal and no regex can prove which side of a recipe
    an id sits on. Presence is therefore evidence that pack machinery exists for
    the item - enough to stop calling it unobtainable, not enough to call it
    crafted. Callers should treat a miss as "worth a look", not as a break.
    """
    touched: set[str] = set()
    texts: list[str] = []
    for directory, pattern in ((KUBEJS_SERVER, "*.js"), (KUBEJS_CONFIG, "*.json")):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob(pattern)):
            text = path.read_text(encoding="utf-8", errors="replace")
            texts.append(text)
            for name in re.findall(r"['\"](?:kubejs:)?([a-z][a-z0-9_]{2,})['\"]", text):
                touched.add("kubejs:" + name)
                touched.add("kubejs:" + name + "_bucket")
    return touched, template_patterns(texts)


def script_recipe_outputs() -> set[str]:
    """Item ids produced by KubeJS server-script recipes."""
    outputs: set[str] = set()
    if not KUBEJS_SERVER.is_dir():
        return outputs
    for path in sorted(KUBEJS_SERVER.glob("*.js")):
        text = path.read_text(encoding="utf-8", errors="replace")
        outputs.update(SCRIPT_RECIPE_RE.findall(text))
        outputs.update(ITEM_OF_RE.findall(text))
    return outputs


class ItemOracle:
    """Answers whether an item id exists in this instance."""

    def __init__(self, refresh_mods: bool = False):
        # Item and block are separate Minecraft registries and merging them is
        # not safe: fluids and item-less blocks (minecraft:lava,
        # minecraft:cave_vines_plant, petrochem:gasoline) appear only in the
        # block registry, and an item task naming one is uncompletable. The
        # item registry alone answers "can a player hold this".
        self.registry: set[str] = set()
        self.blocks: set[str] = set()
        for path, sink in ((REGISTRY_ITEMS, self.registry), (REGISTRY_BLOCKS, self.blocks)):
            if path.exists():
                for line in path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line:
                        sink.add(line)
        self.mods = scan_mods(refresh=refresh_mods)
        self.mods.structures |= VANILLA_STRUCTURES
        self.mods.placed_structures |= VANILLA_STRUCTURES
        self.kubejs_literals, self.kubejs_patterns = kubejs_item_matchers()

    def exists(self, item_id: str) -> bool:
        if item_id in self.registry or item_id in self.mods.items:
            return True
        namespace, _, name = item_id.partition(":")
        if namespace == "kubejs":
            if name in self.kubejs_literals:
                return True
            return any(pattern.match(name) for pattern in self.kubejs_patterns)
        return False

    def why_missing(self, item_id: str) -> str:
        namespace = item_id.partition(":")[0]
        if item_id in self.blocks:
            return "exists only in the block registry - it has no item form"
        if namespace == "kubejs":
            return "no KubeJS registration found in startup_scripts or kubejs/config"
        if namespace in {n.partition(":")[0] for n in self.registry | self.mods.items}:
            return "namespace '" + namespace + "' is installed but does not provide this id"
        return "namespace '" + namespace + "' is not provided by any installed mod"


if __name__ == "__main__":
    oracle = ItemOracle(refresh_mods=True)
    print("registry snapshot ids   ", len(oracle.registry))
    print("ids found in mod jars   ", len(oracle.mods.items))
    print("mod loot tables         ", len(oracle.mods.loot_tables))
    print("mod structures          ", len(oracle.mods.structures))
    print("mod-placed structures   ", len(oracle.mods.placed_structures))
    print("mod biome tags          ", len(oracle.mods.biome_tags))
    print("kubejs literal names    ", len(oracle.kubejs_literals))
    print("kubejs id patterns      ", len(oracle.kubejs_patterns))
    print("script recipe outputs   ", len(script_recipe_outputs()))

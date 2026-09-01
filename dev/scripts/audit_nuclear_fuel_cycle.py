"""Static Phase-I audit for Infinite Domain's Create Nuclear fuel cycle."""

from __future__ import annotations

import json
import re
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "kubejs/config/nuclear_fuel_cycle.json"
MINERALS = ROOT / "kubejs/config/mineral_trace_ore_processing.json"
STARTUP = ROOT / "kubejs/startup_scripts/nuclear_fuel_cycle_items.js"
RECIPES = ROOT / "kubejs/server_scripts/nuclear_fuel_cycle.js"
CHAPTER = ROOT / "config/ftbquests/quests/chapters/era_06_high_energy_and_nuclear_engineering.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REPORT = ROOT / "docs/create-nuclear-phase-i-investigation.md"


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)
    print(f"PASS  {message}")


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    minerals = json.loads(MINERALS.read_text(encoding="utf-8"))
    startup = STARTUP.read_text(encoding="utf-8")
    recipes = RECIPES.read_text(encoding="utf-8")
    chapter = CHAPTER.read_text(encoding="utf-8")
    lang = LANG.read_text(encoding="utf-8")

    jar_path = ROOT / "mods/createnuclear-1.3.2-beta.3-neoforge.jar"
    require(jar_path.exists(), "exact installed Create Nuclear 1.3.2-beta.3 jar exists")
    with zipfile.ZipFile(jar_path) as jar:
        names = set(jar.namelist())
        manifest = jar.read("META-INF/neoforge.mods.toml").decode("utf-8")
        controller = jar.read("net/nuclearteam/createnuclear/content/multiblock/controller/ReactorControllerBlockEntity.class")
        blocks = jar.read("net/nuclearteam/createnuclear/CNBlocks.class")
        blueprint = jar.read("net/nuclearteam/createnuclear/content/multiblock/bluePrintItem/ReactorBluePrintData.class")
        reactor_input = jar.read("net/nuclearteam/createnuclear/content/multiblock/input/ReactorInputInventory.class")
        require('version="1.3.2-beta.3"' in manifest and 'versionRange="[1.21.1]"' in manifest, "manifest matches installed Minecraft and mod versions")
        require(b"formattedPattern" in controller and b"offsets" in controller, "controller retains fixed-grid and local-adjacency fields")
        require(b"baseUraniumHeat" in controller and b"baseGraphiteHeat" in controller, "controller still uses signed uranium/graphite heat fields")
        require(b"URANIUM_ROD" in controller and b"GRAPHITE_ROD" in controller, "controller still checks exact installed rod items")
        require(b"countGraphiteRod" in blueprint and b"countUraniumRod" in blueprint and b"patternAll" in blueprint, "blueprint serialization retains two rod counts plus slot records")
        require(b"URANIUM_ROD" in reactor_input and b"GRAPHITE_ROD" in reactor_input, "reactor input remains a dedicated two-stream inventory")
        require(struct.pack(">d", 10240.0) in blocks, "installed reactor output registers 10,240 SU capacity per RPM")
        for path in (
            "data/createnuclear/recipe/crushing/crushed_raw_uranium.json",
            "data/createnuclear/recipe/mixing/uranium_fluid.json",
            "data/createnuclear/recipe/compacting/uranium_fluid_to_yellowcake.json",
            "data/createnuclear/recipe/enriched/enriched_yellowcake.json",
            "data/createnuclear/recipe/mechanical_crafting/uranium_rod.json",
            "data/createnuclear/tags/item/fuel.json",
            "data/createnuclear/tags/item/cooler.json",
        ):
            require(path in names, f"installed baseline resource inspected: {path}")

    require(config["installedBuild"] == {
        "mod": "createnuclear", "version": "1.3.2-beta.3", "minecraft": "1.21.1", "reactorSlots": 57
    }, "central config records the exact installed build and 57-slot boundary")
    output = config["reactorOutput"]
    require(output == {
        "originalStressCapacityPerRpm": 10240.0,
        "stressCapacityPerRpm": 1024.0,
        "maximumOutputScale": 0.1,
        "preserveHeatAndRpm": True,
    }, "reactor output is capped to 10% without changing heat or RPM")
    balance_jar = ROOT / "mods/infinite-domain-create-nuclear-balance-1.0.0.jar"
    require(balance_jar.exists(), "Create Nuclear balance addon is installed")
    with zipfile.ZipFile(balance_jar) as jar:
        names = set(jar.namelist())
        mixin = jar.read("infinite_domain_nuclear_balance.mixins.json").decode("utf-8")
        balance_class = jar.read("infinitedomain/nuclearbalance/NuclearOutputBalance.class")
        require("infinitedomain/nuclearbalance/mixin/CNBlocksMixin.class" in names, "balance addon packages the capacity mixin")
        require("lambda$static$22" in mixin or b"lambda$static$22" in jar.read("infinitedomain/nuclearbalance/mixin/CNBlocksMixin.class"), "mixin targets the installed 10,240-capacity supplier")
        require(b"stressCapacityPerRpm" in balance_class and struct.pack(">d", 1024.0) in balance_class, "addon reads the centralized 1,024 capacity value with a safe fallback")
    uranium = next(metal for metal in minerals["metals"] if metal["id"] == "uranium")
    require(uranium["processingClass"] == "nuclear" and uranium["primitiveRecovery"] is False, "uranium uses traces but cannot take primitive nugget recovery")
    require(len(uranium["ores"]) == 5 and any("deepslate" in ore for ore in uranium["ores"]), "five installed uranium ore blocks share the normal/deepslate trace economy")

    non_item_ids = {config["uranium"]["trace"], config["uranium"]["slurry"]}
    for item in (*config["uranium"].values(), *config["graphite"].values()):
        if isinstance(item, str) and item.startswith("kubejs:") and item not in non_item_ids:
            require(item.split(":", 1)[1] in startup, f"startup registers {item}")
    for marker in ("create.crushing", "create.milling", "create.splashing", "create.mixing", "create.compacting", "create.pressing", "create.cutting", "create:sequenced_assembly", "create:mechanical_crafting"):
        require(marker in recipes, f"fuel cycle uses {marker}")
    expected_organic = {
        "extractionReagent": "kubejs:chelating_broth",
        "pelletBinder": "kubejs:saponified_collector",
        "graphiteBinder": "kubejs:tannic_pulp",
    }
    require(config["organicInputs"] == expected_organic, "central config reuses the established organic chemistry inputs")
    for key in expected_organic:
        require(f"organic.{key}" in recipes, f"recipe generator consumes configured {key}")
    for removed in ("crushed_raw_uranium", "uranium_fluid", "uranium_fluid_to_yellowcake", "enriched_yellowcake", "mechanical_crafting/uranium_rod", "mechanical_crafting/graphite_rod"):
        require(removed in recipes, f"baseline bypass is explicitly removed: {removed}")

    required_quest_items = [
        "kubejs:uranium_mineral_trace", "kubejs:uranium_bearing_fines", "kubejs:washed_uranium_concentrate",
        "kubejs:purified_uranium_compound", "kubejs:green_fuel_pellet", "kubejs:fired_fuel_pellet",
        "createnuclear:uranium_rod", "kubejs:empty_fuel_cladding", "kubejs:fuel_pellet_stack", "createnuclear:graphite_rod",
    ]
    for item in required_quest_items:
        require(item in chapter, f"Era 6 teaches {item}")
    for quest_id in [f"161000000000000{i}" for i in range(1, 9)] + [f"461000000000000{i}" for i in range(1, 4)]:
        require(f"quest.{quest_id}.title" in lang and f"quest.{quest_id}.quest_desc" in lang, f"quest {quest_id} is localized")

    all_chapters = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "config/ftbquests/quests/chapters").glob("*.snbt"))
    ids = set(re.findall(r'(?m)^\s*id:\s*"([0-9A-F]+)"', all_chapters))
    dependencies = re.findall(r'dependencies:\s*\[(.*?)\]', all_chapters, re.S)
    referenced = {value for block in dependencies for value in re.findall(r'"([0-9A-F]+)"', block)}
    require(not (referenced - ids), "all quest dependencies resolve after the Era 6 rewrite")

    u = config["uranium"]
    g = config["graphite"]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join([
        "# Create Nuclear Phase I Investigation",
        "",
        "## Installed baseline",
        "",
        "- Exact build: `createnuclear-1.3.2-beta.3-neoforge.jar` for Minecraft 1.21.1 and Create 6.0.8+.",
        "- The reactor blueprint remains a fixed 57-position pattern serialized as slot/item records plus uranium and graphite counts/timers.",
        "- The controller evaluates exact `createnuclear:uranium_rod` and `createnuclear:graphite_rod` items, four orthogonal neighbors, signed heat, and a three-uranium-per-graphite overflow condition.",
        "- Uranium and graphite lifetimes default to 3,600 ticks. Maximum heat is 1,000. The configured failure countdown is 600 ticks, preserving an observable intervention window.",
        "- The reactor input exposes two item slots: uranium fuel and graphite. The output converts controller heat into generated rotational speed.",
        "- The installed reactor output registers 10,240 SU of stress capacity per RPM, independently of its heat-to-RPM calculation.",
        "",
        "## Phase boundary",
        "",
        "KubeJS/datapacks can safely own ore drops, intermediates, fluids, Create recipes, bypass removal, quests, and JEI-visible guidance. They cannot make new rod classes behave differently because the installed controller and input inventory check exact items and hardcode uranium/graphite behavior. Generalized component profiles therefore belong to a compiled Phase II patch.",
        "",
        "## Output scaling trial",
        "",
        "The installed 10,240 SU-per-RPM reactor-output capacity is overridden to 1,024, a 90% reduction. Reactor heat, heat thresholds, generated RPM, fuel lifetime, cooling behavior, and failure timing are unchanged. The value is centralized as `reactorOutput.stressCapacityPerRpm` in `nuclear_fuel_cycle.json` and can be tuned without rebuilding the addon.",
        "",
        "## Implemented uranium factory",
        "",
        f"`{u['trace']}` -> `{u['fines']}` -> `{u['washedConcentrate']}` -> `{u['slurry']}` -> `{u['purifiedCompound']}` -> `{u['fuelPowder']}` -> `{u['greenPellet']}` -> `{u['firedPellet']}` -> `{u['pelletStack']}` -> `{u['incompleteRod']}` -> `{u['finishedRod']}`",
        "",
        "One nine-trace chemical batch produces four purified compounds. Each compound yields two powder charges, creating the eight pellets required for one standard rod. The chain consumes the established kelp-derived chelating broth and saponified botanical binder and produces contained tailings plus spent solution.",
        "",
        "## Implemented graphite factory",
        "",
        f"Coal/charcoal -> `{g['carbonFines']}` -> `{g['washedCarbon']}` -> `{g['refinedCarbon']}` -> `{g['boundGraphite']}` -> `{g['greenBlank']}` -> `{g['bakedBlank']}` -> `{g['purifiedBlank']}` -> `{g['component']}` -> `{g['finishedRod']}`",
        "",
        "The graphite line reuses tannic pulp as a renewable binder, then washes, bakes, chemically purifies, machines, and mechanically frames the material. Phase I retains the installed rod's legacy cooling behavior; Phase II will reclassify it as moderation.",
        "",
        "## Bypass policy",
        "",
        "The installed crushed-uranium, liquid-uranium, yellowcake, fan-enrichment, direct rod, coal-dust, graphene, and direct graphite-rod recipes are removed. Ore, raw uranium, raw blocks, and crushed uranium cannot output raw uranium, uranium dust, yellowcake, enriched yellowcake, or a finished Create Nuclear rod.",
        "",
    ]), encoding="utf-8")
    print("\nCreate Nuclear Phase I audit passed.")


if __name__ == "__main__":
    main()

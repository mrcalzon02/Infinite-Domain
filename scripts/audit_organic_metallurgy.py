from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MINERAL_PATH = ROOT / "kubejs/config/mineral_trace_ore_processing.json"
CHEMISTRY_PATH = ROOT / "kubejs/config/organic_metallurgy.json"
STARTUP_PATH = ROOT / "kubejs/startup_scripts/mineral_trace_items.js"
RECIPE_PATH = ROOT / "kubejs/server_scripts/organic_metallurgy.js"
BYPASS_PATH = ROOT / "kubejs/server_scripts/mineral_trace_ore_processing.js"
CHAPTER_DIR = ROOT / "config/ftbquests/quests/chapters"
LANG_PATH = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REPORT_PATH = ROOT / "docs/organic-metallurgy-processing-matrix.md"


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)
    print(f"PASS  {message}")


def quest_id(era: int, number: int) -> str:
    return f"7{era}11{number:012X}"


def generate_report(minerals: dict, chemistry: dict) -> None:
    normal_average = (minerals["balance"]["minimumTracesPerOre"] + minerals["balance"]["maximumTracesPerOre"]) / 2
    deep_bonus = (minerals["balance"]["minimumDeepslateBonus"] + minerals["balance"]["maximumDeepslateBonus"]) / 2
    deepslate_average = normal_average + deep_bonus
    eras = chemistry["eras"]
    lines = [
        "# Organic Chemistry and Metallurgy Processing Matrix",
        "",
        "Generated from the two authoritative KubeJS configuration files. Yields are deterministic recovery budgets, not stacked multipliers.",
        "",
        "## Era chemistry",
        "",
        "| Era | Route | Renewable feedstock | Reagent | Nuggets / 9 traces | Recovery | Reagent used / ingot | Returned / batch | Stages | Principal machines |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for era in eras:
        reagent_per_ingot = chemistry["shared"]["reagentPerBatchMb"] * 9 / era["recoveryNuggets"]
        lines.append(
            f"| {era['era']} | {era['name']} | `{era['feedstock']}` | {era['reagentName']} | "
            f"{era['recoveryNuggets']} | {era['recoveryNuggets'] / 9:.0%} | {reagent_per_ingot:.1f} mB | "
            f"{era['recoveredMb']} mB | {era['processStages']} | {', '.join(era['machines'])} |"
        )
    lines += [
        "",
        "Primitive recovery is 9 nuggets per 9 traces (100%) and consumes no fluid reagent. Era 5 begins partial solution recovery; Eras 6–8 progressively close the loop.",
        "",
        "## Metal families and expected ore value",
        "",
        f"Average ordinary extraction is {normal_average:.1f} traces; average deepslate extraction is {deepslate_average:.1f} traces. The deepslate difference is additive at extraction and disappears once traces exist.",
        "",
        "| Metal | Family | Introduced | Primitive ingots / normal ore | Mechanical | Early chemical | Advanced Era 8 | Primitive ingots / deepslate ore | Era 8 / deepslate ore |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    metal_names = {metal["id"]: metal["name"] for metal in minerals["metals"]}
    for profile in chemistry["metalProfiles"]:
        primitive_normal = normal_average / 9
        mech_normal = normal_average * 10 / 81
        chemical_normal = normal_average * 13 / 81
        advanced_normal = normal_average * 19 / 81
        primitive_deep = deepslate_average / 9
        advanced_deep = deepslate_average * 19 / 81
        lines.append(
            f"| {metal_names[profile['id']]} | {profile['family'].replace('_', ' ').title()} | Era {profile['introducedEra']} | "
            f"{primitive_normal:.3f} | {mech_normal:.3f} | {chemical_normal:.3f} | {advanced_normal:.3f} | "
            f"{primitive_deep:.3f} | {advanced_deep:.3f} |"
        )
    lines += [
        "",
        "A rare raw chunk represents seven traces. Its end-to-end value therefore ranges from 0.778 primitive ingots to 1.642 Era 8 ingots before any optional secondary byproduct. Fortune changes trace extraction only and never affects these processing ratios.",
        "",
        "## Family behavior",
        "",
        "- Ferrous material emphasizes renewable carbon, heat, washing, and foundry conversion.",
        "- Base metals emphasize fine grinding, organic washing, conditioning, and precipitation.",
        "- Precious metals use the same shared reagents but become especially valuable under selective late recovery.",
        "- Alloy-forming metals must be purified before alloying; alloy recipes are not ore-purification shortcuts.",
        "- Advanced metals enter only when their mining era is reached, then use the longest selective-extraction routes.",
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    minerals = json.loads(MINERAL_PATH.read_text(encoding="utf-8"))
    chemistry = json.loads(CHEMISTRY_PATH.read_text(encoding="utf-8"))
    startup = STARTUP_PATH.read_text(encoding="utf-8")
    recipes = RECIPE_PATH.read_text(encoding="utf-8")
    bypass = BYPASS_PATH.read_text(encoding="utf-8")

    # KubeJS server scripts share one global scope: a bare top-level `const`
    # collides across files (this bit the pack once: "redeclaration of const
    # organicMetallurgy"). The generator must keep its constants inside an IIFE.
    recipes_code = "\n".join(
        ln for ln in recipes.splitlines() if not ln.lstrip().startswith("//")
    ).strip()
    require(bool(re.match(r"\(\s*(?:\(\s*\)\s*=>|function\b)", recipes_code)),
            "recipe generator is IIFE-scoped so its constants do not leak into the shared scope")

    metals = {metal["id"] for metal in minerals["metals"] if metal.get("processingClass") != "nuclear"}
    profiles = chemistry["metalProfiles"]
    require({profile["id"] for profile in profiles} == metals, "every non-nuclear trace metal has exactly one family/era profile")
    require(len({profile["id"] for profile in profiles}) == len(profiles), "metal profile IDs are unique")
    require({profile["family"] for profile in profiles} == {"ferrous", "base", "precious", "alloy_forming", "advanced"}, "five centralized metal families")

    eras = chemistry["eras"]
    require([era["era"] for era in eras] == list(range(1, 9)), "one chemistry ribbon for every numbered era")
    require([era["recoveryNuggets"] for era in eras] == [10, 11, 13, 15, 16, 17, 18, 19], "monotonic deterministic recovery curve")
    require(all(a["processStages"] < b["processStages"] for a, b in zip(eras, eras[1:])), "later routes always contain more stages")
    require([era["recoveredMb"] for era in eras] == sorted(era["recoveredMb"] for era in eras), "reagent recycling never regresses")
    require(len({era["reagent"] for era in eras}) == 8 and len({era["extract"] for era in eras}) == 8, "shared era reagents without metal-specific chemical clutter")

    require("StartupEvents.registry('fluid'" in startup and "StartupEvents.registry('item'" in startup, "custom solids and fluids are startup-registered")
    for marker in ("create.milling", "create.crushing", "create.mixing", "create.compacting", "create.pressing", "createmetallurgy:melting"):
        require(marker in recipes, f"recipe generator uses {marker}")
    require("create.splashing" not in recipes,
            "no splashing (Encased Fan wash) route - washing is a Mechanical Mixer / compacting step")
    for marker in ("output: metal.nugget", "createmetallurgy:melting/${metal.id}", "createmetallurgy:bulk_melting/${metal.id}"):
        require(marker in bypass, f"bypass removal covers {marker}")

    create_jar = next((ROOT / "mods").glob("create-1.21.1-*.jar"))
    metallurgy_jar = next((ROOT / "mods").glob("createmetallurgy-*.jar"))
    with zipfile.ZipFile(create_jar) as jar:
        names = jar.namelist()
        require(any("MillingRecipe" in name for name in names), "installed Create jar exposes milling recipes")
    with zipfile.ZipFile(metallurgy_jar) as jar:
        names = set(jar.namelist())
        require("data/createmetallurgy/recipe/casting_in_table/iron/nugget.json" in names, "installed Create: Metallurgy has nugget casting")
        sample = json.loads(jar.read("data/createmetallurgy/recipe/melting/iron/ingot.json"))
        require(sample["type"] == "createmetallurgy:melting" and "heat_requirement" in sample, "custom melting schema matches installed 1.21.1 build")

    all_chapters = list(CHAPTER_DIR.glob("*.snbt"))
    quest_ids: set[str] = set()
    all_text = ""
    for chapter in all_chapters:
        text = chapter.read_text(encoding="utf-8")
        all_text += text
        quest_ids.update(re.findall(r'^\t\t\tid: "([0-9A-F]{16})"$', text, re.MULTILINE))
    dependencies = set(re.findall(r'dependencies: \[([^\]]*)\]', all_text))
    referenced = {value for group in dependencies for value in re.findall(r'"([0-9A-F]{16})"', group)}
    require(referenced <= quest_ids, f"all quest dependencies resolve ({len(referenced)} referenced IDs)")
    expected = {quest_id(0, n) for n in range(1, 5)} | {quest_id(era, n) for era in range(1, 9) for n in range(1, 7)}
    require(expected <= quest_ids and len(expected) == 52, "all 52 processing-ribbon quests are installed")
    language = LANG_PATH.read_text(encoding="utf-8")
    require(all(f"quest.{qid}.title:" in language for qid in expected), "all processing quests are localized")

    generate_report(minerals, chemistry)
    require(REPORT_PATH.is_file(), "processing matrix and end-to-end balance report generated")
    print("\nOrganic metallurgy audit passed.")


if __name__ == "__main__":
    main()

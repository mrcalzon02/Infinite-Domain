from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
AE2_CHAPTER = ROOT / "config/ftbquests/quests/chapters/applied_energistics_recovery.snbt"
ERA5_CHAPTER = ROOT / "config/ftbquests/quests/chapters/era_05_automated_industry.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
CONFIG = ROOT / "config/createappliedkinetics-common.toml"
REGISTRY = ROOT / "docs/registry-inventory/item-ids.txt"
RECIPE_OUTPUTS = ROOT / "docs/recipe-index/recipe-outputs.csv"
ME_PROXY_RECIPE = ROOT / "kubejs/data/createappliedkinetics/recipe/me_proxy.json"
INSCRIBER_RECIPE = ROOT / "kubejs/data/ae2/recipe/network/blocks/inscribers.json"
MOD_JAR = ROOT / "mods/createappliedkinetics-1.5.3-1.21.1.jar"
AE2_GENERATOR = ROOT / "scripts/generators/build_quest_expansion.js"
ERA_GENERATOR = ROOT / "scripts/generators/generate_eras_2_8.js"


def quest_block(source: str, quest_id: str) -> str:
    marker = f'id: "{quest_id}"'
    marker_at = source.index(marker)
    start = source.rfind("\n\t\t{", 0, marker_at)
    end = source.index("\n\t\t}", marker_at) + len("\n\t\t}")
    return source[start:end]


def task_items(block: str) -> list[str]:
    tasks = re.search(r"tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:", block)
    assert tasks, "Quest block has no parseable task list"
    return re.findall(
        r'item:\s*\{\s*count:\s*1,\s*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"\s*\}',
        tasks.group(1),
    )


def kinetic_recipe(archive: ZipFile, recipe_name: str, expected_output: str) -> dict:
    path = f"data/ae2/recipe/inscriber/{recipe_name}.json"
    payload = json.loads(archive.read(path))
    branches = payload.get("recipes", [])
    assert len(branches) == 2, f"{recipe_name} must retain kinetic and Inscriber conditional branches"
    kinetic = branches[0]
    assert kinetic.get("conditions") == [{"type": "createappliedkinetics:ae2_overwrite"}], (
        f"{recipe_name} must select the kinetic branch from the enabled config condition"
    )
    recipe = kinetic.get("recipe", {})
    assert recipe.get("type") == "create:sequenced_assembly", f"{recipe_name} is no longer sequenced assembly"
    results = recipe.get("results", [])
    assert any(entry.get("item") == expected_output for entry in results), f"{recipe_name} has the wrong output"
    transitional = recipe.get("transitionalItem", {}).get("item", "")
    assert transitional.startswith("createappliedkinetics:incomplete_"), f"{recipe_name} lost its transitional item"
    return recipe


ae2_chapter = AE2_CHAPTER.read_text(encoding="utf-8")
era5_chapter = ERA5_CHAPTER.read_text(encoding="utf-8")
language = LANG.read_text(encoding="utf-8")
registry = set(REGISTRY.read_text(encoding="utf-8-sig").splitlines())

assert re.search(r"^overwrite_ae2_recipes\s*=\s*true\s*$", CONFIG.read_text(encoding="utf-8"), re.MULTILINE), (
    "Create: Applied Kinetics recipe replacement must remain enabled"
)

processor_quest = quest_block(ae2_chapter, "5A00000000000004")
assert task_items(processor_quest) == ["ae2:logic_processor"], (
    "The first AE2 processing quest must teach the kinetic Logic Processor, not the ordinary Inscriber workflow"
)
processor_language = language[
    language.index("quest.5A00000000000004.quest_desc:"):
    language.index("quest.5A00000000000005.quest_desc:")
]
assert "Create: Applied Kinetics" in processor_language, (
    "The first kinetic processor lesson must name the mod explicitly"
)

power_quest = quest_block(ae2_chapter, "5A00000000000009")
assert task_items(power_quest) == ["ae2:energy_acceptor", "createappliedkinetics:energy_provider"], (
    "The powered-network milestone must require both halves of the kinetic-to-ME bridge"
)
assert 'icon: "createappliedkinetics:energy_provider"' in power_quest, "The two-task power bridge needs an explicit icon"

proxy_quest = quest_block(ae2_chapter, "5A00000000000020")
assert 'dependencies: ["5A0000000000000A"]' in proxy_quest, "ME Proxy must follow a powered terminal"
assert "optional: true" in proxy_quest and task_items(proxy_quest) == ["createappliedkinetics:me_proxy"]

trial_quest = quest_block(ae2_chapter, "5A00000000000021")
assert 'dependencies: ["5A00000000000020"]' in trial_quest, "Transfer trial must follow ME Proxy construction"
assert "optional: true" in trial_quest and 'type: "checkmark"' in trial_quest
assert "rewards:" not in trial_quest, "A witnessed transfer checkmark must not grant a material reward"
assert "task.6A00000000000021.title:" in language, "The witnessed procedure needs a localized instruction"

era5_inscriber = quest_block(era5_chapter, "3510000000000002")
assert task_items(era5_inscriber) == ["ae2:inscriber"], "The specialist Inscriber compatibility objective must stay intact"
inscriber_language = language[language.index("quest.3510000000000002.title:"):language.index("quest.3510000000000003.title:")]
assert "Create: Applied Kinetics" in inscriber_language and "AE2 Lightning Tech" in inscriber_language, (
    "The specialist Inscriber quest must distinguish compatibility recipes from ordinary processors"
)

era5_processors = quest_block(era5_chapter, "3510000000000004")
expected_processors = ["ae2:logic_processor", "ae2:calculation_processor", "ae2:engineering_processor"]
assert task_items(era5_processors) == expected_processors, "Era 5 must prove all three processor lines"
for item in expected_processors:
    assert re.search(rf'count:\s*8L[\s\S]*?id:\s*"{re.escape(item)}"', era5_processors), f"{item} target must stay at 8"

all_task_items = (
    task_items(processor_quest)
    + task_items(power_quest)
    + task_items(proxy_quest)
    + task_items(era5_inscriber)
    + task_items(era5_processors)
)
missing_items = sorted(set(all_task_items) - registry)
assert not missing_items, f"Unregistered AE2/Create integration task items: {missing_items}"

assert MOD_JAR.is_file(), "Installed Create: Applied Kinetics 1.5.3 jar is missing"
with ZipFile(MOD_JAR) as archive:
    kinetic_recipe(archive, "silicon_print", "ae2:printed_silicon")
    kinetic_recipe(archive, "logic_processor", "ae2:logic_processor")
    kinetic_recipe(archive, "calculation_processor", "ae2:calculation_processor")
    kinetic_recipe(archive, "engineering_processor", "ae2:engineering_processor")

    press_recipe = kinetic_recipe(archive, "engineering_processor_press", "ae2:engineering_processor_press")
    deploy = press_recipe.get("sequence", [])[0]
    assert deploy.get("type") == "create:deploying" and deploy.get("keepHeldItem") is True, (
        "Recovered processor presses must remain non-consumptive templates in the kinetic copy line"
    )

    energy_provider = json.loads(archive.read("data/createappliedkinetics/recipe/energy_provider.json"))
    assert energy_provider.get("type") == "create:mechanical_crafting"
    assert energy_provider.get("result", {}).get("id") == "createappliedkinetics:energy_provider"
    provider_inputs = {entry.get("item") for entry in energy_provider.get("key", {}).values()}
    assert {"create:brass_casing", "create:precision_mechanism", "create:copper_sheet"} <= provider_inputs

proxy_recipe = json.loads(ME_PROXY_RECIPE.read_text(encoding="utf-8"))
assert proxy_recipe.get("result", {}).get("id") == "createappliedkinetics:me_proxy"
proxy_inputs = [entry.get("item") for entry in proxy_recipe.get("key", {}).values()]
assert proxy_inputs.count("allthecompressed:iron_block_2x") == 1, "ME Proxy must retain its compressed-iron gate"
assert "".join(proxy_recipe.get("pattern", [])).count("a") == 4, "ME Proxy must retain four compressed-iron positions"
assert {"ae2:annihilation_core", "ae2:formation_core", "ae2:logic_processor"} <= set(proxy_inputs)

inscriber_recipe = json.loads(INSCRIBER_RECIPE.read_text(encoding="utf-8"))
assert inscriber_recipe.get("result", {}).get("id") == "ae2:inscriber"
assert {entry.get("item") for entry in inscriber_recipe.get("key", {}).values()} == {
    "create_new_age:copper_wire_block",
    "powergrid:copper_coil",
    "create:mechanical_press",
    "ae2:fluix_block",
}, "The specialist Inscriber must retain its Era 4/5 cross-mod reconstruction gate"

with RECIPE_OUTPUTS.open(encoding="utf-8-sig", newline="") as handle:
    output_rows = list(csv.DictReader(handle))
specialist_inscriber_recipes = {
    row["recipe_id"]
    for row in output_rows
    if row.get("enabled") == "True" and row.get("recipe_type") == "ae2:inscriber" and row.get("output_namespace") == "ae2lt"
}
assert {
    "ae2lt:inscriber/overload_circuit_board",
    "ae2lt:inscriber/overload_crystal_dust",
    "ae2lt:inscriber/overload_processor",
} <= specialist_inscriber_recipes, "The retained Inscriber must still have enabled AE2LT specialist work"

ae2_generator = AE2_GENERATOR.read_text(encoding="utf-8")
for token in (
    "Processors in Motion",
    "createappliedkinetics:energy_provider",
    "5A00000000000020",
    "5A00000000000021",
    "optional: true",
):
    assert token in ae2_generator, f"AE2 generator does not preserve {token}"

era_generator = ERA_GENERATOR.read_text(encoding="utf-8")
for token in (
    "The Specialist Inscriber",
    "Create: Applied Kinetics sequenced-assembly chains",
    "ae2:calculation_processor",
    "ae2:engineering_processor",
    "extraItemTasks",
):
    assert token in era_generator, f"Era generator does not preserve {token}"

print(
    "Create: Applied Kinetics audit passed: 2 repaired AE2 milestones, "
    "2 optional integration quests, 3 Era 5 processor objectives, 5 kinetic recipes, "
    "2 bridge-block recipes, and 3 specialist Inscriber recipes verified."
)

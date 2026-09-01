"""Build Cyberspace/Darknet hostile spawns and the Darknet dragon campaign."""

from __future__ import annotations

import json
from pathlib import Path


def snbt(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


ROOT = Path(__file__).resolve().parents[2]
MODIFIERS = ROOT / "kubejs/data/infinite_domain/neoforge/biome_modifier"
RECIPES = ROOT / "kubejs/data/infinite_domain/recipe"
CHAPTER = ROOT / "config/ftbquests/quests/chapters/darknet_draconic_convergence.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
BEGIN = "\t// BEGIN GENERATED DARKNET DRACONIC CONVERGENCE"
END = "\t// END GENERATED DARKNET DRACONIC CONVERGENCE"
GROUP = "569AB980347C1123"
CHAPTER_ID = "381AB56C38F92B74"
CYBERSPACE_ENTRY = "5B00000000000011"

MEKANITES = {
    "drone": ("mekanite_mobs:drone", 20, 1, 3),
    "creeper": ("mekanite_mobs:mekanite_creeper", 23, 2, 5),
    "enderman": ("mekanite_mobs:mekanite_enderman", 16, 2, 3),
    "illusioner": ("mekanite_mobs:mekanite_illusioner", 18, 2, 3),
    "ravager": ("mekanite_mobs:mekanite_ravager", 16, 1, 1),
    "skeleton": ("mekanite_mobs:mekanite_skeleton", 23, 2, 5),
    "slime_big": ("mekanite_mobs:mekanite_slime", 18, 1, 3),
    "slime_medium": ("mekanite_mobs:mekanite_slime_medio", 22, 2, 4),
    "slime_small": ("mekanite_mobs:mekanite_slime_small", 28, 4, 6),
    "spider": ("mekanite_mobs:mekanite_spider", 26, 3, 4),
    "vindicator": ("mekanite_mobs:mekanite_vindicator", 22, 3, 6),
    "witch": ("mekanite_mobs:mekanite_witch", 21, 1, 3),
    "zombie": ("mekanite_mobs:mekanite_zombie", 25, 2, 6),
    "drowned": ("mekanite_mobs:mekanite_zombie_drowned", 20, 3, 8),
    "husk": ("mekanite_mobs:mekanite_zombie_husk", 20, 4, 8),
}

DRAGONS = {
    "fire_dragon": "iceandfire:fire_dragon",
    "ice_dragon": "iceandfire:ice_dragon",
    "lightning_dragon": "iceandfire:lightning_dragon",
}

INJECTOR_SECONDS = [30, 60, 120, 240, 480, 960, 1920, 3840]
INJECTOR_UPGRADES = [
    "ae2:logic_processor",
    "ae2:cell_component_1k",
    "ae2:calculation_processor",
    "ae2:cell_component_4k",
    "ae2:engineering_processor",
    "ae2:cell_component_16k",
    "ae2:cell_component_64k",
]


def item(item_id: str, count: int, name: str, consume: bool = False) -> dict:
    return {"kind": "item", "id": item_id, "count": count, "name": name, "consume": consume}


def kill(entity: str, count: int, name: str) -> dict:
    return {"kind": "kill", "id": entity, "count": count, "name": name}


def dimension(dimension_id: str, name: str) -> dict:
    return {"kind": "dimension", "id": dimension_id, "name": name}


def advancement(advancement_id: str, name: str) -> dict:
    return {"kind": "advancement", "id": advancement_id, "name": name}


def check(name: str) -> dict:
    return {"kind": "checkmark", "name": name}


def quest(title: str, desc: list[str], icon: str, x: float, y: float, tasks: list[dict],
          deps: list[int | str], reward: str | None = "kubejs:era8_supply_bag", shape: str = "circle") -> dict:
    return {"title": title, "desc": desc, "icon": icon, "x": x, "y": y, "tasks": tasks,
            "deps": deps, "reward": reward, "shape": shape}


QUESTS = [
    quest("A Less Reputable Connection", [
        "Acquire a Netcracker. Open the nearby Terminal's inventory and place the Netcracker in its hardware slot; the ordinary Cyberspace link will expose a Darknet connection while it remains installed.",
        "Yes, the illegal-looking cartridge goes into the conspicuously empty computer slot. The design is not subtle. It merely had the decency to omit a manual.",
    ], "cyberspace:netcracker", 0, 0, [item("cyberspace:netcracker", 1, "Netcracker")], [CYBERSPACE_ENTRY]),
    quest("One Hundred Seconds of Bad Decisions", [
        "Select the Darknet connection in the Terminal. The transfer takes two seconds. Your first connection lands at a random Darknet position; later connections remember the last Darknet coordinates.",
        "A 100-second countdown begins on arrival. When it expires, the system forcibly returns you to the Overworld coordinates recorded when the connection started. Do not move the Terminal, obstruct the return point, or confuse a timer with an invitation to sightsee.",
        "The Darknet is now occupied by Mekanite war machines and all three draconic species. Arrive armored, carry ranged damage, and plan what can actually be accomplished inside five thousand ticks.",
    ], "cyberspace:darknet_block", 0, 4, [dimension("cyberspace:darknet_dimension", "Darknet")], [0], shape="diamond"),
    quest("Darknet Data Extraction", [
        "Install a Data Extractor in the same Terminal hardware slot when you intend to recover data rather than open the Darknet link. Bring back Data Hardware as proof that the trip produced something besides elevated pulse rate.",
        "The slot accepts one specialist tool at a time. Swap deliberately; staring at the absent Darknet command while the wrong module is installed will not improve the interface.",
    ], "cyberspace:data_extractor", -4, 8,
        [item("cyberspace:data_extractor", 1, "Data Extractor"), item("cyberspace:data_hardware", 1, "Data Hardware")], [1]),
    quest("Return Before the Carrier Drops", [
        "Complete one Darknet incursion and return alive. Falling below elevation 48 imposes Darkness, although the dimension suppresses fall distance; neither feature makes the lower void a sensible extraction route.",
        "The timer is the reliable exit. The default Leave Cyberspace key is for Cyberspace; do not build a Darknet plan around an exit control that the Darknet session already replaces with forced recall.",
    ], "cyberspace:riftmaker", 4, 8,
        [item("cyberspace:riftmaker", 1, "Riftmaker"), check("Complete a timed Darknet incursion and return alive")], [1], reward=None),

    quest("Fire Signature in the Dark", [
        "Ice and Fire supplies the dragons, trophies, materials, and Dragonforge industry encountered in this campaign.",
        "Kill a Fire Dragon in the Darknet. Treat the flat horizon as a firing lane for both parties and remember that the countdown continues while you admire the target.",
        "Wild dragons are not tameable. If you want one that obeys, you will need an egg from a high-stage female and the patience to raise what hatches.",
    ], "iceandfire:dragon_skull_fire", -12, 12, [kill("iceandfire:fire_dragon", 1, "Fire Dragon")], [3]),
    quest("Fire Dragon Specimens", [
        "Recover the heart, blood, flesh, skull, bones, and red scales from the corpse. Loot a fallen dragon by interacting with its body; waiting for it to behave like an ordinary item fountain is charmingly optimistic.",
    ], "iceandfire:fire_dragon_heart", -12, 16, [
        item("iceandfire:fire_dragon_heart", 1, "Fire Dragon Heart"), item("iceandfire:fire_dragon_blood", 1, "Fire Dragon Blood"),
        item("iceandfire:fire_dragon_flesh", 4, "Fire Dragon Flesh"), item("iceandfire:dragon_skull_fire", 1, "Fire Dragon Skull"),
        item("iceandfire:dragonbone", 16, "Dragon Bone"), item("iceandfire:dragonscales_red", 8, "Red Dragon Scales")], [4]),
    quest("Fire Dragonforge Plant", [
        "Construct the active components for a Fire Dragonforge: seventeen Fire Dragonforge Bricks, one Fire Dragonforge Core, and one Fire Dragonforge Input. The assembled forge must receive breath from a Stage 2 or older Fire Dragon.",
        "This is a multiblock industrial furnace powered by a living siege weapon. Give the breath path clearance and stop calling the animal a fuel line where it can hear you.",
    ], "iceandfire:dragonforge_fire_core_disabled", -12, 20, [
        item("iceandfire:dragonforge_fire_brick", 17, "Fire Dragonforge Brick"), item("iceandfire:dragonforge_fire_core_disabled", 1, "Fire Dragonforge Core"),
        item("iceandfire:dragonforge_fire_input", 1, "Fire Dragonforge Input")], [5]),
    quest("Fire Dragonsteel", [
        "Use the completed Fire Dragonforge to produce four Fire Dragonsteel Ingots. The dragon supplies the breath; the forge supplies containment; your contribution is keeping both pointed at the correct aperture.",
    ], "iceandfire:dragonsteel_fire_ingot", -12, 24, [item("iceandfire:dragonsteel_fire_ingot", 4, "Fire Dragonsteel Ingot")], [6], reward="kubejs:era8_priority_cache", shape="gear"),

    quest("Ice Signature in the Dark", [
        "Kill an Ice Dragon in the Darknet. Cover remains useful until the breath freezes the terrain around it, at which point your carefully selected position becomes a sculpture commemorating misplaced confidence.",
    ], "iceandfire:dragon_skull_ice", 0, 12, [kill("iceandfire:ice_dragon", 1, "Ice Dragon")], [3]),
    quest("Ice Dragon Specimens", [
        "Recover the heart, blood, flesh, skull, bones, and blue scales. The elemental material is the technological point of this expedition; the enormous corpse was not killed merely to improve your decorating options.",
    ], "iceandfire:ice_dragon_heart", 0, 16, [
        item("iceandfire:ice_dragon_heart", 1, "Ice Dragon Heart"), item("iceandfire:ice_dragon_blood", 1, "Ice Dragon Blood"),
        item("iceandfire:ice_dragon_flesh", 4, "Ice Dragon Flesh"), item("iceandfire:dragon_skull_ice", 1, "Ice Dragon Skull"),
        item("iceandfire:dragonbone", 16, "Dragon Bone"), item("iceandfire:dragonscales_blue", 8, "Blue Dragon Scales")], [8]),
    quest("Ice Dragonforge Plant", [
        "Construct seventeen Ice Dragonforge Bricks, one Ice Dragonforge Core, and one Ice Dragonforge Input. A Stage 2 or older Ice Dragon must breathe into the input to operate the assembled forge.",
        "Water management belongs outside the breath channel. Freezing the workshop floor is not a refrigeration system; it is a staffing problem.",
    ], "iceandfire:dragonforge_ice_core_disabled", 0, 20, [
        item("iceandfire:dragonforge_ice_brick", 17, "Ice Dragonforge Brick"), item("iceandfire:dragonforge_ice_core_disabled", 1, "Ice Dragonforge Core"),
        item("iceandfire:dragonforge_ice_input", 1, "Ice Dragonforge Input")], [9]),
    quest("Ice Dragonsteel", [
        "Use the completed Ice Dragonforge to produce four Ice Dragonsteel Ingots. If the dragon is present but the forge is idle, inspect the multiblock and breath alignment before accusing a reptile of poor process control.",
    ], "iceandfire:dragonsteel_ice_ingot", 0, 24, [item("iceandfire:dragonsteel_ice_ingot", 4, "Ice Dragonsteel Ingot")], [10], reward="kubejs:era8_priority_cache", shape="gear"),

    quest("Lightning Signature in the Dark", [
        "Kill a Lightning Dragon in the Darknet. Spread out, avoid conductive clutter, and do not mistake a flat arena for safety when the target's preferred geometry is a bolt from above.",
    ], "iceandfire:dragon_skull_lightning", 12, 12, [kill("iceandfire:lightning_dragon", 1, "Lightning Dragon")], [3]),
    quest("Lightning Dragon Specimens", [
        "Recover the heart, blood, flesh, skull, bones, and electric-blue scales. Keep the samples isolated until the laboratory has earned the right to discover which storage cabinet conducts electricity.",
    ], "iceandfire:lightning_dragon_heart", 12, 16, [
        item("iceandfire:lightning_dragon_heart", 1, "Lightning Dragon Heart"), item("iceandfire:lightning_dragon_blood", 1, "Lightning Dragon Blood"),
        item("iceandfire:lightning_dragon_flesh", 4, "Lightning Dragon Flesh"), item("iceandfire:dragon_skull_lightning", 1, "Lightning Dragon Skull"),
        item("iceandfire:dragonbone", 16, "Dragon Bone"), item("iceandfire:dragonscales_electric", 8, "Electric Dragon Scales")], [12]),
    quest("Lightning Dragonforge Plant", [
        "Construct seventeen Lightning Dragonforge Bricks, one Lightning Dragonforge Core, and one Lightning Dragonforge Input. Power the completed forge with the breath of a Stage 2 or older Lightning Dragon.",
        "Ground the surrounding installation. 'It only arcs when operating' is a diagnosis, not a safety certification.",
    ], "iceandfire:dragonforge_lightning_core_disabled", 12, 20, [
        item("iceandfire:dragonforge_lightning_brick", 17, "Lightning Dragonforge Brick"), item("iceandfire:dragonforge_lightning_core_disabled", 1, "Lightning Dragonforge Core"),
        item("iceandfire:dragonforge_lightning_input", 1, "Lightning Dragonforge Input")], [13]),
    quest("Lightning Dragonsteel", [
        "Use the completed Lightning Dragonforge to produce four Lightning Dragonsteel Ingots. Congratulations: the lightning-breathing apex predator is now a qualified metallurgical subprocess.",
    ], "iceandfire:dragonsteel_lightning_ingot", 12, 24, [item("iceandfire:dragonsteel_lightning_ingot", 4, "Lightning Dragonsteel Ingot")], [14], reward="kubejs:era8_priority_cache", shape="gear"),

    quest("An Egg Is Not Salvage", [
        "Recover a Dragon Egg from a Stage 4 or Stage 5 female. The species and color may vary; the important distinction is that an egg is a future tamed dragon, not another crafting component to leave in an unsorted chest.",
    ], "iceandfire:dragonegg_red", 0, 28, [advancement("iceandfire:iceandfire/dragon_egg", "Obtain a Dragon Egg")], [7, 11, 15], shape="diamond"),
    quest("Incubation Is Elemental", [
        "Hatch the egg under the condition matching its species. Fire eggs remain in fire; Ice eggs remain in water until it freezes; Lightning eggs require open sky and active rain. Hatching takes several minutes and pauses if the condition fails.",
        "Stay nearby. A hatchling bonds to the nearby player as it emerges. Lightning incubation can ignite its surroundings, so keep water available unless your nursery plan includes an electrical fire.",
        "Prepare Dragon Meal as well. Each meal advances growth by one day; Stage 3 is the threshold for riding, not a reason to force-feed seventy-five portions in one sitting.",
    ], "iceandfire:dragon_meal", 0, 32, [item("iceandfire:dragon_meal", 8, "Dragon Meal"), check("Hatch and bond with a Dragon")], [16], reward=None),
    quest("Command, Recall, and Storage", [
        "Equip the basic husbandry set. The Dragon Command Staff changes behavior and sets a home position while sneaking. The Dragon Bone Flute calls a flying dragon down. The Dragon Horn stores and releases your own dragon for transport.",
        "Use the tools before trusting a growing dragon near machinery. Ownership is not the same thing as operational discipline, a distinction many managers also fail to grasp.",
    ], "iceandfire:dragon_stick", 0, 36, [
        item("iceandfire:dragon_stick", 1, "Dragon Command Staff"), item("iceandfire:dragon_flute", 1, "Dragon Bone Flute"),
        item("iceandfire:dragon_horn", 1, "Dragon Horn")], [17]),
    quest("Draconic Industrial Partnership", [
        "Raise a bonded dragon to Stage 3, ride it, and use its breath to operate the matching Dragonforge. This is the complete chain: Darknet expedition, specimen recovery, egg, husbandry, controlled breath, and reproducible Dragonsteel.",
        "The dragon is a partner and weapons platform, not disposable forge equipment. If that ethical distinction seems needlessly sentimental, compare the size of its teeth with the size of your employment contract.",
    ], "iceandfire:dragonarmor_netherite_body", 0, 40, [
        check("Raise and ride a Stage 3 bonded Dragon"), item("iceandfire:dragonarmor_netherite_head", 1, "Netherite Dragon Head Armor"),
        item("iceandfire:dragonarmor_netherite_neck", 1, "Netherite Dragon Neck Armor"), item("iceandfire:dragonarmor_netherite_body", 1, "Netherite Dragon Body Armor"),
        item("iceandfire:dragonarmor_netherite_tail", 1, "Netherite Dragon Tail Armor")], [18], reward=None, shape="rsquare"),
    quest("Three Breaths, One Industrial Doctrine", [
        "Compress the output of all three elemental Dragonforges into one block of Fire, Ice, and Lightning Dragonsteel. This is the auditable conclusion: every hunt, specimen chain, forge plant, and husbandry system is now independently productive.",
        "You have converted three categories of mythological catastrophe into reproducible metallurgy. I would congratulate you more warmly, but that might encourage another category.",
    ], "iceandfire:dragonsteel_lightning_block", 0, 44, [
        item("iceandfire:dragonsteel_fire_block", 1, "Fire Dragonsteel Block"), item("iceandfire:dragonsteel_ice_block", 1, "Ice Dragonsteel Block"),
        item("iceandfire:dragonsteel_lightning_block", 1, "Lightning Dragonsteel Block")], [19, 7, 11, 15],
        reward="kubejs:era8_priority_cache", shape="rsquare"),

    quest("Overworld Carrier Materials", [
        "Prepare the carrier hardware before entering the Darknet: Graphene-Coated Iron, Fluix Crystals, and Logic Processors are all manufacturable with the civilization already operating in the Overworld.",
        "Yes, preparation before entering the timed dragon dimension is permitted. I checked. It is even encouraged, despite the evidence supplied by your previous expeditions.",
    ], "cyberspace:graphene_coated_iron_ingot", -8, 32, [
        item("cyberspace:graphene_coated_iron_ingot", 8, "Graphene-Coated Iron Ingot"),
        item("ae2:fluix_crystal", 4, "Fluix Crystal"), item("ae2:logic_processor", 2, "Logic Processor")], [0]),
    quest("Bounded Temporal Core", [
        "Build a Darknet Temporal Core from a Virtual Machine Core, Quantum Cores, an Applied Energistics Energy Cell and Logic Processor, Graphene-Coated Iron, and Fiber Optics.",
        "Every part is available through Overworld civilization and the Cyberspace fabrication chain. Requiring interplanetary metals to buy thirty more seconds would have been less engineering than hazing.",
    ], "kubejs:darknet_temporal_core", -8, 36, [item("kubejs:darknet_temporal_core", 1, "Darknet Temporal Core")], [21], shape="gear"),
    quest("Session Injector Tier I", [
        "Build four Tier I Darknet Session Injectors. Each is consumed to add thirty seconds to an active session. Every higher tier consumes exactly one injector from the previous tier and doubles the granted time.",
        "Thirty seconds sounds modest because you are comparing it with safety rather than with forced dimensional ejection during a dragon fight.",
    ], "kubejs:darknet_session_injector_tier_1", -8, 40,
        [item("kubejs:darknet_session_injector_tier_1", 4, "Darknet Session Injector Tier I")], [22], shape="gear"),
    quest("Field-Test the Carrier Extension", [
        "Enter the Darknet and right-click any Session Injector while its carrier timer is active. The injector modifies and synchronizes Cyberspace's real countdown, consumes itself, and records this test automatically.",
        "It does nothing outside the Darknet or without an active timer. I have attempted to engineer out every obvious way you might feed valuable hardware to empty air. Surprise me elsewhere.",
    ], "kubejs:darknet_session_injector_tier_1", -8, 44,
        [advancement("infinite_domain:darknet_time_extended", "Extend an active Darknet session")], [23],
        reward="kubejs:era8_priority_cache", shape="diamond"),
    quest("Session Injector Tier II", [
        "Add a pair of Logic Processors to the carrier package. Tier II adds sixty seconds: exactly twice Tier I.",
    ], "kubejs:darknet_session_injector_tier_2", -12, 48,
        [item("kubejs:darknet_session_injector_tier_2", 1, "Darknet Session Injector Tier II")], [24], shape="gear"),
    quest("Session Injector Tier III", [
        "Install 1k Storage Components for a longer carrier-state buffer. Tier III adds one hundred twenty seconds, doubling Tier II.",
    ], "kubejs:darknet_session_injector_tier_3", -8, 52,
        [item("kubejs:darknet_session_injector_tier_3", 1, "Darknet Session Injector Tier III")], [25], shape="gear"),
    quest("Session Injector Tier IV", [
        "Introduce Calculation Processors to correct timing drift. Tier IV adds two hundred forty seconds, doubling Tier III.",
    ], "kubejs:darknet_session_injector_tier_4", -4, 56,
        [item("kubejs:darknet_session_injector_tier_4", 1, "Darknet Session Injector Tier IV")], [26], shape="gear"),
    quest("Session Injector Tier V", [
        "Expand the state buffer with 4k Storage Components. Tier V adds four hundred eighty seconds, doubling Tier IV.",
    ], "kubejs:darknet_session_injector_tier_5", 0, 60,
        [item("kubejs:darknet_session_injector_tier_5", 1, "Darknet Session Injector Tier V")], [27], shape="gear"),
    quest("Session Injector Tier VI", [
        "Replace the control package with Engineering Processors. Tier VI adds nine hundred sixty seconds, doubling Tier V.",
    ], "kubejs:darknet_session_injector_tier_6", 4, 56,
        [item("kubejs:darknet_session_injector_tier_6", 1, "Darknet Session Injector Tier VI")], [28], shape="gear"),
    quest("Session Injector Tier VII", [
        "Install 16k Storage Components. Tier VII adds one thousand nine hundred twenty seconds, doubling Tier VI, without requiring you to kill a dragon to obtain more time for killing dragons.",
    ], "kubejs:darknet_session_injector_tier_7", 8, 52,
        [item("kubejs:darknet_session_injector_tier_7", 1, "Darknet Session Injector Tier VII")], [29], shape="gear"),
    quest("Session Injector Tier VIII", [
        "Close the portable system with 64k Storage Components. Tier VIII adds three thousand eight hundred forty seconds: sixty-four minutes, exactly twice Tier VII and one hundred twenty-eight times Tier I.",
        "If sixty-four additional minutes in the dragon-filled Darknet still feels insufficient, the device is no longer the limiting component in this operation.",
    ], "kubejs:darknet_session_injector_tier_8", 12, 48,
        [item("kubejs:darknet_session_injector_tier_8", 1, "Darknet Session Injector Tier VIII")], [30],
        reward="kubejs:era8_priority_cache", shape="rsquare"),
    quest("Darknet Anchor", [
        "Combine a Tier VIII Session Injector and Darknet Temporal Core with Quantum Cores, Virtual Machine Cores, a 128 cubed Spatial Storage Component, and a Dense Energy Cell. The result is an Applied Energistics Spatial Anchor retuned for a permanent Darknet carrier.",
        "Place it only in the Darknet and connect it to a powered ME network. It binds to its placer, keeps its own network chunks loaded, and prevents the owner's active session timer from expiring anywhere in the dimension.",
        "One anchor per operator. Breaking it, destroying it, or losing ME power terminates the tether and recalls you to the recorded Overworld position. Dying destroys it outright. Apparently immortality still requires maintenance.",
    ], "ae2:spatial_anchor", 16, 44,
        [item("ae2:spatial_anchor", 1, "Darknet Anchor")], [31],
        reward="kubejs:era8_priority_cache", shape="hexagon"),
]


def qid(index: int) -> str:
    return f"5B10{index + 1:012X}"


def tid(index: int, sub: int) -> str:
    return f"6B1{index + 1:09X}{sub + 1:04X}"


def rid(index: int) -> str:
    return f"7B1{index + 1:012X}"


def write_spawns() -> None:
    MODIFIERS.mkdir(parents=True, exist_ok=True)
    for short, (entity, weight, minimum, maximum) in MEKANITES.items():
        data = {"type": "neoforge:add_spawns", "biomes": ["cyberspace:cyberspace_biome", "cyberspace:darknet_biome"],
                "spawners": {"type": entity, "weight": weight, "minCount": minimum, "maxCount": maximum}}
        (MODIFIERS / f"cyber_dimensions_mekanite_{short}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for short, entity in DRAGONS.items():
        data = {"type": "neoforge:add_spawns", "biomes": "cyberspace:darknet_biome",
                "spawners": {"type": entity, "weight": 1, "minCount": 1, "maxCount": 1}}
        (MODIFIERS / f"darknet_{short}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_injector_recipes() -> None:
    RECIPES.mkdir(parents=True, exist_ok=True)
    tier_one = {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "key": {
            "C": {"item": "kubejs:darknet_temporal_core"}, "F": {"item": "ae2:fluix_crystal"},
            "G": {"item": "cyberspace:graphene_coated_iron_ingot"},
            "L": {"item": "ae2:logic_processor"}, "E": {"item": "ae2:energy_cell"},
        },
        "pattern": ["FLF", "GCG", "FEF"],
        "result": {"count": 4, "id": "kubejs:darknet_session_injector_tier_1"},
    }
    (RECIPES / "darknet_session_injector_tier_1.json").write_text(json.dumps(tier_one, indent=2) + "\n", encoding="utf-8")
    for tier, upgrade in enumerate(INJECTOR_UPGRADES, start=2):
        data = {
            "type": "minecraft:crafting_shaped", "category": "misc",
            "key": {
                "G": {"item": "cyberspace:graphene_coated_iron_ingot"},
                "P": {"item": f"kubejs:darknet_session_injector_tier_{tier - 1}"},
                "U": {"item": upgrade},
            },
            "pattern": ["GUG", " P ", "GUG"],
            "result": {"count": 1, "id": f"kubejs:darknet_session_injector_tier_{tier}"},
        }
        (RECIPES / f"darknet_session_injector_tier_{tier}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def task_block(task: dict, task_id: str) -> str:
    if task["kind"] == "item":
        consume = "\t\t\t\tconsume_items: true\n" if task["consume"] else ""
        return "{\n" + consume + f'\t\t\t\tcount: {task["count"]}L\n\t\t\t\tid: "{task_id}"\n' + \
               f'\t\t\t\titem: {{ count: 1, id: {snbt(task["id"])} }}\n\t\t\t\ttype: "item"\n\t\t\t}}'
    field = {"kill": "entity", "dimension": "dimension", "advancement": "advancement"}.get(task["kind"])
    if field:
        count = f'\t\t\t\tvalue: {task["count"]}L\n' if task["kind"] == "kill" else ""
        return "{\n" + f'\t\t\t\t{field}: {snbt(task["id"])}\n\t\t\t\tid: "{task_id}"\n' + count + \
               f'\t\t\t\ttype: {snbt(task["kind"])}\n\t\t\t}}'
    return "{\n" + f'\t\t\t\tid: "{task_id}"\n\t\t\t\ttype: "checkmark"\n\t\t\t}}'


def write_quests() -> None:
    lines = ["{", "\tdefault_hide_dependency_lines: false", "\tdefault_quest_shape: \"circle\"",
             '\tfilename: "darknet_draconic_convergence"', f'\tgroup: "{GROUP}"', f'\tid: "{CHAPTER_ID}"', '\ticon: "cyberspace:netcracker"',
             "\timages: [ ]", "\torder_index: 2", "\tquest_links: [ ]", "\tquests: ["]
    lang = [f'\tchapter.{CHAPTER_ID}.title: "Darknet Draconic Convergence"',
            f'\tchapter.{CHAPTER_ID}.subtitle: "Classified network record // draconic ecology beyond ordinary infrastructure"']
    for i, data in enumerate(QUESTS):
        deps = [qid(d) if isinstance(d, int) else d for d in data["deps"]]
        blocks = []
        for j, task in enumerate(data["tasks"]):
            task_id = tid(i, j)
            blocks.append(task_block(task, task_id))
            if task["kind"] in {"item", "kill"}:
                verb = {"item": "Obtain", "kill": "Eliminate"}[task["kind"]]
                title = f'{verb} {task.get("count", 1)} x {task["name"]}'
            elif task["kind"] == "dimension":
                title = f'Enter {task["name"]}'
            else:
                # Advancement and checkmark names are already complete action phrases.
                title = task["name"]
            lang.append(f'\ttask.{task_id}.title: {snbt(title)}')
        lines.extend(["\t\t{", "\t\t\tdependencies: [" + " ".join(snbt(d) for d in deps) + "]",
                      f'\t\t\ticon: {snbt(data["icon"])}', f'\t\t\tid: "{qid(i)}"'])
        if data["reward"] is not None:
            lines.append(f'\t\t\trewards: [{{ id: "{rid(i)}", item: {{ count: 1, id: {snbt(data["reward"])} }}, type: "item" }}]')
        lines.extend([f'\t\t\tshape: {snbt(data["shape"])}',
                      '\t\t\ttags: ["terminal_classified"]',
                      "\t\t\ttasks: [" + "\n\t\t\t\t".join(blocks) + "\n\t\t\t]",
                      f'\t\t\tx: {data["x"]:.1f}d', f'\t\t\ty: {data["y"]:.1f}d', "\t\t}"])
        lang.append(f'\tquest.{qid(i)}.title: {snbt(data["title"])}')
        lang.append(f'\tquest.{qid(i)}.quest_desc: [' + " ".join(snbt(x) for x in data["desc"]) + "]")
    lines.extend(["\t]", "}"])
    CHAPTER.write_text("\n".join(lines) + "\n", encoding="utf-8")

    text = LANG.read_text(encoding="utf-8-sig")
    if BEGIN in text and END in text:
        before, remainder = text.split(BEGIN, 1)
        _, after = remainder.split(END, 1)
        text = before.rstrip() + "\n" + after.lstrip("\n")
    closing = text.rfind("}")
    generated = BEGIN + "\n" + "\n".join(lang) + "\n" + END + "\n"
    LANG.write_text(text[:closing].rstrip() + "\n" + generated + text[closing:], encoding="utf-8")


def main() -> None:
    write_spawns()
    write_injector_recipes()
    write_quests()
    print(f"Wrote {len(MEKANITES)} dual-dimension Mekanite spawns, {len(DRAGONS)} Darknet dragon spawns, {len(INJECTOR_SECONDS)} injector tiers, and {len(QUESTS)} quests.")


if __name__ == "__main__":
    main()

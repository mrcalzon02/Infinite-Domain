"""Build the Mutant Monster and late-game Mekanite threat dossier."""

from __future__ import annotations

import json
from pathlib import Path


def snbt(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/mutant_and_mekanite_threat_dossier.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
BEGIN = "\t// BEGIN GENERATED MUTANT AND MEKANITE THREAT DOSSIER"
END = "\t// END GENERATED MUTANT AND MEKANITE THREAT DOSSIER"
GROUP = "5F0A5E0000000001"
CHAPTER_ID = "5F0A5E0000000003"
ERA8 = "5810000000000001"
NORTH_SURVEY = "5D0000000000000F"
SOUTH_SURVEY = "5D00000000000015"
OCEAN_SURVEY = "5D00000000000013"


def kill(entity: str, count: int, name: str) -> dict:
    return {"kind": "kill", "entity": entity, "count": count, "name": name}


def item(item_id: str, count: int, name: str, consume: bool = False) -> dict:
    return {"kind": "item", "item": item_id, "count": count, "name": name, "consume": consume}


def quest(title: str, desc: list[str], icon: str, x: float, y: float, tasks: list[dict],
          deps: list[int | str] | None = None, rewards: list[tuple[str, int]] | None = None,
          shape: str = "circle", size: float | None = None) -> dict:
    return {"title": title, "desc": desc, "icon": icon, "x": x, "y": y, "tasks": tasks,
            "deps": deps or [], "rewards": rewards or [("numismatics:cog", 2)],
            "shape": shape, "size": size}


QUESTS = [
    quest("Mutation Inside the Perimeter", [
        "Mutant Monsters adds oversized variants of familiar hostiles with distinct attacks and death behavior.",
        "This is not the Rot. It is ordinary hostile anatomy subjected to an extraordinary and deeply irresponsible increase in mass.",
        "Kill one Mutant Zombie. These mutants have been authorized to spawn inside the initial ring, so this branch is available immediately. Visibility is not a recommendation to fight one with a stone hatchet.",
    ], "mutantmonsters:mutant_zombie_spawn_egg", -12, 0,
        [kill("mutantmonsters:mutant_zombie", 1, "Mutant Zombie")], rewards=[("numismatics:cog", 2), ("the_wasteland_reworked:bandage", 2)]),

    quest("Evaluation: Repeated Resurrection", [
        "Kill three Mutant Zombies and observe the collapse sequence. A fallen specimen can rise again unless you finish the work correctly.",
        "When it drops, set the body alight. Standing beside it and hoping that death has become permanent is not a containment protocol.",
    ], "mutantmonsters:hulk_hammer", -18, 4,
        [kill("mutantmonsters:mutant_zombie", 3, "Mutant Zombie")], deps=[0]),

    quest("Evaluation: Articulated Ballistics", [
        "Kill a Mutant Skeleton. Its ranged attacks and detachable anatomy make open ground a particularly educational place to die.",
        "Use hard cover, close distance deliberately, and expect the remains to stay tactically relevant after the central body fails.",
    ], "mutantmonsters:mutant_skeleton_spawn_egg", -12, 4,
        [kill("mutantmonsters:mutant_skeleton", 1, "Mutant Skeleton")], deps=[0]),

    quest("Evaluation: Explosive Regeneration", [
        "Kill a Mutant Creeper. Distance, line-of-sight breaks, and terrain you can afford to lose are the minimum requirements.",
        "Its death sequence is not permission to approach the crater. You have survived long enough that I should not need to explain secondary explosions, yet here we are.",
    ], "mutantmonsters:mutant_creeper_spawn_egg", -6, 4,
        [kill("mutantmonsters:mutant_creeper", 1, "Mutant Creeper")], deps=[0]),

    quest("Evaluation: Hostile Geometry", [
        "Kill a Mutant Enderman. It teleports, throws terrain, produces Endersoul Clones, and generally treats distance as a suggestion.",
        "Fight beneath controlled cover, clear loose blocks from the position, and stop staring at empty space after it relocates. It has not become polite; it has moved.",
    ], "mutantmonsters:mutant_enderman_spawn_egg", 0, 4,
        [kill("mutantmonsters:mutant_enderman", 1, "Mutant Enderman")], deps=[0]),

    quest("Zombie Termination Procedure", [
        "Repeat the engagement and recover a Hulk Hammer. The tool confirms terminal tissue failure and is substantially more convincing than your verbal assurance that the corpse looked finished.",
        "The hammer is detected but not consumed. Keep it available; blunt-force redundancy is one of the few redundancies nobody complains about during an attack.",
    ], "mutantmonsters:hulk_hammer", -18, 8,
        [kill("mutantmonsters:mutant_zombie", 1, "Mutant Zombie"), item("mutantmonsters:hulk_hammer", 1, "Hulk Hammer")], deps=[1]),

    quest("Skeleton Recovery Drill", [
        "Kill two Mutant Skeletons. Separate their firing lane from the rest of the battlefield instead of allowing every hostile creature to participate in the same experiment.",
        "Recoverable skeletal components are useful. They are still evidence from an armed corpse, not tasteful interior decoration.",
    ], "mutantmonsters:mutant_skeleton_rib_cage", -12, 8,
        [kill("mutantmonsters:mutant_skeleton", 2, "Mutant Skeleton")], deps=[2]),

    quest("Creeper Containment Drill", [
        "Kill two Mutant Creepers without conducting the test beside the settlement wall, fuel depot, animal pens, or anything else you were hoping to retain.",
        "Control the battlefield first. Damage output is not impressive when the enemy chooses what your weapon destroys.",
    ], "mutantmonsters:creeper_shard", -6, 8,
        [kill("mutantmonsters:mutant_creeper", 2, "Mutant Creeper")], deps=[3]),

    quest("Endersoul Containment Drill", [
        "Kill two Mutant Endermen. Mark the original target and do not waste ammunition proving that an Endersoul Clone can disappear.",
        "A low roof limits thrown blocks and vertical displacement. It will not make the encounter easy; it merely replaces chaos with a problem you can solve.",
    ], "mutantmonsters:endersoul_hand", 0, 8,
        [kill("mutantmonsters:mutant_enderman", 2, "Mutant Enderman")], deps=[4]),

    quest("Determination: Mutant-Class Threat", [
        "Eliminate one of each naturally occurring mutant class after completing the individual evaluations. The conclusion is refreshingly uncomplicated: they are independent apex contacts, not a coordinated ecology.",
        "Maintain separate procedures for resurrection, artillery, blast radius, and teleportation. Calling all four 'the large one' is concise but strategically useless.",
    ], "mutantmonsters:mutant_skeleton_skull", -9, 12, [
        kill("mutantmonsters:mutant_zombie", 1, "Mutant Zombie"),
        kill("mutantmonsters:mutant_skeleton", 1, "Mutant Skeleton"),
        kill("mutantmonsters:mutant_creeper", 1, "Mutant Creeper"),
        kill("mutantmonsters:mutant_enderman", 1, "Mutant Enderman"),
    ], deps=[5, 6, 7, 8], rewards=[("numismatics:cog", 8), ("kubejs:era0_priority_cache", 1)], shape="rsquare", size=1.5),

    quest("Controlled Mutation: Snow Golem", [
        "Create and then defeat a Mutant Snow Golem with Chemical X. This is an optional controlled trial, though 'controlled' is carrying an heroic amount of meaning.",
        "Perform it away from the hub and anything flammable. Manufactured threats do not become less embarrassing because the laboratory form was signed correctly.",
    ], "mutantmonsters:mutant_snow_golem_spawn_egg", -13, 16,
        [kill("mutantmonsters:mutant_snow_golem", 1, "Mutant Snow Golem")], deps=[9], rewards=[("numismatics:cog", 4)]),

    quest("Controlled Mutation: Spider Pig", [
        "Create and defeat a Spider Pig with Chemical X. Yes, the name is accurate. No, the result is not improved by being funny.",
        "Use a contained test ground and preserve an exit. Combining porcine persistence with arachnid movement was not a request civilization needed answered.",
    ], "mutantmonsters:spider_pig_spawn_egg", -5, 16,
        [kill("mutantmonsters:spider_pig", 1, "Spider Pig")], deps=[9], rewards=[("numismatics:cog", 4)]),

    # Mekanite branch: all roots require Era 8 and the appropriate outer-continent survey.
    quest("Northern Contact: Machines in the Treeline", [
        "Mekanite Mobs supplies the late-game machine hostiles in the north, Cyberspace, and the Darknet. The northern normal biomes contain hostiles that are mechanical in construction and biological only by analogy; they do not occur in the starting ring.",
        "After reaching Era 8 and completing the northern survey, destroy one Drone. If this machine feels unfair, that is because you brought early-era assumptions to an endgame weapons platform.",
    ], "mekanite_mobs:drone_spawn_egg", 8, 0,
        [kill("mekanite_mobs:drone", 1, "Drone")], deps=[ERA8, NORTH_SURVEY], rewards=[("numismatics:cog", 6)]),

    quest("Southern Contact: Armored Desiccation", [
        "The southern deserts and badlands host Mekanite Husks. Cross the ocean only after the Era 8 logistics chain can support extraction as well as arrival.",
        "Destroy one Mekanite Zombie Husk. Heat management, ranged fire, and a marked return route are equipment, not optional mood-setting.",
    ], "mekanite_mobs:mekanite_zombie_husk_spawn_egg", 20, 0,
        [kill("mekanite_mobs:mekanite_zombie_husk", 1, "Mekanite Zombie Husk")], deps=[ERA8, SOUTH_SURVEY], rewards=[("numismatics:cog", 6)]),

    quest("Ocean Contact: Electrified Boarding Party", [
        "Cold and deep oceans contain Mekanite Zombie Drowned. Their habitat makes a damaged vessel, flooded compartment, or interrupted air supply part of the encounter.",
        "Destroy one only after Era 8 and the northern ocean survey. Fighting underwater without an extraction system is merely drowning with additional paperwork.",
    ], "mekanite_mobs:mekanite_zombie_drowned_spawn_egg", 32, 0,
        [kill("mekanite_mobs:mekanite_zombie_drowned", 1, "Mekanite Zombie Drowned")], deps=[ERA8, OCEAN_SURVEY], rewards=[("numismatics:cog", 6)]),

    quest("Northern Line Infantry", [
        "Destroy three Mekanite Zombies in forest, plains, taiga, swamp, jungle, beach, savanna, or dark forest terrain.",
        "Do not mistake a familiar silhouette for familiar durability. Their components turn a basic melee profile into an industrial accident with legs.",
    ], "mekanite_mobs:mekanite_zombie_spawn_egg", 8, 4,
        [kill("mekanite_mobs:mekanite_zombie", 3, "Mekanite Zombie")], deps=[12], rewards=[("kubejs:era8_supply_bag", 1)]),

    quest("Ballistic Chassis", [
        "Destroy three Mekanite Skeletons. Their common habitat overlaps the Zombie patrol zones, so assume combined contacts rather than arranging a courteous duel.",
        "Break line of sight, isolate firing angles, and close only when the route is actually clear. Running directly at a gun remains a poor innovation.",
    ], "mekanite_mobs:mekanite_skeleton_spawn_egg", 8, 8,
        [kill("mekanite_mobs:mekanite_skeleton", 3, "Mekanite Skeleton")], deps=[15]),

    quest("Chemical Warfare Chassis", [
        "Destroy two Mekanite Witches in forested, frozen-spike, jungle, mushroom, or swamp terrain.",
        "Carry cleansing supplies and fight from positions that let status effects expire without allowing the rest of the biome to join in.",
    ], "mekanite_mobs:mekanite_witch_spawn_egg", 8, 12,
        [kill("mekanite_mobs:mekanite_witch", 2, "Mekanite Witch")], deps=[16]),

    quest("Decoy Command Chassis", [
        "Destroy two Mekanite Illusioners. Their clones are projections of the encounter, not a separate wildlife population, so the terminal records the actual chassis.",
        "Track the source, use cover against ranged fire, and resist the urge to attack every identical silhouette in alphabetical order.",
    ], "mekanite_mobs:mekanite_illusioner_spawn_egg", 8, 16,
        [kill("mekanite_mobs:mekanite_illusioner", 2, "Mekanite Illusioner")], deps=[17]),

    quest("Northern Heavy Chassis", [
        "Destroy one Mekanite Ravager in taiga, savanna, forest, or dark forest terrain.",
        "Establish obstacles, overlapping fire, and a retreat route before contact. A large target is not automatically an easy target; thank you for attending this advanced geometry lecture.",
    ], "mekanite_mobs:mekanite_ravager_spawn_egg", 8, 20,
        [kill("mekanite_mobs:mekanite_ravager", 1, "Mekanite Ravager")], deps=[18], rewards=[("kubejs:era8_priority_cache", 1)]),

    quest("Southern Demolition Chassis", [
        "Destroy three Mekanite Creepers. Their reinforced construction turns blast management into an infrastructure requirement.",
        "Fight beyond the expedition camp and never beside the vessel that must carry you home. This distinction is why I retain custody of the maps.",
    ], "mekanite_mobs:mekanite_creeper_spawn_egg", 20, 4,
        [kill("mekanite_mobs:mekanite_creeper", 3, "Mekanite Creeper")], deps=[13], rewards=[("kubejs:era8_supply_bag", 1)]),

    quest("Electrified Web Chassis", [
        "Destroy four Mekanite Spiders across the warm outer biomes. Their mobility makes open, illuminated firing lanes more useful than an ornate camp perimeter.",
        "Watch vertical surfaces and remove webs before they turn your withdrawal route into an exhibit on poor planning.",
    ], "mekanite_mobs:mekanite_spider_spawn_egg", 20, 8,
        [kill("mekanite_mobs:mekanite_spider", 4, "Mekanite Spider")], deps=[20]),

    quest("Assault Chassis", [
        "Destroy three Mekanite Vindicators in plains, forests, taiga, savanna, or savanna plateau terrain.",
        "Their close-range pressure is designed to punish a scattered formation. Maintain spacing without becoming isolated—an elementary distinction under regrettably non-elementary conditions.",
    ], "mekanite_mobs:mekanite_vindicator_spawn_egg", 20, 12,
        [kill("mekanite_mobs:mekanite_vindicator", 3, "Mekanite Vindicator")], deps=[21], rewards=[("kubejs:era8_priority_cache", 1)]),

    quest("Self-Dividing Chassis", [
        "Destroy a complete Mekanite Slime hierarchy: Big, Medium, and Small. The smaller chassis are still part of the threat, not debris.",
        "Control the surrounding ground before splitting the largest body. Multiplication is less charming when every result is armed.",
    ], "mekanite_mobs:mekanite_slime_spawn_egg", 14, 8, [
        kill("mekanite_mobs:mekanite_slime", 1, "Mekanite Big Slime"),
        kill("mekanite_mobs:mekanite_slime_medio", 2, "Mekanite Medium Slime"),
        kill("mekanite_mobs:mekanite_slime_small", 4, "Mekanite Small Slime"),
    ], deps=[15], rewards=[("kubejs:era8_supply_bag", 1)]),

    quest("Displacement Chassis", [
        "Destroy two Mekanite Endermen. They appear across select northern, southern, coastal, Nether, End, Cyberspace, and Darknet biomes, because ordinary geographic restraint was apparently beneath their designers.",
        "Use overhead cover and redundant targeting. If your plan depends upon the target remaining where you first saw it, you have described a wish.",
    ], "mekanite_mobs:mekanite_enderman_spawn_egg", 14, 12,
        [kill("mekanite_mobs:mekanite_enderman", 2, "Mekanite Enderman")], deps=[12, 13], rewards=[("kubejs:era8_supply_bag", 1)]),

    quest("Determination: Mekanite Extermination Doctrine", [
        "The outer continents, Cyberspace, and the Darknet support a distributed weapons ecology: patrol, artillery, demolition, chemical, decoy, displacement, aquatic, dividing, and heavy assault chassis.",
        "Destroy the representative command threats and return alive. The determination is final: these are Era 8 expedition hazards. They are not an exotic source of early salvage and the ocean is not a shortcut around progression.",
    ], "mekanite_mobs:mekanite_plasma_shield", 14, 24, [
        kill("mekanite_mobs:mekanite_ravager", 1, "Mekanite Ravager"),
        kill("mekanite_mobs:mekanite_vindicator", 1, "Mekanite Vindicator"),
        kill("mekanite_mobs:mekanite_enderman", 1, "Mekanite Enderman"),
        kill("mekanite_mobs:mekanite_zombie_drowned", 1, "Mekanite Zombie Drowned"),
    ], deps=[19, 22, 14, 23, 24], rewards=[("numismatics:cog", 32), ("kubejs:era8_priority_cache", 1)], shape="rsquare", size=1.5),
]


def qid(index: int) -> str:
    return f"5F20{index + 1:012X}"


def tid(index: int, sub: int) -> str:
    return f"6F2{index + 1:09X}{sub + 1:04X}"


def rid(index: int, sub: int) -> str:
    return f"7F2{index + 1:09X}{sub + 1:04X}"


def main() -> None:
    lines = ["{", "\tdefault_hide_dependency_lines: false", "\tdefault_quest_shape: \"circle\"",
             "\tfilename: \"mutant_and_mekanite_threat_dossier\"", f'\tgroup: "{GROUP}"', '\ticon: "mutantmonsters:hulk_hammer"',
             f'\tid: "{CHAPTER_ID}"', "\timages: [ ]", "\torder_index: 1", "\tquest_links: [ ]", "\tquests: ["]
    lang = [f'\tchapter.{CHAPTER_ID}.title: "Aberrant and Mekanite Threat Determinations"',
            f'\tchapter.{CHAPTER_ID}.subtitle: "Hostile mutation records // identification, escalation, and response"']

    for i, data in enumerate(QUESTS):
        dependencies = [qid(d) if isinstance(d, int) else d for d in data["deps"]]
        task_blocks: list[str] = []
        task_lang: list[str] = []
        for j, task in enumerate(data["tasks"]):
            task_id = tid(i, j)
            if task["kind"] == "kill":
                task_blocks.append("{\n" + f'\t\t\t\tentity: {snbt(task["entity"])}\n'
                                   f'\t\t\t\tid: "{task_id}"\n\t\t\t\ttype: "kill"\n'
                                   f'\t\t\t\tvalue: {task["count"]}L\n\t\t\t}}')
                task_lang.append(f'\ttask.{task_id}.title: {snbt(f"Eliminate {task["count"]} x {task["name"]}")}')
            else:
                consume = "\t\t\t\tconsume_items: true\n" if task["consume"] else ""
                task_blocks.append("{\n" + consume + f'\t\t\t\tcount: {task["count"]}L\n'
                                   f'\t\t\t\tid: "{task_id}"\n'
                                   f'\t\t\t\titem: {{ count: 1, id: {snbt(task["item"])} }}\n'
                                   f'\t\t\t\ttype: "item"\n\t\t\t}}')
                task_lang.append(f'\ttask.{task_id}.title: {snbt(f"Obtain {task["count"]} x {task["name"]}")}')

        reward_blocks = ["{\n" + f'\t\t\t\tid: "{rid(i, j)}"\n'
                         f'\t\t\t\titem: {{ count: {count}, id: {snbt(item_id)} }}\n'
                         f'\t\t\t\ttype: "item"\n\t\t\t}}'
                         for j, (item_id, count) in enumerate(data["rewards"])]

        lines.append("\t\t{")
        if dependencies:
            lines.append("\t\t\tdependencies: [" + " ".join(snbt(d) for d in dependencies) + "]")
        lines.extend([f'\t\t\ticon: {snbt(data["icon"])}', f'\t\t\tid: "{qid(i)}"',
                      "\t\t\trewards: [" + "\n\t\t\t\t".join(reward_blocks) + "\n\t\t\t]",
                      f'\t\t\tshape: {snbt(data["shape"])}',
                      '\t\t\ttags: ["terminal_warning"]'])
        if data["size"] is not None:
            lines.append(f'\t\t\tsize: {data["size"]:.1f}d')
        lines.extend(["\t\t\ttasks: [" + "\n\t\t\t\t".join(task_blocks) + "\n\t\t\t]",
                      f'\t\t\tx: {data["x"]:.1f}d', f'\t\t\ty: {data["y"]:.1f}d', "\t\t}"])
        lang.append(f'\tquest.{qid(i)}.title: {snbt(data["title"])}')
        lang.append(f'\tquest.{qid(i)}.quest_desc: [' + " ".join(snbt(x) for x in data["desc"]) + "]")
        lang.extend(task_lang)

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
    kills = sum(task["kind"] == "kill" for q in QUESTS for task in q["tasks"])
    print(f"Wrote {len(QUESTS)} threat quests with {kills} kill objectives.")


if __name__ == "__main__":
    main()

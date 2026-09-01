"""Build the always-accessible Spore threat dossier and its Charles dialogue."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/the_rot_spore_threat_dossier.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
BEGIN = "\t// BEGIN GENERATED SPORE THREAT DOSSIER"
END = "\t// END GENERATED SPORE THREAT DOSSIER"


def snbt(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def q(
    title: str,
    desc: list[str],
    band: str,
    *,
    entity: str | None = None,
    kills: int = 1,
    items: list[tuple[str, str, int, bool]] | None = None,
    special_rewards: list[tuple[str, int]] | None = None,
) -> dict:
    return {
        "title": title,
        "desc": desc,
        "band": band,
        "entity": entity,
        "kills": kills,
        "items": items or [],
        "special_rewards": special_rewards or [],
    }


QUESTS = [
    q("The Rot Does Not Wait", [
        "Spore is the pack's evolving fungal-infection threat system; this dossier teaches identification and containment.",
        "I had hoped the movement outside was merely another starving corpse. It is not. The tissue is fungal, coordinated, and offensively enthusiastic.",
        "Kill one Infected Human. This dossier never waits for an era unlock because neither does the infection. If this specimen strains your equipment, advance the other quest lines before attempting to be heroic.",
    ], "infected", entity="spore:inf_human"),
    q("Filter First, Bravado Later", [
        "Obtain a Gas Mask and keep it available around contaminated ground. It is equipment, not a certificate of invulnerability—an apparently difficult distinction for armed survivors.",
        "Cold suppresses most Spore organisms. Fire may remove biomass, but relying on one damage method is an excellent way to teach an adaptive predator your habits.",
    ], "field", items=[("Gas Mask", "spore:gas_mask", 1, False)]),
    q("Still Wearing a Face", [
        "Kill six Infected Humans. They retain enough anatomy to be recognizable and enough coordination to make recognition a tactical liability.",
        "Do not let apparently minor infected accumulate kills. Spore organisms use kill points to strengthen themselves and the wider infestation.",
    ], "infected", entity="spore:inf_human", kills=6),
    q("Desiccation Was Not a Cure", [
        "Kill four Infected Husks. The fungus has adapted quite comfortably to a host that was already dried out, which is biologically fascinating and aesthetically unforgivable.",
        "Treat every familiar silhouette as unverified until it stops moving.",
    ], "infected", entity="spore:inf_husk", kills=4),
    q("The Water Is Compromised", [
        "Kill four Infected Drowned. Aquatic variants mean coastlines and reservoirs are approach routes, not defensive walls.",
        "Inspect water intakes, light submerged access points, and avoid fighting where retreat requires swimming through the same teeth pursuing you.",
    ], "infected", entity="spore:inf_drowned", kills=4),
    q("A Lab Coat Proves Nothing", [
        "Kill two Infected Scientists. Apparently education does not confer immunity; it merely gives the Rot better pockets.",
        "Search laboratories cautiously. Infested rooms, growth blocks, and spawners can sustain an outbreak after the visible occupants are dead.",
    ], "infected", entity="spore:inf_hazmat", kills=2),
    q("First Tissue Submission", [
        "Submit four Preserved Infected Tissue samples. Yes, I want them sealed. No, your ordinary lunch container does not become a laboratory vessel because you wiped it on your sleeve.",
        "The Charger and Biomonitor are advance compensation. You may not yet possess the infrastructure to use or install them; store them safely instead of improvising surgery.",
    ], "sample1", items=[("Preserved Infected Tissue", "kubejs:infected_tissue_sample", 4, True)],
      special_rewards=[("ae2:charger", 1), ("createcybernetics:eyeupgrades_biomonitor", 1)]),
    q("The Rot Has Inventory", [
        "Collect Biomass, Tumors, and Mutated Fibre. These are not trophies. They are evidence that the infection manufactures specialized tissue instead of merely consuming hosts.",
        "Keep samples isolated from food stores and living soil. That sentence should have been unnecessary, yet here we are.",
    ], "material", items=[
        ("Biomass", "spore:biomass", 32, False), ("Tumor", "spore:tumor", 8, False),
        ("Mutated Fibre", "spore:mutated_fiber", 8, False),
    ]),
    q("Knight: The Fungus Discovers Armor", [
        "Kill four Knights. Their reinforced bodies prove the Rot can specialize for frontal assault.",
        "If you thought the infected were unpleasant, congratulations: those were the organisms before they began allocating a budget.",
    ], "evolved", entity="spore:knight", kills=4),
    q("Spitter: Distance Is Not Safety", [
        "Kill four Spitters. Break line of sight, use cover, and do not cluster where one projectile can contaminate an entire firing position.",
        "The creature has converted digestion into artillery. I am impressed by the efficiency and disgusted by every other part of that sentence.",
    ], "evolved", entity="spore:spitter", kills=4),
    q("Howler: An Alarm With Organs", [
        "Kill three Howlers. Prioritize them before they turn a manageable contact into a coordinated response.",
        "Spore mobs can share targets through links and signals. The loud one is not merely being theatrical, though I resent the competition.",
    ], "evolved", entity="spore:howler", kills=3),
    q("Stalker: Check the Ceiling", [
        "Kill three Stalkers. Sweep above doors, behind machinery, and across vertical surfaces before entering a contaminated room.",
        "If you thought the Howler was bad, this one has discovered patience. You might consider doing the same.",
    ], "evolved", entity="spore:stalker", kills=3),
    q("Brute: Apply More Planning", [
        "Kill two Brutes. Do not trade blows merely to demonstrate that your skeleton is technically present.",
        "Use obstacles, ranged fire, cold effects, and a retreat lane. Your weapon is only one component of the solution.",
    ], "evolved", entity="spore:brute", kills=2),
    q("Gorgon: Biology Becomes a Weapon System", [
        "Kill one Gorgon. This is no longer an infected animal improvising violence; it is a purpose-built organism.",
        "If you thought the Brute was bad, the next ranks abandon recognizable anatomy almost entirely. Improve your equipment while you still have the option.",
    ], "evolved", entity="spore:gorgon"),
    q("Evolved Mutagen Submission", [
        "Submit six Evolved Mutagen Samples. I can now compare specialization across multiple combat forms without asking you to carry an entire twitching carcass home.",
        "The storage cell and targeting implant are field-research dividends. The implant still requires proper surgery. I refuse to debug your skull with a wrench.",
    ], "sample2", items=[("Evolved Mutagen Sample", "kubejs:evolved_mutagen_sample", 6, True)],
      special_rewards=[("ae2:item_storage_cell_1k", 1), ("createcybernetics:eyeupgrades_targeting", 1)]),
    q("Specialized Anatomy", [
        "Collect Hypersuspensile Ligaments, Alveolic Sacks, Spikes, and Wing Membranes. The Rot has solved locomotion, respiration, armor penetration, and flight using wet components grown to order.",
        "Interesting, yes. Touching any of it without gloves remains stupid.",
    ], "material", items=[
        ("Hypersuspensile Ligaments", "spore:ligaments", 8, False),
        ("Alveolic Sack", "spore:alveolic_sack", 4, False),
        ("Spike", "spore:spike", 8, False), ("Wing Membrane", "spore:wing_membrane", 4, False),
    ]),
    q("Inquisitor: It Has Opinions", [
        "Kill two Inquisitors. Hyper-evolved forms combine durability, reach, and tactical behavior rather than merely increasing mass.",
        "If it appears to be judging your tactics, improve them. I dislike conceding intellectual ground to a walking fungal indictment.",
    ], "hyper", entity="spore:inquisitor", kills=2),
    q("Wendigo: Speed With Too Many Joints", [
        "Kill two Wendigos. Maintain overlapping fire and deny it an isolated target.",
        "A lone survivor is prey; a prepared team is a geometry problem. Try to be the latter.",
    ], "hyper", entity="spore:wendigo", kills=2),
    q("Ogre: Structural Damage Is an Attack", [
        "Kill one Ogre. Fight away from irreplaceable machines, weak walls, and the room containing every resource you own.",
        "Your base layout is now part of combat doctrine. Four decorative blocks and optimism do not constitute fortification.",
    ], "hyper", entity="spore:ogre"),
    q("Brotkatze: Ambush Predator", [
        "Kill one Brotkatze. Watch flanks, maintain illumination, and do not pursue it into terrain you have not cleared.",
        "If you thought the Ogre was bad, this one wastes less mass and considerably less time.",
    ], "hyper", entity="spore:brot"),
    q("Hyper-Evolved Core Submission", [
        "Submit four Hyper-Evolved Core Samples. Their internal organization is revoltingly elegant; multiple specialized tissues behave like replaceable machine modules.",
        "I am issuing a larger storage cell and Wired Reflexes. Have a competent surgeon install the latter. Competence is not implied by ownership of a sharp object.",
    ], "sample3", items=[("Hyper-Evolved Core Sample", "kubejs:hyper_evolved_core_sample", 4, True)],
      special_rewards=[("ae2:item_storage_cell_4k", 1), ("createcybernetics:muscleupgrades_wiredreflexes", 1)]),
    q("Armor, Cores, and Spines", [
        "Collect Armor Plates, Living Cores, Hardened Binds, and Spine Segments. These tissues explain why late organisms shrug off improvised weapons.",
        "Spore creatures are generally vulnerable to cold. Vary damage methods and keep cryogenic tools available; adaptation rewards repetition, including repetitive mistakes.",
    ], "material", items=[
        ("Armor Plate", "spore:armor_plate", 8, False), ("Living Core", "spore:living_core", 4, False),
        ("Hardened Bind", "spore:hardened_bind", 8, False), ("Spine Segment", "spore:spine_fragment", 8, False),
    ]),
    q("Flesh Mound: An Outpost That Breathes", [
        "Kill three Flesh Mounds. They are infrastructure: persistent biological outposts that support spread and nearby organisms.",
        "Destroy the organism and clear its growths. Leaving the infected terrain intact is gardening for an enemy that already considers you fertilizer.",
    ], "organoid", entity="spore:mound", kills=3),
    q("Vigil: The Outpost Has Eyes", [
        "Kill one Vigil. Organoids divide battlefield functions between bodies; this one performs observation and coordination.",
        "Remove watchers before assaulting a nest. Being seen is sometimes unavoidable. Remaining seen is usually laziness.",
    ], "organoid", entity="spore:vigil"),
    q("Womb: Reinforcements Manufactured Locally", [
        "Kill one Womb. It turns occupied ground into a supply line for new bodies.",
        "Do not farm it casually. Any strategy containing the phrase 'infinite monsters might be useful' has already failed its safety review.",
    ], "organoid", entity="spore:reconstructor"),
    q("Usurper: The Ground Is Participating", [
        "Kill one Usurper. Organoids can emerge through vulnerable terrain, which makes floor construction a defensive system.",
        "Use hard materials and avoid thick masses of weak blocks in protected interiors. Yes, even the floor requires engineering now.",
    ], "organoid", entity="spore:usurper"),
    q("Organoid Neural Submission", [
        "Submit four Organoid Neural Samples. Their signal tissue confirms that local bodies can act as one distributed hunting system.",
        "The Wireless Terminal and Neural Processor are appropriate rewards: one extends your network, the other may eventually improve yours. Do not confuse the two during installation.",
    ], "sample4", items=[("Organoid Neural Sample", "kubejs:organoid_neural_sample", 4, True)],
      special_rewards=[("ae2:wireless_terminal", 1), ("createcybernetics:brainupgrades_neuralprocessor", 1)]),
    q("Organoid Anatomy", [
        "Collect Organoid Membranes, a Vigil Eye, and Cerebrums. The samples show transmission tissue, sensory specialization, and decentralized control.",
        "If Madness appears without a visible attacker, assume a major coordinating organism is nearby. Milky Sacks can remove it; distance and extermination remain preferable.",
    ], "material", items=[
        ("Organoid Membrane", "spore:organoid_membrane", 8, False),
        ("Eye of the Vigil", "spore:vigil_eye", 1, False), ("Cerebrum", "spore:cerebrum", 4, False),
    ]),
    q("Sieger: The Wall Is a Suggestion", [
        "Kill one Sieger. Calamities are siege organisms, not oversized wildlife.",
        "Evacuate noncombatants, establish fallback positions, and fight somewhere you can afford to lose. If you thought the organoids were bad, they were merely preparing the battlefield.",
    ], "calamity", entity="spore:sieger"),
    q("Howitzer: Counter-Battery Required", [
        "Kill one Howitzer. Break its line of fire and approach through covered routes instead of sprinting across open ground with admirable confidence and no surviving plan.",
        "Long-range biological artillery means towers and rooftops need overhead protection, not just walls.",
    ], "calamity", entity="spore:howitzer"),
    q("Hohlfresser: Underground Is Not Safe", [
        "Kill one Hohlfresser. Burrowing calamities invalidate the comforting fiction that several metres of dirt make a secure bunker.",
        "Segment underground facilities, harden floors, and maintain more than one exit. A single tunnel is a coffin with civil engineering paperwork.",
    ], "calamity", entity="spore:hohlfresser"),
    q("Gazenbreacher: Do Not Admire It Up Close", [
        "Kill one Gazenbreacher. Keep distance, rotate damage sources, and preserve a clear retreat corridor.",
        "Its anatomy is extraordinary. I would enjoy studying it considerably more if it were not trying to study your interior anatomy in return.",
    ], "calamity", entity="spore:gazenbreacher"),
    q("Hindenburg: The Sky Is Infected", [
        "Kill one Hindenburg. Airspace is now part of the containment perimeter.",
        "Use ranged weapons, protected firing positions, and redundant access to roofs. Looking upward after the first impact is technically an observation method, just not a good one.",
    ], "calamity", entity="spore:hindenburg"),
    q("Leviathan: The Sea Is Also Infected", [
        "Kill one Leviathan. Coastal travel and offshore industry require escort, sonar-by-any-other-name, and an emergency route back to land.",
        "If you thought the Hindenburg was bad, the Rot has also decided oceans contain insufficient nightmares.",
    ], "calamity", entity="spore:leviathan"),
    q("Verfalldrache: Terminal Morphology", [
        "Kill one Verfalldrache. This is the infection expressing scale, flight, armor, and predation as a single argument against complacency.",
        "Do not engage because the quest is visible. Engage when the settlement can absorb casualties, equipment loss, and structural damage without collapsing.",
    ], "calamity", entity="spore:verfall"),
    q("Calamity Biomass Submission", [
        "Submit five Calamity Biomass Samples. I am running out of polite anatomical terminology, which is a remarkable achievement on the organism's part.",
        "The Dense Energy Cell and Dense Battery reward sustained preparation. Neither will save someone who mistakes stored power for tactical judgment.",
    ], "sample5", items=[("Calamity Biomass Sample", "kubejs:calamity_biomass_sample", 5, True)],
      special_rewards=[("ae2:dense_energy_cell", 1), ("createcybernetics:organsupgrade_densebattery", 1)]),
    q("Three Environments, One Appetite", [
        "Collect Terrestrial, Aquatic, and Airborne Reforged Biomass plus an Amalgamated Heart. The Rot does not merely occupy environments; it builds bodies specifically for each of them.",
        "We have enough evidence. What remains is the voice coordinating the evidence into an army.",
    ], "material", items=[
        ("Terrestrial Reforged Biomass", "spore:reforged_biomass_t", 2, False),
        ("Aquatic Reforged Biomass", "spore:reforged_biomass_w", 2, False),
        ("Airborne Reforged Biomass", "spore:reforged_biomass_a", 2, False),
        ("Amalgamated Heart", "spore:amalgamated_heart", 1, False),
    ]),
    q("Murder the Hive Mind", [
        "Kill one Proto Hivemind and submit its Cerebral Sample. It links lesser organisms, spreads Madness across a wide area, and turns scattered growth into coordinated territory.",
        "Destroy supporting organoids first, establish a hardened perimeter, bring cold and varied damage, and plan extraction before contact. If this objective looks premature, it is. Go become less premature.",
        "Once it is dead, give me the sample. I am intrigued, disgusted, and—against my better instincts—quite proud that you survived long enough to make those feelings relevant.",
    ], "final", entity="spore:proto", items=[("Hive Mind Cerebral Sample", "kubejs:hive_mind_cerebral_sample", 1, True)],
      special_rewards=[("ae2:wireless_crafting_terminal", 1), ("createcybernetics:brainupgrades_iceprotocol", 1)]),
]


ICONS = {
    "field": "spore:gas_mask", "infected": "spore:biomass",
    "evolved": "spore:mutated_fiber", "hyper": "spore:living_core",
    "organoid": "spore:cerebrum", "calamity": "spore:amalgamated_heart",
    "material": "spore:armor_plate", "sample1": "kubejs:infected_tissue_sample",
    "sample2": "kubejs:evolved_mutagen_sample", "sample3": "kubejs:hyper_evolved_core_sample",
    "sample4": "kubejs:organoid_neural_sample", "sample5": "kubejs:calamity_biomass_sample",
    "final": "kubejs:hive_mind_cerebral_sample",
}

ENTITY_LABELS = {
    "spore:inf_human": "Infected Human",
    "spore:inf_husk": "Infected Husk",
    "spore:inf_drowned": "Infected Drowned",
    "spore:inf_hazmat": "Infected Scientist",
    "spore:brot": "Brotkatze",
    "spore:mound": "Flesh Mound",
    "spore:reconstructor": "Womb",
    "spore:proto": "Proto Hivemind",
}


def quest_id(index: int) -> str:
    return f"5F10{index + 1:012X}"


def task_id(index: int, sub: int) -> str:
    return f"6F{index + 1:010X}{sub + 1:04X}"


def reward_id(index: int, sub: int) -> str:
    return f"7F{index + 1:010X}{sub + 1:04X}"


def main() -> None:
    lines = [
        "{", "\tdefault_hide_dependency_lines: false", "\tdefault_quest_shape: \"circle\"",
        "\tfilename: \"the_rot_spore_threat_dossier\"", "\tgroup: \"5F0A5E0000000001\"", "\ticon: \"spore:gas_mask\"",
        "\tid: \"5F0A5E0000000002\"", "\timages: [ ]", "\torder_index: 0", "\tquest_links: [ ]", "\tquests: [",
    ]
    lang: list[str] = [
        '\tchapter_group.5F0A5E0000000001.title: "Persistent Threats"',
        '\tchapter.5F0A5E0000000002.title: "The Rot — Spore Threat Dossier"',
        '\tchapter.5F0A5E0000000002.subtitle: "Critical containment intelligence // adaptive infection and regional collapse"',
    ]

    for i, quest in enumerate(QUESTS):
        qid = quest_id(i)
        row, col = divmod(i, 3)
        xs = (-4.0, 0.0, 4.0) if row % 2 == 0 else (4.0, 0.0, -4.0)
        dependencies = [] if i == 0 else [quest_id(i - 1)]
        tasks: list[str] = []
        task_titles: list[str] = []

        if quest["entity"]:
            tid = task_id(i, len(tasks))
            tasks.append("{\n" + f'\t\t\t\tentity: {snbt(quest["entity"])}\n\t\t\t\tid: "{tid}"\n\t\t\t\ttype: "kill"\n\t\t\t\tvalue: {quest["kills"]}L\n\t\t\t}}')
            entity_label = ENTITY_LABELS.get(quest["entity"], quest["title"].split(":", 1)[0])
            task_titles.append(f'\ttask.{tid}.title: {snbt("Eliminate " + str(quest["kills"]) + " x " + entity_label)}')

        for display, item_id, count, consume in quest["items"]:
            tid = task_id(i, len(tasks))
            consume_line = "\t\t\t\tconsume_items: true\n" if consume else ""
            tasks.append("{\n" + consume_line + f'\t\t\t\tcount: {count}L\n\t\t\t\tid: "{tid}"\n\t\t\t\titem: {{ count: 1, id: {snbt(item_id)} }}\n\t\t\t\ttype: "item"\n\t\t\t}}')
            verb = "Submit" if consume else "Obtain"
            task_titles.append(f'\ttask.{tid}.title: {snbt(f"{verb} {count} x {display}")}')

        reward_items = [("numismatics:cog", {"infected": 1, "field": 1, "evolved": 2, "hyper": 3, "organoid": 4, "calamity": 8, "material": 2}.get(quest["band"], 4))]
        reward_items.extend(quest["special_rewards"])
        rewards = []
        for rindex, (item_id, count) in enumerate(reward_items):
            rid = reward_id(i, rindex)
            rewards.append("{\n" + f'\t\t\t\tid: "{rid}"\n\t\t\t\titem: {{ count: {count}, id: {snbt(item_id)} }}\n\t\t\t\ttype: "item"\n\t\t\t}}')

        lines.append("\t\t{")
        if dependencies:
            lines.append(f'\t\t\tdependencies: [{" ".join(snbt(d) for d in dependencies)}]')
        lines.extend([
            f'\t\t\ticon: {snbt(ICONS[quest["band"]])}', f'\t\t\tid: "{qid}"',
            "\t\t\trewards: [" + "\n\t\t\t\t".join(rewards) + "\n\t\t\t]",
            f'\t\t\tshape: {snbt("rsquare" if quest["band"] == "final" else "circle")}',
            '\t\t\ttags: ["terminal_critical"]',
        ])
        if quest["band"] == "final":
            lines.append("\t\t\tsize: 1.5d")
        lines.extend([
            "\t\t\ttasks: [" + "\n\t\t\t\t".join(tasks) + "\n\t\t\t]",
            f"\t\t\tx: {xs[col]:.1f}d", f"\t\t\ty: {row * 3.0:.1f}d", "\t\t}",
        ])

        lang.append(f'\tquest.{qid}.title: {snbt(quest["title"])}')
        desc = " ".join(snbt(part) for part in quest["desc"])
        lang.append(f"\tquest.{qid}.quest_desc: [{desc}]")
        lang.extend(task_titles)

    lines.extend(["\t]", "}"])
    CHAPTER.write_text("\n".join(lines) + "\n", encoding="utf-8")

    text = LANG.read_text(encoding="utf-8-sig")
    if BEGIN in text and END in text:
        before, remainder = text.split(BEGIN, 1)
        _, after = remainder.split(END, 1)
        text = before.rstrip() + "\n" + after.lstrip("\n")
    closing = text.rfind("}")
    generated = BEGIN + "\n" + "\n".join(lang) + "\n" + END + "\n"
    text = text[:closing].rstrip() + "\n" + generated + text[closing:]
    LANG.write_text(text, encoding="utf-8")
    print(f"Wrote {len(QUESTS)} Spore quests and {sum(bool(x['entity']) for x in QUESTS)} kill objectives.")


if __name__ == "__main__":
    main()

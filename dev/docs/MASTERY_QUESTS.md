# Infinite Domain Mastery Projects

Date: 2026-08-13  
Status: Era 0 through Era 8 implemented; in-game submission testing remains.

## Purpose

Mastery projects are optional civilization-scale resource sinks. They do not unlock eras, recipes, AE2 equipment, cyberware, or ordinary progression. Each chapter becomes available after its matching era capstone and asks the quest team to permanently submit four resources that define that era.

Every resource task has `consume_items: true`. Players should deposit only materials deliberately committed to mastery. Completing all four branches awards a noncraftable Era Mastery Emblem, 64 Numismatics Cogs, experience, and an otherwise uncraftable creative-mode artifact.

Era 0 additionally places one coveted higher-technology reward on each resource branch: a Building Gadget, Charging Station, Mining Gadget, and Copy-Paste Gadget. Their ordinary recipes are gated behind AE2 formation/annihilation cores, processors, energy infrastructure, spatial components, and 3x-4x compressed iron. The mastery route is therefore an absurdly expensive early alternative, not a cheap recipe bypass.

## Numeric ladder

The ceiling is the signed 32-bit maximum, 2,147,483,647, shifted down by two bits to 536,870,911. Era 8 uses that ceiling per resource. Each preceding era removes one additional bit, giving an approximately doubling mastery curve.

| Era | Required per resource | Four-resource total |
| --- | ---: | ---: |
| 0 | 2,097,151 | 8,388,604 |
| 1 | 4,194,303 | 16,777,212 |
| 2 | 8,388,607 | 33,554,428 |
| 3 | 16,777,215 | 67,108,860 |
| 4 | 33,554,431 | 134,217,724 |
| 5 | 67,108,863 | 268,435,452 |
| 6 | 134,217,727 | 536,870,908 |
| 7 | 268,435,455 | 1,073,741,820 |
| 8 | 536,870,911 | 2,147,483,644 |

The Era 8 four-resource total is deliberately only three items below the signed 32-bit maximum.

## Era resources

| Era | Resource 1 | Resource 2 | Resource 3 | Resource 4 |
| --- | --- | --- | --- | --- |
| 0 | Sticks | Wastelands Scrap Metal | Coarse Dirt | Cobblestone |
| 1 | Andesite | Andesite Alloy | Wheat | Scrap Piles |
| 2 | Coal Coke | TFMG Steel Ingots | Wheat | Re-Automated Node Fragments |
| 3 | Petroleum Coke | Petrochem Sulfur Dust | Rubber Sheets | Plastic Sheets |
| 4 | Create New Age Copper Wire | Insulated Copper Wire | Power Grid Circuit Boards | Oritech Biomass |
| 5 | Oritech Machine Core I | Biosteel Ingots | Certus Quartz Crystals | Cyberware Titanium Components |
| 6 | Uranium Powder | Enriched Yellowcake | Lead Ingots | Oritech Plutonium Dust |
| 7 | Desh Ingots | Corronium Ingots | Heavy Metal Ingots | Ice Shards |
| 8 | 5x Compressed Cobblestone | TFMG Steel Blocks | Stellaris Desh Blocks | AE2 Engineering Processors |

## Creative mastery rewards

| Era | Uncraftable reward |
| --- | --- |
| 0 | Create Creative Crate |
| 1 | Create Creative Motor |
| 2 | TFMG Creative Generator |
| 3 | Create Creative Fluid Tank |
| 4 | Power Grid Creative Voltage Source |
| 5 | Oritech Creative Storage Block |
| 6 | AE2 Creative Energy Cell |
| 7 | Mining Gadgets Creative Battery Upgrade |
| 8 | AE2 Creative Storage Cell |

## Layout and ownership

The mastery quests live in the separate **Civilization Mastery** chapter group. Each chapter has a central warning/orientation node, four parallel submission branches, and a final prestige node requiring all four submissions. Mastery has no outgoing dependency into the civilization-era spine.

The source generator is `scripts/generators/generate_mastery_quests.js`. It refuses to append duplicate language entries if run again without intentionally removing the generated mastery files and localization keys.

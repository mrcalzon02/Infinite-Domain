# Radioactive Salvage System

The wasteland's hazardous blocks are now resources. Every valid sieve operation returns one mundane baseline item, while useful discoveries remain chance-based rather than becoming a clean ore generator.

## Inputs

| Input | Identity | Processing character |
|---|---|---|
| `wastelands:radioactive_waste` | Sparkling green terrain waste | Contaminated minerals, chemicals, and biological debris |
| `the_wasteland_reworked:waste_barrel` | Sealed hazardous barrel | Richer industrial, laboratory, and radiation-protection salvage |
| `the_wasteland_reworked:rusted_barrel` | Abandoned old-world barrel | Scrap, cans, cloth, components, and rare intact instruments |
| `wastelands:scrap_pile` | Six pieces of gathered scrap | Mixed refuse, intact garbage bags, and rare Wastelands survival supplies |

All four blocks can be placed directly into an Ex Deorum sieve. Their tables change with mesh tier instead of merely increasing one generic loot pool.

Scrap Piles follow the same rule but intentionally do **not** sift directly into more metal. They always produce `the_wasteland_reworked:garbage_bag`, then independently roll for survival supplies and industrial remnants. A player may either sieve the bag for targeted Wastelands supplies or place and break it to invoke its native rummaging table of paper, string, sticks, scrap, cans, food, seeds, cloth, damaged equipment, planks, and pipe.

## Guaranteed baseline

Every mesh tier always returns exactly one fallback item before its independent bonus rolls:

| Input | Guaranteed result |
|---|---|
| Radioactive Waste | 1 Wastelands Scrap Metal |
| Waste Barrel | 1 Reworked Scrap Metal |
| Rusted Barrel | 1 Empty Can |
| Scrap Pile | 1 Garbage Bag |

This is the pack-wide sieve rule: scarcity means low-value output, never an empty operation.

## Hammer fallback

- Waste Barrel -> 2 Radioactive Waste
- Rusted Barrel -> 3 Scrap Metal

This gives unwanted barrels a predictable disposal path even when the player does not want to gamble on their barrel-specific sieve table.

## Mesh progression

| Mesh | Typical discoveries |
|---|---|
| String | Survival refuse: scrap, cans, bones, rotten flesh, cloth, sticks, coal |
| Flint | Basic metal fragments, sulfur, redstone, garbage, cartridges, biological scraps |
| Iron | Lead, aluminium, laboratory glass, rubber, filters, trace industrial chemicals |
| Golden | Small amounts of uranium chemistry plus very rare intact utility objects |
| Diamond | Raw uranium, yellowcake, radiation medicine, anomalous Spore remnants |
| Netherite | The best recovery odds and extremely rare intact instruments or records |

## Progression guardrails

- No AE2 item is in these tables.
- No cyberware is in these tables.
- No finished machinery, creative item, diamond, netherite, or nether star is awarded.
- High-value outcomes use fractions of one percent, and most require advanced meshes.
- The guaranteed baseline is fixed at one item; all additional sieve results roll independently.
- The tables are intentionally more rewarding than globally nerfed ordinary dirt/gravel sieving because the inputs are biome salvage and exposure hazards, not renewable bulk material.

## Maintenance

Run `ROOT_tools/build_radioactive_salvage_recipes.ps1` after changing its probability table. It regenerates the recipes under `kubejs/data/infinite_domain/recipe/hammer/hazardous_salvage`, `sieve/hazardous_salvage`, `sieve/wasteland_soil`, and `sieve/wasteland_recovery`.

# Wasteland City Progression-Bypass Audit

Status: **Structural metal and chest-loot bypasses remediated**

The `wastelands` cities are generated procedurally by Java code in `SettlementGenerator`; they are not structure-template NBT files that a datapack can safely replace. Both chest loot and structural blocks currently bypass Infinite Domain's intended Era 0 scavenging progression.

## Hard-coded structural iron

| Generator routine | Confirmed use | Approximate exposure |
|---|---|---:|
| Gate tower | Iron-block corners and a complete iron accent course | About 48 Iron Blocks per tower |
| Silo | Six of nine perimeter layers use Iron Blocks | 96 Iron Blocks per silo |
| Warehouse | Iron Blocks are the secondary wall material, including full top and bottom wall courses | Roughly 80-90 Iron Blocks per warehouse |
| Reinforced wall column | Some columns receive Iron Block inserts | Up to 12 Iron Blocks in an eligible column |
| Workshop | Places a functional Anvil and Smithing Table | Direct workstation bypass rather than raw material |

One silo therefore exposes 864 ingots' worth of reversible storage blocks. A single warehouse can expose roughly 720-810 ingots before counting its four loot chests.

Iron Bars are also used extensively, but vanilla Iron Bars cannot be converted back into ingots and are therefore primarily structural rather than a direct material bypass.

## Chest-loot pressure

The following values are approximate expected results per chest before multiplying by the number of chests in a building or city:

| Loot table | Expected iron ingots | Other notable bypasses |
|---|---:|---|
| Industrial Yard | 1.455 | 4.158 Iron Nuggets, 1.698 Copper Ingots, rare Anvil |
| Logistics Centre | 1.172 | Rails and Minecarts |
| Megacity | 2.357 | 2.652 Copper Ingots, 0.147 Diamonds, enchanted books |
| Military Checkpoint | 1.232 | Iron Sword, Shield, Crossbow |
| Settlement | 0.514 | — |
| Common Ruin | 0.374 | Bucket and Golden Apple |
| Zombie Village | 0.282 | Golden Apple |
| Farm Colony | — | Iron Hoe and Bucket |

A warehouse places four loot chests, so a single Industrial Yard warehouse averages about 5.8 loose Iron Ingots in addition to its structural Iron Blocks.

## Implemented structural salvage law

Infinite Domain now overrides the block loot for vanilla Iron Blocks, Gold Blocks, and all eight full Copper Block weathering/wax states. Breaking any of those blocks yields exactly one `wastelands:scrap_metal` instead of a reversible storage block.

This is deliberately a pack-wide rule, so it also applies to blocks placed by players. Raw-metal storage blocks, ores, Iron Bars, cut copper, machinery, and Netherite Blocks are excluded. That preserves legitimate mining rewards and functional construction while preventing generated city walls from collapsing directly into hundreds of ingots.

The generated loot tables live under `kubejs/data/minecraft/loot_table/blocks/` and are maintained by `ROOT_tools/build_structural_metal_salvage_loot.ps1`.

## Implemented container containment

All nine Wastelands chest tables and all five The Wasteland Reworked chest tables are now overridden. They yield generous foundational debris, salvage, limited food and medicine, and structure-themed poverty supplies. Ingots, nuggets, gems, finished metal equipment, anvils, buckets, vehicles, firearms, and enchanted books are excluded.

See `docs/WASTELAND_CONTAINER_LOOT.md` for the full policy. A later compatibility patch may still replace the generator's metal blocks visually if intact structural blocks are ever needed for building rather than salvage.

## Implementation boundary

Loot-table corrections are datapack-safe. Changing the blocks that the city generator places would still require a small compatibility mod/mixin or an upstream Wastelands configuration/source change, but that is no longer required to close the raw-ingot bypass.

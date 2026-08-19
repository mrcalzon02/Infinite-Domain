# Dimension-Tiered Ore Smelting

Direct furnace processing of ore follows a dimensional value ladder:

- Overworld and deepslate ore produces one corresponding nugget when that nugget exists.
- Nether ore produces one corresponding ingot when an ingot exists.
- Minecraft End ore produces one corresponding storage block when that block exists.
- Ore without a registered equivalent retains its upstream output.
- Stellaris planetary and Rocketnautics lunar ores are left unchanged pending a separate orbital-processing policy.

Where vanilla lacks a material form, Infinite Domain uses an existing pack equivalent.
Vanilla copper uses `create:copper_nugget`, and Create Cybernetics titanium uses
`rocketnautics:titanium_nugget`.

The rule applies to both ordinary smelting and blasting. It does not alter raw ore, dust, crushed ore, scrap recycling, food cooking, alloying, Create processing, or other machine recipes.

Oritech Endstone Platinum Ore has no upstream furnace recipe, so Infinite Domain adds explicit smelting and blasting recipes that produce one Oritech Platinum Block.

More Ores More Gems End Stone Shadow Ore likewise has no upstream furnace route. Infinite Domain adds smelting and blasting routes producing one `more_ores_more_gems:block_of_shadowite`.

Basic Nether Ores' netherrack, basalt, and soul-soil ore families are all classified as Nether ores and therefore retain ingot/bar yields. More Ores More Gems item models are included in equivalence discovery even when the most recent live registry capture predates the mod.

The generated overrides and audit are maintained by `ROOT_tools/build_dimension_tiered_ore_smelting.ps1`.

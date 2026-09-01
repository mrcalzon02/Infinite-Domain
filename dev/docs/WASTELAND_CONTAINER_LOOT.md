# Wasteland Container Loot

All fourteen structure-container loot tables supplied by `wastelands` and `the_wasteland_reworked` are overridden by Infinite Domain. The objective is to make ruins consistently productive for Era 0 survivors without allowing a chest to complete the Stone Age or unlock industrial progression.

## Container model

Every generated container rolls from four sections:

1. Four to six large stacks of foundational debris: coarse dirt, gravel, sand, limited normal dirt, dry sand, sticks, dead vegetation, flint, bones, and rotten flesh.
2. Three to five salvage selections: both mods' scrap metal, garbage bags, empty cans, cardboard boxes, cloth, decayed planks, string, paper, and small amounts of coal.
3. One to two survival selections: seeds, mushrooms, canned food, purified water, or bandages.
4. Two to three selections reflecting the structure type, such as farm supplies, industrial scrap, office paper, empty laboratory glassware, or bunker provisions.

The tables contain no ingots, nuggets, diamonds, emeralds, finished metal tools or armor, firearms, anvils, smithing tables, buckets, minecarts, enchanted books, or advanced medicine.

## Covered tables

- Wastelands: Farm Colony, Industrial Yard, Logistics Centre, Megacity, Military Checkpoint, Common Ruin, Settlement, Starter Bunker, and Zombie Village.
- The Wasteland Reworked: Bureau, Factory, Laboratory, Market, and Military.

The generated tables live beneath `kubejs/data/<namespace>/loot_table/chests/` and are maintained by `ROOT_tools/build_wasteland_poverty_loot.ps1`.

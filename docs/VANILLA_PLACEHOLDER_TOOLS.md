# Vanilla Placeholder Tool Policy

Infinite Domain retains vanilla tiered tools as recipe, advancement, quest, enchanting, and compatibility objects, but prevents them from serving as practical working tools.

## Modified tools

The sword, pickaxe, axe, shovel, and hoe for each of these vanilla materials has a maximum durability of 1:

- Wood
- Stone
- Gold
- Iron
- Diamond

This covers 25 vanilla item IDs. Item IDs, crafting recipes, enchantability, attack and mining attributes, tags, and use as recipe ingredients are otherwise preserved.

## Deliberate exclusions

- Netherite tools
- Primitive Start bone tools and their upgrades
- Modded tools
- Shears, bows, crossbows, fishing rods, flint and steel, brushes, shields, and armor

## Implementation boundary

Minecraft datapacks cannot change the registered maximum durability of every instance of an existing item. Infinite Domain therefore applies this pack rule through the installed KubeJS startup item-modification layer. A full client/server restart is required after changing the rule; `/reload` is insufficient for startup modifications.

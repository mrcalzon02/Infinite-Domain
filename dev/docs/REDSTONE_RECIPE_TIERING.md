# Redstone Recipe Tiering

Infinite Domain treats redstone circuitry as civilization-scale material rather than a dust-sized incidental ingredient.

## Construction rule

- An ingredient slot that originally accepts `minecraft:redstone` or a recognized common redstone-dust tag requires `minecraft:redstone_block`.
- An ingredient slot that originally accepts `minecraft:redstone_block` requires `allthecompressed:redstone_block_1x` through the pack's existing block-compression rule.
- Recipes already using an AllTheCompressed redstone block retain their authored compression level unless their technology tier is deliberately promoted later.

This rule applies to shaped and shapeless crafting. It does not rewrite machine-processing recipes, recipe outputs, redstone packing/unpacking, decompression, or material-recovery recipes.

The rule is maintained by `ROOT_tools/build_compressed_crafting_overrides.ps1`. Its exact substitutions are recorded in `docs/compression-audit/crafting-compression-conversion.csv`.

## Companion bulk-material rules

The same generator escalates small construction ingredients:

- Nuggets to their matching ingot or bar.
- Ingots, bars, and compactable gems to their matching storage block.
- Coal to Coal Block.
- Charcoal to Quark Charcoal Block.
- Snowball to Snow Block.
- Paper to the reversible nine-sheet `kubejs:paper_bundle`.
- Stick to the reversible nine-stick `quark:stick_block`.

Primitive Start bone pickaxes, axes, shovels, hoes, and swords deliberately retain ordinary sticks so the bootstrap survival tools remain craftable.

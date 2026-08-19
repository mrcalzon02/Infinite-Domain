# Primitive Start Recipe Restoration

Primitive Start 21.1.0 supplies twenty-nine recipes with the legacy `result.item` JSON field. Minecraft 1.21.1 requires `result.id`, causing these recipes to disappear while the registered equipment, repair rules, and enchantment information remain visible.

Infinite Domain restores every affected recipe without changing its inputs or pattern. This includes:

- Ten base bone equipment and arrow recipes.
- Seven raw-copper reinforced bone smithing upgrades.
- Seven gold-plated bone smithing upgrades.
- Reinforcement and plating smithing-template recipes.
- Primitive Start's crafting table, copper smithing table, and improvised planks recipes.

The base bone tools continue to accept `#primitivestart:sticks`, whose upstream tag contains ordinary `minecraft:stick`. These recipes are protected from the pack's Stick Block escalation.

The restoration is maintained by `ROOT_tools/restore_primitive_start_bone_recipes.ps1`, with exact outputs recorded in `docs/primitive-start-recipe-restoration.csv`.

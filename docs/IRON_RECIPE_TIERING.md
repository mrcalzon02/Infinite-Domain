# Iron Recipe Tiering

Infinite Domain applies an explicit iron-cost ladder to shaped and shapeless crafting recipes.

## Cost tiers

- **Basic:** every ingredient slot that formerly accepted one Iron Ingot or the common Iron Ingot tag now requires one `minecraft:iron_block`, equivalent to nine ingots.
- **Advanced industry:** every such slot now requires one `allthecompressed:iron_block_1x`, equivalent to nine Iron Blocks or eighty-one ingots.
- **High-energy and automated technology:** every such slot requires one `allthecompressed:iron_block_2x`, equivalent to eighty-one Iron Blocks or 729 ingots.
- **Ultra-advanced global and orbital technology:** every such slot requires one `allthecompressed:iron_block_3x`, equivalent to 729 Iron Blocks or 6,561 ingots.

The basic tier covers hand tools, armor, buckets, shears, cauldrons, cooking equipment, simple survival devices, decorative fittings, and comparable low-technology utilities.

The advanced-industry tier covers Create-era machinery, early storage systems, industrial equipment, mechanical Ex Deorum equipment, blast furnaces, hoppers, pistons, crafters, rails, cannons, pulleys, relays, and comparable infrastructure.

The high tier covers AE2, cybernetics, Oritech, power-grid equipment, nuclear systems, advanced building/mining gadgets, and their major integration components.

The ultra tier covers AE2LT, rockets, spacecraft, orbital systems, advanced aeronautics, submarines, and thruster technology.

## Guardrails

- Iron storage, decompression, and recovery recipes are not rewritten, preventing circular recipes.
- Machine-processing recipes that transform iron into another material are not rewritten by this construction-cost pass. Those processes require separate mass-balance review before their inputs can safely increase.
- Existing compressed block requirements remain in place. This system changes iron-ingot ingredient slots; it does not downgrade ingredients that were already blocks.
- `allthecompressed:iron_block_1x` is used for advanced construction. PneumaticCraft's compressed-iron alloy is a distinct material and is not substituted here.

The rule is maintained by `ROOT_tools/build_compressed_crafting_overrides.ps1`. Run that generator after recipe or mod updates to refresh the generated overrides and audit CSV.

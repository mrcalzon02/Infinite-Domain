# Compressed Crafting Conversion

Direct block-item ingredients in shaped and shapeless crafting recipes are converted to their 1x AllTheCompressed equivalents. One compressed block represents nine ordinary blocks.

- Mode: applied
- Recipes converted or proposed: 2307
- Direct ingredient substitutions: 3136
- Compressible block families available: 103
- Reversible material promotions discovered: 190
- Common material-tag aliases covered: 486
- Existing hand-authored recipe overrides protected: 2256
- Compression/material-recovery recipes protected: 1111
- Stale previously generated overrides removed: 0
- Source JSON parse failures: 0

## Guardrails

- AllTheCompressed recipes are excluded to prevent circular compression recipes.
- Ex Deorum compressed-material recipes and single-input recovery conversions are excluded.
- The ordinary crafting table is retained as the bootstrap needed to make the first 1x compressed block.
- Recipe results are never rewritten.
- Common material tags are replaced by a canonical installed target proven by a reversible recipe.
- Existing Infinite Domain/KubeJS overrides are preserved.
- Machine-processing recipes are not included in this pass.
- Vanilla and Quark full furnace variants remain 3x-compressed milestone exceptions.
- Iron construction tiers are Iron Block, 1x advanced, 2x high-energy/automated, and 3x global/orbital.
- Iron storage, compression, and recovery recipes are protected from circular conversion.
- Redstone Dust construction inputs become Redstone Blocks; original Redstone Block inputs become 1x Compressed Redstone Blocks through the general compression rule.
- Redstone packing, unpacking, storage, and recovery recipes are protected from circular conversion.
- Iron Nuggets become Iron Ingots; Coal and Charcoal become their distinct storage blocks; Snowballs become Snow Blocks; Paper and Sticks become nine-unit bundles.
- Other nuggets become their reversible ingot/bar equivalent; other ingots, bars, and gems become their reversible storage-block equivalent.
- Material promotion is single-pass: a nugget becomes an ingot, never an ingot and then a block during the same generation.
- Every discovered packing/unpacking result is protected from rewriting to prevent circular recipes.
- Primitive Start bone tool recipes retain ordinary sticks as an explicit bootstrap exemption.

Regenerate after mod updates or recipe-set changes. Review crafting-compression-conversion.csv for the exact substitutions.

# Material Recipe Tiering

Infinite Domain promotes construction ingredients by one reversible material
tier in shaped and shapeless crafting recipes:

- Nuggets become the matching ingot or bar.
- Ingots and bars become the matching storage block.
- Gems and other compactable material units become their matching storage block.
- Common material tags are resolved to a canonical installed target with a
  verified reversible conversion.

Equivalences are discovered from installed one-to-nine unpacking recipes. This
allows unconventional mod IDs to participate without assuming that similarly
named items are interchangeable. Food-like compactables are excluded from this
construction-cost pass.

## Safety rules

- Each ingredient receives at most one promotion per generator pass. A nugget
  becomes an ingot, never a block in the same pass.
- Packing, unpacking, decompression, storage, and single-input recovery recipes
  are protected from rewriting.
- Recipe results are never rewritten.
- Only shaped and shapeless crafting recipes are included; machine processing
  remains unchanged.
- Hand-authored KubeJS recipe overrides remain authoritative.
- Iron retains its separate namespace- and era-sensitive cost ladder.
- The generator reads original jar recipes rather than its prior output, so
  rerunning it cannot recursively promote already generated ingredients.

### Manual cross-mod recipes

The four core Building Gadgets are intentionally removed from the generated
override manifest and maintained as hand-authored recipes. Their ordinary route
now requires AE2 processors/cores and energy or spatial infrastructure alongside
3x–4x compressed iron:

- Building Gadget: Formation Cores, Engineering Processor, Dense Energy Cell;
- Exchanging Gadget: Formation and Annihilation Cores, Engineering Processor,
  Dense Energy Cell;
- Destruction Gadget: Annihilation Cores, Engineering Processor, Dense Energy
  Cell;
- Copy-Paste Gadget: Formation and Annihilation Cores, Engineering Processor,
  16³ Spatial Cell Components.

The generator reports these as protected manual overrides and must not recreate
their former vanilla-only ingredient layouts.

The same protection applies to curated progression gateways installed by
`scripts/apply_deep_recipe_integrations.py`. The integration installer validates
registered ingredients and removes its recipe IDs from the compression manifest,
so cost scaling cannot erase functional cross-mod requirements. Recommended
maintenance order is:

1. run `ROOT_tools/build_compressed_crafting_overrides.ps1`;
2. run `scripts/apply_deep_recipe_integrations.py`;
3. rebuild the effective recipe index;
4. run `scripts/audit_era_recipe_integration.py`.

The system is maintained by
`ROOT_tools/build_compressed_crafting_overrides.ps1`. Exact equivalences and
substitutions are recorded in `docs/compression-audit/`.

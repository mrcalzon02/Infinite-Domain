# Infinite Domain Recipe Scaling Overview

## Current effective recipe set

The installed pack contains 21,023 unique recipe IDs. After datapack priority
and KubeJS overrides are applied, 20,945 are enabled and 78 are deliberately
disabled compatibility recipes.

- Effective KubeJS winners: 4,863
- Recipe IDs with more than one definition: 4,654
- Existing cross-namespace integration candidates: 4,561
- Recipes with normalized static inputs and outputs: 20,260
- Effective JSON parse failures: 0

The authoritative planning catalog is `docs/recipe-index/recipe-index.csv`.

## Scaling layers

### Shaped and shapeless construction crafting

The crafting-scaling generator currently owns 2,311 recipes and performs 3,151
direct substitutions.

- Ordinary compressible block ingredients become their 1x AllTheCompressed
  form. The installed catalog contains 103 supported base block families.
- Iron ingots use an era/namespace ladder: Iron Block for basic recipes, then
  1x, 2x, or 3x compressed Iron Blocks for advanced, high-energy, and
  global/orbital technology.
- Redstone Dust becomes a Redstone Block. An originally required Redstone Block
  is independently eligible for 1x block compression.
- Nuggets become the matching ingot or bar.
- Ingots, bars, compactable gems, raw metals, alloys, and comparable reversible
  material units become their matching storage block.
- Coal, charcoal, snowballs, paper, and sticks use their established bulk
  equivalents.
- Quark's full blackstone and deepslate furnaces remain explicit 3x-compressed
  Era 0 milestones.

Material promotion currently contains 190 installed reversible equivalences
and 486 common-tag aliases.

### Dimensional ore smelting

The smelting policy audits 408 ore-smelting and blasting routes:

- Overworld metal ores yield nuggets when a valid material-family nugget exists.
- Nether ore variants retain full ingot/bar output.
- Selected End ores yield storage blocks.
- Other planetary/dimensional routes remain unchanged until their own orbital
  processing policy is defined.
- Gem ores without a valid nugget equivalent retain their gems.

There are 96 effective KubeJS definitions associated with this tiering system.

### Ex Deorum fallback scaling

Ex Deorum has 1,692 effective sieve overrides:

- Each input/mesh table retains one guaranteed baseline result.
- All non-baseline chances are multiplied by 0.025.
- Compressed sieve baselines are capped at one guaranteed item.
- Server settings separately slow manual sieving and composting and increase
  mechanical power costs.

### Repairs, restoration, and disabled compatibility

- 29 Primitive Start recipes are restored to valid Minecraft 1.21 JSON.
- 14 malformed upstream recipes are repaired.
- 78 invalid or unavailable compatibility recipes are deliberately disabled.
- 643 additional KubeJS winners are hand-authored or subsystem-specific and do
  not belong to the three bulk-scaling generators above.

## Non-recursion and circularity protection

- Scaling reads original JAR recipes, not previously generated overrides.
- Each ingredient receives at most one material-tier promotion per pass.
- Recipe results are never scaled.
- Packing, unpacking, decompression, storage, and single-input recovery recipes
  are protected.
- AllTheCompressed's own recipes are excluded.
- Machine-processing recipes are excluded from the construction-crafting pass.
- Existing hand-authored KubeJS overrides are protected.
- Primitive Start bone tools retain normal sticks for bootstrap viability.

## Cross-mod integration workflow

1. Filter `recipe-index.csv` by output, input, recipe namespace, recipe type, or
   `cross_mod_candidate=True`.
2. Inspect `recipe-inputs.csv` and `recipe-outputs.csv` for normalized quantities.
3. Check `recipe-definitions.csv` before editing; it shows every shadowed source
   and which definition currently wins.
4. Put the integration recipe at the row's `recommended_override_path`. Never
   edit a mod JAR.
5. If `scaling_class=crafting_material_scaling`, do not hand-edit the generated
   file without first promoting that recipe to a protected manual override or
   incorporating the integration into the generator. Otherwise regeneration
   will replace the edit.
6. Rebuild this index after every recipe generation pass or mod update with
   `python scripts/build_effective_recipe_index.py`.

## Index files

- `recipe-index.csv`: winning recipe definition and edit path for every ID.
- `recipe-inputs.csv`: one row per normalized input reference.
- `recipe-outputs.csv`: one row per normalized output reference.
- `recipe-definitions.csv`: complete source-priority and override history.
- `cross-mod-candidates.csv`: recipes already connecting multiple namespaces.
- `recipe-index.json`: normalized machine-readable catalog.
- `parse-failures.csv`: effective static-analysis gaps; currently empty.

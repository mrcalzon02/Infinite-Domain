# Effective Recipe Index

Generated from Minecraft 1.21.1, every installed mod JAR, and the current
`kubejs/data` overrides. KubeJS definitions win over matching JAR recipe IDs.

| Measure | Count |
|---|---:|
| Unique recipe IDs | 21096 |
| Enabled effective recipes | 21018 |
| Deliberately disabled recipes | 78 |
| Effective KubeJS overrides | 4951 |
| IDs with multiple definitions | 4677 |
| Cross-mod integration candidates | 4737 |
| JSON parse failures | 0 |
| Recipes with normalized inputs and outputs | 20333 |

## Scaling coverage

| Classification | Recipes |
|---|---:|
| `unscaled` | 16917 |
| `crafting_material_scaling` | 2276 |
| `ex_deorum_probability_scaling` | 1692 |
| `dimension_tiered_smelting` | 90 |
| `disabled_compatibility` | 78 |
| `primitive_recipe_restoration` | 29 |
| `recipe_repair` | 14 |

## Recipe types

Top 40 types are shown here; `recipe-index.csv` contains every type.

| Type | Recipes |
|---|---:|
| `minecraft:crafting_shaped` | 7757 |
| `minecraft:crafting_shapeless` | 3807 |
| `minecraft:stonecutting` | 1498 |
| `exdeorum:sieve` | 1063 |
| `exdeorum:compressed_sieve` | 846 |
| `minecraft:smelting` | 534 |
| `create:crushing` | 462 |
| `minecraft:blasting` | 410 |
| `create:milling` | 262 |
| `createmetallurgy:melting` | 231 |
| `createcybernetics:engineering_table` | 227 |
| `create:deploying` | 184 |
| `create:mechanical_crafting` | 144 |
| `oritech:pulverizer` | 124 |
| `create:mixing` | 120 |
| `farmersdelight:cutting` | 120 |
| `immersiveengineering:crusher` | 114 |
| `oritech:grinder` | 114 |
| `createmetallurgy:casting_in_table` | 112 |
| `immersiveengineering:metal_press` | 97 |
| `create:cutting` | 92 |
| `immersiveengineering:arc_furnace` | 88 |
| `create:filling` | 81 |
| `(unresolved)` | 78 |
| `create_aquatic_ambitions:channeling` | 77 |
| `create:splashing` | 72 |
| `immersiveengineering:sawmill` | 72 |
| `ae2:matter_cannon` | 68 |
| `create:pressing` | 66 |
| `createmetallurgy:grinding` | 63 |
| `exdeorum:barrel_compost` | 63 |
| `minecraft:smithing_transform` | 62 |
| `immersiveengineering:blueprint` | 61 |
| `oritech:assembler` | 57 |
| `create:compacting` | 55 |
| `ae2lt:lightning_assembly` | 52 |
| `oritech:centrifuge_fluid` | 49 |
| `ae2lt:overload_processing` | 48 |
| `cyber_ware_port:assembly` | 46 |
| `cyber_ware_port:engineering` | 46 |

## Files

- `recipe-index.csv`: one editable-planning row per winning recipe definition.
- `recipe-inputs.csv`: normalized input references and declared quantities.
- `recipe-outputs.csv`: normalized output references and declared quantities.
- `recipe-definitions.csv`: every definition in source-priority order, including shadowed recipes.
- `cross-mod-candidates.csv`: recipes already crossing namespace boundaries.
- `recipe-index.json`: normalized machine-readable form of the effective index.
- `parse-failures.csv`: resources requiring manual decoding, if any.

`recommended_override_path` is where a modified recipe should be placed. Never
edit a mod JAR directly.

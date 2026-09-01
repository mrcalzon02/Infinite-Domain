# More Ores More Gems Tool Gating

More Ores More Gems supplies 70 complete tool families: 350 active axe, hoe, pickaxe, shovel, and sword recipes. These tools are not covered by Infinite Domain's one-durability vanilla placeholder rule.

The former all-Titanium safety gate has been replaced by era-material handles. The material forming the head or blade remains unchanged, while every handle position now uses the assigned era's material gate:

| Era | Handle material |
|---:|---|
| 1 | `minecraft:stick` |
| 2 | `minecraft:iron_ingot` |
| 3 | `minecraft:diamond` |
| 4 | `more_ores_more_gems:electrum_ingot` |
| 5 | `more_ores_more_gems:titanium_stick` |
| 6 | `more_ores_more_gems:tungsten` |
| 7 | `stellaris:desh_ingot` |
| 8 | `kubejs:infinite_domain_core` |

The assignment comes from the installed-JAR property audit and material floor in `docs/era-tool-map/momg-era-tool-map.csv`. This makes the recipes tunable by era without allowing a low-stat family to bypass its head material or a high-stat family to remain available from an ordinary stick.

The override deliberately replaces the complete handle ingredient. Original alternate handles therefore cannot bypass the assigned era.

## Maintenance

Run `ROOT_tools/build_momg_titanium_tool_handles.ps1` after changing the More Ores More Gems JAR. The generator requires exactly 350 matching recipes and stops with an error if a future mod version changes that number or removes the expected handle key. Its audit is `docs/material-catalog/momg-titanium-tool-handles.csv`.

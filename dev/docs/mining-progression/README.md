# Infinite Domain ore-era progression

This directory is the authoritative block-side companion to the ERA Tool Map.
It separates three properties that Minecraft treats independently:

1. `material_era`: when the ore's material becomes a normal economic input.
2. `minimum_tool_era`: the earliest tool that may receive the ore's drops.
3. `physical_hardness`: the block's installed destroy-time value, which affects
   mining time but does not itself decide whether drops are allowed.

## Base ladder

| Tool era | Intended tools | Ores opened |
|---:|---|---|
| Bone (pre-Era 0) | wooden and bone pickaxes | ordinary stone only |
| 0 | stone pickaxe | copper, coal, lapis, and other Era 1 feedstocks |
| 1 | copper-reinforced and gold-plated bone picks | iron, gold, and other Era 2 industrial feedstocks |
| 2 | iron pickaxe | diamond, redstone, emerald, quartz, sulfur, and other Era 3 feedstocks |
| 3 | diamond pickaxe | Era 4 electrical/specialty feedstocks and vanilla diamond-only blocks |
| 4 | first post-diamond tools / netherite | Era 5 titanium, tungsten, platinum, and cobalt feedstocks |
| 5 | automated-industry specialist tools | Era 6 radioactive feedstocks |
| 6 | high-energy specialist tools | Era 7 extraterrestrial and capstone feedstocks |
| 7–8 | orbital and Infinite Domain tools | reserved for final tuning and future Era 8 resource gates |

Gold is a deliberate same-era sub-step: copper is opened by stone, the
copper-reinforced pick opens gold, and gold produces the plated Era 1 pick.

## Generated implementation

- `ore-era-map.csv` inventories every live ore block and records both material
  and minimum-tool eras.
- `kubejs/data/infinite_domain/tags/block/needs_era_N_tool.json` contains ores
  requiring a tool from Era N or later.
- `incorrect_for_era_N_tool.json` is cumulative, so a tool cannot skip several
  eras merely because its original mod knew only vanilla's four tiers.
- `incorrect_for_bone_tool.json` keeps bone below stone and includes every
  later requirement layer.
- `kubejs/startup_scripts/era_mining_tiers.js` assigns these cumulative tags to
  the verified ordinary pickaxes. Powered and modular tools remain excluded
  until their custom breaking behavior is confirmed.

Regenerate with `python ROOT_tools/build_era_mining_progression.py`.

## Current verified coverage

- 265 live ore blocks across 17 namespaces are assigned with no unassigned or
  duplicate entries.
- 80 verified ordinary pickaxes have cumulative harvest requirements.
- Hardness is captured for 247 of 265 ores, including MOMG, Basic Nether Ores,
  vanilla, Stellaris, Immersive Engineering, Oritech, Enviromine, Ice and Fire,
  Wasteland Reworked, and Create Cybernetics. The remaining 18 Create-family
  values are still marked for installed-property capture; they are not guessed.

The installed MOMG hardness values range from 1 to 8 and are highly irregular
inside the same era. They are evidence for the next tuning pass, not yet a
license to normalize every block. Harvest-tier corrections are active first;
physical-hardness changes will be applied only after comparable values from the
other installed mods and representative mining-time checks are available.

## Serious break corrected

Primitive Start's installed custom tier tags were not cumulative. A bone pick
only checked its copper tag, and the copper-reinforced pick only checked the
vanilla iron tag, allowing later mod ores to fall through gaps. The generated
incorrect-block tags close that structural bypass across all assigned eras.

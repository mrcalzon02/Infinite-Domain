# Era mining quest and recipe reachability

This report validates the required hand-tool quest at each mining transition against the effective recipe index and authoritative ore map.

- Gateway checks: 9
- Passing: 9
- Failing: 0
- Ore blocks covered by the mining map: 265

| Material era | Ore blocks | Required gateway |
|---:|---:|---|
| 1 | 59 | `primitivestart:reinforced_bone_pickaxe`, `primitivestart:plated_bone_pickaxe` |
| 2 | 63 | `minecraft:iron_pickaxe` |
| 3 | 66 | `minecraft:diamond_pickaxe` |
| 4 | 20 | `more_ores_more_gems:electrum_pickaxe` |
| 5 | 18 | `more_ores_more_gems:titanium_pickaxe` |
| 6 | 26 | `more_ores_more_gems:uranium_pickaxe` |
| 7 | 13 | `more_ores_more_gems:adamantite_pickaxe` |

The gold-plated bone pick is intentionally a same-level Era 1 side-grade. Era 7 is the current maximum ore-mining level; Era 8 does not claim a nonexistent ore tier.

Detailed machine-readable evidence is in `era-mining-gateway-reachability.csv`.

Regeneration order: run `generate_eras_2_8.js`, `generate_mastery_quests.js`, `build_quest_expansion.js`, `repair_era0_quests.js`, `repair_era1_quests.js`, `apply_era_mining_quest_progression.js`, `build_jaffa_quest_line.js`, `build_reautomated_quest_line.js`, and finally `build_era0_pack_basics_quests.js`. Then run the mining, Jaffa, Re-Automated, Era 0 Pack Basics, Echo-store, and global quest audits.

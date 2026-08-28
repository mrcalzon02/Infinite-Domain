# Generator scripts — quarantined

Every script in this folder **writes to live pack data** (`config/ftbquests/`,
`kubejs/data/`). They are here, separate from `scripts/` audits/validators, so it
is obvious that running one mutates the pack.

## Rules

1. **Nothing in here runs automatically.** No script calls another. No CI, no git
   hooks, no Claude hooks invoke these. The only way one runs is you typing its
   name.
2. Run one **deliberately, for its own purpose**, then re-run the audits
   (`python scripts/audit_quest_tree_coherence.py`,
   `node scripts/audit_ftbquests.js --allow-automatic-icons`).
3. If a full rebuild of a family is needed, run its members **by hand in order**
   (below). Do not re-add `child_process` / `subprocess` chaining.

## What each script owns

| Script | Writes | Notes |
|---|---|---|
| `generate_eras_2_8.js` | Era 2–8 chapters + lang + `kubejs/data/infinite_domain/recipe/era_*` | Full Era 2–8 spine. Carries the branch reward-rhythm tables. |
| `build_organic_metallurgy_quests.js` | Era 1–8 chapters + lang | The `7x11*` mineral-trace / metallurgy ancillary chain. |
| `build_reautomated_quest_line.js` | Era 3 chapter + lang | The `6301*` Re-Automated line. |
| `apply_branch_rhythm_rewards.py` | Era 2–8 chapters | Quest-4 utility + quest-7 AE2/cyber teaser rewards. |
| `assign_era_reward_bags.py` | Era 1–8 + 12 side chapters | Supply-bag / priority-cache rewards on gear lessons. |
| `apply_era_mining_quest_progression.js` | Era 0 + Era 1 chapters + lang | Mining-gateway hand-tool progression. |
| `repair_era0_quests.js` | Era 0 chapter + lang | |
| `repair_era1_quests.js` | Era 1 chapter + lang | |
| `build_era0_pack_basics_quests.js` | Era 0 chapter + lang | Pack-basics onboarding nodes. |
| `build_jaffa_quest_line.js` | Era 1 chapter + lang | `610110*` Jaffa line. |
| `build_quest_expansion.js` | AE2 Recovery / Cyberware / specialization chapters + lang | |
| `generate_mastery_quests.js` | `mastery_era_0*` chapters + lang | |
| `generate_stellaris_space_industry.py` | `stellaris_space_industrialization.snbt` + lang + space recipes | |
| `build_coffee_tea_quests.py` | `coffee_tea_economy.snbt` | |
| `build_industrial_food_quests.py` | `feeding_the_domain.snbt` | |
| `build_mutant_mekanite_threat_quests.py` | `mutant_and_mekanite_threat_dossier.snbt` + lang | |
| `build_spore_threat_quests.py` | `the_rot_spore_threat_dossier.snbt` + lang | |
| `build_cyberspace_darknet_campaign.py` | `darknet_draconic_convergence.snbt` + lang + recipes | |
| `ensure_ftbquest_icons.js` | Era 1–8 chapters (icons). `--chapter=<file>` scopes it. | |
| `dedupe_ftbquest_localization.py` | `quests/lang/en_us.snbt` | |
| `localize_quest_item_names.py` | `quests/lang/en_us.snbt` | |
| `apply_charles_voice_templates.py` | `quests/lang/en_us.snbt` | |
| `build_spore_structure_loot.py` | `kubejs/data/spore/loot_table/chests/*` | |

## Full Era 2–8 rebuild order (only if genuinely rebuilding)

```
node scripts/generators/generate_eras_2_8.js
node scripts/generators/build_organic_metallurgy_quests.js
node scripts/generators/build_reautomated_quest_line.js
python scripts/generators/apply_branch_rhythm_rewards.py
python scripts/generators/assign_era_reward_bags.py
node scripts/generators/ensure_ftbquest_icons.js
```

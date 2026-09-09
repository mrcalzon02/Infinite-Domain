# Custom-content error audit — 2026-09-09

Repository `mrcalzon02/Infinite-Domain`, branch `main`, starting `HEAD`
`df5e37f94818283ccb7df6f4b524ec8acbb16f94` (clean at session start).

Read-only audit. **No game content was changed.** Running the project's own audit
suite regenerated ~50 report files under `dev/docs/**` as a side effect; see
[Working-tree effects](#working-tree-effects).

## Method

| Ladder level | What ran | Coverage |
|---|---|---|
| 1 syntax/schema | independent parse of every authored file | 25,113 JSON/mcmeta, 49 SNBT, 11 TOML, 45 JS, 775 NBT |
| 3 registration | every id referenced by custom content resolved against the **live** registries | 10,589 item, 261 block, 82 biome, 294 structure, 29 feature, 2 fluid refs |
| 3 tags | 231 tag references resolved, including nested `#tag` flattening | vanilla + NeoForge + 193 mod jars + pack |
| 4 gameplay data | the project's own validators | 123 scripts |
| 5 NBT integrity | palette-accurate walk of every structure template | 18,140 palette entries in 775 files |
| 8 controlled startup | pinned NeoForge 21.1.248 fixed-seed server | booted, 16 chunks, 0 ERROR/FATAL |

The live registries matter: `dev/docs/registry-inventory/item-ids.txt` was captured
2026-08-16 and its own README declares it stale. A temporary KubeJS probe dumped
the real registries from the running server — **item 16,931** (inventory says
16,552), block 12,216, biome 118, structure 521, template_pool 844, entity_type
590. Several existing validator failures are stale-inventory artefacts, not
content defects.

Reproduce: `dev/scripts/run_worldgen_benchmark.ps1 -Variant baseline -Suite smoke`
with a probe that logs `reg.keySet()` per registry on `ServerEvents.loaded`, then
resolve references against it. The probe was removed after harvesting.

---

## Critical

### C1 — The End is unreachable in any new world

`infinite_domain:nether/lyran_research` holds the pack's only End portal. Its
jigsaw start-pool element cannot load, so the structure never generates.

The chain is correct right up to the last link:

| Step | File | State |
|---|---|---|
| structure set places it | `worldgen/structure_set/nether/lyran_research.json` (random_spread 40/16) | OK |
| structure registered | `worldgen/structure/nether/lyran_research.json`, `start_pool: infinite_domain:nether/lyran_research` | OK — present in the live registry (521 structures) |
| template pool loads | `worldgen/template_pool/nether/lyran_research.json`, element `location: infinite_domain:nether/lyran_research` | OK — present in the live registry (844 pools) |
| **element NBT** | needs `kubejs/data/infinite_domain/**structure**/nether/lyran_research.nbt` | **MISSING** |

The NBT exists, at
`kubejs/data/infinite_domain/**worldgen/structure**/nether/lyran_research.nbt` —
beside the structure JSON, where Minecraft never looks for templates. This is the
only one of the pack's 697 runtime NBTs at a `worldgen/` path; the other 696 are
correctly under `data/<ns>/structure/`.

Severity is total because the fallback routes are deliberately closed:

- `minecraft:has_structure/stronghold` → `{"replace": true, "values": []}`
- `minecraft:stronghold_biased_to` → `{"replace": true, "values": []}`
- `minecraft:eye_of_ender_located` → only `infinite_domain:nether/lyran_research`

So no stronghold generates, and thrown eyes track a structure that cannot exist.
Existing saves with a pre-generated stronghold are unaffected.

Fix: move the file to `kubejs/data/infinite_domain/structure/nether/lyran_research.nbt`.
Same bug class as the Deep Nether igniter tag — correct content, wrong path.

---

## High

### H1 — Six chapter icons contradict the audits that define them

Last session's `dev/docs/ftbquests-chapter-icons.json` was introduced as the icon
authority without discovering that six audits **already assert** specific chapter
icons. The manifest overrode them:

| Chapter | Audit expects | Manifest set |
|---|---|---|
| `create_specialist_workshops` | `compactgearbox:sequential_gearbox` | `create:mechanical_saw` |
| `create_big_cannons_doctrine` | `createbigcannons:cannon_mount` | `createbigcannons:bronze_cannon_barrel` |
| `graveyard_gateway_containment` | `gateway_of_doom:portal_ward_3` | `graveyard:blackstone_gravestone` |
| `powered_field_engineering` | `mininggadgets:mininggadget` | `create:portable_storage_interface` |
| `supplementaries_civic_utility` | `supplementaries:relayer` | `supplementaries:notice_board` |
| `grid_storage_and_recovery` | `powergrid_batteries:small_battery` | `create:item_vault` |

These six audits were **already failing before** last session's change (no chapter
had any icon at commit `4910765c`), so this is not a new breakage — but the
manifest is now wrong against the project's own documented intent and should adopt
the audit values.

Those audits also assert the **string** form (`icon: "ns:id"`), which FTB Quests
cannot read and deletes on save. They need updating to the compound form
`icon: { id: "ns:id" }` at the same time, or they will keep failing after the
manifest is corrected. See `dev/docs/FTBQUESTS_CHAPTER_ICONS.md`.

Also asserted and worth reconciling: `audit_create_applied_kinetics_quests.py`
(one quest icon) and `audit_terminal_quest_theme.py` (`EXPECTED_ICONS`, 7 quest
icons) — both in string form.

### H2 — Three structure palettes reference blocks that do not exist

Palette-accurate check of 18,140 entries across 775 NBTs; 0 parse failures.

| Block in palette | Reality | Files |
|---|---|---|
| `infinite_domain:ruined_blast_furnace` | does not exist; the real block is **`kubejs:ruined_blast_furnace`** | 8 (6 shipping deep-sea structures + 2 unreferenced `_clean_master`) |
| `ae2:terminal` | exists as an **item** only, never a block — it is a cable part | 3 (`ows_006`, `ows_007`, `ows_008`) |
| `minecraft:grass` | renamed to **`minecraft:short_grass`** in 1.20.3 | 2 (`structure_library/extracted/creativelands_cc0/`, donor input, likely non-shipping) |

The affected deep-sea structures are live: `abyssal_mining_rig`,
`akula_wreck_aft`(+`_damaged`), `akula_wreck_spine`, `akula_wreck_forward`,
`coastal_patrol_wreck` are all referenced by worldgen structure/template files.

---

## Medium

### M1 — Seven ingredient tags do not exist, so their recipes can never be satisfied

After adding vanilla and NeoForge tags to the index (they live in the pinned
server install, not in `mods/`), 178 item/block tag references resolve to 7 real
misses:

| Tag | Referenced by | Note |
|---|---|---|
| `#neoforge:rods/iron` | `kubejs/data/createdieselgenerators/recipe/crafting/engine_piston_from_rods.json` | **`#c:rods/iron` exists** — one-word fix |
| `#c:redstone_acid` | `kubejs/data/immersiveengineering/recipe/crafting/capacitor_hv.json` | no provider |
| `#c:ores/{boron,cobalt,iridium,magnesium,thorium}` | 5 `kubejs/data/exdeorum/recipe/compressed_sieve/**` files | no mod provides those ores |

### M2 — 125 of 10,589 item references are dead

1.2% unresolved, all in third-party recipe overlays copied into `kubejs/data`, not
in the pack's own content:

- 49 **dead namespace** — no installed mod owns it: `aether:*`, `blue_skies:*`,
  `chipped:*`, `buzzier_bees:*`, `cave_enhancements:*`, `caverns_and_chasms:*`
- 76 **missing id** — namespace present but the id is not: `ars_nouveau:*`,
  `biomesoplenty:*`

These sit largely under `kubejs/data/exdeorum/` (1,795 files — a large partial
overlay of Ex Deorum's 2,245 recipes) and `kubejs/data/supplementaries/`,
`sophisticatedstorage/`. Minecraft skips such recipes with a load warning, which
is consistent with the 48 runtime recipe warnings
`audit_runtime_log_ownership.py` reports. Not a blocker; a hygiene decision about
whether the pack should carry compat recipes for uninstalled mods.

### M2b — Correction: 32 legacy-path tags actually load empty, not 110

`dev/scripts/audit_legacy_tag_paths.py` was rewritten by a concurrent session to
distinguish the harmless cases, and its result supersedes the figure quoted on
2026-09-08. Of 123 legacy-path tag files:

| State | Count |
|---|---|
| **BROKEN** — nothing supplies the tag at the singular path, so it loads empty | **32** |
| SUSPECT — jar ships both paths but the legacy file has extra values | 1 |
| ported — a pack file covers it (the 2026-09-08 fixes) | 7 |
| harmless — the same jar also ships the singular path | 76 |
| harmless — the legacy file has no values at all | 7 |

The earlier "110 not fixed" counted a pack file merely *existing* at the singular
path, and did not notice that most mods ship both paths. 32 is the real exposure.

### M3 — Four resource-pack `.mcmeta` files are malformed JSON

Trailing comma in the `frames` array, in the pack's own
`resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1` (28,604 tracked files):

- `assets/enviromine/textures/block/block_gas.png.mcmeta`
- `assets/enviromine/textures/block/block_gas_fire.png.mcmeta`
- `assets/enviromine/textures/block/davy_lamp_gas.png.mcmeta`
- `assets/enviromine/textures/block/davy_lamp_lit.png.mcmeta`

GSON is lenient in several of Minecraft's metadata paths so these may load
anyway; strictly they are invalid and the fix is deleting four commas. Not
confirmed either way in game — a dedicated server does not load assets.

---

## Validator-suite health

123 `audit_/validate_/verify_/check_/test_` scripts ran: **67 pass, 26 report
content problems, 30 are themselves broken.** A broken validator cannot judge
content, so those 30 are blind spots, not clean results.

| Class | Count | Examples |
|---|---|---|
| crash | 22 | 8× chapter-icon assertions (H1); `verify_ows009_gate_a_*` (7 scripts, all on one obstruction at `(14, 2, 31)` plus an NBT SHA drift); `validate_ows010_final_builder` D3 drift; `audit_texture_quality` broken image stream |
| missing input | 4 | `audit_terminal_quest_theme`, `validate_creativelands_extraction`, `validate_phase16_selection`, `validate_structure_qa_world` |
| needs args | 3 | `validate_material_profile`, `validate_regional_assignment`, `validate_regional_structures` (all need `--culture`) |
| import error | 1 | `audit_cyberspace_darknet_campaign` cannot import `build_cyberspace_darknet_campaign` |

### Confirmed false positives caused by the stale registry inventory

- `audit_generated_state_values.py` fails with `UNKNOWN_BLOCK kubejs:ruined_*` for
  11 blocks. **All 11 exist in the live registry** (block *and* item). The
  validator reads the 2026-08-16 inventory. Refresh the inventory or point these
  validators at a live dump.
- `audit_domain_compendium_chapter.py` reports "9891 task ids, 0 well-formed item
  tasks". Its regex expects tasks on one line
  (`id: "…", item: { … }, type: "item"`); the file stores them multi-line. The
  chapter is **healthy**: 9,892 item tasks, **zero** `missing_item`, and all
  **9,893 distinct item ids resolve** against the live registry.

### Genuine content failures worth triaging separately

`audit_quest_loot_attainability.py` reports 9 critical `QUEST-STRUCT-UNPLACED` and
3 `LOOT-ORPHAN` (report at `dev/docs/quest-loot-attainability/report.json`);
`audit_inbuilt_structures.py` and `audit_structure_block_fitness.py` report 35
functional/machine blocks used as set dressing without an approved exception, plus
missing audit renders; `validate_habitation_family.py` reports 8 structures
missing purpose fixtures. These overlap the known Old World generation issue and
the structure admission pipeline; they are pre-existing programme state, not new
regressions.

---

## What is clean

Worth stating, because it bounds the search:

- **block, biome, structure, placed_feature and fluid references: 0 unresolved**
  (261 / 82 / 294 / 29 / 2).
- **775 structure NBTs parse**; 0 malformed, 0 non-existent entity ids.
- **475 of 476 jigsaw template references resolve** (the exception is C1).
- Syntax across 25,113 JSON, 49 SNBT, 11 TOML, 45 JS: **4 findings**, all M3.
- The three biome tags reported "empty" are intentionally empty quarantine tags
  (`disabled_primitive_wasteland_settlements`,
  `disabled_quarantine_deep_sea_structures`, `custom_worldgen:no_biomes`).
- The pinned server boots the pack and generates chunks with **0 ERROR/FATAL**.
- Last session's fixes are all present in `df5e37f9` and verified: the Deep Nether
  igniter tag, the Lost Cities biome attachment (14 biomes), the six ported
  `lostcities:*` block tags, 45 compound chapter icons, 371 compound quest icons.

## Working-tree effects

Running the project's own audits regenerated their report files. At close:

| Origin | Paths |
|---|---|
| this audit | ~50 regenerated reports under `dev/docs/**` plus `docs/custom-content-audit/quest-icon-review.csv` |
| concurrent session(s) | `dev/scripts/audit_legacy_tag_paths.py`; `dev/scripts/endgame/validate_hive_world_smoke.py`; `kubejs/server_scripts/hive_world_expedition.js`; `kubejs/data/infinite_domain/function/hive_world/build_arrival.mcfunction` |

The concurrent edits are substantive fixes from other sessions (a KubeJS
`event.cancel()` dead-code bug and a ladder-backing fix) and were left untouched.
`HEAD` did not move during this audit.

Note on `quest-icon-review.csv`: it grew 175 → 495 rows because it was stale, and
Era chapter rows went **42 → 0** — last session's explicit quest icons removed
them from the ambiguous-icon list, which is the intended direction.

## Recommended order

1. **C1** — move one NBT file. Unblocks End progression.
2. **H2** — `infinite_domain:` → `kubejs:ruined_blast_furnace` in 8 palettes;
   decide a real block for `ae2:terminal`; `minecraft:grass` → `short_grass`.
3. **H1** — adopt the six audit-defined icons in the manifest, and convert those
   audits (plus the 8 quest-icon assertions) to the compound form.
4. **Refresh `dev/docs/registry-inventory/`** from a live dump. It is 3+ weeks
   stale and is actively producing false validator failures.
5. **M1** — `#neoforge:rods/iron` → `#c:rods/iron`; decide on the six no-provider tags.
6. Repair the 30 broken validators, or the suite's 67 passes overstate confidence.
7. **M2/M3** — hygiene.

## Not covered

- Fresh-world natural generation and Lost Cities visual placement (ladder 9–10):
  not run. Lost Cities generates as a *feature*, so it never appears in structure
  instrumentation and a 4×4-chunk smoke tile cannot evidence city distribution.
- Client-side load: no client was launched, so resource-pack, model and texture
  loading (including M3) is unverified.
- Java compilation of `dev/packdev/` companion mods was not run;
  `audit_companion_mod_packages.py` reports installed-vs-source resource drift for
  `cyberware-mastery-expansion` and `darknet-worldgen-patch`, and
  `overworld-terrain-companion` has an incomplete source tree.

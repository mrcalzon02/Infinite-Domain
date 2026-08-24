# Infinite Domain — Project Index

*Generated 2026-08-23. This is a map of the instance folder: what lives where, what it's for, and what is/isn't part of the distributable project. See `REPOSITORY_SCOPE.md` for the authoritative tracked/excluded list and `CODEX_STRUCTURE_PIPELINE.md` for the current automation program driving most active work.*

## What this project is

Infinite Domain is a NeoForge 1.21.1 Minecraft modpack (CurseForge instance) built around Create-based tech progression, a post-apocalyptic "wasteland" survival arc, a cyberpunk Darknet dimension (Cyberspace mod integration), and a large custom structure/settlement-generation system layered on Lost Cities. The project's own contributions — custom mods, KubeJS content, datapacks, quests, structure corpus, documentation — are original and distributable. Third-party mod jars, base resource packs, and local player/runtime state are deliberately excluded from the repository (see **Distribution policy** below and the project's standing instruction: never modify 3rd-party jars, never redistribute 3rd-party code/content).

## Top-level orientation

| Path | What it is |
|---|---|
| `README.md`, `REPOSITORY_SCOPE.md` | One-line project name + the authoritative statement of what's tracked vs. excluded from the repo. |
| `LICENSE` | MIT license for the project's own contributions. |
| `DARKNET-ASSETS-LICENSE.md` | Separate MIT-style grant specifically inviting the Cyberspace mod's author to reuse the pack's original Darknet content (textures, mechanics, lore). |
| `.gitignore` / `.gitattributes` | Git tracking rules (excludes third-party binaries, local state, build output) and line-ending/binary rules. |
| `CODEX_STRUCTURE_PIPELINE.md` | The master instruction document for the ongoing autonomous "Codex" work program: finishing the structural audit of built-in schematics, then acquiring/refining a licensed structure corpus for settlement generation. |
| `.codex/` | Working state for that pipeline: `structure_pipeline_state.md` (large running log), `structure_pipeline_blocked.md`, `phase13_bombed_data_center_plan.md`, `structure_pipeline_logs/`. Local/gitignored. |
| `minecraftinstance.json` | CurseForge's own instance manifest (mod list, versions) — used to reconstruct the third-party dependency set rather than shipping the jars. |
| `mods/` | All mod jars actually loaded by the instance (third-party + the project's own). |
| `ROOT_tools/` | Java source projects for the project's own mods, plus their Gradle build output. |
| `kubejs/` | KubeJS scripts and the datapack/resourcepack overlay they and hand-authored data live in. |
| `datapacks/`, `packdev/` | World datapack slot (currently unused) and in-development datapacks (custom worldgen). |
| `config/`, `defaultconfigs/` | Per-mod configuration; mostly third-party mod tuning, with one project-owned subtree (`config/createcybernetics/tattoos`). |
| `docs/` | The project's internal design/audit documentation — by far the largest source of "what was decided and why." |
| `scripts/` | Python/JS/PowerShell tooling that generates and audits most of `docs/`, `kubejs/`, and `structure_library/`. |
| `tools/` | One small standalone script (cyberware index builder). |
| `structure_library/` | The structure corpus system: catalogs, provenance, per-structure "programs," review renders — the data backing the Lost Cities structure-replacement effort. |
| `old_world_narrative/` | A queued (not-yet-executed) narrative/quest-structure content package — canon lore bible plus the automation spec to implement it. |
| `saves/`, `logs/`, `backups/`, `crash-reports/`, `screenshots/` | Local runtime state — worlds, logs, backups, crash dumps. Gitignored. |
| `resourcepacks/` | In-progress "Last Days" texture-compatibility pack work (large zips) — excluded pending file-by-file license clearance. |
| `Infinite-Domain/` | A stray **nested full git checkout** of this same repository sitting inside the instance folder. Not project content — safe to delete; `.gitignore` already excludes it. |
| `.cache/`, `.mixin.out/`, `.pg-native/`, `.sable/`, `ldlib2/`, `nodes/`, `moonlight-global-datapacks/`, `dynamic-*-pack-cache/`, `tmp/`, `local/`, `downloads/`, `shaderpacks/`, `build/` | Mod- or launcher-generated runtime/cache directories. Gitignored, safe to regenerate. |

## `mods/` — the loaded mod set

~150 third-party mod jars (Create ecosystem, AE2, FTB suite, Ice and Fire, Cyberspace, Quark, Sophisticated Storage, Lost Cities, KubeJS, etc.) plus exactly **six project-built jars**, each named `infinite-domain-*`:

- `infinite-domain-create-nuclear-balance-1.0.0.jar`
- `infinite-domain-cyberware-mastery-1.0.0.jar`
- `infinite-domain-darknet-worldgen-1.8.0.jar`
- `infinite-domain-echo-economy-1.0.0.jar`
- `infinite-domain-stellaris-industry-1.0.0.jar`
- `infinite-domain-unified-radiation-1.0.0.jar`

Only these six are the project's own compiled output; everything else in `mods/` is reacquired from its original distribution channel per `REPOSITORY_SCOPE.md` and is never modified in place.

## `ROOT_tools/` — source for the six custom mods

One subfolder per custom jar above, each a small standalone Gradle project (`src/main/java|resources`, `build/` with fetched dependency jars and compiled classes):

- `create-nuclear-balance` — rebalances Create: Nuclear reactor output.
- `cyberware-mastery-expansion` — the branching cyberware item/effect system (`BranchedCyberwareItem`, `CyberwareCatalog`) built on Create Cybernetics.
- `darknet-worldgen-patch` — Darknet dimension guard/worldgen/dragon-texture mixins bridging Cyberspace and Ice and Fire.
- `echo-numismatics-bridge` — currency provider bridging FTB Echoes and Create Numismatics.
- `stellaris-space-industry` — space-suit roles/catalog built on the Stellaris mod.
- `unified-radiation` — a unified radiation-reading system spanning The Wasteland Reworked / Wastelands.

Each also carries its own `neoforge.mods.toml`, mixins config, and (for a few) generated assets/data merged into its jar at build time. `.gitignore` currently excludes all of `ROOT_tools/` as a "local authoring/recovery payload," so despite `REPOSITORY_SCOPE.md` describing source projects as tracked, verify this is intentional before assuming these sources are backed up in git.

## `kubejs/` — scripts + hand-authored datapack/resourcepack overlay

- `startup_scripts/` — item/block registration run once at load (era mining tiers, industrial food items, mineral trace items, nuclear fuel cycle items, old-world-narrative items, ruined functional blocks, space industry catalog, vanilla placeholder tools, MOMG tool balance).
- `server_scripts/` — recipe/loot/event logic: admin spawn-claim system, Create Ultimate Factory progression, cyberware conversion, Darknet anchor/session injector, Gateway of Doom dimension lock, era reward bags, industrial food, mineral trace + nuclear fuel cycle + organic metallurgy processing chains, ruined functional block recipes, space industry recipes, spawn-hub hostile protection, spore analysis samples.
- `client_scripts/` — Create ponders for custom machines (contractor, market, P2P) plus cyberware tooltip conversion.
- `data/` — the project's datapack namespace: `data/infinite_domain/` (advancements, echo_definitions, enchantments, functions, loot tables, Lost Cities hooks, recipes, structures, tags, worldgen) and `data/kubejs/`, `data/ftbquests/` for generated loot/recipe glue.
- `assets/infinite_domain/` — matching resource-pack namespace (blockstates, lang, models, textures) for the custom items/blocks above.
- `config/` — KubeJS's own per-script config JSON (industrial_food, mineral_trace_ore_processing, nuclear_fuel_cycle, organic_metallurgy, plus client/common/web_server settings).

This is effectively the "live code" layer of the pack — most gameplay systems described in `docs/` are implemented here.

## `datapacks/` and `packdev/`

- `datapacks/` — the world's datapack slot; currently holds only Fabric's default-resource-pack marker (no custom datapack installed here at the moment — datapack-equivalent content lives in `kubejs/data/` instead).
- `packdev/gradient_ocean_pack/` — an in-development standalone datapack defining custom worldgen density functions (continent masks, gradients, city/humidity/temperature masks) for the pack's ocean/continent shaping, with its own `README.md` and `pack.mcmeta`.

## `config/` and `defaultconfigs/`

`config/` holds ~150 third-party mod config files (`.toml`/`.json`/`.snbt`) tuning everything from Create add-ons to FTB Quests to Quark — standard modpack configuration, not project source. The one project-owned exception is `config/createcybernetics/tattoos/`, custom tattoo definitions for the cyberware system. `defaultconfigs/` mirrors this for fresh-world defaults (`biolith/`, FTB Essentials/Lost Cities server defaults) and is gitignored as local/regenerable state, except `config/jei/world/` which is separately excluded.

## `docs/` — design & audit documentation (largest content area)

Hundreds of markdown/CSV/JSON files recording design decisions and audit evidence. Rough clusters:

- **Darknet / Cyberspace campaign** — `DARKNET_*.md` (anchor, broker, data nodes, ecology, worldgen, draconic convergence), `CYBERSPACE_VIRTUAL_MACHINE_QUEST.md`, `GATEWAY_OF_DOOM_CONFIGURATION.md`, `art-direction/` (reference art + AI-generation prompts for Darknet textures).
- **Cyberware system** — `CURRENT_CYBERWARE_INDEX.md`, `CYBERWARE_CONVERSION_PLAN.md`, `CYBERWARE_FULL_EXPANSION_PLAN.md`, `cyberware-index/`.
- **Structure / building pipeline & QA** — `INBUILT_STRUCTURE_AUDIT.md` + `inbuilt-structure-audit.json`, `DEEP_SEA_STRUCTURE_*`, `structure-geometry-lint-baseline.*`, `structure-placement-contract-validation.json`, `WASTELAND_SETTLEMENT_REPLACEMENT_STATUS.md`, `road-module-*`, `wasteland-site-manifest.json`, family-validation JSON files (habitation, transit, roadside, urban-commercial, rural-processing, utility-technology, extraction) — this cluster is the evidence trail for the work described in `structure_library/`.
- **Era/progression & quests** — `THREE_PATH_ERA_QUEST_BLUEPRINT.md`, `ERA_*` docs, `QUEST_ARCHITECTURE.md`, `MASTERY_QUESTS.md`, `progression-graph/` (large CSV graph of the entire crafting/quest dependency graph).
- **Recipe / material / economy audits** — `compression-audit/`, `recipe-index/`, `recipe-audit/`, `material-catalog/`, `mining-progression/`, `smelting-audit/`, `DELIVERY_REQUIRED_ECONOMY.md`, `ECHO_STORES.md`.
- **Texture / asset audits** — `texture-audit/` (custom item renders + generated-source PNGs), `last-days-*` files (the Last Days compatibility texture-porting effort backing `resourcepacks/`), `CUSTOM_ITEM_TEXTURE_AUDIT.md`.
- **Worldgen / biome** — `biome-gating-audit/`, `NORTHERN_BIOME_RESTORATION.md`, `OCEAN_RESTORATION.md`, `GRADIENT_OCEAN_PACK_VALIDATION.md`, `WORLDGEN_STRUCTURE_SAFETY.md`.
- **Licensing / permissions** — `STRUCTURE_DONOR_LICENSE_RESEARCH.md`, `permissions/` (includes a screenshotted permission grant), `CREATIVELANDS_VISUAL_TRIAGE.md`.
- **Misc systems** — food/industrial (`INDUSTRIAL_FOOD_SYSTEM.md`), space industry (`stellaris-space-industry.md`), radiation (`unified-radiation-audit.md`), wasteland survival docs, registry inventories (full item/block ID dumps in `registry-inventory/`).

Treat `docs/` as the project's decision log and evidence archive rather than code — most files are either a design spec or a generated audit report a script in `scripts/` produced.

## `scripts/` — the automation layer

~150 Python/JS/PowerShell files, one or a few per system in `docs/`. Naming convention is consistent: `audit_*` inspects/reports, `build_*` or `generate_*` creates content, `validate_*` re-checks generated output, `install_*`/`recolor_*` apply generated textures. Notable heavyweights: `generate_wasteland_sites.py` (400KB+, the core wasteland-structure generator), `validate_structure_programs.py`, `structure_geometry_lint.py` + `structure_geometry_primitives_v2.py` (the current authoritative structure QA gate, see below), `build_structure_qa_world.py` (builds the in-game QA flatworld under `saves/`). A few `.java` files (`CyberwareTextureGenerator.java`, `DarknetOverlayTextureGenerator.java`, `DatavoreSkinGenerator.java`, `DragonTextureGenerator.java`) are compiled ad hoc into `tools/*-texture-tool-classes/` for one-off texture generation, not part of any mod build.

The deep-sea structure and geological feature system (see `structure_library/`
below) has its own three-script set, independent of the land-corpus tooling
above: `generate_deep_sea_structures.py` (generator), **`validate_deep_sea_structures.py`
— the deep-sea structure validator** (metadata/schema, source-NBT dimension,
atmosphere-fill, render-color-fidelity, and placement-gate checks), and
`render_deep_sea_review.py` (isometric + floor-slice render evidence).
Governed by `docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md`,
not `STRUCTURE_REBUILD_SYSTEM_V2.md`.

## `tools/`

Just `build_cyberware_system_index.py` — a standalone indexer for the cyberware system, separate from the main `scripts/` tree.

## `structure_library/` — the structure corpus

The authoritative source-of-truth for buildings admitted to the Lost Cities replacement pipeline (see its own `README.md` and `CORPUS_LAYOUT.md`). Lifecycle: `rough_source → clean_master → damage_variant → occupation_variant → approved`; nothing reaches production world-gen without a validated clean master, a rendered review, and human sign-off.

- `STRUCTURE_REBUILD_SYSTEM_V2.md` — current authoritative design doctrine and QA gate (supersedes the older `generated-structure-refinement-policy.json`).
- `catalog.json`, `corpus-manifest.json` — the active corpus index and path map.
- `programs/` — per-structure room/adjacency/circulation programs (required generation input, not just documentation).
- `variants/` — damage/environment/occupation derivation records.
- `modules/`, `infrastructure/` — reusable architectural modules and road/rail/bridge/parking/waterfront catalogs.
- `licensing/` — provenance/redistribution record per retained donor source or master (no uncertain-license asset may enter a production selector).
- `reviews/`, `audit_renders/` — four-view render evidence for clean masters, derivatives, and every inbuilt template.
- `sources/quarantine/`, `extracted/` — pinned intake archives and normalized review-only conversions not referenced by live worldgen.

`structure_library/` also holds a second, independently governed corpus in
the same directory — deep-sea structures and geological features, covering
underwater wrecks, submariner facilities, and terrain features. Its own
files: `deepsea-corpus-manifest.json` (path map, the deep-sea equivalent of
`corpus-manifest.json` above), `deepsea-metadata.schema.json`,
`deepsea-catalog.json`, `deepsea-refinement-policy.json`, and
`audit_renders/deep_sea/` for its render evidence. Governed by
`docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md` and
`docs/DEEP_SEA_STRUCTURE_AUDIT.md` (its disposition ledger), validated by
`scripts/validate_deep_sea_structures.py`. Do not assume `catalog.json` or
`corpus-manifest.json` cover this corpus — they don't; see
`structure_library/CORPUS_LAYOUT.md`'s "Sibling corpus" section.
- `rebuild-family-roadmap.json`, `rebuild-phases.json` — the checkpoint-wave plan `CODEX_STRUCTURE_PIPELINE.md` currently drives against.

## `old_world_narrative/` — queued, not yet executed

A self-contained content package (see its `README_FIRST.md`) meant to run *after* the current structural audit finishes: converts an authoritative "Old World" lore bible into 64 deeply revised narrative structure variants, 8 book series, 96+ short records, 160+ signs, 48+ graffiti strings, structure-proof items, and an Exploration quest spine. `source/` holds the canon bible and phase docs (`01`–`09`); `structures/` and `reviews/old_world/` already contain a first batch of ~10 structure definitions and their render reviews, so this is partially underway despite being formally "queued behind" the structure audit.

## Local / excluded state (not part of the distributable project)

Per `.gitignore` and `REPOSITORY_SCOPE.md`, none of the following are tracked: `.cache/`, `.codex/`, `.mixin.out/`, `.pg-native/`, `.sable/`, `backups/` (FTBBackups2 zips + manual checkpoints), `crash-reports/`, `downloads/`, `dynamic-data-pack-cache/`, `dynamic-resource-pack-cache/`, `ldlib2/`, `local/`, `logs/`, `moonlight-global-datapacks/`, `nodes/`, `saves/` (includes the `Infinite Domain - Structure QA Flatworld` test world used by the structure QA scripts), `screenshots/`, `shaderpacks/`, `tmp/`, `usercache.json`/`usernamecache.json`, `options.txt`, `command_history.txt`, `hs_err_pid*.log`, and generated build dirs (`**/build/`, `**/.gradle/`, `**/bin/`, `**/out/`, `**/__pycache__/`). Also excluded: `resourcepacks/` (large in-progress "Last Days" compatibility pack zips pending file-by-file license clearance) and `Infinite-Domain/` (the stray nested checkout mentioned above).

## Distribution policy reminder

Per project instructions and `REPOSITORY_SCOPE.md`: third-party jars, base resource-pack ZIPs, and any upstream donor/reference payload are never redistributed or modified in place. Only the project's own KubeJS scripts, datapack/resourcepack overlay, docs, structure-library data, quest data, and the six `infinite-domain-*` mod artifacts (plus, if intended, their `ROOT_tools/` sources) are meant to leave this machine.

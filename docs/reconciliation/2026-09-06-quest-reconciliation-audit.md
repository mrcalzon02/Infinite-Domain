# Infinite Domain Quest Reconciliation Audit

Date: 2026-09-06
Branch: `main`
Starting remote head: `31a8d5994aaf7593b2124ae689df54af209a4e89`
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)
AI Project Manager: v3.0 loaded with repository execution and Minecraft Java profiles.

## Scope

This record captures current-source findings for the developed FTB Quests corpus. It does not promote conversation-only assumptions or historical audit results into current repository truth. Static findings are separated from runtime validation.

The deterministic validators restored at the starting head are:

- `dev/audit_quest_tree_coherence.py`
- `dev/audit_ftbquests.js`
- `dev/quest_explorer_map_standard.js`

A fresh whole-corpus validator execution remains deferred in this environment because the execution container cannot currently resolve `github.com`, preventing materialization of current `main` into an executable worktree. The GitHub repository connector remains available for authoritative source reads and writes.

## 1. Parallel Factory Paths — revision required

Authoritative source: `config/ftbquests/quests/chapters/parallel_factory_paths.snbt`.

The earlier era-reward corrections remain present. The remaining defect is heavy-industry authentication and ordering:

- quest `5D30000000000011` is currently `Chemical-Industrial Integration` with only a checkmark task;
- quest `5D30000000000012` is currently `Electrical-Mechanical Integration` with only a checkmark task;
- historical/current localization authority identifies those IDs as the Excavator and Arc Furnace commissioning positions;
- `5D30000000000015` (`Integrated Factory Commissioning`) is also only a checkmark;
- `5D30000000000016` (`Dual-Path Production Proof`) authenticates only a Create Mechanical Press, IE Voltmeter, and eight IE Fluid Pipes.

This does not prove construction or operation of the Excavator or Arc Furnace before the chapter declares integrated factory capability.

Required root repair: restore Excavator and Arc Furnace commissioning semantics on the existing quest IDs rather than creating duplicate parallel quests. Use deterministic component/operation authentication supported by the pack, then make final commissioning/proof inherit those completed heavy-industry stages.

Status: **REVISION REQUIRED — source-level deterministic defect confirmed.**

## 2. The Rot / Spore Threat Dossier — revision required

Authoritative source: `config/ftbquests/quests/chapters/the_rot_spore_threat_dossier.snbt`.

The dossier is intentionally era-independent, but six current sample milestones directly distribute technology owned by separate AE2 and Create Cybernetics progression trees:

| Quest | AE2 reward | Cybernetics reward |
|---|---|---|
| `5F10000000000007` | `ae2:charger` | `createcybernetics:eyeupgrades_biomonitor` |
| `5F1000000000000F` | `ae2:item_storage_cell_1k` | `createcybernetics:eyeupgrades_targeting` |
| `5F10000000000015` | `ae2:item_storage_cell_4k` | `createcybernetics:muscleupgrades_wiredreflexes` |
| `5F1000000000001B` | `ae2:wireless_terminal` | `createcybernetics:brainupgrades_neuralprocessor` |
| `5F10000000000024` | `ae2:dense_energy_cell` | `createcybernetics:organsupgrade_densebattery` |
| `5F10000000000026` | `ae2:wireless_crafting_terminal` | `createcybernetics:brainupgrades_iceprotocol` |

These rewards create possession-level capability bypasses without requiring the corresponding civilization/technology-tree authority.

Required root repair: preserve Rot as an era-independent threat/research path, remove the six cross-tree hardware reward pairs, and replace them with Rot-specific research/evidence rewards, consumables, Numismatics compensation, or other era-neutral rewards. Synchronize localization so quest text no longer promises removed advanced hardware.

Status: **REVISION REQUIRED — six current capability leaks confirmed.**

## 3. Air/Sea and Abyssal Recovery

The era-boundary repairs already committed before this audit remain the controlling baseline:

- Abyssal Recovery entrance requires Era 4 authority.
- Air/Sea early reward tiers and the advanced exploration Era-4 handoff were corrected.

Remaining non-era reconciliation still includes presentation/icon normalization and the executable-versus-described ship-discovery criterion where the quest description claims any registered Seven Seas ship while implementation has historically required the Unicorn Galleon specifically.

Status: **ERA BOUNDARY REPAIRED / PRESENTATION AND TASK-SEMANTIC REVIEW OPEN.**

## 4. Old World Investigation

The investigation remains intentionally era-independent. The prior direct Precision Mechanism and Era-3 cache/bag leaks were corrected before this audit.

Status: **ERA CAPABILITY LEAK REPAIR PRESENT; global validator rerun still required.**

## 5. Validator reorganization regression — revision required

The deterministic coherence validator was restored after the repository's development-only reorganization, but its auxiliary-data paths were restored in their pre-reorganization form.

Current `dev/audit_quest_tree_coherence.py` resolves these inputs under root-level `docs/`:

- `docs/registry-inventory/item-ids.txt`
- `docs/registry-inventory/entity-ids.txt`
- `docs/registry-inventory/mod-jar-index.json`
- `docs/progression-graph/graph-nodes.csv`
- `docs/recipe-index/recipe-outputs.csv`

Those root paths no longer exist. Commit `1b252ded681b64bf3c67fe07c50b073bf081b18b` (`chore: isolate development-only files under dev`) moved the authoritative datasets under:

- `dev/docs/registry-inventory/`
- `dev/docs/progression-graph/`
- `dev/docs/recipe-index/`

All required current inputs are present at those `dev/docs` locations. The coherence validator's loaders return empty sets when these files are missing, so running the restored script without correcting the paths can suppress registry/producibility checks and produce a misleadingly incomplete audit rather than a hard failure.

`dev/audit_ftbquests.js` has a related output-path reorganization issue: it still writes its generated icon-review report to root `docs/custom-content-audit/`, despite development audit products having been isolated under `dev/docs/`.

Required root repair: update the restored validators themselves to resolve development audit inputs and outputs from `dev/docs`, preserving their deterministic logic and failing explicitly when required oracle inputs are unavailable. Do not copy the moved oracle datasets back into root `docs` and do not add compatibility shims.

Status: **REVISION REQUIRED — deterministic validator authority is not currently trustworthy until path reconciliation is completed.**

## 6. Whole-corpus validation gate

Before procedural quest expansion is admitted, current `main` must receive a fresh execution of the repaired validators and every deterministic critical/warning finding must be dispositioned without weakening the validators.

Required sequence:

1. repair the validator paths to the authoritative `dev/docs` oracle locations and make required-oracle absence fail loudly;
2. materialize authoritative current `main` into an executable worktree;
3. run `dev/audit_quest_tree_coherence.py`;
4. run `dev/audit_ftbquests.js`;
5. inspect generated reports and exact findings;
6. repair authoritative quest/localization sources target-by-target;
7. rerun until the relevant deterministic findings are clean;
8. keep runtime-only claims deferred until a real pack runtime is exercised.

## 7. Procedural expansion candidates — not yet admitted

The following are candidates for depth-of-field after the existing corpus clears reconciliation:

- explicit IE Excavator construction, formation, power, and operation proof;
- explicit IE Arc Furnace construction, electrode/energy/feedstock, and operation proof;
- production-chain proofs that require actual intermediate outputs rather than possession of generic tools;
- era-appropriate cross-tree integration milestones that prove two systems working together without granting technology from one tree through another;
- Rot research/evidence progression that converts escalating biological samples into knowledge, countermeasure, and containment depth rather than unrelated advanced hardware;
- consistent chapter/quest icon coverage and executable objective wording across specialist and exploration chapters;
- Domain Compendium/global namespace validation for quest IDs, task IDs, reward IDs, dependencies, localization, and item/entity references.

Status: **CANDIDATE ONLY — expansion admission remains blocked on reconciliation.**

## Exact next action

Repair the stale development-audit paths in the validator authorities, then obtain an executable current-main worktree through the first available authorized repository path and run both validators. Repair Parallel Factory, Rot, and every additional current-corpus finding produced by that clean validation pass before beginning procedural expansion.
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

## 8. Applied Energistics Recovery — source-level era ordering cleared

Authoritative source: `config/ftbquests/quests/chapters/applied_energistics_recovery.snbt`.

A fresh current-source pass confirms the AE2 progression inserts explicit civilization authorities at the intended capability boundaries rather than relying on reward possession:

- storage-network entry waits on Era 3 authority `5310000000000001` before `ae2:chest` and the subsequent 1K storage-cell objective;
- 4K fluid storage waits on Era 4 authority `5410000000000001`;
- powered-network progression waits on Era 5 authority `5510000000000001` before the Energy Acceptor stage;
- controller progression waits on Era 6 authority `5610000000000001`;
- quantum-link progression waits on Era 7 authority `5710000000000001`;
- the infinite-storage endpoint additionally waits on Era 8 authority `5810000000000002`.

Every inspected quest in the chapter carries an explicit icon. The current source therefore does not reproduce the Rot dossier's possession-level AE2 bypass pattern.

Status: **SOURCE-LEVEL ERA ORDERING CLEARED — localization/global-ID/runtime validation still subject to the whole-corpus gate.**

## 9. Another Lost Soul — source-level presentation/reward pass cleared

Authoritative source: `config/ftbquests/quests/chapters/another_lost_soul.snbt`.

A fresh current-source inspection found explicit icons on the chapter and every implemented quest. Rewards remain low-impact survival/economy or terminal-guide items (`supplementaries:sack`, Wastelands food/water, apples, and the FTB Quests task-screen configurator) rather than civilization-era technology or forward-tier reward bags. The chapter's many checkmark tasks are concentrated in narrative/guide branches and do not presently expose a direct era-capability bypass in source.

Status: **SOURCE-LEVEL ICON/REWARD PASS CLEARED — localization semantics, global IDs, and runtime behavior still subject to the whole-corpus gate.**

## 10. Food-economy specialist chapters — era ordering cleared

Authoritative sources: `config/ftbquests/quests/chapters/coffee_tea_economy.snbt`, `config/ftbquests/quests/chapters/brewery_and_winery.snbt`, `config/ftbquests/quests/chapters/era_01_mechanical_reconstruction.snbt`, and `config/ftbquests/quests/lang/en_us.snbt`.

The shared dependency `4FC0C1C678C71891` has now been traced to `The Mechanical Foundation`, the Era-1 capstone. It requires one completed professional charter, proves sustained mechanical/provision/recovery capability, and explicitly opens Era 2. Both food-economy chapters therefore begin only after the player has already completed Era-1 foundation authority.

Coffee/Tea and Brewery/Winery each have explicit chapter and quest icons in current source. Their Era-1 supply bags and priority caches are retrospective optional side-branch rewards after the Era-1 capstone, not forward-tier capability leaks. Brewery localization explicitly states that the optional line begins after the Mechanical Foundation and never gates an era.

Status: **SOURCE-LEVEL ERA/REWARD/ICON ORDERING CLEARED — global-ID/localization/runtime validation still subject to the whole-corpus gate.**

## 11. Create Big Cannons Doctrine — source-level era ordering cleared

Authoritative source: `config/ftbquests/quests/chapters/create_big_cannons_doctrine.snbt`.

The artillery line begins behind Era 4 authority `5410000000000001`. It then progresses through foundry establishment, barrel machining, first cannon assembly, inspection, breech/loading/mounting, ammunition production, misfire procedure, and firing drill. Automation-heavy traverse/elevation and autocannon stages additionally wait on Era 5 authority `5510000000000001`.

Current rewards in the inspected chapter are Numismatics compensation rather than era bags or granted artillery technology. The chapter and quests carry explicit icons and explicit titles. No source-level forward-era reward leak or ordering inversion was found in this pass.

Status: **SOURCE-LEVEL ERA/REWARD/ICON ORDERING CLEARED — global-ID/localization/runtime validation still subject to the whole-corpus gate.**

## 12. Powered Field Engineering — source-level era ordering cleared

Authoritative source: `config/ftbquests/quests/chapters/powered_field_engineering.snbt`.

The chapter begins behind Era 5 authority `5510000000000001` before commissioning powered Mining Gadgets, Building Gadgets, charging infrastructure, and their ordinary upgrade branches. Extended mining range/size and advanced cut-paste construction additionally wait on Era 6 authority `5610000000000001`.

The visible full progression uses explicit names and icons. Rewards are Numismatics compensation rather than era bags or granted higher-tier hardware. The two main branches converge only after their advanced objectives, so no source-level capability-order inversion was found.

Status: **SOURCE-LEVEL ERA/REWARD/ICON ORDERING CLEARED — global-ID/localization/runtime validation still subject to the whole-corpus gate.**

## 13. Create Specialist Workshops — source-level authority and localization pass substantially cleared

Authoritative sources: `config/ftbquests/quests/chapters/create_specialist_workshops.snbt` and `config/ftbquests/quests/lang/en_us.snbt`.

The specialist chapter starts after `The Mechanical Foundation` (`4FC0C1C678C71891`). Visible branches then add civilization authority before their corresponding capability families: Era 2 `5210000000000001` for Cardan/linear-bearing and automated-walkway work; Era 3 `5310000000000001` for station-platform, compact-gearbox, and delivery-contractor work; and Era 5 `5510000000000001` for high-end P2P delivery and hypertube systems.

Visible rewards are Numismatics compensation rather than technology grants or forward-tier era bags. Every visible quest carries an explicit icon. Although the chapter SNBT intentionally omits inline names, localization supplies the chapter title, quest titles, detailed objectives, and rationale. Localization also establishes that its manual acceptance checkmarks represent witnessed operating procedures and give no material reward, so their existence alone is not a progression bypass.

The source response available in this environment truncates the late tail of this chapter, so this is not yet a full chapter admission claim.

Status: **PARTIAL SOURCE-LEVEL CLEAR — visible era/reward/icon/name semantics are coherent; late-tail/global-ID/runtime validation remains open.**

## 14. Environmental Survival Engineering — audit in progress

Authoritative source: `config/ftbquests/quests/chapters/environmental_survival_engineering.snbt`.

Current source shows explicit chapter/quest icons and a staged environmental-protection progression. Early gas-mask/filter work precedes higher-authority branches; hard-hat/PDA and improved mask work reference `5210000000000002`; ventilation pipe work references `5310000000000002`; ventilation intake references `5410000000000002`. The visible reward sequence includes an Era-2 supply bag after the `521...0002` boundary, an Era-3 supply bag downstream of the `541...0002` boundary, and an Era-0 cache on the early radiation branch.

Those numbered authorities use the `...0002` family rather than the already-traced primary era-entry IDs, so they must be traced before classifying the rewards. A lower-numbered bag behind a later authority is not a forward-tier leak by itself. The available source response also truncates the later radiation/environment tail, so no mutation or full-clear claim is justified yet.

Status: **OPEN — trace the `521/531/541...0002` authorities and finish the late-tail reward/dependency audit before disposition.**

## Exact next action

Continue the current-source chapter sweep by resolving Environmental Survival Engineering's `...0002` authority family and completing the late tail, then finish the remaining Create Specialist Workshops tail and proceed through the next undeveloped specialist chapters. In parallel, repair the stale development-audit paths in the validator authorities when a safe complete-file editing path is available; then obtain an executable current-main worktree through the first authorized functioning repository path and run both validators. Repair Parallel Factory, Rot, Air/Sea's remaining semantic/presentation defect, and every additional current-corpus finding produced by that clean validation pass before beginning procedural expansion.

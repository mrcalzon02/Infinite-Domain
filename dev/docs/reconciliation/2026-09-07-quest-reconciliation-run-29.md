# Infinite Domain Quest Reconciliation — Run 29

## Authority

- Authoritative repository: `mrcalzon02/Infinite-Domain`
- Authoritative branch: `main`
- Starting head verified at `59b0b7503cd889446279fc33ef99e69a95629236`.
- Working method remains evidence-gated DEEFM against authoritative `main`; no alternate branch and no GitHub Actions.

## Abyssal Recovery — source and localization audit

`config/ftbquests/quests/chapters/abyssal_recovery.snbt` was read end to end in bounded source ranges and compared with the active FTB Quests localization and the active KubeJS evidence-item registry.

### What is coherent

The chapter has an explicit `minecraft:heart_of_the_sea` chapter icon and every quest carries an explicit icon. The opening bilateral recovery sequence is mechanically strong: both western and eastern branches require Era-4 authority `5410000000000001` plus the external submarine-capability predecessor `5E00000000000006`, then use biome discovery -> structure entry -> physical evidence return to the settlement safe zone. The Pelagos branch requires `kubejs:abyssal_navigation_core`; the Karsic branch requires `kubejs:karsic_subsea_data_recorder`. Those are the only two abyssal recovery evidence items currently registered by `kubejs/startup_scripts/abyssal_recovery_items.js`.

The two branches join at `5AB0550C00000007`, which requires both surviving evidence items, then split into deeper Pelagos and Karsic abyssal routes. Deeper nodes continue to require the intended biome and/or mapped structure and do not grant forward-era machinery. Rewards remain bounded to Numismatics currency and Era-4 support bags/caches. No direct later-era technology reward was found.

Quest IDs, task IDs and reward IDs inspected within the chapter are internally unique, and all source dependencies point backward within their branch or to the two external prerequisite authorities above.

### Confirmed localization/logic mismatch

The live KubeJS registry explicitly states that the obsolete seven-item deep-research evidence registry was removed and that only `abyssal_navigation_core` and `karsic_subsea_data_recorder` remain active.

However, localization for quests `5AB0550C00000009` through `5AB0550C00000010` still describes physical recovery of removed evidence artifacts including a Pelagos Bathymetric Survey Log, Fracture Sensor Core, Hadal Pressure Record, Karsic Telemetry Package, Karsic Sonar Archive, Blacksite Cipher, and a final Comparative Abyssal Dossier. The executable SNBT no longer requires those items; it authenticates the deeper chain through biome and structure tasks instead.

This is a real player-facing correctness defect: the quest text promises and instructs recovery of artifacts that the active registry intentionally no longer provides. The executable progression is presently completable, but the instructions and implementation disagree.

### Repair disposition

Do **not** restore the removed deep-research item registry merely to satisfy stale text. The authoritative startup script documents their removal as intentional. Correct repair is to reconcile the Abyssal localization with the current biome/structure-authenticated implementation, unless a future design decision explicitly restores a complete evidence-loot pipeline together with registered items and guaranteed structure loot.

The active `en_us.snbt` localization authority is approximately 398 KB and the connected GitHub write surface replaces entire files. It cannot be safely reconstructed from truncated responses in this environment, so no destructive whole-file localization rewrite was attempted. The defect is now explicitly promoted into the active repair ledger rather than being silently treated as clean.

Source-level disposition: **era ordering, dependency shape, reward staging and icon coverage cleared; localization/executable-logic coherence remains open.** Final registry/structure/duplicate-ID validation remains required with the whole corpus.

## Procedural expansion candidates captured

1. If the deeper evidence concept is restored, implement it completely: register each artifact, put it in guaranteed structure evidence loot, require the item in the matching quest, and return it to the settlement or analysis node.
2. Otherwise keep the simplified structure-authenticated route and rewrite the stale descriptions around survey, entry, inspection and comparative mapping rather than nonexistent item recovery.
3. Add submarine operational commissioning before the first slope expedition if a stable vehicle/event hook exists, so possession of a pressure-capable craft is distinguished from successful deep-water operation.
4. Preserve the bilateral Pelagos/Karsic branch symmetry and final comparison node; it is a strong template for later exploration content.
5. Add optional deep-ocean logistics proofs around resupply, pressure-safe staging and recovery-to-safe-zone rather than raw collection volume.

## Updated active repair ledger

1. Rot reward ownership/bypass classification and repair.
2. Era-7 AE2/Create Cybernetics reward-ownership classification.
3. Parallel Factory Excavator and Arc Furnace commissioning semantics.
4. Air/Sea Nether-structure target and infrastructure authentication/presentation cleanup.
5. Abyssal Recovery localization/executable-logic mismatch for removed deep-research evidence items — source ordering/rewards/icons otherwise cleared.
6. Mutant/Mekanite chapter and quest icon/shape normalization — era ordering cleared; safe write path still required.
7. Darknet icon/shape normalization.
8. Old World presentation/era-authority closure.
9. Mekanism Factory family chapter icons.
10. Graveyard/Gateway predecessor provenance and optional operational-authentication upgrades.
11. Scavenging/Defense/Containment chapter and quest icon normalization.
12. Environmental Survival external predecessor provenance plus final recipe/registry validation.
13. Grid Storage and Recovery final registry/recipe validation.
14. Powered Field Engineering final registry/recipe validation.
15. Civilization Mastery final deterministic registry/ID validation; Era-0 bypass already repaired.
16. Undead Settlement Automation final deterministic registry/localization/duplicate-ID validation; source-level ordering/rewards/icons cleared.
17. Deterministic whole-corpus validation including Domain Compendium, duplicate IDs, localization, registry/structure IDs, dependency order, reward-era leakage, and icon/name coverage.

Procedural expansion remains behind correctness closure except for candidate identification and design capture.

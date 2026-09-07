# Infinite Domain Quest Reconciliation — Run 45

## Scope

Continuation from verified authoritative `main` head `06d269ff381ae7969dd6916f1d7e16cdcbc51ddb`, followed by the applied Undead Settlement correction at `235d03726e3cc635dfb43707076dab3a609c553e`.

Audit focus for this run:

- apply and verify the bounded Undead Settlement Era-7 reward correction;
- audit `abyssal_recovery.snbt` through complete current source;
- resolve Abyssal Recovery's external opening predecessor against Air/Sea;
- inspect `air_sea_global_logistics.snbt` for remaining era-order/reward defects;
- carry forward unresolved Rot and localization defects without unsafe reconstruction.

Correctness-first remains authoritative: executable era/progression defects precede presentation normalization and procedural expansion.

## Applied repair — Undead Settlement Automation

Source: `config/ftbquests/quests/chapters/undead_settlement_automation.snbt`

Quest `5D1000000000000F` is downstream of Soul Gate quest `5D1000000000000E`, which explicitly requires Era-7 authority `5710000000000001`.

The stale reward `6AA70A9820BAEF0C` has been corrected from:

- `kubejs:era6_priority_cache`

to:

- `kubejs:era7_priority_cache`

Quest IDs, task IDs, dependencies, positions, icons, and all other rewards were preserved. Live `main` read-back confirmed the corrected item ID after mutation.

Applied commit: `235d03726e3cc635dfb43707076dab3a609c553e` — `Correct Undead Settlement Era 7 cache reward`.

Disposition: **repaired and verified**.

## Abyssal Recovery

Source: `config/ftbquests/quests/chapters/abyssal_recovery.snbt`

Disposition: **source-level progression clean; procedural-authentication expansion candidate**.

Findings:

- Complete current source was inspected rather than a truncated excerpt.
- Chapter has an explicit top-level icon and explicit quest icons throughout.
- Shared English localization contains Abyssal quest entries, closing the missing-name concern for the inspected quest IDs.
- Internal dependencies are backward-only and form a coherent recovery sequence across shipwreck, submarine, seafloor-city, laboratory, submerged-factory, facility, and drowned-city investigation targets.
- Opening predecessor `5E00000000000006` resolves to the Air/Sea Global Logistics submarine-development branch; it is not dangling.
- Later Abyssal progression adds Era-4 authority `5410000000000001` before the higher-capability salvage/investigation section.
- Rewards observed are Numismatics Cogs, Era-4 support provisioning, and explorer-map commands that point toward subsequent recovery sites.
- No AE2, Create Cybernetics, or other unrelated specialist technology is granted as an alternate acquisition path.
- No forward-era reward leak was found in the chapter.

Current Abyssal site/evidence grammar is structurally suitable for expansion: expedition capability -> site location -> deterministic evidence recovery -> analysis/interpretation -> next-site lead.

Procedural-authentication candidates:

- require an operational pressure/oxygen-ready dive package before deep-site work;
- authenticate successful descent and return rather than inventory possession alone;
- require deterministic black-box/data-recorder/navigation-core recovery from the intended site;
- require safe-zone analysis/decode handoff before issuing the next explorer lead;
- add salvage-capacity and decompression/return-readiness checks for deeper locations;
- distinguish discovery, evidence recovery, and institutional inference as separate quest proof stages where appropriate.

## Air/Sea Global Logistics — new executable mismatch

Source: `config/ftbquests/quests/chapters/air_sea_global_logistics.snbt`

The chapter remains under active audit and is **not** certified clean.

Confirmed new mismatch:

- Quest `5E0000000000000D` depends on `5E0000000000000C` and explicit Era-8 authority `5810000000000001`.
- The quest authenticates entry into `stellaris:moon` and awards an explorer map for `stellaris:moon_space_base`.
- Reward `6A460F799FEAFC49` still grants `kubejs:era4_supply_bag`.

This is not a forward-progression bypass, but it is a clear era-provisioning mismatch: an explicitly Era-8-gated orbital milestone is paying an Era-4 supply package.

Bounded corrective requirement:

- replace only reward `6A460F799FEAFC49` item `kubejs:era4_supply_bag` with `kubejs:era8_supply_bag`;
- preserve the Moon dimension task, explorer-map reward, quest ID, dependencies, coordinates, and all unrelated content.

The available connector presents the ~12.5 KB chapter as truncated text through the safe file-fetch path. Because mutation is whole-file replacement, this correction is recorded but **not falsely claimed as applied** until complete authoritative text is available for lossless replacement and read-back.

Previously identified Air/Sea issue still remains:

- player-facing Stronghold language is stale relative to the executable `infinite_domain:nether/lyran_research` implementation and must be normalized to Lyran Research Facility terminology.

Air/Sea procedural-authentication candidates now include:

- actual submarine pressure/ballast/propulsion operation;
- successful airship assembly, station registration, transponder identification, and route completion;
- radar acquisition/use rather than dish possession alone;
- Moon launch/arrival/return-trip proof;
- EVA/oxygen readiness before lunar structure investigation;
- logistics manifests proving cargo movement between transport modes rather than component stockpiles.

## Rot carry-forward

`the_rot_spore_threat_dossier.snbt` remains the highest-severity unresolved progression repair. Six previously bounded milestones still operate as an ungated alternate acquisition path for AE2/Create Cybernetics equipment. No unsafe whole-file reconstruction was attempted in this run.

## Correctness queue after Run 45

1. Remove the six bounded Rot AE2/Create Cybernetics reward pairs while preserving Rot-native rewards and progression.
2. Correct Air/Sea Moon quest `5E0000000000000D` reward `6A460F799FEAFC49` from `era4_supply_bag` to `era8_supply_bag` through a source-safe complete-file path.
3. Repair Air/Sea Stronghold -> Lyran Research localization drift.
4. Repair Scavenging biome localization IDs `5D00000000000011` through `...16`.
5. Strengthen Parallel Factory commissioning proof.
6. Strengthen Air/Sea operational commissioning proof.
7. Normalize remaining presentation metadata in Rot, Scavenging, Mutant/Mekanite, Old World, Darknet, Undead Settlement, and other chapters still using generic/missing metadata.
8. Finish remaining external-ID, item-registry, advancement, and structure-target provenance closure.
9. Run deterministic whole-corpus validation, explicitly including shared localization and the very large `domain_compendium.snbt` corpus.

## Procedural depth status

Abyssal Recovery adds a strong reusable investigation grammar: **capability preparation -> expedition -> site authentication -> deterministic evidence recovery -> safe analysis -> inference -> next-site lead**. Air/Sea should use the same philosophy for transport: prove operational movement, registration, navigation, cargo transfer, and return capability rather than merely requiring stacks of transport components.

These expansion candidates remain behind unresolved correctness repairs and corpus validation.

## Authority note

The exact persistent `AI Project Manager.md` did not surface from the available Library lookup in this run. No similarly named document or prior summary was substituted and falsely treated as the authoritative file.
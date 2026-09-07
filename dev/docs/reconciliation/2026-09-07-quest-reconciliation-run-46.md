# Infinite Domain Quest Reconciliation — Run 46

## Scope

Continuation from verified authoritative `main` head `3b09ac711b6b6e951409edb874d08d0e055c826a`.

Audit focus for this run:

- confirm the authoritative repository and current head before mutation;
- re-open the Air/Sea executable mismatch from Run 45 and verify that complete blob retrieval is now available;
- audit `create_big_cannons_doctrine.snbt`;
- audit `create_specialist_workshops.snbt`;
- inspect `early_livestock_exchange.snbt` and bound its remaining predecessor-provenance question;
- extend procedural-authentication candidates without allowing expansion work to outrun correctness.

Correctness-first remains authoritative.

## Air/Sea source-read boundary

Source: `config/ftbquests/quests/chapters/air_sea_global_logistics.snbt`

The Run-45 mismatch remains physically present:

- quest `5E0000000000000D` depends on `5E0000000000000C` and Era-8 authority `5810000000000001`;
- it authenticates entry into `stellaris:moon` and issues the Moon Space Base explorer-map command;
- reward `6A460F799FEAFC49` still grants `kubejs:era4_supply_bag`.

The important tooling boundary changed in this run: direct blob retrieval returned the complete authoritative source rather than a truncated excerpt. This removes the prior read-side blocker to a lossless whole-file replacement. No mutation was attempted in this run because the correction still requires exact complete-source preservation and read-back verification.

Required repair remains exactly one item-ID substitution:

- `kubejs:era4_supply_bag` -> `kubejs:era8_supply_bag` for reward `6A460F799FEAFC49` only.

The stale player-facing Stronghold wording for the now-executable `infinite_domain:nether/lyran_research` path remains separately unresolved in shared localization.

## Create Big Cannons Doctrine

Source: `config/ftbquests/quests/chapters/create_big_cannons_doctrine.snbt`

Disposition: **source-level era/reward clean; procedural-authentication expansion candidate**.

Findings:

- chapter has an explicit title and chapter icon;
- every quest has an explicit title and icon;
- opening quest is gated by Era-4 authority `5410000000000001` before the cannon foundry is established;
- the later automated traverse/elevation and autocannon branches add Era-5 authority `5510000000000001` before those capabilities;
- internal dependencies are backward-only and form a coherent foundry -> machining -> cannon assembly -> loading/mounting -> ammunition -> firing -> automation/advanced-ammunition/autocannon -> battery-commissioning topology;
- rewards are Numismatics Cogs only; no AE2, cyberware, later-era cache, weapon component, or unrelated specialist technology is granted as a bypass;
- no mismatched era cache or forward technology reward was found.

Authentication weakness:

- `6F10000000000004` — `Inspect the Gun Assembly` is a checkmark;
- `6F1000000000000A` — `Establish Misfire Procedure` is a checkmark;
- `6F1000000000000B` — `Prove the Firing Drill` is a checkmark;
- terminal `6F1000000000000F` — `Artillery Battery Commissioned` is also a checkmark.

These are not ordering defects, but they are weak commissioning proofs. Future depth should authenticate actual artillery operation rather than player acknowledgement.

Procedural candidates:

- require a completed cannon assembly that passes an inspection interaction or dedicated advancement;
- prove one successful load/ram/breech-close/fire cycle;
- prove a controlled misfire-clearance or safe unload procedure if the mod exposes a reliable event;
- require successful traverse/elevation operation on a mounted cannon;
- require one fuzed round and one autocannon burst to be fired successfully;
- make final battery commissioning depend on successful operation rather than another checkmark.

## Create Specialist Workshops

Source: `config/ftbquests/quests/chapters/create_specialist_workshops.snbt`

Disposition: **source-level era/reward clean; presentation/localization verification and operational-proof expansion remain**.

Findings:

- chapter has an explicit icon but no inline chapter title/name field;
- quests have explicit icons but no inline title/name fields, so player-facing naming depends on shared localization and should remain in the localization-verification corpus;
- opening workshop quest depends on `4FC0C1C678C71891`, the already-resolved Mechanical Foundation/Era-1 settlement-capability milestone;
- Cardan/linear-bearing and escalator branches add Era-2 authority `5210000000000001`;
- rail/platform, compact-gearbox, and delivery-contract branches add Era-3 authority `5310000000000001` where appropriate;
- P2P delivery and hypertube branches add Era-5 authority `5510000000000001` before those capabilities;
- rewards observed are Numismatics Cogs only;
- no cross-era specialist-technology reward or stale era cache was found;
- internal dependencies are backward-only across the inspected full chapter.

Authentication weakness:

Several branch-final milestones remain checkmarks rather than operational proofs, including chimney operation, linear-bearing operation, public-address/signal operation, compact-gearbox operation, delivery-contract execution, P2P operation, and hypertube operation. The Escalated branch is stronger because it uses concrete advancements for walkway and long-escalator operation.

Procedural candidates:

- chimney: prove active exhaust/smoke handling rather than block possession;
- linear bearing: prove a completed translated-motion cycle and torsional-anchor use;
- station/public-address: prove one announcement or signal-mediated train operation;
- compact gearbox: prove controller-driven ratio/sequence change;
- delivery required: complete one real contractor delivery and one P2P transfer;
- hypertube: complete an entrance -> accelerated tube -> junction transit and detector-trigger event.

## Early Livestock Exchange — bounded follow-up

Source: `config/ftbquests/quests/chapters/early_livestock_exchange.snbt`

The chapter itself is structurally consistent:

- explicit chapter name/icon;
- explicit quest names/icons;
- all six exchanges are repeatable currency-for-spawn-egg trades;
- each task consumes the required Numismatics denomination;
- no internal dependency mismatch exists because every exchange shares the same external predecessor `3AFBE38263D3351E`.

However, this chapter is **not yet certified for era correctness** until `3AFBE38263D3351E` is resolved against its authoritative source. The relevant question is whether livestock access is intentionally available at the planned early settlement/economy stage or accidentally floats behind an unrelated predecessor.

Potential depth candidates after provenance closure:

- first successful breeding pair for each livestock family;
- sustainable feed production before repeated livestock scaling;
- settlement herd-capacity or pen-readiness milestones;
- optional animal-product economy branches rather than simply buying additional spawn eggs.

## Correctness queue after Run 46

1. Remove the six bounded Rot AE2/Create Cybernetics reward pairs while preserving Rot-native rewards and progression.
2. Apply the Air/Sea Moon reward correction now that complete blob retrieval is available, then read back the exact quest block.
3. Repair Air/Sea Stronghold -> Lyran Research shared localization.
4. Repair Scavenging biome localization IDs `5D00000000000011` through `...16`.
5. Resolve Early Livestock predecessor `3AFBE38263D3351E` and classify its era availability.
6. Strengthen Parallel Factory commissioning proof.
7. Strengthen Air/Sea operational commissioning proof.
8. Verify shared-localization naming for chapters whose executable source intentionally omits inline title/name metadata, including Create Specialist Workshops.
9. Normalize remaining presentation metadata in Rot, Scavenging, Mutant/Mekanite, Old World, Darknet, Undead Settlement, and other generic/missing-metadata chapters.
10. Finish remaining external-ID, item-registry, advancement, and structure-target provenance closure.
11. Run deterministic whole-corpus validation, explicitly including shared localization and `domain_compendium.snbt`.

## Procedural expansion direction

Two reusable commissioning grammars are now reinforced:

- **manufacturing doctrine:** establish tooling -> manufacture components -> assemble system -> operate system -> demonstrate safe failure/recovery -> certify line/battery;
- **specialist infrastructure:** acquire hardware -> install network/system -> execute one real service cycle -> prove control/monitoring -> certify sustained operation.

These are better expansion primitives than increasing raw inventory counts. Expansion remains subordinate to unresolved correctness work.

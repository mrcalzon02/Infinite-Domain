# Quest Reconciliation Run 32

## Authority and live state

- Repository: `mrcalzon02/Infinite-Domain`
- Branch: `main`
- Starting HEAD verified from remote commit history: `dfa8f0809e51c4dd8b1dda8a2deec63dfd922029` (`Record quest reconciliation run 31`).
- Working method remains evidence-gated DEEFM against authoritative `main`; no alternate branch and no GitHub Actions.
- The exact persistent `AI Project Manager.md` still did not surface through Library retrieval in this run. No similarly named document was substituted as authority; standing project-manager/DEEFM rules remained in force.

## New confirmed correctness defect — Era 2 Heavy Industry cyberware bypass

The Era 2 Heavy Industry source contains quest `2210000000000007`, reached through the Era-2 farming branch after the wheat / harvester / log / millstone / bread / purified-water sequence. Completing its 32-hay-block objective directly rewards `createcybernetics:eyeupgrades_biomonitor`.

The authoritative Cyberware Ascension tree does not permit the Biomonitor milestone until quest `5B00000000000008`, which explicitly depends on both the preceding iron-plated-arm cyberware milestone and Era-4 authority `5410000000000001`.

Therefore the Era-2 reward is a genuine forward-technology bypass: the Heavy Industry branch can hand the player an augmentation that the dedicated cyberware progression deliberately gates behind Era 4.

**Required repair:** remove reward block `2270000000000007` from Era-2 quest `2210000000000007` while preserving the hay-block task, dependencies, quest ID, shape and coordinates. Do not replace it with another technology item; currency or an Era-2 support/cache reward would be acceptable only if reward-density review shows one is needed.

The current connected GitHub write primitive replaces the entire ~14 KB SNBT file and the fetched file body is tool-truncated. A whole-file reconstruction would risk unrelated quest loss, so the source was not rewritten from incomplete text. The defect is now classified as correctness-blocking and must be removed through a precise local patch or a complete authoritative-file read before final corpus admission.

## Environmental Survival Engineering — predecessor provenance advanced

The chapter root `5D20000000000001` depends on `3AFBE38263D3351E`. That external ID is now resolved directly: it is the opening milestone in `lets_get_started_shall_we.snbt`, itself downstream of the Prologue/onboarding chain. The Environmental Survival root is therefore intentionally available from the early survival curriculum rather than floating on an unknown dependency.

The chapter then adds explicit era authorities as capability increases: the hard-hat/basic industrial protection branch references Era-2 authority, ventilation advancement references later era authorities, and Nether entry is additionally coupled to the Air/Sea Nether-access chain. No new reward-order inversion was identified in the inspected Environmental Survival source.

Remaining Environmental Survival work is reduced to exact provenance of the numbered terminal-era IDs plus deterministic registry/recipe validation of its EnviroMine/Wasteland items and biome IDs.

## Sustenance, Medicine and Habitation — source-level audit cleared

This chapter is a coherent early-survival parallel branch. It has an explicit chapter name/icon and every inspected quest has an explicit name, icon and purpose-specific shape. Its chain begins behind `3AFBE38263D3351E`, which is now resolved to the early Getting Started milestone, and advances through biome survey, seed reserve, rich-soil cultivation, cooking, food stockpiling, grape/yeast cultivation, wasteland survey, radiation medicine and habitation bedding.

Rewards are Numismatics currency and Era-0 priority caches only. No later-era machinery, cyberware, AE2 equipment or other forward technology is granted. No dependency inversion was found.

Disposition: **source-level names/icons/order/reward ownership cleared; final duplicate-ID and registry/biome validation remains in the deterministic corpus gate.**

## Spawn Exchange — source-level audit cleared

Spawn Exchange has explicit chapter and quest names/icons. Its optional broker nodes are tied to the appropriate completed-era handoff IDs: early survivor support after the Prologue, mechanical reconstruction after the furnace/era-1 handoff, then later brokers following the successive civilization-era completions. The apparently offset labels are intentional: each broker becomes available after completion of the preceding era so it can support entry into the named next-era domain.

All nine nodes are optional checkmark/interface encounters and contain no direct item rewards in this chapter, so they cannot themselves leak later technology.

Disposition: **source-level ordering/presentation/reward leakage cleared; final cross-ID existence and duplicate-ID validation remains.**

## Active correctness queue after Run 32

1. **Era-2 Heavy Industry:** remove the confirmed `createcybernetics:eyeupgrades_biomonitor` reward from quest `2210000000000007`; dedicated Cyberware gates it behind Era 4.
2. Air/Sea localization: replace stale relocated-Stronghold wording with Lyran Research wording for `5E0000000000001E` and dependent End-route guidance.
3. Rot reward ownership/bypass classification, including unresolved Era-7 AE2/Create Cybernetics reward ownership and ingredient-era provenance.
4. Parallel Factory: real Excavator/Arc Furnace commissioning evidence where a stable event/advancement/project hook exists.
5. Air/Sea infrastructure authentication: train cargo, submarine, airship station/transponder/radar operational proof.
6. Mutant/Mekanite icon and shape normalization.
7. Darknet presentation normalization.
8. Old World chapter/quest icon normalization.
9. Mekanism Factory chapter icon coverage.
10. Graveyard shared-predecessor provenance.
11. Scavenging/Defense/Containment chapter and quest icon normalization.
12. Abyssal Recovery localization still describing the intentionally removed seven-item deep-research evidence set.
13. Environmental Survival remaining exact terminal-era provenance plus registry/recipe validation.
14. Remaining external registry/provenance checks.
15. Deterministic whole-corpus validator pass including Domain Compendium, duplicate IDs, localization coverage, registry/structure IDs, dependency ordering, reward-era leakage, and icon/name coverage.

## Procedural expansion candidates — identification only

- Sustenance/Habitation: replace stockpile-only depth with optional sustained meal-production, water reserve, crop-diversity and shelter-capacity proofs once stable event hooks exist.
- Environmental Survival: operational ventilation acceptance, exposure-response drills and safe-zone instrumentation rather than additional possession-only PPE tasks.
- Spawn Exchange: broker availability can become a clean diegetic entry surface for era-specific contracts, but broker interaction must remain optional and must never become an alternate technology-unlock path.
- Era-2 farming: after the Biomonitor bypass is removed, use agriculture-native rewards or operational farm-throughput proofs rather than cross-tree cyberware gifts.

Procedural expansion remains behind correctness closure except for candidate identification and design capture.

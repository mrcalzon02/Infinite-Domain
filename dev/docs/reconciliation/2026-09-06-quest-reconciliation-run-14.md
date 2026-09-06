# Quest Reconciliation Run 14

Authoritative branch: `main`
Baseline reconciled before mutation: `e1d0810f1efd9359db71487cc4fcaf6156cc4d34`

## Abyssal Recovery — predecessor trace resolved

The previously unresolved predecessor `5E00000000000006` is `Construct a Submarine` in `config/ftbquests/quests/chapters/air_sea_global_logistics.snbt`. Abyssal Recovery also independently requires Era 4 authority `5410000000000001`, so the branch cannot open before Era 4 merely through its logistics prerequisite.

Combined with the prior internal audit—real biome/structure tasks, faction-specific evidence recovery, dual-branch convergence, explicit icons, and Era-4-tier rewards—Abyssal Recovery is now source-level era-cleared, subject to the eventual global deterministic validation pass.

## Air-Sea and Global Logistics — deterministic Nether objective defect

Source: `config/ftbquests/quests/chapters/air_sea_global_logistics.snbt`

A full source trace exposed a hard completion defect in the Nether transit sequence:

- `5E0000000000000D` (`Find Nether Structure Map`) follows Nether entry and instructs the player to locate `minecraft:stronghold` in `minecraft:the_nether`; its advancement logic also requires creation of the filled target map while in the Nether.
- `5E0000000000000E` (`Reach the Nether Structure`) then uses a STRUCTURE task with `structure: "minecraft:stronghold"` and `dimension: "minecraft:the_nether"`.

This pairs an Overworld stronghold identifier with the Nether and does not implement the intended Nether-research-facility route. Under ordinary generation it can make the route impossible. This is a quest-logic/procedural-development blocker, not merely a wording or icon defect.

Do not repair this by blindly substituting `minecraft:fortress`. The authoritative intended Nether research structure must be identified first. Repository tree/name searches in this run did not expose a clearly named `Lyran` structure authority, so no speculative source mutation was made.

## Air-Sea presentation and authentication follow-up

The same chapter remains under presentation/authentication review:

- no explicit chapter icon was observed in the inspected chapter header;
- `default_quest_shape` is `circle`, which must be reconciled against the established six-shape legend;
- numerous construction/infrastructure milestones use CHECKMARK tasks, including railway station, airfield, propeller aircraft, airline route, submarine, sea facility, shipping route, airship/global route, shuttle/global hub and later planetary logistics. These are not automatically invalid, but each must be matched against localization and any external advancement/structure evidence before being admitted as procedurally authenticated rather than self-certified.

## Validator authority remains blocked by stale oracle paths

`dev/audit_quest_tree_coherence.py` still resolves registry inventory, progression graph, recipe index, and report output beneath obsolete root `docs/` locations even though their authoritative development-only locations are under `dev/docs/`. Missing inputs silently degrade to empty datasets. The repair remains to update the authoritative validator itself and fail loudly on absent required oracle data; do not copy datasets back or add compatibility shims.

The connected GitHub write surface available in this run exposes complete-file replacement, not a targeted source patch. Because the validator and Air-Sea chapter are large authoritative files, they were not reconstructed from segmented reads merely to force a mutation. That would create unnecessary corruption risk without executable regression validation.

## Mandatory repair ledger after this pass

1. Repair `dev/audit_quest_tree_coherence.py` oracle/output paths to `dev/docs` and make required oracle absence fatal.
2. Normalize the secondary FTB Quests validator output destination under `dev/docs`.
3. Remove the six Rot AE2/Cyberware hardware reward bypasses without damaging intended Rot progression.
4. Restore Parallel Factory Excavator and Arc Furnace commissioning semantics on the existing authoritative IDs.
5. Resolve Air-Sea `5E...0D` / `5E...0E` against the authoritative intended Nether research structure, then finish CHECKMARK/icon/shape reconciliation.
6. Normalize Mutant/Mekanite chapter and quest icon metadata.
7. Add the missing Stellaris chapter icon.
8. Normalize Darknet chapter/quest icon metadata and quest-shape legend usage.
9. Run the repaired deterministic validators across the entire current corpus, including the Domain Compendium, and repair every deterministic critical/warning defect before procedural expansion is admitted.

## Expansion candidates retained behind the gate

Once the existing corpus passes the repair gate, prioritize depth that authenticates actual capability: Excavator/Arc Furnace formation and production proofs; structure-backed Air-Sea logistics commissioning; Rot-specific biological research/countermeasure progression; systematic structure-discovery evidence; and per-era operating demonstrations for infrastructure currently represented only by witnessed manual completion.

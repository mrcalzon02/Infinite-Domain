# Old World Investigation Quest Audit — 2026-09-06

Authoritative repository: `mrcalzon02/Infinite-Domain`

Authoritative branch: `main`

Baseline observed before this audit: `cc0e2d3d6e0b52e58c8eda5c41e740b47bdc2d3b`

## Disposition

`config/ftbquests/quests/chapters/old_world_investigation.snbt` is structurally strong in its exploration and evidence authentication, but it is not yet fully admitted as era-correct because its entry authority and presentation metadata remain unresolved.

The chapter header has no explicit chapter `name` and no chapter `icon`. The inspected quest bodies likewise contain no explicit quest icons. Player-facing names may be supplied by localization, so localization completeness must be traced before missing inline names are classified as a defect.

The root quest `4F57000000000000` is an ungated octagon with a single checkmark, no predecessor, and no material reward. This functions as the orientation/entry node but exposes the Old World investigation tree without an explicit era authority.

The downstream implementation uses substantially stronger proof. Explorer-map commands target matching `infinite_domain:old_world/...` structures, subsequent quests require the actual STRUCTURE objective, and evidence nodes require recovered project items from those locations. Confirmed chains include Atlas roadside repair/conveyor/bulk-crushing sites, VCF culture-service/grow-hall/cold-chain/mycological/PT-9 sites, and PolyCore seal-failure/elastomer-exposure sites.

Inspected material rewards are Era-0 priority caches and Numismatics compensation; structure-map commands provide navigation rather than forward-era technology. No direct forward-technology reward leak was found in this chapter during this pass.

## Remaining authority trace

Before source-level era clearance, trace the actual availability of `create:wrench`, `create:fluid_pipe`, and the recovered `kubejs:` evidence items. The open root is acceptable only if these downstream requirements preserve the intended civilization timing and cannot expose progression-critical evidence earlier than planned.

## Validator blocker reconfirmed

`dev/audit_quest_tree_coherence.py` still points required registry, mod-index, progression-graph, recipe-index, and output paths at obsolete root `docs/...` locations. Its missing-file loaders still substitute empty datasets. Whole-corpus validation therefore remains untrustworthy until those authorities move to `dev/docs/...` and required missing oracle files fail loudly.

## Current repair ledger

1. Primary validator `dev/docs` path and fail-loud repair.
2. Rot six AE2/Cyberware reward bypasses.
3. Parallel Factory Excavator/Arc Furnace commissioning restoration.
4. Air/Sea impossible Nether stronghold target plus infrastructure-authentication/icon/shape reconciliation.
5. Mutant/Mekanite chapter/quest icon normalization.
6. Stellaris chapter icon.
7. Darknet chapter/quest icon and legend-shape normalization.
8. Old World localization/icon normalization and root/Create/evidence era-authority trace.
9. Complete deterministic corpus pass including Domain Compendium before procedural expansion is admitted.

## Expansion candidates retained behind the gate

After existing correctness is closed, prioritize operational demonstrations rather than additional possession checks: multiblock commissioning proofs, structure-backed logistics acceptance, Rot biological-countermeasure depth, systematic evidence-led structure discovery, and per-era capability demonstrations that prove infrastructure works before it becomes a dependency of the next civilization tier.

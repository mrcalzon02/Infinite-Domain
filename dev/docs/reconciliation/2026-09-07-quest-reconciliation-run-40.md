# Quest Reconciliation Run 40 — 2026-09-07

## Authority and live-state reconciliation

- Authoritative repository: `mrcalzon02/Infinite-Domain`, branch `main`.
- Run-start `main` HEAD: `4db3770063a5b497c8c5d5ee610af58044d99484` (`Record Rot quest reward audit`).
- The exact persistent file named `AI Project Manager.md` was searched again by title and by the v3.0 Repository Execution Protocol / Minecraft Java Project Profile wording, but did not surface through the available Library lookup. No substitute document was treated as that exact authority.
- Run 39's Rot repair boundary remains authoritative: six mixed AE2/Create Cybernetics reward pairs must be removed while preserving the Cogs, objectives, dependencies, IDs, positions, and final milestone. The current connector still exposes complete-file replacement rather than a true patch primitive, so no unsafe Rot reconstruction was attempted.

## Old World Investigation — full source audit

Source: `config/ftbquests/quests/chapters/old_world_investigation.snbt`, current blob `fafedadcfbfadb39e487070eaec40772c94be95c`.

The entire current chapter was read. It is an optional early investigation tree with three currently developed institutional paths: VCF agricultural/cultural recovery, Atlas industrial-service recovery, and PolyCore material-failure recovery.

### Dependency and ordering findings

- The root `4F57000000000000` is an ungated acknowledgement/checkmark milestone.
- Atlas opens from the root with a Create Wrench, then follows OWS-009 structure discovery -> deterministic evidence -> OWS-010 -> transfer card -> OWS-012.
- VCF opens from the root with bread, then follows OWS-001 -> culture-service evidence -> OWS-002 -> emergency authorization -> OWS-003 -> culture records -> OWS-004 -> cultivation handbook -> OWS-006 -> PT9 report.
- PolyCore branches from the developed Atlas path after the transfer-hall investigation, then follows a fluid-pipe capability check -> OWS-015 -> seal-failure evidence -> OWS-016 -> repeated elastomer-exposure evidence.
- Every dependency in the current chapter points backward to an existing quest in the same source. No dangling quest ID or ordering inversion was found.
- Rewards are explorer maps, Numismatics Cogs, and Era-0 priority caches. No forward-era machinery or specialist-technology reward bypass was found.

### Evidence-item provenance

The chapter's proof items resolve cleanly across the two intended registries:

- `kubejs/config/old_world_evidence.json` is the canonical deterministic proof-item source and explicitly defines one unique item for each OWS-001 through OWS-064 site. The current Old World quest slice uses canonical entries including `vcf_culture_service_manifest`, `emergency_grow_authorization`, `vcf_culture_batch_record`, `evercrop_cultivation_handbook`, `pt9_symbiosis_report`, `atlas_service_plate`, `atlas_transfer_maintenance_card`, `atlas_bulk_process_manual`, `polycore_seal_failure_report`, and `polycore_elastomer_exposure_test`.
- `kubejs/startup_scripts/old_world_narrative_items.js` deliberately registers supplemental lore artifacts without duplicating canonical evidence. Every supplemental document referenced by the current chapter is present there: `vcf_return_crate_log`, `vcf_global_licensing_brief`, `atlas_transfer_maintenance_manual`, `polycore_service_interval_board`, and `polycore_exposure_test_04`.
- `kubejs/startup_scripts/old_world_evidence_items.js` loads the canonical JSON and registers its item list at startup. This closes the previous concern that the quest might refer to unregistered narrative/evidence IDs.

### Structure provenance

The referenced structure IDs use the same `infinite_domain:old_world/...` names present under `kubejs/data/infinite_domain/worldgen/structure/old_world/`. The current directory contains the OWS structure family, including the VCF and Atlas structures used by this chapter. No mismatched namespace or obsolete structure target was found in the developed Old World slice.

### Remaining Old World concerns

1. The chapter source has no explicit top-level `icon`, so Old World remains in the presentation-normalization queue.
2. The root is a bare checkmark rather than a concrete discovery/briefing interaction. That is not an era bypass because the developed rewards are Era-0/support-grade, but it is weak procedural authentication.
3. The currently developed chapter stops after only a subset of the 64 canonical Old World sites. This is not a broken quest condition; it is a major procedural-expansion opportunity once correctness closure is complete.
4. Quest-title/description coverage remains part of the global localization validator because the shared `en_us.snbt` is approximately 398 KB and should be checked mechanically rather than by risky manual whole-file reconstruction.

## Correctness disposition

Old World Investigation is now **source-level cleared for IDs, dependency ordering, evidence registration, structure namespace/provenance, and reward-era ownership**. It remains open only for presentation metadata, stronger root authentication, localization-machine validation, and future expansion of the undeveloped OWS corpus.

## Active correctness queue after this audit

1. Apply the six exact Rot mixed-reward removals through a source-safe mutation path.
2. Normalize stale Air/Sea localization from Nether Stronghold wording to the implemented `infinite_domain:nether/lyran_research` target.
3. Strengthen Parallel Factory end-state commissioning so operational Excavator/Arc Furnace production is proven rather than acknowledged.
4. Strengthen Air/Sea train, submarine, and airship commissioning where stable hooks exist.
5. Normalize presentation metadata in Rot, Old World, Mutant/Mekanite, Scavenging/Defense/Containment, Darknet, and remaining Mekanism-related chapters.
6. Close remaining external predecessor/registry/structure provenance questions outside Old World.
7. Regenerate the deterministic structural audit against current `main`, then extend it to localization coverage, explicit names/icons, registry/structure IDs, reward-era ownership, and Domain Compendium consistency.

## Procedural expansion candidates — Old World

Old World is unusually well suited to deeper procedural investigation because the authoritative evidence registry already defines 64 site-specific proof artifacts while the quest chapter currently exercises only a small subset. Expansion should preserve a repeated archaeological/investigative grammar rather than becoming a generic structure checklist:

`capability preparation -> explorer lead -> structure discovery -> deterministic site evidence -> safe-zone return/analysis -> institutional inference -> next-site lead`.

The strongest expansion families are the currently unused VCF OWS-005/007/008 chain, Atlas OWS-011/013/014 chain, PolyCore OWS-017 through OWS-020, then the Pleroma, Aevum, Helion, Blackglass, Emergency Authority, Continuity, municipal/civilian, and Asterion site families already represented by canonical evidence IDs. Each family should expose a distinct institutional failure mode and require the relevant practical capability before its sites enter the investigation sequence.

The root checkmark should eventually become a concrete Old World briefing or first recovered lead if a stable interaction/event hook is available. Later institutional conclusions should preferably prove that evidence has been returned to a safe analysis context, preventing the chain from collapsing into 'touch structure, move on.'

## Next execution target

Continue correctness before expansion implementation: audit/repair Air/Sea localization and the remaining presentation/provenance chapters, while preserving the exact bounded Rot repair until a complete safe replacement or patch-capable mutation path is available. After chapter-level closure, regenerate and extend the whole-corpus validator and use it to drive the final deterministic error pass across Domain Compendium and shared localization.
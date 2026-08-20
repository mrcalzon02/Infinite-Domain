# 02 — Transition from the Existing Structure Review

## Purpose

This target is intentionally chained after the Wasteland City / basic structure review so the expensive work already spent examining and improving schematics becomes the source pool for narrative locations.

## The handoff is a one-way milestone

When the current review is complete, create a **frozen handoff snapshot** containing at minimum:

- structure ID / registry name;
- schematic/template file path;
- dimensions and approximate footprint;
- generic archetype (warehouse, office, lab, apartment, utility, tower, depot, etc.);
- worldgen registration and rarity/weight if known;
- review result: keep / keep-with-fixes / strong revision source / replace / reject;
- structural defects already fixed;
- notable rooms/features worth preserving;
- dependency on processors, jigsaws, loot tables, entities, modded blocks, or scripts;
- suitability for one or more narrative families.

This snapshot prevents Codex from repeatedly re-auditing the same structures during every later narrative pass.

## Mapping rule

For each of the 64 rows in `04_STRUCTURE_REVISION_MATRIX.csv`:

1. Search the frozen handoff catalog for the best functional source archetype.
2. Prefer a reviewed structure whose size and layout already serve the desired function.
3. Create a revision descendant with a new narrative-specific ID/path.
4. Record explicit lineage: `source_structure -> narrative_variant`.
5. Keep the generic original unless there is a separate reason to replace it.
6. If no reviewed source can support the target without absurd surgery, either:
   - combine modules from multiple reviewed structures, or
   - build the missing structure from scratch and record why reuse was rejected.

## Do not confuse reuse with low-effort reskinning

The point of using reviewed structures is to avoid rebuilding every shell from zero, not to avoid design work. A quest-grade revision should often re-zone interiors, alter access routes, add or remove floors/rooms, change loading/utility connections, add site-specific machinery, create breach/failure evidence, and establish a coherent institution.

A copied warehouse with a VCF sign and a special chest is not a VCF narrative structure.

## Preserve the structural review's lessons

When revising a source structure, retain fixes and quality improvements already made during the audit. Do not resurrect problems the review removed: inaccessible rooms, bad stairs, floating blocks, unsupported decorative elements, broken palettes, impossible doors, generation collisions, bad bounding boxes, dead-end navigation, or unlootable containers.

## Revision lineage manifest

Maintain a machine-readable lineage registry. Recommended fields:

- narrative_variant_id
- source_structure_id
- source_path
- variant_path
- family
- rarity
- collapse_phase
- revision_intensity
- quest_critical
- proof_item_id
- locator_structure_tag/id
- loot_table
- text_registry_ids
- status
- last_validation

This registry becomes the authoritative implementation index for the project.

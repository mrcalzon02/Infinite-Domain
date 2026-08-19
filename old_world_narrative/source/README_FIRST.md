# Infinite Domain — Old World Narrative & Quest-Structure Automation Package

## What this package is

This package is the **next Codex automation target after the current Wasteland City / basic structure review and revision program is complete**. It is not a replacement for that review and must not interrupt it.

The target converts the authoritative Old World narrative bible into an implemented world-storytelling layer. The work is deliberately physical: revised structures, corporate design languages, damage histories, quest-specific locations, structure-bound proof items, readable records, signs, graffiti, rare long-form books, exploration objectives, maps/locators, loot, and late-game re-exploration.

The included canon document is the source of truth. If any instruction in this package accidentally conflicts with that document, **the canon document wins**.

## Immediate execution rule

1. Continue the already-established structural review process using its current method until that process itself says the review is complete.
2. Preserve its final inventory/classification as the source catalog for this project.
3. Then begin `CODEX_AUTOMATION_TARGET.txt` without waiting for another planning cycle.
4. Execute the implementation in incremental, testable waves until the acceptance criteria in `07_IMPLEMENTATION_AND_VALIDATION.md` are met.
5. Do not stop after creating plans, manifests, placeholder JSON, or a small proof-of-concept. Those are intermediate work products, not completion.

## Core target

Create **64 deeply revised narrative structure variants** from the reviewed structure inventory wherever practical. These are revision descendants, not merely renamed duplicates. They must look, function, fail, and tell stories differently enough to serve unique or strongly themed exploration locations.

Also implement the written narrative system needed to support those structures:

- 8 rare serialized long-form in-world book series;
- at least 96 short records / reports / diaries / memos / logs;
- at least 160 reusable sign strings grouped by institution and collapse phase;
- at least 48 graffiti strings, used sparingly;
- 64 unique structure-proof items or equivalent proof tokens;
- the major Exploration quest spine from the canon bible;
- Darknet-gated return visits to selected earlier structures;
- dependable structure-location methods, with Explorer maps as the default fallback for specific rare targets;
- administrator-only recovery documentation for missing or already-looted quest structures on multiplayer worlds.

## The governing design idea

**Charles narrates the rebuilding of civilization. The ruins narrate its death.**

Technology grants capability. Exploration uses that capability. The player physically discovers evidence. Charles interprets it. Existing non-exploration progression continues to do its original job.

## Package contents

- `CODEX_AUTOMATION_TARGET.txt` — paste/attach this as the master execution instruction.
- `01_CANON_AND_NONNEGOTIABLES.md` — fixed facts and narrative constraints.
- `02_TRANSITION_FROM_STRUCTURE_REVIEW.md` — exact handoff from the current audit/revision work.
- `03_STRUCTURE_REVISION_PROGRAM.md` — how to turn reviewed structures into quest-grade narrative variants.
- `04_STRUCTURE_REVISION_MATRIX.csv` — 64 target variants and their intended roles.
- `04A_STRUCTURE_REVISION_MATRIX_GUIDE.md` — how Codex should map the abstract targets to actual audited schematics.
- `05_WRITTEN_LORE_NOVELS_AND_TEXTS.md` — corpus architecture and writing rules.
- `05A_LORE_CORPUS_SEED.csv` — concrete seed titles and placements.
- `06_EXPLORATION_QUEST_INTEGRATION.md` — quest spine, proof items, maps, and re-exploration.
- `07_IMPLEMENTATION_AND_VALIDATION.md` — phases, tests, and completion gates.
- `08_ADMIN_RECOVERY_AND_MULTIPLAYER.md` — safe multiplayer recovery model.
- `09_AUTOMATION_STATE_TEMPLATE.json` — restart-safe progress ledger schema.
- `source/...CANON.docx` — authoritative narrative bible copied into the package.

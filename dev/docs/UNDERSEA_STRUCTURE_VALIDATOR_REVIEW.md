# Undersea Structure Validator — End-to-End Review

*Reviewed 2026-08-23. Scope: the deep-sea/"undersea" structure subsystem — `docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md`, `docs/DEEP_SEA_STRUCTURE_AUDIT.md`, `docs/deep-sea-structures.md`, `structure_library/deepsea-catalog.json`, `structure_library/deepsea-metadata.schema.json`, `structure_library/deepsea-refinement-policy.json`, `docs/deepsea-structure-validation.json`, and the three scripts that run the pipeline: `scripts/generate_deep_sea_structures.py`, `scripts/validate_deep_sea_structures.py`, `scripts/render_deep_sea_review.py`. Cross-referenced against `CODEX_STRUCTURE_PIPELINE.md`, `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md`, and `.codex/structure_pipeline_state.md`.*

*Method: this wasn't a read-through alone. The generator and validator were copied into a scratch sandbox and actually executed — regenerating all nine assets' NBT from the real source, running the real validator against that output, and inspecting the resulting block data directly — the same "dump real coordinates, don't just re-read the code" standard the project's own audit docs hold themselves to. Every finding below marked "verified" was confirmed this way, not inferred from reading the script.*

## Summary

The system is well-designed and unusually self-aware — the standards document and both audit files already candidly list several open gaps (no in-game walkthrough, no real submersible-hull testing, Tier 1 out of scope, no four-view-render parity with the land corpus). Those are accurately disclosed already and aren't repeated here as new findings.

What this review adds: three concrete defects the existing process does not currently catch, verified by actually running the pipeline, plus a handful of process-level gaps in how this subsystem connects back to the rest of the Codex pipeline's discipline. None of this is visible from reading the docs alone — all three code-level findings required executing the generator and inspecting its output, which is exactly the class of defect the docs' own "Size and visual composition audit" section was written to catch (it explicitly says the initial wave "passed every automated check while still being genuinely" wrong in ways nobody had looked for). The pattern continues.

## Confirmed defects

### 1. `flooded_relay_shelter`'s access shaft has a one-block dry gap, mid-column, in a structure declared fully flooded

**Verified.** The asset's metadata declares `dominant_atmosphere_state: flooded`, `has_mixed_compartments: false` — i.e., no exceptions, the whole thing should read as submerged. Regenerating the NBT and reading the shaft column at `x=4, z=4` (the ladder shaft connecting the chamber to the seabed trapdoor) shows:

| y | block |
|---|---|
| 2 | sea_pickle (waterlogged) |
| 3 | water |
| **4** | **ladder, `waterlogged: false`** |
| 5 | ladder, `waterlogged: true` |
| 6 | ladder, `waterlogged: true` |
| 7 | ladder, `waterlogged: true` |
| 8 | iron_trapdoor, `waterlogged: false` |

The cell at `y=4` — right where the chamber ceiling meets the shaft — is a dry, unwaterlogged ladder rung sandwiched between water at `y=3` and waterlogged (flooded) rungs at `y=5–7`. A wider scan of all nine generated assets for "dry passable cell with water immediately above and below" found exactly one hit, and this is it — every other structure's flood columns are continuous.

This is the exact defect class `DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md` names as "the single most common silent defect class for this asset type": an accidental air pocket in a compartment meant to be flooded. It's also the same *kind* of fill-order bug the audit already caught and fixed twice elsewhere in this same wave (the wreck's biofouling, the rig's moon pool) — but this one slipped through.

**Why the validator missed it.** `validate_atmosphere_fill()`'s check for `flooded_relay_shelter` only samples `y in (1, 2, 3)` — the chamber interior and floor. The shaft column runs `y=4` through `y=8` and is never sampled at all. Re-running the real validator against the real regenerated NBT confirms this directly: it reports `"_atmosphere_fill": {"metadata_valid": true, "issues": []}` — a clean pass — on a file that has a verified air pocket. The committed `docs/deepsea-structure-validation.json` reflects this same false-clean result.

**Suggested fix:** extend `validate_atmosphere_fill()`'s `flooded_relay_shelter` sample set to cover the shaft column (`x=4, z=4, y=4..8`, or better, derive it from the same constants the generator uses — see the process note below), then fix the generator: the ladder re-carve loop in `flooded_relay_shelter()` only touches `y in (5, 6, 7)` and should include `y=4` (whether that means waterlogging it or, if `y=4`/`y=8` are meant to stay dry as a design choice, declaring `has_mixed_compartments: true` instead of `false` so the metadata matches reality).

### 2. Re-running the generator silently duplicates rows in the shared registrant CSV

**Verified, reproduced.** `append_ocean_structure_set_row()` in `generate_deep_sea_structures.py` unconditionally appends five rows to `docs/biome-gating-audit/ocean-structure-sets.csv` every time `generate()` runs, with no check for whether those rows already exist. Running the real script three times in a row against a copy of the real CSV took the deep-sea row count from 5 to 15 to 20 — the same five registrants duplicated verbatim on every run. `validate_placement_gate()` doesn't catch this either: its check is `name in csv_text` (a substring-presence test), which stays true regardless of how many duplicate rows exist.

The live committed CSV is currently clean (exactly one row per registrant) — but this generator has already been re-run at least twice in this project's own history (the Wave 1 furniture fix and the Wave 2 addition are both described as full regenerations), and a Codex pipeline whose own operating model is "resume the next unfinished unit" across sessions will run it again. `docs/biome-gating-audit/ocean-structure-sets.csv` is explicitly described as "the single source of truth" and "the authoritative registrant list every placement in this system must be checked against" — an append-only write with no idempotency guard is a standing risk to that claim, not a hypothetical one.

**Suggested fix:** have `append_ocean_structure_set_row()` (or `generate()` before calling it) skip rows whose `target` value already appears in the CSV, or rewrite the deep-sea section of the CSV wholesale each run (the same idempotent pattern `write_json` already uses everywhere else in this script).

### 3. The validator silently skips two of the schema's required fields for every Tier-3 structure

**Verified.** `structure_library/deepsea-metadata.schema.json` requires `category`, `build_style`, `burial_state`, `access_connector`, `dominant_atmosphere_state`, `source_role`, `refinement_intensity`, `source_license`, `production_status`, `footprint`, and `height` for any `asset_class: structure` entry. Diffing the schema's controlled-vocabulary enums against `validate_deep_sea_structures.py`'s hand-copied Python sets shows those are all in sync — that part is healthy. But `validate_structure()` never checks `category` or `source_role` at all; neither string appears anywhere in the validator source. A future entry with a missing or misspelled `category`/`source_role` would pass validation silently.

`footprint` and `height` fare a little better but are weaker than they look: they're only checked via `validate_nbt_dimensions()`, which returns immediately if `source_template` isn't set — meaning an entry with no NBT yet (a legitimate state for a `rough_source`-stage asset) gets no footprint/height check at all, not even a presence check. And even when `source_template` is set, a missing `footprint` (as opposed to a wrong one) is never flagged, because the comparison is guarded by `isinstance(footprint, dict)`, which silently short-circuits when it's absent.

None of this currently produces a false pass — all nine shipped assets happen to declare every field correctly. It's a latent gap for the next asset, not a live defect in this wave.

**Suggested fix:** add `check_enum(entry, "category", {"wreck", "submariner_facility"}, issues)` and `check_enum(entry, "source_role", {"rough_source", "clean_master", "damage_variant", "occupation_variant"}, issues)` to `validate_structure()`, and add an explicit `require(entry, "footprint", dict, issues)` / presence check for `height` independent of whether `source_template` is set.

## Process-level gaps

**The deep-sea system's own progress is invisible to the pipeline's resumability file.** `CODEX_STRUCTURE_PIPELINE.md` requires updating `.codex/structure_pipeline_state.md` "after every meaningful verified batch" and instructs every new session to read that file first to decide what to resume. It contains zero mentions of "deep sea" or "deepsea" anywhere — despite Wave 1, Wave 2, and the size/visual-composition pass (three substantial, multi-defect-fixing batches) all having happened roughly four days after that file's last edit (by file mtime). A future Codex session following its own documented startup procedure would have no way to learn this subsystem exists from the file that's supposed to be authoritative for exactly that purpose; it would have to stumble onto `DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md` independently. Similarly, `.codex/structure_pipeline_blocked.md` records the land corpus's "no Minecraft client access" blocker but doesn't cross-reference that this is the same root blocker the deep-sea audit separately (and correctly) cites for its own "no in-game walkthrough yet" status — two parallel, unlinked blocker narratives for one underlying constraint.

**The subsystem doesn't use the shared QA gate the rest of the pipeline just adopted for the same reason this bug exists.** Stage A.5 of `CODEX_STRUCTURE_PIPELINE.md` replaced the land corpus's old per-structure heuristic checker (`assess_fidelity()`) with a shared, more rigorous `scripts/structure_geometry_lint.py` specifically because the old ad hoc checker "cannot and does not detect" defect classes like accidental air/water gaps — it's described as "a door/window/fixture keyword counter." The deep-sea system, built after that lesson was written down, doesn't import or reference `structure_geometry_lint.py` or `structure_geometry_primitives_v2.py` at all (confirmed by search — zero matches in either direction); it has its own bespoke, hand-rolled validator instead. Defect #1 above is precisely an instance of the failure mode Stage A.5 exists to prevent, happening again in the one part of the pipeline that didn't inherit the fix.

**Directory-layout claim doesn't quite match practice.** The standards doc states deep-sea assets should live "under `structure_library/` using the existing corpus layout (`sources/`, `variants/`, `reviews/`, `licensing/`) with a `deep_sea` category, rather than a parallel directory tree." In practice, `structure_library/audit_renders/deep_sea/` does follow that pattern, but `variants/`, `reviews/`, and `sources/` have no deep-sea entries at all — the system instead uses its own root-level trio (`deepsea-catalog.json`, `deepsea-metadata.schema.json`, `deepsea-refinement-policy.json`) that parallels, rather than reuses, the land corpus's `catalog.json` / `structure-metadata.schema.json` / `generated-structure-refinement-policy.json`. This is a minor label/reality mismatch, not a functional bug — but worth resolving one way or the other so the stated convention is either followed or corrected.

**Hardcoded coordinates duplicate the generator's geometry instead of sharing it.** The atmosphere-fill checks in `validate_deep_sea_structures.py` re-derive sample coordinates as literals (`(x, y, 17)` for the wreck's breach, `RIG_CX_CONST = 13 // 2  # mirrors RIG_CX in generate_deep_sea_structures.py`, etc.) rather than importing the generator's actual constants. This isn't a bug today — the render-color-table sync between generator and validator is a working example of the same pattern kept correctly in sync — but it's the same structural risk that produced defect #1: nothing enforces that the validator's idea of "where the interesting cells are" tracks the generator's idea of "where I put them" if either changes.

## What's already known and accurately disclosed (not repeated as new findings)

The standards doc and both audit files already state, correctly: no in-game walkthrough has happened (no Minecraft client access this session); the access connectors (`diver_hatch`, `buried_shaft`, `moon_pool`) haven't been tested against real `create_submarine`/`create_aquatic_ambitions` hulls; the renderer doesn't yet match the land corpus's four-view isometric treatment; the exclusion-zone geometry check against `WORLDGEN_STRUCTURE_SAFETY.md`'s 8-chunk standard is recorded as spacing/salt data but hasn't been run in-game; and Tier 1 (macro geological terrain) is explicitly out of scope for this wave. All of that is accurate and doesn't need re-flagging here.

## Verified healthy

For balance: several things this review specifically checked for turned out fine. The render-color curated table (`render_deep_sea_review.py`'s `KNOWN_BLOCK_COLORS`) and the validator's mirror of it are in exact sync — every block name actually placed across all nine regenerated assets resolves to a curated color with zero hash-fallback warnings, confirmed by generating fresh NBT and diffing its full block-name set against both lists. The controlled-vocabulary enums (asset class, depth band, build style, burial state, access connector, atmosphere state, refinement intensity, production status, damage causes, occupation states) are byte-for-byte identical between the schema and the validator's Python sets. And the three previously-documented fixes — the Wave 1 furniture-height correction, the wreck's biofouling fill-order fix (independently recounted here: 12 `prismarine_bricks`, 3 `sea_pickle`, matching the ledger exactly), and the mining rig's moon-pool reseal — are all genuinely present in the current generator code, not just claimed in the docs.

## Recommended priority

1. Fix the `flooded_relay_shelter` shaft air gap (defect #1) and extend its atmosphere-fill check to actually cover the shaft — this is a live, shipped defect in the one asset currently registered for world generation from that family.
2. Add a dedupe guard to `append_ocean_structure_set_row()` before this generator is run again (defect #2) — cheap fix, currently-clean state, but the next regeneration will corrupt it otherwise.
3. Backfill `.codex/structure_pipeline_state.md` with a deep-sea section so the subsystem is discoverable through the pipeline's own resumability discipline, and decide whether `structure_geometry_lint.py` should be extended to cover underwater geometry or whether the standards doc should explicitly document why it doesn't apply.
4. Close the validator's `category`/`source_role`/footprint-presence gaps (defect #3) before the next wave adds assets that could actually trip them.

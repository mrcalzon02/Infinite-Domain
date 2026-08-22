# [SYSTEM REPORT] Old World Herd Automation Protocol

## Purpose

This document is the durable orchestration contract for scheduled advancement of the Infinite Domain Old World heavy-rebuild program. It exists so a fresh scheduled conversation can recover from GitHub state rather than from accumulated chat context.

## Authorities

1. Procedure: `docs/HEAVY_REBUILD_DOCTRINE.md`
2. State: `old_world_narrative/registry/heavy_rebuild_state.json`
3. Repository branch: `main` only
4. Per-target review records and persisted fixed-camera artifacts are the evidence authority for visual gates.

Never create a feature branch or pull request for this program. Never force-push. Never infer runtime approval from static/heavy-rebuild completion.

## Herd execution model

An hourly run may advance several OWS targets as independent lanes when doing so does not create conflicting writes. The lane is the unit of work; all lane work must remain target-qualified.

Each target still obeys the complete doctrine sequence:

`donor audit -> Phase 0 baseline -> Passes 2-5 -> Gate A -> Passes 7-12 -> Gate B -> Passes 13-18 -> Gate C -> Pass 19 -> authoritative shipping builder -> Gate D -> static validation -> quality promotion`

Concurrency is permitted for independent authoring, analysis, rendering preparation, and target-local implementation. Shared authoritative writes must be serialized.

## Hard visual-gate rule

Automation may build and render Gate A/B/C/D candidates, run mechanical assertions, compare hashes, compute image-regression metrics, and persist provenance. It may not invent or silently record visual approval.

A gate changes to `PASSED` only after the exact persisted fixed-camera artifact for that revision has been inspected and an explicit review record states the decision. If no reviewer is available during a scheduled run, leave the lane at `REVIEW NEEDED` and advance other lanes that are not blocked.

A worker that authored a candidate must not treat its own source-code expectations or mechanical assertions as visual approval.

## Shared-state serialization

The following are single-writer resources and must not be raced between lanes:

- `old_world_narrative/registry/heavy_rebuild_state.json`
- authoritative production-builder dispatch tables
- common generation registries
- common loot/proof registries
- common workflows when a change affects more than one target
- generated shipping structures when a common generator rewrites the complete set

Target-local review documents, target-local renderer modules, target-local artifacts, and target-local planning records may be prepared independently, then merged into shared state sequentially.

Before every write, re-read current `main` or recent commits. Preserve concurrent work that has already landed. Do not duplicate or overwrite newer target progress.

## Lane selection

At the beginning of an hourly run:

1. Read current `main`, recent commits, doctrine, authoritative state, and active gate records.
2. Identify all targets with useful work that can proceed without pretending a blocked visual decision has occurred.
3. Prefer finishing the oldest/most advanced target, but allow younger independent lanes to perform planning, donor audits, baseline preparation, or implementation that does not violate the single-target sequencing contracts encoded in state.
4. Do not allow downstream history/damage work to begin before the target's Gate B is explicitly passed.
5. Do not allow Pass 19 or shipping synchronization before Gate C is explicitly passed.
6. Do not promote static quality before Gate D is explicitly passed and authoritative shipping synchronization is proven.

## Authoritative synchronization

For a final target:

- production geometry must live in side-effect-free production code, not import review/rendering modules;
- the production builder must reproduce the accepted Gate-C D3 geometry before Pass-19-only microdetail;
- Gate D must build through the authoritative production dispatch;
- normal production stabilization must be applied exactly as shipping generation applies it;
- serialized authoritative-builder bytes and generated shipping NBT must match exactly after decompression;
- Gate D renders the shipping NBT itself;
- image regression against the accepted Gate-C D3 artifact may reject excessive drift but may not approve the gate;
- manual inspection of the exact Gate-D artifact remains mandatory.

## Failure behavior

Mechanical defect: repair only the demonstrated defect and rerun the same gate revision or next revision as appropriate.

Visual defect: write an explicit `REVISION REQUIRED` record, freeze accepted aspects, revise only the failing aspects, and rerender.

Tool/capacity boundary: persist exact provenance/status and stop that lane without falsely marking progress.

Concurrent repository advancement: rebase the plan conceptually onto live `main`; do not recreate work that already landed.

## Scheduled-run output grammar

Keep scheduled conversation output extremely small. One line/phrase per lane only:

`OWS-### <gate/pass> — ADVANCED`

or

`OWS-### <gate/pass> — REVIEW NEEDED`

or

`OWS-### <gate/pass> — BLOCKED: <short reason>`

Finish with one phrase:

`NEXT: <single highest-value action>`

Do not narrate routine GitHub reads, compilation, artifact uploads, or successful assertions in the scheduled conversation.

## Current recovery rule

Never trust this document for the current target number or revision. Always derive those from live `main` and `heavy_rebuild_state.json` at the beginning of each run.

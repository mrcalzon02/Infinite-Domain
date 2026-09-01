# [SYSTEM REPORT] Old World Herd Automation Protocol

## Purpose

This document is the durable orchestration contract for scheduled advancement of the Infinite Domain Old World heavy-rebuild program. It exists so a fresh scheduled conversation can recover from GitHub state rather than from accumulated chat context.

This file is **not** itself an automatic scheduler trigger. Codex automatically discovers repository instructions through the root `AGENTS.md`; the actual recurring trigger must be configured as a Codex Scheduled Task for this project. Once configured, the scheduled task points back to this durable contract and the repository becomes the continuity source between runs.

## Authorities

1. Procedure: `docs/HEAVY_REBUILD_DOCTRINE.md`
2. State: `old_world_narrative/registry/heavy_rebuild_state.json`
3. Repository branch: `main` only
4. Per-target review records and persisted fixed-camera artifacts are the evidence authority for visual gates.
5. Repository Codex entrypoint: `AGENTS.md`
6. Project-scoped subagent definitions: `.codex/agents/`

Never create a long-lived feature branch or pull request for this program. Never force-push. Never infer runtime approval from static/heavy-rebuild completion.

## Codex scheduled-task bootstrap

### Recommended scheduled task

Create a **standalone Codex Scheduled Task** with the following configuration:

- Name: `Old World Heavy Rebuild Herd`
- Project: the local Infinite Domain repository
- Execution location: the local project checkout on `main`
- Cadence: hourly
- Conversation behavior: standalone/fresh scheduled run, not a permanently growing chat thread

The fresh-run behavior is intentional. Every invocation must recover from repository state and this document, not depend on previous scheduled-task conversation context. This keeps long-lived automation restartable and prevents accumulated chat context from becoming the state authority.

For local-project execution, the machine and Codex desktop application must be available when the scheduled task fires. Do not manually edit the same authoritative files while an unattended herd run is actively writing them.

If the user explicitly chooses isolated worktree execution instead, the coordinator must still preserve `main` as the only authoritative development history and must integrate accepted work deliberately rather than allowing long-lived parallel branches to accumulate.

### Exact scheduled-task prompt

Use this prompt verbatim or preserve its semantics exactly:

```text
Execute the Infinite Domain Old World Heavy Rebuild Herd.

Read and obey AGENTS.md, docs/OLD_WORLD_HERD_AUTOMATION.md, docs/HEAVY_REBUILD_DOCTRINE.md, and live old_world_narrative/registry/heavy_rebuild_state.json.

Act as Herd Coordinator. Explicitly spawn the project-scoped Codex subagents defined in .codex/agents/: use one ows-structure-worker per eligible target, up to six concurrent target lanes when safe and capacity allows; use ows-visual-reviewer, ows-integration-reviewer, and ows-validator independently where applicable. Keep all shared authoritative writes serialized through the coordinator.

Recover only from live main/repository state; never redo completed work. Advance each target only in doctrine order. Never fabricate visual approval. If a lane reaches a review-only gate, persist it as REVIEW NEEDED and immediately use available worker capacity on another eligible target.

Continue dispatch/integration waves until this scheduled run has no safe executable work remaining, then emit only the scheduled-run output grammar defined in docs/OLD_WORLD_HERD_AUTOMATION.md.
```

### One-command Codex setup request

From a Codex chat opened on the Infinite Domain project, the user can request creation of the schedule with:

```text
Create a standalone scheduled task named "Old World Heavy Rebuild Herd" for this Infinite Domain project. Run it hourly in the local project using the exact Scheduled Task Prompt in docs/OLD_WORLD_HERD_AUTOMATION.md. After creating it, start the first run now.
```

The scheduled task is the recurring heartbeat. Do not create a nested permanent `/goal` inside every scheduled run. A `/goal` may be used separately when the user wants one immediate long-running manual marathon session, but repository state remains authoritative either way.

## Native Codex subagent herd

The coordinator must use the project-scoped agent definitions under `.codex/agents/` when native subagents are available:

- `ows-structure-worker` — one exclusively owned OWS target at a time;
- `ows-visual-reviewer` — independent inspection of persisted fixed-camera artifacts where the doctrine permits agent review;
- `ows-integration-reviewer` — independent quest/evidence/loot/proof/worldgen/registry review;
- `ows-validator` — independent static, serialization, structural, and regression validation.

Default structure-worker concurrency is **up to six target lanes**, bounded by the current Codex concurrency limit and by actual write independence. The coordinator should refill a worker slot with the next eligible unresolved target whenever a worker completes or reaches a genuine review/blocking boundary.

Per-target work may be parallel. Shared authoritative mutation is serialized. The coordinator is the only lane permitted to integrate competing shared-state changes after re-reading live `main`.

Do not alter the current `heavy_rebuild_state.json` execution-policy schema merely to advertise concurrency unless the repository's validators/schema are also deliberately revised. The orchestration contract can permit multiple target lanes while each individual target continues to obey the full sequential doctrine.

If the current Codex runtime cannot spawn subagents, state that fact honestly and continue useful safe work sequentially. Never simulate reports from workers that were not actually created.

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
7. Assign exclusive ownership for every target selected into the current worker wave.
8. When a worker slot becomes free, re-read live state and dispatch the next eligible target rather than idling while independent work remains.

## Wave integration protocol

For every concurrent worker wave:

1. The coordinator assigns exclusive target ownership.
2. Structure workers advance only target-local work and return proposed shared mutations instead of racing common files.
3. Independent visual, integration, and validation agents inspect the resulting target work where applicable.
4. The coordinator waits for the required results, evaluates conflicts, and re-reads current `main`.
5. The coordinator serializes shared authoritative writes one at a time.
6. Run the relevant repository validators after shared integration.
7. Commit a coherent verified batch to `main` when appropriate.
8. Re-read state and refill the available worker pool with the next eligible targets.

Parallel execution must increase throughput without weakening the doctrine, visual-gate requirements, provenance, or completion honesty.

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

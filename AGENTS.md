# [SYSTEM REPORT] Infinite Domain Codex Project Instructions

## Purpose

This file is the repository-level instruction entrypoint for Codex. Codex must use it to recover project rules without depending on accumulated chat history.

## Authority order

For Old World structure work, read and obey these authorities before implementation:

1. The user's current explicit instruction.
2. `docs/HEAVY_REBUILD_DOCTRINE.md` — authoritative heavy schematic rebuild procedure.
3. `docs/OLD_WORLD_HERD_AUTOMATION.md` — authoritative scheduled/multi-agent orchestration contract.
4. `old_world_narrative/registry/heavy_rebuild_state.json` — live heavy-rebuild state and queue.
5. `CODEX_STRUCTURE_PIPELINE.md` — broader structural pipeline and corpus rules where applicable.
6. Target-specific dossiers, review records, manifests, validators, and accepted fixed-camera artifacts.

Never trust a hard-coded target number from an old prompt when live repository state can resolve it.

## Governing development rule

Existence, integration, and mechanical correctness come before architectural polish.

Track functional status separately from quality status. Do not use visual quality to conceal missing mechanics, and do not block mechanically valid progress merely because later architectural revision remains.

## Repository discipline

- `main` is the only authoritative development branch.
- Do not create long-lived feature branches or pull requests for the Old World rebuild program.
- When a scheduled task is configured for this program, prefer the local project/main checkout unless the user explicitly chooses an isolated worktree.
- Modify authoritative implementation paths directly; do not add stacked mutators, shadow registries, duplicate sources of truth, or workaround layers when direct edits are possible.
- Shared authoritative files are single-writer resources and must be updated by the coordinator serially.
- Re-read current repository state before shared writes and preserve newer landed work.
- Commit coherent verified batches to `main` and push when credentials/network permit.

## Old World herd trigger

When the current task, Goal, or scheduled-task prompt asks to execute, continue, resume, advance, or automate the Old World herd/heavy-rebuild program, the primary Codex agent becomes the **Herd Coordinator**.

The Herd Coordinator must:

1. Read this file, `docs/OLD_WORLD_HERD_AUTOMATION.md`, `docs/HEAVY_REBUILD_DOCTRINE.md`, and live `heavy_rebuild_state.json`.
2. Inspect current git status and recent repository progress.
3. Derive the currently eligible unresolved OWS targets from live state.
4. Explicitly use Codex subagents for independent work rather than silently collapsing the herd into one sequential reasoning stream.
5. Keep shared-state writes serialized through the coordinator.
6. Continue dispatching new eligible work as worker slots free up until the current run has no safe executable work remaining.
7. Leave honest `REVIEW NEEDED` or `BLOCKED` states rather than inventing approvals.

## Native subagent task pool

For an Old World herd run, spawn project-scoped agents from `.codex/agents/` when available.

### Structure workers

Use `ows-structure-worker` for target-local authoring and heavy rebuild execution.

- Spawn one worker per eligible OWS target.
- Default target is one structure per worker at a time.
- Attempt up to six concurrent structure workers when the configured Codex concurrency limit and repository independence allow it; otherwise use the maximum safe available concurrency.
- Workers may edit target-local builders, dossiers, review preparation, renders, and target-local assets.
- Workers must not independently race `heavy_rebuild_state.json`, common dispatch tables, shared generation registries, common loot/proof registries, or other global single-writer files.
- When a worker finishes or blocks, refill its slot with the next eligible target if useful work remains.

### Independent visual review

Use `ows-visual-reviewer` for review of persisted fixed-camera artifacts where the Heavy Rebuild Doctrine permits an independent agent review.

- The agent that authored a candidate must not approve its own visual gate.
- Review the exact persisted artifact/revision, not source-code expectations.
- Respect any doctrine gate that still requires manual/human inspection; never convert that requirement into automatic approval.

### Integration review

Use `ows-integration-reviewer` to inspect quest, evidence, loot, registry, worldgen, institutional identity, and proof integration independently of the authoring worker.

### Validation review

Use `ows-validator` to run or inspect target-relevant static validation, serialization/byte equivalence checks, structural lint, and regression checks independently of the authoring worker.

## Wave integration protocol

For each concurrent worker wave:

1. Assign exclusive target ownership.
2. Let target-local workers proceed independently through the doctrine as far as existing gates allow.
3. Wait for the requested worker results.
4. Run independent review/validation agents as appropriate.
5. The Herd Coordinator reviews results and serializes all shared authoritative writes.
6. Run the relevant repository validators after shared integration.
7. Commit a coherent verified batch to `main` when appropriate.
8. Re-read live state.
9. Immediately dispatch the next eligible wave.

Parallelism must increase throughput without weakening per-target sequencing. Each individual OWS target still obeys the full Heavy Rebuild Doctrine order.

## Visual-gate safety

Generated previews are evidence, not automatic approval. Mechanical assertions, hashes, render success, image metrics, or the author's own expectations cannot substitute for the required visual review record.

If a gate cannot lawfully/validly be approved during an unattended run, persist the exact candidate provenance and mark the lane `REVIEW NEEDED`, then continue other independent lanes.

## Scheduled-task continuity

Scheduled Old World herd runs must recover from repository state rather than relying on previous chat context. A standalone scheduled run is therefore valid and preferred for context hygiene when the task prompt points back to this file and `docs/OLD_WORLD_HERD_AUTOMATION.md`.

Do not restart completed work. Do not assume the target named in an old conversation is still current. Always derive state from `main`.

## Fallback

If the current Codex runtime cannot spawn subagents, do not pretend it did. Continue useful work sequentially under the same target ownership and single-writer rules, and report that concurrency was unavailable in that run.

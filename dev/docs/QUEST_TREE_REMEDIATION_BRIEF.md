# Quest Tree Remediation — execution brief

Hand this to a fresh session. It is the *current* state of the quest-tree
findings and what to do next. The reasoning, inventory, and systemic analysis
live in `QUEST_TREE_COHERENCE_AUDIT.md`; this brief only reconciles that plan
against what the audit reports **today** and orders the remaining work.

Baseline verified 2026-09-01, after the Domain Compendium item-form fix:

```
python dev/scripts/audit_quest_tree_coherence.py     # 0 critical, 936 findings
python dev/scripts/audit_quest_loot_attainability.py # exit 0, 11 LOOT-ORPHAN warnings
python dev/scripts/audit_domain_compendium_chapter.py # PASS, 9,891 items / 301 sections
```

**All criticals are cleared.** Everything below is warning or info.

## Standing constraints — read before touching anything

1. **Never hand-edit quest SNBT.** FTB Quests rewrites these files on load: it
   converts unresolvable item ids to `ftbquests:missing_item` (preserving the
   intended id in a `components` entry) and strips fields it considers default —
   it silently removed the Compendium's chapter `icon:`. A manual fix survives
   until the next launch. Fix the generator, then regenerate.
2. **Quest ids are player progress.** FTB keys progress on task id. The Compendium
   is now protected by `dev/docs/domain-compendium/quest-id-ledger.csv`, which
   binds ids to content instead of file position; regenerating reports
   `0 newly issued`. **Other chapters are still positional** — reordering or
   inserting quests there renumbers everything after the insertion point. Extend
   the ledger pattern before any chapter-wide regeneration.
3. **Use the shared oracle.** `dev/scripts/pack_content_oracle.py`. Use
   `ItemOracle.has_item_form()` for anything a player must hand in — `exists()`
   is looser (it trusts ids scraped from mod jars and returns True for block-only
   ids a jar merely mentions). Do not build a second existence check.

## Validation gate for every workstream

```
python dev/scripts/audit_quest_tree_coherence.py      # 0 critical, no new findings
python dev/scripts/audit_quest_loot_attainability.py  # still exit 0
node dev/scripts/audit_ftbquests.js --allow-automatic-icons
```

Compare finding counts **by category** against the baseline above. A total that
drops is not sufficient evidence — check that nothing increased.

## Workstreams, in dependency order

### W0 — acceptance probe repair *(in flight, blocks W4)*

`acceptance.probeErrors` is non-empty, so the benchmark proves the pack boots and
generates chunks but cannot substantiate any structure-level claim.
`structureStartsByNamespace` comes back `{}`.

Current failure, stage `structure_starts`, reproduced in two consecutive runs:
Rhino cannot disambiguate `server.getLevel(...)` at
`kubejs/server_scripts/worldgen_benchmark.js:156` because a mod adds a
`getLevel(ResourceLocation)` overload alongside vanilla's `getLevel(ResourceKey)`.
Earlier runs failed differently (3 errors at stage `mod_snapshot` on 2026-08-31),
so audit **every** probe stage, not just this one.

Done when a smoke run completes *and* `acceptance.probeErrors` is empty.

### W1 — 88 `missing-title` warnings *(largest, most mechanical, start here)*

Quests with no localized title, concentrated in companion-mod chapters:

| chapter | count |
|---|---|
| `create_specialist_workshops` | 24 |
| `create_big_cannons_doctrine` | 15 |
| `graveyard_gateway_containment` | 15 |
| `powered_field_engineering` | 15 |
| `supplementaries_civic_utility` | 14 |

Each of these chapters has its own audit script in `dev/scripts/`
(`audit_create_specialist_workshops.py`, `audit_powered_field_engineering.py`,
…). Treat this as **one systemic generator defect**, not 88 edits: find where
those chapters are produced and make them emit lang keys the way the era
chapters do. Verify the keys land in `config/ftbquests/quests/lang/en_us.snbt`.

Low risk, no id changes, no design decisions. Best first win.

### W2 — 2 `era-regression-dependency` warnings *(small, real progression bug)*

```
era_03 quest 6301100000000008 'Create Re-Automated: Netherite Drill' -> era_04 quest 6411000000000001
era_03 quest 6301100000000009 'Create Re-Automated: Stabilizer'      -> era_05 quest 6511000000000001
```

An Era 3 quest gated behind Eras 4 and 5. This is exactly item 4 (W5) of
Tranche A, which `QUEST_TREE_COHERENCE_AUDIT.md` records as **applied on
2026-08-27** — yet both findings are still live. Establish whether the fix was
never applied or has regressed before re-fixing, and correct the audit doc's
status either way. Relocate or re-parent the two quests.

### W3 — 70 `checkmark-outside-prologue` + 12 `weak-authentication` *(Tranche C)*

Self-certified checkmarks standing in for real completion, spread across
`parallel_factory_paths` (8), `create_specialist_workshops` (7),
`era_08_infinite_domain` (7), `graveyard_gateway_containment` (5),
`create_big_cannons_doctrine` (4), and others. Per Tranche C: convert to
item/structure/advancement/stat tasks where the intent is verifiable; keep only
genuine orientation and planning nodes and give those a distinct shape. Then
address the 12 weak-authentication quests (multiblock outputs, unique
intermediates).

Per-quest judgment — the slowest workstream. Do it after W1/W2 have proven the
validation loop.

### W4 — 19 `gate-item-structure-loot` warnings *(blocked on W0 + a decision)*

| chapter | count |
|---|---|
| `old_world_investigation` | 11 |
| `abyssal_recovery` | 4 |
| `stellaris_space_industrialization` | 4 |

Quests gated on craftless items that only drop from structure loot. **An earlier
session recorded that most Old World structures never generate.** That was not
verifiable in this session's runs — the probe failure left
`structureStartsByNamespace` empty — so treat it as unconfirmed. If it is true,
these are not warnings, they are hard blocks, and this workstream jumps the
queue.

**Verify first** (needs W0), then apply open decision 1 in
`QUEST_TREE_COHERENCE_AUDIT.md` §5: register the evidence items with guaranteed
loot pools, or rewrite the quests as pure `structure` visits.

### W5 — visual coherence *(Tranche D, do last)*

21 `backward-dependency-line` (worst: `darknet_draconic_convergence` 4,
`era_08_infinite_domain` 4, `era_01_mechanical_reconstruction` 3) and 7
`non-legend-shape` chapters. Cosmetic; gated on open decision 2 (adopt `rsquare`
into the legend, or replace it).

### Not defects

- **602 `acquisition-unverified` (info)** — inherent to a 9,891-task catalogue.
  Do not try to drive this to zero.
- **38 `chapter-icon-missing`, 39 `recipe-coverage-gap`, 34
  `project-item-unverified`** — informational; triage only if a chapter is being
  touched anyway.

## Decisions still owed by the owner

Blocking, from `QUEST_TREE_COHERENCE_AUDIT.md` §5 — unchanged and still open:

1. **Abyssal evidence items** (blocks W4): create the seven `kubejs:` items with
   guaranteed structure loot, or rewrite those quests as `structure` visits?
2. **`rsquare` shape** (blocks W5): adopt into the legend as "commissioning /
   milestone sub-node", or replace with gear/octagon?
3. **Stellaris chapter**: annex of Era 7, or standalone specialization?
4. **Old World Investigation**: bind to an era, keep as an always-available
   parallel track, or leave to the queued `old_world_narrative` package?
5. **Era 1 rebuild**: normalize in place, or regenerate from a reconciled
   generator?

W1, W2, and W3 need none of these and can start immediately.

## Toolchain gotchas

- `benchmark_runs/**/server-console.log` is **UTF-16**. Decode explicitly or
  greps silently return nothing.
- Piping `run_worldgen_benchmark.ps1` into another command **masks its exit
  code** — a run can print a stack trace and still report 0. Check for the
  `benchmark_started` marker, or `Expected one benchmark_started marker, found 0`.
- A smoke run takes ~5 minutes and leaves evidence in
  `benchmark_runs/<batch>/<run>/result.json`. `-KeepRuntime` retains the runtime,
  whose `config/` is a real copy — that is the safe way to observe what the
  running game does to config files without risking the working tree.
- The `dev/` restructure broke path resolution in many scripts. Python tooling
  uses `parents[2]`; if a script fails to find `mods/` or `config/`, check its
  root resolution before assuming a deeper problem.

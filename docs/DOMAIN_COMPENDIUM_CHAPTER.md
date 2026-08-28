# Domain Compendium Chapter — Authority Document

*Created 2026-08-27. Governs the "collect one of every obtainable item and block"
FTB Quests chapter and the deterministic tooling that produces it.*

## 1. Purpose

A single optional FTB Quests chapter — the **Domain Compendium** — that contains
one non-consumptive `item` task for (close to) every item and block in the pack
that a player can actually obtain and that renders with a real texture. It is a
completionist catalogue, not a progression path: nothing depends on it and it
gates nothing.

The player-facing promise is: *if it has a recipe or an obtainment method and it
is not a broken phantom, it is in the Compendium.*

## 2. Authority & precedence

| Rank | Source | Scope |
|---|---|---|
| 1 | This document | Compendium chapter contents, scope rules, structure |
| 2 | `docs/registry-inventory/` | The registered item/block id truth set |
| 3 | `docs/progression-graph/` | Obtainment-route evidence (recipe / loot / worldgen) |
| 4 | Loaded resource assets (mod jars + `kubejs/assets` + enabled packs) | Texture-resolution truth |
| 5 | `docs/MOD_QUEST_COVERAGE_AUDIT.md` | Superseded **only** for this chapter (see §3) |

### 3. Relationship to the Mod Quest Coverage Audit

`docs/MOD_QUEST_COVERAGE_AUDIT.md` states that decorative / cosmetic palettes
(Rechiseled, Rechiseled Create, decorative Quark / Supplementaries, Bells &
Whistles) should feed optional design contracts and that "requiring dozens of
cosmetic variants would create checklist fatigue without teaching a system."

That judgement still holds for the **progression and specialization chapters**.
The Domain Compendium is the deliberate exception: it is the one place where
exhaustive breadth is the point. The coverage audit is not violated, it is
scoped — no era/threat/specialization chapter gains cosmetic checklists as a
result of this work.

## 4. Status

- **Audit tooling: LIVE.** `scripts/audit_domain_compendium_candidates.py`
  produces the candidate inventory (§6). Runs in ~2 s, no live instance needed.
- **Chapter generator: LIVE.** `scripts/generators/build_domain_compendium_chapter.py`
- **Chapter validator: LIVE.** `scripts/audit_domain_compendium_chapter.py`
  (exact-coverage check against the candidate CSV) — **passing**.
- **Chapter file: GENERATED 2026-08-27.**
  `config/ftbquests/quests/chapters/domain_compendium.snbt` — 85 sections,
  305 section quests, **9,999 item tasks**, root + capstone. 1.30 MB.
- **Peer validators:** `scripts/audit_quest_tree_coherence.py` → 0 critical,
  0 warning from this chapter (550 `info` acquisition-unverified are inherent to
  a 10 k catalogue, see §5.1). `scripts/audit_ftbquests.js` → all-zero for
  `domain_compendium.snbt`.
- **NOT yet verified in a running client** — see §11 (quest-book size risk).

### 4.1 Validator allow-list entries added for this chapter

| File | Entry | Why |
|---|---|---|
| `scripts/audit_quest_tree_coherence.py` | `CATALOGUE_FILES = {"domain_compendium"}`; capstone id in `STARTER_CHECKMARK_ALLOW` | optional catalogue: root/capstone checkmarks are `info`, capstone emblem is earned behind 305 quests |
| `scripts/audit_ftbquests.js` | capstone id in `starterCheckmarkRewards` | same |

## 5. Definitions and tests

### 5.1 "Obtainable"

An id is *obtainable* if `docs/progression-graph/graph-edges.csv` records it as
the target of a `recipe_output`, `loot`, or `worldgen_block` edge.

Known limits (documented, not bugs):

- The graph is built from statically declared JSON. Code-only recipes, some
  mod-specific recipe types (Create sequenced assembly outputs, a subset of AE2
  and vehicle-mod shaped recipes), villager/wandering-trade stock, and
  runtime-expanded tags are **not** all captured. Obtainability is therefore a
  *lower bound* — some `review`-bucket items are in fact craftable.
- For that reason the primary include gate is **texture resolution** (§5.2),
  with obtainability used to sort and to justify exclusions, not as a hard veto
  except where a namespace is entirely creative/technical.

### 5.2 "Textured"

For `ns:name`, resolve the item model `assets/ns/models/item/name.json` (and, for
blocks, `assets/ns/models/block/name.json`), walking the `parent` chain and
merging `textures` maps. Every concrete (non-`#`) texture reference must resolve
to an existing `assets/<tns>/textures/<path>.png` in the loaded asset set:

- every `mods/*.jar`
- the vanilla client jar (`Install/versions/1.21.1/1.21.1.jar`)
- `kubejs/assets/`
- resource packs enabled in `options.txt` that exist on disk
  (`resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1.21.1.zip`)

Verdicts: `yes` (all concrete refs exist), `no` (a ref is missing — renders
broken), `unknown` (model has no static texture, or no model file — usually
blockstate-only or runtime-generated; **not** auto-included).

Known limit: the runtime `moonlight:merged_pack` dynamic resource pack cannot be
scanned statically, so a small number of Supplementaries/Moonlight blocks may
read as `unknown` when they are in fact fine. These land in `review`.

## 6. Candidate inventory (generated 2026-08-27)

Source: `docs/domain-compendium/candidate-inventory.csv` (one row per id),
`docs/domain-compendium/candidate-summary.txt`,
`docs/domain-compendium/allthecompressed-families.csv`.

| Measure | Count |
|---|---:|
| Registered ids (items ∪ blocks) | 17,277 |
| With an obtainment route | 15,047 |
| Texture resolves (`yes`) | 15,434 |
| Texture broken (`no`) | 982 |
| Texture `unknown` | 861 |
| **`include` (textured + obtainable)** | **13,865** |
| `review` (textured, obtainment unproven — mostly graph gaps) | 1,788 |
| `exclude` (broken texture, or no route and unverified) | 1,624 |

### 6.1 AllTheCompressed

199 material families × 9 tiers = 1,791 blocks (+3 misc). **103 families
resolve** their base texture → **927 tier blocks valid**, 864 are phantoms whose
base mod is absent (`alltheores`, `allthemodium`, `aoa3`, `enderio`, `powah`,
`megacells`, `productivebees`, `xycraft`, `extendedae`, `forbidden_arcanus`,
`pneumaticcraft`, `allthetweaks`). The 103 count matches
`docs/compression-audit/` independently.

### 6.2 Ex Deorum sieves

67 sieve entries (`<wood>_sieve`, `<wood>_compressed_sieve`, `mechanical_sieve`).
**23 valid** — every installed wood (oak, spruce, birch, jungle, acacia,
dark_oak, crimson, warped, mangrove, cherry, bamboo) plus the mechanical sieve.
44 excluded — Blue Skies, Biomes O' Plenty, Ars Nouveau, Aether, Twilight woods
that are not installed. These are the "sifters requiring wood types that don't
exist."

### 6.3 Largest included namespaces

| Namespace | `include` | Note |
|---|---:|---|
| rechiseled | 3,628 | chisel re-texture variants — **open decision #1** |
| minecraft | 1,218 | |
| more_ores_more_gems | 1,064 | ~40 materials × block/ore/raw/tool/armor |
| allthecompressed | 930 | 103 families × 9 + 3 |
| quark | 760 | |
| create | 664 | |
| tfmg | 542 | |
| immersiveengineering | 470 | |
| rechiseledcreate | 242 | chisel variants — **open decision #1** |

Full table in `docs/domain-compendium/candidate-summary.txt`.

## 7. Scope policy

Per-namespace policy, applied by the generator from a table it prints on every
run. Three values:

- `full` — every `include` id becomes a task (default)
- `collapsed` — reserved for a future "one representative per family" mode
- `excluded` — the namespace contributes nothing

Default: **every namespace `full`.** Deviations require an entry here.

| Namespace | Policy | Reason |
|---|---|---|
| `rechiseled` | `excluded` | Decision 1 — chisel re-texture variants (3,628) |
| `rechiseledcreate` | `excluded` | Decision 1 — chisel re-texture variants (242) |
| *(all others)* | `full` | |

Items in `review` / `exclude` are never emitted. Fixing a graph gap that moves an
id into `include` is the way to add it, not a manual override list.

## 8. Decisions (owner, 2026-08-27)

| # | Decision | Ruling |
|---|---|---|
| 1 | Rechiseled + Rechiseled Create (3,870 ids) | **Excluded** (`EXCLUDED_NAMESPACES` in the generator). A future `collapsed` mode may add one entry per base block. |
| 2 | The `review` items (graph gaps, e.g. some AE2 parts recovered by the §5.2 fix; others still unproven) | **Ship without them.** Close gaps per namespace; an id enters the chapter automatically when the audit promotes it to `include`. |
| 3 | Chapter grouping | **Own group** `7C0DEC0FFEE00001` "Domain Compendium". |
| 4 | Task granularity | **One task per id, 40 per quest.** 305 section quests. |
| 5 | Task behaviour | **Consume items** (`consume_items: true`). Civilisation-scale sink, same spirit as the Mastery chapters. Capstone grants `kubejs:ultima_collection_emblem` (previously an unused orphan item). |

Result: **9,999 catalogued ids.**

## 9. Chapter structure (as built)

- Chapter id `7C0DE0C000000000`, filename `domain_compendium`, group
  `7C0DEC0FFEE00001`, `order_index: 0`.
- `default_hide_dependency_lines: true`, `default_quest_shape: "rsquare"`.
- **Root** `7C0DE0C000000001` — octagon at `(0, 0)`, `optional: true`, checkmark
  ("Open the Compendium"). Every section depends on it; being at the chapter's
  top edge with dependents makes the coherence analyzer read it as an
  orientation node.
- **Sections** `7C0DE1<10-hex index>` — one column per namespace
  (`x = column * 2.0`), ordered by `include` count descending then name. Each
  section quest: `optional: true`, `shape: "rsquare"`, `size: 0.75`, up to 40
  `consume_items: true` `count: 1` `item` tasks with sorted ids, titled
  `"<Mod Name>"` or `"<Mod Name> <n>"` when a namespace spans several. Task ids
  `7C0DE2<10-hex index>`.
- **Capstone** `7C0DE0C0000000FF` — octagon below the tallest column,
  `optional: true`, depends on **every** section quest, grants
  `kubejs:ultima_collection_emblem`.
- IDs are a deterministic function of the running index, so regeneration is a
  clean diff. Lang keys are spliced into `en_us.snbt` between
  `# --- BEGIN/END domain_compendium (generated) ---` markers.

## 10. Determinism & regeneration

1. `python scripts/build_mod_index.py` (only if mods changed)
2. `python scripts/audit_domain_compendium_candidates.py`
3. `python scripts/generators/build_domain_compendium_chapter.py`
4. `python scripts/audit_domain_compendium_chapter.py` (must pass)
5. `python scripts/audit_quest_tree_coherence.py` (0 critical, no new warning)
6. `node scripts/audit_ftbquests.js` (all-zero for `domain_compendium.snbt`)

Steps 2–4 are pure functions of the registry export, the progression graph, the
loaded assets, and the §7 policy table. No step needs a running game.

If `scripts/generators/generate_eras_2_8.js` or `generate_mastery_quests.js` is
re-run afterwards they rewrite `en_us.snbt` wholesale — re-run step 3 to
re-splice the compendium lang block.

## 11. Risks

| Risk | Mitigation |
|---|---|
| 10k+ tasks bloat the quest book / client sync | Measure SNBT size + in-game load after generation; decision #1 removes ~28% |
| Graph gaps silently drop craftable items | `review` CSV is reviewed per namespace; §5.1 states it is a lower bound |
| `moonlight:merged_pack` dynamic textures read as `unknown` | Documented; affected ids listed in the `review` CSV for manual promotion |
| AllTheCompressed / Ex Deorum add a base mod later | Re-run the audit; families move `include` automatically |
| A later `generate_eras_*` run clobbers shared lang | Generator appends its own lang block with fenced markers; validator checks it survives |

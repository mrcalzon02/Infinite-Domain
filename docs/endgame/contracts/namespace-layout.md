# Endgame — namespace and layout contract

**Authority:** `docs/Endgame.md` §5.5 and checkpoint `EG-P00-S05-C0009`.
**Status:** ACCEPTED 2026-08-27. This fixes the file tree, the datapack-vs-module
boundary, and generated-output ownership so Phase 1 has no unresolved layout decision.

Depends on: C0003 (namespace token `hive_world`), C0005 (four-layer architecture),
C0006 (height contract).

## 1. Namespace and token

- Registry namespace: **`infinite_domain`** (the pack's existing own namespace).
- Path / registry token for all Hive content: **`hive_world`** — either the directory
  `hive_world/` or the prefix `hive_world_`.
- Dimension ID: `infinite_domain:hive_world` (permanent).
- Companion mod ID: **`infinite_domain_hive`** (follows the `infinite_domain_*` mod-ID
  convention from `PROJECT_INDEX.md`).
- Player-facing strings never contain the substring `hive` (C0003).

## 2. Datapack tree (in `kubejs/data/`, matching the rest of the pack)

```
kubejs/data/infinite_domain/
  dimension/hive_world.json                         # generated (…generate_hive_world_biome_routing.py)
  dimension_type/hive_world.json                    # hand-authored
  worldgen/
    noise_settings/hive_world.json                  # generated (scripts/endgame/generate_hive_world_noise.py)
    density_function/hive_world/*.json               # generator-partitioned density + biome routing fields
    biome/hive_world_*.json                          # generated (…generate_hive_world_biomes.py)
    configured_feature/hive_world/*.json             # generated
    placed_feature/hive_world/*.json                 # generated
    structure/hive_world/*.json                      # generated (JSON structure defs)
    structure_set/hive_world/*.json                  # generated
    template_pool/hive_world/*.json                  # generated
    processor_list/hive_world/*.json                 # generated
  tags/worldgen/biome/hive_world*.json               # generated
  structure/hive_world/*.nbt                         # hand-authored or NBT-tool output (never under worldgen/)
```

- **No `world_preset` entry.** The Hive is entered by the travel mechanic only, never
  routed through `minecraft:worldgen/world_preset/*`.
- **No shared-file overrides.** The Hive datapack must not modify, override, or add to
  any `minecraft:`, `wastelands:`, or `gradient_ocean_pack` worldgen file. The Hive has
  its own `noise_settings` and biome source and touches nothing shared. This keeps the
  unresolved `gradient_ocean_pack` ownership conflict (C0001 defect 5) entirely out of
  the Hive's scope.
- **No binary NBT under a JSON registry path.** JSON structure defs go under
  `worldgen/structure/hive_world/`; binary templates go under `structure/hive_world/`.
  (The misplaced `worldgen/structure/nether/lyran_research.nbt`, C0001 defect 4, stays
  on the clean-baseline list and is not a Hive file.)

## 3. Prototype scripts (Phase 1 only)

```
kubejs/server_scripts/hive_world_expedition.js       # reversible entry/return prototype (C0019)
kubejs/server_scripts/hive_world_atmosphere_proto.js # data-only exposure prototype (C0018 fallback), only if used
```

These are **disposable**. Nothing critical remains in KubeJS past Phase 1 — the
companion module takes over travel transactions and hazard state (C0002:
"Phase 1 data-only; critical logic in companion module"). `EG-P01-S06-C0023` proves
removal.

## 4. Companion module (Phase 5+ — NOT built in Phase 0/1)

```
packdev/hive-world-companion/
  settings.gradle  build.gradle  gradle.properties   # pinned NeoForge Gradle module
  src/main/java/infinitedomain/hive/…
  src/main/resources/META-INF/neoforge.mods.toml     # modId infinite_domain_hive
scripts/build_hive_world_companion.ps1               # portable: parametrised paths, NO destructive in-place jar replace
```

Per C0002 clean-baseline prerequisite 7, this module uses a pinned Gradle NeoForge
build. It does **not** copy the existing `scripts/build_*.ps1` pattern unchanged
(hardcoded JDK/library paths, destructive `Remove-Item` of installed jars). Its build
script writes to a build directory and the operator installs the artifact explicitly.

## 5. Docs, generators, validators, evidence

```
docs/endgame/
  adr/ADR-*.md
  identity/placeholder-terms.md
  contracts/*.md
  test-strategy.md
  phase-1-backlog.md
  generated-output-manifest.json      # every generated file -> its one generator
  evidence/<checkpoint-id>/…           # screenshots, spark reports, log excerpts, validator output
scripts/endgame/
  generate_hive_world_*.py             # one authoritative generator per generated family
  validate_hive_world_smoke.py
  validate_hive_world_*.py
saves/Infinite Domain - Hive World QA/ # gitignored QA world
```

## 6. Generated-output ownership

`docs/endgame/generated-output-manifest.json` is the single index. Every file under a
"generated" path in §2 has exactly one `generator` entry. Hand-authored files
(`dimension_type/hive_world.json`, arrival NBT, and authored band modules) are listed
with `"generator": null` and `"hand_authored": true`. Manual edits to generated files
are forbidden (`docs/Endgame.md` §17.3); regenerate instead.

## 7. Collision and repository-scope check

| Check | Result |
|---|---|
| `hive_world` registry-path collision inside `infinite_domain:` | none — only the uncommitted `docs/hive-strain/` scratch and `scripts/build_hive_strain_roster.py` use the string, both docs-only, no registry object |
| Overlap with `gradient_ocean_pack` / shared worldgen | none — Hive owns a separate dimension, its own noise settings, and adds nothing to any preset (§2 rule) |
| Binary-NBT-in-JSON-path repeat of C0001 defect 4 | prevented — §2 separates `structure/hive_world/*.nbt` from `worldgen/structure/hive_world/*.json` |
| `datapacks/` slot vs. `kubejs/data/` | Hive uses `kubejs/data/` like the rest of the pack (`PROJECT_INDEX.md`); `datapacks/` stays unused |
| Distribution scope | all Hive content is original and tracked; QA world and `build/` dirs are gitignored |
| Mod-ID convention | `infinite_domain_hive` matches the seven existing `infinite_domain_*` mod IDs |

## 8. Deferred

Exact per-file names inside each generated family → the Phase 1 backlog (C0011) and the
subsystem checkpoints. The companion module's internal package layout → `EG-P05-S02`.

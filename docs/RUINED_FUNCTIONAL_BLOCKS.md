# Ruined Functional Block Policy

## Why this exists

The 2026-08-19/20 structure-corpus review found live, working modded machinery placed as
set dressing — most severely `createnuclear:reactor_core`/`reactor_casing`/`reactor_frame`
(6,224 combined placements across just two structures) and heavy `create:fluid_tank`,
`immersiveengineering:capacitor_mv/hv`, and `ae2:controller` usage. A player who mines any
of that out of a ruin skips the entire technology chain those blocks are supposed to gate.
Vanilla progression blocks placed as plain, working furnaces have the same problem on a
smaller scale. This is a hard rule going forward, not a style preference.

## The rule

1. **Vanilla-first.** Structure massing, walls, floors, and roofing use vanilla or already
   LAST-DAYS-authored blocks by default. Modded blocks are the exception and need a reason.
2. **No live-functional blocks as set dressing, ever.** A structure must never place a real
   working furnace/smoker/blast furnace, a real modded machine, tank, capacitor, controller,
   or reactor component purely for visual flavor. If a scene calls for "this room has a
   furnace" or "this was a reactor room," it gets the **decorative** equivalent, never the
   real block.
3. **Ruined-equivalent blocks are the required stand-in** wherever one exists (see below).
   Where no ruined-equivalent exists yet for a given machine family, use a vanilla proxy
   (iron block, chiseled stone, scaffolding, etc.) as a temporary stopgap and flag it in the
   structure's review notes — it is not a silent permanent substitute.
4. **This is retroactive.** Every one of the 94 structures in the QA gallery gets re-passed
   through this rule; automated gates that were green under the old policy do not carry
   forward as approval.

## The Ruined Functional Block set (implemented 2026-08-23)

Three new decorative blocks exist under the `infinite_domain` namespace:

| Block | Replaces | Recycling recipe |
|---|---|---|
| `infinite_domain:ruined_furnace` | `minecraft:furnace` | → 2× `wastelands:scrap_metal` |
| `infinite_domain:ruined_smoker` | `minecraft:smoker` | → 2× `wastelands:scrap_metal` |
| `infinite_domain:ruined_blast_furnace` | `minecraft:blast_furnace` | → 4× `wastelands:scrap_metal` |

Each one is visually a normal furnace/smoker/blast furnace with a damage overlay
(soot, cracks, rust bleed) layered on top, mineable and placeable like any block, but has
**no block entity, no GUI, no smelting behavior** — it is purely decorative. It can be
recycled into scrap via a shapeless crafting recipe.

### How the look stays texture-pack compatible

The block model references the live vanilla texture IDs directly (`minecraft:block/furnace_top`,
`_side`, `_front`, and `smoker`'s distinct `_bottom`) rather than a baked copy, with a second,
slightly-inset cube element layering `infinite_domain:block/ruin_overlay/damage_generic` (or
`damage_scorched` for the blast furnace) on top. Whatever resource pack supplies the base
furnace textures — including the active LAST DAYS conversion — is what these blocks show
underneath the damage. If LAST DAYS re-authors the furnace textures later, the ruined
variants update automatically; nothing here needs to be touched.

### Implementation

- `kubejs/startup_scripts/ruined_functional_blocks.js` — registers all three via KubeJS's
  `cardinal` block type (the same type KubeJS documents for furnace/lectern-style
  horizontal-facing blocks), hardness/resistance matched to vanilla furnace (3.5/3.5),
  stone sound, pickaxe-required.
- `kubejs/assets/infinite_domain/{blockstates,models}/ruined_*.json` — hand-authored so
  KubeJS's dev-asset auto-generation never overwrites them; the startup script deliberately
  never calls `.model()`/`.texture()`/`.textureAll()`.
- `kubejs/assets/infinite_domain/textures/block/ruin_overlay/*.png` — the two overlay
  textures, 16×16 to match vanilla's native resolution.
- `kubejs/server_scripts/ruined_functional_blocks_recipes.js` — the scrap recipes.

**Needs a restart, not `/reload`.** Custom block registration only takes effect on a full
client/server relaunch (this is a KubeJS constraint, same as the vanilla-placeholder-tools
rule already documented in `docs/VANILLA_PLACEHOLDER_TOOLS.md`). After restarting, sanity
check in Creative: block renders correctly on all four `facing` rotations, item icon looks
right in inventory, breaking it with a pickaxe drops itself, and the scrap recipe resolves
in JEI/REI.

## Backlog

- Only furnace/smoker/blast furnace exist so far. The block-fitness audit
  (`docs/structure-block-fitness-audit.json`) lists the next highest-volume offenders that
  need their own ruined-equivalent before any structure using them can pass:
  `create:fluid_tank` (6,964 placements), `createnuclear:reactor_casing`/`reactor_core`/
  `reactor_frame` (6,224 combined — `nuclear_research_annex` cannot pass review until this
  exists), `immersiveengineering:capacitor_mv`/`capacitor_hv` (4,291 combined), and
  `ae2:controller` (1,961).
- Until a family's ruined-equivalent exists, its structures stay on the vanilla-proxy
  stopgap and stay blocked from production approval either way.

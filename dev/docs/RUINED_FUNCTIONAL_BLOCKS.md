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

## The Ruined Functional Block set (implemented 2026-08-23, expanded 2026-08-26)

Eighteen inert decorative blocks are registered by KubeJS under the `kubejs`
namespace:

| Block | Replaces | Recycling recipe |
|---|---|---|
| `kubejs:ruined_furnace` | `minecraft:furnace` | → `wastelands:scrap_metal` |
| `kubejs:ruined_smoker` | `minecraft:smoker` | → `wastelands:scrap_metal` |
| `kubejs:ruined_blast_furnace` | `minecraft:blast_furnace` | → `wastelands:scrap_metal` |
| `kubejs:ruined_stonecutter` | `minecraft:stonecutter` | → `wastelands:scrap_metal` |
| `kubejs:ruined_smithing_table` | `minecraft:smithing_table` | → `wastelands:scrap_metal` |
| `kubejs:ruined_grindstone` | `minecraft:grindstone` | → `wastelands:scrap_metal` |
| `kubejs:ruined_cartography_table` | `minecraft:cartography_table` | → `wastelands:scrap_metal` |
| `kubejs:ruined_fletching_table` | `minecraft:fletching_table` | → `wastelands:scrap_metal` |
| `kubejs:ruined_loom` | `minecraft:loom` | → `wastelands:scrap_metal` |
| `kubejs:ruined_lectern` | `minecraft:lectern` | → `wastelands:scrap_metal` |
| `kubejs:ruined_brewing_stand` | `minecraft:brewing_stand` | → `wastelands:scrap_metal` |
| `kubejs:ruined_composter` | `minecraft:composter` | → `wastelands:scrap_metal` |
| `kubejs:ruined_cauldron` | empty/water/lava/powder-snow cauldrons | → `wastelands:scrap_metal` |
| `kubejs:ruined_crafting_table` | `minecraft:crafting_table` | → `wastelands:scrap_metal` |
| `kubejs:ruined_anvil` | intact/chipped/damaged anvils | → `wastelands:scrap_metal` |
| `kubejs:ruined_campfire` | `minecraft:campfire` | → `wastelands:scrap_metal` |
| `kubejs:ruined_soul_campfire` | `minecraft:soul_campfire` | → `wastelands:scrap_metal` |
| `kubejs:ruined_enchanting_table` | `minecraft:enchanting_table` | → `wastelands:scrap_metal` |

Each one derives its visual identity from the matching vanilla workstation, is mineable and
placeable like any block, but has **no block entity, no GUI, and no workstation behavior** —
it is purely decorative. It can be recycled into scrap via a shapeless crafting recipe.

### How the look stays texture-pack compatible

A hand-authored decal overlay (soot/cracks/rust bleed baked as a separate 16×16 texture,
layered on an inset cube) was tried first and rejected — it clashed badly with any resource
pack that reskins the base furnace at a different resolution or art style (see the 2026-08-25
screenshot review). The block model now simply sets `"parent"` to the vanilla block model
directly (`minecraft:block/furnace`, `minecraft:block/smoker`, `minecraft:block/blast_furnace`)
with no textures or extra elements of its own. Whatever resource pack reskins the vanilla
block — including the active LAST DAYS conversion — reskins the ruined variant identically,
automatically, with zero custom texture assets to keep in sync.

### Implementation

- `kubejs/startup_scripts/ruined_worldgen_furnaces.js` — authoritative registry index for
  all eighteen inert blocks and their supported orientation properties.
- `kubejs/client_scripts/ruined_worldgen_assets.js` — generates the KubeJS-namespace
  blockstates and crack-overlay models for the expanded workstation family.
- `kubejs/server_scripts/ruined_functional_blocks_recipes.js` — the scrap recipes.
- `scripts/audit_ruined_functional_blocks.py` — audits/remediates terrestrial surface NBT
  and converted Lost Cities palettes, validates its targets against the KubeJS index, and
  writes `docs/ruined-functional-block-structure-audit.json` on `--apply`.

**Needs a restart, not `/reload`.** Custom block registration only takes effect on a full
client/server relaunch (this is a KubeJS constraint, same as the vanilla-placeholder-tools
rule already documented in `docs/VANILLA_PLACEHOLDER_TOOLS.md`). After restarting, sanity
check in Creative: block renders correctly on all four `facing` rotations, item icon looks
right in inventory, breaking it with a pickaxe drops itself, and the scrap recipe resolves
in JEI/REI.

## Gate coverage correction (2026-08-24)

The gate this policy relies on, `scripts/audit_structure_block_fitness.py`,
was not enforcing rule 2 as written. It missed on two independent axes at
once:

1. **Scan path.** `STRUCTURES` was pinned to
   `kubejs/data/infinite_domain/structure/wasteland`, so the deep-sea corpus —
   which is authored, ships modded blocks, and is covered by this policy —
   was never inspected at all.
2. **Vanilla blocks.** The sweep only considers blocks whose namespace is not
   `minecraft:`, so a live vanilla furnace/smoker/blast furnace placed as set
   dressing could never be flagged, even inside the scan path. Rule 2 names
   those blocks explicitly.

Together those meant seven live `minecraft:blast_furnace` placements sat in
the deep-sea corpus while the gate reported green: `coastal_patrol_wreck`
(three variants), `abyssal_mining_rig` (two variants), and the Wave 3
`akula_project971` turbine room (two). All are now
`kubejs:ruined_blast_furnace`.

Fixed by rooting `STRUCTURES` at the whole `structure/` tree and adding an
explicit `VANILLA_FORBIDDEN` set covering the blocks rule 2 names. The report
now records `categories_scanned` so a future corpus added outside the scan
path is visible rather than silent. **This change is syntax-checked only** —
running it requires the vanilla jar and `mods/`, which the session that made
it could not execute against; run it once on a machine that has them before
treating the gate as trustworthy again.

## Backlog

- The block-fitness audit (`docs/structure-block-fitness-audit.json`) lists the next
  high-volume *modded machine* offenders that still need their own ruined-equivalent before
  any structure using them can pass:
  `create:fluid_tank` (6,964 placements), `createnuclear:reactor_casing`/`reactor_core`/
  `reactor_frame` (6,224 combined — `nuclear_research_annex` cannot pass review until this
  exists), `immersiveengineering:capacitor_mv`/`capacitor_hv` (4,291 combined), and
  `ae2:controller` (1,961).
- Until a family's ruined-equivalent exists, its structures stay on the vanilla-proxy
  stopgap and stay blocked from production approval either way.

# Endgame — module and connector schema (P04 candidate)

**Authority:** `docs/Endgame.md` §2.7 (structures own legibility), §2.8 (dark mineral
masonry); `docs/endgame/adr/ADR-0001`; `docs/endgame/contracts/massing-contract.md`.
**Status:** authored 2026-08-27 by owner direction, ahead of Phase 4. Formally adopted
as `EG-P04-S01-C0051` (module schema) + `EG-P04-S01-C0052` (connector validator) when
Phase 4 opens.
**Validated by:** `scripts/endgame/validate_hive_world_modules.py` (the connector
validator) against `docs/endgame/hive-world-module-manifest.json`.

Every Hive structure module obeys this contract so the jigsaw grammar assembles
predictably into traversable, legible architecture stamped into the solid mass.

---

## 1. Authoring coordinates

- A module is a single `minecraft:single_pool_element` NBT with `projection: rigid`.
- **Local origin** `(0,0,0)` is the module's minimum corner.
- **Floor blocks** sit at local `Y = 0`. The **walkable floor datum** is local `Y = 1`.
- Footprint `<= 48 x 48`, height `<= 32` for the spike (the `performance-budget.md`
  hard cap is `128 x 128 x 96`).
- `<= 6` block entities, `<= 48,000` non-air blocks, `<= 2 MB` NBT per module.
- A module carries a `band` in its manifest entry; its palette (§5) must match.

## 2. Connector types

The jigsaw-block `name`/`target` vocabulary. Connecting connectors must have **equal
type**, **opposite facing**, and **equal local floor datum**.

| Type | `name` = `target` | Opening (w x h, air) | `joint` | Use |
|---|---|---|---|---|
| `door` | `infinite_domain:hive_world/door` | 1 x 3, floor at connector datum | `aligned` | standard pedestrian join |
| `hall` | `infinite_domain:hive_world/hall` | 3 x 4, floor at connector datum | `aligned` | monumental / transit / bay mouths |
| `service` | `infinite_domain:hive_world/service` | 1 x 2, floor at connector datum | `aligned` | cramped crawl / duct routes (Drown, Underworks) |

- **`joint`** is `aligned` on every connector **except** a module with exactly **one**
  connector (a leaf), which may use `rollable`.
- The jigsaw block sits **in the opening**, centred on its width, at local
  `Y = <connector floor datum>`, `orientation` = the direction it faces (outward from
  the module).
- `final_state`:
  - open connector -> `minecraft:air`;
  - a **bulkhead** terminal module -> `minecraft:chiseled_polished_blackstone`
    (the connector seals when nothing attaches).

## 3. Connector floor datum

- A **level module** (all connectors on one storey): every connector's local Y is the
  same value, the module's single floor datum.
- A **transition module** (bridges two bands): it has a **low** connector at one floor
  datum and a **high** connector at another; the module internally provides the climb
  (stairs or ladder). Its manifest `role` is `transition` and the two data are declared.
- No connector may sit where a player cannot stand: `>= 3` blocks of headroom
  (`>= 2` for `service`) and `>= 1` block of walkable floor leading into the opening on
  the module side.

## 4. Roles and pools

| `role` | Connectors | Appears in pool | Notes |
|---|---|---|---|
| `start` | `>= 3` | `start` only (exactly one element) | the district origin (`transit_hub`) |
| `branch` | `>= 2` | `branch` | corridors, bays, transition modules |
| `leaf` | exactly `1`, `pool: minecraft:empty` | `branch` | rooms with one entrance |
| `terminal` | `1`, `pool: minecraft:empty`, `final_state` seals | `terminal` only | bulkhead caps |

Pool contract:

- `start`: exactly one element, `fallback: minecraft:empty`.
- `branch`: `>= 3` weighted elements, `fallback: infinite_domain:hive_world/terminal`.
- `terminal`: one or more bulkheads, `fallback: minecraft:empty`.
- Every connector's `pool` is a real pool ID **or** `minecraft:empty`.
- `size` (jigsaw recursion depth) is set on the structure, not the modules; spike = 6.

## 5. Palette binding (dark mineral masonry, §2.8)

| Band | Structural shell | Floor / trim | Detail / ornament |
|---|---|---|---|
| The Drown | `deepslate`, `cobbled_deepslate` | `tuff`, `mud` accents | `deepslate_wall`, chains, iron bars (corroded read) |
| The Underworks | `cobbled_deepslate`, `deepslate_bricks` | `blackstone` | patched `polished_blackstone`, `deepslate_tiles` |
| The Furnace Tiers | `blackstone`, `polished_blackstone` | `deepslate_tiles` | `polished_deepslate`, iron bars, `chain`, machinery blocks |
| The Billet Decks | `polished_blackstone_bricks` | `polished_blackstone` | `chiseled_polished_blackstone`, slabs, `deepslate_brick_stairs` |
| The Vaulting | `polished_blackstone`, `polished_blackstone_bricks` | `chiseled_polished_blackstone` | columns, `polished_blackstone_wall`, arches |
| The Crown | `deepslate_bricks`, `deepslate_tiles` | `polished_deepslate` | `chiseled_deepslate`, `deepslate_tile_stairs` |

- No bright or predominantly metallic shell (§2.8). Metal (`iron_bars`, `chain`,
  `iron_block`) is a **detail accent**, never the primary material.
- Light sources are sparse and read as **failing fixtures**: `sea_lantern` set into
  ceilings/walls, never floods.

## 6. Required manifest (`docs/endgame/hive-world-module-manifest.json`)

Emitted by `generate_hive_world_structures.py`, one entry per module:

```json
{
  "id": "infinite_domain:hive_world/<name>",
  "nbt": "kubejs/data/infinite_domain/structure/hive_world/<name>.nbt",
  "size": [x, y, z],
  "band": "sump | works | vault | any",
  "role": "start | branch | leaf | terminal | transition",
  "floor_data": [1],
  "non_air": <int>,
  "block_entities": <int>,
  "connectors": [
    { "type": "door", "local_pos": [x, y, z], "facing": "north|south|east|west",
      "pool": "infinite_domain:hive_world/branch | minecraft:empty", "final_state": "minecraft:air" }
  ]
}
```

The connector validator asserts the manifest matches the NBT (every declared connector
is a real jigsaw block at that position/orientation, and vice versa).

## 7. Connector validator checks (`validate_hive_world_modules.py`)

1. NBT parses; `size`, `palette`, `blocks` well-formed; `DataVersion` = 3955.
2. Size and block/BE counts within §1 budget.
3. Every jigsaw block: `name` = `target` and in the §2 type set; `final_state` legal;
   `joint` legal for the module's connector count (§2).
4. The opening is carved: air of the type's `w x h` immediately in front of each
   jigsaw block, floor at the connector datum.
5. Floor-datum consistency (§3): a `level` module has one datum; a `transition` module
   declares two.
6. Headroom/clearance at every connector (§3).
7. `role` matches connector count and pool usage (§4); `leaf`/`terminal` have exactly
   one `minecraft:empty` connector.
8. Every connector `pool` resolves to a real pool file or is `minecraft:empty`; every
   pool `fallback` and element `location` resolves; `start`/`terminal` pools are used
   only by the right roles.
9. The manifest entry matches the NBT (declared vs. actual connectors).
10. Palette: every block in the module is in the §5 list for the module's `band`
    (or in the shared neutral set for `band: any`) — **warning, not failure**, until
    the per-band families land (`C0055`-`C0060`).

## 7a. Inherited block replacement

`generate_hive_world_structures.py` reuses `scripts/generate_wasteland_sites.py` for its
NBT writer and `Template` class, and therefore inherits that module's
`STRUCTURE_BLOCK_REPLACEMENTS` pass: functional blocks placed in a module are rewritten
to their `kubejs:ruined_*` equivalents (crafting table, furnace, anvil, …) and metal
grilles/fences to `minecraft:oxidized_copper_grate`. This is **kept** — it gives the
modules a derelict read for free and satisfies the intent of the inert-machine policy
(`EG-P04-S06-C0064`): no live production machinery ends up in set dressing. A
deliberate damage-state system (`EG-P04-S06-C0063`) supersedes this later.

## 8. Spike deviations from this schema

| Deviation | Modules | Closes at |
|---|---|---|
| No `band` tag / palette binding — all modules are generic `works`-ish | all 7 | `C0055`-`C0060` |
| `stair_shaft` uses a ladder, not authored stairs | `stair_shaft` | `C0054` |
| No `service` (crawlway) connector type used yet | — | `C0056` |
| Sizes not on a strict grid (13, 9, 13 etc.) | all | acceptable — schema uses connector alignment, not a grid |
| Only one `branch` pool — no per-band `branch` variants | pools | `C0065` (district assembly) |
| `industrial_bay` has 4 block entities near the manifest budget headroom | `industrial_bay` | monitor at `C0067` |

## 9. Rollback

Modules and pools are one generator (`generate_hive_world_structures.py`) plus one
structure + structure_set. Remove the structure_set -> the district stops generating;
the dimension is unaffected. The modules themselves are inert NBT.

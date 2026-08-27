# Endgame — height contract

**Authority:** `docs/Endgame.md` §3 and checkpoint `EG-P00-S03-C0006`.
**Status:** ACCEPTED 2026-08-27.

## Accepted initial contract

The `infinite_domain:hive_world` dimension uses the **proven vanilla envelope
`-64..319`**.

| Field | Value | Where |
|---|---|---|
| `min_y` | `-64` | `dimension_type/hive_world.json`, `noise_settings/hive_world.json` |
| `height` | `384` | same |
| `logical_height` | `384` | `dimension_type/hive_world.json` |
| top block Y | `319` | `min_y + height - 1` |
| `sea_level` | provisional `-40` (acid table in The Drown) | `noise_settings/hive_world.json`, refined at `EG-P03-S04-C0044` |

Rationale:

- The base pack already runs this exact envelope: `wastelands` noise settings use
  `min_y -64, height 384`; `cyberspace:darknet_dimension` runs `min_y -64, height 320`.
- Every downstream system (light engine, FTB Chunks claims and force-load, installed
  map/minimap mods, structure spread, mob spawn light checks, client render distance,
  fog, sky) is exercised at `-64..319` by the base pack today. No new compatibility risk
  is introduced.
- The six accepted bands (C0004) tile `-64..319` exactly (32 + 80 + 64 + 80 + 64 + 64 =
  384).

## Engine constraints recorded

Vanilla `DimensionType` codec bounds (1.21.1):

- `min_y` ∈ `[-2032, 2031]`, multiple of 16;
- `height` ∈ `[16, 4064]`, multiple of 16;
- `min_y + height ≤ 2032`;
- `logical_height ≤ height`.

`-64..319` (min_y −64, height 384) satisfies all four. A taller envelope is therefore
**engine-permitted**; the risk of going taller is downstream mod compatibility, not the
core codec. The Hive dimension type uses the plain vanilla `dimension_type` codec and
does **not** depend on Isekai for its bounds (the Isekai build-height report was
`runtime-unverified` in C0002 and is not on this path).

## Taller-world option — DEFERRED

A taller dimension is an optional later decision. It **may not be adopted** until a
dedicated taller-height compatibility checkpoint is seeded and passed. That checkpoint
is **not on the current critical path** and is only seeded if the owner requests a
taller Cinderstack. No `noise_settings` or `dimension_type` for the Hive may exceed
`height 384` before it passes.

### Adoption criteria (all required)

1. Light propagation correct at the new roof and the new floor (no black bands, no
   permanent darkness where skylight/none is expected).
2. Every Y-placement code path (jigsaw, features, the Hive macro planner, arrival
   platform math) respects the new bounds with no clamping or overflow.
3. FTB Chunks claim UI, claim persistence, and force-load correct across the full new
   range.
4. Installed map/minimap mods render the new vertical range without clipping or crash.
5. Mob spawn and light-level checks correct at the new extremes.
6. Client render distance, fog planes, and sky rendering not clipped at the new roof.
7. Entry arrival and return math correct for the new envelope.
8. No chunk-serialization, heightmap, or block-palette overflow; dedicated-server safe.

### Evidence method

Fixed-seed probe at roof, floor, sea level, and every band transition; relog;
region pregeneration; dedicated-server start and join; client log capture. Compare
against the `-64..319` baseline captured at `EG-P01-S05-C0021`.

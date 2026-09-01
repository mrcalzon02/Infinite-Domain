# Endgame — height contract

**Authority:** `docs/Endgame.md` §3 and checkpoint `EG-P00-S03-C0006`.
**Status:** REOPENED 2026-08-28 as `EG-P00-S03-C0006-R1`; owner-directed extended-height candidate. Runtime compatibility evidence remains required before production acceptance.

## Owner-directed candidate contract

The `infinite_domain:hive_world` dimension targets **`-64..607`**. Minecraft requires
the configured height to be a multiple of 16, so the legal value is `672`: 64 blocks
below the Y0 planetary surface and 608 blocks above it. This approximately doubles the
former Y0-to-roof build space while keeping Y0 as an intuitive world datum.

| Field | Value | Where |
|---|---|---|
| `min_y` | `-64` | `dimension_type/hive_world.json`, `noise_settings/hive_world.json` |
| `height` | `672` | same |
| `logical_height` | `672` | `dimension_type/hive_world.json` |
| top block Y | `607` | `min_y + height - 1` |
| planetary surface datum | `Y 0` | dead-waste terrain and Spire bases meet here |
| `sea_level` | `0` | acid seas use the same datum; refined at `EG-P03-S04-C0044` |

Rationale:

- The former `-64..319` contract remains the proven rollback envelope.
- `height 600` itself is codec-invalid because height must be divisible by 16. `672`
  is the nearest legal envelope that supplies approximately 600 blocks above Y0.
- The dead wastes occupy a comparatively thin 64-block planetary layer from Y-64 to
  Y0. Stack masses begin at the Y0 surface datum and may rise through the remaining
  608 blocks.
- Every downstream system (lighting, claims, maps, structures, mobs, client render,
  fog, sky, serialization, portals) must now be re-proven across the extended range.
- The six revised bands tile `-64..607` exactly (64 + 96 + 112 + 144 + 128 + 128 = 672).

## Engine constraints recorded

Vanilla `DimensionType` codec bounds (1.21.1):

- `min_y` ∈ `[-2032, 2031]`, multiple of 16;
- `height` ∈ `[16, 4064]`, multiple of 16;
- `min_y + height ≤ 2032`;
- `logical_height ≤ height`.

`-64..607` (min_y −64, height 672) satisfies all four. The candidate is therefore
**engine-permitted**; the risk is downstream mod compatibility, not the core codec.
The Hive dimension type uses the plain vanilla `dimension_type` codec and
does **not** depend on Isekai for its bounds (the Isekai build-height report was
`runtime-unverified` in C0002 and is not on this path).

## Extended-height acceptance — REQUIRED

The owner requested the taller Cinderstack on 2026-08-28, so the compatibility
checkpoint is now seeded and on the critical path. Candidate data may use `height 672`
for isolated testing, but P02 massing may not freeze and no existing production world
may be migrated until every adoption criterion passes. Failure rolls the data back to
the proven `height 384` envelope without changing the Y0 surface design intent.

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

Fixed-seed probe at roof Y607, floor Y-64, acid-sea/surface Y0, and every band transition; relog;
region pregeneration; dedicated-server start and join; client log capture. Compare
against the `-64..319` baseline captured at `EG-P01-S05-C0021`.

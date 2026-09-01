# Wasteland Hex-Grid Cave System

## Production contract

Infinite Domain's canonical Overworld now carves a literal honeycomb cave system
inside Wasteland land terrain. The implementation belongs to the
`wastelands:wasteland` noise router selected by `minecraft:normal`; it is not a
decorative schematic, an organizational guide, or a post-generation script.

The project-owned `infinite_domain_worldgen:hex_grid_cave` density codec folds
world X/Z coordinates into regular axial hex cells. Each repeated cell contains:

- an eight-block-wide corridor following all six sides of the cell;
- a 24-block-wide concentric hexagonal chamber;
- an intervening solid wall that keeps both silhouettes readable;
- three navigable strata centered at Y -40, 4, and 48, each eleven blocks high.

The grid uses a 48-block circumradius. Its signed field is negative only inside
the authored corridors/chambers and their vertical bands, so the canonical
final-density router can carve it with `minecraft:min` while leaving the prior
Overworld terrain, aquifers, entrances, spaghetti caves, pillars, and noodle
caves in place.

## Fractal occlusion

`custom_worldgen:wasteland_hex_plasma` is a four-octave Minecraft NormalNoise
field. Minecraft seeds this noise from the world's generation seed. The cached
plasma barrier is combined with the literal geometry through `minecraft:max`:
low and middle lobes preserve or narrow a corridor, while only high positive
lobes close it. The result can interrupt, thicken, thin, and locally erase the
network without substituting generic noise for the underlying hexagons.

The geometry is deliberately stable while the occlusion changes with the world
seed. This preserves a recognizable architectural language across worlds without
making every world's route graph identical.

## Geography and multiplayer ownership

The cave field is active only where `custom_worldgen:continents` is in the land
range `-0.19..1.21`. It returns positive, solid-preserving density throughout the
Pelagos/Karsic Abyssal oceans and the north/south ocean corridors. This leaves the
central radius-4,000 continent, radius-4,800 feather, cold northern islands, hot
southern islands, recurring east/west continents, and paired Abyssal seabed
program unchanged.

Radius 288 around `(0,0)` is excluded in the codec itself. This covers the full
Spawn Hospital reservation, including its square corners and foundation margin,
without relying on biome interpolation.

The terrain graph contains no quest, player, team, advancement, scoreboard, or
game-stage input. Every new chunk uses the world seed and coordinates alone, so
multiplayer exploration cannot create divergent cave placement.

## Ownership

- Codec source: `packdev/overworld-terrain-companion/`
- Installed project artifact: `mods/infinite-domain-overworld-terrain-1.0.0.jar`
- Geometry: `custom_worldgen:wasteland_hex_geometry`
- Seeded occlusion: `custom_worldgen:wasteland_hex_plasma_barrier`
- Land gate: `custom_worldgen:wasteland_hex_caves`
- Canonical consumer: `kubejs/data/wastelands/worldgen/noise_settings/wasteland.json`
- Focused gate: `python scripts/validate_wasteland_hex_caves.py`
- Pack-wide gate: `python scripts/validate_overworld_geography.py`

The focused report is `docs/wasteland-hex-cave-validation.json`. It proves the
installed codec, final-density reachability, land/ocean and origin bounds,
multi-octave seeded barrier, exact six-sided topology samples, vertical strata,
and multiplayer-safe ownership.

## Runtime load and chunk generation

The isolated NeoForge 21.1.248 smoke run
`20260831-193211_baseline_smoke-r01` loaded the companion JAR and canonical
datapack without a missing density codec or noise reference. A fresh fixed-seed
world then completed the 4x4 `central_wasteland_smoke` tile: 16 remote Overworld
chunks in 136,698 ms, followed by a `benchmark_completed` marker and clean server
shutdown. This establishes the runtime load/serialization boundary and sampled
fresh-chunk generation. One smoke run is not a performance conclusion.

The run's unrelated Arise/Lost Cities acceptance snapshots encountered Rhino
local-declaration errors. The controller was hardened after the run and its
static self-test passes, but those broader acceptance probes require a future
runtime rerun; they are not used as cave evidence.

## Visual acceptance still required

Static, signed-distance, and headless generation proof do not establish visual
quality. Inspect only newly generated chunks.

1. Use spectator mode at remote land coordinates and inspect all three strata.
   Corridors must read as repeated six-sided loops with smaller hex chambers and
   solid wall bands between them.
2. Compare at least three fresh seeds. Occlusion should change route closures
   while the literal honeycomb remains recognizable.
3. Cross a land/ocean coast and confirm the system stops before the seabed; inspect
   the east/west Abyssal corridors for accidental caves.
4. Inspect the complete Spawn Hospital reservation down to Y -48 and confirm it
   remains solid except for unrelated vanilla cave intersections outside the new
   field's ownership.
5. Profile fixed-seed chunk generation against the retained baseline. If the
   field is too expensive, optimize its codec implementation without replacing
   the visible geometry with generic caves.

No visual or performance approval is claimed by the static report or smoke run.

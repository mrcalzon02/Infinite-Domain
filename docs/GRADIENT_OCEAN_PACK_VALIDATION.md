# Gradient Ocean Pack — Isekai API Migration

Source specification: `C:\Users\Admin\Downloads\gradient_ocean_datapack_spec.pdf`

The original vanilla-only scaffold has been migrated to Isekai API 2.1.0 for NeoForge 1.21.1. The installed dependency is:

`mods/isekai-api-2.1.0-neoforge-1.21.1.jar`

## What is active

- `isekai_api:coordinate` supplies the missing raw Z coordinate.
- Isekai arithmetic, clamp, absolute-value, step, and lerp functions replace the nonexistent vanilla codecs.
- The median mask is 1 at Z=0 and reaches 0 at Z=-750 and Z=750.
- The center blends toward large, land-biased continents and retains only Wastelands land biomes.
- The central terrain is radial, not a north-south strip. Radius 3,200 through 3,900 is reserved as a continuous `wastelands:mountains` annulus. The expanded central continent remains guaranteed land through radius 4,000 and blends toward the outer ocean by radius 4,800, preserving the original central geography at exactly 2x linear scale.
- The outer zones blend toward smaller, ocean-biased continents.
- Direction now distinguishes the infinite outer world: east and west blend toward recurring large, land-preferred continents and force the wasteland climate band, while north and south retain small, ocean-preferred continents. The diagonal boundaries use an approximately 500-block transition instead of a hard seam.
- Northern land is exclusively cold-facing terrain: snowy plains and taiga, groves, old-growth taiga, ice spikes, snowy slopes and beaches, frozen rivers, and frozen/jagged peaks. Northern ocean bands are exclusively frozen, deep-frozen, cold, and deep-cold water so biome-specific outer expeditions such as the Spore iceberg mines remain possible.
- Southern land contains every vanilla hot-biome family: Desert; all three Badlands variants; Savanna, Savanna Plateau, and Windswept Savanna; Jungle, Sparse Jungle, and Bamboo Jungle; and Mangrove Swamp. It also includes the installed Wastelands biome families. Southern ocean bands use Warm Ocean and Deep Lukewarm Ocean.
- `data/minecraft/worldgen/density_function/overworld/continents.json` connects the result to terrain that consumes the vanilla overworld continentalness density function, including the Wastelands noise settings.
- `data/minecraft/worldgen/density_function/overworld/erosion.json` overrides the vanilla erosion parameter inside the central continent (see **Central-continent interior: no mountains** below).
- `data/minecraft/worldgen/density_function/overworld/depth.json` overrides the vanilla depth parameter to subtract `custom_worldgen:abyssal_floor_depression` — the direct seabed-depth channel for the East/West abyssal ocean. Continentalness manipulation alone saturates on the flat `-0.2222` offset-spline plateau, so the abyssal plain/fracture/hadal bands need a `depth` delta to actually sink. It is `0` outside the gated abyssal corridor and clamped so the hadal floor keeps a bedrock margin. Authority: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`.
- Moonlight's global datapack folder now points at the instance `datapacks` directory, so the pack is offered to every world rather than sitting unused at instance level.

## Central-continent expansion

The authoritative radial geometry has been expanded without changing biome ownership or the outer directional regime:

- guaranteed central land: radius 2,000 -> 4,000;
- shoreline/outer blend: radius 2,000-2,400 -> 4,000-4,800;
- mountain annulus: radius 1,600-1,950 -> 3,200-3,900;
- central-continent mask falloff multiplier: 0.0025 -> 0.00125 so the transition width scales from 400 to 800 blocks rather than changing shape.

The safe zone, north/south temperature logic, east/west directional preference, abyssal depth zoning, and recurring outer continents are not rescaled; they serve different geographic roles and remain authoritative outside the enlarged center.

## Central-continent interior: no mountains

`wastelands:mountains` is the only central-continent land biome in
`#infinite_domain:lostcities_city_excluded`, and the Lost Cities pack worldstyle
(`kubejs/data/lostcities/lostcities/worldstyles/standard.json`) gives every biome
in that tag a **city-chance multiplier of 0.0**. A mountain-dominated spawn region
therefore suppressed Lost Cities generation near spawn entirely — the custom
`infinite_domain:wasteland_*` city styles never had anywhere to appear.

To fix this the central continent interior is now flattened out of the mountain
band:

- `custom_worldgen:base_erosion` is the raw vanilla erosion shifted-noise term.
- `custom_worldgen:central_interior_mask` is a radial plateau — `1` out to radius
  4,650, feathering to `0` by radius 4,750 — multiplied by `1 - mountain_ring_mask`.
- `data/minecraft/worldgen/density_function/overworld/erosion.json` lerps between
  `base_erosion` and `max(base_erosion, -0.5)` by that mask. Inside the plateau,
  erosion can never fall below `-0.5`, so it can never enter the
  `wastelands:mountains` routing band (`erosion [-1.0, -0.55]` in the world
  preset). The interior fills with `wastelands:city` / `forest` / `apocalypse`
  instead, and terrain relief there is correspondingly gentler.

What is deliberately **not** changed:

- the guaranteed `wastelands:mountains` ring at radius 3,200–3,900 — the mask is
  `0` across the ring annulus, so its erosion (and biome) are untouched;
- the outer directional continents beyond radius 4,750 — the mask is `0`, so
  erosion is bit-identical to vanilla and east/west mountains are unaffected;
- the abyssal ocean program — same reason.

A thin residual mountain band can still occur in the 100-block mask feather
(radius ~4,650–4,750), where the central continent has already blended almost
entirely to open ocean. This is far outside the ring and the playable interior
and is treated as acceptable coastal relief.

Static proof over the density-function graph:
`python scripts/validate_central_interior_mask.py`
(report: `docs/central-interior-mask-validation.json`).

## Pack-wide geography and multiplayer ownership gate

Run `python scripts/validate_overworld_geography.py` after changing the world
preset, regional routing, density graph, Abyssal depth chain, or structure sets.
Its generated report is `docs/overworld-geography-validation.json`.

The gate proves from live files that `minecraft:normal` is the only advertised
Overworld preset; the central continent is guaranteed through radius 4,000 and
feathers by 4,800; north/south retain their cold/hot ocean-separated regimes;
east/west retain recurring large continents and Pelagos/Karsic Abyssal
corridors; Karsic surface biomes remain eastern-only; high-fanout 2D routing
and feature masks stay cached; and structure placement is ordinary datapack
worldgen independent of quests, players, teams, advancements, scoreboards, and
game stages.

The canonical preset, Karsic routing, and cache wrappers are one contract. If a
merge preserves the validator but drops those generated/data edits, this gate
must fail rather than silently falling back to generic temperate land or an
alternate preset.

## Dedicated-server benchmark launcher

The fixed-seed benchmark now uses the official NeoForge 21.1.248 dedicated-server
installation contract instead of reconstructing a server classpath from the
CurseForge client manifest. `scripts/bootstrap_worldgen_benchmark_server.ps1`
downloads the pinned installer, verifies its SHA-256, and installs the patched
server jar plus `win_args.txt` beneath ignored `benchmark_runs/.launcher-cache/`.
Each run receives a disposable hard-linked copy of the server libraries and its
manifest records the server-jar and argument-file hashes.

Dedicated staging also applies the narrow, evidence-backed exclusions in
`scripts/worldgen_benchmark_server_mod_policy.json`. The policy currently removes
Sodium after a real headless smoke reached ModLauncher and failed in
`sodium_service` on the absent LWJGL runtime, plus Barebones McQoy after the next
smoke reached mod construction and its subscriber loaded a client GUI class on
the dedicated-server distribution. Every exclusion must match exactly one
installed jar, retain its reason and observed evidence, and is written with the
policy hash into the per-run manifest; diagnostic variant omissions are tracked
separately.

Run `python scripts/validate_worldgen_benchmark_launcher.py --output
docs/worldgen-benchmark/launcher-validation.json` for the archive-level gate. It
proves all referenced libraries are present, the three launcher/server archives
are intact, and the required BootstrapLauncher, ModLauncher, and Minecraft server
entry points exist. This does not replace `-Suite smoke`: only a completed run
with `benchmark_started`, `tile_completed`, and `benchmark_completed` markers
proves registry/datapack load and real chunk generation.

## Deliberately not claimed complete

The removed `custom_worldgen:overworld` noise-settings file was invalid and unreferenced. It omitted a surface rule, used constant final density, and could not generate the requested terrain.

## Southern sea — settled as warm water

An earlier design goal was a continuous lava sea south of Z=750. That is **dropped by owner decision (2026-08-27)**: the southern ocean stays ordinary warm water (Warm Ocean / Deep Lukewarm Ocean) and the southern islands carry the full warm/hot biome set, which is already how the biome routing is configured. The unused `custom_worldgen:south_lava_mask` density function was deleted rather than left disconnected. Minecraft's `noise_router.lava` only picks lava *aquifers* and is not a per-coordinate `default_fluid` override, so no partial implementation remains to maintain.

## New-world validation

Worldgen changes only affect newly generated chunks. Create a disposable world using the Wastelands preset, then run:

1. `/isekai validate custom_worldgen`
2. `/tp @s 0 100 -1500`
3. `/tp @s 0 100 0`
4. `/tp @s 0 100 1500`

Expected at this stage: the directional climate logic remains intact inside the enlarged central landmass. Northern and southern biome selection should retain the established cold/hot families while the radial central-continent mask keeps terrain land-biased until the expanded shoreline transition.

Validate the mountain ring at representative compass points: `/tp @s 3500 140 0`, `/tp @s -3500 140 0`, `/tp @s 0 140 3500`, and `/tp @s 0 140 -3500`. Each surface location should resolve to Wasteland Mountains. Also sample just inside and outside the band (for example radius 3,100 and 4,000) to confirm the annulus terminates cleanly.

Validate the mountain-free interior: `/tp @s 0 120 0`, `/tp @s 1500 120 0`, `/tp @s -2500 120 0`, `/tp @s 0 120 2800`. None of these should resolve to Wasteland Mountains — expect Ruined City, Dead Forest, or Apocalyptic Wasteland with visibly gentler relief than the ring. The only Wasteland Mountains inside radius 4,650 should be the ring itself.

Validate the shoreline transition at radius 4,000, 4,400, and 4,800 on all four cardinal axes. The central mask should be fully land-biased at radius 4,000, partially blended at 4,400, and fully handed off to the established outer regime by radius 4,800. A little mountainous coastal relief between radius ~4,650 and 4,750 is expected and acceptable.

Validate the infinite directional regimes safely beyond the expanded central shoreline with `/tp @s 7000 160 0` and `/tp @s -7000 160 0` for east/west large Wastelands continents. Compare those with `/tp @s 0 160 7000` and `/tp @s 0 160 -7000`, which should remain dominated by ocean and smaller hot/cold continents. Large continents are preferred rather than guaranteed at each exact coordinate, so an east/west test point may still land in the ocean separating two large continents.

Validate the abyssal seabed-depth channel far out along the east/west corridor (roughly `/tp @s 9000 120 0` and `/tp @s -9000 120 0`, then fly outward until deep ocean biomes appear). Swim the shelf outward and confirm a readable descent: continental slope, then an **abyssal plain floor clearly deeper than a vanilla deep ocean** (well below Y 35), then patchy fracture / hadal pockets that go **noticeably deeper again without exposing bedrock** (`-64`). Check `F3` biome names track the depth bands (`…continental_slope` → `…abyssal_plain` → `…fracture_field` / `…hadal_trench`). Confirm the north/south oceans (`/tp @s 0 120 9000`) are untouched — normal deep-ocean depth, no abyssal deepening. If the plain is still shallow, raise the `1.0` gain in `abyssal_floor_depression`; if the hadal floor nears bedrock, lower the `0.55` clamp.

Confirm there are **no floating square blocks of dirt/gravel hanging above the abyssal plains** near structure sites (the `start_height` 32 → 0 seating fix). Abyssal structures should sit on or partly in the seabed, not on a raised pedestal or under a floating slab.

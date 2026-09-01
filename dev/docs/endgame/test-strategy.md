# Endgame — test strategy

**Authority:** `docs/Endgame.md` §6.3 and checkpoint `EG-P00-S05-C0010`.
**Status:** ACCEPTED 2026-08-27. Reproducible instructions a fresh worker can follow
without prior context.

## 1. Smoke / QA world

- Path: `saves/Infinite Domain - Hive World QA` (gitignored).
- Type: superflat, creative, cheats on, a documented fixed world seed from §2.
- Entry for testing: `/execute in infinite_domain:hive_world run tp @s <x> <y> <z>`
  (operator) or the prototype travel mechanic once C0019 exists.
- The world is disposable and rebuildable; never a source of truth.

## 2. Reserved seed set

Every seed sweep uses **exactly** these, in this order:

```
1
1234
88888888
-4206942069
2147483647
0
```

## 3. Fixed probe coordinates

| Probe | Coordinates | Purpose |
|---|---|---|
| arrival | `(0, <arrival_y>, 0)` | safe-arrival repeat test (C0020) |
| world floor | `(0, -64, 0)` and `(1200, -64, 1200)` | floor seal, fog maximum, serialization |
| planetary surface / acid sea | `(0, 0, 0)` and `(1200, 0, 1200)` | terrain datum, coastline, Spire seating |
| band: The Drown | `(0, -32, 0)` and `(1200, -32, 1200)` | band identity, atmosphere, acid |
| band: The Underworks | `(0, 48, 0)` and `(1200, 48, 1200)` | band identity, navigation |
| band: The Furnace Tiers | `(0, 152, 0)` and `(1200, 152, 1200)` | band identity, circulation |
| band: The Billet Decks | `(0, 280, 0)` and `(1200, 280, 1200)` | band identity, districts |
| band: The Vaulting | `(0, 416, 0)` and `(1200, 416, 1200)` | monumental scale, sightlines |
| band: The Crown | `(0, 544, 0)` and `(1200, 544, 1200)` | skyline, ascent |
| world roof | `(0, 607, 0)` and `(1200, 607, 1200)` | roof seal, lighting, client clipping |
| chunk border | `(16, y, 16)`, `(-1, y, -1)` | seam / continuity |
| deep wastes | `(6000, <surface>, 0)` | wasteland-share sampling |

Band midpoints are the accepted C0004 ranges' centres and move only if C0004 changes.

## 4. Command catalogue

```
/execute in infinite_domain:hive_world run tp @s 0 <y> 0
/locate biome infinite_domain:hive_world_<name>
/data get entity @s Dimension
# there is no /forge or /neoforge dimensions command on NeoForge 21.1;
# confirm registration by tab-completing "/execute in " or by the tp above succeeding
/spark profiler --start ; /spark profiler --stop
/spark tps ; /spark healthreport
/tick freeze ; /tick step
```

## 5. Screenshot cameras

- Naming scheme: `hive-cam-<region>-<nn>`, region in
  `{waste, drown, underworks, furnace, billet, vaulting, crown, arrival, trunk}`.
- Exact positions and angles are frozen at `EG-P02-S01-C0025`.
- Phase 1 uses only `hive-cam-arrival-01` and `hive-cam-waste-01`.

## 6. Evidence paths

`docs/endgame/evidence/<checkpoint-id>/` holds every artifact for that checkpoint:
screenshots (`.png`), `spark` reports (`.txt`/`.json`), trimmed log excerpts
(`log-<topic>.txt`), and validator output (`<validator>.json`).

## 7. Offline smoke validator — `scripts/endgame/validate_hive_world_smoke.py`

Runs with no live instance. Asserts:

1. every Hive JSON file parses;
2. every registry reference resolves against `docs/registry-inventory/` plus the Hive's
   own declared IDs;
3. `dimension_type/hive_world.json` bounds equal the C0006 height contract
   (`min_y -64`, `height 672`, `logical_height 672`, top block `Y607`, sea level `Y0`);
4. `dimension/hive_world.json` references a real `noise_settings` and biome source;
5. the arrival-platform structure and any entry item/advancement IDs exist;
6. no Hive file writes under a forbidden shared path
   (`minecraft:`, `wastelands:`, `gradient_ocean_pack`, or `worldgen/.../*.nbt`);
7. no player-facing lang **value** contains the substring `hive` (case-insensitive);
8. each Hive server script is IIFE-wrapped (KubeJS server scripts share one global
   scope, so a bare top-level `const` collides across files).

## 8. Runbook (fresh worker)

1. Confirm the Hive datapack files are present under `kubejs/data/infinite_domain/`.
2. `python scripts/endgame/validate_hive_world_smoke.py` and
   `python scripts/endgame/validate_hive_world_modules.py` — both must pass before any launch.
3. Launch the client on the QA world (or a fresh world with a §2 seed).
4. Check `logs/latest.log` for a clean pre-Hive baseline, then for zero new
   `infinite_domain:hive_world` errors.
5. `/execute in infinite_domain:hive_world run tp @s 0 0 0`; walk the §3 probe list.
6. Capture the Phase-appropriate cameras from §5.
7. `/spark profiler` for a 2-minute sample while flying the probe route; save to the
   evidence dir.
8. Record results in the checkpoint handoff (`docs/Endgame.md` §6.4 schema).

## 9. Removal test procedure (feeds `EG-P01-S06-C0023`)

1. Record the exact Hive path list (datapack + prototype scripts + companion, if built).
2. Move all Hive paths aside (`git stash --` the paths, or a documented delete list).
3. Relaunch a fresh client and a dedicated server.
4. Assert: Overworld, Nether, and End generate and load unchanged; no registry or
   datapack errors; no orphaned `infinite_domain:hive_world` entry in existing
   `level.dat` / dimension data; existing saves open.
5. Restore the Hive paths; confirm the smoke validator still passes.

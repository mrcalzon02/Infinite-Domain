# EG-P01-S05-C0021 — client baseline (evidence)

**Status:** authoring done (the dimension-type effect fields are set); the captures
below are **the owner's in-client step** and are not yet in this folder.

## Temporary client assumptions (set in `dimension_type/hive_world.json`)

| Field | Value | Rationale (Phase 1 only) |
|---|---|---|
| `effects` | `minecraft:the_nether` | proven vanilla effect key (C0002); original Hive rendering is a companion-module client checkpoint |
| `ambient_light` | `0.1` | matches `cyberspace:darknet_dimension`; testable without being blind. C0021 may darken it toward the §2.8 tomb intent |
| `fixed_time` | `18000` | permanent gloom; `has_skylight` is false so this only affects sky/phantom logic |
| `has_skylight` / `has_ceiling` | `false` / `false` | sealed, sunless interior |

## Captures the owner adds to this folder

1. `hive-cam-arrival-01.png` — standing on the arrival deck facing +X.
2. `hive-cam-waste-01.png` — in `hive_world_dead_waste` (the open shaft), a long vertical sightline.
3. `client-log.txt` — trimmed `logs/latest.log`: zero new `infinite_domain:hive_world`
   client errors; note any shader/resource-pack warnings.
4. `baseline-client-spark.txt`, `baseline-server-spark.txt` — **pre-Hive** `spark`
   profiler + healthreport with **no Hive content loaded** (the C0008 baseline). Record
   the dev-machine CPU/GPU/RAM and MC settings (render distance, graphics) at the top.

## Why the baseline matters

Every C0008 budget is "absolute ceiling AND no worse than +X% vs. this baseline."
Without the pre-Hive capture the later Phase 2 / Phase 7 performance gates have nothing
to compare against.

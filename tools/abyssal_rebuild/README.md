# Abyssal Rebuild Generator

`generate_abyssal_sites.py` is the deterministic source for the next active revisions of the six deep abyssal structure NBTs.

Run from repository root:

```bash
python tools/abyssal_rebuild/generate_abyssal_sites.py kubejs/data/infinite_domain/structure/abyssal
```

Expected deterministic Git blob hashes for the generated files:

- `pelagos_abyssal_relay.nbt` — `3c2131b132b8765c2ee1bb66174d28d7d94ae54a`
- `pelagos_fracture_observatory.nbt` — `b26ffb308ed79027411ab4893fccc8b33f6c38b4`
- `pelagos_hadal_probe_station.nbt` — `c7c28af60c67d2b9033d9860d711614cf5338f64`
- `karsic_abyssal_pipeline_station.nbt` — `3d8b155d3552cd9084f691a92a0b19e01ba07e5d`
- `karsic_fracture_listening_post.nbt` — `b322e203a86be4ff7963eae31c6978cfb85e19fe`
- `karsic_hadal_blacksite.nbt` — `84b2de43cd4298db62ed0a49958d0fb41c53c1bd`

The generator uses Minecraft 1.21.1 `DataVersion 3955`, deterministic gzip (`mtime=0`), the existing stable structure filenames, site-specific evidence loot tables and secondary salvage tables.

The GitHub connector used during authoring could not preserve large binary NBT payloads byte-exactly, so the source generator is committed instead of risking corrupted active structures. The current repository NBT shells remain active until the deterministic generator is run in a normal filesystem-capable development environment and the resulting six files are committed.

After materialization, update `config/ftbquests/quests/chapters/abyssal_recovery.snbt` so the six deep records are detected as physical item tasks rather than compatibility rewards issued on structure completion.

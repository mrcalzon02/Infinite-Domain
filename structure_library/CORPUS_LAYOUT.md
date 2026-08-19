# Canonical Structure Corpus

`structure_library` is the single authoritative corpus index. Existing NBT remains in the Minecraft data-pack path so it can be loaded without a second copied asset tree.

- `catalog.json` — metadata for the active refinement/conversion corpus.
- `corpus-manifest.json` — authoritative path map and counts.
- `licensing/provenance.json` — one provenance and redistribution record per retained source or master.
- `programs/` — declared room, adjacency and circulation programs.
- `variants/` — damage, environment and occupation derivation records.
- `modules/catalog.json` — reusable architectural modules and their connectors.
- `infrastructure/catalog.json` — roads, rail, bridges, tunnels, parking and waterfront modules.
- `reviews/` — four-view clean-master and derivative review evidence.
- `audit_renders/` — four-view evidence for every inbuilt template.
- `sources/quarantine/` — pinned intake archives and evidence; license approval does not bypass compatibility/quality quarantine.
- `extracted/` — normalized review-only conversions that are not referenced by live world generation.
- `sources/quarantine/` — pinned intake archives and evidence; license approval does not bypass compatibility/quality quarantine.
- `extracted/` — normalized review-only conversions that are not referenced by live world generation.

Source lineage is always:

```text
source original -> normalized master -> refined clean master -> condition variant -> occupation variant
```

No uncertain-license donor may enter a distributable or production selector. Empty module/infrastructure catalogs are deliberate gates, not implied completeness.

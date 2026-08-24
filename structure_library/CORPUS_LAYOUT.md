# Canonical Structure Corpus

`structure_library` is the shared directory for the project's structure
corpora. This layout describes the **land** corpus specifically; see
"Sibling corpus: deep-sea structures" below for the other one it shares
the directory with. Existing NBT remains in the Minecraft data-pack path so it can be loaded without a second copied asset tree.

Design doctrine and the QA gate live in `STRUCTURE_REBUILD_SYSTEM_V2.md`, not in `generated-structure-refinement-policy.json` (superseded — see `README.md`).

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

## Sibling corpus: deep-sea structures

Underwater structures and geological features are a separate,
independently governed corpus living alongside this one: its own manifest
(`deepsea-corpus-manifest.json`), schema (`deepsea-metadata.schema.json`),
catalog (`deepsea-catalog.json`), refinement policy
(`deepsea-refinement-policy.json`), and validator
(`scripts/validate_deep_sea_structures.py`), governed by
`docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md` rather than
`STRUCTURE_REBUILD_SYSTEM_V2.md`. It is a sibling to this corpus, not a
subset of it — `catalog.json`/`corpus-manifest.json` above do not cover it,
and its counts are tracked separately in `deepsea-corpus-manifest.json`.

# Infinite Domain Old World Narrative

This directory is the repository-owned implementation control surface for the approved Old World narrative package.

The supplied canon is pinned by SHA-256 `eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182`. The binary DOCX is not stored here; normalized source instructions, matrices, and seed records are imported into `source/`, while generated stable registries live in `registry/`.

Implementation remains incremental:

1. preserve the approved 84-structure source corpus;
2. map each OWS target to an approved source or a documented new build;
3. satisfy at least four of the six narrative revision dimensions;
4. make mandatory proof deterministic and structure-bound;
5. add a reliable locator before making a rare site mandatory;
6. validate static contracts on every slice;
7. record runtime/worldgen checks as pending until they are actually run.

The two corpus counts are intentionally different. The 84 structures are the
authoritative Wasteland source-template inventory. The Old World narrative
program selects and transforms that inventory into exactly 64 descendants,
`OWS-001` through `OWS-064`; it does not define `OWS-065` through `OWS-084`.
`docs/old-world/structure-worldgen-roles.json` owns each descendant's biome
selector independently of whether that staged structure has been admitted to a
structure set.

Current heavy-rebuild slice: OWS-008, the VCF Emergency Persistence
Investigation Laboratory. Gate A r2 and the repaired Gate B r2 intact model are
independently passed; Passes 7–12 are complete and historical layering is the
next legal stage. Gate C remains blocked until Passes 13–18 are verified. OWS-009
remains the representative functional investigation for the opening `THEY WERE
HERE FIRST` quest.

Build after importing the supplied package:

```powershell
python scripts/build_old_world_narrative.py --package-root <extracted-package-root>
python scripts/generate_old_world_narrative_structures.py
python scripts/validate_old_world_narrative.py
```

Subsequent registry and quest rebuilds do not require the external package:

```powershell
python scripts/build_old_world_narrative.py
```

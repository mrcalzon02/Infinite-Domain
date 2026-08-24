# Infinite Domain Structure Corpus

This is the source-of-truth library for buildings admitted to the Lost Cities replacement pipeline. Production world generation must reference approved derivatives, never an unreviewed rough source directly.

Lifecycle:

1. `rough_source` — imported or existing recognizable geometry.
2. `clean_master` — heavily rebuilt, architecturally articulated, fully programmed building without wasteland damage.
3. `damage_variant` — spatially coherent damage derived from the clean master.
4. `occupation_variant` — gameplay state layered onto a clean or damaged derivative.
5. `approved` — automatic validation and visual review both complete.

The corpus is deliberately mixed and includes rough sources plus clean masters. Every entry remains quarantined from the Lost Cities building selectors until its clean master, conversion, rendered review, in-world walk-through and human approval are complete.

**Superseded:** `generated-structure-refinement-policy.json` described the previous "heavy rebuild" standard. The first player-scale review found that standard was never mechanically enforced and let systemic floating geometry, incoherent damage, and context-blind ground surfacing through as `candidate_for_in_world_review`. The authoritative design doctrine and QA gate are now `STRUCTURE_REBUILD_SYSTEM_V2.md` in this directory, enforced by `scripts/structure_geometry_lint.py` and built with `scripts/structure_geometry_primitives_v2.py`. Every structure's `structure_library/programs/<id>.json` — its purpose-driven room, circulation, and damage program — is a required generation input under v2, not optional documentation.

**Not covered by this README:** the deep-sea structure and geological
feature corpus is a separate system living in the same `structure_library`
directory (`deepsea-catalog.json`, `deepsea-metadata.schema.json`,
`deepsea-refinement-policy.json`, `deepsea-corpus-manifest.json`), governed
by `docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md` and
validated by `scripts/validate_deep_sea_structures.py` — its own validator,
independent of `structure_geometry_lint.py` and `validate_structure_corpus.py`
above. See `structure_library/CORPUS_LAYOUT.md`'s "Sibling corpus" section.

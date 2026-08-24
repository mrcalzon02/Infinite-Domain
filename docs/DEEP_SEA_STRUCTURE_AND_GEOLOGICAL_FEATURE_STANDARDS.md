# Deep-Sea Structure and Geological Feature Standards

This is the authoring and audit standard for everything Infinite Domain places
underwater: natural terrain features and built structures alike. It is a
sibling to the land heavy-rebuild system (`CODEX_STRUCTURE_PIPELINE.md`,
`structure-metadata.schema.json`, `docs/INBUILT_STRUCTURE_AUDIT.md`,
`docs/WASTELAND_SETTLEMENT_REPLACEMENT_STATUS.md`), not a replacement for it —
this document says what carries over unchanged, what the underwater
environment forces to be different, and what is genuinely new.

## Relationship to the heavy-rebuild system

Carried over unchanged:

- the lifecycle — `rough_source -> clean_master -> damage_variant -> occupation_variant -> approved`;
- the provenance/licensing manifest (Phase 11 of `CODEX_STRUCTURE_PIPELINE.md`);
- disposition-ledger discipline — a quarantined or rebuilt disposition is a
  completed audit, not a quality approval; production admission is a
  separate, human-reviewed gate; automatic validation never writes an
  approval;
- diversity enforcement by architecture family, independent of condition and
  occupation variants;
- the core rule: `reuse -> repair -> refine -> modularize -> derive`, never
  `discard -> hallucinate a replacement cube`.

New, because the operating environment is genuinely different:

- two asset classes the land pipeline does not model — natural geological
  terrain, and a three-tier authoring taxonomy instead of one;
- an operating-condition model specific to submersion: depth band,
  per-compartment atmosphere state, access/vehicle connectors instead of
  roads, and burial state;
- a damage and occupation vocabulary suited to marine decay and
  multi-faction submariner history rather than wasteland decay;
- low-visibility legibility rules — these are designed to read in silhouette
  and near-field, not from across a settlement.

Scope boundary with existing ocean work: `docs/OCEAN_RESTORATION.md` and
`docs/WORLDGEN_STRUCTURE_SAFETY.md` already establish the biome and sea-level
foundation (sea level 63, restored `#minecraft:is_ocean` membership, monument
and Seven Seas exclusion radii), and `docs/biome-gating-audit/ocean-structure-sets.csv`
is the authoritative registrant list every placement in this system must be
checked against. This document does not restate or override those; it is the
authoring/audit layer built on top of them.

## Asset classes

Three tiers, each with its own authoring mechanism, disposition
requirements, and validation depth. One location can combine tiers — a
trench (Tier 1) containing a vent field (Tier 2) containing a buried
listening post (Tier 3) — but each constituent gets its own ledger entry and
its own `asset_id`.

### Tier 1 — Macro geological terrain

Large-scale seafloor shape: trench systems, mid-ocean ridges, abyssal
plains, seamounts, continental-shelf breaks, canyon networks. Authored as
biome-scoped worldgen data (density functions, noise routers, surface
rules), in the same pattern as `OCEAN_RESTORATION.md`'s continentalness-band
override — never as a hand-placed block loop. No `structure_id`; identified
by the named terrain feature and its biome/noise scope. Escalate to a
project-owned companion jar (following the `packdev/darknet-worldgen-patch`
precedent) only when a shape genuinely cannot be expressed as datapack
worldgen — for example, a virtual floor-datum override for a dependent mod's
placement code — not for shapes ordinary density functions already produce.

### Tier 2 — Meso decoration features

Site-scale, non-programmed dressing: hydrothermal vent fields, brine pools,
silt/sediment fans, rock-arch clusters, methane seep pockets, bioluminescent
growth beds, debris scatter fields. Authored as ordinary compressed NBT
template-pool features placed through `configured_feature`/`placed_feature`
or small jigsaw pools — the same mechanism `docs/alien-structures.md`
already uses for its landmarks. No rooms, no circulation, no entrances.
Validation is lighter than Tier 3: terrain safety and hazard-marker checks,
not program/circulation checks.

### Tier 3 — Structures

Authored, programmed built environments: wrecks (surface-origin ships that
sank, or purpose-built submersible wrecks), and abandoned or contested
submariner facilities — habitats, research stations, mining platforms,
listening posts, military installations — belonging to one of the pack's
faction/build-style families. These receive the full heavy-rebuild-equivalent
lifecycle and every gate below. This is the tier that corresponds directly
to the land `programmed_building` / `multi_story_building` profiles in
`structure-metadata.schema.json`.

## The underwater operating-condition model

Four properties every Tier 3 asset must declare (and Tier 2 partially),
because none of them exist in the land system.

### Depth band

Sea level is 63 (`docs/WORLDGEN_STRUCTURE_SAFETY.md`). Bands are declared by
the seafloor Y the asset sits on, not by dimension height:

| Band | Seafloor Y | Light | Typical biome |
|---|---|---|---|
| `shelf` | 50–62 | daylight reaches the floor most hours | ocean, warm/lukewarm ocean |
| `open_floor` | 30–50 | dim, weather/time dependent | ocean, cold ocean |
| `deep_floor` | -10–30 | effectively dark without authored light | deep ocean variants |
| `abyssal` | -64 to -10 | fully dark; Tier 1 trench territory | deep/frozen deep ocean, carved trenches |

### Atmosphere state

Declared per compartment, not per structure — one facility can be part
flooded, part dry:

- `flooded` — water-filled; normal aquatic mob eligibility; no player breath
  management inside.
- `dry_pressurized` — air-filled behind a sealed hull; a breach means
  flooding, not ambience.
- `mixed_breached` — a formerly dry compartment now flooding through a hull
  failure. This is the underwater equivalent of a localized wasteland
  collapse, and must read the same way: spatially coherent, tracing back to
  one legible cause, never scattered.

### Access / vehicle connector

Replaces `road_connection`; there is no road network underwater.

`enum: [diver_hatch, moon_pool, submarine_dock, surface_shaft, buried_shaft, none]`

A `submarine_dock` or `moon_pool` must be sized against the hull footprints
of the installed submersibles (`create_submarine`, `create_aquatic_ambitions`)
so the pack's own vehicles can actually use it — verify this in-game, not
only in the schematic.

### Burial state

`enum: [exposed, partially_buried, subterranean]`. `subterranean` is the
underwater analog of the land `buried_sites` family (`bunker_network`,
`survivor_cache`): reached by a shaft, not by swimming up to a visible hull.

## Faction / build-style catalog

Structures should read as belonging to a history, not a random kit-bash.
The catalog is extensible; these families are already grounded in the
pack's existing factions and installed content, so new entries reinforce
the project's identity instead of fragmenting it.

| Build style | Grounding | Typical form |
|---|---|---|
| pre-collapse civilian/industrial | land `bunker_network`, `survivor_cache` families | drowned or buried shelter, utility plant, flooded suburb remnant |
| Create industrial offshore | `create_aquatic_ambitions`, `create_submarine`, `petrochem` | rigs, pump stations, mining platforms, submarine pens |
| military remnant | land `military_remnants` family | listening posts, scuttled vessels, minefields (as Tier 2 hazard scatter) |
| Darknet-adjacent | `docs/DARKNET_*.md`, Cyberware faction | a drowned relay/data node using the established corrupted-circuit visual language; a themed variant only — never a portal into the actual Darknet dimension |
| ancient/unknown-origin | `docs/alien-structures.md` precedent | mystery sites reusing the established coordinate-glyph motif, gated by relic-driven progression rather than raw exploration |
| survivor/scavenger occupation | cross-cutting occupation state, not its own build style | applied on top of any of the above |

Do not invent a new faction identity per structure. Every new Tier 3 asset
declares which existing build style it belongs to, or makes an explicit,
documented case for a new one.

## Damage vocabulary

Underwater decay reads differently from wasteland decay and needs its own
controlled list, audited the same way Phase 26 audits wasteland damage:
spatially coherent, tracing to one legible cause, never independent random
block deletion.

`corrosion`, `biofouling` (coral/algae/barnacle overgrowth), `silt_burial`,
`pressure_hull_failure` (implosion — violent, localized, debris-radial),
`flooding_breach` (the `mixed_breached` atmosphere state made physical),
`listing_settle` (the structure has tilted/settled into soft seafloor, not
floating), `anchor_drag_scarring`, `current_scour`, `thermal_scarring`
(only adjacent to Tier 1/2 vent features).

## Occupation vocabulary

Parallel to land Phase 27, substituting aquatic-appropriate agents:

`derelict` (empty), `salvage_crew`, `faction_garrison` (per the build-style
catalog), `hostile_aquatic` (guardians, drowned, and the installed
`ftboceanmobs` / `mekanite_mobs` / Ice and Fire siren roster as appropriate
to depth band and build style), `quarantine_outbreak`, `smuggler_cache`,
`quest_location`. Prefer overlays/data-driven composition over duplicated
schematics, exactly as Phase 27 directs on land.

## Metadata schema

`structure_library/deepsea-metadata.schema.json` extends the land schema's
discipline (`format_version`, controlled vocabularies, an `asset_id`
pattern) with an `asset_class` discriminator
(`geological_macro` | `geological_feature` | `structure`) and the four
operating-condition fields above. Tier 3 entries additionally reuse
`source_role`, `refinement_intensity`, `source_license`, and
`production_status` unchanged from `structure-metadata.schema.json` — a
deep-sea clean master moves through the same
`rough_source -> clean_master -> damage_variant -> occupation_variant -> approved`
states as a land one. See the schema file for exact required fields per
tier.

## Provenance and licensing

Unchanged from Phase 11–13 of `CODEX_STRUCTURE_PIPELINE.md` and the intake
rules in `docs/STRUCTURE_DONOR_LICENSE_RESEARCH.md`: every non-original
asset needs `source_project`, `source_author`, `source_url`,
`source_license`, `required_attribution`, `commercial_use_allowed`,
`modification_allowed`, `redistribution_allowed`, and a conversion history.
Uncertain licensing excludes an asset from distributable builds.
Project-page license labels only qualify a candidate for quarantined
intake, never for redistribution. This system does not create a second
licensing track — it feeds the same one.

This also carries the project's own hard rule: nothing here modifies a
third-party mod jar. Every deep-sea asset is our own NBT/schematic, datapack
worldgen JSON, or KubeJS script, or — only when unavoidable — a project-owned
companion jar built the same way `packdev/darknet-worldgen-patch` was. Never
a repackaged or altered copy of someone else's mod, and no third-party mod
code or content gets uploaded alongside it.

## Placement, spacing, and exclusion contract

Every Tier 3 structure set and every Tier 1/2 placed feature is checked
against `docs/biome-gating-audit/ocean-structure-sets.csv` before it is
added to the registrant list, the same way `docs/WORLDGEN_STRUCTURE_SAFETY.md`
already validates Seven Seas ships against monuments:

- record `spacing`, `separation`, `salt`, and an explicit `exclusion_zone`
  (chunk radius from monuments and from other registrants) for every new
  entry, and append it to that CSV so the registrant list stays the single
  source of truth;
- validate footprint against a real biome-and-surface-height radius, not a
  single-chunk check — the Seven Seas fix in `WORLDGEN_STRUCTURE_SAFETY.md`
  (an 8-chunk biome plus surface-height radius for ~114-block ships) is the
  minimum bar for anything with a comparable footprint;
- depth-band biome gating follows the table above: an `abyssal` structure
  does not spawn in a `shelf`-band biome, or the reverse;
- Tier 1 changes stay inside the reserved continentalness bands
  `OCEAN_RESTORATION.md` carved out for vanilla ocean biomes, and do not
  re-encroach on the Wastelands landward climate points.

## Audit checklist (Stage A equivalent)

Adapted from the land Stage A audit expectations in
`CODEX_STRUCTURE_PIPELINE.md`, with underwater-specific substitutions.
Evaluate, where applicable:

- parse/load validity; MC version and block-state compatibility, including
  correct waterlogged states on every intended-flooded block;
- dimensions, seafloor origin, and declared depth band;
- access connectors (moon pool / dock / hatch / shaft), sized and tested
  against installed submersibles;
- interior/compartment connectivity, evaluated per atmosphere state — a
  flooded compartment needs swim-through connectivity, a dry compartment
  needs walkable connectivity, a mixed compartment needs both to make sense
  together;
- vertical traversal appropriate to atmosphere state (ladders/stairs in dry
  compartments, shafts in flooded or buried ones);
- accidental air pockets in compartments meant to be flooded, and accidental
  flooding in compartments meant to be dry — the underwater equivalent of
  "sealed/impossible rooms," and the single most common silent defect class
  for this asset type;
- unsupported/floating geometry, distinguished from intentional
  negative-buoyancy elements — a suspended habitat section on authored
  anchor chains or pylons is not a defect; an unexplained floating debris
  field is;
- façade/silhouette coherence evaluated at the asset's declared depth-band
  light level and at typical underwater fog/render distance, not at full
  daylight render distance — land buildings are designed to read from afar;
  these are designed to read in silhouette and near-field; see "Size and
  visual composition audit" below for the concrete checklist this expands
  into;
- hull breach placement and doors/windows/airlocks appropriate to
  atmosphere state;
- rotation behavior on sloped or uneven seafloor terrain, not flat terrain;
- block entities/containers/loot markers;
- worldgen metadata and the placement/exclusion contract above;
- renders/gallery evidence captured under the declared depth-band lighting,
  not the render pipeline's default lighting;
- known defect reports.

Do not mark a disposition complete because a command exited successfully.
Structural and visual quality require actual evidence, exactly as the land
pipeline requires.

## Size and visual composition audit

This section exists because the initial reference wave shipped and passed
every automated check while still being genuinely hard to read: the audit
renders themselves used placeholder colors for most of the palette, one
family's support legs were the same material as its hull, and a landmark
mast was too visually similar to the hull it rose from to register. All of
that validated cleanly under "parse/load validity" and "unsupported/floating
geometry" — this section is the checklist item those defects fell through,
made concrete enough to actually catch the next one.

1. **Render color fidelity is a prerequisite for any render to count as
   evidence.** `scripts/render_deep_sea_review.py`'s `KNOWN_BLOCK_COLORS`
   table is a curated, real approximation of each block's in-game
   appearance, not an arbitrary or hash-derived placeholder. Every material
   an asset places must resolve there — the script warns to stderr on any
   block that falls through to the hash fallback, and
   `scripts/validate_deep_sea_structures.py` fails validation on it. A
   render built from uncalibrated colors is not audit evidence, no matter
   how confident it looks; treat a fallback-color warning as a blocking
   defect, not a cosmetic one.

2. **Footprint and height must fit the asset's declared role**, not just
   its `asset_class`. Rough size bands, as a sanity check rather than a
   hard rule:

   | Role scale | Footprint | Height | Examples |
   |---|---|---|---|
   | small facility/shelter | roughly 7–11 per side | 6–9 | single-chamber outpost, relay shelter, listening post |
   | mid vessel/facility | roughly 9–13 wide, 15–30 long, or 9–13 square | 8–12 | patrol/cargo wreck, small habitat, pump station |
   | large industrial platform | roughly 13–20 per side | 8–16 | mining rig, submarine pen, processing platform |

   A structure whose catalog `notes` claim it is a major facility but whose
   footprint reads as a small shack (or the reverse) is a fitness-for-purpose
   defect even when every other check passes. State the claimed size band
   and reasoning in the catalog entry for anything that isn't an obvious fit.

3. **Every structure needs at least three visually distinct material
   zones** for its major structural roles: a primary shell/hull material, a
   distinct floor/deck material, and at least one landmark or accent
   element (mast, chimney, support leg, hatch marker, console glow) in a
   third material. A single material carrying the hull, the superstructure,
   and the support structure is a defect, not an aesthetic choice — it was
   the actual state of both `coastal_patrol_wreck` (mast was `iron_block`,
   same as the hull) and `abyssal_mining_rig` (legs were `iron_block`, same
   as the deck and hull) before this pass. Fixed by moving the mast to
   `minecraft:oxidized_cut_copper` and the rig's legs to
   `minecraft:blackstone` — pick materials that contrast in value (light
   vs. dark), not just hue, since that's what survives fog and low light.

4. **Exposed and partially-buried Tier 3 structures need a landmark
   silhouette element** — something that breaks the structure's own
   bounding-box massing (a mast, derrick, chimney stack, antenna, or a
   deliberate listing/leaning profile) so it reads as "a structure" rather
   than "a lump of seafloor" at range in fog. `subterranean` structures are
   explicitly exempt from this requirement — see the next point.

5. **Range-silhouette legibility is judged relative to `burial_state`, not
   uniformly.** `exposed` and `partially_buried` structures are judged on
   how well their silhouette reads at range. `subterranean` structures are
   judged instead on close-up tell legibility only: the single surface
   feature (a shaft mouth, a trapdoor, an exposed pipe or vent) that a diver
   swimming or digging past would actually notice — since the entire design
   intent of `subterranean` is that nothing is visible at range. Do not add
   a landmark spike to a buried asset merely to satisfy point 4; that
   contradicts its own declared burial state.

6. **Damage/occupation dressing has a density ceiling.** Biofouling, silt,
   and corrosion dressing must not obscure more than roughly half of any
   single structural face's visible surface area. Past that, a structure
   stops reading as "a wreck with growth on it" and starts reading as
   "a mound" — the defect that first prompted this section, before the
   render-color fix made it clear how much of that impression was the
   placeholder-color problem versus real overgrowth density. Judge this by
   eye during render review; it does not need to be a hard automated gate.

7. **Every structure's single defining functional feature must be
   identifiable in at least one required render.** A wreck's
   mast/pilothouse, a rig's moon pool, a shelter's shaft mouth, a vent
   field's chimneys — if the two-view renderer's fixed isometric angle
   occludes it (as it does for the mining rig's moon pool, which the
   surrounding hull hides from that angle but the floor-slice at the deck
   level shows clearly), say so explicitly in the ledger's audit-evidence
   column and cite which view actually carries the evidence, rather than
   letting a real gap in the render pass silently.

## Quality scoring

Same axes as land Phase 20 — structural coherence, accessibility,
architectural detail, functional readability, visual variation, worldgen
suitability, performance cost — plus one addition specific to this system:

**Hazard/atmosphere fit** — does the asset's danger density and legibility
match its depth band and low-visibility conditions? A shelf-band derelict
ambushing a player with abyssal-tier hostiles is a design defect, not
difficulty. An entrance compartment with no light source in a
zero-ambient-light band is unfair, not atmospheric.

## Production admission gate

Mirrors `structure_library/production-approvals.json`'s discipline exactly:
automatic validation never writes an approval, and a human-reviewed gate is
required before any Tier 3 structure or Tier 1/2 feature enters live world
generation. Required checks before admission:

`license_approved`, `normalized`, `fluid_and_atmosphere_state_validated`,
`render_reviewed_at_declared_depth_band`, `render_color_fidelity_verified`
(no uncalibrated/fallback colors in the evidence renders),
`size_and_silhouette_fitness_reviewed` (against the "Size and visual
composition audit" section above), `quality_threshold_passed`,
`metadata_complete` (including depth band, build style, and access
connector), `rotation_and_terrain_placement_tested`,
`access_connector_tested_against_installed_submersibles`,
`exclusion_zone_validated_against_ocean_structure_sets_csv`.

## Diversity enforcement

Track architecture family independently of condition/occupation variants,
exactly as Phase 28 requires on land — variants of one wreck or one facility
design all belong to the same family, and worldgen must not over-repeat one
family merely because it has many derivative variants. This applies across
all three tiers: a trench system (Tier 1) with many vent-field variants
(Tier 2) is still one geological family.

## Performance budget

Underwater assets carry a cost land assets do not: waterlogged block state
and fluid-tick load. Measure and record, in addition to the land Phase 29
metrics (blocks placed, parsing, selection, chunk-generation time, memory):
the fluid-tick cost of any structure that creates new water/air boundaries
at generation time, and the terrain-carving cost of Tier 1 macro shaping
separately from Tier 3 structure placement cost — the two are not
comparable operations.

## Disposition ledger

`docs/DEEP_SEA_STRUCTURE_AUDIT.md` is the authoritative Stage-A-equivalent
ledger for this system, in the same format as
`docs/INBUILT_STRUCTURE_AUDIT.md`: one row per asset, with `Tier`,
`Depth Band`, `Build Style`, `Family`, `Profile`, `Size`, `Disposition`, and
`Audit Evidence`. A quarantined or rebuilt disposition there is a completed
audit, not a production approval — approvals live only in
`structure_library/production-approvals.json` (or its deep-sea equivalent,
once one exists).

## Initial reference wave

`infinite_domain:deep_sea/coastal_patrol_wreck` (Tier 3) and
`infinite_domain:deep_sea/coastal_patrol_debris_field` (Tier 2) are Wave 1:
the first assets authored against this standard, generated by
`scripts/generate_deep_sea_structures.py`, checked by
`scripts/validate_deep_sea_structures.py`, and rendered by
`scripts/render_deep_sea_review.py`. They play the reference role the
bungalow rebuild plays for the land corpus — later deep-sea assets should
match their lifecycle discipline and metadata completeness, not necessarily
their exact geometry. See `docs/deep-sea-structures.md` for what the wave
covers and `docs/DEEP_SEA_STRUCTURE_AUDIT.md` for its ledger entries. Both
assets are quarantined behind the empty
`#infinite_domain:disabled_quarantine_deep_sea_structures` biome tag and
have not had an in-game walkthrough.

Wave 3 added `akula_project971`, the corpus's first hero-scale asset: a 1:1
Project 971 Shchuka-B nuclear attack submarine (113 m) as an intact clean
master, plus the two-section shelf-break wreck derived from
`docs/deepsea-akula-impact-simulation.json`. It establishes three things this
standard did not previously have:

- **Damage may be derived rather than dressed.** Where a damage variant's
  cause is a discrete physical event, model the event first and author the
  geometry from it. The model must report what it rules out as well as what
  it produces, and must say plainly where it bounds a value rather than
  deriving it — `validate_deep_sea_structures.py`'s `_akula_impact_conformance`
  then checks the authored attitude against the model so the two cannot
  silently drift apart.
- **A hero asset may sit outside the size band table**, provided the ledger
  states the claimed band and the reasoning, as point 2 of the size audit
  already requires.
- **A site may be assembled from several pieces.** Where a single event
  produced more than one asset, they belong to one jigsaw structure so they
  generate together, rather than to separate structure sets that happen to
  place similar-looking things. `akula_wreck_site` is the reference: a start
  piece carrying the cause, children registered pool-only so they cannot also
  generate on their own, and a validator check that resolves the joints out of
  the shipped NBT. The mechanics and the pitfalls are in
  `docs/deep-sea-structures.md`.
- **Prefer the mechanism the site can show.** When more than one physical
  mechanism explains a damage state, the standards' requirement that damage
  trace back to one *legible* cause is a tiebreak, not just a description:
  choose the mechanism that leaves visible evidence in world, and record the
  ones ruled in or out so the choice is auditable.
- **A hero asset earns a fuller view set.** One fixed isometric angle cannot
  audit a 113-block hull. `scripts/render_deep_sea_review.py` now also emits
  port profile, bow-on elevation, plan, range silhouette, centreline cutaway
  and transverse frame sections, all under the asset's declared depth-band
  fog rather than the pipeline's default lighting — which this checklist has
  always asked for and the two-view pass could not deliver.

Three automated checks were added with it and apply corpus-wide, not just to
Wave 3: `_akula_structural_continuity` (no unsupported floating geometry),
`_akula_dressing_density` (point 6's density ceiling, measured against exposed
skin rather than judged by eye alone), and a duplicate-registrant check on
`ocean-structure-sets.csv`.

Wave 2 added `flooded_relay_shelter` (open_floor, pre_collapse_civilian_industrial)
and `abyssal_mining_rig`/`abyssal_vent_field` (deep_floor,
create_industrial_offshore). A subsequent size-and-visual-composition pass
across all nine assets found and fixed the render-color-fidelity defect and
the material-contrast defects described in "Size and visual composition
audit" above — see `docs/deep-sea-structures.md` for the specific fixes and
`docs/DEEP_SEA_STRUCTURE_AUDIT.md` for the updated ledger evidence.

## Repository conventions for new assets

- Deep-sea corpus assets live under `structure_library/` using the existing
  corpus layout (`sources/`, `variants/`, `reviews/`, `licensing/`) with a
  `deep_sea` category, rather than a parallel directory tree — this is one
  corpus, not two.
- Worldgen JSON, KubeJS placement scripts, and structure NBT are the only
  files this system should ever require; escalate to a project-owned
  companion jar only under the same bar `packdev/darknet-worldgen-patch`
  set — a genuine placement-code limitation, never convenience.
- Every new entry updates `docs/DEEP_SEA_STRUCTURE_AUDIT.md` and, where
  licensing applies, the shared provenance ledger — never silently.

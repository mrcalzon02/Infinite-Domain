# Infinite Domain — Terrain Affordance Guarantees and Spawn Separation for Scatter-Placed Structures

Status: **Phases 0 / 0.5 / 0.75 landed (data-only).** Scope decided 2026-08-26: **data-only, Phases 0–1.** The companion-mod options (A3, A4, B5) are **out of scope** and retained only as §11 (rejected-for-now). The numbers in §3–§4 are measured from the live pack on 2026-08-26. §5–§6 are the option analysis; §7 is the committed plan.

**2026-08-27 — the spawn-separation half of the trigger (a) is addressed for `wasteland/`.** The owner reported structures still generating on top of each other after Phase 0.5. Root cause: the §7.3 single-spine `exclusion_zone` hub only cleared ground around one structure; 29 other salted grids still overlapped each other, which is a within-set problem. Fix landed as **Phase 0.75 / B2 (§7.5)**: the 30 per-family wasteland sets are consolidated into 5 placement tiers, so `separation` now guarantees a minimum gap between any two members of a tier, with a shallow `exclusion_zone` chain between tiers. `minor/*` still awaits its own B2 pass. The seating half (trigger b) is still Phase 1.

Phase 0 changes landed against this document:
- separation raised on the densest wasteland and `minor/*` structure sets (§7 Phase 0, §3.2) — `scripts/generate_wasteland_sites.py` `FAMILIES`, `scripts/generate_minor_exoplanet_sites.py` `KIND_STEP`/`KIND_SEP`, and the emitted `structure_set` JSON.
- `scripts/validate_structure_seating.py` and `scripts/validate_structure_separation.py` added as **report-only** (no CI gate yet). Baseline output captured at `docs/structure-seating-audit.txt` and `docs/structure-separation-audit.txt`.
- A6 buried-regime list named (§5).

Phase 0 baseline findings (from the validators): 125 in-scope structures run `beard_box` on the `grade_y ≈ 1` assumption; 8 are on the A6 buried list; 0 footprint clips; 0 codec violations; 90/90 live in-scope structure sets carried no `exclusion_zone`. *(The cross-set overlap cause: Phase 0.5 added a single-spine hub §7.3, then Phase 0.75 §7.5 replaced it with the B2 tier consolidation — the `wasteland/` half is now fixed; `minor/*` still runs 36 independent grids.)*

Trigger: the "New World" playtest showed (a) custom scatter-placed structures generating on top of one another, and (b) the wasteland gas station standing on a pedestal above the surrounding terrain, its below-grade room at natural ground level and true grade several blocks higher.

---

## 1. Authority and precedence

| Rank | Source | Role |
|---|---|---|
| 1 | `old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md` | Immutable world facts. |
| 2 | `docs/WORLDGEN_STRUCTURE_SAFETY.md` | Existing worldgen-safety overrides. This document **extends** it: the flatness-radius rule already applied there to Seven Seas ships is generalised here. Any change here that touches a structure named in that file must be reflected back into it. |
| 3 | `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` | Geometry doctrine: real foundations, site-specific ground, edge transitions. A terrain-affordance rule must not contradict V2 §3 ("real foundations", "edge transitions"). |
| 4 | `docs/HEAVY_REBUILD_DOCTRINE.md` | Visual gates; a re-seated structure is re-reviewed at Gate A (massing/scale in situ). |
| 5 | **This document** | The seating contract, the separation contract, the validators, and the phasing. |
| 6 | `scripts/generate_wasteland_sites.py`, `scripts/generate_alien_structures.py`, `scripts/generate_minor_exoplanet_sites.py`, `scripts/generate_continuity_offworld_expansion.py`, `scripts/generate_continuity_offworld.py` | The generators that emit the affected files. They implement this document; they do not define it. |

Format precedent: `docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md`, `docs/ABYSSAL_OCEAN_PROGRAM.md`. Future work updates this file rather than forking it.

---

## 2. Scope

**In scope:** every `minecraft:jigsaw` structure under `kubejs/data/infinite_domain/worldgen/structure/` that is placed on the land surface by a `minecraft:random_spread` structure set — the "scatter-placed" corpus.

**Out of scope:**

- `abyssal/` (40) and `deep_sea/` (9) seabed structures. They already use `terrain_adaptation: bury` + `project_start_to_heightmap: OCEAN_FLOOR_WG` + `start_height {absolute: 32}` and are governed by `docs/ABYSSAL_OCEAN_PROGRAM.md` / `docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md`. Their regime works; changing it is a separate decision.
- `old_world/ows_*` (64). These have jigsaw JSON files but **no structure set references them** (only `old_world/controlled_pt9_probe` exists). They reach the world exclusively as Lost Cities buildings. They are dead weight for natural worldgen today — see open decision OD-5.
- Lost Cities city generation, Dungeons Arise, Spore, and third-party structure mods.

**Affected corpus (verified count, 2026-08-26):**

| Family | Count | Structure sets | Notes |
|---|---|---|---|
| `wasteland/` | 85 | **5 tiers** (was 30 sets), salts as §7.5 | The bulk of the problem. B2-consolidated 2026-08-27 (§7.5). |
| `minor/` | 36 | 36 sets (one per structure), large random salts | Moon/Mars/Venus/etc. waypoints, wrecks, caches, debris. Dense: spacing 22 / separation 9. B2 pass still pending. |
| `planetary/` | 10 | 10 sets, `*_minor_expansion` / `*_major_expansion` | Off-world expansion packs. |
| `alien/` | 5 | 5 sets, salts 73194511–73194515 | |
| `offworld/` | 4 | 4 sets | Continuity lunar/mercury/venus. |
| `nether/` | 1 | 1 set | `lyran_research`, `terrain_adaptation: none`. |
| **Total surface scatter** | **~141** | **~62 sets** (post-§7.5) | |

Total structure-set files in the pack: 113 (post-§7.5; was 139). Total custom structure JSONs: 254.

---

## 3. Problem 1 — structures with no separation from each other

### 3.1 What `random_spread` actually guarantees

`minecraft:random_spread` divides the world into a grid of `spacing`×`spacing` chunk cells. In each cell it picks one candidate chunk, constrained to be at least `separation` chunks from the cell edges (so from the candidate in the neighbouring cell). A per-set `salt` decorrelates one set's grid from another's.

**`separation` is within a single set only.** Two different sets have different salts and independent grids. Nothing in vanilla `random_spread` keeps set A's placement away from set B's placement unless set A declares an **`exclusion_zone`**.

### 3.2 Current state

- **No structure set in the pack uses `exclusion_zone`.** (Verified: zero matches across `kubejs/data/**/worldgen/structure_set/`.)
- ~87 surface sets run concurrently on the same land area with independent grids.
- The densest sets:

| Set | spacing | separation | structures |
|---|---|---|---|
| `wasteland/expanded_wilderness_roadside` | 16 | 6 | 5 |
| `wasteland/roadside_debris` | 18 | 8 | 3 |
| `wasteland/expanded_city_civic` | 22 | 8 | 5 |
| `wasteland/expanded_city_commercial` | 22 | 8 | 5 |
| `wasteland/expanded_city_residential` | 22 | 8 | 5 |
| `minor/*` (each) | 22 | 9 | 1 |
| `wasteland/expanded_city_transit` | 24 | 9 | 4 |
| `wasteland/expanded_city_utilities` | 27 | 11 | 5 |

With three `expanded_city_*` sets each on a 22/8 grid but decorrelated by salt, a civic ruin, a commercial ruin, and a residential ruin can all start within a few chunks of each other, none of them aware of the others. Multiply by ~87 sets and clustering is not a tail case, it is the expected texture of the surface. This is what the playtest showed.

*(Superseded for `wasteland/` by §7.5: the civic / commercial / residential ruins named above are now all members of one set, `wasteland_major`, so `separation` keeps them apart by construction. The table above is the pre-Phase-0.75 state, kept for the analysis it drives. `minor/*` still runs 36 independent grids and awaits its own B2 pass.)*

### 3.3 The `exclusion_zone` constraint that shapes the fix

`exclusion_zone` is a **single** object on the `placement`:

```json
"exclusion_zone": { "other_set": "<one structure set id>", "chunk_count": <1..16> }
```

- `other_set` is one set, not a list.
- `chunk_count` is 1–16 chunks (16–256 blocks); the check is against the *other set's* placement grid, evaluated deterministically at placement time.
- It is one-directional: A excluding B does not make B exclude A.

Because only one `other_set` is allowed per set, a full N×N "everyone avoids everyone" matrix is impossible in pure data. The realistic data-only shape is a **hub**: designate one "spine" set per tier and have lighter sets exclude the spine.

---

## 4. Problem 2 — structures not seated at terrain height

### 4.1 How a single-NBT jigsaw structure is positioned vertically (verified mechanics, MC/NeoForge 1.21.1)

Every affected structure is a **single rigid NBT**: `size: 1`, a start pool with one `minecraft:single_pool_element`, `projection: rigid`. There is no jigsaw assembly. Placement is:

1. `y0 = start_height` (for `{absolute: N}`, `y0 = N`).
2. The NBT bounding box is created with its origin corner at `y0`, so `box.minY = y0`.
3. If `project_start_to_heightmap` is set: `anchor = y0 + firstFreeHeight(footprintCentreX, footprintCentreZ, <heightmap>)`. One heightmap sample, at the footprint centre.
4. `groundRef = box.minY + element.getGroundLevelDelta()`.
5. The piece is moved vertically by `anchor − groundRef`.

Net result with heightmap projection:

```
final box.minY = y0 + H − groundLevelDelta
```

where `H` is terrain height at the footprint centre. So **NBT layer number `groundLevelDelta − y0` is the layer that ends up at terrain height `H`.**

### 4.2 `groundLevelDelta` cannot be set for these structures

- `getGroundLevelDelta()` for `minecraft:single_pool_element` returns the engine default (**1** in current versions). The datapack `single_pool_element` schema has no field for it.
- The structure `.nbt` format as written by the structure block does **not** contain a `GroundLevelDelta` tag. Verified directly: `ruined_gas_station.nbt`, `gas_station_clean_master.nbt`, and `abandoned_bungalow.nbt` all contain `size`, `palette`, `DataVersion` and **no `GroundLevelDelta`**.

So for the entire scatter corpus, `groundLevelDelta = 1`, always. The engine believes "natural ground is one block above the NBT origin" for every structure regardless of what was authored.

### 4.3 The Beardifier uses the same wrong reference

`terrain_adaptation` (`beard_thin`, `beard_box`, `bury`, `encapsulate`) runs during noise generation. It reads the **finished** structure piece bounding boxes. For beard modes, its ground reference plane is `box.minY + groundLevelDelta` — the same `box.minY` **after** the §4.1 move, plus the same `groundLevelDelta = 1`.

Consequence, and this is the crux:

> **`start_height` moves `box.minY` and the beard reference together. Changing `start_height` relocates the seating error; it can never correct it.** The beard is only aligned to the intended grade line of the build when `groundLevelDelta` equals the NBT layer index of that grade line. The datapack cannot make that true.

`beard_box` (used by nearly every surface structure here) conforms terrain over the **entire bounding-box footprint rectangle**. So any vertical error is expressed as a full-footprint rectangular platform or trench, not a soft blob — the worst possible way for the error to show.

### 4.4 Worked example — the gas station

`kubejs/data/infinite_domain/worldgen/structure/wasteland/ruined_gas_station.json`:

```json
"terrain_adaptation": "beard_box",
"start_height": { "absolute": -7 },
"project_start_to_heightmap": "WORLD_SURFACE_WG"
```

NBT size `39 × 28 × 45` (X×Y×Z). The `-7` is a hand-tuned fudge (it is **not** in the generator's `SURFACE_CUT_OFFSETS`, which only lists `abandoned_quarry: -12`, `collapsed_mine_entrance: -8`, `excavator_pit: -10` — the value was edited into the file directly).

- The build was authored with a below-grade room (fuel tanks / service pit) at the bottom of the box and the forecourt slab roughly 7 layers up.
- Placement: `final box.minY = −7 + H − 1 = H − 8`. The NBT origin sits 8 blocks below the surface sample.
- Beard reference: `box.minY + 1 = H − 7`.
- The Beardifier conforms the natural terrain across the full 39×45 footprint toward `H − 7`, roughly 6 blocks below the authored forecourt slab.
- Because the terrain is only sampled once (footprint centre) and then forced flat across the whole rectangle, on any slope, coast, or wherever the authored grade line is not exactly `origin + 1`, the building rises out of, or sinks into, a hard rectangular shelf. In the playtest it read as "raised": the tank room at natural ground level, the true grade a few blocks up, the forecourt floating over a bearded pad.

The `-7` "worked" in the sense that the slab lands near `H − 1`; it fails because the **beard reference is 6 blocks below the slab**, so the terrain blend happens at the wrong height and the footprint gets a rectangular scar instead of a graded transition.

### 4.5 Current per-structure seating knobs (for reference)

`generate_wasteland_sites.py` currently decides seating like this:

- `terrain_adaptation`: `"bury"` if the name is in `UNDERGROUND = {survivor_cache, bunker_network, collapsed_subway_station}`, else `"beard_box"`.
- `start_height`:
  - `SURFACE_CUT_OFFSETS` (`abandoned_quarry: -12`, `collapsed_mine_entrance: -8`, `excavator_pit: -10`) if listed;
  - `-17` for `bunker_network`, `-9` for `survivor_cache`;
  - otherwise a `minecraft:uniform` band `{absolute 18}..{absolute 34}` (for `UNDERGROUND` structures with no heightmap projection).
- `project_start_to_heightmap`: `OCEAN_FLOOR_WG` for `{hydroelectric_refuge_dam, warm_industrial_mountain_port, cold_industrial_mountain_port}`, else `WORLD_SURFACE_WG`, applied to every non-underground name.

There is no declared grade line, no validator on the offsets, and the values were tuned by eye. `scripts/structure_geometry_primitives_v2.py::terrain_footing()` already documents the honest position in its docstring for the `submerged` profile: *"actual world-height alignment happens at placement time and must be verified in-world, not assumed from local template coordinates."* That caveat is currently unenforced.

---

## 5. Part A — options for a Terrain Affordance Guarantee

Goal: every scatter-placed build meets the natural ground along its authored grade line, with a graded transition, not a rectangular shelf, and no floating or half-buried result on ordinary terrain.

### A1 — Grade-line seating contract (data only)

Declare, per structure, a `seating` block (§9.4). The full convention, formulas, footing rule, and audit procedure are in **§9** (OD-2 resolved: floor-flush). In short:

- `grade_y` = the interior walking-floor layer; `start_height.absolute = −grade_y` seats it flush at `H − 1`.
- Sub-grade anchoring is an explicit solid footing pad of ≤ 3 courses (§9.3); anything deeper or with a room below the floor goes to A6.
- Move `beard_box → beard_thin` (thin follows the base footprint; box paints the whole rectangle and is the main reason the error is so visible).

- **Pros:** pure data; deterministic; fixes the common case (slab-on-grade ruins, ~120 of ~141); cheap; no new mod.
- **Cons:** forbids sub-grade rooms in the naturally-placed variant (A6 takes them); one heightmap sample means slopes stay imperfect — with the flatness gate out of scope (§11), the only mitigations are A2 skirts and a generous `grade_y` tolerance; requires re-export of ~141 NBTs through the deterministic pipeline; `beard_thin` still cannot be *exactly* right because `groundLevelDelta` is still 1, not `grade_y` — it is only right because we force `grade_y ≈ 1`.

### A2 — Self-bearded NBT: bake the blend, `terrain_adaptation: none`

Every surface NBT gets a baked apron via `terrain_footing()`: a footing course, plus a feathered `coarse_dirt`/stone skirt ring 3–5 blocks past the footprint sloping from grade down to about −3. `terrain_adaptation: none`; the engine performs no terrain edit.

- **Pros:** total determinism; identical in every biome; no Beardifier behaviour to reason about at all; uses an existing V2 primitive; directly satisfies V2 doctrine ("real foundations", "site-specific ground", "edge transitions").
- **Cons:** the baked skirt is a fixed shape — it clips into a hill on the uphill side and floats on the downhill side, so without a flatness gate it needs a generous skirt and tolerance of some slope clipping; larger NBTs; re-export of all; still one heightmap sample.
- **Precedent:** the deep-sea Akula wreck already took this route for the same underlying reason. `scripts/generate_deep_sea_structures.py::register_akula_assembly` sets `terrain_adaptation: none` and its docstring records: *"the whole assembly shares ONE seabed datum, taken at the outcrop. On a steep slope a section can therefore end up higher or lower against the terrain than its own authored bed assumes … recorded in `docs/deep-sea-structures.md` rather than left for someone to rediscover in world."* A2 generalises that accepted trade-off to the land surface.

### A3 — Fix the anchor at the source with a companion mixin *(out of scope — see §11)*

Ship a mixin so `minecraft:single_pool_element` reads a `ground_level_delta` (or `infinite_domain:grade_y`) field from the structure JSON and returns it from `getGroundLevelDelta()`. Then `start_height: 0`, `terrain_adaptation: beard_thin`, and **both** the §4.1 solve and the §4.3 beard use the true grade layer.

- **Pros:** correct at the source; sub-grade rooms are allowed again; `beard_thin` finally behaves as designed; per-structure; deterministic; the data files stay legible (`grade_y` is a readable field). This is the only option that makes the mechanics actually correct rather than worked around.
- **Cons:** requires a Java mixin in a pack mod. `mods/infinite-domain-darknet-worldgen-1.8.0.jar` is the pack's mixin mod (NeoForge, `JAVA_21`, mixin config `infinite_domain_darknet_worldgen.mixins.json`) but **its source is not in this repo** — this means either locating that source, rebuilding it, or shipping a second companion mod. A build artifact, not a data edit; slow to iterate; harder to reverse.

### A4 — Placement flatness gate *(out of scope — see §11)*

Only allow a surface structure to start where the terrain under its footprint (sampled on a grid) varies by ≤ N blocks — exactly the rule `docs/WORLDGEN_STRUCTURE_SAFETY.md` already applies to Integrated Seven Seas ships ("an eight-chunk surface-height radius with at most one block of variation"). Needs a placement hook: a mixin into `StructureCheck` / `ChunkGenerator.tryGenerateStructure`, or a mod-provided structure type with a heightmap-variance predicate (vanilla has none).

- **Pros:** makes any beard or baked-skirt behaviour predictable by only ever seating on near-flat ground; thins spawns in mountainous biomes (probably desirable for ruined-city and roadside families); the same hook serves B5.
- **Cons:** needs code; reduces counts in hilly biomes; does nothing about the anchor by itself — it is a multiplier on A1/A2/A3, not a substitute.

### A4b — `isekai_api:grounded_template` — the flatness gate already ships

`isekai_api` (loaded: `isekai-api-2.1.0-neoforge-1.21.1.jar`) registers a `grounded_template` structure **type** that is exactly the A4 mechanism as data, no mixin to write. Codec:

```json
{
  "type": "isekai_api:grounded_template",
  "template": "infinite_domain:wasteland/ruined_gas_station",
  "clearance_above_fluid": 2,     // reject if the low corner is <= seaLevel + this
  "max_slope": 4,                 // reject if the 5-point surface sample spans more than this
  "vertical_offset": -3           // template Y=0 seats at centre-column surface + this
}
```

Behaviour (decompiled `GroundedTemplateStructure.findGenerationPoint`): samples `getFirstFreeHeight(WORLD_SURFACE_WG)` at the footprint centre and its four corners; if `max−min > max_slope` **or** `min ≤ seaLevel + clearance_above_fluid` it returns `Optional.empty()` (the start is skipped); otherwise the template is placed unrotated with its corner at `centreSurfaceY + vertical_offset`. No beard, no carve — it only ever seats where the ground already fits, and `vertical_offset` gives the sub-grade bite.

- **Pros:** no mod to build — it is a loaded dependency; deterministic; per-structure `max_slope` / `vertical_offset`; solves the buried-room case (`vertical_offset −7` buries the sump with terrain untouched) and the slope case (bad sites are skipped, not scooped) in one type; `GroundedTemplatePiece` is a plain `TemplateStructurePiece`. Structure sets reference it by id like any `Structure`.
- **Cons:** single template, **no rotation** (every instance faces the same way) and **no jigsaw** (single-piece only — fine for all ~141 scatter assets, which are already `size: 1` single-pool); skips spawn attempts on rough ground so counts drop in hilly biomes (same trade as A4, generally desirable); changes the structure `type`, so the seating validator and generators must learn it; `handleDataMarker` is a no-op so any NBT data markers are ignored; needs the standard in-world verification pass.
- **Status:** candidate for the Phase 1 universal path and for the gas-station / bank-vault durable decision. Not yet used anywhere in the pack.

### A5 — `terrain_matching` projection for thin/debris families only

Switch `projection: rigid → terrain_matching` on the start pool element for assets with ≤ ~3 blocks of vertical structure: roadside debris, wrecked vehicles, fences, barricades, road patches, cairns, small caches. Leave every building on `rigid`.

- **Pros:** those assets genuinely follow slopes; one-line change per file; no mod.
- **Cons:** only valid for flat/thin assets; `terrain_matching` shears anything with walls. Candidate list must be curated (roughly: `wrecked_sedan`, `delivery_van`, `battle_tank`, `radio_mast`, `martian_signal_cairn`, most `minor/*_debris`, `minor/*_wreck`).

### A6 — Formalise the buried regime for genuinely sub-grade structures

Bunkers, vaults, tank rooms, mine entrances, buried caches: `terrain_adaptation: bury`, deep negative `start_height`, a surface access stub baked into the NBT, and no expectation that the body meets grade. This is already what `bunker_network` (`-17`) and `survivor_cache` (`-9`) do; A6 makes it a **named list** with a rule and a validator, and moves any A1-incompatible structure onto it.

**The A6 buried list (Phase 0 baseline, from current hand-tuned offsets — Phase 1 `grade_y` audit may add to it):**

| Structure | current `start_height` | current `terrain_adaptation` | Phase 1 target |
|---|---|---|---|
| `wasteland/bunker_network` | −17 | `bury` | keep |
| `wasteland/survivor_cache` | −9 | `bury` | keep |
| `wasteland/collapsed_subway_station` | uniform 18–34 (no projection) | `bury` | keep (`underground_structures` step) |
| `wasteland/abandoned_quarry` | −12 | `beard_box` | keep — the scoop is the intended open pit |
| `wasteland/collapsed_mine_entrance` | −8 | `beard_box` | `bury`, or `none` if the shaft descends into undisturbed rock (ambiguous — owner call) |
| `wasteland/excavator_pit` | −10 | `beard_box` | keep — the scoop is the intended pit |
| `wasteland/ruined_gas_station` | −7 | **`none`** (Phase 0.5, §7.2) | **durable decision open:** keep `none`, or `isekai_api:grounded_template` (slope-gated, no scoop, loses rotation), or cut the sump and make it plain A1 |
| `wasteland/buried_bank_vault` | −7 | **`none`** (Phase 0.5, §7.2) | same decision as gas station |

Everything else in scope currently sits at `start_height 0` + `beard_box` (`grade_y ≈ 1` assumed) and is A1 territory.

- **Pros:** removes the hardest cases from the A1 contract; matches existing working behaviour.
- **Cons:** those structures become "find the hatch" content; a design choice per structure.

### Recommended A path (committed — data-only)

1. **A1** for every slab-on-grade ruin (Phase 1; data only, gated by the seating validator).
2. **A6** for the ~8 structures with real sub-grade content (Phase 1; includes resolving the gas station).
3. **A2 baked skirt** for the large landmark structures where the beard looks worst even after A1 (Phase 1, selective).
4. **A5** `terrain_matching` for the curated thin/debris list (Phase 1, optional).

**Open for Phase 1:** whether **A4b (`isekai_api:grounded_template`)** replaces A1+A6 as the universal path. It is data-only (the mod is loaded), fixes the slope case and the buried-room case together, and costs rotation variety + some spawn attempts on rough ground. If adopted it would be the default for every `size: 1` scatter asset, with A1/A2 kept only where rotation matters. This is the single biggest open call in the plan — see A4b and OD-7.

The **companion-mixin** path (A3 anchor fix, A4 gate) is still **not** taken — see §11 — but A4b delivers most of A4's value without it.

---

## 6. Part B — options for spawn separation

Goal: no two scatter-placed structures generate with overlapping or touching footprints; landmark structures get real breathing room.

> **Status:** the committed path for `wasteland/` is **B3 (Phase 0) → B2 (Phase 0.75, §7.5)**. B1 below is the option that was analysed and used only as the Phase 0.5 stopgap (§7.3, now superseded). `minor/*` still needs B2. The rest of §6 is the original option menu, kept for the reasoning.

### B1 — `exclusion_zone` hub (data only, vanilla)

Given the single-`other_set` constraint (§3.3): define ~4 tiers, designate one "spine" set per tier, and have every set in that tier and every lighter tier set `exclusion_zone.other_set` to the heavier spine.

| Tier | Example spine | `chunk_count` others use against it |
|---|---|---|
| Landmark (`hydroelectric_landmarks`, `lost_data_centers`, `ruined_city_landmarks`, `warm/cold_industrial_ports`) | a landmark set | 12 |
| Major (`major_settlements`, `military_remnants`, `mountain_military`, `forest_industry`, `expanded_city_*`) | `major_settlements` | 8 |
| Common (`residential_ruins`, `commercial_ruins`, `expanded_wilderness_*`, `rural_ruins`) | `commercial_ruins` | 5 |
| Micro (`roadside_debris`, `expanded_wilderness_roadside`, `minor/*`) | `roadside_debris` | 3 |

- **Pros:** pure data; deterministic; native; the generators already emit these files, so the arrays can be generated from a tier table.
- **Cons:** one-directional and one-target, so it only cleanly separates *across* tiers; same-tier different-set adjacency is not fixed by B1 alone (needs B2); `chunk_count 12` against a common spine can sterilise large areas near every landmark — needs tuning.

### B2 — Consolidate sets  ✅ **landed for `wasteland/` 2026-08-27 — see §7.5**

Collapse the ~30 wasteland sets into a handful (`wasteland_landmark` / `_coastal` / `_major` / `_common` / `_micro`), each holding many structures with weights. Per-structure biome targeting already lives on the structure's own `biomes` field (and `STRUCTURE_BIOME_TAGS`), not on the set, so the set does not need to be per-family. `separation` within each set then genuinely guarantees spacing within a tier. **`ChunkGenerator`'s weighted picker retries** the remaining members when a pick's biome does not match, so mixing biome-restricted members in one tier does not waste placement slots.

- **Pros:** far fewer knobs; spacing guaranteed within a tier by construction; kills same-tier overlap outright; then only a short B1 chain is needed between tiers.
- **Cons:** loses per-family `spacing`/`separation`/`frequency` dials and the per-set salt history; thins the surface (fewer, better-spaced structures — see the §7.5 density delta); `minor/*` (36 one-per-file sets) would need the same treatment per body (still pending).
- **As implemented (§7.5):** 5 tiers, not 4 — `wasteland_coastal` (dam + ocean ports) is split out from `wasteland_landmark` because it is an ocean/river placement regime with an unchanged large spacing. `minor/*` B2 deferred.

### B3 — Raise separation / stagger spacing on the densest sets (immediate stopgap)

Bump `separation` toward `spacing − 2` and nudge `spacing` apart on the ~12 sets in the §3.2 table. Data only, minutes of work, no new world needed to author.

- **Pros:** immediate reduction in the worst clustering; buys time for B1/B2.
- **Cons:** palliative; does not guarantee anything; cross-set overlap still possible.

### B4 — `frequency < 1.0` on the noisiest sets

Add `"frequency": 0.5`–`0.7` to `roadside_debris`, `expanded_wilderness_roadside`, `expanded_city_*`.

- **Pros:** trivially thins the surface; data only.
- **Cons:** probabilistic, not a separation guarantee; reduces content density everywhere, not just where it clusters.

### B5 — Placement veto hook (mixin) *(out of scope — see §11)*

The A4 hook, extended: at placement, query nearby saved structure references and cancel this start if any lies within a per-structure radius derived from both footprints. True cross-set, footprint-aware, per-structure radius. Needs the same companion mod as A3/A4.

### Recommended B path (committed — data-only)

1. **B3** on the densest sets (Phase 0, done — §7).
2. **B2** consolidation — **done for `wasteland/` (Phase 0.75, §7.5): 30 sets → 5 tiers with a depth-≤2 `exclusion_zone` chain between tiers.** `minor/*` per-body B2 still pending (Phase 1).
3. **B4** `frequency` trims — not needed so far; fold into per-tier `spacing` tuning after the in-world check.

---

## 7. Committed plan (data-only)

| Phase | Contents | Kind | Status |
|---|---|---|---|
| **0** | B3 separation raise on the densest wasteland + `minor/*` sets; A6 list named (§5); seating + separation validators added as **report-only** | data only | landed |
| **0.5** | Interim, landed 2026-08-26 after a New-World spot check still showed the gas-station scoop + heavy cross-set overlap: gas station + bank vault → `terrain_adaptation: none` (§7.2); single-spine B1 exclusion hub on all 30 wasteland sets (§7.3); spawn safe-zone biome shrunk from a 384² hard square to an r≈64 feathered disc (§7.4) | data only | landed |
| **0.75** | **B2 consolidation for `wasteland/` (§7.5), landed 2026-08-27 after the owner reported overlap still occurring.** The 30 per-family sets → 5 placement tiers (`wasteland_landmark` / `_coastal` / `_major` / `_common` / `_micro`); within-tier `separation` now *guarantees* a minimum gap between any two members; a depth-≤2 `exclusion_zone` chain replaces the §7.3 single-spine hub. `minor/*` B2 still pending. | data only (no NBT re-export) | landed |
| **1** | `grade_y` audit of all ~141 in-scope NBTs → `seating` block (§9); A1 applied via generators; A6 applied to the sub-grade list; A2 skirt for selected landmarks; A5 for the thin/debris list; `minor/*` B2 pass; validators switch to gating | data only, re-export of NBTs | not started |

All changes are **new-world-only**. Existing chunks keep their terrain and structures, exactly as stated in `docs/WORLDGEN_STRUCTURE_SAFETY.md`.

### 7.1 Phase 0 separation changes (landed)

`scripts/generate_wasteland_sites.py` `FAMILIES` — `(spacing, separation)` per family:

| Family | was | now |
|---|---|---|
| `roadside_debris` | 18 / 8 | 18 / 10 |
| `residential_ruins` | 32 / 13 | 32 / 15 |
| `ruined_city_blocks` | 28 / 11 | 30 / 16 |
| `ruined_city_streets` | 34 / 14 | 34 / 17 |
| `expanded_city_civic` | 22 / 8 | 24 / 13 |
| `expanded_city_transit` | 24 / 9 | 26 / 13 |
| `expanded_city_commercial` | 22 / 8 | 28 / 15 |
| `expanded_city_residential` | 22 / 8 | 32 / 17 |
| `expanded_city_utilities` | 27 / 11 | 28 / 15 |
| `expanded_wilderness_roadside` | 16 / 6 | 22 / 13 |
| `expanded_wilderness_rural` | 32 / 12 | 32 / 15 |
| `expanded_wilderness_extraction` | 36 / 14 | 36 / 17 |
| `expanded_wilderness_survival` | 34 / 13 | 34 / 16 |

The three `expanded_city_*` sets are deliberately staggered to spacings 24 / 28 / 32 so their salt-decorrelated grids also differ in period. Cross-set overlap is still possible — B1/B2 in Phase 1 is the actual fix.

`scripts/generate_minor_exoplanet_sites.py` — `KIND_STEP` / `KIND_SEP`:

| kind | was (step / sep) | now |
|---|---|---|
| `waypoint` | 26 / 10 | 30 / 13 |
| `wreck` | 22 / 9 | 26 / 12 |
| `cache` | 18 / 7 | 22 / 10 |
| `debris` | 24 / 10 | 28 / 12 |

`minor/*` structures are all 7–13 blocks, so their overlap is far less visually severe than the wasteland city sets; this is a light touch pending B2.

### 7.2 Phase 0.5 — gas station / bank vault seating (landed)

`scripts/generate_wasteland_sites.py` `BURIED_ROOM_SITES = {"ruined_gas_station", "buried_bank_vault"}`. Both keep `start_height.absolute = -7` and `project_start_to_heightmap = WORLD_SURFACE_WG` but move `terrain_adaptation: beard_box → none`.

Why: both NBTs carry a hollow room 6–7 layers below the ground-floor slab (gas station: fuel-tank sump under the forecourt at NBT layer 7, which is 99.9 % filled; vault: strongroom under layer ~8). With `beard_box` the Beardifier carves the **entire** 39×45 / 49×45 bounding-box rectangle down to `box.minY` (the room floor, ~`H − 8`), so the building ends up standing in an open rectangular scoop with natural terrain a storey above its slab — the "gas station on a pedestal" seen at spawn. `none` leaves the surrounding terrain intact, so the room is genuinely underground and the forecourt slab lands flush at `H − 1`.

Cost of `none`: no feathering, so on a slope steeper than ~2 the rigid forecourt slab clips the uphill side / oversails the downhill side. Acceptable for roadside/flat sites; the durable fix (a slope-gated placement, e.g. `isekai_api:grounded_template` with `vertical_offset −7`, or cutting the sub-grade room and treating it as plain A1) is a Phase 1 decision. `abandoned_quarry` / `collapsed_mine_entrance` / `excavator_pit` keep `beard_box` + negative offset — there the scoop **is** the intended excavation. Enforced by `validate_structure_placement_contracts.py` (`NO_BEARD_BURIED_ROOM`).

### 7.3 Phase 0.5 — B1 single-spine exclusion hub (SUPERSEDED by §7.5, 2026-08-27)

*Historical. The single-spine hub described here was replaced by the B2 tier consolidation in §7.5. Kept for context.*

`scripts/generate_wasteland_sites.py` `_exclusion_zone_for()`. All 30 wasteland structure sets except the spine carried:

```json
"exclusion_zone": { "other_set": "infinite_domain:wasteland/ruined_city_landmarks", "chunk_count": 8 }
```

`ruined_city_landmarks` (the toppled skyscraper) was the spine and carried **no** `exclusion_zone`, so the "excludes-against" graph was a DAG with the spine as a sink. Effect: a hard 8-chunk (128-block) clear radius around every landmark. **Why it was not enough:** vanilla `exclusion_zone` names exactly one `other_set`, so this cleared ground around *one* structure only. The 29 other independent salted grids still overlapped each other freely — a civic ruin on a commercial ruin, a house on a gas station — which is what the owner still saw in the New-World playtest. That is a within-set-separation problem, and it is only solvable by putting the structures in the same set: §7.5.

### 7.5 Phase 0.75 — B2 tier consolidation (landed 2026-08-27)

`scripts/generate_wasteland_sites.py`: the `FAMILIES` table (30 entries) and `_exclusion_zone_for()` are replaced by `TIERS` (5 entries). Emitted: 5 `structure_set/wasteland/*.json` (the 30 old files deleted); `docs/wasteland-site-manifest.json` `families` rewritten to the 5 tiers. **No NBT re-export** — this is a pure structure-set/manifest change, so it stays clear of the R-5 generator-drift blocker. The 5 JSONs + manifest were hand-synced to match the new generator logic exactly (Phase 0.5 precedent); a future clean `generate()` run reproduces them.

| Tier | Members | spacing / separation | salt | `exclusion_zone` |
|---|---|---|---|---|
| `wasteland_landmark` | 2 — `toppled_skyscraper`, `bombed_data_center` | 72 / 34 | 87130416 | — (sink) |
| `wasteland_coastal` | 3 — `hydroelectric_refuge_dam`, warm/cold `industrial_mountain_port` | 176 / 72 | 87130413 | — (sink) |
| `wasteland_major` | 50 — settlements, complexes, city blocks/streets, **all 30 `CITY_EXPANSION` buildings**, wind/solar farms | 24 / 14 | 87130404 | → `wasteland_landmark`, `chunk_count 8` |
| `wasteland_common` | 26 — houses, small commercial, farms, all roadside/rural/extraction/survival wilderness sites | 20 / 12 | 87130402 | → `wasteland_major`, `chunk_count 4` |
| `wasteland_micro` | 4 — `radio_mast`, `wrecked_sedan`, `delivery_van`, `battle_tank` | 12 / 7 | 87130401 | → `wasteland_major`, `chunk_count 2` |

**Why this fixes the complaint.** Every member of a tier now shares one `random_spread` grid, so `separation` guarantees a minimum gap of `separation × 16` blocks between *any two* of that tier's structures (not just same-family ones). Each tier's `separation` clears its largest member's footprint diagonal with margin: major 14 ch = 224 b vs a ~109 b max diagonal; common 12 ch = 192 b vs ~96 b; micro 7 ch = 112 b vs ~30 b. Same-tier interpenetration — the civic-on-commercial, mall-on-hospital case — is now impossible.

**Cross-tier** is the shallow `exclusion_zone` chain in the table: `major` vetoes a start within 8 chunks of a landmark, `common` within 4 chunks of a major ruin, `micro` within 2 chunks of a major ruin. `wasteland_landmark` / `wasteland_coastal` are sinks (no exclusion), so the graph is a DAG with max recursion depth 2 — bounded, no cycle.

**Biome targeting is unchanged.** It lives on each structure's own `biomes` field (from `STRUCTURE_BIOME_TAGS`), never on the set. When `ChunkGenerator` picks a weighted member whose biome does not match the candidate chunk, it removes it and retries with the rest of the tier, so a mountain-only or ocean-only member simply doesn't fire in the wrong place — the slot falls through to a member that fits.

**Density delta (intended).** Consolidation necessarily thins the surface — you cannot space 60–80-block buildings apart without fewer of them. `validate_structure_separation.py` reports wasteland start density **234.9 → 114.1** starts per 10,000 shared-ground chunks (≈ halved). If that reads too sparse in-world, the one knob per tier is `spacing` (lower = denser); `separation` and the `chunk_count`s are the anti-overlap knobs and should not go below the footprint-diagonal clearances above.

**Verify in-world on a fresh world** (standing worldgen rule): (1) no two wasteland structures interpenetrate; (2) landmarks sit in cleared ground; (3) the surface does not feel barren. Tune `spacing` per tier if needed.

### 7.4 Phase 0.5 — spawn safe-zone biome shrink (landed)

`datapacks/gradient_ocean_pack/data/custom_worldgen/worldgen/density_function/start_city_mask.json`. Was `min()` of four `isekai_api:step` axis cuts at x,z = ±192 — a hard-edged 384×384 axis-aligned square, every block of which routed to `infinite_domain:safe_zone`. Now:

```
clamp( (96 − distance_xz(0,0,0)) / 32 , 0, 1 )
```

Solid core (mask 1.0 → humidity forced to 2.0 → `safe_zone`) to r ≈ 64, linear feather to 0 at r = 96. Net: the `safe_zone` biome becomes a ~128-diameter disc (≈91 % smaller by area) that blends through a `wastelands:city` humidity ring into normal routing, instead of ending on a hard square line. r ≈ 64 still fully contains the 7×7-chunk admin spawn claim (±56). Tunables: the `96.0` (outer feather radius) and `0.03125` = 1/32 (feather width) constants. Audited by `audit_era0_pack_basics_quests.py::_safe_zone_is_compact_radial`. **Verify in-world before marking complete** (per the standing worldgen rule).

---

## 8. Validators

Every rule above is enforced by one of these. Names are proposed; none exist yet.

| Validator | Checks | State |
|---|---|---|
| `scripts/validate_structure_seating.py` | **Phase 0 (report-only, built):** for each in-scope `worldgen/structure/*.json` — flags `beard_box` combined with negative `start_height` (the mismatch signature); flags missing `project_start_to_heightmap` on a `beard_*` structure; flags `max_distance_from_center` below the NBT footprint half-diagonal or above 116; lists every distinct `(terrain_adaptation, start_height)` combination in use. **Phase 1 (gating):** a `seating` block (§9.4) is declared; `start_height.absolute == −grade_y`; the sub-grade layers `0..grade_y−1` are a solid footing pad of ≤ 3 courses with no void (else the name must be on the A6 buried list); `terrain_adaptation` matches `seating.beard`. | Phase 0 built |
| `scripts/validate_structure_separation.py` | **Phase 0 (report-only, built):** parse every `structure_set`; assert `spacing > separation ≥ 0`; list sets that share a `salt` (ignoring inert `"structures": []` sets); list sets with no `exclusion_zone`; per set, estimate mean spacing in blocks and flag any live set under a footprint-derived floor. **Phase 1 (gating):** every live set has an `exclusion_zone` at its tier spine or heavier; the aggregate per-chunk co-occurrence estimate is under budget. | Phase 0 built |
| `docs/structure-seating-world-validation.json` (in-world gate) | `/place` every in-scope structure in three reference sites — flat plains, hill flank, coast — record actual grade-layer world-Y vs local surface, and screenshot. Phase 1 completion is **not** claimed from a green script exit; this file must show the measured seating. (Per the standing "verify in-world, never assume from local template coordinates" rule.) | Phase 1 |

---

## 9. The seating-contract data model

### 9.1 `grade_y` — the definition (OD-2 resolved 2026-08-26)

**Convention: floor-flush.** `grade_y` is the NBT layer index of the **interior walking floor** — the slab a player stands on when they walk in from outside at natural grade. It is seated at world `Y = H − 1` (the layer the topmost natural ground block would otherwise occupy), so its top face is level with the surrounding surface. A player crosses the threshold without stepping up or down.

Rejected alternative: "seat one block into the ground" (`start_height = −grade_y − 1`). That sinks every build into a 1-block rectangular depression the beard then has to feather out of, and reads as a structure subsiding rather than sitting. The sub-grade anchoring it was after is delivered instead by the **footing rule** below, which is explicit and under the builder's control.

### 9.2 The formulas the generator applies

With `groundLevelDelta` fixed at 1 (§4.2) and `project_start_to_heightmap` set:

```
start_height.absolute = −grade_y
  ⇒ final box.minY = H − 1 − grade_y
  ⇒ NBT layer `grade_y` lands at world Y = H − 1        (floor flush)
  ⇒ the Beardifier's ground reference (box.minY + 1) = H − grade_y
```

For the common slab-on-grade ruin the floor is NBT layer 0, so `grade_y = 0` and `start_height = 0` — the value already on 122 of the 141 structures. The audit's job is to find the ~20 where the authored floor is *not* at layer 0 and give them the right negative offset.

### 9.3 The footing rule

Layers `0 .. grade_y − 1` (everything below the floor) must be a **fully solid footing pad of at most 3 courses** with no interior space, no rooms, no doorways. This pad is what sits below natural grade, gives the beard something to grip on a slope, and lets the build tolerate roughly `grade_y` blocks of downhill terrain fall before the floor edge is exposed.

- More than 3 solid sub-grade courses, or any room/void below the floor ⇒ the structure is **not** `surface` regime; it goes on the **A6 buried list** and is re-authored for `terrain_adaptation: bury`.
- `thin` regime (roads, aprons, vehicles, debris, cairns — the A5 list): `grade_y = 0`, no footing, `terrain_adaptation: none` or `beard_thin`; these want their bottom face flush, not a pad.

### 9.4 The `seating` block

One block, added to each structure's catalog / program entry (not invented per-generator):

```json
{
  "structure_id": "infinite_domain:wasteland/ruined_gas_station",
  "seating": {
    "grade_y": 0,
    "regime": "buried",            // "surface" | "buried" | "thin"
    "footprint": [39, 45],
    "footing_courses": 0,           // solid sub-grade pad depth; surface regime only, <= 3
    "beard": "bury",               // "beard_thin" (surface) | "none" (A2 / thin) | "bury" (A6)
    "notes": "tank room below grade; re-authored as a bury structure with a surface hatch"
  }
}
```

The generators read `seating` and emit `start_height` (`= −grade_y`), `terrain_adaptation` (`= beard`), and `project_start_to_heightmap`. No generator hand-codes an offset.

### 9.5 The `grade_y` audit rule (Phase 1)

For each in-scope NBT:

1. `B` = lowest Y layer whose solid fill over the footprint bounding box is ≥ 60%.
2. Walk up from `B`: while a layer is a full solid slab with no wall verticals, doorway gaps, or furniture, it is footing. `grade_y` = the first layer that is *not* footing — the layer where the building starts being a building.
3. `footing_courses = grade_y − B`. If `footing_courses > 3`, or any layer in `B .. grade_y − 1` contains a void/room, flag for A6.
4. The audit writes a proposed `seating` block per structure; a human ratifies the batch before any `start_height` changes (review-gated, per house rule).

---

## 10. Risks and open decisions

| # | Item | Notes |
|---|---|---|
| OD-1 | **Data-only vs companion mod.** | **Resolved 2026-08-26: data-only, Phases 0–1.** The mixin path (A3/A4/B5) is deferred to §11. Consequence accepted: sub-grade rooms are not allowed in naturally-placed variants (A6 covers them instead), and slope seating stays imperfect (mitigated by A2 skirts + generous `grade_y` tolerance, not eliminated). |
| OD-2 | ~~`grade_y` convention.~~ | **Resolved 2026-08-26: floor-flush** (§9.1). `grade_y` = interior walking-floor layer, seated at `H − 1`; `start_height = −grade_y`; sub-grade anchoring comes from an explicit ≤3-course solid footing pad (§9.3), not from engine burial. `validate_structure_seating.py` Phase 1 checks this exact rule. |
| OD-3 | **A2 skirt: which structures.** | Every landmark, or only the ones that visibly fail after A1? Deferred to Phase 1 in-world review. |
| OD-4 | ~~Consolidation cost.~~ | **Resolved 2026-08-27 — B2 landed for `wasteland/` (Phase 0.75, §7.5).** 30 families → 5 tiers (`landmark` / `coastal` / `major` / `common` / `micro`); per-structure `biomes` + `weight` preserved; per-family `spacing`/`separation`/`salt` folded into 5 tier values; a depth-≤2 `exclusion_zone` chain between tiers replaces the §7.3 single-spine hub. **R-5 sidestepped:** only the 5 `structure_set` JSONs and `wasteland-site-manifest.json` `families` were rewritten (hand-synced to the new `TIERS` table in the generator) — no NBT re-export, so no full `generate()` run. `minor/*` per-body B2 is still a later pass. Validators `validate_structure_placement_contracts.py` and `validate_structure_separation.py` both pass; wasteland start density 234.9 → 114.1 per 10k chunks. Needs the standard fresh-world visual check. |
| OD-5 | **`old_world/ows_*` (64 dead jigsaw JSONs).** | They carry no placement today. Delete them, or wire them into the surface scatter under this contract? If wired, they enter scope and the §2 counts grow by 64. |
| OD-6 | ~~`akula_wreck_forward` / `akula_wreck_site` share salt `48217706`.~~ | **Not a bug (verified 2026-08-26).** `akula_wreck_forward` and `akula_wreck_aft` are `retire_structure_set()` outputs with `"structures": []` — inert. An empty set places nothing regardless of salt. `generate_deep_sea_structures.py` lines 2747–2749. No change needed. |
| OD-7 | ~~Adopt `isekai_api:grounded_template` (A4b) as the universal path?~~ | **Recommended 2026-08-27: targeted A4b, not wholesale.** Keep A1 (rigid jigsaw + random rotation) as the default for buildings — losing rotation across ~120 repeatedly-seen structures is a bigger realism cost than imperfect slope seating. Use `grounded_template` surgically where it earns its keep: (a) the buried-room sites (gas station, bank vault) — replaces the §7.2 `none` stopgap and adds the slope/fluid gate; (b) structures whose whole point is a landform (`mountain_pass_terminator` → real passes only, see OD-8); (c) optionally the A5 thin/debris/vehicle list instead of `terrain_matching`. The Phase 1 `grade_y` audit then produces a `grade_y`/`beard_thin` block for most and a `grounded` block for that shortlist. |
| OD-8 | ~~`mountain_pass_terminator` is an orphan builder.~~ | **Resolved 2026-08-27: added to `mountain_military`.** It is a highway-closure checkpoint (jersey barriers, guard booth, rockslide) biome-locked to `wastelands:mountains`; `mountain_military` is the only family whose biome context already matches, and it reads as the fortified road approach to a mountain military zone. Its lowland twin is `military_checkpoint` in `military_remnants` — together they are the "wasteland highway is closed" pair, one per terrain type. **How it should seat:** it is the model A4b case — a pass is a flattish saddle between steep terrain, and `beard_box` (current) carves a rectangular shelf wherever it lands including mid-cliff. Switch it to `grounded_template` + `max_slope: 3` so it only generates in genuine passes (small, near-symmetric through-road → no rotation cost). |
| R-5 | **Generator drift + validator desync (found 2026-08-27).** | `scripts/generate_wasteland_sites.py` was already modified pre-session with a `RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS` pass (furnace/brewing_stand/anvil/… → `kubejs:ruined_*`) that has **not** been run or committed. ~180 wasteland NBTs + ~799 `lostcities/parts/converted/*` are stale against it. `validate_structure_programs.py` still asserts `minecraft:brewing_stand ≥ 10` for the hospital and fails (0) the moment the pass is active. Any full generator run — B2 included — must be preceded by: finish the ruined-blocks pass, update `validate_structure_programs.py` (and any sibling validators) to accept the `ruined_*` variants, then regenerate + commit outputs as one deliberate change. Phase 0.5's structure edits were kept minimal (NBT regen reverted) to stay clear of this. |
| R-1 | **`exclusion_zone chunk_count` max is 16 (256 blocks).** | A landmark spine at 12 against a common tier can leave large sterile rings. Model the sterile area before committing the Phase 1 tier table. |
| R-2 | **`beard_thin` "extends to where the final parts generate".** | For single-piece structures this is just the one box, so the warning is mild — but `max_distance_from_center` (currently 80 on almost everything) must still cover footprint + beard margin; the Phase 0 seating validator flags shortfalls. |
| R-3 | **Re-exporting ~141 NBTs in Phase 1.** | Any non-determinism in the exporter becomes a silent geometry regression. Tie the re-export to the determinism contract (`STRUCTURE_REBUILD_SYSTEM_V2.md` §C8) and diff block counts before/after. |
| R-4 | **Third-party ocean/lost-city structures are untouched.** | This contract does not coordinate with Dungeons Arise, Spore, or Lost Cities placement. Cross-program overlap (a wasteland ruin inside a Lost City chunk) is out of scope here. |

---

## 11. Rejected for now — the companion-mod path

Recorded so a future session does not re-derive it. **Not** scheduled.

- **A3 — `getGroundLevelDelta()` from JSON.** A mixin on `SinglePoolElement` (or a `StructureTemplate` load hook) so `ground_level_delta` becomes a per-structure datapack field, read by both the placement solve (§4.1) and the Beardifier (§4.3). This is the only change that makes `beard_thin` on a structure with a real basement actually correct.
- **A4 — flatness gate.** A mixin on `StructureCheck` / `ChunkGenerator.tryGenerateStructure` (or a mod-supplied structure type) that rejects a start where footprint terrain variation exceeds a per-structure budget. Generalises the Seven Seas ship rule in `WORLDGEN_STRUCTURE_SAFETY.md`.
- **B5 — placement veto.** The A4 hook extended to also reject a start within a footprint-derived radius of any existing structure of any set — an exact cross-set separation guarantee.

**Blocker:** the pack's mixin mod `mods/infinite-domain-darknet-worldgen-1.8.0.jar` (NeoForge, `JAVA_21`, config `infinite_domain_darknet_worldgen.mixins.json`, classes under `infinitedomain.darknet.mixin.*`) has **no source in this repository**. Taking this path requires either recovering that source or standing up a second companion mod, plus a build/test loop. If the mod path is ever revived, do it as its own change on top of a completed Phase 1, not instead of it — Phase 1 is still the right data layer underneath a mixin.

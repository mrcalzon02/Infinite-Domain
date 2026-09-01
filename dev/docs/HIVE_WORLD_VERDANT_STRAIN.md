# Infinite Domain — Hive World "Verdant Strain" (green Spore variants)

Status: **design contract + deterministic asset generators are implemented and
self-validating. The runtime — companion mod, hit-point handler, dimension-scoped
reskin, and spawn integration — is DEFERRED. `infinite_domain:hive_world` does
not yet exist as a loadable dimension (see `docs/Endgame.md`), so nothing in this
document has been observed in-world. No behavioural claim here is a measurement.**

Working name **"Verdant Strain"** is provisional and yields to the Phase 0
identity contract `EG-P00-S02-C0003` if that names the Hive World's infection
differently.

---

## 1. Authority and precedence

| Scope | Authority |
|---|---|
| This subsystem's design, roster, palette, hit-point rule, delivery split | `docs/HIVE_WORLD_VERDANT_STRAIN.md` (this file) |
| Hive World program, phases, gates, spatial contract, identity | `docs/Endgame.md` (**supersedes this file on any conflict**) |
| Base "Rot" infection in the Overworld (quests, loot, threat dossier) | `docs/SPORE_THREAT_QUESTS_AND_LOOT.md` (unchanged by this work) |
| Recolour + overlay rule as data | `docs/hive-strain/palette-map.json` |
| Generated roster | `docs/hive-strain/roster-manifest.json` |

This document is the **design input for Endgame checkpoint `EG-P06-S04-C0089`
(enemy roster)**. It does not redefine the Endgame program, its phase order, its
gate model, or Section 11's ledger. Where the Endgame coordinator later folds
this subsystem into the program, Section 12 gives the exact ledger text to apply;
this file does not edit `docs/Endgame.md` (Sections 4.2 / 5.5 make it
coordinator-serialized).

Future work updates this authority rather than forking it.

---

## 2. Status detail

| Deliverable | State | Location |
|---|---|---|
| Design contract | Implemented | this file |
| Recolour + overlay rule | Implemented | `docs/hive-strain/palette-map.json` |
| Roster manifest generator | Implemented, idempotent | `scripts/build_hive_strain_roster.py` |
| Texture generator (recolour + emissive overlay) | Implemented, idempotent, ~5 s | `scripts/generate_hive_strain_textures.py` |
| Asset validator (7 checks) | Implemented, passing | `scripts/validate_hive_strain_assets.py` |
| Recoloured texture set | Generated locally, **gitignored** (`build/hive_strain/`) | not distributed — see Section 11 |
| Companion mod (`packdev/hive-strain-patch/`) | **Not started** | Section 9 |
| Hit-point handler | **Not started** | Section 7 |
| Dimension-scoped reskin (renderer mixin) | **Not started** | Section 9 |
| Spawn placement / containment | **Not started** — open sub-decision | Section 8 |
| In-world / codec / performance validation | **Blocked** on the dimension existing | Section 10 |

---

## 3. Concept

The Hive World carries its own strain of the Rot: a **fleshy, deep-green
mycelial mutation** that never took hold in the Overworld's climate. It is the
same organism family — the same silhouettes, the same anatomy, the same
behaviours — grown wrong and grown tougher in a dead, toxic, enclosed world.

Player-facing reads:

- every mycelial red / crimson / magenta surface is instead a **deep-dark-green
  to bright-green** ramp (the flesh itself still reads as flesh);
- a faint **emissive green spore bloom** clings to the infested areas, with
  brighter sporulating flecks;
- the creatures are **three times as durable** as their Overworld counterparts;
- they exist **only** inside `infinite_domain:hive_world`.

Naming, lore, and faction text are original Infinite Domain work; no third-party
setting material is used.

---

## 4. Roster

The roster is **generated**, never hand-maintained:
`scripts/build_hive_strain_roster.py` → `docs/hive-strain/roster-manifest.json`.
Inputs: the 96 `spore:` ids in `docs/registry-inventory/entity-ids.txt`, the
six-band taxonomy transcribed from `kubejs/server_scripts/spore_analysis_samples.js`,
an explicit non-creature exclusion list, base health scraped from
`config/spore-startup.toml` + `config/spore-common.toml`, and the entity-texture
index of `mods/spore_1.21.1_2.2.0j_neo.jar`.

**All combat creatures receive a variant** (owner decision, 2026-08-27). Scope:

| Band | Creatures | Base HP | Verdant HP (×3) | HP resolved from config |
|---|---:|---|---|---|
| infected | 12 | 15–35 | 45–105 | 11 / 12 |
| evolved | 32 | 12–70 | 36–210 | 29 / 32 |
| hyper_evolved | 12 | 60–110 | 180–330 | 9 / 12 |
| organoid | 10 | 20–80 | 60–240 | 8 / 10 |
| calamity | 10 | 70–500 | 210–1500 | 9 / 10 |
| hivemind | 1 | 100 | 300 | 1 / 1 |
| **total** | **77** | | | **67 / 77** |

The 19 excluded ids are projectiles, thrown objects, detached boss body-parts
(`*_arm`, `*_head`, `*_seg`, `*_tail`), and pure FX entities (`spore:acid`,
`spore:bile`, `spore:wave`, `spore:illusion`, `spore:corpse_piece`,
`spore:arena_tendril`, `spore:tumoroid_nuke`, `spore:harpoon`, `spore:spit`,
`spore:thrown_*`). Full list in the manifest's `excluded_non_creatures`.

**10 creatures have `health_source: unresolved`** — the mod sets their health in
code, not config: `spore:busser`, `spore:nuclea`, `spore:brot`, `spore:hevoker`,
`spore:hvindicator`, `spore:reconstructor`, `spore:scent`, `spore:kraken`,
`spore:licker`, `spore:inf_diseased_villager`. This is **not a blocker**: the ×3 rule in Section 7 is a
multiplicative modifier on whatever `MAX_HEALTH` the entity actually has at
spawn, so an unresolved config value only means the spec's roster table can't
pre-compute the number. Resolving the remaining names is a documentation task
(**RV** — confirm against the running entity once the dimension exists).

`reskin: true` for every roster entry. The recolour pass (Section 5) processes
**all 364** entity textures in the jar regardless of the manifest's best-effort
`textures[]` field, so a creature whose texture name does not string-match its id
is still fully reskinned.

---

## 5. Palette contract

Rule file: `docs/hive-strain/palette-map.json` (`version: verdant-strain-palette-v1`).
Consumer: `scripts/generate_hive_strain_textures.py`. Validator:
`scripts/validate_hive_strain_assets.py` check 4 / check 7.

### 5.1 Mycelial band (what gets remapped)

A source pixel is remapped **only if** its HSV falls in the mycelial band:

- hue ∈ `[325°, 360°]` ∪ `[0°, 28°]` (saturated crimson / red / magenta-pink);
- saturation ≥ `0.30`;
- value ≥ `0.10`;
- alpha ≠ 0.

The saturation floor deliberately spares the **desaturated pinkish-grey infected
flesh** so the creature still reads as flesh. Bone, teeth, metal, leather-brown,
near-black, already-cool hues, and every transparent pixel are **copied
byte-identically** (validator check 4 enforces this: any modified pixel outside
the band is a failure).

### 5.2 Green ramp (what it becomes)

Remapped pixels are replaced by a 5-stop deep→bright green ramp, indexed by the
**source pixel's HSV value** (dark source → deep green, bright source → bright
green), linearly interpolated in 8-bit sRGB:

| t (source value) | hex |
|---:|---|
| 0.00 | `#071c0c` |
| 0.18 | `#0a2a12` |
| 0.45 | `#1f7a2e` |
| 0.72 | `#3fce43` |
| 1.00 | `#5bff3a` |

Alpha is preserved exactly. Every remapped output pixel must have hue within the
envelope `[95°, 150°]` (validator check 4). The ramp is monotonic in value
(validator check 7).

Output: `build/hive_strain/assets/infinite_domain/textures/entity/hive_strain/<same relative path>`.

---

## 6. Emissive overlay contract

Rule file: same JSON, `overlay` block. Output:
`build/hive_strain/assets/infinite_domain/textures/entity/hive_strain_glow/<same relative path>`.
A mostly-transparent RGBA image, identical dimensions to the base, intended for
`RenderType.entityTranslucentEmissive` (companion mod, Section 9).

| Layer | Where | ARGB |
|---|---|---|
| `growth_glow` | every pixel that was inside the mycelial band | `0x3341ff52` (alpha 20 %) |
| `spore_speckle` | `⌊w·h / 23⌋` deterministically sampled pixels | `0x9963ff4a` |
| `spore_core` | `⌊w·h / 211⌋` deterministically sampled pixels, drawn last | `0xc0b6ffa0` |

**Determinism:** `random.Random(fnv1a_32(relative_texture_path))` — a fixed-seed
Mersenne Twister, reproducible across runs, machines, and Python builds. `glow`
comes from the band mask; then the speckle stream draws indices via
`rng.randrange(w*h)`; then the core stream continues the same RNG. No wall-clock,
no OS entropy.

**Budgets (validator check 5):**

- `growth_glow` coverage ≤ the mycelial-band pixel fraction (it is a strict
  subset of the recoloured area, and may legitimately cover a whole
  heavily-infested texture such as `worm_innards.png`);
- `spore_speckle` + `spore_core` combined ≤ `0.09` of the texture;
- the overlay contains only the three declared ARGB values plus full
  transparency.

---

## 7. Hit-point rule

**×3 max health**, in `infinite_domain:hive_world` only. Runtime, deferred.

Intended implementation (companion mod, Section 9; a KubeJS fallback is possible
but weaker):

1. On `EntityJoinLevelEvent` (or KubeJS `EntityEvents.spawned`), if
   `entity.level().dimension()` is `infinite_domain:hive_world`, `entity` is an
   `net.minecraft.world.entity.Mob`, and its type namespace is `spore`:
   - attach a **transient** `MAX_HEALTH` attribute modifier with a fixed UUID,
     operation `MULTIPLY_TOTAL`, amount `+2.0` (net ×3);
   - set current health to the new maximum;
   - write a persistent `hive_strain` flag (NBT / attachment) so the client
     reskin (Section 9) and any later logic can key on the entity itself rather
     than re-checking the dimension every frame.
2. **Re-assert on the entity's first server tick.** Fungal Infection: Spore is an
   MCreator mod; several creatures set their own `MAX_HEALTH` in an
   initial-spawn procedure that can run *after* `EntityJoinLevelEvent`. A
   transient modifier survives a `setBaseValue`, but a full attribute-map rebuild
   or a later `setHealth` clamp would not — one re-assert on tick 1 covers this.
   **RV.**

Interaction notes:

- **Stacks multiplicatively** with the mod's own `Global Health Modifier`
  (`config/spore-common.toml`, currently `1.0`). If that is ever raised, Verdant
  HP scales with it — intended.
- **Independent of** the mod's hard-mode *damage* cap (that caps outgoing/incoming
  damage on evolved/hyper creatures; it does not touch `MAX_HEALTH`).
- **Evolution is automatic:** when an infected evolves, Spore replaces the entity;
  the replacement fires a fresh join event in `hive_world` and is re-buffed.
- **Calamity ×3 is large** (`spore:howitzer` 500 → 1500, `spore:leviathan`
  450 → 1350). Section 10 flags a balance-pass dependency on `EG-P06-S08-C0098`;
  the multiplier is a single constant in `palette-map.json`
  (`hit_points.multiplier`) and the eventual handler, easy to retune per band if
  the playtest demands it.

---

## 8. Spawn and containment rule

**The variant is not a new entity type.** "Verdant Strain X" is exactly
"`spore:X` while in `infinite_domain:hive_world` / carrying the `hive_strain`
flag" — a dimension-conditional reskin + buff. Consequences, guaranteed by
construction:

- the green look and the ×3 HP **cannot leak to the Overworld**;
- the Overworld's red Rot **cannot leak into the Hive World** as a base entity,
  because nothing spawns `spore:` mobs there except the mechanism chosen below.

`config/spore-startup.toml` `[Spawns]` is **global and biome-tag-gated**
(`minecraft:is_overworld` allow, `c:is_cold` / `minecraft:deep_dark` deny) and
does **not** currently include any Hive World biome, so base Spore natural
spawning will not reach `hive_world` on its own.

**Open sub-decision for `EG-P06-S04-C0089` / `EG-P06-S04-C0090`:**

| Option | Notes |
|---|---|
| **A. Companion-mod stratum spawn handler** (recommended) | Spawns curated roster bands per Hive vertical band (Sump/Underhive/Forge/Hab/Monumental/Spire), tied to the encounter grammar `C0090`. Full control; every spawn is tagged on the spot. |
| B. Add a Hive biome tag to Spore's `[Spawns]` allow-list + tag Hive biomes | Edits a third-party mod's config for global behaviour; risks bleed; still needs the tagging pass for the reskin. Not preferred. |
| C. Datapack structure spawners inside Hive structures | Works for fixed encounters; does not populate open traversal. Could complement A. |

**Also open:** whether base Spore *mechanics* — block-infection spread, raids,
calamity chunk-loading, the Proto World Modifier — are **suppressed**,
**re-themed green**, or **left off** in `hive_world`. Recommendation: suppress the
world-altering mechanics (block infection, Proto World Modifier) and keep only
deliberate, placed encounters, so the Hive World's authored geometry is not
overwritten. Decide at `C0089`.

Green theming of infection **blocks and particles** (mycelium / biomass / spore
FX in `hive_world`) can reuse the Section 5 recolour over
`assets/spore/textures/block/` and a green spore particle colour. Noted as a
**candidate sub-checkpoint**, not built here.

---

## 9. Delivery architecture

A new companion module **`packdev/hive-strain-patch/`**, built and shaped exactly
like `packdev/darknet-worldgen-patch/` (`scripts/build_darknet_worldgen_patch.ps1`
is the build template: direct `javac` against
`C:\Users\Admin\curseforge\minecraft\Install\libraries`, jar → `mods/`).

| Component | Mirrors | Responsibility |
|---|---|---|
| `HiveGuard.isHiveWorld(level)` | `darknet/DarknetGuard.java` | single dimension check |
| `HiveStrainTextures.digitize(rl)` | `darknet/DarknetDragonTextures.java` | `spore:textures/entity/<p>` → `infinite_domain:textures/entity/hive_strain/<p>` |
| `mixin/EntityRenderDispatcherMixin` **or** a `getTextureLocation` mixin on Spore's renderers | `darknet/mixin/EntityRenderDispatcherMixin.java`, `EnumDragonTexturesMixin.java` | swap the base texture path for `hive_strain`-flagged entities |
| `client/HiveStrainOverlayLayer` + `mixin/LivingEntityRendererMixin` | `darknet/client/DarknetEntityOverlayLayer.java` (`RenderType.entityTranslucentEmissive`) | draw the `hive_strain_glow` emissive layer |
| server `EntityJoinLevelEvent` handler | — | the Section 7 HP rule + `hive_strain` flag |
| (optional) stratum spawn handler | `darknet/entity/DarknetFaunaRules.java` + `RegisterSpawnPlacementsEvent` | Section 8 option A |

Client texture root (parallel, UV-identical to `spore`):
`assets/infinite_domain/textures/entity/hive_strain/…` and `…/hive_strain_glow/…`.

**KubeJS fallback (HP only):** `kubejs/server_scripts/hive_strain.js` using
`EntityEvents.spawned` — mind the KubeJS-2101 gotchas documented in
`kubejs/server_scripts/spawn_hub_hostile_protection.js` (`level.dimension` is a
**property**; `EntityType#getCategory` is unavailable — test the Java `Mob`
class). This cannot do the reskin; a companion mod is required for that.

---

## 10. Build, determinism, and validation

```bash
python scripts/build_hive_strain_roster.py       # -> docs/hive-strain/roster-manifest.json
python scripts/generate_hive_strain_textures.py   # -> build/hive_strain/  (gitignored, ~5 s)
python scripts/validate_hive_strain_assets.py      # 7 checks; exit 0 = pass
```

All three are deterministic and idempotent — a second run on the same repository
state produces byte-identical output.

`scripts/validate_hive_strain_assets.py` (imports its band-mask logic directly
from the generator so the two can never diverge):

| # | Check |
|---|---|
| 1 | every roster id exists in `docs/registry-inventory/entity-ids.txt` |
| 2 | no excluded (projectile / body-part / FX) id leaked into the roster |
| 3 | every roster texture path exists in the installed Spore jar |
| 4 | each base PNG: size == source; pixels outside the mycelial band byte-identical to source; recoloured pixels within the `[95°,150°]` hue envelope; alpha channel unchanged |
| 5 | each glow PNG: size == base; only the 3 declared ARGB values + transparency; speckle+core ≤ 9 %; glow wash ⊆ band |
| 6 | idempotence — re-running the generator reproduces byte-identical output |
| 7 | `palette-map.json` self-consistency (ramp monotonic 0→1 and in value; hue ranges valid; overlay periods > 0; seed formula present) |

**Deferred / blocked validation (needs `infinite_domain:hive_world` to exist):**

| Axis | Why blocked | Target checkpoint |
|---|---|---|
| Reskin only inside `hive_world`, no Overworld bleed | no dimension | `EG-P06-S04-C0089` |
| ×3 HP applied and surviving MCreator health procedures | no dimension | `EG-P06-S04-C0089` (RV) |
| Evolution / calamity re-buff | no dimension | `EG-P06-S04-C0089` |
| Spawn placement, containment, mechanics suppression | open sub-decision | `EG-P06-S04-C0089` / `C0090` |
| Encounter density and per-band balance of ×3 | no dimension | `EG-P06-S05-C0090` / `EG-P06-S08-C0098` |
| Overlay render cost on the large calamity atlases (`adapted_hohl_head.png` is 2048², `gazen.png`/`graken.png` ~350 KB) | no dimension | `EG-P06-S04-C0089` performance audit |
| Quest integration (native `hive_world` kill tasks) | no dimension, and depends on the Overworld quest refactor | `EG-P06-S08-C0097` |

---

## 11. Risks and open decisions

| # | Item | Disposition |
|---|---|---|
| R1 | **Texture-derivative licensing.** The recoloured PNGs are derivative works of Fungal Infection: Spore art (author *the_harbinger69*). | Owner decision 2026-08-27: **generate locally, gitignore** (`build/hive_strain/`), do not distribute, pending the author's written permission — same treatment as `resourcepacks/`. The `packdev/darknet-worldgen-patch` precedent commits similar derivatives but only under an explicit reuse grant (`DARKNET-ASSETS-LICENSE.md`). **A Verdant Strain release requires an equivalent grant or a from-scratch texture pass.** |
| R2 | **MCreator fragility.** Spore's renderer internals, per-creature health procedures, and evolution entity-swap are all bespoke MCreator code and can change between mod versions. | The reskin mixin targets vanilla `EntityRenderDispatcher` / `LivingEntityRenderer`, not Spore classes, to minimise coupling (Darknet does the same). HP re-assert on tick 1 (Section 7). Pin the Spore version in the companion module's notes; re-run the validator after any Spore update. |
| R3 | **10 unresolved config health values** (Section 4). | Not blocking — the ×3 modifier is value-agnostic. Resolve the config-section↔id map as an RV documentation task. |
| R4 | **Calamity ×3 magnitude** (up to 1500 HP). | Single constant, retunable per band at `EG-P06-S08-C0098`. |
| R5 | **Overlay cost on large atlases.** | `entityTranslucentEmissive` is one extra pass; measure on `adapted_hohl_head.png` (2048²) during the `C0089` performance audit. Speckle budget (≤ 9 %) keeps overdraw bounded. |
| R6 | **Spawn / mechanics containment** (Section 8). | Open sub-decision for `C0089` / `C0090`. Recommendation recorded: companion-mod stratum spawner + suppress world-altering Spore mechanics in `hive_world`. |
| R7 | **Dimension does not exist.** | Entire runtime is deferred; this pass ships only the design contract and the deterministic asset pipeline, which are useful and verifiable now. |
| R8 | **Infection blocks / particles not themed.** | Candidate sub-checkpoint; recolour tooling already covers `textures/block/`. |

---

## 12. Proposed `docs/Endgame.md` ledger wiring (for the coordinator to apply)

This file does **not** edit `docs/Endgame.md`. When the Endgame coordinator
reaches Phase 6, the following belongs in the `EG-P06-S04-C0089` checkpoint
record:

> **Design input:** `docs/HIVE_WORLD_VERDANT_STRAIN.md` — the "Verdant Strain"
> green Spore-variant contract (roster of 77 combat creatures, deterministic
> recolour + emissive-overlay pipeline, ×3 hit-point rule, dimension-conditional
> reskin with no new entity types). Deterministic generators and a 7-check
> validator are already implemented under `scripts/*hive_strain*` and
> `docs/hive-strain/`. Outstanding for `C0089`: companion module
> `packdev/hive-strain-patch/`, the HP handler, the renderer texture-swap +
> overlay mixins, the spawn/containment sub-decision, and all in-world
> validation. Blocked on Phase 1 delivering the dimension. Licensing hold on the
> recoloured textures (R1).

No new checkpoint id is proposed; the work fits inside `C0089`'s stated scope
("role-based enemies by stratum and hazard compatibility | registry, spawn,
performance, and encounter audit").

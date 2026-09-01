# Gemstone Glitter Effect

*Authority document. Added 2026-08-27.*

Gemstone blocks and gem ore blocks from **More Ores More Gems** (`more_ores_more_gems`)
carry a **pulsing, erratic emissive "glint"** — a few pixels on the gem surface
twinkle on their own irregular cadence, so the block appears to catch and throw
light. This is a **render-only** effect: it does **not** change the block's light
emission, so it costs the lighting engine nothing and cannot be toggled by
redstone (see *Why render-only* below).

## Scope

Driven deterministically from the tracked More Ores More Gems texture pipeline:

| Set | Source of truth | Count |
|---|---|---|
| Gem ore blocks | `docs/more-ores-more-gems-derived-textures.csv` rows whose `Method` names the *generic gem containment* machinery | 63 |
| Gem storage blocks | `docs/more-ores-more-gems-texture-scope.csv` category `gem_storage_block` | 45 |
| **Total** | | **108** |

**Excluded** (not gemstones): all metal ores (the 71 *metallic ore container*
rows), `blockof_titanium` (a metal storage block mis-categorised upstream as
`gem_storage_block`), gem *items* (handled by their own texture pass; a dropped
item does not need the block effect), and every non–More Ores More Gems gem block
(vanilla `amethyst_block`, `iceandfire:sapphire_block`, …). Extending to those is
a one-line change to `GEM_STORAGE_EXCLUDE` / a second namespace block in the
generator if wanted later.

## Mechanism

Two things per block, both emitted into the project resource overlay
`kubejs/assets/more_ores_more_gems/`:

1. **Glint sprite** — `textures/block/glint/<sprite>_glint.png`, a 32 px,
   6-frame vertical strip. Every frame is fully transparent except for a handful
   of bright twinkle pixels. Paired `.png.mcmeta` uses `interpolate: true` and an
   **irregular per-frame `time` list** (seeded per block) so no two gems pulse in
   lockstep — collectively "erratic".

2. **Model override** — `models/block/<model>.json`, replacing the mod's
   `cube_all` model with a two-element cube:
   - element 1: the **original** texture, normal lighting, `cullface` on all six
     faces (unchanged look, still occludes neighbours);
   - element 2: the **glint** texture, pushed `0.008` proud, `shade: false`,
     `"neoforge_data": { "block_light": 15, "sky_light": 15 }` on all six faces
     → the twinkle pixels render full-bright regardless of surrounding light.
   - whole model `"render_type": "cutout_mipped"` (needed for the transparent
     glint layer; the opaque base renders identically to `solid`).

The base texture, its `.mcmeta`, and every file under
`resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/` and
`docs/more-ores-more-gems-derived-textures.*` are **not touched**.

### Precedent

`ae2lt` (Applied Energistics 2 Lots, in `mods/`) ships exactly this face data
(`neoforge_data.block_light`) for its controller "on" models, and the project
already ships cross-namespace animated `.png.mcmeta` overrides for AE2's spatial
anchor in `kubejs/assets/ae2/`. This effect is the two combined.

## Why render-only (not a real light)

A redstone lamp swaps between two block-states with different
`lightLevel(...)` values defined **in Java**. A data/resource pack cannot add a
light level, a block-state, or tick logic to another mod's block — that needs a
custom mod or a mixin. And a light that actually *flickers* forces a full
block-light re-flood every few ticks for every such block in view; a cave wall of
flickering gem ore would stutter. Nothing in vanilla flickers world light for
this reason. The emissive-face approach gives the *look* of a flickering glow
with zero lighting-engine cost. A fixed, non-flickering light level would be
cheap and safe but still needs a mod — out of scope here.

## Determinism

- Per-block seed: `blake2b(texture_id, digest_size=16)`. Everything random
  (twinkle site count, positions, phases, widths, hue jitter, the mcmeta `time`
  list) is drawn from a `random.Random` seeded with that digest. No wall-clock,
  no dict-order dependence (targets are sorted).
- Regenerate: `python scripts/generate_gemstone_glitter.py`
- Verify: `python scripts/validate_gemstone_glitter.py` — checks every target has
  a sprite + mcmeta + model, strip height = `32 * frames`, mcmeta frame indices
  in range, model references the right sprite and preserves the upstream base
  texture, no stray files in the overlay dir, and that re-running the generator
  in-memory reproduces identical **pixels** for every sprite (encoder-agnostic).
- Manifest with SHA-256 of every emitted file: `docs/gemstone-glitter-manifest.json`.

## Parameters

Constants at the top of `scripts/generate_gemstone_glitter.py`:

| Name | Default | Meaning |
|---|---|---|
| `GLINT_RES` | `32` | sprite edge px |
| `FRAMES` | `6` | animation frames per sprite |
| `SITES_BASE` / `SITES_JITTER` | `8` / `3` | twinkle sites per block = base + `rng(0..jitter)` |
| `GLINT_BLOCK_LIGHT` / `GLINT_SKY_LIGHT` | `15` / `15` | emissive level of the glint layer |
| `STORAGE_BASE_BLOCK_LIGHT` | `0` | optional faint glow on the *base* of storage blocks (0 = off) |
| `PROUD` | `0.008` | how far the glint cube sits proud of the base cube |
| `MCMETA_STEPS` | `10` | length of the irregular `time` list |

## In-game verification (not machine-checkable)

1. The **KubeJS resource pack must win the model override** over the mod jar.
   It loads above mods by default; confirm a gem block shows the twinkle. If not,
   the fix is pack ordering, not the assets.
2. **Emissive faces must render bright under Sodium** (0.8.12, NeoForge). The
   `ae2lt` controller blocks are the reference — if they glow, these will.
3. Eyeball a storage block and a gem ore in a dark room and in daylight; tune
   `SITES_*` / `FRAMES` / `MCMETA_STEPS` if the pulse is too busy or too sparse.

## Files

```
docs/GEMSTONE_GLITTER_EFFECT.md                        this document
docs/gemstone-glitter-manifest.json                    generated: sha256 of every emitted file
scripts/generate_gemstone_glitter.py                   generator
scripts/validate_gemstone_glitter.py                   validator
kubejs/assets/more_ores_more_gems/models/block/*.json          108 model overrides
kubejs/assets/more_ores_more_gems/textures/block/glint/*.png    108 glint strips
kubejs/assets/more_ores_more_gems/textures/block/glint/*.png.mcmeta
```

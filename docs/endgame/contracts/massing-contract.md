# Endgame — massing contract (P02 candidate)

**Authority:** `docs/Endgame.md` §3, §2.2, §2.3; `docs/endgame/contracts/spatial-metrics.md`;
`docs/endgame/adr/ADR-0001`.
**Status:** authored 2026-08-27 by owner direction, ahead of Phase 2. This is the spec
the **P02-GATE** freezes. It is formally adopted as `EG-P02-S01-C0025` (slice contract)
when Phase 2 opens; until then it is a working contract the spike is measured against.
**Validated by:** `scripts/endgame/validate_hive_world_smoke.py` assertions 4/9,
in-client probes from `docs/endgame/test-strategy.md`.

The purpose of freezing the massing is to give generator work (Phase 3, `C0037` onward)
a fixed target: once P02-GATE accepts, the Y bands, seam widths, mass ceiling, sealed
edges, and carve-fraction envelopes below **do not move** — Phase 3 tunes *within* them.

---

## 1. Vertical datum and bands (candidate-frozen)

From `spatial-metrics.md`, pinned here as the massing target:

| # | Band | Y range | Height | Band datum (nominal working level) | Seam zone at the upper boundary |
|---|---|---:|---:|---:|---:|
| 1 | The Drown | `-64..-33` | 32 | `-48` | 6-10 blocks |
| 2 | The Underworks | `-32..47` | 80 | `0` | 8-16 blocks |
| 3 | The Furnace Tiers | `48..111` | 64 | `72` | 8-16 blocks |
| 4 | The Billet Decks | `112..191` | 80 | `144` | 8-16 blocks |
| 5 | The Vaulting | `192..255` | 64 | `216` | 8-12 blocks |
| 6 | The Crown | `256..319` | 64 | `288` | n/a (world roof) |

- The **band datum** is the Y a module family's ground floor sits on and the Y a
  cross-band route is measured from.
- A **seam zone** is a band-transition region that reads as an architectural join
  (a plant deck, a rubble choke, a transit interchange) — authored at `C0053`/`C0065`,
  not a hard plane.
- Bands tile `-64..319` exactly (32+80+64+80+64+64 = 384).

## 2. The mass model (candidate-frozen envelopes)

The generator produces one **solid engineered mass** and carves voids out of it
(`generate_hive_world_density.py`). Every parameter below is an envelope; Phase 3
picks the value, P02-GATE freezes the envelope.

| Parameter | Envelope | Spike value | Role |
|---|---|---|---|
| `mass_ceiling` | `Y 280..300` | 292 | top of the buildable mass; above it is open to the roof |
| `roof_seal` | top `10..20` blocks are bedrock | ~14 (Y306-319) | the sealed cap; nothing breaches it |
| `floor_seal` | bottom `9..18` blocks always solid | ~9 (Y-64..-55) | no void reaches the world floor |
| `network` carve fraction | `8..18 %` of mass volume | ~ (untuned) | informal, "choked" circulation |
| `network` clear width | commonly `3..7` blocks | noise-driven | per `spatial-metrics.md` §3 |
| `shaft` bore | `4..9` blocks | ~5-7 | formal vertical circulation |
| `shaft` reachability | a shaft within `~64` blocks horizontal of any point in a core | noise density | per `spatial-metrics.md` §3 cadence |
| `hall` band | inside The Vaulting (`192..255`) | Y~200-244 | the monumental release space |
| `hall` min open dimension | `>= 48` blocks | window × noise | per `spatial-metrics.md` §4 |
| `hall` sightline | `>= 120` blocks | untuned | per `spatial-metrics.md` §4 |
| `hall` column spacing | `12..24` blocks | column noise | keeps the hall from being a plain box |

**Combine rule (frozen shape):**

```
final_density = max(
    min( mass, network_keep, shaft_keep, hall_keep ),
    roof_seal,
    floor_seal
)
```

where each `*_keep` field is `+1` (solid) except `-1` (void) in its carved region.

## 3. Deferred to Phase 3 — the macro layer (ADR-0001 layer 2)

These fields are **out of scope** for a pure vanilla density graph (no X/Z coordinate
access) and require the Hive-owned macro-placement layer:

| Field | Role | Closing checkpoint |
|---|---|---|
| `stack_core` mask | the radial footprint of a stack cluster vs. the dead wastes | `EG-P03-S02-C0039` |
| `stack_apron` mask | perimeter walls, collapsed suburbs, slag | `EG-P03-S02-C0039` |
| `trunk_axis` | deterministic aligned corridors/causeways between clusters | `EG-P03-S02-C0040` / `EG-P04-S05-C0062` |

Until then the spike treats **the entire dimension as one stack core** with no wastes
and no inter-cluster axis. P02-GATE reviews the *single-core* massing; the multi-core
planetary layout is a Phase 3 gate.

## 4. Band identity — the "reads without labels" contract

`P02-GATE` requires every band be distinguishable without a label. Each band must
differ from **both** its neighbours on at least **three** of these axes:

| Band | Palette (floor skin) | Ambient light | Fog | Ceiling character | Feature set | Sound bed |
|---|---|---|---|---|---|---|
| The Drown | tuff | very low | near-black, tight | low, wet, dripping | acid pools, few fixtures | basalt-deltas loop |
| The Underworks | cobbled deepslate | low | dark, close | broken, uneven, patched | dense narrow tunnels, salvage | (shared) |
| The Furnace Tiers | blackstone | low-mid | hot haze, orange cast | tall industrial bays | machinery bays, salvage, fixtures | nether-wastes loop |
| The Billet Decks | polished blackstone bricks | mid | thin haze | regular slab ceilings | habitation cells, markets | nether-wastes loop |
| The Vaulting | polished blackstone | mid, directional | thin, deep, long throw | cathedral-scale, columns | the monumental hall, bridges | soul-sand-valley loop |
| The Crown | deepslate bricks | mid, cold | thin, cold blue | fortified, capped | observatories, capstone | soul-sand-valley loop |

The spike currently delivers the palette column (surface rule) and a 3-biome grouping
of the fog/sound column. The per-band split (6 biomes or a rule biome source), light,
and ceiling character are Phase 3/5.

## 5. Traversal-rhythm binding

Carried from `spatial-metrics.md` §4, restated as a massing requirement:

- On any authored bottom-to-top route, a **monumental release** (smallest open
  dimension ≥ 48, sightline ≥ 120) at a cadence between every two bands and every
  half-band.
- No constricted run longer than **~140 blocks** without a release or a passing
  chamber (a local widening ≥ 12 with a landmark).
- Unbroken corridor and unbroken megacavern both **fail**.
- The spike's `network` (constriction) + `shaft` (bypass) + `hall` (one release)
  is the minimum; Phase 3/4 add the intermediate releases and thresholds.

## 6. Spike deviations from this contract

| Deviation | Where | Closes at |
|---|---|---|
| No `stack_core` / `apron` / `trunk_axis` — whole dimension is one core, no wastes | density graph | `C0038`-`C0040` |
| `hall` is noise-gated and partial, not an authored single release space | `hive_world/hall_keep` | `C0043` / `C0059` |
| Shaft placement is noise, not deterministic anchors | `hive_world/shaft_*` | `C0037` / `C0043` |
| Only one monumental release on the full route (contract wants a cadence) | density graph | `C0033` / `C0043` |
| Band identity: only palette + a 3-biome fog grouping (contract wants 6-way, +light +ceiling) | biomes / surface rule | `C0046` / Phase 5 |
| Carve fractions untuned — no measured % of volume | density graph | `C0035` / `C0049` |

## 7. Freeze criteria (what P02-GATE checks)

1. The full route is traversable in **both** directions (timed, dead-end audited).
2. Every band is distinguishable without labels (§4, independent visual review).
3. At least one compression → threshold → release sequence is **independently approved**.
4. The monumental hall reads as **authored scale**, not accidental empty volume.
5. Chunk generation is inside the `performance-budget.md` envelope at the greybox scale.
6. On acceptance: §1 Y bands + datums + seam-zone widths, §2 `mass_ceiling` /
   `roof_seal` / `floor_seal` / carve-fraction envelopes, and the §2 combine rule are
   **frozen**. Phase 3 tunes values within the frozen envelopes only.

## 8. Rollback

The massing is one generator (`generate_hive_world_density.py`) writing one density
family. Revert = point `noise_settings` `final_density` at a vanilla constant / simple
gradient; the dimension still loads as a bare mass. No other system depends on the
internal density-function names.

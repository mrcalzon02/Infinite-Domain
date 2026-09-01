# Plan — activating the planetary macro topology (C0038–C0040)

**Authority:** `dev/docs/Endgame.md` §2.4, §2.7; `dev/docs/endgame/contracts/massing-contract.md` §2–§3;
`dev/docs/endgame/adr/ADR-0001` (layer 2 = macro placement).
**Status:** PLAN, authored 2026-08-31. No worldgen artifact is changed by this document.
**Supersedes the claim** in `dev/docs/endgame/PROGRESS-AUDIT.md` that the macro layer is "NOT STARTED".

---

## 1. The finding that changes the plan

The macro layer is **not missing — it is built and disconnected.**

`dev/packdev/hive-world-companion` registers two custom density-function codecs
(`infinite_domain_hive_world:stack_field` and `:trunk_axis`) backed by
`HiveMacroLayout` / `HiveStackField` / `HiveTrunkAxis`. These give the generator the
X/Z access that ADR-0001 said a pure vanilla density graph could never have — which was
the original blocker for the entire macro layer.

On top of them, **15 density functions already describe the complete intended
topology**, and every one of them is orphaned:

```
apron_height  apron_mass  apron_or_waste  apron_shape  core_shape  macro_body
spire_mass    spire_shell trunk_axis      trunk_mass   trunk_vertical
waste_and_trunk  waste_base  waste_crust   waste_noise
```

`noise_settings` still roots terrain at `final`, which is the single-core spike:

```
final = max( carved, roof, floor )          <- LIVE (one continuous core)
```

while the finished alternative sits unreferenced:

```
macro_body = core_shape in [0,2) ? spire_shell : apron_or_waste
├── spire_shell     = max( carved, min( roof, core_shape ) )
└── apron_or_waste  = apron_shape in [0,2)
                      ? max( waste_and_trunk, apron_mass )
                      : waste_and_trunk
    ├── apron_mass      = min( apron_height, apron_shape )     apron caps Y48 -> 80
    └── waste_and_trunk = max( waste_crust, trunk_mass )
        ├── waste_crust = waste_base + 0.35 * waste_noise      surface approx Y-4
        └── trunk_mass  = min( trunk_axis, trunk_vertical )    causeway Y-2 -> 10
```

**This is already a live defect, not merely missing work.** `biome_region` *is* wired to
the macro masks (`core_mask` / `apron_mask`), so biome routing already labels Wastes and
Apron — while terrain generates full stack mass there. Today the game says "Wastes" and
builds a hive. Connecting `macro_body` **fixes** that incoherence.

## 2. Parameters verified against the contracts

Computed from the live JSON (`cell_size 3072`, `radius 520`, `vertical_taper 0.45`):

| Metric | Contract target | Actual | |
|---|---|---|---|
| Stack core diameter | 600–1200 (`spatial-metrics` §3) | **1040** at Y0, tapering to 572 at Y607 | PASS |
| Core-to-core separation | 2000–4000 | **3072** | PASS |
| Surface wastes share | >= 70 % (pillar §2.4) | **91 %** at Y0, rising to 97 % at crown | PASS |
| Trunk causeway width | — | 28 blocks (half-width 14), Y-2 -> 10 | consistent with §3 |

The vertical taper produces the silhouette the mission asks for: a broad base narrowing
to a crown, rather than a cylinder.

## 3. Four defects that block a naive swap

A one-line `final -> macro_body` swap is **wrong**. In severity order:

**D1 — the world floor seal is lost (blocking).**
`macro_body` never references `floor`. `massing-contract` §2 requires the bottom 9–18
blocks always solid. On the waste/apron path a player would reach the world floor or
fall out of the world. **Fix:** keep the frozen combine-rule shape and wrap:
`final = max( macro_body, roof, floor )`.

**D2 — no caching anywhere (blocking on performance).**
Zero `cache_2d` / `flat_cache` / `interpolated` wrappers exist in the entire Hive density
tree. Per sample, `stackValue` performs 9 `hypot` calls and `trunkValue` performs 18
segment-distance calls. `trunk_axis` is **fully Y-invariant** — a textbook `cache_2d`
candidate. `stack_field` depends on Y only through a cheap linear taper, so its expensive
2D nearest-centre distance should be split out and cached with the taper applied on top.
This is a **Java change**, not just JSON, and is the highest-leverage work in this plan.
C0008 allows p50 <= 25 ms/chunk; the current cost is unmeasured.

**D3 — `spire_shell` double-counts `roof`.**
It already contains `min(roof, core_shape)`; after D1 it is also `max`-ed with `roof`.
Harmless, but simplify once D1 lands so the graph stays readable.

**D4 — `spire_mass` is dead.**
Superseded by `spire_shell` (which adds the carve and roof terms). Delete it rather than
leave two plausible spire roots for a future worker to choose between.

## 4. Recommended sequence

Each stage is independently reversible and independently validatable. Do **not** collapse
them — the point is that a failure localises.

**S0 — toolchain path repair (PREREQUISITE, done 2026-08-31).**
The `dev/` restructure left every endgame script rooted at `parents[2]` (= `dev/`) while
`kubejs/` and `mods/` live at the instance root one level above, so **all twelve endgame
generators and validators could not find the data they operate on**. Repaired by moving
the root to `parents[3]` and completing the half-finished `docs/` -> `dev/docs/` and
`packdev/` -> `dev/packdev/` prefixes. Verified: all three validators PASS and all six
emitting generators are byte-idempotent against `kubejs/`. Nothing below can proceed
without this.

**S1 — static graph activation (no behaviour change inside cores).**
Fix D1/D3/D4 and re-root `final` on `macro_body`. Extend
`dev/scripts/endgame/validate_hive_world_smoke.py` assertion 9 to also assert *reachability*: every
`hive_world/*` density function must be reachable from a `noise_settings` root, so an
orphaned topology can never silently recur. Expected result: the orphan list drops to
zero and the wastes / apron / trunk fields go live.

**S2 — performance instrumentation before tuning.**
Add the `cache_2d` wrap for `trunk_axis` and the 2D-distance split for `stack_field`.
Measure with `spark` over a fixed-seed pregeneration (C0010 reserved seeds) at the
Wastes / Apron / Core / Trunk probes, recorded against the C0008 budget. **Measure before
and after**, so the optimisation is evidenced rather than assumed.

**S3 — seam and continuity proof.**
The macro fields are cell-based with jitter; the risks are discontinuity at cell borders
and at the core -> apron -> waste transitions. Add
`dev/scripts/endgame/validate_hive_world_macro_topology.py` that samples the fields analytically (a pure
Python re-implementation of the same arithmetic) and asserts: field continuity across
cell boundaries; the >= 70 % wastes pillar; core diameter and separation inside contract
envelopes; trunk connectivity between adjacent cells; and that no core is fully sealed.
This mirrors how `dev/scripts/endgame/validate_hive_world_biome_routing.py` already proves routing offline.

**S4 — in-client acceptance (owner).**
Fresh world. Confirm: the wastes read as open dead planet; cores are visible silhouettes
on the horizon; a trunk causeway physically connects two cores; the apron reads as a
distinct skirt; band districts still generate only inside cores.

**S5 — contract reconciliation.**
`massing-contract` §3 currently states "the spike treats the entire dimension as one
stack core". On S4 acceptance that section is rewritten and the §6 deviation row closed.
This is also what unblocks **P02-GATE**.

## 5. Ordering note — do this before P02-GATE

P02-GATE freezes the massing. Freezing the *single-core* massing and then immediately
activating a multi-core planetary topology would spend the gate on a shape the pack will
never ship. **S1–S3 should land first**, so the gate reviews the real topology.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Generation cost blows the C0008 budget | S2 measures before/after; the `cache_2d` split is the designed lever; `radius` / `cell_size` are tunable without touching Java |
| Existing generated chunks seam against new terrain | Expected and acceptable — the dimension is unreleased; test on a fresh world |
| Band districts try to place in the wastes | Already biome-gated (HBR-6); S3 asserts it offline, S4 confirms it in client |
| Trunk causeways float or fail to connect | S3 asserts adjacent-cell connectivity analytically |
| Deleting `spire_mass` removes something intended | It is unreachable and strictly weaker than `spire_shell`; recoverable from git |

## 7. Rollback

Single-line: re-point `noise_settings` `final_density` at `hive_world/final` in its
pre-S1 form. The macro functions become orphans again and the dimension returns to the
single-core spike. The companion module can stay installed — its codecs are inert when
unreferenced.

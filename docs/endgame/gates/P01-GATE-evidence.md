# P01-GATE — evidence assembly

**Authority:** `docs/Endgame.md` Phase 1, §7.3, §8, checkpoint `EG-P01-S06-C0024`.
**Status:** `REVIEW_NEEDED` — assembled 2026-08-27. Two things gate acceptance:
(1) the owner's in-client runtime run, and (2) an independent integration review.
Also blocked behind **P00-GATE** acceptance (`EG-P00-S06-C0012`).

## Checkpoint status

| Checkpoint | Status | Spike commit | Outputs |
|---|---|---|---|
| C0013 registry skeleton | EVIDENCE_READY | `10121b4a` | dimension + dimension_type + placeholder biome |
| C0014 baseline generator | EVIDENCE_READY | `10121b4a` | `generate_hive_world_noise.py` + noise settings |
| C0015 spike biomes | EVIDENCE_READY | `74e4010c` | `generate_hive_world_biomes.py` + 2 biomes |
| C0016 3D routing | EVIDENCE_READY | `74e4010c` | router depth gradient + `minecraft:multi_noise` split at ~Y48 |
| C0017 acid feature | EVIDENCE_READY | `74e4010c` | `generate_hive_world_acid.py` + bounded acid lake |
| C0018 air-hazard prototype | EVIDENCE_READY | `74e4010c` | `hive_world_atmosphere_proto.js` + filter item |
| C0019 reversible entry | EVIDENCE_READY | `10121b4a` | `hive_world_expedition.js` + items + advancement |
| C0020 safe arrival | EVIDENCE_READY | `10121b4a` | `build_arrival.mcfunction` |
| C0021 client baseline | authoring done, capture pending | `10121b4a` | dimension-type effect fields; `docs/endgame/evidence/EG-P01-S05-C0021/` |
| C0022 smoke validator | DONE (passing) | `74e4010c` | `scripts/endgame/validate_hive_world_smoke.py` |
| C0023 spike removal test | authoring done, run pending | this commit | `scripts/endgame/remove_hive_world_spike.py`, `docs/endgame/hive-world-path-manifest.txt` |
| C0024 phase-1 gate | REVIEW_NEEDED | — | this file |

## Mechanical review (coordinator) — PASS

- `python scripts/endgame/validate_hive_world_smoke.py` → PASS (8 assertions incl.
  multi_noise two-entry split, the acid block reference, the height-contract match,
  "no `hive` in any player-facing string", and IIFE-scoping of the server scripts).
- `node --check` → PASS on `hive_world_expedition.js`, `hive_world_atmosphere_proto.js`,
  `hive_world_items.js`.
- All 6 endgame commits for the spike are path-scoped; the 15-file manifest
  (`remove_hive_world_spike.py`) resolves and the dry run is clean.
- `default_fluid` is codec-safe (`minecraft:water` at `sea_level -63`, no fluid body
  actually forms); acid is a static block (no fluid updates).

## Runtime evidence the OWNER must add (not yet done)

| Test | Command / action | Pass condition |
|---|---|---|
| datapack codec load | fresh world, check `logs/latest.log`; tab-complete `/execute in ` | zero `infinite_domain:hive_world` errors; the dimension appears in the `/execute in ` completion |
| fresh generation + height probes | `/execute in infinite_domain:hive_world run tp @s 0 <y> 0` at the six band midpoints | solid crust below ~Y0, air middle, bedrock roof ~Y306–319; arrival anchor solid |
| biomes + routing | `/locate biome infinite_domain:hive_world_dead_waste` and `..._stack_test`; sample biome at the probes | both resolve; stack_test below ~Y48, dead_waste above |
| acid | fly to an acid lake; `/tick freeze`; walk a mob/player in | pool is bounded; `spark` shows 0 ongoing fluid ticks in a settled chunk; contact damages |
| air hazard | descend unprotected, then with `kubejs:cinderstack_filter`; sit on the deck | meter rises unprotected, ~5× slower filtered, vents on the deck; `spark` tick cost within the C0008 companion budget |
| round trip | `/give @s kubejs:cinderstack_marker`, use it; return via marker and via the lodestone | lands on the deck; returns to the exact origin (pos + facing) |
| recovery matrix | die in the Hive; disconnect mid-transfer; obstruct the platform then re-enter; delete the origin dimension then return | normal respawn out; no dupe/void loop; platform rebuilt; overworld fallback fires |
| removal | `python scripts/endgame/remove_hive_world_spike.py --apply`, relaunch | Overworld/Nether/End unchanged; no orphaned dimension in level data |

## Completeness matrix (§8) — Phase 1 spike

| Axis | Verdict | Basis |
|---|---|---|
| Registry | PARTIAL | objects authored + smoke-checked; codec load is owner-pending → audited at C0100 |
| Serialization | PARTIAL | JSON/JS parse offline; datapack + script load owner-pending → C0101 |
| Terrain | PARTIAL | generator respects the height contract; fresh-gen + probes owner-pending |
| Biomes | PARTIAL | two biomes + a depth-based `multi_noise` split; `/locate` owner-pending |
| Structures | NOT_APPLICABLE | the spike uses a `/function` platform, not worldgen structures; structure grammar is Phase 4 |
| Navigation | PARTIAL | arrival deck is walled, lit, deterministic, rebuilt on entry; walk test owner-pending |
| Environment | PARTIAL | bounded acid + a C0007-shaped exposure prototype; contact + tick-cost owner-pending |
| Gameplay | NOT_APPLICABLE | the spike has no objectives; gameplay is Phase 6 |
| Progression | PARTIAL | entry is operator/creative-gated — no earlier-progression bypass; the real gate is C0084; full audit C0111 |
| Visual identity | DEFERRED | `minecraft:the_nether` placeholder effects; original identity at C0021 / Phase 5 |
| Performance | DEFERRED | budgets defined (C0008); spike measurement + pre-Hive baseline owner-pending at C0021 |
| Multiplayer | DEFERRED | spike is single-player scope; matrix at C0110 |
| Recovery | PARTIAL | death / disconnect / stranding / missing-origin fallback all handled in code; matrix run owner-pending → C0109 |
| Documentation | PASS | every spike file has a header + manifest entry; test strategy, removal manifest, and this gate exist |
| Distribution | PASS | all content original and tracked; no third-party jar or resource modified; QA world gitignored |

## P01-GATE exit criteria

| Criterion | Met? |
|---|---|
| a fresh world loads without datapack or registry errors | **owner-pending** |
| the dimension generates new chunks and respects the height contract | authored to contract; **owner-pending** |
| a player can enter and return safely | code complete; **owner-pending** |
| acid and atmosphere prototypes work without global side effects | designed bounded (static acid, O(players) tick); **owner-pending** |
| no production scope is prematurely coupled to disposable spike code | PASS — every spike file is marked disposable; removal helper proves separability |

## Decision

`REVIEW_NEEDED`. Cannot advance until: P00-GATE is accepted, the owner completes the
runtime table above, and an independent integration reviewer signs off.

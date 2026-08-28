# Endgame — environment implementation (Phase 5, spike scale)

**Authority:** `docs/Endgame.md` Phase 5, `docs/endgame/contracts/hazard-contract.md`
(C0007 shape). This records the **tuned spike values** for the datapack + KubeJS
environment systems. The companion module re-owns the transactional parts at
`EG-P05-S02-C0071`; every number here is provisional and is re-tuned against playtests
at `EG-P05-S01-C0069` / `C0072` / `C0082`.

Owner-directed Phase 5 work, ahead of the P02/P05 gates.

---

## 1. Exposure model (C0069) — `hive_world_atmosphere_proto.js`

```
exposure_gain_per_second =
    base_band_rate(y)
  * (1 - ppe_reduction)
  * fume_multiplier
  * (0 if at a waystation else 1)
```

| Band | Y range | `base_band_rate` |
|---|---:|---:|
| The Drown | `-64..-33` | 4.0 |
| The Underworks | `-32..47` | 2.6 |
| The Furnace Tiers | `48..111` | 1.9 |
| The Billet Decks | `112..191` | 1.5 |
| The Vaulting | `192..255` | 1.2 |
| The Crown | `256..319` | 1.0 |

- `fume_multiplier` = **1.5** when `the_wasteland_reworked:acid` is within a 6-block
  radius (a fume zone, C0074); **1.0** otherwise.
- `exposure` is clamped `0..100`, stored in `persistentData.id_cinderstack_exposure`.
- **Recovery** (`RECOVER_PER_SEC = 9`) happens **only at a waystation**, never in the
  open even with full PPE (C0007 non-trivialisation).

### Effect thresholds

| `exposure` | Effect (1 s, refreshed) |
|---|---|
| `>= 40` | HUD bossbar turns yellow; a one-time Charles warning at `>= 65` |
| `>= 65` | `nausea` + `weakness` |
| `>= 90` | `nausea` + `darkness` + `slowness 1` + `2` magic damage/s |
| `= 100` | as above with `4` magic damage/s |

## 2. PPE and filter economy (C0070 / C0072)

| Carried | `ppe_reduction` | Notes |
|---|---:|---|
| nothing | 0.00 | full band rate |
| `kubejs:cinderstack_mask` only | 0.35 | the respirator alone is a poor seal |
| mask **+** `kubejs:cinderstack_filter` | 0.84 | the working configuration |

- Items are **carried**, not worn — no armour-slot dependency in the spike.
- **Filter drain:** while filtering, `wear += gain + base_band_rate * 0.1` per second;
  every `26` wear consumes one cartridge (`WEAR_PER_CARTRIDGE`). Charles announces each
  spend and the last one. Roughly: one cartridge lasts **~10 s of Drown exposure** or
  **~40 s in the Crown**.
- **Mask durability:** `maxDamage 512`; takes 1 damage per second of filtered use, then
  breaks with an item-break sound. So there is no permanent zero-cost protection
  (mission §2.5).
- **Recipes** (`hive_world_atmosphere_proto.js` `ServerEvents.recipes`):
  - mask: glass panes + leather + iron + paper (shaped), id `infinite_domain:cinderstack/mask`;
  - filter x2: 2 paper + 2 charcoal + 1 iron nugget (shapeless), id `infinite_domain:cinderstack/filter`.

## 3. Shelter / ventilation (C0073) — spike model

- A **lodestone within a 6-block radius** is a **clean-air waystation**: exposure decays
  at `RECOVER_PER_SEC` and does not rise.
- Waystations are already placed by the arrival hall and every `transit_hub` module, and
  lodestones are craftable (netherite-tier), so a player can drop personal waystations
  as they push deeper — a natural mid-tier logistics cost.
- **Deferred:** a powered `kubejs:cinderstack_vent` block projecting a larger sealed
  volume, with power-loss / breach / chunk-unload failure behaviour, is the real C0073
  and moves to the companion module.

## 4. Acid contact (C0074) — spike position

- Acid is the static block `the_wasteland_reworked:acid`; TWR supplies collision
  contact damage, which the spike relies on unchanged.
- **Fume zones** (§1) are the only Hive-added acid interaction so far.
- **Corrosion is disabled** (armour/tool durability unaffected by proximity) per C0007.
- Item burn, boat/vehicle behaviour, and a deliberate contact handler are the real
  C0074 and are deferred.

## 5. Environmental feedback (C0079)

- A per-player **bossbar** `infinite_domain:air_<username>`: value = exposure, colour
  green `< 40` / yellow `< 65` / red otherwise, title "Atmosphere NN%" or
  "Filtered air NN%", hidden at exposure 0.
- Charles chat lines on the first `>= 65` crossing and on every cartridge spend.

## 6. Failure / recovery persistence (C0080)

| Event | Behaviour |
|---|---|
| death in the Cinderstack | exposure + wear reset to 0; bossbar cleared (`bed_works`/`natural` false already sends the player out) |
| relog | exposure persists (`persistentData`); the bossbar is re-created on the next tick in the Hive |
| leaving the dimension | exposure decays fast (`-25`/2 s) and the bossbar hides |
| creative / spectator | exposure forced to 0, bossbar hidden |

## 7. Ambience (C0076 / C0077 / C0078) — biome effects

`generate_hive_world_biomes.py`, per band group:

| Biome | Fog | Particle | Ambient loop | Music |
|---|---|---|---|---|
| `hive_world_sump` | near-black `0x14140F` | `white_ash` p=0.0022 | basalt-deltas | `music.overworld.dripstone_caves` |
| `hive_world_works` | warm dark `0x23201B` | `white_ash` p=0.0032 | nether-wastes | `music.nether.nether_wastes` |
| `hive_world_vault` | cold blue `0x1B2129` | `warped_spore` p=0.0009 | soul-sand-valley | `music.overworld.deep_dark` |

- All three carry `mood_sound` (cave) and `additions_sound`.
- **Deferred:** a truly original sky, directional light, and fog *volumes* (not just
  colour) need a custom `DimensionSpecialEffects` in the companion module (C0075). The
  spike keeps `minecraft:the_nether` dimension effects.

## 8. Budget note (C0081)

- The atmosphere tick is `O(players in the Hive)`, runs every 20 ticks, and does one
  `~1180`-block scan per player per second (waystation + fume). Acceptable for the
  spike; the companion module replaces the scan with tracked shelter volumes.
- Bossbar updates are ~5 silent commands per player per second — trim at C0081 if the
  server profile flags it.

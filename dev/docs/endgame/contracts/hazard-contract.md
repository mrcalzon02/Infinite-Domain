# Endgame — hazard contract

**Authority:** `docs/Endgame.md` §2.5 and checkpoint `EG-P00-S04-C0007`.
**Status:** ACCEPTED 2026-08-27 as a contract. All numbers are shapes and bounds;
tuning is Phase 5 (`EG-P05-S01-C0069` exposure model, `C0070` PPE, `C0072` filter
economy, `C0073` ventilation/shelter, `C0074` acid contact).

Depends on: C0002 capability classifications. Does **not** choose art, particle art,
or final damage values.

## 1. Hazard systems and ownership

| Hazard | Signature | Owner | C0002 basis | Phase 1 fallback |
|---|---|---|---|---|
| **Atmosphere** (choking, non-breathable) | dimension-wide; worse low and in the open | Hive companion module — a dimension-scoped exposure applied to `infinite_domain:hive_world` at every Y | EnviroMine dimension toxicity classified **unsuitable** as-is (Y-derived below Y63, no dimension-atmosphere API) | KubeJS data-only periodic exposure tick |
| **Acid** | acid reservoirs in The Drown, sparse basins in the wastes, fume zones near large bodies | TWR `the_wasteland_reworked:acid` for the fluid + a Hive contact adapter | acid fluid + collision damage **usable-with-adapter**; corrosion absent | bounded decorative pools + generic contact damage; corrosion disabled |
| **Ventilation / shelter** | powered safe volumes; airlocks | Hive companion owns true sealed volumes; EnviroMine vents used as explicit powered "safe bubbles" | EnviroMine vents/masks **usable-with-adapter**; a vent inflates an AABB and does not model walls | treat vents as explicit safe bubbles |
| **PPE** | consumable mask + filter; sealed suit later | EnviroMine mask/filter items + a Hive atmosphere adapter | masks/filters **usable-with-adapter** | data-only filter item with a drain counter |
| **Radiation** | localised, tagged sources only; **no ambient Hive radiation** | Wastelands `RadiationManager` through `infinite-domain-unified-radiation` — sole dose authority | unified radiation **usable** | retain localised tagged sources only |
| **Oxygen (Stellaris)** | not adopted unless a later spike accepts it | none — the companion atmosphere model is the non-breathable model | Stellaris oxygen **runtime-unverified**, no local custom planet | companion air budget |

## 2. Non-trivialization rule (satisfies §2.5)

1. Exposure is a **rate**, never a binary state negated by one item.
2. Open-air survival always consumes a logistical resource (filter charge, shelter
   power, or air reserve) that depletes over time. **No equipment reduces open-air
   exposure rate to zero for unlimited duration.**
3. The best PPE reduces the rate and buys time; it does not remove route planning,
   spare-carrying, or shelter power.
4. Shelters require power and fail predictably (power loss, breach, chunk unload) with
   no residual protection after failure.
5. Hazard layers are **independent**: atmosphere PPE is not acid protection is not
   radiation shielding. A fully air-kitted player can still die to acid or a radiation
   pocket.
6. Progression may reduce attrition (better filters, sealed vehicles, powered beacons,
   restored ventilation) but the dimension never becomes "safe"; every capstone and
   repeatable loop keeps a logistical cost.

## 3. Exposure model (shape — values tuned at C0069)

```
exposure_gain_per_tick =
    base_band_rate
  * (1 - ppe_reduction)          # 0 with no PPE; ~0.70-0.85 with mask+working filter
  * event_multiplier             # 1 normal; >1 during storms / fume zones / breaches
  * (0 if in_powered_sealed_volume else 1)

base_band_rate ordering (worst -> lightest):
  The Drown  >  open Dead Wastes  >  The Underworks  >  Furnace/Billet interiors
             >  Vaulting/Crown sheltered
```

- **Recovery:** `exposure` decays only in clean air (a powered sealed volume or a
  verified clean-air zone). It never decays in the open, even with full PPE.
- At `exposure >= threshold`: periodic damage + movement/vision penalty.
- At `exposure = max`: heavier damage + screen effects.
- Death / respawn / relog / dimension change must all reset or persist exposure
  coherently (tested at `EG-P05-S06-C0080`).

## 4. Filter economy (shape — values tuned at C0072)

- A filter has N charges; drains 1 charge per second of *active* filtering (only while
  exposed, not while sealed).
- HUD + audible warning at 20 % and 5 %.
- On exhaustion: immediate unprotected state, distinct alarm.
- Filters are craftable and replaceable (recipe gated at `C0070`). There is no infinite
  or self-regenerating filter.

## 5. Interaction matrix

### Atmosphere × protection state

| State | Effect |
|---|---|
| Unprotected, open air | exposure meter rises at `base_band_rate`; damage + penalties past threshold |
| Mask + working filter | exposure rate cut ~70-85 %; filter drains; on exhaustion -> unprotected + alarm |
| Powered sealed shelter / airlock (unbreached) | exposure paused; slow recovery |
| Sealed vehicle (only if a vehicle is added) | exposure paused while enclosed — decision deferred to the vehicle checkpoint |

### Acid × target

| Target | Effect |
|---|---|
| Player in acid | contact damage per tick (TWR base, amplified in Hive); exit is always possible — never a one-way pit |
| Player near a large acid body | adds an `event_multiplier` fume contribution to atmosphere exposure |
| Dropped item in acid | provisional: burns after ~5 s grace (blocks acid trash-chute exploits); confirmed at `C0074` |
| Mob in acid | TWR damage applies; used deliberately in encounter design |
| Boat / vehicle | provisional: damaged over time; confirmed at `C0074` |
| Armour / tool durability (corrosion) | **disabled initially**; may be enabled at `C0074` with an explicit model and grief limits |
| Adjacent water source | TWR acid->smooth-basalt reaction exists; Hive bounds acid features so the reaction stays controlled |

### Layered hazards

| Combination | Rule |
|---|---|
| Atmosphere + acid | independent; a mask does not protect from acid contact |
| Atmosphere + radiation pocket | independent; a filter does not reduce dose; radiation stays localised and tagged |
| Shelter power loss during a storm | atmosphere resumes immediately; no residual protection |
| PPE for one hazard | never implies protection from another |

## 6. Deferred

Exact rates, thresholds, filter counts, PPE registry list, shelter power draw, storm
frequency, corrosion decision, and vehicle behaviour -> Phase 5 checkpoints C0069-C0074
and C0077. Enemy hazard-compatibility -> `EG-P06-S04-C0089`.

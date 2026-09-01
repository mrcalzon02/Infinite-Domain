# Queued: Datavore distance scaling

Status: planning only. This file does not change the currently shipped Datavore
Dragon in companion mod 1.8.0.

## Required behavior

Datavore Dragons become stronger for every complete 1,000 blocks beyond the
initial 3,000-block Darknet frontier. The tier is calculated from horizontal
distance to Darknet origin when the entity spawns and is saved on that entity.
It never changes during the fight.

```text
distance = floor(sqrt(x * x + z * z))
depth_tier = max(1, floor(distance / 1000) - 2)
maximum_health = depth_tier * 1000
loot_scale = depth_tier
```

Examples:

| Spawn radius | Depth tier | Maximum health | Base loot scale |
|---:|---:|---:|---:|
| 3,000–3,999 | 1 | 1,000 | 1× |
| 4,000–4,999 | 2 | 2,000 | 2× |
| 5,000–5,999 | 3 | 3,000 | 3× |
| 10,000–10,999 | 8 | 8,000 | 8× |

The current 2,800–3,600 spawn annulus must become a minimum-frontier rule when
this feature is implemented; otherwise no higher tiers could spawn. Natural
spawning should begin at radius 3,000 and remain valid at all greater distances.

## Spawn snapshot and persistence

- Calculate the depth tier from the dragon's spawn position, not a nearby player.
- Store the tier and original spawn radius in synchronized entity data and NBT.
- Set maximum and current health once during final spawn initialization.
- Preserve the saved tier across chunk unloads, server restarts, and dimension
  transfers.
- Summoned Datavores should use their summon position unless an explicit tier is
  supplied in NBT for testing or authored encounters.
- Moving or luring a Datavore across a 1,000-block boundary must not heal it,
  reduce it, or change its rewards.

## Scaling rewards

Guaranteed Darknet intelligence scales linearly with `loot_scale`:

- Darknet Data Caches: `(16–32) × loot_scale`
- Scraped Access Tokens: `(24–48) × loot_scale`
- Encrypted Credential Bundles: `(8–16) × loot_scale`
- Black ICE Kernels: `(2–5) × loot_scale`

Rare rewards should scale by adding independent rolls rather than multiplying a
single probability above 100 percent:

- Zero-Day Archive: `loot_scale` rolls at 50% each, 1–2 per success.
- Root Authority Key: `loot_scale` rolls at 10% each, one per success.
- Nether Stars: `loot_scale` rolls at 50% each, 1–2 per success.

Netherite is the only reward that should not grow without restraint. Use
`(4–12) × ceil(sqrt(loot_scale))` so distant farming primarily feeds Charles's
Darknet data economy instead of trivializing every material economy.

All drops must use the entity's saved tier. Loot must not recalculate distance
from the death position.

## Presentation

- Boss bar name should expose the snapshot tier, for example
  `Datavore Dragon — Depth Tier 4`.
- The bar remains 20-segment red unless later tiers receive explicit visual
  variants.
- Charles should explain that distance is effectively network depth and that
  deeper Datavores have accumulated larger, more valuable archives.

## Implementation notes

The implementation belongs in `DatavoreDragon`, with saved/synchronized tier
data and loot context or tier-specific reward emission. Extend the Datavore
audit with boundary tests at radii 2,999, 3,000, 3,999, 4,000, and 10,000, plus
save/load persistence and death-position invariance checks.

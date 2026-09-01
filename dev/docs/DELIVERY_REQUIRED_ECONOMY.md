# Create: Delivery Required economy

Infinite Domain treats Delivery Required as a logistics profession, not an
unrestricted material shop. The Contractor pays for moving factory output; the
Market provides expensive emergency imports; staged Echo shops remain the only
pack-controlled source for specialist replacement parts.

## Contractor exports

`config/createdeliveryrequired-contract-item-prices.toml` is an allowlist. Its
32 entries cover ordinary ores, industrial inputs, selected Nether and ocean
exports, brass and precision production, lava, and brewed potions. It omits:

- every item sold by an Echo shop, preventing buy-and-redeliver currency loops;
- diamonds, emeralds, netherite, Echo Shards, and Nether Stars;
- cyberware and finished implants;
- Foundation Cores, quest charters, machines, and other progression tokens.

Generated demand uses a budget of 64 Spurs per offer. A normal job therefore
represents approximately one Cog of cargo before the configured star and rank
bonuses. Per-item rank XP is reduced to `0.25` so low-value bulk cargo does not
outrank difficult long-distance work solely through stack count.

## Market imports

`config/createdeliveryrequired-market-item-prices.toml` contains only 17 mundane
commodities: coal, charcoal, copper, iron, gold, clay, bricks, slime, leather,
string, feathers, gunpowder, wheat, bread, paper, sugar, and glass.

The existing 3x purchase multiplier makes these imports substantially more
expensive than producing them. The maximum quantity per offer is 256 instead of
103,680. The Market cannot sell redstone, enchanting materials, Nether access
materials, boss drops, Create mechanisms, cyberware, potions, or Echo inventory.

## Progression rules

- Currency never substitutes for an era stage; Echo inventories retain their
  `infinite_domain:era_N` requirements.
- Contractor jobs may consume advanced exports but cannot grant advanced items.
- The lobby Contractor may be installed as a public job board without exposing
  the old open commodity catalogue.
- P2P trade remains player-supplied and should receive a separate abuse review
  before it is promoted as a progression path.

Price-list and server-config changes take effect after a full game restart and
newly generated offers. Existing accepted jobs or cached boards may retain their
old values until they expire or refresh.

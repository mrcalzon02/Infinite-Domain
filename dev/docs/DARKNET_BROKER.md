# Darknet Broker

## Entity and spawning

The Darknet Broker is a custom wandering-trader entity registered as
`infinite_domain_darknet_worldgen:darknet_trader`. Its localized name is Darknet
Broker. Natural spawning is admitted only to `cyberspace:darknet_biome`, at weight
1 and group size one. Its spawn predicate also requires the Darknet dimension,
surface Y=2 or higher, normal mob-spawn validity, and no other Broker within 384
blocks. A Broker remains for 72,000 ticks while not trading, then despawns using
the native wandering-trader lifecycle.

It uses the wandering trader's model, folded-arm merchant interface, navigation,
trade persistence, and avoidance behavior. Its custom attributes are 60 health,
12 armor, 0.5 knockback resistance, 0.5 movement speed, and 48 follow range. The
custom exact-UV skin is near-black and oxblood with circuitry, cyan packet faults,
and magenta visor pixels. The normal universal Darknet entity circuitry and shimmer
still render over it.

Admin test command:

`/summon infinite_domain_darknet_worldgen:darknet_trader ~ ~ ~`

## Currency

Darknet Scrip is an anonymous bearer credit used only by the Broker economy. It is
not craftable. Players acquire it by liquidating recovered data and the two premium
ore bonuses. Retail prices are always higher than wholesale returns, preventing a
buy-and-resell currency loop.

## Broker purchases from the player

| Player pays | Broker pays | Uses |
| --- | --- | ---: |
| 16 Scraped Access Tokens | 1 Darknet Scrip | 12 |
| 8 Darknet Data Caches | 2 Darknet Scrip | 12 |
| 4 Encrypted Credential Bundles | 3 Darknet Scrip | 10 |
| 2 Black ICE Kernels | 5 Darknet Scrip | 8 |
| 1 Zero-Day Archive | 10 Darknet Scrip | 6 |
| 1 Root Authority Key | 24 Darknet Scrip | 4 |
| 1 Ghost-Market Cipher | 16 Darknet Scrip | 6 |
| 1 Black-Ledger Writ | 48 Darknet Scrip | 3 |

## Broker sales

| Scrip cost | Result | Uses |
| ---: | --- | ---: |
| 1 | 4 Scraped Access Tokens | 16 |
| 3 | 2 Darknet Data Caches | 12 |
| 5 | 1 Encrypted Credential Bundle | 8 |
| 9 | 1 Black ICE Kernel | 6 |
| 18 | 1 Zero-Day Archive | 4 |
| 36 | 1 Root Authority Key | 2 |
| 6 | 1 Fragmented Data Node | 12 |
| 14 | 1 Corrupted Data Node | 8 |
| 32 | 1 Encrypted Data Node | 4 |
| 64 | 1 Root Access Node | 2 |

The emergency Darknet Anchor offer costs 64 Darknet Scrip plus eight Root Authority
Keys and has one use. Buying those keys back from Brokers first raises its effective
retail burden to 352 Scrip, before the final 64-Scrip payment. This is intentionally
an absurd fallback rather than a replacement for constructing the Anchor.

## Premium ore recoveries

Ghost-Market Ciphers and Black-Ledger Writs are non-craftable premium data finds:

- Corrupted Data Node: 2% Ghost-Market Cipher.
- Encrypted Data Node: 7.5% Ghost-Market Cipher and 1% Black-Ledger Writ.
- Root Access Node: 25% Ghost-Market Cipher and 7.5% Black-Ledger Writ.

Darknet Extraction continues to apply only to each node's primary recovered-data
stack. It does not multiply these premium bonuses.

## Art provenance

`docs/art-direction/darknet-broker-reference.png` and
`docs/art-direction/darknet-broker-items-reference.png` are the built-in
image-generation references; their exact prompts are stored beside them.
`scripts/generate_darknet_broker_art.ps1` deterministically extracts and recolors
Minecraft's exact wandering-trader UV sheet and produces the three 32×32 item
textures from the checked-in reference strip.

The companion mod is `infinite-domain-darknet-worldgen-1.8.0.jar`. Entity, item,
and renderer registration require a full game restart.

# Darknet native ecology

Companion mod 1.8.0 gives the Darknet a small native ecology instead of using
ordinary Overworld animals with a post-process tint.

## Native creatures

| Creature | Natural group | Relative weight | Preserved behavior |
|---|---:|---:|---|
| Darknet Rabbit | 2-4 | 12 | Rabbit movement, food, breeding, and drops |
| Darknet Cow | 2-3 | 8 | Cow breeding, milking, beef, and leather |
| Darknet Hound | 1-3 | 4 | Wolf combat, taming, collars, sitting, and inherited pup ownership |
| Darknet Fox | 1-2 | 6 | Fox stalking, pouncing, sleeping, carried items, and breeding |
| Darknet Slime | 1-2 | 10 | Hostility, size, jumping, slimeball drops, and same-type splitting |

Every natural-spawn predicate independently verifies the
`cyberspace:darknet_dimension` dimension and a surface position at Y=2 or
higher. The biome modifiers target only `cyberspace:darknet_biome`, providing a
second independent scope guard. These entities therefore cannot naturally
populate the Overworld, Nether, End, or normal Cyberspace.

The base textures are exact vanilla UV transformations in matte black,
oxblood, signal red, cyan, and restrained magenta. The existing universal
Darknet living-entity layer adds the static circuit overlay and animated shimmer
on top. Hounds have separate wild, tame, and angry base sheets; foxes have
separate awake and sleeping sheets.

## Native foliage

- Signal Grass is the common ground cover.
- Packet Fern forms less-common branching patches.
- Cipher Bloom is rare and emits visible cyan light.
- Blackroot Shrub is uncommon, low, dark cover with a weak glow.

Foliage attempts one small weighted patch per three chunks during vegetal
decoration. A patch makes only 20 placement attempts, keeping the flatland open
and unsettling. All four blocks are non-solid, non-colliding, instantly
breakable, self-dropping cross-model foliage. Generation is limited to the
Darknet biome and affects newly generated chunks; there is intentionally no
retroactive conversion requirement.

## Lossy ecology-to-data conversion

Darknet ecology can be recycled into the first three recovered-data tiers. Each
recipe consumes a complete 3x3 grid of one ingredient and returns exactly one
data item—a deliberately poor 9:1 rate.

| Data tier | Output | Accepted ecology resources |
|---:|---|---|
| 1 | Scraped Access Token | Signal Grass, raw or cooked rabbit, raw or cooked beef |
| 2 | Darknet Data Cache | Packet Fern, rabbit hide, leather, Slimeball |
| 3 | Encrypted Credential Bundle | Cipher Bloom, Blackroot Shrub, rabbit foot |

Black ICE Kernels, Zero-Day Archives, Root Authority Keys, Ghost-Market
Ciphers, and Black-Ledger Writs have no ecology conversion recipe. They remain
exclusive to mining, dangerous loot, and the Broker economy.

## Administration and testing

The exact summon commands are:

```mcfunction
/summon infinite_domain_darknet_worldgen:darknet_rabbit ~ ~ ~
/summon infinite_domain_darknet_worldgen:darknet_cow ~ ~ ~
/summon infinite_domain_darknet_worldgen:darknet_hound ~ ~ ~
/summon infinite_domain_darknet_worldgen:darknet_fox ~ ~ ~
/summon infinite_domain_darknet_worldgen:darknet_slime ~ ~ ~ {Size:3}
```

Use `/place feature infinite_domain:darknet_foliage` at a clear Darknet surface
to validate the plant patch without waiting for fresh-chunk generation.

Run `scripts/generate_darknet_ecology_art.ps1` to recreate the model-correct
skins and foliage sprites from the installed 1.21.1 client textures and the
approved palette. The reference and exact generation prompt are stored under
`docs/art-direction/`. A full game restart is required after installing this
ecology pass because it registers five new entity types and four new blocks.

The pack's original Darknet textures and mechanics are offered under the MIT
License, with an explicit invitation for the Cyberspace/Darknet mod author to
reuse them. See `DARKNET-ASSETS-LICENSE.md` for the complete grant and the
important boundary around upstream third-party assets.

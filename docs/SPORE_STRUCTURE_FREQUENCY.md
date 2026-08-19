# Spore Landmark Placement and Terrain Policy

Spore structures are part of Infinite Domain early-world environmental pressure. Their upstream definitions were too narrowly bound to individual vanilla biomes for the custom Wasteland preset.

- Every one of the thirteen Spore structure families has one concentric-ring candidate.
- The eleven Wasteland land landmarks occupy three escalating central-island hazard bands. Their configured distances run from 3 through 21 chunks; the shared outer band uses distinct salts so its candidates do not collapse onto one bearing.
- Surface structures use beard-thin terrain blending. Graves, labs, prisons, and mines use buried terrain adaptation.
- The eleven land landmarks are restricted to the Infinite Domain wasteland-only biome tag.
- Iceberg mines and cold mines retain their original 39- and 36-chunk outer rings and their specialized frozen-ocean and cold-biome requirements. They are deliberate expeditions beyond the central Wasteland island.
- Bearings are seed-dependent. Vanilla placement cannot guarantee literal cardinal directions while retaining terrain and biome adaptation.
- A candidate still requires a qualifying biome. The central eleven share the Wasteland landmark tag; the two outer exceptions require the northern recovery biomes.
- Changes affect newly generated chunks only.

Exact before-and-after settings are recorded in `spore-structure-frequency.csv`.

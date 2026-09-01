# LAST DAYS texture-conversion audit

Generated from the installed 1.21.1 mod JARs and the editable LAST DAYS pack. Exact-path coverage means the pack currently contains an override at the same namespace and texture path; it does not claim that the art has passed visual review.

## Baseline

- Installed texture-bearing namespaces: 132
- In-scope mod textures: 19063
- Exact-path overrides already present: 18999
- Missing in-scope overrides: 64
- Current pack PNG files: 24992
- Current animated texture metadata files: 1730
- Current normal maps (*_n.png): 8
- Current specular maps (*_s.png): 9
- Cyberworld exclusion rule used by this audit: namespaces containing `cyber` or `darknet`. These remain inventoried but are excluded from conversion totals.
- Compatibility-mod branding exclusions: 12 logo/pack-icon textures intentionally inherit from their source mods and are not conversion targets.

## Highest-volume conversion namespaces

| Namespace | Total | Covered | Missing | Coverage | Blocks | Items | Entities | GUI | Animated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| infinite_domain_space | 36 | 0 | 36 | 0% | 0 | 36 | 0 | 0 | 0 |
| lostcities | 18 | 0 | 18 | 0% | 0 | 0 | 0 | 18 | 0 |
| infinite_domain | 340 | 331 | 9 | 97.4% | 0 | 0 | 340 | 0 | 1 |
| deepnether | 2 | 1 | 1 | 50% | 0 | 1 | 0 | 0 | 0 |
| ae2 | 616 | 616 | 0 | 100% | 207 | 130 | 2 | 11 | 40 |
| ae2lt | 380 | 380 | 0 | 100% | 171 | 103 | 0 | 51 | 57 |
| aeronautics_utility_objects | 7 | 7 | 0 | 100% | 7 | 0 | 0 | 0 | 0 |
| aeronauticscovers | 1 | 1 | 0 | 100% | 0 | 1 | 0 | 0 | 0 |
| allthecompressed | 14 | 14 | 0 | 100% | 14 | 0 | 0 | 0 | 1 |
| amendments | 3 | 3 | 0 | 100% | 3 | 0 | 0 | 0 | 0 |
| ancientcompass | 32 | 32 | 0 | 100% | 0 | 32 | 0 | 0 | 0 |
| appleskin | 2 | 2 | 0 | 100% | 0 | 0 | 0 | 1 | 0 |
| bellsandwhistles | 54 | 54 | 0 | 100% | 52 | 2 | 0 | 0 | 0 |
| bjornlib | 38 | 38 | 0 | 100% | 0 | 0 | 0 | 14 | 0 |
| bno | 55 | 55 | 0 | 100% | 31 | 24 | 0 | 0 | 0 |
| brewery | 79 | 79 | 0 | 100% | 43 | 36 | 0 | 0 | 8 |
| buildinggadgets2 | 142 | 142 | 0 | 100% | 9 | 27 | 0 | 39 | 0 |
| cable_facades | 3 | 3 | 0 | 100% | 0 | 3 | 0 | 0 | 0 |
| charginggadgets | 6 | 6 | 0 | 100% | 5 | 0 | 0 | 1 | 0 |
| cloth-config2 | 3 | 3 | 0 | 100% | 0 | 0 | 0 | 3 | 0 |
| compactgearbox | 16 | 16 | 0 | 100% | 13 | 0 | 0 | 3 | 0 |
| create | 1296 | 1296 | 0 | 100% | 961 | 122 | 7 | 36 | 17 |
| create_abyss | 6 | 6 | 0 | 100% | 2 | 0 | 3 | 1 | 0 |
| create_aero_radar | 7 | 7 | 0 | 100% | 4 | 2 | 0 | 0 | 0 |
| create_aeronautics_automated_logistics | 13 | 13 | 0 | 100% | 3 | 0 | 0 | 10 | 0 |
| create_aeronautics_ftb_chunks | 1 | 1 | 0 | 100% | 1 | 0 | 0 | 0 | 0 |
| create_aeronautics_throwable_rope_connector | 4 | 4 | 0 | 100% | 2 | 2 | 0 | 0 | 0 |
| create_aeronautics_toolgun | 7 | 7 | 0 | 100% | 0 | 7 | 0 | 0 | 0 |
| create_aquatic_ambitions | 11 | 11 | 0 | 100% | 5 | 5 | 0 | 1 | 2 |
| create_chimneys | 18 | 18 | 0 | 100% | 16 | 0 | 0 | 0 | 0 |
| create_hypertube | 18 | 18 | 0 | 100% | 16 | 1 | 0 | 0 | 4 |
| create_mtg | 17 | 17 | 0 | 100% | 17 | 0 | 0 | 0 | 0 |
| create_new_age | 86 | 86 | 0 | 100% | 62 | 18 | 0 | 0 | 0 |
| create_radar | 75 | 75 | 0 | 100% | 44 | 8 | 0 | 13 | 0 |
| create_submarine | 59 | 59 | 0 | 100% | 48 | 3 | 1 | 6 | 1 |
| create_winery | 47 | 47 | 0 | 100% | 13 | 17 | 0 | 0 | 0 |
| createaeronauticscarworks | 11 | 11 | 0 | 100% | 8 | 1 | 0 | 2 | 1 |
| createappliedkinetics | 13 | 13 | 0 | 100% | 2 | 11 | 0 | 0 | 0 |
| createbigcannons | 373 | 373 | 0 | 100% | 234 | 46 | 11 | 3 | 8 |
| createdeliveryrequired | 27 | 27 | 0 | 100% | 23 | 3 | 0 | 0 | 0 |

## Visual language

- **Material identity first:** preserve whether a surface reads as steel, cast iron, ceramic, rubber, glass, cloth, flesh, stone, or energy before adding grime.
- **LAST DAYS treatment:** low-saturation industrial palette, oxidized edges, chipped paint, accumulated soot, uneven repairs, warning markings, and restrained high-value highlights.
- **Depth hierarchy:** broad material masses first, panel/brick segmentation second, seams and fasteners third, scratches and dirt last. Avoid uniform noise.
- **Variation:** author wear for the object and its physical stress points. Reuse a family design language, not generic damage masks.
- **Readability:** retain gameplay-critical silhouettes, color coding, connection states, inventory recognition, and emissive status indicators.
- **Resolution:** preserve the installed source texture dimensions and author directly at native size. Enlarged nearest-neighbor images are inspection aids only.

## Model-aware authoring workflow

1. Identify the block or item, its models, block states, texture references, animation metadata, shared textures, and renderer behavior.
2. Reconstruct how every active UV region maps to geometry, including repeated, mirrored, moving, connected, and hidden surfaces.
3. Study comparable LAST DAYS materials and functions, then define the target hierarchy, construction, and gameplay markings.
4. Re-author the texture directly at its native dimensions. Do not apply a universal palette, rust, dirt, noise, or edge-processing pass.
5. Keep related states registered and visually coherent while preserving inputs, outputs, tiers, motion, direction, and active-state information.
6. Validate alpha, dimensions, UV islands, animation frame order/timing, model references, and state-to-state visual deltas.
7. Review the wrapped model in game when available, then classify the family as retain, revise, or reauthor.

## Special textures and animation

- **Magma/lava:** preserve seamless flow cadence and emissive fissure continuity. Treat each frame as one evolving material; do not independently grime frames.
- **Obsidian:** usually static, but needs deliberate crystalline depth, low-value separation, and sparse sharp highlights. If animated by a mod, motion should be extremely slow and localized.
- **Portals/energy fields:** preserve transparency and frame dimensions. Add layered turbulence, scan-line breakup, unstable edge noise, and restrained color variation without obscuring the portal silhouette.
- **Machines:** active/off/damaged states must share registration. Animate lights, belts, gauges, vents, or fluid windows—not the whole housing.
- **Fluids/fire:** verify interpolation and frame timing in `.png.mcmeta`; normals must follow each frame, and specular response must not flicker.
- **Entities:** maintain eye/face landmarks and armor overlays. Authored wear must follow UV islands rather than crossing seams randomly.

## Normal/specular-map policy

- Author height/material masks alongside albedo so PBR can be enabled later without redoing texture structure.
- Keep normals subtle at 32x: seams, bolts, cracks, bricks, plate edges, and large corrosion pits; avoid turning painted noise into deep geometry.
- Specular maps should distinguish metal, wetness, glass, rubber, ceramic, cloth, and emissive areas. Rust and soot should normally suppress metal reflectance.
- The current instance has Sodium but no detected Iris/Oculus-equivalent shader loader, so normal/specular maps are presently foundation assets rather than active visuals.

## Production order

1. World-frequency blocks and terrain additions.
2. Core progression machines, multiblocks, cables/pipes, and active-state animations.
3. Common items, tools, armor, weapons, food, and fluids.
4. Common hostile/passive entities and vehicles.
5. GUI, icons, particles, environmental effects, and rare/decorative assets.
6. Normal/specular companions after each albedo family passes visual review.

## Working ledgers

- `last-days-namespace-coverage.csv`: planning totals by namespace.
- `last-days-texture-inventory.csv`: every discovered texture with path, dimensions, animation flag, exact coverage, priority, exclusion flag, and source JAR.

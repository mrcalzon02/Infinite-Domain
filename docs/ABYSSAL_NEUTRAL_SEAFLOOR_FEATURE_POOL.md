# Infinite Domain — Neutral Oceanographic Seafloor Feature Pool

Parent authority: `docs/ABYSSAL_ENVIRONMENTAL_SITES.md`

Status: **required / planned expansion. Existing cold seep, fracture vent field, hadal vent complex, seabed deformation and cave systems remain active; the feature catalog below is not yet mechanically implemented unless separately marked active.**

## Purpose and ownership

The Abyssal program requires a third environmental layer in addition to the two faction-specific remnant pools:

1. **Pelagos oceanographic-remnant pool** — Western/Pelagos abyssal biomes only.
2. **Karsic subsea-industrial/surveillance-remnant pool** — Eastern/Karsic abyssal biomes only.
3. **Neutral oceanographic seafloor-feature pool** — natural geology, sedimentology, chemistry and biology shared across both sides, but depth-weighted by oceanographic conditions.

This neutral pool exists to make the route from continental shelf to abyssal plain, fracture province and hadal trench read as an actual ocean basin rather than ordinary Minecraft ocean terrain with structures placed on top. It may coexist with faction debris but must never be used to mix Pelagos and Karsic built remnants.

The pool should span the full environmental continuum:

- continental shelf and shelf edge;
- continental slope / cliff break;
- lower slope and submarine-canyon approaches;
- abyssal plains;
- fracture/ridge provinces;
- volcanic and hydrothermal provinces;
- hadal trench walls and trench floor.

Where the shelf is still represented by existing normal/deep-ocean biomes and underwater-village rules rather than a dedicated Infinite Domain shelf biome, implementation must bind to the already-authoritative shelf/ocean tags rather than invent a duplicate geography system.

## AGE-018 — Neutral oceanographic seafloor-feature pool

`AGE-018` is the umbrella planning ID for the shared natural-feature pool. Individual `OSF-*` IDs below are stable planning identifiers, not yet Minecraft registry IDs.

### Volcanic and tectonic seafloor features

- **OSF-001 — Submarine volcanic cones**  
  Small-to-medium basaltic cones with cratered or breached summits. Prefer fracture and hadal-adjacent provinces; rare lower-slope examples allowed. Use basalt/blackstone/magma language rather than exposed flowing lava until runtime behavior is validated.

- **OSF-002 — Seamounts**  
  Larger isolated volcanic highs rising above the abyssal plain. These should be uncommon terrain-scale landmarks, potentially implemented through bounded density deformation rather than ordinary structure NBTs.

- **OSF-003 — Flat-topped seamount / guyot analogues**  
  Eroded or sediment-capped volcanic highs with broad flattened summits. Most appropriate toward the outer slope and abyssal plain.

- **OSF-004 — Submarine calderas**  
  Circular or asymmetric collapse basins with broken rims, central depressions and optional hydrothermal activity. Larger than the existing discrete hadal vent template and intended as terrain-scale geology.

- **OSF-005 — Pillow-lava fields**  
  Rounded basaltic lava-lobe terrain associated with young volcanic crust. Use the existing cellular-basin/pillow-lava visual vocabulary where practical.

- **OSF-006 — Cooled lava / magma-tube systems**  
  Basalt tubes running beneath or partly exposed at the seabed, including straight, branching and collapsed sections. These are geological tunnels, not ordinary caves, and should be strongly associated with volcanic provinces.

- **OSF-007 — Lava-tube skylights and collapse windows**  
  Openings into OSF-006 tubes, with collapsed basalt rims, rubble cones and occasional connections to broader cave systems.

- **OSF-008 — Basaltic flow lobes and lava fronts**  
  Overlapping sheet/lobe forms, pressure ridges and abrupt cooled flow fronts on volcanic seafloor.

- **OSF-009 — Dike / fissure ridge swarms**  
  Narrow parallel or branching basalt ridges associated with extensional fracture terrain.

- **OSF-010 — Volcanic rubble aprons**  
  Talus, angular basalt blocks and failed cone/flank material surrounding larger volcanic features.

- **OSF-011 — Rift-axis graben fields**  
  Parallel fault-bounded depressions and raised shoulders reinforcing fracture-field terrain. Prefer terrain deformation over freestanding structure templates.

- **OSF-012 — Fault scarps and exposed tectonic faces**  
  Rock faces, stepped faults and narrow rubble shelves that visually express active deformation along fracture and hadal boundaries.

### Hydrothermal and seep systems

- **OSF-013 — Diffuse hydrothermal vent fields**  
  Low-temperature venting expressed through mineralized rock, sparse magma blocks and broad altered-seabed patches rather than tall chimneys.

- **OSF-014 — Black-smoker chimney clusters**  
  Small and medium active chimney groups extending the existing fracture vent field with multiple shapes and damage states.

- **OSF-015 — Inactive / extinct chimney fields**  
  Mineralized dead chimneys, collapsed stacks and sediment-covered vent remains with no active bubble or magma behavior.

- **OSF-016 — Hydrothermal sulfide-mound analogues**  
  Mineralized mounds at vent bases. Decorative only: they must not become high-tier ore farms or progression bypasses.

- **OSF-017 — Carbonate cold-seep mounds**  
  Larger, more varied descendants of AGE-001 with carbonate crust, mud, clay and seep-centered relief.

- **OSF-018 — Linear fissure seeps**  
  Long narrow seep zones aligned with cracks rather than isolated circular seep templates.

- **OSF-019 — Pockmark fields**  
  Clusters of shallow gas/fluid-escape depressions across abyssal sediment plains and lower slopes.

- **OSF-020 — Mud-volcano / diapir analogues**  
  Low conical or blister-like sediment mounds with breached centers. Keep visually distinct from igneous volcanic cones.

- **OSF-021 — Brine-pool / hypersaline-basin analogues**  
  Rare deep depressions visually representing dense brine accumulation. Do not introduce a custom fluid or assume fluid-layer behavior until a safe implementation path is verified; geometry and mineral crust may precede actual fluid differentiation.

- **OSF-022 — Chemosynthetic mat fields**  
  Broad pale/dark bacterial-mat analogues around seeps and diffuse vents, implemented with safe decorative blocks or future custom textures rather than valuable materials.

### Shelf, slope and sediment-transport features

- **OSF-023 — Shelf sand-wave / ripple fields**  
  Large bedform patterns in shallower shelf and upper-slope zones, distinct from ordinary flat sand disks.

- **OSF-024 — Shelf-edge erosional scarps**  
  Small step-like cuts, exposed rock/sediment faces and headwall scars preceding larger slope failures.

- **OSF-025 — Submarine canyon systems**  
  Large shelf/slope-cutting channels that descend toward the deep basin. These should be terrain-scale systems and can intersect the existing custom slope caves without being identical to caves.

- **OSF-026 — Canyon tributary gullies**  
  Smaller branching channels feeding the main submarine canyon network.

- **OSF-027 — Turbidity-current channels**  
  Sinuous deep-water sediment-transport channels extending from canyon mouths across lower slopes and plains.

- **OSF-028 — Submarine fan lobes**  
  Broad sediment aprons deposited where turbidity channels exit onto flatter abyssal terrain.

- **OSF-029 — Levee and channel-margin ridges**  
  Low parallel depositional ridges flanking major turbidity channels.

- **OSF-030 — Contourite drift fields**  
  Elongated sediment accumulations shaped by persistent bottom currents, especially along lower slope and basin margins.

- **OSF-031 — Slump blocks / rotated sediment rafts**  
  Large coherent blocks displaced downslope beneath shelf-collapse headwalls, complementing AGE-013.

- **OSF-032 — Debris-flow boulder trains**  
  Chaotic linear or fan-shaped fields of transported blocks and mixed sediment on steep slopes and trench walls.

- **OSF-033 — Canyon-mouth talus fans**  
  Rock/gravel aprons concentrated where steep canyon walls meet deeper basin floors.

- **OSF-034 — Sediment scour pits**  
  Irregular current-eroded hollows around obstacles, rock outcrops or former structures.

- **OSF-035 — Abyssal sediment ponds**  
  Smooth fine-sediment pockets collecting between rougher volcanic/faulted terrain.

- **OSF-036 — Hadal ponded-sediment basins**  
  Very deep flat pockets accumulating fine material between trench scarps and axial channels.

### Abyssal and hadal mineral/surface features

- **OSF-037 — Manganese / polymetallic nodule-field analogues**  
  Scattered dark nodules across abyssal sediment plains. Decorative/non-progression material unless a later recipe review explicitly approves otherwise.

- **OSF-038 — Ferromanganese crust analogues**  
  Dark mineral coatings on exposed hard substrate, especially seamounts and old volcanic rock.

- **OSF-039 — Calcite/chalk ooze patches**  
  Pale fine-sediment areas using calcite-compatible visual language where appropriate.

- **OSF-040 — Red-clay abyssal patches**  
  Low-relief reddish/brown deep sediment provinces, subject to verified block palette availability.

- **OSF-041 — Exposed abyssal bedrock pavements**  
  Sediment-starved hard-rock patches on current-swept or tectonically active seafloor.

- **OSF-042 — Mineral-veined fracture faces**  
  Sparse non-ore mineral staining and calcite/dripstone-like veins across exposed fracture walls.

- **OSF-043 — Trench axial channels**  
  Narrow deep channels running along the lowest portion of hadal trenches, representing continued sediment transport along the trench floor.

- **OSF-044 — Trench-wall landslide scars**  
  Large headwalls and stripped surfaces feeding the collapse debris and boulder fields below.

### Biogenic and organic-fall features

- **OSF-045 — Whale-fall sites**  
  Rare large skeletal carcass-fall analogues using bone-block/bone geometry or future custom remains. Variants should represent different decomposition stages: relatively coherent skeleton, dispersed ribs/vertebrae, and heavily sedimented old fall. These are ecological landmarks, not loot piñatas.

- **OSF-046 — Mature whale-fall bone reefs**  
  Older scattered skeleton/bone-bed forms with surrounding chemosynthetic-mat analogues and mineralized sediment.

- **OSF-047 — Small cetacean / large-fish fall analogues**  
  Much smaller and rarer skeletal/organic-fall scenes allowing biogenic detritus without every discovery being a full whale skeleton.

- **OSF-048 — General bone-bed / scavenger-fall patches**  
  Dispersed bone fragments and disturbed sediment representing accumulated biological remains. No high-value loot dependency.

- **OSF-049 — Wood-fall sites**  
  Sunken trunks, root masses and timber fragments supporting localized deep-sea biological succession. Natural wood falls must be visually distinct from factional wreckage or manufactured debris.

- **OSF-050 — Kelp / macroalgal detritus falls**  
  Organic debris piles transported downslope from productive shallower waters, most plausible on shelf/slope and lower-slope margins.

- **OSF-051 — Cold-water coral gardens**  
  Sparse deep coral-framework analogues on hard substrate, cliffs and seamount flanks. Use only blocks/organisms verified to behave acceptably at depth or replace with custom decorative equivalents.

- **OSF-052 — Coral-rubble fields**  
  Broken/dead framework accumulations beneath cliffs, seamounts and old biological growth areas.

- **OSF-053 — Deep sponge gardens**  
  Sparse clusters on hard substrate and current-swept seamount/slope terrain. Implementation depends on safe decorative palette availability.

- **OSF-054 — Filter-feeder / crinoid-field analogues**  
  Low-profile biological-garden scenery on current-exposed rock surfaces, preferably via future custom decorative blocks rather than misusing valuable vanilla items.

- **OSF-055 — Shell-hash / mollusk-bed analogues**  
  Pale shell-rich sediment patches around seeps, shelves and productive slope environments.

- **OSF-056 — Chemosynthetic seep-fauna gardens**  
  Tube-worm/mussel-like environmental clusters around seeps and vents. These should be visual/ecological features and require verified or custom assets rather than invented registry IDs.

### Current-conditioned and erosional microfeatures

- **OSF-057 — Current scour moats around seamounts/outcrops**
- **OSF-058 — Sediment tails behind boulders and structures**
- **OSF-059 — Rippled mud/sand transition patches**
- **OSF-060 — Exposed-rock streaks along bottom-current corridors**
- **OSF-061 — Small erosional potholes and depressions**
- **OSF-062 — Sediment drapes over old lava and debris**
- **OSF-063 — Buried-to-exposed transition variants for natural features**
- **OSF-064 — Mixed hardground/soft-sediment mosaics**

These microfeatures should usually be configured/placed features or surface-expression rules rather than structure templates.

## Depth and condition weighting

The neutral pool is not a uniform random table. Each depth zone must preferentially draw the processes that make oceanographic sense there.

### Shelf / shelf edge
Favor:
- OSF-023 sand waves;
- OSF-024 erosional scarps;
- OSF-025/026 canyon heads and tributary gullies;
- OSF-031 slump blocks;
- OSF-049/050 wood and macroalgal falls;
- OSF-051/052 coral gardens/rubble where substrate and temperature permit;
- OSF-055 shell-rich sediment.

### Continental slope / cliff region
Favor:
- OSF-025/026 canyon systems;
- OSF-027 turbidity channels;
- OSF-030 contourite drifts;
- OSF-031/032 slump/debris-flow fields;
- OSF-033 canyon-mouth talus;
- OSF-012 exposed fault faces;
- OSF-049/050 organic falls;
- OSF-051–054 hard-substrate biological gardens.

### Abyssal plain
Favor:
- OSF-019 pockmarks;
- OSF-017/018 seep systems;
- OSF-028/029 submarine fans and levees;
- OSF-030 contourite drifts;
- OSF-035 sediment ponds;
- OSF-037 nodule fields;
- OSF-039/040 sediment-province variants;
- OSF-045–050 whale/organic falls;
- rare OSF-002/003 isolated seamounts/guyots.

### Fracture / ridge provinces
Favor:
- OSF-001 volcanic cones;
- OSF-004 calderas;
- OSF-005 pillow lava;
- OSF-006/007 lava tubes and skylights;
- OSF-008/009 flows and dike swarms;
- OSF-011 rift grabens;
- OSF-013–016 hydrothermal systems;
- OSF-038/041/042 exposed mineralized hardground;
- OSF-051/053/054 hard-substrate biological gardens where appropriate.

### Hadal trench walls and floor
Favor:
- OSF-012 fault scarps;
- OSF-021 rare brine-basin analogues where implementation is safe;
- OSF-032 debris-flow boulder trains;
- OSF-036 ponded sediment basins;
- OSF-043 axial channels;
- OSF-044 landslide scars;
- rare OSF-013–016 hydrothermal activity;
- rare OSF-045/046 deep whale falls;
- sparse OSF-041/042 hardground/mineralized faces.

## Implementation doctrine

- AGE-018 is neutral and may spawn in either faction's ocean geography when the relevant depth/condition selector matches.
- AGE-018 must never act as a bridge allowing Pelagos built remnants into Eastern biomes or Karsic built remnants into Western biomes.
- Prefer terrain-density deformation for seamounts, canyons, calderas, grabens and other landforms larger than practical structure templates.
- Prefer configured/placed features or surface rules for ripples, nodules, sediment patches, mineral crusts, bacterial mats and other distributed geology.
- Prefer deterministic NBT structures for coherent localized scenes such as whale falls, tube skylights, chimney groups, coral/sponge gardens and discrete slump blocks when a structure template is the more natural representation.
- Do not use exposed flowing lava as a default stand-in for active submarine volcanism. Magma blocks, basalt and controlled enclosed lava may be considered only after runtime behavior/performance validation.
- Whale falls and other carcass analogues must be rare enough to remain notable discoveries.
- Geological minerals are environmental texture first. They must not provide diamonds, netherite, high-tier ores or progression-bypassing resources.
- Biological gardens must use verified registry IDs or custom pack assets. Do not guess mod IDs.
- Surface and biological features must preserve submarine navigability and must not fill every cave mouth, trench or plain with visual clutter.

## Production priority

First implementation tranche:
1. OSF-005 pillow-lava fields;
2. OSF-006/007 cooled lava tubes and tube skylights;
3. OSF-019 pockmark fields;
4. OSF-023 sand-wave/ripple fields;
5. OSF-027 turbidity-current channels;
6. OSF-037 nodule-field analogues;
7. OSF-045 whale-fall sites;
8. OSF-049 wood-fall sites.

Second tranche:
- OSF-001/002/004 volcanic cones, seamounts and calderas;
- OSF-025 submarine canyon systems;
- OSF-028/029 submarine fans and levees;
- OSF-030 contourite drifts;
- OSF-031/032 mass-wasting features;
- OSF-051–056 biological-garden families.

Third tranche:
- larger terrain-conditioned province systems, hadal axial/depositional features, brine analogues and additional microfeature variation after runtime terrain inspection becomes available.

## Validation boundary

None of AGE-018's planned additions should be described as active until implementation files and worldgen references are committed. Runtime must later verify landform scale, placement frequency, block interaction, bubble behavior, cave/tube flooding, submarine clearance, feature overlap and generation cost.

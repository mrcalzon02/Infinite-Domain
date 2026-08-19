# Infinite Domain Cyberware Conversion Plan

## Decision

Create Cybernetics (`createcybernetics`) is the authoritative cyberware system for Infinite Domain.

Cyber Ware Port (`cyber_ware_port`) remains installed as a compatibility and donor-content mod, but its surgery system is retired from pack progression. Its components and implants become salvage, conversion inputs, and advanced assembly ingredients for Create Cybernetics-native implants.

This direction follows the installed content: Create Cybernetics exposes roughly 389 registered items and a substantially deeper API for humanity, per-slot installation, requirements, incompatibilities, power, degradation, repair, dyes, limb sides, cyberdecks, chipware, wetware, and integration recipes. Cyber Ware Port exposes roughly 93 items and a second, overlapping installation path.

## Authority boundary

| Concern | Authoritative system | Treatment of the other system |
|---|---|---|
| Surgery and installed-player capability | Create Cybernetics | Port surgery machines are retired |
| Body slots and humanity cost | Create Cybernetics | Port slot/essence values are not used for new content |
| Energy, degradation, and repair | Create Cybernetics | New items implement the Create Cybernetics API |
| Engineering and fabrication | Create Cybernetics Engineering Table and Create machinery | Port workbench may remain as a donor teardown bench |
| Existing Port implants | Create-compatible conversion recipes | Never deleted from inventories or worlds |
| CyberChems | Create Cybernetics support chemistry | Used as calibration and stabilization reagents |
| Darknet drops | End-era assembly gate | Used in top branch recipes, never as an alternate surgery system |
| Shops and quests | Create Cybernetics progression | Port surgery tasks and offers are removed or converted |

## Machine retirement

The following Cyber Ware Port blocks are the legacy installation pair:

- `cyber_ware_port:robo_surgeon`
- `cyber_ware_port:surgery_chamber`

Retirement is implemented non-destructively:

1. Remove all recipes whose output is either legacy surgery block.
2. Cancel placement of either block with a short player message directing players to the Create Cybernetics clinic.
3. Cancel interaction with already placed legacy surgery blocks so the second installation capability cannot remain active.
4. Add recovery recipes that consume the legacy machines and return Create Cybernetics machinery or useful donor components.
5. Do not scan inventories, delete items, or silently replace existing world blocks.

The Port workbench and scanner may remain because they do not establish the competing installed-player capability. Their role becomes inspection and donor teardown.

## Donor conversion matrix

| Cyber Ware Port source | Create Cybernetics destination |
|---|---|
| `component_actuator` | `component_actuator` |
| `component_fiberoptics` | `component_fiberoptics` |
| `component_plating` | `component_plating` |
| `component_storage` | `component_storage` |
| `component_synthnerves` | `component_synthnerves` |
| `component_microelectric` | wiring/diodes/LED salvage split |
| `component_ssc` | SSD/graphics-card salvage split |
| `component_titanium` | titanium rod/sheet salvage split |
| `component_fullerene` | mesh and high-density substrate |
| `component_reactor` | battery/reactor core and end-era assemblies |
| Port cyberware, pristine | calibrated donor module plus recoverable components |
| Port cyberware, scavenged | degraded donor module with lower recovery yield |

Conversions should be lossy enough that Port loot is useful without bypassing the Create Cybernetics engineering ladder. Direct component equivalents return one part; complex components return partial or probabilistic outputs through the engineering/deconstruction path.

## New catalogue target

Add 48 installable Create Cybernetics-native items: four branches for each of its 12 native slots.

| Branch | Role | Cost profile | Durability/power profile |
|---|---|---|---|
| Degraded | Cheap downgrade with a real drawback | Salvage plus low-tier components | Low durability, easy repair, usually passive |
| Reclaimed | Practical sidegrade | Degraded unit, Port donor, and CyberChem reagent | Moderate durability and modest power draw |
| Calibrated | Focused upgrade | Reclaimed unit plus existing Create Cybernetics implant(s) | High durability, meaningful power draw |
| Darknet | End-era specialist assembly | Multiple cyberware parts, high assembly, and Darknet drops | Expensive, high humanity/power burden, strongest effect |

Native slots:

- Brain
- Eyes
- Heart
- Lungs
- Organs
- Right arm
- Left arm
- Right leg
- Left leg
- Muscle
- Bone
- Skin

Left/right limb branches use paired names and textures, and support only their correct native side. They may share a gameplay family but remain distinct installable parts.

## High-end assembly chain

Four non-installable assemblies bridge the ecosystems:

1. Ghost-Circuit Lattice: Create Cybernetics neural hardware + Port fiberoptics + Darknet data cache.
2. Quantum Synapse Matrix: multiple neural/storage parts + Ghost-Circuit Lattice + mid/high Darknet injector.
3. Void-Shield Mesh: skin, mesh, fullerene, and high-tier Darknet access material.
4. Datavore Control Core: Quantum Matrix + Void Mesh + Port reactor + Darknet Temporal Core + Tier VIII injector.

Darknet-tier implants consume one of these assemblies plus an earlier implant from the same branch. This prevents direct crafting of end-era gear from drops alone.

## Texture strategy

Every new icon derives from an existing Create Cybernetics texture. The generator applies a branch-specific palette and overlay:

- Degraded: desaturated metal, oxidation, broken traces, red fault marks.
- Reclaimed: mismatched brass/copper patches and visible repair seams.
- Calibrated: clean cyan signal traces and reinforced edges.
- Darknet: violet substrate, cyan data pulses, and sparse void-black masking.

Left/right limb textures retain their handed silhouettes. No generated icon replaces an upstream asset; all variants live in the Infinite Domain namespace.

## Progression and quest conversion

The existing `Cyberware Ascension` chapter currently mixes both systems. Convert it to this order:

1. Recover the hospital.
2. Build the Create Cybernetics Engineering Table.
3. Build its Surgery Chamber and Surgery Table.
4. Learn donor teardown using the Port workbench/scanner.
5. Convert a Port component into a Create Cybernetics component.
6. Build a first degraded implant.
7. Build a reclaimed sidegrade using a Port donor and CyberChem.
8. Install foundational Create Cybernetics limbs/organs.
9. Build the Create Cybernetics Robosurgeon.
10. Produce a calibrated branch.
11. Enter Cyberspace and recover Darknet materials.
12. Assemble an end-era Darknet implant.

The quest-pack shop must use the same item and price catalogue as the main shops. Legacy Port surgery machines are excluded from every shop. Donor parts may be sold only at salvage-tier prices; calibrated and Darknet implants remain craft-only.

## Balance guardrails

- No Port conversion may yield more Create Cybernetics material value than its recipe cost.
- Degraded implants must remain useful but carry an explicit drawback.
- Reclaimed and calibrated branches must be sidegrades or specializations, not universal linear upgrades.
- Darknet implants require at least one earlier branch implant, one multi-part assembly, and one Darknet campaign gate.
- Humanity, energy draw, and durability increase with capability.
- Scavenged donor drops cannot skip the Engineering Table or surgery milestones.
- All shop prices use the pack's default exchange rate and mirror into the Quest Pack shop.

## Implementation order

1. Retirement and migration scripts for the Port surgery pair.
2. Port-to-Create component conversion recipes and donor tags.
3. Create Cybernetics-native companion item classes and registrations.
4. Generated models, recolors, and overlays.
5. Four-branch recipes and Darknet assembly chain.
6. Mob salvage drops and deconstruction recovery.
7. Quest and shop retargeting.
8. Registry, recipe, texture, quest, and live-log audits.

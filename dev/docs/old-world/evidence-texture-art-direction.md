# Old World Evidence Item Texture Direction

This is the production art contract for the 64 proof items registered by `kubejs/config/old_world_evidence.json`. The `art` field on every item selects a physical object archetype. It is not a palette preset.

## Global rules

Proof items must read by silhouette at inventory scale before surface detail is considered. Preserve material identity first: paper must read as paper, stamped steel as steel, ceramic as ceramic, polymer as polymer, glass as glass, and electronic media as manufactured electronic media. Apply the established LAST DAYS hierarchy: broad material masses first, construction and segmentation second, seams/fasteners/connectors third, localized damage and dirt last.

Do not author one universal document, card, or data chip and recolor it sixty-four times. Wear must follow handling and failure mode: folded paper creases at folds, steel plates abrade around mounting holes, cartridges damage around connectors and latches, cold-chain items frost around seals, medical carriers crack around clear windows, and field electronics weather around exposed edges.

Author directly at the native inventory texture resolution used by the surrounding pack. Enlarged nearest-neighbor previews are review aids only; they are not source art. No generic saturation reduction, rust-speckle, dirt-noise, or automatic edge mask is acceptable as the primary transformation.

## Institutional object families

### Verdant Continuum Foods / VCF
Use laminated field manifests, molded culture-vial carriers, thick weathered cultivation handbooks, and rigid specimen/data cards. Agricultural evidence should feel mass-produced and mundane before it becomes ominous: cold-chain labels, batch ticks, culture handling symbols, torn return tags, condensation marks, and later contamination annotations.

### Atlas Kinetic
Use stamped service plates, grease-stained maintenance punch cards, folded industrial manuals, and rugged controls archive cartridges. Shapes should emphasize mounting holes, keyed connectors, serial fields, machine hazard markings, and mechanic handling rather than corporate stationery.

### PolyCore
Use tested material coupons, fractured ceramic/composite tiles, sealed engineering failure packets, and barrier-test cartridges. Damage should expose cross-sections, fracture edges, sample notches, impact rings, clamp marks, and lot identifiers. These are physical evidence of material failure, not generic paperwork.

### Pleroma
Use freight manifests, insulated cold-chain tags, broken container-seal records, and stacks of logistics data wafers. Emphasize routing blocks, container IDs, tamper seals, inspection marks, temperature indicators, and keyed freight-system contacts.

### Aevum
Use clinical patient cards, biologic vial cases, medical data wafers, and sealed archive cartridges. Keep them recognizably medical through biometric strips, treatment fields, sample sockets, cold-storage marks, privacy tabs, and reinforced clinical archive housings rather than simple white/red recolors.

### Helion
Use heavy electrical service tags, grid-control cartridges, scorched incident plates, and coolant sample cases. Include cable eyelets, voltage/breaker fields, heat warping, soot localized to failure edges, gasket geometry, crystallized coolant residue, and utility-system connectors.

### Blackglass
Use matte encrypted data wafers, armored archive cartridges, access tokens, and cracked compact tablets. The family should be sparse and deliberately hard to read: recessed serials, broken seals, shielded contacts, revoked-access marks, and small surviving status glyphs. Avoid making every object a featureless black rectangle.

### Emergency Authority
Use punched quarantine passes, reinforced perimeter/continuity badges, and chemically stained decontamination incident cards. These should feel rapidly issued, heavily handled, and repeatedly checked.

### Joint Research / Continuity / Meridian Military
Joint Research receives a biohazard-sealed incident cartridge. Meridian Military uses command-directive folders, rugged operations wafers, and bent after-action plates. Continuity uses reinforced cross-disciplinary archive cartridges and field-science folders. Continuity Science uses a weathered atmospheric monitoring cartridge. Their forms may share emergency-era manufacturing, but silhouettes must remain function-specific.

### Civilian and Municipal
Civilian proof should be materially humble: battered handwritten logbooks and folded evacuation notes. Municipal evidence uses mounted closure notices, utility logbooks, removed refuge-board sheets, and punched relief distribution cards. Handwriting, tape residue, thumbtack holes, water damage, and improvised corrections distinguish these from institutional data media.

### Asterion
Use launch manifests, mission-control cartridges, orbital communications wafers, spacecraft assembly work-order folders, and a large armored primary-launch archive. This family should become progressively more specialized and robust as the terrestrial story approaches the space transition: telemetry strips, payload blocks, shielded contacts, assembly stage tabs, mission insignia recesses, multiple connectors, and emergency seals.

## Initial authoring order

Author VCF OWS-001 through OWS-008 first because those eight items establish the earliest agricultural narrative and exercise four different physical silhouettes. Then author Atlas and PolyCore, followed by logistics/medical/utilities, then encrypted/emergency/military evidence, and finally Asterion. Each completed batch should be checked at native size beside existing LAST DAYS inventory items before the next family is accepted.

Every texture path is `kubejs/assets/kubejs/textures/item/<proof_item_id>.png`; the registry already points to those exact paths.

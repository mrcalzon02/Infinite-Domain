# Atlas Kinetic Evidence Texture Recovery Method

Status: **Atlas OWS-009 through OWS-014 proof art is rejected and must be re-authored.**

This document records the recovery gate after the failed Atlas graphics pass. It does not approve or regenerate any Atlas texture.

## What the repository actually shows

The Old World evidence registry and item paths are structurally sound, but the previous Atlas PNGs cannot be treated as accepted merely because they exist. The inspected PNG headers show the rejected Atlas service plate and the accepted VCF evidence examples both use a 128×128 canvas. A nearby successful item-specific pack texture such as `apple_soda_can.png` is also 128×128. Meanwhile the established progression-item pipeline deliberately authors cohesive icons at 32×32.

That means **resolution is not the art style**. Infinite Domain already contains both deliberate 32×32 pixel-authored icons and more detailed 128×128 item-specific sprites. Atlas therefore must be judged by silhouette, construction, material identity, information hierarchy and inventory-scale legibility, not by canvas size or by matching the orange institutional palette.

The repository’s existing `scripts/audit_texture_quality.py` already provides the correct review pattern: preserve alpha, build nearest-neighbor contact sheets, and inspect icons together rather than judging an enlarged image in isolation. `scripts/build_progression_item_textures.py` also demonstrates the useful construction order: broad shell first, then inset panels/segmentation, then small identifying features. The Atlas recovery method must follow those proven pack practices instead of generic image-generation cleanup.

## Production method

Atlas evidence will use a 128×128 final canvas because that is the established Old World evidence canvas and is also used by successful nearby item-specific assets. Every object must first be designed as a readable inventory silhouette. During authoring, the sprite must be repeatedly previewed at approximately 32×32 and 16×16 effective display size; details that only exist when the 128×128 source is enlarged do not count as communicated information.

Construction order is mandatory:

1. Define the physical object archetype and its outer silhouette.
2. Establish broad material masses and large value breaks.
3. Add construction geometry: folded sections, housings, reinforced edges, recessed panels, spines, clamps or mounting flanges.
4. Add functional details: mounting holes, fasteners, serial fields, keyed connectors, punch marks, latches, hazard bands or service tabs.
5. Add only localized use/damage appropriate to how that object is handled.
6. Add Atlas identity last, as a manufactured marking on an already recognizable object rather than as the thing that makes the object recognizable.

Noise, rust speckles, desaturation, scratches and orange recoloring are not a substitute for construction.

## Six Atlas object archetypes

**OWS-009 — `atlas_service_plate`**  
A stamped metal machine service plate, not a document. It needs a rigid plate silhouette, mounting holes or rivet positions, stamped/engraved serial zones, a machine-rating field and edge wear concentrated around mounting and handling points. The object should remain readable as metal even with the Atlas markings removed.

**OWS-010 — `atlas_transfer_maintenance_card`**  
A mechanic-handled punch/service card. It should be thinner and less rigid than the service plate, with clipped or worn paper/card edges, grease-finger handling, punched service intervals and a compact machine-routing field. It must not share the service plate silhouette.

**OWS-011 — `atlas_emergency_service_log`**  
A field-service log or compact rugged clipboard/binder used in a municipal emergency shop. It needs a bound or clamped construction, multiple visible page/tab masses and hard-use edge damage. Municipal/emergency markings should coexist with Atlas equipment-service fields.

**OWS-012 — `atlas_bulk_process_manual`**  
A folded or bound industrial manual with enough thickness to read as a manual rather than a single sheet. Give it a reinforced spine, tabbed process sections, crusher/mill hazard symbology and localized shop grime around page edges and grip zones.

**OWS-013 — `atlas_manual_bypass_notice`**  
A lockout/bypass object rather than generic paperwork. Use a rigid or laminated warning-card/tag silhouette, attachment slot or clamp point, strong manual-override field and service-authority markings. Damage should occur around the attachment and repeatedly handled corners.

**OWS-014 — `atlas_controls_archive_module`**  
A manufactured electronic archive cartridge. It requires a housing, connector edge, keyed insertion geometry, latch/recess features and protected serial/status surfaces. Orange Atlas markings are secondary to the electronics construction. This object should be visually closer to rugged industrial data media than to any document family.

## Review gate before any Atlas art commit

No Atlas proof texture may return to `kubejs/assets/kubejs/textures/item/` until the six rejected outputs have been replaced rather than edited forward.

For each replacement, review it beside:
- the accepted VCF Old World proof sprites;
- several successful 128×128 item-specific pack sprites;
- several successful 32×32 progression icons enlarged with nearest-neighbor scaling.

Acceptance requires that the object class be identifiable without reading text or relying on Atlas orange, that the material is recognizable, that the silhouette remains distinct from the other five Atlas objects, and that meaningful construction survives inventory-scale preview.

The first accepted replacement should establish the family’s line weight, value grouping and pixel-cluster discipline. The remaining five should inherit those rendering conventions while preserving genuinely different object construction.

## Repository status rule

Until this gate is passed, Atlas evidence IDs, item registration, loot placement, structure descendants, quest/locator hooks and narrative logic may continue to advance. **Atlas proof PNGs may not.** Missing Atlas PNGs are preferable to silently shipping the rejected pass as if it were approved art.

# [SYSTEM REPORT] OWS-005 Heavy-Rebuild Restart Dossier

**Target:** OWS-005 — Verdant Continuum Foods Harvest & Packaging Annex  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Frozen Phase-0 baseline:** `d2cdec5739d8d2c1423973f6ed7c59ee59224789`  
**Shipping structure:** `infinite_domain:old_world/ows_005_vcf_harvest_packaging_annex`  
**Donor:** `infinite_domain:abandoned_orchard_cannery_clean_master`  
**Current dimensions:** 59 x 24 x 51  
**Narrative phase:** Early anomaly  
**Functional status:** static source implemented; runtime/worldgen activation deferred

## Institutional purpose

OWS-005 is the downstream consumer-food interface of VCF's Evercrop system. Harvest lots arrive from cultivation sites, are identified and checked, pass through PT-9 sanitation and quality control, are graded and packed, enter temperature-controlled finished-goods holding, and leave as ordinary branded food. The site proves that Evercrop was embedded in routine commerce before the public understood the anomaly.

Canonical workflow:

`harvest receiving -> lot registration -> dirty/raw staging -> wash and PT-9 sanitation -> inspection/reject diversion -> grading -> packing and case coding -> cold hold -> dispatch`

Supporting flows must include clean packaging supply, sanitation chemicals and wash-water service, refrigeration plant, rejected-lot quarantine, staff hygiene/changeover, waste/culled-product exit and maintenance access.

## Donor audit

The clean cannery donor contributes useful food-industry bones:

- a 59 x 24 x 51 site with enough depth for a one-direction material flow;
- a substantial brick processing hall and attached lower service volumes;
- factory-floor surfaces, large enclosed spans and roof monitors/clerestories;
- an orchard/loading side that can be reinterpreted as harvest arrival and covered raw staging;
- existing receiving, wash, heating/processing, packing and rear loading cues;
- eight working door leaves and 647 framed-glass blocks in the functional derivative.

Those relationships are useful, but the donor remains an orchard cannery rather than an advanced sanitary packing annex.

## Shipping implementation audit

The frozen and live shipping NBT are byte-identical at audit time. The generated structure record reports 59 x 24 x 51, 23,785 placed blocks, 47 palette states, 5,133 modded blocks, one proof chest, no spawners and no vertical-access span.

Existing VCF overlay value:

- a wash/sanitation lane using light-blue floor coding, fluid pipe and tanks;
- four inspection/press/depot stations;
- carton staging, cooler banks and palletized output;
- a yellow rejected-lot/quarantine field;
- deterministic `kubejs:vcf_packaging_quality_report` proof in the canonical loot table;
- the intended raw-to-packed workflow is partially recoverable from coordinates.

Blocking weaknesses:

- most of the architecture is unchanged brick cannery geometry;
- VCF identity is primarily a white/lime stripe pasted onto the front wall;
- the large orchard canopy dominates the silhouette without reading as controlled receiving;
- material-flow stations are isolated equipment islands inside a generic hall;
- raw receiving, clean packaging supply, rejected-lot removal and finished dispatch are not architecturally separated;
- cold storage is a small exposed equipment bank rather than an insulated zone with connected refrigeration plant;
- PT-9 sanitation is a colored floor patch, not a controlled hygiene boundary;
- the main roof is a broad flat/monitor surface without coherent refrigeration, ventilation, wash-water or maintenance anatomy;
- no encounter architecture exists; later passes must add deliberate pressure without endangering proof;
- current proof placement at local `(52, 2, 36)` is guaranteed but visually close to carton/quarantine staging and must be retained or deliberately relocated to a credible quality-records node through serialized integration.

## Provisional donor disposition

Retain, subject to Gate A/B review:

- the 59 x 24 x 51 worldgen envelope for the first massing study;
- the long food-factory orientation and one-direction flow opportunity;
- a limited brick/copper industrial-memory layer rather than the whole donor facade;
- roof-monitor daylighting where it agrees with clean processing areas;
- the western arrival-yard concept and eastern/rear dispatch opportunity;
- canonical IDs, quest task, loot table and guaranteed proof system.

Rebuild substantially:

- receiving and dispatch as distinct vehicle/product thresholds;
- raw, wet/sanitation, clean packing and cold-hold architectural zones;
- public/quality-assurance frontage and staff hygiene threshold;
- insulated cold-storage mass and connected roof/service plant;
- structural rhythm, roof hierarchy and loading canopies;
- reject/quarantine architecture so the early anomaly grows from ordinary QA practice;
- VCF identity as sanitary workflow and optimistic food infrastructure, not only lime color.

## Doctrine state

Donor audit is complete. The exact frozen baseline has been rendered and reviewed separately in `OWS-005_PHASE0_BASELINE_REVIEW.md`; it requires a substantial rebuild. Functional implementation remains preserved as a separate status and is not treated as runtime approval.


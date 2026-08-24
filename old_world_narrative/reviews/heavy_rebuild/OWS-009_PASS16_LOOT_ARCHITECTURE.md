# OWS-009 Pass 16 — Loot Architecture

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Canonical table:** `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`  
**Status:** implemented for Gate-C r1

Gate C adds no ad-hoc loot. Exactly one chest uses the existing canonical table, which guarantees one `kubejs:atlas_service_plate`, one `kubejs:atlas_transfer_maintenance_manual`, and bounded repair-material rolls. The container is placed only in D3 at the controlled records/proof node.

Parts crates, depots, steel core bins and data drives remain architectural blocks without duplicate loot tables.

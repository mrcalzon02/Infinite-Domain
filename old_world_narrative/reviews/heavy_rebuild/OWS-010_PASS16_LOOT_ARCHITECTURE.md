# OWS-010 Pass 16 — Loot Architecture

**Target:** OWS-010 — Atlas Conveyor Transfer Hall  
**Canonical table:** `infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall`  
**Status:** implemented for Gate-C r1

Exactly one D3 chest uses the existing canonical table. The table guarantees one `kubejs:atlas_transfer_maintenance_card` and adds bounded Atlas repair materials through its existing rolls. No replacement or ad-hoc table is introduced.

Physical crates, removed modules, depots, empty shelves and data drives remain environmental architecture without secondary loot contracts. The canonical table contains no `kubejs:atlas_transfer_maintenance_manual`, so LOR-006 is not duplicated.

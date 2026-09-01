# OWS-009 Pass 2 — Functional Definition

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Institution:** Atlas Kinetic Industries  
**Narrative phase:** Phase A — pre-crisis / normal operation  
**Status:** complete for Passes 2–5 planning; no massing authorized

## Exact institutional function

OWS-009 is a compact roadside depot that diagnoses, exchanges and recalibrates standardized mechanical drive assemblies used by freight vehicles, agricultural machines and small industrial equipment. It is not a general consumer garage, a vehicle showroom, a warehouse or a miniature factory.

Atlas designed the depot around modular replacement: a disabled unit is recovered from the road, identified at intake, scanned and isolated, stripped only far enough to exchange a failed shaft/gearbox/control assembly, then calibrated and released. Failed assemblies move to bounded rework or return-to-plant stock rather than being improvised on the customer floor.

## Primary workflow

`road recovery / appointment arrival -> controlled intake -> diagnosis and lockout -> module strip-down -> replacement / repair -> calibration and loaded test -> release inspection -> outbound handoff`

Supporting flows:

- `parts delivery -> secure parts receive -> parts issue -> repair cell -> removed-core quarantine / return`;
- `tools / calibrators -> controlled issue -> technician service spine -> cell -> check-in`;
- `customer / driver -> pedestrian entrance -> service desk / viewing point -> release desk`;
- `oil, damaged components and refuse -> rear rework/waste hold -> separate collection`;
- `compressed air, power and exhaust -> roof/rear plant -> overhead service rails -> each bay`.

## Operational zones

1. **Recovery and intake apron** — disabled-unit drop, tow alignment and queue without crossing customer pedestrians.
2. **Customer/service bar** — reception, service authorization, status view and release paperwork; controlled away from operating bays.
3. **Bay 01: intake diagnostics and lockout** — scan gantry, wheel/drive restraint, tagged fault isolation and initial condition record.
4. **Bay 02: exchange and heavy repair** — lift/pit, overhead handling, strip bench and guarded press/assembly cell.
5. **Bay 03: calibration, loaded test and release inspection** — alignment datum, controlled run-up/load station and release checkpoint.
6. **Transverse unit-transfer aisle** — moves vehicles or modular pallets among cells while keeping work zones legible.
7. **Rear technician/service spine** — parallel staff route for tools, parts, power, air and removed assemblies; never used as customer circulation.
8. **Parts receive and controlled issue** — high-turn shafts/gears/casings near the service spine, with external replenishment access.
9. **Tool and calibrator crib** — checked tools and traceable reference equipment adjacent to Bay 03 and records.
10. **Rework/core return hold** — failed assemblies awaiting rebuild or return, separated from clean replacement stock.
11. **Service records and authorization custody** — protected Atlas plate/manual/proof setting, maintenance history and calibration release records.
12. **Utilities and roof plant** — exhaust capture, compressed air, power distribution, drainage and maintenance access visibly connected to work cells.

## Users and circulation

- **Customers/drivers** use only the pedestrian service entrance, desk and controlled viewing/release area.
- **Disabled and service vehicles** use the recovery apron and framed bay thresholds.
- **Technicians** move behind the cells through a two-block-minimum service spine.
- **Parts staff** enter from the side delivery threshold directly into receive/issue storage.
- **Removed cores and waste** leave through the rear/side rework threshold without crossing customer space or replacement stock.

## Atlas institutional reading

The depot must communicate maintainable heavy-industrial precision:

- standardized numbered bays rather than unrelated machines;
- orange tied to operational thresholds and service rails;
- charcoal machine frames, steel supports and justified yellow lockout fields;
- visible access around every machine and utility connection;
- replacement modules, tool control and calibration records treated as architecture;
- a short, legible service chain that explains why Atlas automation was valuable before it explains later maintenance pressure.

## Normal-operation historical constraint

This is an intact pre-crisis site. It may show repaired guards, replaced casings, scheduled-service tags, used-core stock and ordinary floor wear. It must not show quarantine, generalized collapse, emergency bypasses, fungus or crisis-scale cannibalization. Later D0 must first prove a functioning depot.

## Preserved integration contract

- structure ID: `infinite_domain:old_world/ows_009_atlas_roadside_repair_depot`;
- proof: `kubejs:atlas_service_plate`;
- lore: `kubejs:atlas_transfer_maintenance_manual`;
- loot table: `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`;
- quest / structure / proof tasks: `4F58000000000009`, `4F58100000000009`, `4F58200000000009`;
- major quest: `OWQ-01 — THEY WERE HERE FIRST`;
- deterministic proof remains inside a controlled records/parts-custody node, with exact final coordinates deferred to Pass 17.

## Anti-definition

OWS-009 must not become:

- an orange warehouse with random Create machinery;
- a three-car consumer repair shop with no automated material handling;
- a factory manufacturing new vehicles;
- a crisis ruin before intact operation is proven;
- a proof chest hidden in unrelated storage;
- a decorative gantry or service rail that reaches no real cell.

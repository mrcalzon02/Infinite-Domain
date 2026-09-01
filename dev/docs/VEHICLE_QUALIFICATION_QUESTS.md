# Vehicle Qualification and Interplanetary Freight

Date: 2026-08-29  
Status: Implemented as optional branches in Air, Sea and Global Logistics

## Purpose

The logistics chapter previously detected submarine and airship parts but did not
ask the player to operate either vehicle. Radar was represented by one dish, the
installed flight-control and propulsion extensions were absent, and the Moon
objective did not prove that industrial cargo returned to Earth.

This pass retains the existing 33 quests and IDs, then adds ten optional quests
(`5E...30` through `5E...39`). No Foundation Core, dimension route, or existing
quest depends on them. The branch therefore teaches and rewards vehicle engineering
without forcing unstable physics-mod behavior into civilization progression.

## Qualification ladder

### Submarine operations — Era 4

1. **Closed-Cycle Submarine Plant** adds an Electrolyzer, two Oxygene Diffusers,
   and two Water Thrusters to the existing pressure-hull and ballast lessons.
2. **Submarine Recovery Trial** witnesses controlled submergence, depth holding,
   atmosphere operation, propulsion restart, surfacing, and intact cargo recovery.

### Airship service — Eras 4–5

3. **Articulated Flight Controls** teaches Create Aeronautics: Transmission &
   Linkage through paired universal-joint rods and hydraulic regulators.
4. **Scheduled Cargo Circuit** requires one registered airship to serve two named
   Automated Logistics stations, carry a marked full container, return, and remain
   dispatchable after a stop.
5. **Integrated Traffic Control** connects Create: Radars to Create Aero Radars
   with a fixed dish, two vehicle links, and a safe-zone designator.

### High-energy flight and orbital freight — Eras 6–7

6. **Flight-Rated Avionics** reuses the established aerospace component tree:
   Avionics Controller, Navigation Unit, and Power Distribution Unit. Those parts
   already join AE2, PowerGrid, Create New Age, Immersive Engineering, Create, and
   Stellaris manufacturing.
7. **Vectored Propulsion Qualification** commissions four Create Propulsion:
   Simulated vector thrusters and four Create Aeronautics: Gadgets & Gizmos
   thrusters.
8. **Crewed Vehicle Qualification** witnesses translation, yaw, stationary hold,
   radar identification, deliberate power loss, and controlled landing or docking.
9. **Lunar Return Cargo** packages sixteen lunar laminates into the existing
   count-preserving Lunar Materials Pallet after the Moon base is reached.
10. **Interplanetary Service Qualification** witnesses the sealed pallet's return,
    inventory accounting, unloading at the named terrestrial endpoint, and vehicle
    readiness for the next mission.

The four witnessed procedures are manual checkmarks because FTB Quests cannot
reliably measure assembled-vehicle physics, station routing, failure recovery, or
cargo provenance. They have explicit icons and no material rewards.

## Non-bypassable vehicle recipes

Three exposed vehicle gateways now obey the cross-mod integration policy. The
curated recipe authority overwrites every enabled recipe ID for each output:

| Output | Functional industries now required |
|---|---|
| `create_radar:radar_dish_block` | TFMG structure, Create: Radars data link, AE2 calculation, Oritech machine core, PowerGrid control |
| `createpropulsion:vector_thruster` | Propulsion platinum/ion hardware, TFMG heavy plate, Create New Age motor, AE2 engineering processor |
| `createthrusters:thruster` | TFMG heavy plate, mod-local oxidizer, Create New Age motor, Create burner, PowerGrid control |

Create Aeronautics assembly hardware remains available earlier; the expensive
gate applies to instrumented high-thrust qualification, not the first experimental
airframe. Two identical-cost Thruster recipes remain because the installed mod
publishes two enabled recipe IDs; both are overwritten so neither is a cheaper
alternate route.

## Rewards and ownership

- Hardware is detected, not consumed; vehicles remain team infrastructure.
- Only Articulated Flight Controls, Flight-Rated Avionics, and Lunar Return Cargo
  pay one Cog each.
- Manual procedures pay nothing, so self-certification cannot mint value.
- The lunar pallet's scripted recipe is count-preserving and its objective is not
  repeatable.
- No new loot table, vendor, exchange, or free vehicle component was added.

## Validation

`scripts/audit_vehicle_qualification_quests.py` verifies exact optional topology,
14 registered item objectives, four unrewarded procedures, player-facing mod
signposting, scripted aerospace-component sources, every enabled gateway recipe
override, and at least three foreign functional industries per gateway.

Static validation cannot prove the installed physics implementations work under
load. A live team test should use one submarine and one airship built in survival,
then record:

1. submarine pressure/oxygen behavior and clean recovery after a propulsion stop;
2. station registration, transponder persistence, cargo transfer, and re-dispatch;
3. radar link/safe-zone behavior on a moving assembled vehicle;
4. high-thrust control, power-loss landing, and chunk-boundary recovery;
5. Lunar Materials Pallet inventory before launch and after terrestrial unloading.

# Create Specialist Workshops

Date: 2026-08-30  
Status: implemented; static validation complete, live commissioning pending

## Purpose

The optional `Create Specialist Workshops` chapter turns nine small Create extensions into connected settlement capabilities instead of isolated catalogue items. The chapter never gates a Foundation Core or later era. Its 24 quests open from the Mechanical Foundation and add later-era requirements only where the machinery actually needs mature industry.

## Workshop clusters

- Chimneys: iron/masonry exhaust stacks and a witnessed furnace-hall draft survey.
- Cardan Shafts and Linear Bearing: surveyed offset transmission, guided motion, magnetic docking, and a ten-cycle recovery trial.
- Escalated: powered walkways and escalators verified by the installed `escalated:walkway` and `escalated:escalator_100` advancements.
- Bells & Whistles and Mind the Gap: readable platforms, rolling-stock safety hardware, announcements, and a witnessed two-station passenger trial.
- Compact Gearbox: manual/sequential ratio control and a loaded transmission qualification.
- Delivery Required: ordinary export contracts, expensive emergency imports, and an Era 4 peer-logistics custody/return trial.
- Hypertubes: a two-way personnel line, routed junctions, entity/redstone detection, braking, escape, and recovery.

The Mind the Gap announcement flag is intentionally not a possession task. It is registered but has no enabled installed recipe; the chapter uses craftable announcement boxes and empty train signals instead.

## Progression and economy

Only five objectively detected hardware milestones award one Cog. Manual procedures and advancement tasks award no material reward. Delivery Required retains its 32-entry export allowlist, 17 ordinary emergency-import items plus 12 damaged salvage components, a three-times market price multiplier, a 256-item purchase ceiling, and reduced item-volume XP. Existing Contractor, Market, and P2P Ponders provide operating instructions.

Three outputs are governed by the deep-integration recipe authority:

- `compactgearbox:compact_gearbox` joins Create precision/control to TFMG heavy plate;
- `createdeliveryrequired:p2p_terminal` joins AE2 interfaces/computation to Create storage and PowerGrid control;
- `create_hypertube:hypertube_junction` joins Hypertube routing to AE2 calculation, PowerGrid control, TFMG fabrication, and Create brass.

Every enabled recipe ID for those outputs receives the same curated overlay, so alternate recipes cannot bypass the intended era seam.

## Scope correction

Older generated registry evidence mentions Rocketnautics/Cosmonautics. A complete scan of the current installed mod JARs finds neither namespace. They are not valid quest targets unless those mods are deliberately installed and the registry inventory is regenerated.

## Validation and live checks

Run:

```powershell
python scripts/audit_create_specialist_workshops.py
node scripts/audit_mod_signposting.js
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
```

The static contract verifies exact quest topology, localization, optional isolation, rewards, registered/reachable objective items, installed advancements, Delivery economy/Ponders, and all gateway overlays. The remaining live proof is a two-player contract and P2P custody cycle, a routed Hypertube return/escape test, and a normal-scale terminal layout review.

# Graveyard and Gateway Containment

Date: 2026-08-30

## Purpose

`Graveyard and Gateway Containment` is a fifteen-quest optional Civilization
Specialization spanning early Graveyard field evidence and late Cyberspace
gateway control. It closes two substantial installed-system gaps without making
either system part of a Foundation Core or later-era unlock.

The branch teaches:

- representative Graveyard lighting and funerary fittings;
- the pack-owned roadside church/cemetery, four ordinary Graveyard hostiles,
  Corruption recovery, dark-iron quarantine hardware, one natural horde, and a
  witnessed post-alarm recovery drill;
- the complete five-tier Gateway of Doom Portal Ward ladder;
- the blue, red, and violet Easy/Medium/Hard Devil Eyes;
- bounded arena, casualty, abort, cost-accounting, and two-player continuity
  procedures.

Five objective milestones pay one Cog each. All five witnessed procedures are
unrewarded, and `mobDropsEnabled` remains false, so neither manual certification
nor repeatable gateway combat becomes a material shortcut.

## World-generation ownership

All seventeen upstream Graveyard landmark switches remain disabled in
`config/graveyard-common.toml`. This preserves Infinite Domain's authored world:
the central main continent, its north/south zones, and the east/west continents
separated by the Pelagos and Karsic Abyssal oceans remain owned by the gradient
and regional structure programs.

The discovery objective uses the production-approved
`infinite_domain:wasteland/roadside_church_cemetery`. It is registered as a
normal jigsaw structure, selected from the ordinary Wasteland common set, and
restricted by `#infinite_domain:wasteland_rural_biomes`. The FTB structure task
only detects entry after placement. The preceding objective grants a standard
explorer-map handoff to the already generated site; it neither places nor
unlocks one. No quest, player, party, team, advancement, scoreboard, or game
stage creates or unlocks the site.

Graveyard's ordinary mob spawns and daily horde remain enabled. They provide the
mod's active ecological pressure without injecting a second uncontrolled
landmark distribution into the planned continents.

## Gateway ownership and bypass prevention

Gateway of Doom remains confined to `cyberspace:cyberspace_dimension`:

- the Overworld exploration, Nether timer, and End timer rules remain disabled;
- the ordinary Cyberspace hard timer remains enabled at 30–60 minute intervals;
- every Devil Eye is rejected outside ordinary Cyberspace without consumption;
- the Darknet and every offworld dimension remain excluded;
- the three Eye recipes require the matching ward and progressively stronger
  Cyberspace/Cyberware components;
- Portal Wards II–V consume the preceding ward tier.

The quest branch detects the ward and Eye items before use and witnesses the
encounters afterward. It does not run a command, place a portal, alter a timer,
grant an Eye, or change encounter profiles.

## Validation

Run:

```text
node scripts/generators/build_graveyard_gateway_containment.js
python scripts/audit_graveyard_gateway_containment.py
node scripts/generators/ensure_ftbquest_icons.js --check
node scripts/audit_ftbquests.js
python scripts/audit_quest_tree_coherence.py
python scripts/validate_overworld_geography.py
```

In-game follow-up should cover one fresh Wasteland cemetery discovery, a natural
Graveyard horde, all three manually activated gateway profiles in ordinary
Cyberspace, one passive hard gateway, a disconnect/withdrawal recovery, and the
two-player role exchange.

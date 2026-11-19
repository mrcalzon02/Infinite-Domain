# Darknet Anchor

Date: 2026-08-14

The pack repurposes the AE2 Spatial Anchor as the Darknet Anchor. Its inherited
item model and all six placed/powered textures use a dark oxblood and crimson
palette while retaining the original AE2 geometry and animation.

The recipe uses only Cyberspace and Applied Energistics technology: Quantum
Cores, Data Hardware, Virtual Machine Cores, a Darknet Temporal Core, a 128^3
Spatial Storage Component, a Tier VIII Session Injector, and a Dense Energy
Cell. Its quest follows Tier VIII as the permanent-access capstone.

The block is placeable only in the Darknet and binds to its placer. One anchor
may be bound per player. AE2 remains responsible for real chunk loading and
power validation through the Spatial Anchor block entity. While the anchor is
online, the bridge holds the owner's positive Darknet timer above expiration
anywhere in the dimension. Breaking the anchor or losing ME power sets the timer
to zero so Cyberspace's native recall returns the player to the recorded
Overworld position. The bound block destroys itself when its owner dies.
Placement and login allow ten seconds for the ME grid and its chunk ticket to
initialize. After that grace period, an unloaded or missing anchor is treated as
a severed tether and recalls the owner.

Keep the ME network compact: a Spatial Anchor loads every chunk containing part
of its network, and its native AE/t cost increases as that chunk count grows.

## Repair verification — 2026-10-13

The break handler now checks the event dimension before matching coordinates.
Previously, breaking an AE2 Spatial Anchor at the same coordinates outside the
Darknet could clear a player's Darknet binding and trigger recall. Only a break
in the Darknet can now sever the registered tether.

Run `node dev/scripts/test_darknet_anchor_runtime.js` for eleven behavioral
scenarios against the live script: valid/rejected placement, duplicate binding,
breaks in another dimension or at another position, owner recall, powered timer
maintenance without reviving expired sessions, power-loss grace, missing/unloaded
anchors, login grace, and death in the Darknet. These use mocked KubeJS and Java
objects; they do not confirm event delivery or AE2 chunk tickets in Minecraft.
The existing anchor, rejection-feedback, and Gateway configuration audits also
pass. Live client verification remains pending.

The broader quest audit still reports existing failures involving icons,
third-person Charles wording, and the Lyran Research explorer-map handoff.
Those failures are outside this tether repair. The cyberware mastery audit
passes.

## KubeJS 2101 dimension-access repair — 2026-11-19

Darknet Anchor placement, break, block-entity tick, player tick, death, and
recall checks now use the live KubeJS `Level.dimension` property instead of the
invalid `dimension().location()` call. The existing eleven-scenario handler
harness now mocks a **non-callable** dimension property, preventing a false pass
against an API that does not exist. Session Injector handlers use the same
property access, cancel invalid/inactive use only after showing feedback, and
show short three-second warnings instead of seventy-five-second overlays.

Run `node dev/scripts/test_darknet_anchor_runtime.js` and
`node dev/scripts/test_darknet_session_injector.cjs` for local simulated
handler checks. These are not proof of live KubeJS/AE2/Cyberspace event delivery,
ME-network tickets, or player recall. A full NeoForge 1.21.1 client/server
smoke test remains required before labeling those flows runtime-verified.

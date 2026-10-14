# Mechanics repair — 2026-10-13

## Darknet tether

The anchor break handler now requires the Darknet dimension before matching
the bound coordinates. Eleven mocked runtime scenarios pass, including breaks
at matching coordinates in another dimension, power loss, grace periods,
expired timers, recall, and death in the Darknet. See `DARKNET_ANCHOR.md`.

## Lyran End route

The live structure objective and its existing Bastion map reward already target
Lyran Research in the Nether. Added the missing dimension override to the shared
map helper so audits and future map generation agree with that live route.
Updated the expansion generator's retired stronghold objective and End briefing
to Lyran, and corrected its moved map-helper import. Updated live quest prose
to explain the facility and Gate rather than the retired stronghold.
All existing quest, task, dependency, and reward IDs are preserved.

`node dev/scripts/test_lyran_map_handoff.js` passes. It verifies the live route,
Nether map command and reward ID, End dependency, generator target/helper,
preservation of existing rewards, and idempotent map insertion in an isolated
fixture. The full chapter map enforcer requires no additional rewards.

## Quest audit and voice

The general quest audit now recognizes chapter icons stored as item compounds,
the format required by FTB Quests. The dedicated icon audit reports 45 valid
chapter icons and 408 explicit quest icons with zero invalid-icon findings;
33 KubeJS icons remain statically unverified. Missing explicit quest icons are
a separate signposting queue.

Corrected four third-person Charles references in live Old World localization
and its owning narrative generator to match the direct field-terminal voice.

## Remaining work

The structural audit with automatic icons allowed still fails on the missing
title for optional Era 4 quest `72F9F10C569BD362` and the rewarded cottage-build
checkmark `5D10000000000004`. The latter was deliberately retained in
`2026-09-07-quest-reconciliation-run-28.md` pending a reliable commissioning hook;
it needs reconciliation with the stricter reward rule rather than an unexamined
exception. Strict icon mode also reports missing explicit icons.

Minecraft verification of map delivery/search, Lyran discovery, End portal
activation, and actual KubeJS/AE2 tether events remains pending. The full
expansion generator was not run against the live pack because it rewrites
unrelated chapters and world-generation settings.

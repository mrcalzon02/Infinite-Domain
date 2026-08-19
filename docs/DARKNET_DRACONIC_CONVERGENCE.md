# Darknet Draconic Convergence

Date: 2026-08-14

Cyberspace modpack usage and quest-graphic permission is retained under
`docs/permissions/`; this custom integration remains pack-side and does not
alter the upstream project's general license.

The generated campaign adds the full Mekanite Mobs roster to both
`cyberspace:cyberspace_biome` and `cyberspace:darknet_biome` using the roster's
native weights and group sizes. Fire, Ice, and Lightning Dragons are added only
to the Darknet at weight 1, group size 1, so they remain rare apex encounters.

The quest chapter follows Cyberware Ascension's **First Connection to
Cyberspace** quest. It documents the installed Cyberspace 4.1.1 behavior:

- put a Netcracker in the Terminal hardware slot to expose the Darknet link;
- the connection transfer takes 40 ticks (two seconds);
- the first landing uses random Darknet coordinates and subsequent connections
  remember the player's last Darknet position;
- the Darknet session lasts 100 seconds, then returns the player to the recorded
  Overworld connection coordinates;
- descending below Y 48 applies Darkness, while Darknet movement logic clears
  fall distance.

After the access and extraction chain, Fire, Ice, and Lightning each receive
four linked quests: combat, specimen collection, Dragonforge construction, and
Dragonsteel production. Those branches converge on egg recovery, elemental
incubation, husbandry tools, Stage 3 riding, dragon armor, and a final
automatically verified block of each Dragonsteel type.

## Eight-tier Darknet Session Injector

The technology branch introduces a Darknet Temporal Core followed by eight
consumable Session Injector tiers. A successful right-click during an active
Darknet connection modifies Cyberspace 4.1.1's actual synchronized player timer,
consumes the injector, and grants the field-test advancement. Injectors do
nothing outside the Darknet or when no carrier timer is active. Rejected use
does not consume the injector. Charles selects from separate eight-line response
pools for the wrong dimension and an inactive session; wrong-dimension responses
identify whether the player is in the Overworld, Nether, End, Cyberspace, or a
different modded dimension before explaining that the injector requires the
Darknet. The complete response remains in chat, while its mechanical warning
and immediate remedy remain as a title and subtitle for 75 seconds.

The tiers double exactly:

| Tier | Added time |
| ---: | ---: |
| I | 30 seconds |
| II | 60 seconds |
| III | 120 seconds |
| IV | 240 seconds |
| V | 480 seconds |
| VI | 960 seconds |
| VII | 1,920 seconds |
| VIII | 3,840 seconds (64 minutes) |

The Temporal Core and every injector tier are deliberately achievable in the
Overworld before the first Darknet expedition. The core uses an Energy Cell,
Fiber Optics, Graphene-Coated Iron, a Logic Processor, a Quantum Core, and a
Virtual Machine Core. Tier I combines that core with Fluix Crystals, a Logic
Processor, Graphene-Coated Iron, and Energy Cells, producing four injectors.

Each later tier consumes exactly one injector from the previous tier, four
Graphene-Coated Iron Ingots, and two matching Applied Energistics components.
The progression is Logic Processor, 1k Storage Component, Calculation
Processor, 4k Storage Component, Engineering Processor, 16k Storage Component,
and 64k Storage Component. It contains no Darknet drops, Nether or End materials,
dragon products, or circular requirements.

The egg quest uses Ice and Fire's own `dragon_egg` advancement. Hatching and
Stage 3 riding use manual confirmations alongside substantial item objectives,
because the installed mod exposes no species-aware tame or ride advancement for
FTB Quests to observe directly. Those confirmations have substantial item tasks
and no reward; the rewarded finale is verified entirely through produced items.

Generation is deterministic through
`scripts/build_cyberspace_darknet_campaign.py`; validate it with
`scripts/audit_cyberspace_darknet_campaign.py` and the global FTB quest audit.

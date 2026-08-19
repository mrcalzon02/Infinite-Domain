# Critical Progression Bypass Hotspots

This is the first design-facing triage pass over the static graph and exposed economy configuration. It does not remove routes yet; it identifies the routes that conflict most directly with the intended era and quest structure.

## Priority 0 — Cyberware bartering

`createcybernetics:gameplay/hogboy_bartering` can yield 159 distinct Create Cybernetics items. The pool includes finished implants, base limbs, advanced upgrades, scavenged implants, crafting components, and upgrade templates.

This directly conflicts with making cyberware a coveted quest-progression reward. A repeatable barter source can skip both the quest ladder and the industrial production ladder.

Recommended policy: override this loot table before Era 0 balancing. Limit it to low-grade scavenged components, medical consumables, or quest turn-in scraps; do not leave finished implants in the general barter pool.

## Resolved Priority 0 — Open commodity market

The original Delivery Required market sold progression-sensitive vanilla resources at fixed prices, including diamonds, emeralds, netherite scrap, netherite ingots, echo shards, and nether stars. Market purchases used a 3x price multiplier, but availability itself bypassed exploration, boss, and extraction gates once players could earn currency reliably.

Implemented policy: the Market now has a 17-item mundane import allowlist and a 256-item purchase cap. Dimension, boss, enchanting, mechanism, cyberware, potion, and milestone resources are absent. The Contractor uses a separate 32-item export allowlist, excludes every Echo-sold item, and generates approximately 64 Spurs of demand per job rather than one million. See `docs/DELIVERY_REQUIRED_ECONOMY.md`.

## Priority 1 — AE2 material loot

AE2 Lightning Tech starship loot supplies certus quartz, charged certus, fluix crystal/dust, silicon, sky dust, and sky stone. Firmament starships also supply overload alloy/crystal and AE2 tools. Vanilla AE2 researcher gifts provide certus, fluix, and sky stone.

These routes do not currently hand out storage cells, drives, terminals, or controllers, so they do not invalidate the planned Heavy Industry payoff by themselves. They can, however, let exploration pre-stock most early AE2 materials before the quest unlock.

Recommended policy: preserve a small amount as exciting foreshadowing, but gate actual AE2 machines and cells through quests. Review the starship structure's accessibility and quantities after Era 0/1 costs exist.

## Priority 1 — Space progression loot

Stellaris structures distribute steel, space-suit pieces, rocket upgrades, and planetary materials through many chests. This is appropriate after orbital access, but any Earth-accessible operation base, satellite, meteor, or structure can leak space-tier equipment into earlier eras.

Recommended policy: classify every Earth-accessible Stellaris structure by intended era and remove or substitute finished space equipment from pre-orbital loot.

## Priority 1 — Automated resource sources

Oritech deep-drill loot tables and the deliberately sparse ReAutomated Ore Nodes remain independent acquisition routes alongside ordinary ores and processing chains. They are not automatically bypasses; they become bypasses if their machine construction or operating inputs unlock earlier than the resource they produce.

Recommended policy: assign each extractor an era and energy/infrastructure prerequisite before recipe edits. The graph can then flag any output whose source era precedes its intended material era.

## Required classification pass

The graph contains 4,237 broad multi-route candidates. Many are harmless block self-drops or alternate processing recipes. To determine every *real* bypass, add three fields to important resource and route nodes:

- earliest intended era;
- earliest actual availability;
- renewable cost or limiting dependency.

A route is a real bypass when actual availability precedes intended availability, or when its repeatable cost trivializes the milestone it replaces. Era 0 and Era 1 recipe design should begin only after the Priority 0 routes above are constrained and this metadata pass covers their milestone resources.

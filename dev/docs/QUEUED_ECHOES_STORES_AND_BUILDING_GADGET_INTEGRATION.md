# Queued Echoes Stores and Building Gadget Integration

Status: implemented 2026-08-14; physical projector coordinates and in-game shop
validation remain after the spawn-hub restoration is complete.

## Confirmed FTB Echoes implementation

The installed mod is `ftb-echoes-21.1.10.jar` on Minecraft 1.21.1. Echoes are
data-pack resources under:

`data/<namespace>/echo_definitions/<echo>.json`

An Echo definition supplies its NPC model, dialogue stages, required progression
stage, and `shop_unlock` entries. A shop entry can contain one item or a bundle,
a Numismatics cost expressed in Spur value, a global or per-player claim limit,
and a maximum stage. Infinite Domain's currency provider connects Echoes to the
physical coin inventory and honors the default 1/8/16/64/512/4096 exchange ladder.
The physical lobby store should therefore be an Echo Projector assigned the same
Echo definition used by its quest-book mirror. The shop inventory must have one
canonical definition; the quest book should advertise and navigate the inventory,
not duplicate its purchasing rewards.

## Storefront plan

Create at least six visually distinct Echo vendors in the protected spawn hub.
Each vendor may contain multiple staged inventory pages, but no page becomes
available before its corresponding era has been completed or entered according
to the final progression policy.

1. **Quartermaster — Lost Survivors (Era 0)**
   - Food, clean water support, torches, basic medicine, primitive tools, string,
     leather, common salvage, and modest building repair supplies.
   - No machinery, rare ore, or item that completes an Era 0 charter.
2. **Mechanist — Mechanical Reconstruction (Era 1)**
   - Create-scale mechanical consumables and basic workshop stock: shafts, belts,
     cogs, andesite-alloy class materials, glue, and modest bulk stone/wood.
   - Brass-era or advanced components remain locked until their real milestone.
3. **Foundry Broker — Heavy Industry (Era 2)**
   - Coke/coal support, steel-class construction stock, refractory materials,
     rails, treated wood, and heavy-industry maintenance consumables.
   - Avoid selling machines or complete Foundation components.
4. **Fuel and Chemical Cooperative — Petrochemical Civilization (Era 3)**
   - Containers, seals, rubber/plastic intermediates, sulfur-class consumables,
     refinery support materials, and emergency fuel in controlled quantities.
   - Petroleum outputs must be priced around the deliberately remote oil economy,
     not become a substitute for exploration and refining.
5. **Grid Supply — The Electrical Grid (Era 4)**
   - Wire, connectors, insulation, lamps, redstone-control stock, batteries or
     other modest grid-maintenance goods appropriate to Era 4.
   - Only the limited AE2 infrastructure already authorized by Era 4 may appear.
6. **Systems Exchange — Automated Industry (Era 5)**
   - AE2 processors/components, automation consumables, logistics parts, Oritech
     support stock, and cybernetic-manufacturing inputs.
   - Do not sell completed automation machines or bypass autocrafting milestones.

Recommended additional late-game vendors, so one NPC does not become an
overloaded catalogue:

7. **Containment Office — High Energy and Nuclear Engineering (Era 6)**
   - Radiation protection, containment/maintenance stock, and tightly limited
     nuclear support materials; never finished fuel-cycle progression items.
8. **Expedition Exchange — Orbital Industry and Infinite Domain (Eras 7–8)**
   - Sealed-habitat consumables, expedition replacements, and orbital construction
     stock. Infinite Domain stock should be convenience material, not mastery.

## Quest-book mirror

Add a dedicated **Spawn Exchange** chapter to the mobile-terminal quest-book
revision. It should contain one storefront node per physical Echo vendor, using
the same era dependency as that vendor's first relevant shop stage. Each node
should include:

- vendor name, hub location, role, and currency explanation;
- an era-labelled inventory summary rather than a checkmark quest;
- links/dependencies to the relevant era introduction and Foundation capstone;
- clear disclosure of per-player/global purchase limits;
- no duplicate item rewards merely for opening the catalogue.

The exact relationship between `required_stage` and FTB Quests completion must be
implemented and tested before launch. If a bridge script is needed, it should
award the Echo stage from the era's actual crafted Foundation Core/capstone, not
from a manual checkbox.

## Economy and balance rules

- Numismatics currency must have documented sources and sinks before prices are final.
- Staple materials are repeatable but priced above normal local production.
- Rare recovery items and emergency progression protection use per-player limits.
- Nothing sold may complete the same milestone that unlocks it.
- Bulk blocks may reduce rebuilding tedium, but must not replace Mining, Farming,
  or Exploration routes.
- Store inventories must be checked against the effective recipe index for hidden
  cross-mod progression bypasses.

## Building Gadget diagnosis

The effective recipe `buildinggadgets2:gadget_building` is currently supplied by:

`kubejs/data/buildinggadgets2/recipe/gadget_building.json`

Its pattern is:

```text
iri
drd
ili
```

with 2x-compressed iron (`i`), diamond block (`d`), redstone block (`r`), and
lapis block (`l`). It has no AE2 component because the automatic material scaler
only promotes ingredients already present in a recipe. Its non-recursive safety
rules intentionally prevent it from inventing cross-mod integration.

This recipe therefore needs a deliberate hand-authored override after the desired
AE2 tier is chosen. The preferred baseline is to make the central control element
an `ae2:engineering_processor`, while retaining the scaled structural materials.
Before implementation, compare the Mining Gadget and Copy-Paste Gadget overrides
so all Building Gadgets follow one coherent AE2/energy progression ladder. After
the manual override is added, mark it as protected from generator replacement and
rebuild the effective recipe index.

## Implementation checklist (when resumed)

1. Finalize six to eight vendor identities and lobby positions.
2. Map every inventory entry to an era and run a progression-bypass audit.
3. Define the Echo JSON files and test data-pack reload validation.
4. Establish the FTB Quests-to-Echo-stage bridge using real capstones.
5. Place/configure Echo Projectors, then capture them in the final spawn structure.
6. Add the Spawn Exchange quest chapter during the Charles/mobile-terminal rewrite.
7. Hand-author and protect the Building Gadget AE2 recipe.
8. Regenerate the effective recipe index and test JEI, purchases, caps, multiplayer
   team behavior, reconnect persistence, and fresh-world structure placement.

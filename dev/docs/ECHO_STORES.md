# Spawn-Hub Echo Stores

Infinite Domain defines nine FTB Echoes vendors under
`kubejs/data/infinite_domain/echo_definitions/`. Their stock is mirrored by the
**Spawn Exchange** FTB Quests chapter without duplicating purchase rewards.

## Era unlocks

The Quartermaster is available to every player on login. Each subsequent vendor
uses an invisible per-player FTB Quests stage reward on the preceding era's real
Foundation capstone. FTB Library stores these as player stages, and FTB Echoes
reads the same stage provider.

| Vendor | Available in |
| --- | --- |
| Quartermaster | Era 0 |
| Mechanist | Era 1 |
| Foundry Broker | Era 2 |
| Chemical Cooperative | Era 3 |
| Grid Supply | Era 4 |
| Systems Exchange | Era 5 |
| Cybernetics Exchange | Era 5 |
| Containment Office | Era 6 |
| Expedition Exchange | Era 7 |

Each Echo gives a one-time Numismatics allocation when its stage is completed.
All prices are stored in Spur value and use Numismatics' default exchange rates:
Spur 1, Bevel 8, Sprocket 16, Cog 64, Crown 512, and Sun 4096. The companion
`infinite-domain-echo-economy-1.0.0.jar` provider spends physical Numismatics
coins from the player's inventory and returns change in the fewest coins.
Routine stock is repeatable; emergency or unusually valuable stock has per-player
claim limits. No shop sells the capstone or charter that unlocks it.

Every vendor carries twelve role-appropriate offers. The catalogue expands from
survival and repair stock through mechanical, foundry, chemical, grid, automation,
containment, and orbital replacement supplies without selling era capstones or
finished progression machines.

## Physical placement

After restoring a lobby stall, run its placement function at the exact block
coordinate where the projector should stand. For example:

```mcfunction
/execute positioned 4 64 -8 run function infinite_domain:admin/place_echo_quartermaster
```

Available function suffixes are:

- `place_echo_quartermaster`
- `place_echo_mechanist`
- `place_echo_foundry_broker`
- `place_echo_chemical_cooperative`
- `place_echo_grid_supply`
- `place_echo_systems_exchange`
- `place_echo_cybernetics_exchange`
- `place_echo_containment_office`
- `place_echo_expedition_exchange`

These functions replace exactly one block with an Echo Projector and assign its
`echo_id`. Choose and record the final nine coordinates before capturing the
completed hospital as the spawn-hub structure.

# Custom Item Texture Audit

Infinite Domain registers 46 `kubejs:` items in
`kubejs/startup_scripts/main.js`. These are contribution charters, Foundation
Cores, mastery emblems, and collection markers. They intentionally reuse
installed Minecraft and mod textures rather than maintaining duplicate artwork.

## Resolved defects

The 2026-08-14 registry-to-archive audit found 12 affected custom items using 11
missing resource paths. One invalid Mechanical Harvester texture was shared by
two items. The failures were aliases for block items, an animated compass, armor,
or models whose PNGs do not live at the conventional `textures/item/<id>.png`
location.

All aliases now point to PNG resources verified inside the installed Minecraft
1.21.1 client or mod JARs. Current result:

- Registered custom items: 46
- Texture assignments: 46
- Unique referenced PNGs: 35
- Missing texture references: 0
- Custom items affected by missing textures: 0

Run the repeatable check from the instance root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\audit_custom_item_textures.ps1
```

Because these are startup-registered items, restart Minecraft after changing
their texture aliases. A resource reload alone is not the authoritative test for
startup registry changes.

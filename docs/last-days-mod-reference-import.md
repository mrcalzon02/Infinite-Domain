# LAST DAYS installed-mod reference import

Mode: Applied

This baseline copies original texture files from the installed mods into the editable resource pack at their exact `assets/<namespace>/textures/...` paths. Existing pack files always win and are never overwritten.

Compatibility-mod logos, mod-name artwork, and pack icons are intentionally excluded from the editable texture workspace. The authoritative exclusion list is `ROOT_tools/last_days_mod_branding_exclusions.txt`; gameplay assets whose names merely contain “pack” are not excluded.

- Installed mod JARs scanned: 187
- JARs containing texture files: 130
- JARs with no texture files: 57
- Unique texture/support paths discovered: 22209
- Existing pack files preserved: 871
- Missing files imported: 21330
- Conflicting duplicate paths resolved: 0
- Identical duplicate paths collapsed: 1
- Animation metadata skipped to protect an existing custom PNG: 8

Duplicate paths prefer the JAR that declares ownership of the texture namespace. If no candidate declares ownership, selection is deterministic by JAR and entry name and remains visible in the collision ledger.

Working ledgers:

- `last-days-mod-reference-assets.csv`: one row per unique texture or support file, including hashes and source selection.
- `last-days-mod-reference-collisions.csv`: every duplicate candidate and the selected winner.
- `last-days-mod-reference-jar-coverage.csv`: coverage accounting for every installed mod JAR, including jars with no texture files.

## Final validation

- All discovered mod PNG paths covered: 20,536 / 20,536
- In-scope conversion paths covered: 19,106 / 19,106
- Preserved Cyberworld/darknet paths covered: 1,430 / 1,430
- Editable pack files: 28,592
- Editable pack PNG files: 24,989
- Asset namespaces in the finished pack: 143
- Distribution ZIP entries: 28,592
- Duplicate ZIP paths: 0
- Source files missing from ZIP: 0
- Pre-existing assets changed by import: 0
- Invalid PNG signatures: 0
- Distribution ZIP size: 151,465,107 bytes
- Distribution ZIP SHA-256: `52994182F37529E9F2F6AB0AE2F0543252BB9A1D68D334AD56CB13D58E20A7D7`

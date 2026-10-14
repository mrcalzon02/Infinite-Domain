# Boot data compatibility

Project-owned NeoForge 1.21.1 module. Build and verify from the instance root:

```
python dev/scripts/build_boot_data_compat.py
python dev/scripts/audit_boot_tag_compat.py
```

The build installs `mods/infinite-domain-boot-data-compat-1.0.0.jar`. Sources,
metadata, tests, and the installed project artifact are retained in Git.
The builder emits reproducible jar entry ordering and timestamps, and the
revision-2 closeout verifies an identical checksum on a second build.

The mixin redirects reader creation only inside `TagLoader.load`. It preserves
the ordinary reader for every owner except `mod/tracks` and `mod/primitivestart`.
Tracks' three known uppercase identifiers become valid lowercase identifiers;
the two unregistered variant blocks are optional, while registered track_mount
remains required. Primitive Start's iron-ore removal tag gains the mandatory
empty values array. Its remove and replace fields remain intact. Existing
valid Primitive Start tags are unchanged.

This is a resource-reading correction, not a replacement tag or global filter:
all other contributions to mineability and Create safe-NBT tags still load.
It does not modify upstream jars, disable logging, or change unrelated recipes.
The required injection fails loudly if a Minecraft update changes the target;
review the module on version updates rather than carrying it forward silently.

`audit_boot_tag_compat.py` exercises the transformer from the actual installed
jar against packaged upstream resources, checks repeat application and owner
isolation, and inventories all installed top-level mod contributions to the
four affected tag resources. The inventory is scoped; it is not a dump of the
complete live tag registry or arbitrary per-world datapacks.

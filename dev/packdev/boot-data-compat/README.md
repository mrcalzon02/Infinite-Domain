# Boot data compatibility

Project-owned NeoForge 1.21.1 module. Build and verify from the instance root:

```
python dev/scripts/build_boot_data_compat.py
python dev/scripts/audit_boot_tag_compat.py
```

Pass `--out dev/docs/boot-dimension-audit/revision-3` to the tag audit when
retaining evidence for the current revision without rewriting historical data.

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

The module also supplies the missing Orange Jelly Slime attributes for
Jaffabricate **1.1.3 only**. It reuses the complete vanilla Slime supplier; the
upstream entity's own `setSize` continues to set health to size squared, movement
speed to 0.2 plus 0.1 times size, and attack damage to size. It does not register
a fallback for future Jaffabricate releases or entities already present in the
default supplier table. Review the compatibility hook when updating the mod.

`boot_compat_acceptance.js` exercises real entity construction and size-two
attributes only when the isolated `dimension_audit` plan is enabled. It does
not spawn a mob into normal worlds. Its acceptance marker must be present and
successful before claiming live verification of this repair.

`audit_boot_tag_compat.py` exercises the transformer from the actual installed
jar against packaged upstream resources, checks repeat application and owner
isolation, and inventories all installed top-level mod contributions to the
four affected tag resources. The inventory is scoped; it is not a dump of the
complete live tag registry or arbitrary per-world datapacks.

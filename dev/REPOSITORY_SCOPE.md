# Infinite Domain Repository Scope

This repository preserves Infinite Domain's project-owned implementation and pack
configuration without redistributing third-party mod binaries or unapproved source
payloads.

Tracked release-relevant content includes:

- project-built `infinite-domain-*` mod artifacts and their source projects;
- KubeJS scripts, assets, recipes, tags, loot, structures, and worldgen data;
- datapacks, default configurations, active pack configuration, and quest data;
- custom structure authoring data, validation scripts, and project documentation;
- CurseForge instance metadata used to reconstruct the third-party dependency set.

Intentionally excluded content includes:

- third-party mod JARs;
- third-party/base resource-pack ZIPs;
- the combined resource-pack working tree pending file-by-file license clearance;
- local worlds, backups, logs, crash reports, caches, downloads, and player identity;
- compiled dependency caches and generated build directories;
- upstream donor/reference payloads not required in the distributable project source;
- implementation state, tooling state, issue state, release state, or deliverables belonging to any other repository.

Only changes and evidence committed to this repository on the authoritative branch count as Infinite Domain repository state. External repository work must remain external unless a required Infinite Domain-side artifact is deliberately imported and committed here.

Third-party mods must be reacquired from their original distribution channels using
the CurseForge instance metadata. The local resource-pack working tree remains the
authoritative source until a separately reviewed, redistribution-cleared subset can
be published.

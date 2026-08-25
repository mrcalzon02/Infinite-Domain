# Infinite Domain

Infinite Domain is an open-source Minecraft modpack/project built around a harsh, post-apocalyptic progression experience and a heavily customized Minecraft 1.21.1 / NeoForge content stack.

## Our LAST DAYS Megapack

The repository now contains the active editable **LAST DAYS: Infinite Domain** resource-pack source at:

[`resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/`](resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/)

This is the Infinite Domain continuation and compatibility layer for the LAST DAYS visual language. It is not merely a reference to an external pack: the resource-pack structure, metadata, assets, documentation, pack icon, credits, and compatibility namespaces are present directly in the repository on `main`.

### Current pack identity

- **Target:** Minecraft 1.21.1 / NeoForge
- **Resource-pack format:** 34
- **Pack description:** `LAST DAYS: Infinite Domain — 32x post-apocalyptic total-conversion foundation for Minecraft 1.21.1`
- **Localized pack name:** `LAST DAYS mega pack`
- **Working source:** `resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/`
- **Build/distribution name:** `LAST_DAYS_INFINITE_DOMAIN_1.21.1`

The editable megapack is intentionally additive and non-destructive. It preserves the original namespace and asset path expected by Minecraft and each installed mod, retains upstream material rather than rewriting the upstream archive in place, and layers Infinite Domain compatibility and authored replacement art on top.

### Coverage status

The current porting ledger records:

- all **3,070 Minecraft 1.21.1 vanilla texture paths** present;
- all current pack model and blockstate texture references resolving;
- **138 legacy textures** migrated to current paths;
- **265 modern GUI sprites** reconstructed through exact coordinate mapping from legacy LAST DAYS GUI sheets;
- **29 malformed legacy PNG containers** recovered losslessly;
- all **132 actual animations** passing frame-size, frame-index, and timing validation;
- exact namespace/path entries for all **19,106 in-scope installed-mod PNG paths**;
- a complete installed-mod reference layer spanning **143 namespaces**;
- **24,989 PNG files** in the editable pack after the current compatibility/reference import.

Coverage does **not** mean every texture is finished LAST DAYS artwork. Original vanilla or mod art is deliberately retained as a structural/reference placeholder wherever a proper themed conversion has not yet been authored. The current ledger still identifies **556 vanilla placeholders** requiring conversion or review. This distinction is part of the validation standard: placeholder coverage is not counted as completed art.

### Authored compatibility work

The earlier low-fidelity Create palette/noise placeholder pass was rejected and restored from the installed Create assets rather than being accepted as finished compatibility art. Current Create work instead requires authored structural pixel changes, source/model awareness, native-path validation, reduction review, and direct original-versus-final inspection.

Completed or substantially completed authored Create families currently include the **Mechanical Press, Mechanical Mixer, Mechanical Saw, Basin, Crushing Wheels, Encased Fan, Deployer, Mechanical Crafter, shared Brass foundation, and Millstone**. The **Cogwheel family** is in active conversion. Complex new Create assets now use a resolution-adaptive workflow with **64px as the working minimum where native resolution cannot preserve the required information**, with higher resolutions permitted when necessary; earlier 16px/32px authored families remain valid work but are queued for fidelity review where appropriate.

For the detailed source-layer rules, provenance, validation status, current conversion ledger, and next-pass priorities, see [`PORTING.md`](resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/PORTING.md). Historical LAST DAYS credits and upstream information remain in the pack-local [`README.md`](resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/README.md) and [`credits.txt`](resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/credits.txt).

## License — MIT

**If anything in this repository that I created is useful to you, take it and use it.**

The original code, configuration, documentation, tools, data files, and other project material authored for Infinite Domain are released under the [MIT License](LICENSE). You may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, including republishing or incorporating the material into your own projects, provided the MIT copyright and permission notice are retained.

No permission request is required. Commercial and non-commercial use are both permitted. Attribution beyond retaining the MIT notice is not required.

### Third-party material

This repository may include or reference Minecraft, mods, libraries, textures, sounds, models, code, or other third-party material. The MIT License applies only to material for which this repository's authors have the legal right to grant that license.

Any third-party code, assets, libraries, documentation, or other material that is present in this repository—whether intentionally included, incorporated as a dependency, or accidentally included—remains the property of its original author, creator, copyright holder, or other applicable rights holder. Inclusion in this repository does **not** transfer ownership, waive existing rights, or relicense that third-party material under the Infinite Domain MIT License unless the applicable rights holder has separately authorized that licensing.

Third-party material remains subject to its original license, copyright, attribution requirements, and other applicable terms. If third-party material has been included in error, that inclusion should not be interpreted as a claim of ownership by the Infinite Domain project or its contributors.

See [`LICENSE`](LICENSE) for the full legal text governing original Infinite Domain material.

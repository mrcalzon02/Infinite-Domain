# Our LAST DAYS Megapack — Infinite Domain

This directory contains the active editable **LAST DAYS: Infinite Domain** resource pack for Minecraft **1.21.1 / NeoForge**. It continues the LAST DAYS visual language while adding the compatibility coverage and authored replacement work required by the Infinite Domain modpack.

## CurseForge project history

**Our Last Days MegaPack** is the long-running CurseForge resource-pack project published by **Mrcalzon02** under CurseForge project ID **253075**:

https://www.curseforge.com/minecraft/texture-packs/our-last-days-megapack

The CurseForge listing records support/releases across Minecraft **1.7.10, 1.11, 1.11.1, 1.11.2, and 1.20.1**. Its historical release/update notes are retained here so the current Infinite Domain continuation has an explicit lineage back to the public MegaPack releases.

### CurseForge-listed changelog

- **November 1, 2016 — Our Last Days Mega pack Day-1 / Minecraft 1.7.10:** Initial Day-1 public MegaPack release.
- **February 5, 2017:** Added custom sounds and music and continued the early update pass around the LAST DAYS base pack and modded-use environment.
- **February 6, 2017 — Last_Days1.01.zip / Minecraft 1.7.10:** Follow-up 1.7.10 release published.
- **February 12, 2017 — Last_Days_1.11R1:** First listed 1.11-generation release line.
- **February 22, 2017 — Our Last Days 1.11 R2 / Minecraft 1.11.2:** Development focus moved to Minecraft 1.11 and later. This update expanded planned mod support, realigned several container GUI textures, repaired zombie-villager and zombie textures, adjusted Guardian/Elder Guardian textures, added Prismarine variants and Magma, retextured the wooden trapdoor, restored/modified assorted animated blocks, and re-enabled the US English language file.
- **March 21, 2024 — LAST_DAYS_1_20_1.zip / Minecraft 1.20.1:** Latest public CurseForge release. Its file-level changelog is listed as **“Changes updates and tweaks.”** This 1.20.1 archive is the untouched upstream source retained for the current Infinite Domain porting effort.

The CurseForge project predates the current Minecraft 1.21.1 / NeoForge conversion work in this repository. The entries above describe the **published Our Last Days MegaPack history**; the sections below describe the newer Infinite Domain compatibility and authored-art work that has not yet been represented by those older CurseForge release notes.

## Current pack identity

- **Target:** Minecraft 1.21.1 / NeoForge
- **Resource-pack format:** 34
- **Pack description:** `LAST DAYS: Infinite Domain — 32x post-apocalyptic total-conversion foundation for Minecraft 1.21.1`
- **Localized pack name:** `LAST DAYS mega pack`
- **Working source:** `resourcepacks/LAST_DAYS_INFINITE_DOMAIN_1_21_1/`
- **Build/distribution name:** `LAST_DAYS_INFINITE_DOMAIN_1.21.1`

The editable megapack is intentionally additive and non-destructive. It preserves the original namespace and asset path expected by Minecraft and each installed mod, retains upstream material rather than rewriting the upstream archive in place, and layers Infinite Domain compatibility and authored replacement art on top.

## Coverage status

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

## Authored compatibility work

The earlier low-fidelity Create palette/noise placeholder pass was rejected and restored from the installed Create assets rather than being accepted as finished compatibility art. Current Create work instead requires authored structural pixel changes, source/model awareness, native-path validation, reduction review, and direct original-versus-final inspection.

Completed or substantially completed authored Create families currently include the **Mechanical Press, Mechanical Mixer, Mechanical Saw, Basin, Crushing Wheels, Encased Fan, Deployer, Mechanical Crafter, shared Brass foundation, and Millstone**. The **Cogwheel family** is in active conversion. Complex new Create assets now use a resolution-adaptive workflow with **64px as the working minimum where native resolution cannot preserve the required information**, with higher resolutions permitted when necessary; earlier 16px/32px authored families remain valid work but are queued for fidelity review where appropriate.

For the detailed source-layer rules, provenance, validation status, current conversion ledger, and next-pass priorities, see [`PORTING.md`](PORTING.md). Historical LAST DAYS credits and upstream attribution remain below and in [`credits.txt`](credits.txt).

---

## Upstream LAST DAYS history and links

**LAST DAYS** was a texture pack started by **[doku](http://www.minecraftforum.net/user/14329-)** (creator of the ever-popular [RPG pack](http://www.minecraftforum.net/topic/513093-)). Doku began this pack with the essential landscape-defining textures (Dirt, Grass, Stone, water, trees, etc.) but did not have time to do much more before discontinuing the pack. The concept he had, and the work he finished, was too good to let die. Using Doku's visual and conceptual foundation, **[History](http://www.minecraftforum.net/user/53403-)** continued the pack, expanded it, and improved it. After History's disappearance, the pack was continued and further improved by **[Croco15](http://www.minecraftforum.net/user/158674-)** and **[HalphPrice](http://www.minecraftforum.net/user/249941-)**. Finally, **[dereksmith](http://www.minecraftforum.net/user/98378-)** chose to keep LAST DAYS updated with the help of the community and continue to improve it, as the other texture-pack owners had before. **[Gwolfski](https://www.minecraftforum.net/members/Gwilk)** later joined the team after a period of inactivity.

This MegaPack is a continuation with additional mod support.

### Threads

- ~~The [Original Thread](http://www.minecraftforum.net/topic/30422-) by [doku](http://www.minecraftforum.net/user/14329-)~~
- ~~The [Second Thread](http://www.minecraftforum.net/topic/126176-) by [History](http://www.minecraftforum.net/user/53403-)~~
- ~~The [Third Thread](http://www.minecraftforum.net/topic/369814-) by [Croco15](http://www.minecraftforum.net/user/158674-)~~
- The [Fourth (current) Thread](http://www.minecraftforum.net/topic/1059319-) by [dereksmith](http://www.minecraftforum.net/user/98378-) (not really active)

### Discord

- Join the LAST DAYS Discord: https://discord.gg/QDXhjWx

### Downloads and references

- ~~[Home Page for Downloads and Info](https://krulunio.github.io/last_days/)~~
- https://www.curseforge.com/minecraft/texture-packs/last-days
- https://resourcepack.net/last-days-resource-pack/
- Latest upstream dev build: use the green **Code** button on the upstream repository, download the ZIP, and extract it into the Minecraft resource-pack directory.

# 08 — Administrator Recovery and Multiplayer Safety

## Problem

A multiplayer server can create edge cases that do not exist in a solo fresh world:

- another player loots a unique proof item first;
- the quest was added after surrounding chunks were already generated;
- a worldgen bug prevented the target from spawning;
- a structure generated but was destroyed or heavily modified;
- a map points to a location whose required chest was already opened;
- a server updates the pack between narrative revisions.

The canon source specifically anticipates the need for recovery while rejecting the idea of casually exposing world-spawn commands in the public questbook.

## Safety model

Player-facing quest content may provide:

- a new locator/map if safe;
- an alternate search objective if deliberately designed;
- information telling the player to contact an administrator if the site is missing.

Administrator documentation may provide:

- commands to locate the narrative structure ID/tag;
- commands to grant/restore a proof item;
- commands or supported tooling to place/regenerate a specific quest structure when necessary;
- verification commands to inspect quest/advancement state;
- migration steps for already-generated worlds.

Do not place privileged structure-generation commands in clickable public quest text.

## Required admin recovery entries

For every mandatory quest structure, document:

- quest name;
- narrative structure ID/tag;
- locator command/tool supported by the installed pack;
- unique proof item ID;
- safe proof-item restore command/procedure;
- structure placement/regeneration procedure if supported;
- warnings about chunk overwrite or player-build destruction;
- what to do if the exact original structure instance cannot be recovered.

## Preferred recovery order

1. Locate another naturally generated copy if the quest permits it.
2. Restore only the missing proof item if the structure was legitimately explored but loot was lost.
3. Provide a replacement locator/map to an untouched copy.
4. As an administrator-only last resort, place/regenerate the specific narrative structure in a safe, unoccupied region using the actual supported structure command/API.

Never overwrite player builds casually to repair a lore quest.

## Existing-world migration

Where possible, make new narrative structures generate in unexplored chunks after pack update. Do not assume retroactive generation into old chunks.

For unique landmark quests in long-running worlds, provide a documented server-admin migration path rather than pretending an old explored region will magically gain a new structure.

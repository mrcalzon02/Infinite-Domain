# Administrative Spawn Claim

Infinite Domain reserves a radius-three FTB Chunks claim around world coordinate
`0,0` in the Overworld. Radius means three chunks outward from the center chunk,
not a literal 3-by-3 selection.

- Chunk range: X `-3..3`, Z `-3..3`
- Total claimed area: 49 chunks (7 by 7)
- Block footprint: X `-48..63`, Z `-48..63`
- Owning team: the FTB server team `Admin Spawn`

The startup script uses the installed FTB Teams and FTB Chunks APIs to create or
repair the server team and explicitly claim chunk coordinates `-3..3`. The claim
is reasserted on every server load, making it effective for both the existing
test world and newly created worlds without depending on command grammar.

## Permissions

The server team is private for block editing, general block interaction, entity
interaction, and non-living-entity attacks. Explosions, mob griefing, and PvP are
disabled. The global PvP mode is `per_team`, leaving ordinary teams at their
default while honoring the Spawn team's PvP prohibition. Players can spawn, walk through the structure, read the rules, use
quests, and leave through any exit, but cannot modify the hub.

The pack extends `ftbchunks:interact_whitelist` with the five Numismatics shop and
bank blocks. These remain usable by visitors even though general block
interaction is private. FTB Chunks already whitelists Create table-cloth shops.

Admins can toggle protection bypass while standing in the claim:

```text
/ftbchunks admin bypass_protection
```

Verify the center and corners after loading the world:

```text
/ftbchunks info 0 0 minecraft:overworld
/ftbchunks info -3 -3 minecraft:overworld
/ftbchunks info 3 3 minecraft:overworld
```

## Spore Hospital spawn shell

The installed Spore Hospital is a single 48 by 48 by 48 structure template. Its
native worldgen projects to the world surface with a start-height offset of `-9`.
The supplied admin function preserves that relationship while centering the
even-width template around the four blocks adjoining `0,0`:

- Template origin: X/Z `-24,-24`
- Template footprint: X/Z `-24..23`
- Exact center: the intersection between the four central blocks containing
  coordinates `(-1,-1)`, `(-1,0)`, `(0,-1)`, and `(0,0)`
- Claim buffer: at least eight blocks on every side

The origin is an ocean basin. The original surface-sampling implementation used
the ocean floor and submerged the first placement. The corrected function uses
the pack's fixed Overworld sea level of Y `63`. After in-world inspection found
the native alignment two blocks too low for this basin, the final placement was
raised to template origin `-24 56 -24`. The finished hub's world spawn is
`0 64 0`, one block above sea level in the central parking lot.

Every server load now verifies the lobby using its structure-specific
`spore:lab_block` at world position `20 95 20`. If that signature is absent,
the pack prepares the terrain and places the complete lobby before a player can
connect. Completed lobbies are untouched. The manual recovery function remains
available because deliberate re-placement replaces a 48-cubed region,
including air:

```text
/function infinite_domain:admin/place_spawn_hospital
```

Back up the world before running it. Run it only once; repeating it restores the
original infected hospital template over any cleanup or shop conversion.

## Spawn-point correction

The hospital-placement function now delegates spawn setup to a separate safe
function. The global spawn is `0 64 0`, the random spawn radius is zero, and all
players online when the function runs have stale personal bunker spawnpoints
replaced with the hub position:

```text
/function infinite_domain:admin/set_spawn_hub
```

This function does not place, replace, or remove blocks and is safe to run after
the hospital has been restored. It intentionally affects only players currently
online. Offline players with old personal spawn data should join, then an admin
can run the function again. Beds used afterward work normally; the correction is
not reasserted on every server start.

`scripts/read_level_spawn.py` can inspect either `level.dat` or a player `.dat`
file while the game is closed. Before finalization, the active test save audit
found global spawn at `0 63 0` while the existing player was still assigned to
`2 55 6`; that stale personal point explains why the old bunker remained
authoritative for the character. Run the correction only after the rebuilt hub
has been captured and installed. It moves both spawn targets to `0 64 0`.

An automatic repair records one pending arrival correction. The first player
to connect is moved to the parking lot one tick after login, after starter-world
handlers finish, and receives the corrected personal spawnpoint. This covers
worlds first opened under the former manual-only behavior. Later new players use
the global hub spawn normally.

## Starting documentation

More Ores More Gems 1.1.9 does not expose a working configuration switch for
its starting book. The grant is hardcoded into its first-login advancement
handler, and its displayed recipes conflict with the pack's overrides. Infinite
Domain therefore removes `more_ores_more_gems:book_momg` once, one tick after a
player's first pack login. Charles's FTB Quests guide remains the authoritative
starting book.

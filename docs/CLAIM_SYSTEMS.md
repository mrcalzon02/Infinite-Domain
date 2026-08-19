# Claim and team systems

## Active authority

Infinite Domain uses **FTB Teams + FTB Chunks** for player parties, quest-team
progress, land protection, map waypoints, and chunk force-loading.

- `ftb-teams-neoforge-2101.1.10.jar` is active.
- `ftb-chunks-neoforge-2101.1.21.jar` is active.
- `create_aeronautics_ftb_chunks-1.21.1-NeoForge-1.1.1.jar` is active and
  explicitly requires both FTB mods. It lets claimed Create Aeronautics
  contraptions consume FTB Chunks force-loading capacity.
- The public Spawn Hub is owned by the FTB server team `spawn` and claimed with
  the FTB Chunks `claim_as` command.

Players should therefore be taught one ordinary claim workflow: open **My
Team** from the inventory sidebar, then use the **FTB Chunks Map/Claim Manager**.

## Disabled remnants

Open Parties and Claims and AeroClaims are present only as disabled archives:

- `open-parties-and-claims-neoforge-1.21.1-0.29.3.jar.disabled`
- `aeroclaims-0.9.3.jar.disabled`

Their TOML files remain under `config/`, but NeoForge does not load either mod.
The OPAC provider selections in `aeroclaims-server.toml` are consequently
inactive and do not create a second live claim ledger.

Older generated reports can still mention `aeroclaims:claim_block` if they were
built before the archive was disabled. Regenerating the effective recipe index
from the current `mods/*.jar` set excludes `.jar.disabled` archives.

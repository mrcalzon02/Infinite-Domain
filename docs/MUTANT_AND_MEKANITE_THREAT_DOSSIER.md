# Mutant and Mekanite Threat Dossier

Date: 2026-08-14

This Persistent Threats chapter deliberately separates two encounter models.

## Mutant Monsters

The four naturally occurring mutant classes can spawn inside the initial world
ring, so their entry quest has no era dependency. Mutant Zombie contact opens
parallel evaluations for Zombies, Skeletons, Creepers, and Endermen. Those
branches converge on a four-class threat determination. Mutant Snow Golem and
Spider Pig trials remain optional follow-up work because they require deliberate
Chemical X conversion rather than ordinary natural contact.

The dossier teaches the important encounter differences: a downed Mutant Zombie
must be burned, Mutant Skeletons require hard cover, Mutant Creepers require a
disposable blast area, and Mutant Endermen invalidate uncontrolled open terrain.

## Mekanite Mobs

Mekanite enemies are treated as Era 8 expedition hazards. Their three geographic
entry routes require the Era 8 opening quest and an appropriate existing
outer-world survey:

- Snowy Taiga for the northern land branch;
- Desert Corridor for the southern land branch;
- Deep Cold Ocean for the aquatic branch.

The tree covers all fifteen independently registered natural Mekanite spawns:
Drone; Zombie; Husk; Drowned; Skeleton; Creeper; Spider; Big, Medium, and Small
Slimes; Witch; Illusioner; Vindicator; Ravager; and Enderman. The Illusioner's
temporary clone is explained in dialogue but is not treated as an independent
population or required kill.

All fifteen variants also use their native weights and group sizes in both the
Cyberspace and Darknet biomes. These are alternate Era 8 encounter spaces gated
by the Cyberspace/Netcracker technology chain; they do not place Mekanites in the
initial ring.

Normal encounters reward modest Cogs or Era 8 Supply Bags. Branch conclusions
and the final extermination doctrine can award an Era 8 Priority Cache. No
Mekanite weapon, armor set, or completed combat item is granted directly.

Generation is deterministic and idempotent through
`scripts/build_mutant_mekanite_threat_quests.py`. Run
`scripts/audit_mutant_mekanite_threats.py` after any roster or dependency edit.

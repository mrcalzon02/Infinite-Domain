# Endgame — placeholder terminology register

**Authority:** `docs/Endgame.md` §10 checkpoint `EG-P00-S02-C0003` (Identity contract).

**Purpose:** every institutional, crew, inhabitant, or place name introduced for the
`infinite_domain:hive_world` dimension before checkpoint `EG-P06-S06-C0093` is a
**placeholder**. This file is the single register of those terms. A placeholder may
appear in prototype data, greybox signage, and internal docs. It may **not** appear
in committed player-facing lang files, quest chapters, books, advancements, signs, or
the resource pack until `EG-P06-S06-C0093` promotes it.

Promotion to canon requires either a new entry in the canon source hierarchy
(`old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md`) or explicit owner
approval recorded in the `C0093` handoff. No placeholder may contradict fixed canon
(EP-7 / PT-9, the Firebreak Wars, the corporate roster VCF / Aevum / PolyCore / Atlas /
Pleroma / Helion / Blackglass / Continuity / Asterion, or Charles's arc).

## Status vocabulary

| Tag | Meaning |
|---|---|
| `PLACEHOLDER` | Provisional. Internal / prototype use only. |
| `WORKING-CANON` | Owner has accepted it as a working assumption but it is not yet written into the canon source. |
| `CANON` | Promoted at `C0093` or entered in the canon bible. Cleared for player-facing text. |

## Register

| Term | Tag | Provisional meaning | Canon anchor |
|---|---|---|---|
| Ordan | `WORKING-CANON` | The dead, airless industrial planet the Old World developed for off-world heavy manufacturing; the body the Cinderstack stands on. | none yet — proposed at C0003 |
| the Cinderstack | `WORKING-CANON` | The dimension: one continuous engineered city-mass from planetary crust to exosphere. "The Stack" colloquially. Player-facing name in advancements, quests, and the return HUD. | none yet — proposed at C0003 |
| tier / deck | `WORKING-CANON` | The vertical layers of the Stack. Replaces the prohibited "spire / hab / underhive". | none yet |
| stacker | `PLACEHOLDER` | Old World work-slang for a Cinderstack labourer. All dead; encountered as remains, automata, and records. | none yet |
| the Lift Authority | `PLACEHOLDER` | The builder / operator institution of the Cinderstack. | proposed hook: an Atlas + Helion venture, Pleroma logistics (C0003 §working canon hook) |
| the Drown | `PLACEHOLDER` | Working name for the flooded bottom band (C0004 band identity). | none yet |
| the Underworks | `PLACEHOLDER` | Working name for the collapsed-habitation band. | none yet |
| the Furnace Tiers | `PLACEHOLDER` | Working name for the heavy-industry band. | none yet |
| the Billet Decks | `PLACEHOLDER` | Working name for the habitation band. | none yet |
| the Vaulting | `PLACEHOLDER` | Working name for the monumental-release band. | none yet |
| the Crown | `PLACEHOLDER` | Working name for the fortified upper band. | none yet |
| Verdant Strain | `PLACEHOLDER` | Prior uncommitted scratch (`docs/hive-strain/`): a Spore-derived biological rot that colonised the warm dark interior after the crew died. Enemy roster is `EG-P06-S04-C0089`; not adopted or blocked here. | descends from EP-7 / PT-9 lineage (compatible with canon) |

## Prohibited source-distinctive terminology and mandatory replacements

The acknowledged inspiration (`docs/Endgame.md` §2.6) is the broad idea of vertically
stratified arcologies in a dead industrial world. The following terminology is
source-distinctive and is **prohibited everywhere in Hive content** — player-facing
strings, committed narrative, registry IDs, and comments a player could later read.

| Prohibited | Reason | Mandatory replacement |
|---|---|---|
| hive city, hive world, hive cluster | Source signature | the Cinderstack; the Stack; stack-mass; industrial massif |
| spire (as an upper-class stratum) | Source social term | the Crown; the headworks; the upper works |
| underhive | Source signature | the Underworks; the low stack; the drownlevels |
| hab, hab-block, hab-slab | Source term | quarters; billet-decks; residential decks |
| manufactorum | Source term | manufactory; the works; production decks |
| sump, sump sea | Source-specific | the acid sink; the Drown; catch-basins |
| ash wastes | Source term | the cinder waste; ashflats; the sulfur flats |
| gang; House (with the six source house names) | Source factions | placeholder crews under this policy |
| Palanite; Enforcers (capitalised as a body) | Source term | placeholder "wardens" under this policy |
| Imperium, Adeptus, aquila, sanctioned, Ecclesiarchy | Source setting | none — do not reference imperial or ecclesiastical framing at all |
| skull-and-eagle iconography, gothic-imperial ornament, gang heraldry | Source visual signature | original industrial-tomb iconography chosen at a later visual checkpoint, building on §2.8 |

Also prohibited: traced, copied, or lightly-reskinned structure geometry, terrain
kits, prose, character names, or unit names from the inspiration's games or art.

## Note on the technical token `hive_world`

`infinite_domain:hive_world` is the permanent engine-facing dimension ID and the
path/registry token for all Hive content. It is a **code token only**. The literal
substring `hive` must never appear in any player-facing string: lang files, item or
block display names, dimension-effect strings shown to players, advancement titles or
descriptions, quest text, book or sign text, or HUD strings.

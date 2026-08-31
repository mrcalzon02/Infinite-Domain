# Endgame — Cinderstack custom-entity master plan

**Authority:** `docs/Endgame.md` §2.1, §2.3, §2.5, §2.7 and Phase 6 checkpoints
`EG-P06-S04-C0089`, `C0090`, `C0093`, and `C0095`.

**Status:** owner-directed master development contract, authored 2026-08-28.
It is the working authority for the Cinderstack enemy program and becomes the formal
`C0089` roster contract when Phase 6 opens. Names marked **WORKING** are design handles,
not approved player-facing text; C0093 owns final names and faction language.

**Inputs:** `docs/registry-inventory/entity-ids.txt`,
`docs/registry-inventory/mod-jar-index.json`, the unadopted
`docs/hive-strain/roster-manifest.json`, `docs/endgame/contracts/hazard-contract.md`,
`docs/endgame/contracts/performance-budget.md`, and the six-band spatial contract.

**Implementation owner:** the dedicated Hive World companion module registers and
runs production entities. Datapack resources own tags, loot, encounter profiles, and
structure-facing data. KubeJS may support disposable prototypes only; it does not own
production AI, encounter persistence, or multiplayer scaling.

---

## 1. Non-negotiable outcome

The Cinderstack is endgame content at **every** elevation. The Drown is not a tutorial
zone, the wastes are not a safe transit plain, and lower altitude does not mean lower
combat tier. A prepared player in proven endgame equipment can survive through skill,
planning, and resource expenditure; an inattentive player in the same equipment can
be killed in any band.

Vertical progression changes the **kind** of pressure:

- lower regions weaponize acid, darkness, confinement, swarms, and ambush;
- middle regions weaponize machinery, crossfire, pursuit, and industrial hazards;
- upper regions weaponize coordination, access control, vertical displacement,
  command units, and precise high-status equipment.

The Crown may be more organized and opulent, but it does not make The Drown's enemies
mere fodder. Every band owns at least one threat that remains relevant to a fully
developed build.

The custom roster is broader than Spore, while the Verdant Strain deliberately uses a
simple **same creatures, same behavior, 3× health** rule. All **77 viable Spore combat creatures** in the generated
roster are in scope; the other 19 `spore:` IDs are their projectiles, detached parts,
thrown objects, or effect helpers and remain active when their owning creatures use
them. Verdant forces participate in ordinary traversal, patrols, territory, assaults,
landmarks, and calamity events at every elevation. They coexist and fight with the
custom families rather than being reduced to a token outbreak subset.

## 2. Design pillars

1. **Endgame floor, not a vertical level curve.** Every standard formation is tuned
   against the accepted C0083 reference kits. Height changes tactics and composition,
   not whether enemies can hurt the player.
2. **Original custom-entity identity, with one explicit Spore exception.** Newly built
   enemies use original registry IDs, names, models, textures, sounds, loot, and lore.
   The full Spore roster remains the original `spore:` entity types with unchanged AI,
   receiving only the approved dimension-scoped Verdant visual treatment and 3× health.
3. **Role before appearance.** Every entity has one primary combat role, a readable
   tell, a counterplay window, a band purpose, and a weighted encounter cost.
4. **Predictable Spore rematch.** The established dimension-only 3× health modifier is
   the accepted Verdant difficulty rule. Spore AI, attacks, evolution, summons, and
   progression remain unchanged and recognizable; the Cinderstack environment and
   encounter placement make the familiar progression harder to survive.
5. **Territorial ecology.** Enemy families own understandable spaces. The player can
   infer likely threats from architecture, damage, sound, residue, and weather.
6. **Fair lethality.** Lethal attacks are telegraphed, avoidable, and recoverable.
   No unavoidable spawn damage, silent one-shots, permanent stun chains, or forced
   deletion of irreplaceable equipment.
7. **Hazards remain independent.** Air PPE, acid protection, radiation shielding,
   shields, and armor never become one universal defence.
8. **Server authority and bounded cost.** AI, damage, spawning, persistence, and loot
   are server-authoritative and dimension-scoped. No enemy may generate unbounded
   pathfinding, entities, projectiles, fluid updates, or block damage.

## 3. Corpus policy: extract capabilities, do not clone creatures

The registry inventory contains raw entity IDs from the installed pack. Counts include
projectiles, multipart helpers, clones, vehicles, and cosmetic/support types, so they
are corpus size—not an adoption count.

| Source corpus | Raw registry presence | Useful donor questions | Production ruling |
|---|---:|---|---|
| Fungal Infection: Spore | 96 IDs: 77 viable creatures + 19 auxiliary entities | complete established infection/evolution/organoid/calamity progression | explicit owner-approved production exception: ship the full raw roster with unchanged behavior, dimension-scoped Verdant textures/overlay, and exactly 3× maximum health |
| Ice and Fire | 76 IDs | flight, burrowing, multipart scale, breath cones, boss navigation | mechanical research only unless a specific creature passes a strict visual/IP/performance audit; fantasy creatures do not ship raw |
| Graveyard | 18 IDs | revenant pursuit, spectral movement, ranged undead, summons | strong proxy pool for dead inhabitants; production visuals and names must be original |
| Mekanite Mobs | 16 IDs | drones, mechanized line units, ranged specialists, heavy frames | primary greybox pool for machine roles; no assumption that neon/vanilla-derived presentation fits final art |
| Stellaris | 16 IDs | off-world locomotion, aerial/ground fauna, projectile patterns | selective mechanical donors; visual and cross-dimension assumptions require audit |
| Mutant Monsters | 14 IDs | heavy impact, breakable phases, oversized melee, death events | miniboss/boss research only; avoid recognizable raw mutants in production |
| FTB Ocean Mobs | 11 IDs | sludge movement, acid-adjacent fauna, tentacle control, abyssal silhouettes | primary acid-sink-fauna proxy pool after land/pathing and acid tests |
| The Wasteland Reworked | 9 IDs | arid scavengers, crawling fauna, surface pursuit | primary waste proxy pool; entities implying ambient radiation require renaming/reframing or rejection because the Hive has no ambient radiation |
| Vanilla and other installed mobs | varied | stable goals, navigation, targeting, equipment, projectiles | preferred code-level primitives; raw vanilla reskins alone are insufficient for production identity |
| Razor Tyrant / other unique bosses | isolated IDs | phase pacing, arena presence, recovery | benchmark/proxy only; never adopted as the Cinderstack capstone identity |

### 3.1 Donor audit record

Every considered raw entity receives one row in
`docs/endgame/entity-corpus-audit.json` before code adoption:

```text
source_id
source_mod_and_version
registry_kind                 # mob / projectile / helper / vehicle / other
candidate_role
observed_ai_and_goals
navigation_type
hitbox_and_eye_height
base_attributes
attack_and_projectile_profile
summons_or_child_entities
block_or_fluid_interaction
acid_atmosphere_and_radiation_behavior
despawn_and_persistence
sound_and_visual_fit
server_tick_and_path_cost
client_render_cost
licence_and_asset_reuse_ruling
adopt_research_reject
evidence_paths
```

No entity advances on an ID/name-based assumption. “Looks suitable” without a live
behaviour and cost capture is `runtime-unverified`.

### 3.2 Permitted reuse levels

| Level | Permitted use | Shipping status |
|---|---|---|
| 0 — reference | inspect registry, configuration, animation timing, combat role, and live behaviour | always allowed as research |
| 1 — greybox proxy | summon an installed non-Spore entity in a disposable QA encounter with controlled equipment/attributes | test-only; never final identity |
| 2 — mechanic adaptation | implement an original goal/ability from the observed combat problem using pack-owned code | preferred production path; do not copy third-party source or assets without an explicit licence ruling |
| 3 — supported composition | interact with an installed entity through public APIs/tags when the dependency and absence behaviour are accepted | allowed only after a compatibility checkpoint |
| approved Spore exception | use the installed `spore:` creatures directly with the deterministic Verdant recolor/emissive overlay and dimension-only 3× health modifier; do not change their AI/progression | production-approved by owner direction; asset delivery still follows the Verdant source contract |
| prohibited | recolor or rename any other third-party mob and present it as a new original enemy; subclass private/internal mod implementation as a permanent foundation; redistribute assets without permission | never ships |

## 4. Threat families and territorial logic

All family names in this section are **WORKING**.

### 4.1 The Continuance — machine custodians

The surviving administrative/industrial defence network is the signature threat.
Corroded maintenance frames occupy the lower works; specialized industrial units own
the Furnace; disciplined security formations occupy the Billet Decks and Vaulting;
pristine, ornamented command frames defend the Crown.

This family makes rising wealth visible through enemies: cleaner silhouettes, higher
quality materials, quieter motion, better formation discipline, narrower telegraphs,
and more capable support systems—not merely larger health bars.

Mechanical donors: Mekanite drone/spider/skeleton/vindicator/illusioner/ravager roles,
vanilla ranged/melee/raid goals, selected Stellaris projectile patterns.

### 4.2 Ashbound — living remnant crews

Salvagers, descendants, trespassers, failed expeditions, and institutional holdouts.
They use cover, doors, alarms, improvised firearms/tools, filters, and retreat routes.
Not every Ashbound group is hostile: C0093 must reserve neutral, negotiable, and
conditionally hostile states so the dimension is not a universal kill field.

Mechanical donors: pillager/vindicator equipment logic, Graveyard corrupted-humanoid
proxies, vanilla team/target/restriction systems.

### 4.3 Sinkborn — caustic fauna

Predators and scavengers adapted to acid margins, darkness, flooded foundations, and
fume zones. They use concealment and forced movement rather than armor. Acid adaptation
is role-specific: a true acid swimmer may be immune; a ledge predator may only resist
splash; neither receives unrelated fire/radiation immunity.

Mechanical donors: FTB Ocean sludge, sludgeling, corrosive and tentacled roles; selected
Wasteland crawler/scavenger movement; selected burrow research from Ice and Fire.

### 4.4 The Procession — dead institutional remnants

Workers, overseers, guards, and officials persist as revenant echoes tied to locations
and routines. They supply horror and history without fungalizing every corpse. Their
equipment, posture, and tactics preserve class distinction: crushed labour masses low,
formal sentinels and command echoes high.

Mechanical donors: Graveyard ghoul, ghouling, wraith, reaper, revenant, and corrupted
humanoid roles. Production models and effects must follow Cinderstack art direction.

### 4.5 Verdant Strain — full active biological threat

The complete generated roster is adopted in scope: 12 infected, 32 evolved, 12
hyper-evolved, 10 organoid, 10 calamity, and one hivemind creature (`77` total).
All receive the established green dimension variant and fixed 3× maximum-health
modifier inside `infinite_domain:hive_world`. The 19 excluded registry IDs are not
missing enemies; they are projectiles, detached body parts, thrown objects, or pure
effect entities used by the viable creatures.

Verdant forces are present in every band and in the wastes through ordinary territory,
patrol, authored encounter, roaming assault, nest/organ site, and calamity channels.
Not every species appears at every elevation: profiles follow locomotion, room scale,
hazard compatibility, and encounter role. Every one of the 77 viable creatures must,
however, resolve to at least one production profile and be observed in the retained
seed/encounter test corpus.

Verdant territory is visibly marked and collides with every other family. Three-sided
fights are a core feature: machines purge growth, fauna hunts it, and remnant crews may
weaponize, contain, or flee it. World-altering infection, unbounded child spawning,
calamity chunk loading, and permanent structure conversion remain suppressed or
companion-bounded so the active threat cannot destroy authored architecture or the
server budget.

The 3× modifier is the complete Spore stat/behavior adaptation. No species receives
new AI, attacks, timing, resistances, target selection, or role rewrites from this
program. Encounter data still assigns spawn eligibility and population cost so the
full roster remains active without exceeding entity/performance budgets. Existing
Spore evolution and behavior remain the player's predictable progression vocabulary.

## 5. Production roster blueprint

This is the target minimum viable roster: **20 regular/elite entities plus three major
encounters**. Technical IDs are stable proposals; display names remain working text.

| Technical ID suffix | Family | Role | Primary pressure | Donor research | Principal counterplay |
|---|---|---|---|---|---|
| `ash_skitterer` | Sinkborn | light flanker | fast lateral attacks in fog and rubble | Wasteland crawler; Spore scamper; spider navigation | sound tell, low poise, vulnerable during leap recovery |
| `caustic_grazer` | Sinkborn | line tank | body-blocks ledges and leaves short acid residue | abyssal sludge; mossback/heavy fauna | flank slow turn, break exposed sacs, avoid residue |
| `sink_lurker` | Sinkborn | controller | tongue/tentacle pull toward acid or drop edges | tentacled horror; fishing/guardian projectile concepts | sever/interrupt wind-up, anchor behind cover |
| `gloom_wing` | Sinkborn | aerial spotter | marks player and wakes nearby territory | abyssal winged; drone; gargoyle flight research | break line of sight or kill fragile spotter first |
| `ash_scavenger` | Ashbound | skirmisher | cover-to-cover ranged harassment | pillager/corrupted pillager | push during reload, flank cover |
| `bulkhead_breacher` | Ashbound | assault | shield advance and door pressure | vindicator/heavy humanoid | rear arc, stamina break, electrical stagger |
| `fume_chemist` | Ashbound | area denial | bounded smoke/acid ampoules split formations | witch/chemist projectile patterns | shoot carried charge, relocate before cloud blooms |
| `route_hunter` | Ashbound | tracker | follows recent player route and attacks retreat | hound/stalker pursuit research | decoy/noise, sealed airlock, kill tracker before extraction |
| `survey_drone` | Continuance | spotter/support | alarm, marking, light suppression | Mekanite drone | fragile; break line of sight or disable before alarm completes |
| `cinder_hound` | Continuance | pursuit | sustained chase and dodge punishment | Mekanite spider; hound goals | timed heavy stagger, obstacles, EMP |
| `furnace_suppressor` | Continuance | ranged line | controlled bursts deny long corridors | skeleton/drone ranged goals | telegraphed heat cycle, lateral cover movement |
| `slag_bulwark` | Continuance | tank | directional shield protects formation | ravager/heavy-frame research | rear vents, shield overload, separated support |
| `repair_cantor` | Continuance | support | repairs armor/disabled units, not raw resurrection spam | healer/summoner goal research | visible channel; priority target; long cooldown |
| `null_bailiff` | Continuance | controller | locks doors/lifts and projects bounded anti-mobility fields | illusioner/control research | destroy relay, interrupt cast, alternative route |
| `processional_guard` | Continuance | elite melee | disciplined parry/advance around monumental thresholds | vindicator/knight concepts | bait finite guard meter; punish recovery |
| `crown_adjudicator` | Continuance | commander | formation orders, target designation, reinforcement budget | illusioner/raid captain logic | sever command link; commander vulnerable during orders |
| `burdened_dead` | Procession | pressure line | slow advance, grabs, space denial | ghoul/ghouling/revenant | head/limb stagger, fire/light tools, keep formation |
| `gallows_echo` | Procession | ambusher | descends from ceilings/shafts after a readable omen | nameless-hanged/wraith research | look/listen, light the anchor, interrupt descent |
| `vault_wraith` | Procession | displacement specialist | bridge knockback, phase across gaps, sightline pressure | wraith/reaper | grounding field, cover, phase-exit vulnerability |
| `ledger_revenant` | Procession | elite ranged | marks resource use and punishes repeated healing/filtering | acolyte/lich projectile research | vary actions, break focus, destroy record sigils |

### 5.1 Complete Verdant roster (in addition to the 20-entity custom core)

The full viable Spore roster is a mandatory parallel combat roster, not three encounter
modules. `docs/hive-strain/roster-manifest.json` is the generated inclusion authority:

| Verdant class | Included creatures | Endgame function |
|---|---:|---|
| infected | 12 | familiar baseline bodies rebuilt as dangerous formation members, carriers, decoys, tool users, and pressure screens |
| evolved | 32 | the main role-complete combat body: flankers, artillery, pursuit, tanks, support, control, and disruption |
| hyper-evolved | 12 | elites and formation breakers; ordinary encounters use them deliberately rather than as uncontrolled spam |
| organoid | 10 | territory infrastructure, support, reconstruction, command, and nest/organ objectives |
| calamity | 10 | landmark, assault, roaming catastrophe, and major-encounter threats with exclusive or heavily bounded budgets |
| hivemind | 1 | rare command/ecology controller; never a casual ambient roll |
| auxiliary entities | 19 | projectiles, detached parts, thrown objects, and effects activated only through owning creature mechanics |

This is intended to feel like **everything the player has already survived, repeated
harder**. The creatures keep the same recognizable attacks, evolution, progression,
summons, strengths, weaknesses, and counterplay. Their sole direct combat alteration
is the dimension-scoped 3× maximum-health modifier. The harsher result comes from
needing to execute the already-learned counters for much longer while also managing
the Cinderstack's fog, acid, atmosphere, routes, and other enemy families.

The companion must not “improve” Spore target selection, timing, resistance, crowd
control, pathing, damage, evolution, or abilities. Predictability is part of the design:
the player understands what is coming, but cannot erase it with the same short burst
that worked earlier in progression.

### 5.2 Verdant presence by elevation

| Region | Mandatory Verdant presence | Escalated rematch character |
|---|---|---|
| Dead wastes / apron | infected/evolved hunting groups; rare hyper-evolved patrol or announced calamity | the same open-ground threats take three times as long to kill under sulfur fog and with fewer safe landmarks |
| The Drown | locomotion-compatible infected/evolved, organoid sites, selected calamities | unchanged ambush/control behavior becomes harder beside acid, darkness, ledges, and filter pressure |
| The Underworks | broad infected/evolved roster plus hyper-evolved hunters | unchanged pursuit and pack behavior persists through dense routes long enough to threaten retreat |
| Furnace Tiers | evolved/hyper-evolved groups and organoid support | familiar artillery, brutes, and reconstruction survive longer amid industrial hazards |
| Billet Decks | infected tool users, evolved formations, hyper-evolved creatures | familiar roles remain predictable but cannot be burst down before room geometry matters |
| The Vaulting | aerial/ranged evolved, hyper-evolved elites, organoids, bounded calamities | unchanged flight, displacement, and artillery last longer across bridges and long sightlines |
| The Crown | hyper-evolved, organoid sites, calamity/hivemind encounters, supported by selected lower classes | the complete established progression returns at full breadth with 3× durability and endgame surroundings |

Every region includes Verdant entries in ordinary or authored traversal—not only rare
events. Across the retained reserved-seed suite, all 77 viable creatures must be
reachable without debug summoning through documented production encounter paths.

### 5.2 Major encounters

| Technical handle | Location/function | Required identity |
|---|---|---|
| `acid_sink_engine` | Drown landmark; pumps, acid level controls, caustic fauna | environmental boss built around valves, safe ledges, and fume timing—not a health sponge |
| `trunk_warden` | restored causeway objective | mobile machine formation boss proving long-axis cover, reinforcements, and extraction |
| `last_superintendent` | Crown capstone | original command intelligence using lockdown, atmosphere, architecture, and subordinate roles across clear phases |

The Last Superintendent may not be a renamed raw boss. It requires an original model,
sound identity, arena language, failure/recovery loop, and multiplayer repeat test.

## 6. Band deployment: equal endgame floor, different encounter language

| Region | Ordinary composition | Signature pressure | Why endgame gear is still threatened |
|---|---|---|---|
| Dead wastes / apron | 2–5 Sinkborn/Ashbound/Continuance or 2–5 Verdant creatures; mixed-territory collisions | weather concealment, long pursuit, sparse cover, filter attrition | attackers force movement away from navigation landmarks and shelters; no “safe run between Stacks” |
| The Drown | 3–6 fauna/dead/custom units or locomotion-compatible Verdant roster | acid edges, pulls, low visibility, short escape lanes | environment amplifies familiar and custom threats; acid and atmosphere remain independent defenses |
| The Underworks | 5–9 mixed custom or Verdant pursuit units | vents, flanks, alarms, route hunting | numerical pressure and 3× Verdant durability attack retreat plans rather than armor alone |
| Furnace Tiers | 4–7 machines or Verdant evolved/hyper/organoid composition | crossfire, reconstruction, machinery lanes | extended familiar fights and custom suppression punish static high-DPS play |
| Billet Decks | 5–8 organized custom squad or Verdant formation | shields, doors, room pressure, reinforcement routes | durable known threats and coordinated new threats both require target priority |
| The Vaulting | 3–6 custom elites/controllers or Verdant aerial/ranged/hyper/calamity composition | flight, bridges, long sightlines, displacement | small groups remain lethal through long exposure to positional failure and fall risk |
| The Crown | 3–5 pristine custom elites, or bounded Verdant hyper/organoid/calamity/hivemind encounter | access pressure, complete progression, major threats | optimized builds face either command synergy or the full familiar roster at 3× health |

No band table may contain only light/fodder roles. Every ordinary composition includes
either a specialist, controller, support, elite, environmental amplifier, or a Verdant
composition whose established behavior and 3× durability meet the same threat budget.

## 7. Encounter grammar and spawn ownership

### 7.1 Spawn channels

| Channel | Owner | Use | Persistence |
|---|---|---|---|
| ambient territorial fauna | companion dimension spawn rules | low-density wastes/Drown ecology only | normal despawn; strict local budget |
| Verdant territorial spawn | companion stratum/region spawn handler | full viable Spore roster across wastes and all six bands, preserving native behavior/evolution | normal Spore lifecycle plus dimension containment and strict local budget |
| authored room encounter | companion encounter director + structure anchor | primary city combat | one-shot or reset-policy state keyed to anchor UUID |
| patrol/route encounter | director + navigation graph | moving Ashbound/Continuance formations | route state, leash, clean unload |
| Verdant nest/assault/calamity | director + explicit event/territory marker | organoid territory, roaming assaults, calamities, and cross-family conflict | bounded placement/event state with cleanup and cooldown; native creature AI unchanged |
| landmark/boss | dedicated controller | objectives and capstones | explicit start, wipe, recovery, completion and repeat state |

Biome natural-spawn tables do not own city elites, commanders, or bosses. Permanent
vanilla spawners are prohibited for the production loop because they create farming,
chunk-ticking, and persistence problems.

### 7.2 Encounter anchors

Phase 4 modules receive inert `infinite_domain_hive_world:encounter_anchor` markers
with:

```text
anchor_uuid
band
room_role
territory
encounter_profile
min_clear_radius
spawn_and_fallback_points
retreat_boundary
safe_route_boundary
reset_policy
loot_authority
```

The companion replaces/consumes the marker when the containing structure becomes
active, validates walkable spawn points, and stores completion in level data. Chunk
reload must never duplicate a formation or its secured reward.

### 7.3 Weighted population budget

| Role | Budget weight |
|---|---:|
| light / spotter | 1 |
| standard line / skirmisher | 2 |
| specialist / controller / support | 3 |
| elite | 6 |
| commander | 10 |
| boss | exclusive controller; never shares ambient budget |

Verdant budget mapping preserves behavior and changes only encounter accounting:

| Existing Spore class | Initial budget treatment |
|---|---|
| infected | standard line/skirmisher; 1–2 points according to actual body/child cost |
| evolved | standard or specialist; 2–3 points |
| hyper-evolved | specialist/elite; 3–6 points |
| organoid | support/controller/commander; 3–10 points and placed-territory rules |
| calamity | elite, commander, or exclusive major controller; never uncontrolled ambient spam |
| hivemind | exclusive landmark/ecology controller |
| auxiliary entities | charged to their owner; hard lifetime/child caps where the base mod does not already provide them |

Initial limits, pending C0090/C0098 profiling:

- ambient territory: 8 points per nearby player, capped at 16 for the area;
- authored solo room: 16–20 points;
- each additional nearby participating player: +6 points, capped at 36;
- no more than 18 regular hostile creatures from the custom-plus-Verdant encounter
  program within 128 blocks of one solo player, unless an explicitly profiled calamity
  controller requires fewer large entities;
- no ambient spawning while a boss controller is active in the same landmark;
- no AI ticking outside the configured player activation radius.

Multiplayer scaling adds roles and ability frequency before health. Starting shape:
`+25%` boss/commander health and `+6` formation points per additional participating
player, capped at four additional-player steps. Damage rises only after playtest proves
that added crossfire is insufficient. This custom-entity scaling does not alter Spore
AI or stats: Verdant creatures remain at exactly 3× maximum health regardless of party
size; multiplayer changes only how many/which creatures an encounter profile selects.

## 8. Endgame balance contract

### 8.1 Reference kits precede final numbers

C0083 must define at least four reproducible kits:

1. heavy armor / low mobility;
2. high mobility / lower mitigation;
3. ranged or explosive damage specialist;
4. cyberware/utility specialist.

Every kit declares armor, toughness, effective health, healing per minute, sustained
and burst DPS, range, crowd control, movement, shield behavior, consumables, filter
capacity, acid protection, and energy/ammunition limits. Balance evidence records the
exact item IDs and configuration versions. “Netherite equivalent” is too vague.

Until C0083 freezes those kits, all values below are **initial tuning envelopes for the
20 new custom entities**, not accepted stats. They do not override any base Spore
attribute except the fixed Verdant 3× maximum-health modifier.

### 8.2 Initial attribute envelopes

| Class | Health | Armor | Single-hit raw damage | Intended solo TTK against benchmark output |
|---|---:|---:|---:|---:|
| light / spotter | 70–140 | 4–10 | 10–18 | 2–5 s |
| standard line / skirmisher | 160–320 | 8–18 | 16–28 | 6–12 s |
| specialist / support | 140–280 | 6–16 | 12–26 plus bounded mechanic | 6–14 s when focused |
| elite | 450–900 | 14–24 | 24–42 | 20–45 s |
| commander | 1,000–2,200 | 18–28 | 30–52 | 60–120 s with formation |
| major encounter | phase pools totalling 4,000–10,000 | mechanic-specific | 35–65, heavily telegraphed | 4–9 min solo; 3–7 min prepared group |

These are not permission to maximize every column. Armor, health, mobility, support,
and damage consume a role power budget. High armor requires a break state or exposed
weak point. High mobility requires recovery windows. High damage requires strong
telegraph and limited frequency.

### 8.3 Lethality and resource targets

- A normal authored solo encounter should threaten 20–40 percent of effective health
  or consume an equivalent share of healing/energy/ammunition/filter reserve when
  handled competently; repeated rooms create expedition attrition.
- A standard formation should defeat an idle reference-kit player in roughly 12–20
  seconds. This is an anti-trivialization test, not normal expected play.
- A competent reference-kit player must have a reproducible win path without perfect
  reaction time or foreknowledge.
- One light unit is pressure, not a duel boss. Its danger comes from formation role.
- No ordinary attack removes more than 35 percent of a reference kit's effective
  health after expected mitigation. Boss attacks may exceed this only with a clear
  tell, escape route, and recovery window.
- Armor bypass, percent-health damage, shield disable, EMP, healing suppression, and
  equipment drain are capped typed mechanics. No unit receives all of them.
- True damage is reserved for environmental contract interactions and exceptional,
  telegraphed boss mechanics; it is not a shortcut around balancing armor.

### 8.4 Custom-entity anti-bullet-sponge rule and Spore exception

An enemy that exceeds its TTK target must lose health/armor before gaining damage.
An enemy that fails to threaten optimized gear gains formation synergy, accuracy,
positioning, or a typed mechanic before gaining health. Blanket multipliers across a
non-Spore donor corpus are prohibited.

The complete Spore roster is the explicit exception: owner direction accepts exactly
3× maximum health because the desired experience is the same predictable progression
again, but harder to put down. A long Verdant TTK is therefore not by itself a failure.
Balance review checks whether population density, calamity overlap, and environmental
pressure remain survivable and performant without changing creature behavior or the
multiplier.

## 9. Ability construction rules

Every ability data record includes:

```text
ability_id
owner_roles
range_and_shape
windup_ticks
active_ticks
recovery_ticks
cooldown_ticks
line_of_sight_rule
damage_and_damage_type
status_or_movement_effect
projectile_or_child_entity_budget
terrain_and_block_interaction
audio_visual_tell
interrupt_conditions
counterplay
multiplayer_scaling
server_cost_budget
```

Required fairness rules:

- tells remain readable through the intended fog range;
- off-screen lethal projectiles have directional audio and a minimum travel time;
- crowd control has diminishing returns and cannot chain-lock a player;
- pulls/knockback near acid or voids provide an interrupt or anchoring response;
- teleports require valid destination, sight/omen, cooldown, and stuck recovery;
- summons consume the same encounter budget and die/despawn with their controller;
- no permanent block destruction, acid placement, fire spread, or fluid grief;
- doors and lifts may be locked only through encounter state and must unlock on clear,
  wipe, timeout, or controller failure;
- abilities fail safe on chunk unload and dimension exit.

## 10. Hazard compatibility matrix

| Family | Atmosphere | Acid | Radiation | Shelter/doors | Special rule |
|---|---|---|---|---|---|
| Continuance | immune to breathing exposure | ordinary frames corrode; designated acid-sink frames resist | no ambient immunity claim; localized EMP/radiation interactions explicit | can operate locks but cannot spawn inside verified safe volumes | EMP is a bounded stagger/ability disruption, not permanent shutdown |
| Ashbound | requires masks/filters or clean territory | damaged normally unless visibly equipped | same localized rules as players | may use/breach authored doors; cannot invalidate a certified shelter without an encounter tell | their equipment obeys resource logic in fiction and encounter timing |
| Sinkborn | adapted to local air | immunity/resistance only by species role | no special radiation benefit | cannot enter sealed shelters except explicit breach species | acid swimming never grants immunity to all chemical/heat damage |
| Procession | no breathing exposure | damaged unless a specific spectral phase says otherwise | no ambient interaction | may phase through designated porous/ruined boundaries only | phase state is visible and cannot bypass protected arrival rooms |
| Verdant | full roster retains native Spore breathing behavior | native acid behavior unchanged | independent | cannot grow permanently through protected volumes | AI/progression unchanged; world spread, child/entity count, and chunk-loading side effects are containment concerns, not creature redesign |

Enemy attacks do not consume player filter charge directly unless the specific ability
adds atmosphere exposure through the established C0069 API. No enemy may silently
write its own parallel air/radiation system.

## 11. Original entity implementation architecture

### 11.1 Code/data boundary

| Concern | Owner |
|---|---|
| entity type, attributes, goals, navigation, abilities, damage, networking, persistence | Hive companion Java |
| role/family/band/hazard tags | Hive datapack |
| encounter profile composition and weights | validated data consumed by companion |
| models, textures, animations, particles, sounds | original Hive resource assets |
| loot tables and salvage pools | Hive datapack, coordinated with C0091/C0092 |
| temporary donor summons and QA commands | development-only scripts/commands |

Production IDs use `infinite_domain_hive_world` for code registries and
`infinite_domain:hive_world_*` for datapack resources. Player-facing values obey the
C0003 prohibited-language contract.

### 11.2 Class shape

Prefer pack-owned composition:

```text
HiveEnemyEntity / HiveFlyingEnemyEntity
  + EnemyRoleProfile
  + AbilityController
  + HazardAffinity
  + EncounterMembership
  + StuckRecovery
  + ServerTelemetry
```

Shared goals and abilities are pack-owned reusable components. Do not create twenty
copy-pasted monolith classes and do not make production types depend on private
third-party entity classes. Vanilla `Monster`, `PathfinderMob`, navigation, goals,
attributes, and projectile primitives are preferred stable foundations.

GeckoLib is present in the instance and may be adopted for original animated models
after a client/dedicated-server dependency and render-budget spike. Simple entities
should use vanilla model/render infrastructure when it is sufficient; animation
middleware is not mandatory for every creature.

### 11.3 Data versioning and failure behavior

- Each entity saves `entity_schema_version`, family, role, anchor UUID, encounter UUID,
  and ability state needed for a clean reload.
- Unknown/old versions migrate or despawn with a logged recovery record; they do not
  crash world load.
- Missing optional donor mods cannot break production entities because donor classes
  are not their runtime base.
- Missing required animation/runtime dependencies fail during startup with an explicit
  dependency declaration, never as a mid-fight renderer crash.
- Removing the entire Hive feature remains additive: the rollback manifest owns code,
  data, assets, encounter state keys, and the companion JAR.

## 12. Art, animation, audio, and readability

### 12.1 Shared visual progression

- Drown/Underworks: corroded, repaired, mismatched, residue-heavy, blunt silhouettes.
- Furnace: heat shielding, exposed actuators, hazard paint, industrial tools.
- Billet: standardized security profiles and institutional insignia.
- Vaulting: elongated ceremonial profiles readable across long sightlines.
- Crown: pristine finish, deliberate ornament, restrained luminous detail, precise
  motion and superior equipment.

Opulence increases with height, but brightness does not become visual noise. Enemies
remain readable against dark mineral architecture and cloud/fog strata.

### 12.2 Required animation states

At minimum: idle/search, locomotion, acquire/alert, primary wind-up/active/recovery,
stagger or break, ability state, death, and any traversal-specific state. Commanders
also need an unmistakable order/channel state. Boss phases require transition and wipe
recovery states.

### 12.3 Audio rules

Each family has a navigational sound language:

- Continuance: relay tones, actuator rhythm, command pips;
- Ashbound: muffled speech/radio, equipment, filter breath;
- Sinkborn: fluid movement, scraping, pressure clicks;
- Procession: architectural resonance and repeated institutional motifs;
- Verdant: the established Spore audio language is preserved so the rematch remains
  immediately recognizable; the green visual treatment and Cinderstack ambience supply
  the variant identity.

Priority attacks must remain directionally legible beneath ambience. Continuous loops
are range-limited and stop on unload/death.

## 13. Loot, farming, and progression

- Ordinary entities drop bounded salvage components, biological samples, credentials,
  or damaged parts—not intact endgame machines or final weapons.
- Enemy drops feed C0091 uses and C0092 tables. No drop exists without a declared sink.
- Formation/anchor completion owns secured rewards; individual mobs cannot be farmed
  to bypass landmark or capstone progression.
- Summons, clones, and child entities have no independent valuable loot.
- Repeated encounter rewards follow an explicit reset/cooldown policy and are audited
  for multiplayer duplication, chunk reload, death, retreat, and dimension transfer.
- Equipment visible on an enemy is not automatically a guaranteed item drop.
- Boss rewards are granted transactionally after completion state is persisted.

## 14. Performance and anti-pathology budgets

Initial budgets, subordinate to `performance-budget.md` and proven at C0098/P06-GATE:

- all active custom-enemy AI within one player's 128-block combat radius: average
  `<= 2.0 ms/tick`, p95 `<= 4.0 ms/tick` on the reference host;
- ordinary entity AI: average `<= 0.08 ms/tick`; elite `<= 0.16`; commander `<= 0.30`;
- path recalculation is cooldown-bound; no every-tick full route searches;
- no more than 32 hostile projectiles and 12 short-lived ability area entities inside
  one active non-boss encounter;
- every child/projectile/area entity has a hard lifetime and owner cleanup;
- no ticking block entity is created solely to run enemy AI;
- stuck recovery cannot teleport more than once per configured cooldown and never into
  a shelter, fluid hazard, wall, or unloaded chunk;
- no enemy force-loads chunks;
- inactive anchored encounters serialize and stop ticking;
- client LOD/culling is tested in the Vaulting's longest sightlines and through cloud
  decks; animation and particles honor the Nether-comparison frame budget.

## 15. Validation program

### 15.1 Static validator

Create `scripts/endgame/validate_hive_world_entities.py` to prove:

1. every custom entity ID is registered exactly once;
2. every entity has family, role, band eligibility, attributes, hazard profile,
   abilities, loot, budget weight, model/texture, sound, and translation entries;
3. every encounter profile resolves real roles and stays within its point envelope;
4. all 77 viable Verdant creatures occur in at least one production spawn/encounter
   profile, all 19 auxiliaries are classified, and no viable creature is silently omitted;
5. no player-facing string violates C0003;
6. no entity or spawn table targets a non-Hive dimension/biome;
7. summons/projectiles have owner, cap, lifetime, and no valuable loot;
8. no raw non-Spore donor ID appears in a production encounter profile; `spore:` IDs
   are the explicit full-roster exception and must resolve through the Verdant manifest;
9. no permanent spawner or unsafe generic natural-spawn rule owns elites/bosses;
10. every drop resolves to C0091/C0092 ownership.

### 15.2 Live donor audit

For every donor candidate, capture: summon success, attributes, navigation in the three
route widths, target acquisition, door/ledge/fluid behavior, every attack, child count,
despawn, death, chunk unload/reload, TPS sample, and client frame sample. The audit
decides `research`, `greybox`, or `reject`; it does not create a production adoption.

### 15.3 Reference-kit combat matrix

Each of the four C0083 kits runs:

- solo and 2/4-player versions;
- one ordinary encounter in every band plus wastes;
- the exact base Spore behavior/progression versus its Verdant counterpart, proving
  behavioral parity and exactly 3× maximum health for all 77 viable creatures;
- a retained encounter/spawn path for every viable Spore creature without debug summon;
- each specialist in isolation to verify readable counterplay;
- two mixed formations per band;
- acid-adjacent, fog, bridge, shaft, doorway, shelter-boundary, and long-corridor cases;
- retreat, wipe, return, chunk unload, relog, death, and repeat completion;
- optimized damage burst, crowd control, flight/high mobility, shielding, and terrain
  cheese attempts.

Record damage taken, effective health lost, healing/energy/ammunition/filter consumed,
enemy TTK, encounter duration, downs/deaths, path failures, stuck recovery, spawned
entity peak, server ms/tick, and client FPS.

### 15.4 Acceptance conditions

C0089/C0090 cannot be accepted until:

- every band can kill an idle endgame reference player within the target envelope;
- every band can be cleared reproducibly by competent play with each viable reference
  kit and no mandatory single build;
- independent reviewers identify family, role, attack tell, and counterplay without
  debug labels;
- no ordinary enemy is a bullet sponge outside its TTK envelope;
- no unavoidable one-shot, stun lock, spawn trap, shelter violation, permanent door
  lock, loot duplication, or cross-dimension spawn occurs;
- hazard affinities match §10 and no parallel atmosphere/radiation system appears;
- all static, dedicated-server, multiplayer, persistence, performance, and visual
  matrices pass;
- all 77 viable Spore creatures preserve base behavior and receive exactly the green
  dimension treatment plus 3× maximum health, with no cross-dimension leakage;
- the Last Superintendent passes the C0095 repeatable multiplayer failure/recovery
  test and receives independent visual approval.

## 16. Development sequence

| Slice | Deliverable | Gate to next slice |
|---|---|---|
| E1 — corpus audit tooling | entity-corpus audit generator/schema plus QA summon arena | every prioritized donor measured and classified |
| E2 — reference kits | exact four-kit manifests and combat telemetry harness | C0083 kits reproducible on client/server |
| E3 — companion foundation | registration, base entity classes, role/ability/hazard/telemetry components | dedicated server and client start; save/reload clean |
| E4 — three-role vertical slice | `survey_drone`, `ash_skitterer`, `burdened_dead` with original assets | one machine/fauna/revenant role passes TTK, readability, hazard and perf tests |
| E5 — encounter director | anchors, weighted profiles, persistence, cleanup, multiplayer scaling | no duplicate/leak/farm across reload/death/transfer |
| E6 — band roster | remaining 17 core entities and band profiles | every band meets equal endgame floor with distinct tactics |
| E7 — full Verdant integration | dimension renderer/overlay, fixed 3× health handler, all 77 viable creatures, all 19 auxiliaries, stratum spawn handler, organoid/calamity placement and cross-family hostility | 77/77 reachable, behavior parity, exact multiplier, containment, cleanup, performance and three-sided fights pass |
| E8 — major encounters | Acid-Sink Engine and Trunk Warden | objective, wipe/recovery, repeat and performance pass |
| E9 — capstone | Last Superintendent, arena, rewards, failure/recovery | C0095 independent multiplayer acceptance |
| E10 — production balance | C0098 full kit/band/party/cheese matrix | P06-GATE |

The first production implementation slice is deliberately three entities, not twenty.
It proves the complete pipeline—original identity, code, data, rendering, sound,
encounter ownership, hazard behavior, telemetry, and rollback—before roster expansion.

## 17. Required evidence paths

```text
docs/endgame/entity-corpus-audit.json
docs/endgame/entity-roster-manifest.json
docs/endgame/encounter-profile-manifest.json
docs/endgame/evidence/EG-P06-S04-C0089/
  donor-audit/
  registry-and-assets/
  hazard-matrix/
  reference-kit-combat/
  persistence-and-multiplayer/
  performance/
  visual-review/
docs/endgame/evidence/EG-P06-S04-C0090/
docs/endgame/evidence/EG-P06-S07-C0095/
scripts/endgame/validate_hive_world_entities.py
```

Every evidence directory contains exact mod/config versions, seed, coordinates,
reference kit, party size, encounter profile, raw telemetry, screenshots/video where
applicable, validator output, reviewer identity, and pass/fail disposition.

## 18. Explicit rejection list

- omitting any of the 77 viable Spore creatures from production encounter reachability;
- treating any of the 19 Spore auxiliary entities as an independent roster creature;
- rewriting Spore AI, attacks, evolution, progression, resistances, or timing for the
  Verdant variant instead of preserving the predictable base behavior;
- applying any Verdant multiplier other than the owner-approved dimension-only 3×
  maximum health rule;
- making lower bands early-game difficulty;
- raw fantasy dragons/mythic creatures as ordinary Cinderstack inhabitants;
- a roster made solely from recognizable vanilla mobs with renamed display strings;
- permanent mob spawners as the main encounter system;
- random natural spawning of elites, commanders, or bosses;
- silent armor-bypass/true-damage attacks;
- universal immunity to acid, atmosphere, radiation, fire, and EMP;
- AI that breaks arbitrary player blocks, places persistent acid/fire, force-loads
  chunks, or teleports through certified shelters;
- valuable summon/clone drops or reload-duplicable rewards;
- one mandatory combat build or one immunity item that trivializes a family;
- production dependence on private third-party entity classes or unapproved assets;
- claiming visual or balance acceptance from static registry/build evidence alone.

## 19. Decision summary

The production enemy identity is a contested vertical ecosystem containing the **full
active Verdant roster** alongside the Continuance, Ashbound crews, Sinkborn fauna, and
Procession revenants. Verdant is the complete familiar Spore progression with unchanged
behavior, a green dimension treatment, and exactly 3× maximum health—everything the
player fought before, now much harder to put down. The other installed entities
accelerate research and greyboxing, while new non-Spore enemies remain pack-owned
custom types with original assets, bounded encounter ownership, explicit hazard
behavior, and measured reference-kit balance.

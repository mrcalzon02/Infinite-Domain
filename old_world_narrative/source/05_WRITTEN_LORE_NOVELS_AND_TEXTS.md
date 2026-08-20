# 05 — Written Lore, Novels, Books, Signs, and Texts

## Narrative philosophy

The canon bible explicitly says that most Minecraft books should be short and carry one useful idea, and that signs should do more work because players can read them while moving. Preserve that rule.

The user also wants **multiple Minecraft novels/books/texts**. Implement that by dividing written content into two layers:

1. **Common short-form evidence** — reports, memos, logs, notices, manifests, maintenance cards, medical briefs, orders, diaries. These carry the main archaeological story.
2. **Rare long-form collectible series** — optional serialized books that deepen characters, culture, and human experience without hiding mandatory quest facts behind long reading sessions.

## Minimum corpus at completion

- 8 serialized long-form series.
- 96 short written records minimum.
- 160 sign strings minimum.
- 48 graffiti strings minimum.
- 64 unique proof-item texts/names or equivalent unique tokens.
- Charles reaction text for each major Exploration quest and selected optional branches.

## Stable text registry

Create a single registry/manifold for all narrative texts. Each entry should have:

- stable ID;
- title;
- author or issuing institution;
- document class;
- approximate chronology / collapse phase;
- spoiler tier;
- structure families where it may appear;
- whether it is quest-critical;
- deterministic or random placement rule;
- body/localization key;
- optional series/volume number;
- any Darknet gating requirement.

Do not duplicate entire book bodies across many scripts. Prefer localization/data-driven sources where supported.

## Document voices

### Corporate material
Optimistic, polished, commercial, competent. Early VCF material should be proud because Evercrop really solved problems. Aevum material should sound like genuine medical progress.

### Technical records
Dry, specific, procedural. Concern rises through numbers, replacement intervals, anomalous samples, and repeated failure rather than melodrama.

### Continuity records
Analytical and cross-disciplinary, increasingly frustrated. They should show uncertainty, argument, comparison, and synthesis—not supernatural certainty.

### Military records
Concise and operational. Show decisions, objectives, constraints, evacuation windows, sterilization criteria, and local success metrics.

### Civilian records
Personal, incomplete, sometimes wrong. Rumor is allowed. Civilians do not need to explain EP-7/PT-9 taxonomy in a diary.

### Blackglass archives
Often metadata-heavy, encrypted, access-controlled, and valuable mainly after Darknet progression.

### Asterion records
Technical/operational but increasingly detached from Earth's information collapse; they can preserve records terrestrial systems lost.

## Rare long-form series

Implement at least these eight series or canon-consistent equivalents. Treat them as multi-volume written-book collectibles so no single item becomes an absurd wall of text.

### Series 1 — *Green Without Fields*
Type: popular science / corporate-era nonfiction.
Purpose: lets the player experience why urban fungal agriculture was admired before the crisis.
Suggested 5 volumes: The Vertical Acre; Cultures That Travel; The End of Crop Loss; Feeding Dense Cities; The Future Pantry.
Placement: libraries, VCF offices, schools, clean markets, homes.
Spoiler level: low. Do not reveal catastrophe.

### Series 2 — *A Hundred Good Years*
Type: patient-story / medical popular press collection.
Purpose: demonstrates the genuine human value of APL-derived medicine.
Suggested 5 volumes: The Second Recovery; Nerves Remember; After the Tumor; The Long Middle Age; Waiting Lists.
Placement: Aevum clinics, hospitals, homes, libraries.
Spoiler level: low-to-mid. Later volume may mention supply pressure but not the full ecological mechanism.

### Series 3 — *The Maintenance Winter*
Type: facilities engineer memoir / serialized diary.
Purpose: turns the material-integrity crisis into lived experience: 180-day service, then 41, then 11, then permanent crews.
Suggested 6 volumes.
Placement: Atlas, Helion, municipal utilities, PolyCore sites.
Spoiler level: mid.

### Series 4 — *Letters from Gate Seven*
Type: civilian correspondence.
Purpose: follows a family separated by quarantine boundaries that keep moving while authorities promise temporary closure.
Suggested 6 volumes.
Placement: shelters, apartments, transit stations, checkpoints, libraries.
Spoiler level: mid.

### Series 5 — *No Clean Zone*
Type: collected Continuity working papers edited into a rare archive series.
Purpose: deepens the cross-disciplinary reasoning behind Distributed Reservoir Theory.
Suggested 7 volumes, each centered on one evidence family rather than one omniscient answer.
Placement: Continuity sites and late Blackglass archives.
Spoiler level: high. Some volumes gated until mid/late Exploration.

### Series 6 — *Firebreak: Six Days of Sterility*
Type: operations chronicle assembled from military and civic records.
Purpose: shows why the first Firebreak appeared to work locally and why that visible success changed policy.
Suggested 5 volumes.
Placement: military bases, observation bunkers, late libraries/archives.
Spoiler level: high.

### Series 7 — *Nineteen Kilometers*
Type: atmospheric station field chronicle.
Purpose: humanizes the monitoring teams and builds toward the final high-altitude detection without replacing the canonical detection record itself.
Suggested 4 volumes.
Placement: remote science stations and Continuity archives.
Spoiler level: very high. Final mandatory proof remains a separate short record.

### Series 8 — *Last Light from Asterion*
Type: mission-log / evacuation chronicle.
Purpose: bridges terrestrial collapse into orbital archaeology and preserves uncertainty about how long off-world populations endured.
Suggested 6 volumes.
Placement: Asterion facilities and later orbital locations.
Spoiler level: late/space.

## Long-form series rule

A long-form series is optional atmosphere, not a mandatory decoding test. The player should never be required to collect all volumes of a novel to prove a core quest beat.

Volume length should be comfortable in the actual Minecraft implementation. Discover the pack/version's real written-book component/NBT format and practical page limits; do not assume a schema from memory. Keep paragraphs short enough for the in-game book UI.

## Short-record distribution

Use the seed corpus in `05A_LORE_CORPUS_SEED.csv` as required anchors, then expand to at least 96 records.

Recommended distribution minimums:

- VCF: 16
- Atlas: 8
- PolyCore: 12
- Pleroma/ports: 10
- Aevum: 12
- Helion: 8
- Blackglass: 8 readable + encrypted archive entries
- Continuity: 10
- military/Firebreak: 8
- civilian/municipal: 8
- Asterion: 8

Counts may overlap categories and may exceed 96.

## Signs

Signs are the high-frequency timeline. Build pools by institution and phase.

Examples of semantic progression:

Normal operation -> special handling -> containment -> material prohibition -> airborne warning -> Firebreak authority -> abandonment.

Do not make every sign a lore speech. Most should be plausible operational labels: room names, dock numbers, culture levels, safety rules, maintenance intervals, queue instructions, quarantine status, route closure, access control.

## Graffiti

Use sparingly. Graffiti is rumor and fear, not objective exposition. Recurring phrases can create cultural memory, but do not plaster every wall.

Seed ideas consistent with canon include:

- IT'S IN THE WALLS
- THE FILTERS DON'T WORK
- VCF KNEW
- DON'T GO SOUTH
- THE PORT IS CLOSED
- STOP BURNING IT
- THERE IS NO CLEAN ZONE
- IF YOU CAN SEE THE BLOOM YOU'RE ALREADY TOO LATE

Add additional short civilian phrases, but preserve ambiguity where accusations exceed what the canon proves.

## Quest-critical placement

Every mandatory written proof should have deterministic placement or a guaranteed loot mechanism inside its target structure. Ambient records can be random. Never make a mandatory quest depend on a 10% chest roll.

## Duplicate handling

It is fine for common corporate manuals or public notices to repeat. Unique quest proofs should not randomly appear everywhere. Keep their identity and placement controlled enough that finding one means something.

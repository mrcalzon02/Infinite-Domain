# Endgame — spatial-metrics contract

**Authority:** `docs/Endgame.md` §3 and checkpoint `EG-P00-S02-C0004`.

**Status:** accepted 2026-08-27 as a working contract. Every number here is
**provisional** and must be proven at Phase 2 (`EG-P02` greybox) and frozen only at
`P02-GATE`. This checkpoint chooses names, bands, fields, and rhythm — not geometry.

Depends on: C0003 identity (band and field names honour the prohibited-terminology
table). Does not depend on: C0005 architecture, C0006 numeric height, C0007 hazards.

---

## 1. Vertical bands (accepted names)

The six placeholder band identities in `docs/Endgame.md` §3 are replaced as follows.
The working ranges are unchanged from the source table and remain provisional.

| # | Accepted band name | Working range (Y) | Height | Primary identity | Traversal grammar |
|---|---|---:|---:|---|---|
| 1 | **The Drown** | `-64..-33` | 32 | acid reservoirs, buried foundations, ancient machinery, structural roots | flooded ledges, maintenance gantries, sealed shafts |
| 2 | **The Underworks** | `-32..47` | 80 | collapsed quarters, unsanctioned settlement, tunnels, abandoned transit | short loops, vertical bypasses, unstable crossings |
| 3 | **The Furnace Tiers** | `48..111` | 64 | manufactories, freight rail, waste conduits, power and ventilation plants | industrial halls, rail axes, service networks |
| 4 | **The Billet Decks** | `112..191` | 80 | residential slabs, markets, institutions, civic monuments, civic ruins | district streets, stacked interiors, public stairs |
| 5 | **The Vaulting** | `192..255` | 64 | cathedral-scale arches, suspended transit, processional voids | long axes, bridges, elevators, major thresholds |
| 6 | **The Crown** | `256..319` | 64 | fortified crowns, observatories, command centres, capstone sites | exposed ascent, controlled gates, final expedition loop |

Total engineered extent: `-64..319` (383 blocks). Band boundaries are *transition
zones*, not hard planes: each boundary owns a 6–16 block architectural seam
(a plant deck, a rubble choke, a transit interchange) authored at Phase 4.

Band identity must be legible **without labels** (`P02-GATE` exit criterion): a player
dropped at a random Y inside a stack core must be able to name the band from
architecture, light, fog, palette, and enemy signature alone.

## 2. Horizontal world-scale fields (accepted names)

The four placeholder field names in `docs/Endgame.md` §3 are replaced as follows.

| # | Accepted field name | Role | Generator ownership |
|---|---|---|---|
| 1 | **Stack core** | full-height engineered mass and the six strata | density mass field + deterministic macro placement (C0005) |
| 2 | **Stack apron** | perimeter walls, collapsed suburbs, slag, transport yards, defence works | apron mask + jigsaw module families |
| 3 | **Trunk axis** | aligned corridors, causeways, rail, pipes, pylons, and monumental arches between clusters | deterministic cross-chunk axis planner (Hive-owned, `EG-P04-S05-C0062`) |
| 4 | **Dead wastes** | dominant planetary terrain separating clusters | wasteland noise settings + sparse features |

"Trunk axis" replaces the placeholder "interhive axis". "Stack core / apron" replace
"hive core / apron". Player-facing text never uses the words in the C0003 prohibited
table.

## 3. Provisional scale targets (to be proven at Phase 2/3)

| Metric | Provisional target | Proven at |
|---|---|---|
| Stack core diameter | 600–1,200 blocks | `EG-P03-S02-C0039` |
| Stack-cluster separation (core to core) | 2,000–4,000 blocks | `EG-P03-S02-C0039` |
| Monumental void width (in The Vaulting) | 80–240 blocks | `EG-P02-S04-C0031`, `EG-P03-S04-C0043` |
| Apparent trunk-axis length | 500–1,500 blocks across independently aligned segments | `EG-P03-S02-C0040`, `EG-P04-S05-C0062` |
| Repeated monumental arch bay | 48–96 blocks | `EG-P04-S04-C0059` |
| Choked-route clear width | commonly 3–7 blocks, with passing niches and encounter chambers | `EG-P02-S02-C0028` |
| Surface wasteland share outside test regions | ≥ 70 % | `EG-P03-S05` seed sweep, `EG-P07-S02-C0103` |
| Vertical circulation cadence | a reachable up/down route at least every 48 blocks of horizontal travel inside a core | `EG-P04-S02-C0054` |

## 4. Traversal rhythm contract

The §2.2 grammar `constricted route -> readable threshold -> monumental release -> new
constricted network` is quantified as a **release cadence**:

- On any authored bottom-to-top route, the player meets a *monumental release* (a space
  whose smallest open dimension is ≥ 48 blocks, with a sightline ≥ 120 blocks) **no less
  often than every 2 bands and no more often than every half-band**.
- Every release is entered through a *readable threshold*: a framed portal, gate,
  bridgehead, or balcony that is visible from inside the preceding constricted network
  and telegraphs the release beyond it.
- No constricted network longer than ~140 blocks of continuous travel without either a
  release or a *passing chamber* (a local widening ≥ 12 blocks with a landmark, light
  change, or encounter).
- Unbroken corridor and unbroken megacavern both **fail** the rhythm check
  (`EG-P02-S05-C0033`, `EG-P02-S05-C0034`).

## 5. Consistency check

| Check | Result |
|---|---|
| Bands tile `-64..319` with no gap or overlap | PASS — 32 + 80 + 64 + 80 + 64 + 64 = 384 = height of the `-64..319` envelope |
| Band count matches §2.1 "distinct vertical strata" | PASS — 6 distinct strata |
| Band and field names avoid every C0003 prohibited term | PASS — verified against `docs/endgame/identity/placeholder-terms.md` |
| Wasteland dominance (§2.4) preserved | PASS — field 4 is the dominant field; ≥ 70 % target retained |
| Compression/release (§2.2) is measurable | PASS — §4 release cadence and threshold rule |
| Empty scale is authored (§2.3) | PASS — monumental voids are a reserved field feature, not absence of generation (`EG-P03-S04-C0043`) |
| Numbers stay provisional (Phase 0 rule) | PASS — every metric names a later proving checkpoint |
| No architecture, palette, or height number chosen here | PASS — deferred to C0005 / C0006 and Phase 2/4 |

## 6. Deferred

Exact core geometry, arch spans, and void shapes → Phase 3/4. Numeric height envelope
→ C0006. Fog and sightline distances per band → `EG-P05-S04-C0076`. The greybox
measurement kit and camera list → `EG-P02-S01-C0026` / `EG-P02-S01-C0025`.

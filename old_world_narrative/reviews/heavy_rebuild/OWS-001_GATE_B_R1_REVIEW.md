# [SYSTEM REPORT] OWS-001 — Gate B r1 Intact-State Review

## Decision

**REVISION REQUIRED. Gate B remains closed.**

The first D0 intact/normal-operation model is materially stronger than the historical grocery-derived baseline and it preserves the approved Gate-A r2 massing. It is not yet a believable fully operational Verdant Continuum Foods Neighborhood Culture Service Depot, however. Four hard architectural defects are visible in the authored model and must be corrected before historical anomaly or damage work begins.

## Blocking findings

### 1. Culture-locker service lane is undersized

The model comments and Pass-8 circulation contract require a clear three-block staff/service lane through the primary culture-locker hero space. The actual r1 locker banks occupy x=21–22 and x=24–25 at repeated z rows, leaving only x=23 between them. That is a one-block aisle, not the required three-block operational clearance.

This is not a cosmetic issue. The hero space must read as a serviceable cold-chain workplace rather than a dense wall of coolers.

**Required r2 correction:** re-space the locker banks so the central maintenance/issue aisle remains at least three blocks clear, with depots/counters placed outside that clearance.

### 2. The central staff spine pinches at receiving

The D0 plan deliberately establishes x=17–19 as a three-block north/south staff spine. r1 receiving staging then places inbound crates/pallets across the south end of that route, reducing the approach through the receiving zone to roughly one usable block at the critical freight handoff.

The operational sequence is supposed to be legible as receiving -> batch/temperature check -> clean stock while staff circulation remains independent of staged freight.

**Required r2 correction:** move receiving pallets/crates to explicit west/east staging pockets and preserve the full three-block staff spine through the receiving threshold.

### 3. Roof maintenance access is physically incomplete

The east service ladder currently runs only from y=2 through y=8 while the cold-chain block has a solid roof plane at y=9. There is no roof hatch/opening at the ladder head. In normal operation the ladder therefore terminates into the ceiling rather than providing the promised staff-only route to the refrigeration plant.

**Required r2 correction:** provide a real roof penetration/hatch landing and safe rooftop service pad tied to the approved roof plant.

### 4. Wall-sign placement is not physically supported

`base.wall_sign()` places the wall-sign block at the supplied coordinate. Several r1 signs are written directly into wall-plane coordinates—for example the primary corporate signs at z=3 on the public pavilion wall. Because the pavilion interior immediately behind those positions is air, placing the sign at the wall coordinate replaces its support block instead of mounting the sign to it.

The heavy-rebuild doctrine requires purpose-driven signage that survives as real architecture, not labels that only exist in source intent.

**Required r2 correction:** place wall signs one block in front of their supporting wall faces and verify the facing direction against the actual exterior/interior wall orientation. Do the same audit for every operational sign in OWS-001.

## Non-blocking observations carried forward

- Gate-A r2 massing remains accepted; this review does **not** reopen the 39x13x33 envelope.
- The D0 clean-versus-return zoning concept remains valid.
- The public pavilion, rear freight bay, east cold-chain mass and west returns annex remain the right high-level composition.
- Rooftop refrigeration is now functionally motivated, but its access and final pipe/support presentation still need the r2 correction above.
- Sign vocabulary and corporate wording are appropriate; the failure is physical placement/support, not the VCF language itself.

## Gate rule

No D1 anomaly, emergency overlay, centuries-of-decay treatment, encounter dressing, loot architecture or D3 collapse work may begin until the intact r2 building is rendered and Gate B passes.

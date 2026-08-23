# [SYSTEM REPORT] OWS-008 Heavy-Rebuild Restart Dossier

**Target:** OWS-008 — Emergency Investigation & Persistence Lab  
**Institution:** Verdant Continuum Foods (VCF)  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Frozen Phase-0 source:** `e14b3f35306fc313e7ea9a114f2384696864533a`  
**Shipping structure:** `infinite_domain:old_world/ows_008_vcf_emergency_persistence_investigation_lab`  
**Shipping NBT:** `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_008_vcf_emergency_persistence_investigation_lab.nbt`  
**Donor:** `infinite_domain:mountain_biohazard_lab_clean_master`  
**Current dimensions:** 55 x 22 x 49  
**Narrative phase:** Active containment  
**Rarity / quality intensity:** Rare / Very High

## Canonical integration contract

The target is statically implemented and staged out of natural worldgen. Its functional contract must survive a later architectural rebuild:

- guaranteed proof item: `kubejs:vcf_persistence_incident_file`;
- canonical structure loot table: `infinite_domain:chests/old_world/ows_008_vcf_emergency_persistence_investigation_lab`;
- proof container in the legacy implementation: X47/Y2/Z41;
- exploration quest: `4F58000000000008`;
- structure-detection task: `4F58100000000008`;
- proof task: `4F58200000000008`;
- locator command: `/structure_map infinite_domain:old_world/ows_008_vcf_emergency_persistence_investigation_lab 2`;
- major quest hook: `OWQ-09 — THE GREY BLOOM`, paired with OWS-047;
- reserved Darknet return: reopen the persistence-incident clean-room cache and compare suppressed breach chronology;
- narrative payload: a sterilized zone later tests positive inside a service joint, proving that repeated procedural changes cannot restore containment;
- runtime validation remains deferred and must not be inferred from static or visual work.

## Donor audit

The project-owned mountain-biohazard-lab donor is approved for modification and redistribution. It contributes unusually useful institutional bones for this target:

- a 55 x 22 x 49 rare-site envelope already organized as a pressure-zoned laboratory rather than a generic office box;
- four visibly stepped masses: north public/security intake, west two-level research wing, east containment wing and southwest utility/emergency annex;
- a real intake sequence with security/reception, lockers/changing and first-stage decontamination;
- sample receiving, wet laboratory, clinical/infirmary, preparation, cold-store, upper analysis, records and observation-control spaces;
- staged decontamination, a controlled east spine, observation-fronted quarantine rooms and a lead-lined specimen chamber;
- rear waste processing, filtration plant, east loading exit and a separate south emergency exit;
- two independent research stairs and an upper observation/data level;
- stepped roof forms, laboratory service monitors, shielded exhaust stacks, retaining shoulders and separate public/service site approaches.

These are valuable operational relationships, but they are not automatically a VCF persistence-investigation laboratory. The donor remains visually and programmatically a broad radiological/biohazard institution. Later passes must decide which pressure boundaries serve the persistence investigation, which remain generic donor residue and which must be rebuilt.

## Legacy shipping implementation audit

The exact shipping NBT is byte-identical to the `main` blob at the frozen source commit. It has the same 55 x 22 x 49 bounds as the donor. Direct decompressed comparison found:

- 13,212 non-air shipping positions versus 12,054 in the clean donor;
- 2,108 changed positions total;
- 1,258 additions, 100 removals and 750 replacements;
- 1,268 new/replacement framed-glass blocks;
- 287 yellow-concrete and 188 lime-concrete new/replacement blocks;
- 143 crate, 54 fluid-pipe, 12 mycelium and four mushroom new/replacement blocks;
- one deterministic proof chest.

The target descriptor separately reports 30,720 placed entries, 69 palette states, 9,118 modded entries, 37 working doors, no orphan door halves, 84 functional fixtures, a 16-block vertical-access span and structural lint passed. Those mechanical facts are useful but do not constitute quality approval.

The OWS-specific overlay currently consists chiefly of:

1. white/lime facade bands at the north frontage;
2. four large framed-glass boxes inserted across the lower research/containment plan;
3. one narrow yellow service strip and pipe run behind each box;
4. a small mycelium seam and mushroom inside each repeated bay;
5. a long yellow floor band and single pipe line across the rear interior;
6. four paired lime equipment blocks and crate stacks;
7. the deterministic proof chest near X47/Y2/Z41.

The overlay preserves proof and creates a visible clean-zone motif, but it is a thin intervention relative to the donor. It does not yet prove an actual investigation workflow, repeated clean-to-dirty boundary testing, causal service-joint contamination, sterilization plant capacity or incident-command/records architecture.

## Provisional donor disposition

Retain for independent baseline review and later Passes 2–5 study:

- the overall rare-site scale as the initial study envelope;
- the public intake -> changing/decon -> research/containment pressure sequence;
- the stepped public, research, containment and utility/service masses;
- upper analysis/records and two-stair circulation potential;
- quarantine observation and specimen-chamber concepts;
- rear filtration, waste, loading and independent emergency-egress relationships;
- the idea of repeated investigation bays and a deliberately exposed service-joint failure;
- deterministic proof/loot identity and every quest/worldgen ID.

Rebuild or fundamentally reinterpret:

- radiological/clinical donor identity that conflicts with a VCF-led fungal persistence investigation;
- VCF identity currently limited to thin applied color bands;
- four nearly identical glass boxes that erase useful donor rooms but lack credible vestibules, pass-throughs, controls and independently serviced clean states;
- clean/dirty material flow, specimen custody, sterilization validation and failed-zone isolation;
- mechanical plant serving air, wash, sterilant, drainage and service-joint inspection;
- investigation-command, comparative results and secure incident-record architecture;
- the generic roof field, which does not explain intake/exhaust segregation or decontamination utilities;
- public, staff, sample, waste and emergency threshold expression where the exterior still reads as the donor;
- the proof location if later adjacency planning shows it is not a plausible incident archive or clean-room cache.

## Target-local planning constraints

OWS-008 is not a normal-operation VCF product lab and must not duplicate OWS-006 or OWS-007. Its intact Gate-B state will represent a professional facility already converted into emergency investigation duty. The architecture must communicate repeated attempts to answer one question: why does a sterilized zone become positive again?

Later planning must make the following distinguishable before damage obscures them:

- contaminated specimen intake and custody;
- dirty-side examination and initial neutralization;
- staged personnel/material decontamination;
- sterilization treatment rooms with separately monitored cycles;
- clean-room hold and post-treatment verification;
- controlled persistence challenge/testing;
- exposed service-wall/joint inspection access;
- retained samples, comparative results and incident chronology;
- air/wash/sterilant/drainage plant with service access;
- investigation command and secure archive;
- waste hold/removal that does not cross the clean chain.

The crisis story must be legible as successive professional interventions being defeated, not as random mushrooms added to a laboratory. D0/Gate B should preserve the complete emergency operating architecture. D1 and later states may then show repeated seals, added barriers, opened service cavities and contamination recurring behind them.

## Live doctrine hold

The exact shipping baseline was rendered into fixed-camera set `ows008_fixed_v1` and independently reviewed as **REBUILD REQUIRED**. Passes 2–6 then produced a replacement D0 massing model. Independent Gate-A r1 review **PASSED** that exact model and froze its nine accepted macro aspects.

Passes 7–12 were implemented in the target-local Gate-B r1 review model and independently **PASSED**. That decision freezes the intact architecture, threshold hierarchy, pressure/circulation boundaries, distinct Cells A–D, inspection spine, connected services, west command relationship and VCF/emergency identity.

Passes 13–18 were implemented in the target-local Gate-C r1 D0/D1/D3 set and independently **PASSED**. That decision freezes the accepted D3 recurrence path, local roof/canopy failures, proof, encounters, preserved routes and restrained damage footprint.

Pass 19 is now implemented in `scripts/old_world_ows008_final.py`. Its pure `build_accepted_d3()` reproduces the accepted D3 SHA-256 exactly; `build_008()` adds eight localized recurrence/moisture details and no other geometry changes. Normal door stabilization is a no-op.

Authoritative import/dispatch integration and shipping generation are complete. Gate-D r1 proves exact canonical builder-to-shipping serialized and decompressed equality, renders the actual shipping NBT with `ows008_fixed_v1`, and passes target-local mechanical and image-regression guards. Independent visual review, Pass 20, quality scoring and promotion remain coordinator-owned and incomplete.

**CURRENT HOLD: GATE D r1 REVIEW NEEDED — INDEPENDENT VISUAL DECISION REQUIRED.**

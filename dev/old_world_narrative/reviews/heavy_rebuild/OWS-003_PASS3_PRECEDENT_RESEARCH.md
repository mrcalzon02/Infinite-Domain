# [SYSTEM REPORT] OWS-003 Pass 3 — Real-World Precedent Research

**Target:** OWS-003 — Verdant Continuum Foods Cold-Chain Culture Nursery  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Research date:** 2026-08-21  
**Status:** COMPLETE

## Research objective

The goal is not to find a real facility identical to Evercrop culture logistics. The goal is to extract credible operational and architectural principles from real systems that manage valuable temperature-sensitive biological material.

The precedent set focuses on:

- time/temperature-sensitive warehousing;
- biological/genetic-resource storage;
- intake inspection and excursion handling;
- batch/accession identity and documentation;
- controlled release and distribution;
- long-duration preservation infrastructure;
- emergency handling when storage integrity becomes questionable.

## Precedent A — WHO time- and temperature-sensitive storage/distribution

**Source:** World Health Organization, *TRS 961 — Annex 9: Model guidance for the storage and transport of time- and temperature-sensitive pharmaceutical products*.  
**Reference:** https://www.who.int/publications/m/item/trs961-annex9-modelguidanceforstoragetransport

WHO describes the guidance as setting principal requirements for safe storage and distribution of time- and temperature-sensitive products across regulated logistics systems.

### Architectural lesson

A temperature-controlled warehouse is not merely a room with refrigeration.

Its building must support:

- controlled receiving;
- monitored temperature zones;
- disciplined storage;
- protected staging;
- distribution handoff;
- equipment/plant capable of maintaining the environmental envelope;
- procedures for stock whose condition is uncertain.

### OWS-003 translation

- receiving should be a complete threshold, not an exterior door directly into the nursery;
- inbound loads should reach an intake/condition-check node before general storage;
- main cold storage should be architecturally separated from loading exposure;
- outbound cold staging should sit immediately upstream of dispatch;
- refrigeration/environmental plant must be visibly substantial enough to serve the building;
- maintenance access and monitoring should be part of the architecture.

## Precedent B — FAO Genebank Standards: preservation + identity + access

**Source:** Food and Agriculture Organization of the United Nations, *Genebank Standards for Plant Genetic Resources for Food and Agriculture*, revised edition 2014.  
**Reference:** https://www.fao.org/4/i3704e/i3704e.pdf

The FAO standards organize genebank work around acquisition, storage, viability monitoring, documentation, distribution/exchange, security and safety duplication. They explicitly treat preservation of identity, viability/genetic integrity and access as common operating principles.

The standards also emphasize that effective use depends on a chain connecting stored genetic resources to users, and that proper identification depends on careful documentation through storage and distribution.

### Architectural lesson

A biological-stock repository needs **records architecture** as much as storage architecture.

The physical material and its identity cannot be separated operationally.

### OWS-003 translation

- every nursery/cold-vault bay should read as batch-addressable rather than anonymous refrigeration;
- a batch-control / licensing-records node belongs close to release and dispatch decisions;
- monitoring stations should be distributed where staff can actually inspect storage conditions;
- destination authorization and physical dispatch should be adjacent processes;
- the proof/lore documents belong naturally in the release/licensing control area;
- storage should include clear distinction between active/released stock and material requiring additional review.

## Precedent C — FAO viability monitoring and active collection management

**Source:** FAO Genebank Standards, viability-monitoring sections.  
**Reference:** https://www.fao.org/4/i3704e/i3704e.pdf

FAO treats monitoring as active management rather than passive preservation. Stored accessions are periodically checked, and monitoring intervals change when deterioration is detected.

### Architectural lesson

Long-term biological storage requires staff to **reach, sample and monitor** stored material without destroying the storage system's organization.

### OWS-003 translation

- cold-vault and nursery layouts need real service aisles;
- representative batch inspection should have a dedicated operational QA position;
- environmental-monitoring points should be visible at room/cell thresholds;
- the later D1 anomaly can credibly increase inspection frequency and move selected batches into temporary hold without changing the facility into a research lab.

## Precedent D — CDC receiving and temperature-excursion handling

**Source:** U.S. Centers for Disease Control and Prevention, *Pink Book — Chapter 5: Vaccine Storage and Handling*.  
**Reference:** https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-5-vaccine-storage-and-handling.html

CDC guidance requires prompt handling of incoming temperature-sensitive deliveries. Shipment condition and packing information are checked on receipt. When a temperature excursion is suspected, affected stock is labeled not for use and stored separately from other stock until viability is determined.

### Architectural lesson

A temperature excursion creates an **exception state**, not instant disposal and not continued normal circulation.

That exception state needs a place.

### OWS-003 translation

- receiving must immediately connect to batch/condition inspection;
- quality hold should be physically separate but still temperature controlled;
- suspect batches need visible temporary labels/routing rather than generic hazard decoration;
- the early anomaly should increase the amount of segregated stock, replacement seal material and inspection activity;
- normal stock should still continue through the facility around the bounded exception.

## Precedent E — ATCC culture preservation and storage integrity

**Sources:** American Type Culture Collection culture-preservation guidance.  
**References:**  
https://www.atcc.org/resources/culture-guides/bacteriology-culture-guide  
https://www.atcc.org/resources/culture-guides/mycology-culture-guide  
https://www.atcc.org/resources/technical-documents/cryogenic-storage-of-animal-cells

ATCC's culture guidance shows that biological cultures may require very different preservation states depending on preparation, including refrigerated freeze-dried material, low-temperature mechanical storage and cryogenic storage. It also emphasizes controlled freezing, appropriate containers, temperature alarms, durable labeling and records.

Of particular narrative relevance, ATCC notes that some internally threaded cryovials depend on silicone gaskets and that seal condition/tightening matters to leak performance.

### Architectural lesson

The storage container, seal, temperature regime and records system form one preservation system.

### OWS-003 translation

- the nursery should use more than one visual storage condition rather than repeating a single generic cooler wall everywhere;
- sealed batch cells, controlled freezer/cooler banks and monitored holding can create distinct room types;
- the material-anomaly story can focus on flexible seals/gaskets without claiming the cultures themselves are immediately defective;
- replacement seal stock and repacking positions belong near quality hold and release inspection;
- refrigeration failure alarms/monitoring and backup-service access are operationally justified details.

## Precedent F — FAO distribution/exchange and destination documentation

**Source:** FAO Genebank Standards, distribution/exchange and documentation sections.  
**Reference:** https://www.fao.org/4/i3704e/i3704e.pdf

FAO's standards treat distribution as a documented process connected to destination requirements, permissions and the identity of the material being transferred.

### Architectural lesson

Global biological distribution is not ordinary anonymous freight.

The outgoing shipment needs to be tied to:

- identity;
- destination;
- permission/documentation;
- handling condition;
- release status.

### OWS-003 translation

- the licensing brief should sit in the same operational neighborhood as outbound batch release;
- packing should use destination/batch lanes rather than one undifferentiated pile of crates;
- dispatch staging can be organized by region/license class;
- the facility can tell the global-distribution story visually through labeled shipping racks and route boards before the player reads the lore document.

## Combined design rules derived from precedent

1. **Cold-chain receiving is a controlled threshold.** Exterior freight does not open directly into the main nursery.
2. **Identity follows material.** Batch labels, records and physical storage positions must correspond.
3. **Suspect stock is separated, not forgotten.** Quality hold remains conditioned and operationally connected to inspection.
4. **Storage is actively monitored.** Service aisles, monitoring points and inspection access are mandatory.
5. **The nursery must contain several preservation states.** A large biological-stock facility should not be represented by four identical cooler strips.
6. **Release is a decision point.** Inspection and licensing/routing occur before conditioned packing and dispatch.
7. **Outbound logistics remain temperature controlled until handoff.** Packing, outbound cold staging and dispatch are distinct.
8. **Refrigeration plant is major architecture.** The size of the plant and service network must match the amount of conditioned space.
9. **Seal/gasket failure is a credible early anomaly.** It can increase inspections, replacement stock and rerouting while the system remains broadly operational.
10. **Adaptive reuse should remain visible.** The former cannery can survive as older brick massing while VCF cold rooms, clean service inserts and plant visibly belong to a later conversion.
11. **Documentation is not office filler.** The proof/lore node should physically control release and destination routing.
12. **The player should infer a global biological distribution network from architecture before reading the documents.**

## Pass 3 decision

**PRECEDENT RESEARCH: COMPLETE.**

The next valid stage is Pass 4: translate the functional sequence and precedent-derived rules into a program/adjacency plan inside the retained 59 x 24 x 51 study envelope.
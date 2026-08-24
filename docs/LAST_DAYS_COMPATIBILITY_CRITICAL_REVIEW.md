# LAST DAYS compatibility critical review

## Review protocol

Every new compatibility family begins with one representative asset and remains unpropagated until it passes all gates below.

1. **Authority:** actual model, block state, texture path, source dimensions, alpha, animation, and shared-use relationships are established.
2. **Object:** construction, materials, function, and gameplay markings are recorded before authoring.
3. **LAST DAYS references:** successful pack art is selected by material and construction, not merely palette.
4. **Native authorship:** the texture is authored directly at the installed source dimensions. Enlarged sheets are inspection-only.
5. **Geometry:** details support the mapped surface and do not cross unrelated UV islands.
6. **Material:** major materials remain distinct and physically plausible.
7. **Hierarchy:** silhouette and construction read before wear and fine detail.
8. **Restraint:** no generic rust, noise, scratches, or decorative rivet fields.
9. **Function:** states, ports, direction, motion, and inventory recognition remain legible.
10. **Technical:** dimensions, alpha, filenames, animation metadata, references, and ZIP contents validate.

## Candidate CR-001 — Immersive Engineering crate

- Status: **PASS — INSTALLED AS THE SIMPLE FULL-CUBE REFERENCE**
- Namespace: `immersiveengineering`
- Asset: `crate`
- Texture: `textures/block/wooden_device/crate.png`
- Model: `models/block/crate.json`
- Block state: `blockstates/crate.json`
- Mapping: `minecraft:block/cube_all`; the same opaque face is used on all six sides.
- Native dimensions: 16x16 RGBA, fully opaque.
- Object: rugged wooden shipping/storage crate with joined perimeter rails and crossed load bracing.
- LAST DAYS references: `oak_planks.png` for timber field; `barrel_side.png` and `crafting_table_front.png` for storage framing, recess depth, fasteners, and value hierarchy.
- Gameplay information: block identity is carried by the crate silhouette and crossed structural bracing; no ports, state colors, or animation exist.
- Production rule: one direct 16x16 candidate was previewed before installation. The first revision was rejected because its framing erased the timber field and read as schematic iconography. The second revision passed and alone was installed.

### Critical verdict

- Geometry: **PASS** — `cube_all` mapping is fully understood; the texture contains no face-specific markings that become incorrect when repeated.
- Material: **PASS** — the timber field comes from established LAST DAYS oak construction; frame, brace, fastener, and repair colors remain distinguishable.
- Hierarchy: **PASS** — perimeter frame and crossed load brace read first; plank variation and the repaired joint remain secondary.
- Restraint: **PASS** — no global recolor/noise/rust pass; fasteners appear only at joints and wear is confined to one replaced brace segment.
- Function: **PASS** — the crate remains immediately recognizable in block and inventory use.
- Originality: **PASS** — the native IE brown board artwork was replaced by a reconstructed LAST DAYS timber-and-frame face rather than filtered.
- Technical: **PASS** — 16x16, fully opaque, unchanged path and model reference; original retained at `backups/last-days-compatibility/immersiveengineering/crate-original.png`.
- Scope limitation: this proves only a simple full-cube storage-block method. It does not authorize directional-machine, multipart, connected, or animated propagation.

### Installed artifact

- SHA-256: `6b1ddc4720ff565ecf7eb91d1ea69d29c6ee7d743c7d5ce94a3578e499c355da`
- Review sheet order: original IE crate; LAST DAYS oak; LAST DAYS barrel; LAST DAYS crafting-table face; installed candidate.

## Candidate CR-002 — Immersive Engineering reinforced crate

- Status: **PASS — INSTALLED AS CONTROLLED SAME-MODEL PROPAGATION**
- Mapping: the same opaque 16x16 `cube_all` geometry as CR-001.
- Object: wooden shipping crate strengthened by a continuous steel perimeter, steel crossed load braces, joint fasteners, and one replacement segment.
- References: approved CR-001 crate for family construction; LAST DAYS spruce planks for protected timber infill; `iron_block.png` and `furnace_side.png` for steel value behavior.
- First preview: **REJECTED** because steel and timber collapsed into the same gray-green material family.
- Revision: **PASS** after restoring warmer protected timber pockets behind the gray steel structure.

### Critical verdict

- Geometry: **PASS** — identical proven `cube_all` mapping with no directional markings.
- Material: **PASS** — warm timber infill remains visibly separate from the steel frame and braces.
- Hierarchy: **PASS** — reinforcement reads before plank texture, fasteners, and localized repair.
- Restraint: **PASS** — no global damage pass; only joint hardware and one repaired brace segment are emphasized.
- Family coherence: **PASS** — construction follows CR-001 while the stronger material system remains immediately distinct.
- Technical: **PASS** — native 16x16, fully opaque, unchanged path; original retained at `backups/last-days-compatibility/immersiveengineering/reinforced-crate-original.png`.
- SHA-256: `9593b18174296810a11f0ae344b919ffc5821de9158d30623b665cdf3256e157`
- Scope limitation: this validates only the normal and reinforced crate pair. Festive variants remain untouched because their decorative/state requirements need separate review.

## CR-003 — Immersive Engineering kinetic dynamo

- Status: **PASS — THREE ACTIVE NATIVE 16x16 FACES INSTALLED**
- Model finding: north uses `dynamo_front`; east/west use `dynamo_side`; up/down/south use `dynamo_top`. `dynamo_bottom.png` is not referenced by the installed model and was left untouched.
- Front: octagonal copper field coil, steel bearing collar, and dark shaft bore preserve the kinetic connection.
- Side: copper windings remain exposed inside a framed service bay with a distinct laminated core.
- Shared face: quieter access plate remains suitable for top, bottom, and rear model use.
- Critical correction: the first front preview read as a square hatch and was revised before installation.
- Technical: all three files remain opaque 16x16; editable and active-ZIP hashes match; originals are backed up under `backups/last-days-compatibility/immersiveengineering/kinetic_dynamo`.

# Cross-Mod Recipe Integration Policy

Date: 2026-08-14

Cross-mod integration increases with technological maturity. Compression alone
changes cost; it does not count as functional cross-mod integration.

## Era 0 — Lost Survivors

Keep recipes legible, local, and survival-oriented. Vanilla, Primitive Start,
Wastelands, and Ex Deorum may meet at a few deliberately taught bridges, but an
ordinary tool should not require knowledge of several unrelated mods.

- Normal target: no foreign technology namespace.
- Exceptional target: one clearly explained bridge.
- Never use late processors, powered components, or hidden industrial chains.

## Era 1 — Mechanical Reconstruction

Use cross-mod ingredients sparingly and pedagogically. Create may connect to
Farmer's Delight, Sophisticated Storage, or regional materials when a quest
explicitly teaches that relationship.

- Normal target: zero or one meaningful foreign technology namespace.
- Cross-mod requirements must appear in a support quest before a capstone needs
  them.
- Do not turn introductory rotational components into opaque dependency knots.

## Eras 2–3 — Industrial coupling

Major machines and progression items must depend on at least one established
foreign industry. Heavy Industry and Petrochemical Civilization should exchange
steel, foundry parts, transport components, seals, pipes, fuels, and process
equipment in both directions.

- Target: at least one meaningful foreign technology namespace per major recipe.
- Prefer functional components over decorative tokens or arbitrary ingots.
- Recipes should express what the machine does: pressure equipment uses seals and
  pipes; extraction uses drills and structural frames; foundries use refractory
  and controlled-motion components.

## Eras 4–5 — Infrastructure systems

Electrical and automated machinery should combine mechanical fabrication,
electrical control, storage/logistics, computation, and appropriate materials.

- Target: at least two meaningful foreign technology namespaces per major recipe.
- Power consumers require a real electrical interface or energy component.
- Automated machines require control, logistics, or computation components—not
  merely redstone promoted to a larger block.
- AE2, Oritech, Power Grid, Create New Age, Create, and cybernetic manufacturing
  should form deliberate two-way bridges where their functions overlap.

## Eras 6–8 — Deep civilization integration

High-energy, nuclear, orbital, and Infinite Domain technology must be the output
of a mature multi-industry civilization.

- Target: at least three meaningful foreign technology namespaces per major
  recipe, or an equivalently deep multi-stage process.
- Nuclear systems require containment, control, power handling, material
  processing, and safety infrastructure.
- Orbital systems require life support, power, computation/navigation, structural
  materials, and logistics.
- Endgame devices should consume earlier systems as components where sensible;
  they must not reduce to eight rare ingots surrounding one mod-local part.

## What counts

Meaningful integration includes a functional component, machine subassembly,
processor, storage/logistics interface, power component, safety system, or
processed material whose originating industry is relevant to the output.

The following do **not** satisfy the integration target by themselves:

- Minecraft ingredients;
- common tags;
- AllTheCompressed blocks introduced by cost scaling;
- arbitrary decorative blocks from another namespace;
- a foreign ingot added only to increase the namespace count;
- contribution charters or Foundation Cores that merely summarize work already
  performed.

## Enforcement

`scripts/audit_era_recipe_integration.py` joins FTB Quests objective items to the
effective recipe index and reports shallow milestone recipes by era. Reports are
written to `docs/recipe-integration-audit/`. The audit is a triage tool: namespace
depth is measurable, but functional relevance still requires design review.

The audit grades the **weakest** effective recipe for an objective. One strong
recipe cannot conceal an easier alternate route. Early contribution items are
reported separately as branch aggregators; they may summarize several taught
systems without making ordinary onboarding hardware cross-mod dependent.

## Implemented gateway pass

`scripts/apply_deep_recipe_integrations.py` is the maintainable design source for
the curated gateway recipes. Run it after the compression generator. It validates
every ingredient against the installed item registry and overrides every recipe
ID that produces a selected output, preventing alternate-recipe bypasses.

The current pass covers 30 gateway outputs through 36 effective recipe IDs:

- Era 2: foundry crucible, blast stove, and mechanical saw;
- Era 3: distillation control, pumpjack well, and chemical vat;
- Era 4: motor, energy acceptance, circuit design, and advanced energising;
- Era 5: Inscriber, Assembler, Molecular Assembler, Pattern Provider, Crafting
  Terminal, Centrifuge, and Surgery Table;
- Era 6: both reactor controllers and radiation-protection module;
- Era 7: rocket engine, launch pad, oxygen distributor, nose cone, and fins;
- Era 8: Quantum Ring, Accelerator Controller, ME Drive, Dense Energy Cell, and
  256k Item Storage Cell.

These are gateway recipes, not an assertion that hay bales, food, raw ores,
fluid buckets, or every incidental quest hand-in needs cross-mod ingredients.
Remaining `SHALLOW` rows are the review queue for subsequent machine-level
passes; `NO_EFFECTIVE_RECIPE` commonly identifies processing outputs, fluids,
ores, or acquisition objectives rather than missing crafting recipes.

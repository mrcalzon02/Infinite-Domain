# Create Nuclear Phase I Investigation

## Installed baseline

- Exact build: `createnuclear-1.3.2-beta.3-neoforge.jar` for Minecraft 1.21.1 and Create 6.0.8+.
- The reactor blueprint remains a fixed 57-position pattern serialized as slot/item records plus uranium and graphite counts/timers.
- The controller evaluates exact `createnuclear:uranium_rod` and `createnuclear:graphite_rod` items, four orthogonal neighbors, signed heat, and a three-uranium-per-graphite overflow condition.
- Uranium and graphite lifetimes default to 3,600 ticks. Maximum heat is 1,000. The configured failure countdown is 600 ticks, preserving an observable intervention window.
- The reactor input exposes two item slots: uranium fuel and graphite. The output converts controller heat into generated rotational speed.
- The installed reactor output registers 10,240 SU of stress capacity per RPM, independently of its heat-to-RPM calculation.

## Phase boundary

KubeJS/datapacks can safely own ore drops, intermediates, fluids, Create recipes, bypass removal, quests, and JEI-visible guidance. They cannot make new rod classes behave differently because the installed controller and input inventory check exact items and hardcode uranium/graphite behavior. Generalized component profiles therefore belong to a compiled Phase II patch.

## Output scaling trial

The installed 10,240 SU-per-RPM reactor-output capacity is overridden to 1,024, a 90% reduction. Reactor heat, heat thresholds, generated RPM, fuel lifetime, cooling behavior, and failure timing are unchanged. The value is centralized as `reactorOutput.stressCapacityPerRpm` in `nuclear_fuel_cycle.json` and can be tuned without rebuilding the addon.

## Implemented uranium factory

`kubejs:uranium_mineral_trace` -> `kubejs:uranium_bearing_fines` -> `kubejs:washed_uranium_concentrate` -> `kubejs:leached_uranium_slurry` -> `kubejs:purified_uranium_compound` -> `kubejs:fuel_grade_uranium_powder` -> `kubejs:green_fuel_pellet` -> `kubejs:fired_fuel_pellet` -> `kubejs:fuel_pellet_stack` -> `kubejs:incomplete_standard_fuel_rod` -> `createnuclear:uranium_rod`

One nine-trace chemical batch produces four purified compounds. Each compound yields two powder charges, creating the eight pellets required for one standard rod. The chain consumes the established kelp-derived chelating broth and saponified botanical binder and produces contained tailings plus spent solution.

## Implemented graphite factory

Coal/charcoal -> `kubejs:carbon_fines` -> `kubejs:washed_carbon` -> `kubejs:refined_reactor_carbon` -> `kubejs:bound_graphite_mix` -> `kubejs:green_graphite_blank` -> `kubejs:baked_graphite_blank` -> `kubejs:purified_graphite_blank` -> `kubejs:nuclear_graphite_component` -> `createnuclear:graphite_rod`

The graphite line reuses tannic pulp as a renewable binder, then washes, bakes, chemically purifies, machines, and mechanically frames the material. Phase I retains the installed rod's legacy cooling behavior; Phase II will reclassify it as moderation.

## Bypass policy

The installed crushed-uranium, liquid-uranium, yellowcake, fan-enrichment, direct rod, coal-dust, graphene, and direct graphite-rod recipes are removed. Ore, raw uranium, raw blocks, and crushed uranium cannot output raw uranium, uranium dust, yellowcake, enriched yellowcake, or a finished Create Nuclear rod.

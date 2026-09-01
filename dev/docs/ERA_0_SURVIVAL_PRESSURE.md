# Era 0 Survival Pressure

Era 0 is intended to be materially starved, dangerous, and deliberately inefficient. Players should shelter in holes, mud huts, and scavenged structures while extracting marginal value from dirt, refuse, bones, and undead remains.

## Active pressure rules

- Vanilla zombies, zombie villagers, skeletons, strays, bogged, and phantoms do not burn away merely because daylight arrives.
- Mutant zombie natural-spawn weight is increased from 0.05 to 0.25, a fivefold first-pass increase.
- Spore structures are allowed across the custom wasteland surface biomes instead of depending primarily on isolated vanilla biomes.
- Every Spore landmark family receives three concentric-ring candidates in its assigned radial band. In addition, general surface sites receive a 42/16 random-spread pool, cold mines receive an 84/30 scatter set, and frozen-ocean iceberg mines receive a 96/34 scatter set. Surface structures blend into terrain; buried facilities use buried terrain adaptation.
- Primitive Start bone equipment is the intended first practical tool family.
- Vanilla wood, stone, gold, iron, and diamond tools remain one-durability crafting placeholders.
- Ex Deorum remains a painfully slow emergency resource path.

## Performance guardrails

Mutant zombies are increased incrementally rather than set near the configuration maximum. Daylight persistence does not itself add entities; it removes daytime attrition, so loaded-area hostile populations should be monitored during testing. Spore structure changes affect newly generated chunks only and require qualifying biomes.

// Non-destructive safety net for third-party recipe collisions. We never
// remove or override another mod's recipe here - only add an alternate
// path on a different machine/recipe type so a shadowed output stays
// reachable no matter which of the colliding recipes the game happens
// to pick. See docs/recipe-integration-audit for the collision writeup.

ServerEvents.recipes(event => {
    // create:crushing/limestone (tfmg, unconditioned) and
    // create_ultimate_factory:compat/tfmg_crushing_limestone (also
    // unconditioned once tfmg is loaded) both match create:limestone.
    // Whichever the recipe manager doesn't pick, its Quartz/Lapis bonus
    // becomes unreachable. Reproduce the full set via Basin + Mechanical
    // Mixer instead of touching either mod's recipe.
    event.recipes.create.mixing([
        Item.of('tfmg:limesand'),
        CreateItem.of('minecraft:quartz', 0.125),
        CreateItem.of('minecraft:lapis_lazuli', 0.08)
    ], [Item.of('create:limestone'), Fluid.of('minecraft:water', 250)])
        .id('infinite_domain:compat_patch/limestone_mineral_wash')
})

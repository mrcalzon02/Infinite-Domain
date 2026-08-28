// Endgame EG-P06-S01-C0084 - shared entrance/return portal assembly.
(() => {
    function portalAssembly(scene, util) {
        const base = [0, 0, 0, 6, 0, 4]
        const core = [2, 1, 2]
        const portalCenter = [3.0, 3.0, 2.5]

        scene.scaleSceneView(0.78)
        scene.setSceneOffsetY(-1)
        scene.world.setBlocks(base, 'minecraft:polished_deepslate', false)
        scene.showStructure()
        scene.idle(12)

        scene.text(75, 'Build a vertical 4 x 5 frame: the minimum Nether Portal footprint.', [3.0, 1.2, 2.5])
            .colored(PonderPalette.INPUT)
            .placeNearTarget()
            .attachKeyFrame()
        scene.world.setBlocks([1, 1, 2, 4, 1, 2], 'kubejs:cinderstack_portal_frame', false)
        scene.idle(80)

        scene.text(70, 'Replace either lower inner block with the endgame Portal Core.', [2.5, 2.2, 2.5])
            .colored(PonderPalette.INPUT)
            .placeNearTarget()
            .attachKeyFrame()
        scene.world.setBlock(core, 'kubejs:cinderstack_portal_core', false)
        scene.showControls(45, [2.5, 2.2, 2.5], 'down')
            .withItem('kubejs:cinderstack_portal_core')
        scene.idle(80)

        scene.text(65, 'Raise three-block Portal Frame pillars at both ends.', portalCenter)
            .colored(PonderPalette.BLUE)
            .placeNearTarget()
            .attachKeyFrame()
        scene.world.setBlocks([1, 2, 2, 1, 4, 2], 'kubejs:cinderstack_portal_frame', false)
        scene.world.setBlocks([4, 2, 2, 4, 4, 2], 'kubejs:cinderstack_portal_frame', false)
        scene.idle(75)

        scene.text(70, 'Close the arch, leaving a 2 x 3 walk-through opening.', [3.0, 5.3, 2.5])
            .colored(PonderPalette.BLUE)
            .placeNearTarget()
            .attachKeyFrame()
        scene.world.setBlocks([1, 5, 2, 4, 5, 2], 'kubejs:cinderstack_portal_frame', false)
        scene.idle(75)

        scene.text(75, 'Replace all four corners with Portal Actuators.', portalCenter)
            .colored(PonderPalette.INPUT)
            .placeNearTarget()
            .attachKeyFrame()
        scene.world.setBlock([1, 1, 2], 'kubejs:cinderstack_portal_actuator', false)
        scene.world.setBlock([4, 1, 2], 'kubejs:cinderstack_portal_actuator', false)
        scene.world.setBlock([1, 5, 2], 'kubejs:cinderstack_portal_actuator', false)
        scene.world.setBlock([4, 5, 2], 'kubejs:cinderstack_portal_actuator', false)
        scene.showControls(45, [1.5, 5.5, 2.5], 'down')
            .withItem('kubejs:cinderstack_portal_actuator')
        scene.idle(85)

        scene.text(85, 'Like a Nether Portal, larger frames may be up to 23 x 23 and may face either axis.', portalCenter)
            .colored(PonderPalette.MEDIUM)
            .placeNearTarget()
            .attachKeyFrame()
        scene.idle(90)

        scene.text(80, 'Use either Cinderstack marker on the Portal Core in the lower edge.', [2.5, 2.0, 2.5])
            .colored(PonderPalette.OUTPUT)
            .placeNearTarget()
            .attachKeyFrame()
        scene.showControls(55, [2.5, 2.2, 2.5], 'down')
            .rightClick()
            .withItem('kubejs:cinderstack_marker')
        scene.idle(65)

        scene.world.setBlocks([2, 2, 2, 3, 4, 2], 'kubejs:cinderstack_portal_field', false)
        scene.text(80, 'The core projects an End-Portal-textured field across the opening.', portalCenter)
            .colored(PonderPalette.OUTPUT)
            .placeNearTarget()
            .attachKeyFrame()
        scene.idle(90)
    }

    Ponder.registry(event => {
        event
            .create('kubejs:cinderstack_marker')
            .scene('cinderstack_portal_assembly', 'Assembling a Cinderstack Portal', portalAssembly)
        event
            .create('kubejs:cinderstack_return_marker')
            .scene('cinderstack_return_portal_assembly', 'Assembling a Cinderstack Portal', portalAssembly)
    })
})()

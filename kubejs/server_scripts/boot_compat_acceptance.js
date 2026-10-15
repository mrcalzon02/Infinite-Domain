// Inert outside the isolated dimension-audit run. Exercise a real entity,
// without spawning a mob into the world or altering the player's save.
ServerEvents.loaded(event => {
    const config = JsonIO.read('kubejs/config/worldgen_benchmark.json')
    if (!config || config.enabled !== true || String(config.suite) !== 'dimension_audit') return
    // Rhino can redeclare native-class locals when they are const-bound inside
    // a try block. Use function-scope bindings, as the benchmark controller does.
    let bootAcceptanceRegistry, bootAcceptanceLocation, bootAcceptanceAttributes
    let bootAcceptanceType, bootAcceptanceEntity, bootAcceptanceHealth
    let bootAcceptanceAttack, bootAcceptanceSpeed
    try {
        bootAcceptanceRegistry = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
        bootAcceptanceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
        bootAcceptanceAttributes = Java.loadClass('net.minecraft.world.entity.ai.attributes.Attributes')
        bootAcceptanceType = bootAcceptanceRegistry.ENTITY_TYPE.get(bootAcceptanceLocation.parse('jaffabricate:orange_jelly_slime'))
        bootAcceptanceEntity = bootAcceptanceType.create(event.server.overworld())
        if (!bootAcceptanceEntity) throw new Error('Orange Jelly Slime construction returned null')
        bootAcceptanceEntity.setSize(2, true)
        bootAcceptanceHealth = bootAcceptanceEntity.getMaxHealth()
        bootAcceptanceAttack = bootAcceptanceEntity.getAttribute(bootAcceptanceAttributes.ATTACK_DAMAGE).getBaseValue()
        bootAcceptanceSpeed = bootAcceptanceEntity.getAttribute(bootAcceptanceAttributes.MOVEMENT_SPEED).getBaseValue()
        if (bootAcceptanceHealth !== 4 || bootAcceptanceAttack !== 2 || Math.abs(bootAcceptanceSpeed - 0.4) > 0.0001) {
            throw new Error('Unexpected size-two attributes: ' + bootAcceptanceHealth + '/' + bootAcceptanceAttack + '/' + bootAcceptanceSpeed)
        }
        bootAcceptanceEntity.discard()
        console.info('[ID-BOOT-ACCEPTANCE] ' + JSON.stringify({
            entity: 'jaffabricate:orange_jelly_slime', constructed: true,
            size: 2, health: bootAcceptanceHealth, attack: bootAcceptanceAttack, speed: bootAcceptanceSpeed, passed: true
        }))
    } catch (error) {
        console.error('[ID-BOOT-ACCEPTANCE] Jelly attribute acceptance FAILED: ' + error)
    }
})

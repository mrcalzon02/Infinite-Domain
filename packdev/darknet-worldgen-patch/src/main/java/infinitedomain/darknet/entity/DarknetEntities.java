package infinitedomain.darknet.entity;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import infinitedomain.darknet.DarknetWorldgenPatch;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.event.entity.RegisterSpawnPlacementsEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class DarknetEntities {
    private static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(Registries.ENTITY_TYPE, DarknetWorldgenPatch.MOD_ID);
    public static final DeferredHolder<EntityType<?>, EntityType<DatavoreDragon>> DATAVORE_DRAGON = ENTITIES.register(
        "datavore_dragon",
        () -> EntityType.Builder.of(DatavoreDragon::new, MobCategory.MONSTER)
            .sized(2.0F, 2.0F).clientTrackingRange(16).updateInterval(2).canSpawnFarFromPlayer()
            .build(DarknetWorldgenPatch.MOD_ID + ":datavore_dragon")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetTrader>> DARKNET_TRADER = ENTITIES.register(
        "darknet_trader",
        () -> EntityType.Builder.of(DarknetTrader::new, MobCategory.CREATURE)
            .sized(0.6F, 1.95F).clientTrackingRange(10).updateInterval(3)
            .build(DarknetWorldgenPatch.MOD_ID + ":darknet_trader")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetRabbit>> DARKNET_RABBIT = ENTITIES.register(
        "darknet_rabbit", () -> EntityType.Builder.of(DarknetRabbit::new, MobCategory.CREATURE)
            .sized(0.4F, 0.5F).clientTrackingRange(8).build(DarknetWorldgenPatch.MOD_ID + ":darknet_rabbit")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetCow>> DARKNET_COW = ENTITIES.register(
        "darknet_cow", () -> EntityType.Builder.of(DarknetCow::new, MobCategory.CREATURE)
            .sized(0.9F, 1.4F).clientTrackingRange(10).build(DarknetWorldgenPatch.MOD_ID + ":darknet_cow")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetWolf>> DARKNET_HOUND = ENTITIES.register(
        "darknet_hound", () -> EntityType.Builder.of(DarknetWolf::new, MobCategory.CREATURE)
            .sized(0.6F, 0.85F).clientTrackingRange(10).build(DarknetWorldgenPatch.MOD_ID + ":darknet_hound")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetFox>> DARKNET_FOX = ENTITIES.register(
        "darknet_fox", () -> EntityType.Builder.of(DarknetFox::new, MobCategory.CREATURE)
            .sized(0.6F, 0.7F).clientTrackingRange(10).build(DarknetWorldgenPatch.MOD_ID + ":darknet_fox")
    );
    public static final DeferredHolder<EntityType<?>, EntityType<DarknetSlime>> DARKNET_SLIME = ENTITIES.register(
        "darknet_slime", () -> EntityType.Builder.of(DarknetSlime::new, MobCategory.MONSTER)
            .sized(0.52F, 0.52F).clientTrackingRange(10).build(DarknetWorldgenPatch.MOD_ID + ":darknet_slime")
    );

    private DarknetEntities() {}

    public static void register(IEventBus bus) {
        ENTITIES.register(bus);
        bus.addListener(DarknetEntities::createAttributes);
        bus.addListener(DarknetEntities::registerSpawnPlacement);
    }

    private static void createAttributes(EntityAttributeCreationEvent event) {
        event.put(DATAVORE_DRAGON.get(), EntityDragonBase.bakeDragonAttributes(1000.0, 0.35, 40.0, 20.0).build());
        event.put(DARKNET_TRADER.get(), Mob.createMobAttributes()
            .add(Attributes.MAX_HEALTH, 60.0)
            .add(Attributes.MOVEMENT_SPEED, 0.5)
            .add(Attributes.FOLLOW_RANGE, 48.0)
            .add(Attributes.ARMOR, 12.0)
            .add(Attributes.KNOCKBACK_RESISTANCE, 0.5)
            .build());
        event.put(DARKNET_RABBIT.get(), DarknetRabbit.createAttributes().build());
        event.put(DARKNET_COW.get(), DarknetCow.createAttributes().build());
        event.put(DARKNET_HOUND.get(), DarknetWolf.createAttributes().build());
        event.put(DARKNET_FOX.get(), DarknetFox.createAttributes().build());
        event.put(DARKNET_SLIME.get(), Monster.createMonsterAttributes().build());
    }

    private static void registerSpawnPlacement(RegisterSpawnPlacementsEvent event) {
        event.register(DATAVORE_DRAGON.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DatavoreDragon::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_TRADER.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetTrader::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_RABBIT.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetFaunaRules::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_COW.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetFaunaRules::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_HOUND.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetFaunaRules::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_FOX.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetFaunaRules::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
        event.register(DARKNET_SLIME.get(), SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
            DarknetFaunaRules::canSpawn, RegisterSpawnPlacementsEvent.Operation.REPLACE);
    }
}

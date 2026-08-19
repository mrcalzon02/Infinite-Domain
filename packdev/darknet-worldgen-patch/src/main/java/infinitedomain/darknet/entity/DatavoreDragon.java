package infinitedomain.darknet.entity;

import com.github.alexthe666.iceandfire.entity.EntityLightningDragon;
import infinitedomain.darknet.DarknetGuard;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.AABB;

public final class DatavoreDragon extends EntityLightningDragon {
    public static final double MAX_HEALTH = 1000.0;
    public static final int MIN_RADIUS = 2800;
    public static final int MAX_RADIUS = 3600;
    private static final ResourceLocation LOOT = ResourceLocation.fromNamespaceAndPath("infinite_domain", "entities/datavore_dragon");

    private final ServerBossEvent bossEvent = createBossEvent();

    private static ServerBossEvent createBossEvent() {
        ServerBossEvent event = new ServerBossEvent(
            Component.translatable("entity.infinite_domain_darknet_worldgen.datavore_dragon"),
            BossEvent.BossBarColor.RED,
            BossEvent.BossBarOverlay.NOTCHED_20
        );
        event.setDarkenScreen(true);
        event.setPlayBossMusic(true);
        return event;
    }

    public DatavoreDragon(EntityType<? extends DatavoreDragon> type, Level level) {
        super(type, level);
        setAgeInDays(125);
        setMale(false);
        setVariant(3);
        setPersistenceRequired();
    }

    public static boolean canSpawn(EntityType<DatavoreDragon> type, ServerLevelAccessor level, MobSpawnType reason,
                                   BlockPos pos, RandomSource random) {
        if (!DarknetGuard.isDarknet(level.getLevel())) return false;
        long distanceSquared = (long) pos.getX() * pos.getX() + (long) pos.getZ() * pos.getZ();
        if (distanceSquared < (long) MIN_RADIUS * MIN_RADIUS || distanceSquared > (long) MAX_RADIUS * MAX_RADIUS) return false;
        return level.getLevel().getEntitiesOfClass(DatavoreDragon.class, new AABB(pos).inflate(512.0)).isEmpty();
    }

    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType reason,
                                        SpawnGroupData spawnData) {
        SpawnGroupData result = super.finalizeSpawn(level, difficulty, reason, spawnData);
        setAgeInDays(125);
        setMale(false);
        setPersistenceRequired();
        forceBossAttributes(true);
        return result;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide) {
            forceBossAttributes(false);
            bossEvent.setName(getDisplayName());
            bossEvent.setProgress(Math.max(0.0F, getHealth() / getMaxHealth()));
        }
    }

    private void forceBossAttributes(boolean heal) {
        var maxHealth = getAttribute(Attributes.MAX_HEALTH);
        if (maxHealth != null && maxHealth.getBaseValue() != MAX_HEALTH) maxHealth.setBaseValue(MAX_HEALTH);
        if (heal || getHealth() > getMaxHealth()) setHealth(getMaxHealth());
    }

    @Override public void startSeenByPlayer(ServerPlayer player) { super.startSeenByPlayer(player); bossEvent.addPlayer(player); }
    @Override public void stopSeenByPlayer(ServerPlayer player) { super.stopSeenByPlayer(player); bossEvent.removePlayer(player); }
    @Override public void remove(RemovalReason reason) { bossEvent.removeAllPlayers(); super.remove(reason); }
    @Override public ResourceLocation getDeadLootTable() { return LOOT; }
}

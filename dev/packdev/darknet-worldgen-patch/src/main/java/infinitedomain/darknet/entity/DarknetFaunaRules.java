package infinitedomain.darknet.entity;

import infinitedomain.darknet.DarknetGuard;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.ServerLevelAccessor;

/** Shared, dimension-locked surface rules for the Darknet's native ecology. */
public final class DarknetFaunaRules {
    private DarknetFaunaRules() {}

    public static <T extends Mob> boolean canSpawn(EntityType<T> type, ServerLevelAccessor level,
                                                   MobSpawnType reason, BlockPos pos, RandomSource random) {
        if (!DarknetGuard.isDarknet(level.getLevel()) || pos.getY() < 2) return false;
        return !level.getBlockState(pos.below()).isAir() && level.getFluidState(pos).isEmpty();
    }
}

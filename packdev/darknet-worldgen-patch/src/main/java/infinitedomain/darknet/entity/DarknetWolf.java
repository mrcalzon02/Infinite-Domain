package infinitedomain.darknet.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Wolf;
import net.minecraft.world.level.Level;

public final class DarknetWolf extends Wolf {
    public DarknetWolf(EntityType<? extends Wolf> type, Level level) {
        super(type, level);
    }

    @Override
    public Wolf getBreedOffspring(ServerLevel level, AgeableMob mate) {
        DarknetWolf child = DarknetEntities.DARKNET_HOUND.get().create(level);
        if (child != null && isTame()) {
            child.setOwnerUUID(getOwnerUUID());
            child.setTame(true, true);
        }
        return child;
    }
}

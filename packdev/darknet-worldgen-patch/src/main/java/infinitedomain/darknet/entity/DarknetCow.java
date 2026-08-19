package infinitedomain.darknet.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Cow;
import net.minecraft.world.level.Level;

public final class DarknetCow extends Cow {
    public DarknetCow(EntityType<? extends Cow> type, Level level) {
        super(type, level);
    }

    @Override
    public Cow getBreedOffspring(ServerLevel level, AgeableMob mate) {
        return DarknetEntities.DARKNET_COW.get().create(level);
    }
}

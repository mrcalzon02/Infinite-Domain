package infinitedomain.darknet.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Rabbit;
import net.minecraft.world.level.Level;

public final class DarknetRabbit extends Rabbit {
    public DarknetRabbit(EntityType<? extends Rabbit> type, Level level) {
        super(type, level);
    }

    @Override
    public Rabbit getBreedOffspring(ServerLevel level, AgeableMob mate) {
        DarknetRabbit child = DarknetEntities.DARKNET_RABBIT.get().create(level);
        if (child != null) child.setVariant(getVariant());
        return child;
    }
}

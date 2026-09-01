package infinitedomain.darknet.entity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Fox;
import net.minecraft.world.level.Level;

public final class DarknetFox extends Fox {
    public DarknetFox(EntityType<? extends Fox> type, Level level) {
        super(type, level);
    }

    @Override
    public Fox getBreedOffspring(ServerLevel level, AgeableMob mate) {
        DarknetFox child = DarknetEntities.DARKNET_FOX.get().create(level);
        if (child != null) child.setVariant(getVariant());
        return child;
    }
}

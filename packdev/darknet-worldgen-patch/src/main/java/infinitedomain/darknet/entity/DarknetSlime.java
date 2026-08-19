package infinitedomain.darknet.entity;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Slime;
import net.minecraft.world.level.Level;

/** The inherited slime removal routine recreates this registered type when splitting. */
public final class DarknetSlime extends Slime {
    public DarknetSlime(EntityType<? extends Slime> type, Level level) {
        super(type, level);
    }
}

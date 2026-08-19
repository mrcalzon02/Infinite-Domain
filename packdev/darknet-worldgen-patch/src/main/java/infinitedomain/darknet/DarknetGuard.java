package infinitedomain.darknet;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;

public final class DarknetGuard {
    private static final ResourceLocation DARKNET = ResourceLocation.fromNamespaceAndPath("cyberspace", "darknet_dimension");

    private DarknetGuard() {
    }

    public static boolean isDarknet(Level level) {
        return level.dimension().location().equals(DARKNET);
    }
}

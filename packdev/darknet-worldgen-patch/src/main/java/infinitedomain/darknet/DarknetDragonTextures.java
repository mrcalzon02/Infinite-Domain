package infinitedomain.darknet;

import net.minecraft.resources.ResourceLocation;

/** Maps a native Ice and Fire dragon layer to its UV-identical Darknet copy. */
public final class DarknetDragonTextures {
    private static final String NATIVE_PREFIX = "textures/models/";
    private static final String DARKNET_PREFIX = "textures/entity/darknet/models/";

    private DarknetDragonTextures() {}

    public static ResourceLocation digitize(ResourceLocation nativeTexture) {
        if (nativeTexture == null || !nativeTexture.getPath().startsWith(NATIVE_PREFIX)) {
            return nativeTexture;
        }
        return ResourceLocation.fromNamespaceAndPath(
            "infinite_domain",
            DARKNET_PREFIX + nativeTexture.getPath().substring(NATIVE_PREFIX.length())
        );
    }
}

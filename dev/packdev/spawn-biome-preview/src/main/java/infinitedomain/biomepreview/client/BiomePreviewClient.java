package infinitedomain.biomepreview.client;

import com.mojang.blaze3d.platform.NativeImage;
import infinitedomain.biomepreview.PreviewPayload;
import infinitedomain.biomepreview.SpawnBiomePreview;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FastColor;

/** Owns the per-world dynamic texture used by every survey painting. */
public final class BiomePreviewClient {
    private static final ResourceLocation TEXTURE = SpawnBiomePreview.id("dynamic/world_biome_preview");
    private static DynamicTexture dynamicTexture;
    private static long fingerprint = Long.MIN_VALUE;

    private BiomePreviewClient() {}

    public static void accept(PreviewPayload payload) {
        Minecraft minecraft = Minecraft.getInstance();
        NativeImage image = new NativeImage(payload.width(), payload.height(), false);
        int[] pixels = payload.pixels();
        for (int y = 0; y < payload.height(); y++) {
            for (int x = 0; x < payload.width(); x++) {
                int argb = pixels[y * payload.width() + x];
                image.setPixelRGBA(x, y, FastColor.ABGR32.fromArgb32(argb));
            }
        }

        if (dynamicTexture != null) {
            minecraft.getTextureManager().release(TEXTURE);
            dynamicTexture.close();
        }
        dynamicTexture = new DynamicTexture(image);
        minecraft.getTextureManager().register(TEXTURE, dynamicTexture);
        dynamicTexture.upload();
        fingerprint = payload.worldFingerprint();
    }

    public static ResourceLocation texture() {
        return dynamicTexture == null ? null : TEXTURE;
    }

    public static long fingerprint() {
        return fingerprint;
    }
}

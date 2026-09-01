package infinitedomain.biomepreview;

import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;

/**
 * Generates a world-specific biome survey without creating distant chunks and
 * displays it on one dedicated painting variant.
 */
@Mod(SpawnBiomePreview.MOD_ID)
public final class SpawnBiomePreview {
    public static final String MOD_ID = "infinite_domain_spawn_biome_preview";
    public static final ResourceLocation PAINTING_ID = id("world_biome_preview");

    public SpawnBiomePreview(IEventBus modBus) {
        modBus.addListener(PreviewPayload::register);
        NeoForge.EVENT_BUS.addListener(BiomePreviewServer::onPlayerLogin);
        NeoForge.EVENT_BUS.addListener(BiomePreviewServer::onServerTick);
        NeoForge.EVENT_BUS.addListener(BiomePreviewServer::onRegisterCommands);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
    }
}

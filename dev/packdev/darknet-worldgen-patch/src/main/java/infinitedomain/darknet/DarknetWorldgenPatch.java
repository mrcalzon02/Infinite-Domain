package infinitedomain.darknet;

import infinitedomain.darknet.client.DarknetClient;
import infinitedomain.darknet.entity.DarknetEntities;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;

@Mod(DarknetWorldgenPatch.MOD_ID)
public final class DarknetWorldgenPatch {
    public static final String MOD_ID = "infinite_domain_darknet_worldgen";

    public DarknetWorldgenPatch(IEventBus modBus) {
        DarknetEntities.register(modBus);
        if (FMLEnvironment.dist == Dist.CLIENT) DarknetClient.register(modBus);
    }
}

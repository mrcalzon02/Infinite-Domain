package infinitedomain.hiveworld;

import infinitedomain.hiveworld.client.HiveAtmosphereClient;
import infinitedomain.hiveworld.worldgen.HiveDensityFunctions;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;

/**
 * Runtime owner for Hive World systems that cannot be expressed by datapack JSON.
 */
@Mod(HiveWorldCompanion.MOD_ID)
public final class HiveWorldCompanion {
    public static final String MOD_ID = "infinite_domain_hive_world";

    public HiveWorldCompanion(IEventBus modBus) {
        HiveDensityFunctions.register(modBus);
        if (FMLEnvironment.dist == Dist.CLIENT) {
            HiveAtmosphereClient.register(modBus);
        }
    }
}

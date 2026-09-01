package infinitedomain.worldgen;

import infinitedomain.worldgen.density.OverworldDensityFunctions;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

/** Registers Infinite Domain terrain codecs that cannot be expressed in datapack JSON. */
@Mod(InfiniteDomainWorldgen.MOD_ID)
public final class InfiniteDomainWorldgen {
    public static final String MOD_ID = "infinite_domain_worldgen";

    public InfiniteDomainWorldgen(IEventBus modBus) {
        OverworldDensityFunctions.register(modBus);
    }
}

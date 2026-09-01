package infinitedomain.lostcitiescompat;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(LostCitiesHighwayCompat.MOD_ID)
public final class LostCitiesHighwayCompat {
    public static final String MOD_ID = "infinite_domain_lostcities_highway_compat";

    public LostCitiesHighwayCompat(IEventBus modBus) {
        // All behavior is supplied by the Mixin in the mixin package; no
        // registration is needed here.
    }
}

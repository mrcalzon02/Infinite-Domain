package infinitedomain.cyberware;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(InfiniteDomainCyberware.MOD_ID)
public final class InfiniteDomainCyberware {
    public static final String MOD_ID = "infinite_domain_cyberware";

    public InfiniteDomainCyberware(IEventBus modBus) {
        CyberwareCatalog.register(modBus);
    }
}

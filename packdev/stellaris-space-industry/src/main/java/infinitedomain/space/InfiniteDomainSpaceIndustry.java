package infinitedomain.space;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;

@Mod(InfiniteDomainSpaceIndustry.MOD_ID)
public final class InfiniteDomainSpaceIndustry {
    public static final String MOD_ID = "infinite_domain_space";

    public InfiniteDomainSpaceIndustry(IEventBus modBus) {
        SpaceSuitCatalog.register(modBus);
        NeoForge.EVENT_BUS.addListener(SuitSpecializations::onEquipmentChange);
        NeoForge.EVENT_BUS.addListener(SuitSpecializations::onLogin);
    }
}

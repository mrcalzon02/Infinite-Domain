package infinitedomain.echoeconomy;

import dev.ftb.mods.ftblibrary.integration.currency.CurrencyHelper;
import net.neoforged.fml.common.Mod;

@Mod(InfiniteDomainEchoEconomy.MOD_ID)
public final class InfiniteDomainEchoEconomy {
    public static final String MOD_ID = "infinite_domain_echo_economy";

    public InfiniteDomainEchoEconomy() {
        CurrencyHelper.getInstance().setActiveImpl(NumismaticsCurrencyProvider.INSTANCE);
    }
}

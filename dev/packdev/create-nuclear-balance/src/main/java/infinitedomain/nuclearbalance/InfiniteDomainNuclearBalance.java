package infinitedomain.nuclearbalance;

import net.neoforged.fml.common.Mod;

@Mod(InfiniteDomainNuclearBalance.MOD_ID)
public final class InfiniteDomainNuclearBalance {
    public static final String MOD_ID = "infinite_domain_nuclear_balance";

    public InfiniteDomainNuclearBalance() {
        // The capacity override is applied by CNBlocksMixin while Create Nuclear
        // registers its reactor output block.
    }
}

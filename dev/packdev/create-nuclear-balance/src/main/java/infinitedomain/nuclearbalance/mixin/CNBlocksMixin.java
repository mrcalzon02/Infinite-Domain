package infinitedomain.nuclearbalance.mixin;

import infinitedomain.nuclearbalance.NuclearOutputBalance;
import net.nuclearteam.createnuclear.CNBlocks;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.ModifyConstant;

@Mixin(value = CNBlocks.class, remap = false)
abstract class CNBlocksMixin {
    @ModifyConstant(
        method = "lambda$static$22",
        constant = @Constant(doubleValue = 10240.0D),
        require = 1
    )
    private static double infiniteDomain$limitReactorStressCapacity(double installedValue) {
        return NuclearOutputBalance.capacityPerRpm(installedValue);
    }
}

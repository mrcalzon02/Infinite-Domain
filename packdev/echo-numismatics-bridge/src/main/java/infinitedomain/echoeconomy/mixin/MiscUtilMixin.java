package infinitedomain.echoeconomy.mixin;

import dev.ftb.mods.ftbechoes.util.MiscUtil;
import infinitedomain.echoeconomy.NumismaticsCurrencyProvider;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value = MiscUtil.class, remap = false)
abstract class MiscUtilMixin {
    @Inject(method = "formatCost", at = @At("HEAD"), cancellable = true)
    private static void infiniteDomain$formatNumismaticsCost(
        int cost,
        CallbackInfoReturnable<Component> callback
    ) {
        callback.setReturnValue(NumismaticsCurrencyProvider.format(cost));
    }
}

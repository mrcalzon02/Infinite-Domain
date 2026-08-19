package infinitedomain.space.mixin;

import com.st0x0ef.stellaris.common.utils.Utils;
import infinitedomain.space.SpaceSuitCatalog;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value = Utils.class, remap = false)
public abstract class StellarisSuitCompatibilityMixin {
    @Inject(method = "isLivingInSpaceSuit", at = @At("RETURN"), cancellable = true, remap = false)
    private static void infiniteDomain$recognizeRoleSuits(LivingEntity entity, CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValue() && SpaceSuitCatalog.isCompleteCustomSuit(entity)) {
            cir.setReturnValue(true);
        }
    }
}

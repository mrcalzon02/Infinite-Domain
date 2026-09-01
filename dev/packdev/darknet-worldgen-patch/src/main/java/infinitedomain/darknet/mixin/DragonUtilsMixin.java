package infinitedomain.darknet.mixin;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import infinitedomain.darknet.DarknetGuard;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(targets = "com.github.alexthe666.iceandfire.entity.util.DragonUtils", remap = false)
abstract class DragonUtilsMixin {
    @Inject(method = "canGrief", at = @At("HEAD"), cancellable = true)
    private static void infiniteDomain$protectDarknetFloor(
        EntityDragonBase dragon,
        CallbackInfoReturnable<Boolean> callback
    ) {
        if (DarknetGuard.isDarknet(dragon.level())) {
            callback.setReturnValue(false);
        }
    }
}

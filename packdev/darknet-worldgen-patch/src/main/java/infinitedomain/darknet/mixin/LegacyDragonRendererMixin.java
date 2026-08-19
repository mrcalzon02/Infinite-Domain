package infinitedomain.darknet.mixin;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import infinitedomain.darknet.DarknetDragonTextures;
import infinitedomain.darknet.DarknetGuard;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Preserves the renderer's layered male pattern while digitizing that layer. */
@Mixin(targets = "com.github.alexthe666.iceandfire.neoforge.LegacyNeoForgeClientBootstrap$LegacyDragonRenderer", remap = false)
abstract class LegacyDragonRendererMixin {
    @Inject(method = "maleOverlay", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeMaleOverlay(
        EntityDragonBase dragon,
        CallbackInfoReturnable<ResourceLocation> callback
    ) {
        if (DarknetGuard.isDarknet(dragon.level())) {
            callback.setReturnValue(DarknetDragonTextures.digitize(callback.getReturnValue()));
        }
    }
}

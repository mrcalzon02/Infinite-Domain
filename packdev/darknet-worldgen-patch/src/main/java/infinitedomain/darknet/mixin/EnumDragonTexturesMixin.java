package infinitedomain.darknet.mixin;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import com.github.alexthe666.iceandfire.entity.EntityDragonSkull;
import com.github.alexthe666.iceandfire.enums.EnumDragonTextures;
import infinitedomain.darknet.DarknetDragonTextures;
import infinitedomain.darknet.DarknetGuard;
import infinitedomain.darknet.entity.DatavoreDragon;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Digitizes every native body, sleeping, skeleton, eye, and skull selection. */
@Mixin(value = EnumDragonTextures.class, remap = false)
abstract class EnumDragonTexturesMixin {
    private static final ResourceLocation DATAVORE = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/datavore/datavore.png");
    private static final ResourceLocation DATAVORE_EYES = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/datavore/datavore_eyes.png");
    private static final ResourceLocation DATAVORE_SKELETON = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/datavore/datavore_skeleton.png");

    @Inject(method = "getTextureFromDragon", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeBody(EntityDragonBase dragon, CallbackInfoReturnable<ResourceLocation> callback) {
        if (dragon instanceof DatavoreDragon) {
            callback.setReturnValue(dragon.isSkeletal() ? DATAVORE_SKELETON : DATAVORE);
            return;
        }
        if (DarknetGuard.isDarknet(dragon.level())) {
            callback.setReturnValue(DarknetDragonTextures.digitize(callback.getReturnValue()));
        }
    }

    @Inject(method = "getEyeTextureFromDragon", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeEyes(EntityDragonBase dragon, CallbackInfoReturnable<ResourceLocation> callback) {
        if (dragon instanceof DatavoreDragon) {
            callback.setReturnValue(DATAVORE_EYES);
            return;
        }
        if (DarknetGuard.isDarknet(dragon.level())) {
            callback.setReturnValue(DarknetDragonTextures.digitize(callback.getReturnValue()));
        }
    }

    @Inject(method = "getFireDragonSkullTextures", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeFireSkull(EntityDragonSkull skull, CallbackInfoReturnable<ResourceLocation> callback) {
        infiniteDomain$digitizeSkull(skull, callback);
    }

    @Inject(method = "getIceDragonSkullTextures", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeIceSkull(EntityDragonSkull skull, CallbackInfoReturnable<ResourceLocation> callback) {
        infiniteDomain$digitizeSkull(skull, callback);
    }

    @Inject(method = "getLightningDragonSkullTextures", at = @At("RETURN"), cancellable = true)
    private static void infiniteDomain$digitizeLightningSkull(EntityDragonSkull skull, CallbackInfoReturnable<ResourceLocation> callback) {
        infiniteDomain$digitizeSkull(skull, callback);
    }

    private static void infiniteDomain$digitizeSkull(EntityDragonSkull skull, CallbackInfoReturnable<ResourceLocation> callback) {
        if (DarknetGuard.isDarknet(skull.level())) {
            callback.setReturnValue(DarknetDragonTextures.digitize(callback.getReturnValue()));
        }
    }
}

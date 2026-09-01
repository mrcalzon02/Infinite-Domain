package infinitedomain.darknet.mixin;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import com.mojang.blaze3d.vertex.PoseStack;
import infinitedomain.darknet.DarknetDragonTextures;
import infinitedomain.darknet.DarknetGuard;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Redirects all four composed dragon-armor pieces to their Darknet copies. */
@Mixin(targets = "com.github.alexthe666.iceandfire.neoforge.LegacyNeoForgeClientBootstrap$LegacyDragonArmorFeature", remap = false)
abstract class LegacyDragonArmorFeatureMixin {
    @Redirect(
        method = "render(Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;ILcom/github/alexthe666/iceandfire/entity/EntityDragonBase;FFFFFF)V",
        at = @At(value = "INVOKE", target = "Lnet/minecraft/resources/ResourceLocation;toString()Ljava/lang/String;")
    )
    private String infiniteDomain$digitizeArmorLayer(
        ResourceLocation nativeTexture,
        PoseStack poses,
        MultiBufferSource buffers,
        int packedLight,
        EntityDragonBase dragon,
        float limbSwing,
        float limbSwingAmount,
        float partialTicks,
        float ageInTicks,
        float netHeadYaw,
        float headPitch
    ) {
        return (DarknetGuard.isDarknet(dragon.level())
            ? DarknetDragonTextures.digitize(nativeTexture)
            : nativeTexture).toString();
    }
}

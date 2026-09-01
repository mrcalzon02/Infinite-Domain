package infinitedomain.darknet.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import infinitedomain.darknet.DarknetGuard;
import infinitedomain.darknet.client.DarknetEntityOverlayLayer;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(net.minecraft.client.renderer.entity.layers.HumanoidArmorLayer.class)
abstract class HumanoidArmorLayerMixin {
    @Inject(method = "renderArmorPiece", at = @At("TAIL"))
    private void infiniteDomain$overlayArmor(PoseStack poses, MultiBufferSource buffers, LivingEntity entity,
                                             EquipmentSlot slot, int packedLight, HumanoidModel<?> armorModel,
                                             CallbackInfo callback) {
        if (entity.isInvisible() || !DarknetGuard.isDarknet(entity.level())) return;
        armorModel.renderToBuffer(poses, buffers.getBuffer(RenderType.entityTranslucentEmissive(DarknetEntityOverlayLayer.CIRCUITRY)),
            0x00F000F0, OverlayTexture.NO_OVERLAY);
        armorModel.renderToBuffer(poses, buffers.getBuffer(RenderType.entityTranslucentEmissive(DarknetEntityOverlayLayer.SHIMMER)),
            0x00F000F0, OverlayTexture.NO_OVERLAY);
    }
}

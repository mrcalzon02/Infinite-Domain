package infinitedomain.biomepreview.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.math.Axis;
import infinitedomain.biomepreview.SpawnBiomePreview;
import infinitedomain.biomepreview.client.BiomePreviewClient;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.PaintingRenderer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.decoration.Painting;
import net.minecraft.world.entity.decoration.PaintingVariant;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Draws the generated image over the front of only the dedicated survey variant. */
@Mixin(PaintingRenderer.class)
public abstract class PaintingRendererMixin {
    private static final ResourceKey<PaintingVariant> PREVIEW_VARIANT =
            ResourceKey.create(Registries.PAINTING_VARIANT, SpawnBiomePreview.PAINTING_ID);

    @Inject(
            method = "render(Lnet/minecraft/world/entity/decoration/Painting;FFLcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;I)V",
            at = @At("TAIL")
    )
    private void infiniteDomain$renderPreview(
            Painting painting,
            float entityYaw,
            float partialTick,
            PoseStack poseStack,
            MultiBufferSource buffers,
            int packedLight,
            CallbackInfo callback
    ) {
        if (!painting.getVariant().is(PREVIEW_VARIANT)) return;
        ResourceLocation texture = BiomePreviewClient.texture();
        if (texture == null) return;

        PaintingVariant variant = painting.getVariant().value();
        float halfWidth = variant.width() / 2.0F;
        float halfHeight = variant.height() / 2.0F;
        float front = -0.033F;

        poseStack.pushPose();
        poseStack.mulPose(Axis.YP.rotationDegrees(180.0F - entityYaw));
        PoseStack.Pose pose = poseStack.last();
        VertexConsumer vertices = buffers.getBuffer(RenderType.entitySolid(texture));

        vertex(vertices, pose, halfWidth, -halfHeight, front, 0.0F, 1.0F, packedLight);
        vertex(vertices, pose, -halfWidth, -halfHeight, front, 1.0F, 1.0F, packedLight);
        vertex(vertices, pose, -halfWidth, halfHeight, front, 1.0F, 0.0F, packedLight);
        vertex(vertices, pose, halfWidth, halfHeight, front, 0.0F, 0.0F, packedLight);
        poseStack.popPose();
    }

    private static void vertex(
            VertexConsumer consumer,
            PoseStack.Pose pose,
            float x,
            float y,
            float z,
            float u,
            float v,
            int packedLight
    ) {
        consumer.addVertex(pose, x, y, z)
                .setColor(-1)
                .setUv(u, v)
                .setOverlay(OverlayTexture.NO_OVERLAY)
                .setLight(packedLight)
                .setNormal(pose, 0.0F, 0.0F, -1.0F);
    }
}

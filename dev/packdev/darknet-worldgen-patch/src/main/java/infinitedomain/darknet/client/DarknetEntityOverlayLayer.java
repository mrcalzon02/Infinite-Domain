package infinitedomain.darknet.client;

import com.github.alexthe666.iceandfire.entity.EntityDragonBase;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import infinitedomain.darknet.DarknetGuard;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;

/** Universal post-skin Darknet circuitry and shimmer for living entities. */
public final class DarknetEntityOverlayLayer<T extends LivingEntity, M extends EntityModel<T>> extends RenderLayer<T, M> {
    public static final ResourceLocation CIRCUITRY = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet_overlay_static.png");
    public static final ResourceLocation SHIMMER = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet_overlay_shimmer.png");

    public DarknetEntityOverlayLayer(RenderLayerParent<T, M> parent) {
        super(parent);
    }

    @Override
    public void render(PoseStack poses, MultiBufferSource buffers, int packedLight, T entity,
                       float limbSwing, float limbSwingAmount, float partialTicks,
                       float ageInTicks, float netHeadYaw, float headPitch) {
        if (entity.isInvisible() || !DarknetGuard.isDarknet(entity.level())) return;

        // Dragons already carry a complete bespoke digitized skin; the universal
        // layer still marks them as active Darknet matter, but at normal opacity.
        int light = entity instanceof EntityDragonBase ? packedLight : 0x00F000F0;
        renderOverlay(poses, buffers, light, CIRCUITRY);
        renderOverlay(poses, buffers, light, SHIMMER);
    }

    private void renderOverlay(PoseStack poses, MultiBufferSource buffers, int packedLight, ResourceLocation texture) {
        VertexConsumer vertices = buffers.getBuffer(RenderType.entityTranslucentEmissive(texture));
        getParentModel().renderToBuffer(poses, vertices, packedLight, OverlayTexture.NO_OVERLAY);
    }
}

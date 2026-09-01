package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.WolfRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Wolf;

public final class DarknetWolfRenderer extends WolfRenderer {
    private static final ResourceLocation WILD = texture("wolf");
    private static final ResourceLocation TAME = texture("wolf_tame");
    private static final ResourceLocation ANGRY = texture("wolf_angry");
    public DarknetWolfRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public ResourceLocation getTextureLocation(Wolf wolf) {
        return wolf.isTame() ? TAME : wolf.isAngry() ? ANGRY : WILD;
    }
    private static ResourceLocation texture(String name) {
        return ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet/" + name + ".png");
    }
}

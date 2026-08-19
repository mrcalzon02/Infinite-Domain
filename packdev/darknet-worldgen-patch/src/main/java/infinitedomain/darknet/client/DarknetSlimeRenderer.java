package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.SlimeRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.monster.Slime;

public final class DarknetSlimeRenderer extends SlimeRenderer {
    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet/slime.png");
    public DarknetSlimeRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public ResourceLocation getTextureLocation(Slime slime) { return TEXTURE; }
}

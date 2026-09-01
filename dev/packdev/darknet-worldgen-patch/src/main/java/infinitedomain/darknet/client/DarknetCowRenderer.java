package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.CowRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Cow;

public final class DarknetCowRenderer extends CowRenderer {
    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet/cow.png");
    public DarknetCowRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public ResourceLocation getTextureLocation(Cow cow) { return TEXTURE; }
}

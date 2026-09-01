package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.RabbitRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Rabbit;

public final class DarknetRabbitRenderer extends RabbitRenderer {
    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet/rabbit.png");
    public DarknetRabbitRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public ResourceLocation getTextureLocation(Rabbit rabbit) { return TEXTURE; }
}

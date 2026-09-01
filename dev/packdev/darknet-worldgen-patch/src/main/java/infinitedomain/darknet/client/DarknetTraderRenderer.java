package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.WanderingTraderRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.npc.WanderingTrader;

public final class DarknetTraderRenderer extends WanderingTraderRenderer {
    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath(
        "infinite_domain", "textures/entity/darknet_broker.png"
    );

    public DarknetTraderRenderer(EntityRendererProvider.Context context) {
        super(context);
    }

    @Override
    public ResourceLocation getTextureLocation(WanderingTrader trader) {
        return TEXTURE;
    }
}

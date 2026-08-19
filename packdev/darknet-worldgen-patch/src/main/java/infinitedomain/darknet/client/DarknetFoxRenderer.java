package infinitedomain.darknet.client;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.FoxRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Fox;

public final class DarknetFoxRenderer extends FoxRenderer {
    private static final ResourceLocation AWAKE = texture("fox");
    private static final ResourceLocation ASLEEP = texture("fox_sleep");
    public DarknetFoxRenderer(EntityRendererProvider.Context context) { super(context); }
    @Override public ResourceLocation getTextureLocation(Fox fox) { return fox.isSleeping() ? ASLEEP : AWAKE; }
    private static ResourceLocation texture(String name) {
        return ResourceLocation.fromNamespaceAndPath("infinite_domain", "textures/entity/darknet/" + name + ".png");
    }
}

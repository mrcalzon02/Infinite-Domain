package infinitedomain.darknet.mixin;

import infinitedomain.darknet.client.DarknetEntityOverlayLayer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(LivingEntityRenderer.class)
abstract class LivingEntityRendererMixin<T extends LivingEntity, M extends EntityModel<T>> extends EntityRenderer<T> {
    protected LivingEntityRendererMixin(EntityRendererProvider.Context context) { super(context); }

    @Shadow protected abstract boolean addLayer(RenderLayer<T, M> layer);

    @SuppressWarnings("unchecked")
    @Inject(method = "<init>", at = @At("TAIL"))
    private void infiniteDomain$addDarknetOverlay(EntityRendererProvider.Context context, M model, float shadowRadius, CallbackInfo callback) {
        addLayer(new DarknetEntityOverlayLayer<>((LivingEntityRenderer<T, M>) (Object) this));
    }
}

package infinitedomain.darknet.mixin;

import com.github.alexthe666.iceandfire.entity.IafEntityRegistry;
import infinitedomain.darknet.entity.DatavoreDragon;
import java.util.Map;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(EntityRenderDispatcher.class)
abstract class EntityRenderDispatcherMixin {
    @Shadow private Map<EntityType<?>, EntityRenderer<?>> renderers;

    @SuppressWarnings("unchecked")
    @Inject(method = "getRenderer", at = @At("HEAD"), cancellable = true)
    private <T extends Entity> void infiniteDomain$useLightningDragonRenderer(T entity,
        CallbackInfoReturnable<EntityRenderer<? super T>> callback) {
        if (entity instanceof DatavoreDragon) {
            callback.setReturnValue((EntityRenderer<? super T>) renderers.get(IafEntityRegistry.LIGHTNING_DRAGON.get()));
        }
    }
}

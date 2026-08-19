package infinitedomain.darknet.mixin;

import infinitedomain.darknet.DarknetGuard;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Explosion;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(targets = "com.github.alexthe666.iceandfire.entity.IafDragonDestructionManager", remap = false)
abstract class IafDragonDestructionManagerMixin {
    @Redirect(
        method = "destroyAreaCharge",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/level/Level;explode(Lnet/minecraft/world/entity/Entity;DDDFLnet/minecraft/world/level/Level$ExplosionInteraction;)Lnet/minecraft/world/level/Explosion;"
        )
    )
    private static Explosion infiniteDomain$protectDarknetFromChargedBreath(
        Level level,
        Entity source,
        double x,
        double y,
        double z,
        float radius,
        Level.ExplosionInteraction interaction
    ) {
        Level.ExplosionInteraction safeInteraction = DarknetGuard.isDarknet(level)
            ? Level.ExplosionInteraction.NONE
            : interaction;
        return level.explode(source, x, y, z, radius, safeInteraction);
    }
}

package infinitedomain.darknet.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

/** Makes the generated Darknet foundation deliberately mineable by players. */
@Mixin(targets = "cyberspace.block.Darknetblock1Block", remap = false)
abstract class Darknetblock1Mixin {
    private static final float DARKNET_FOUNDATION_HARDNESS = 12.0F;
    private static final float DARKNET_FOUNDATION_BLAST_RESISTANCE = 1200.0F;

    @ModifyArg(
        method = "<init>",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/level/block/state/BlockBehaviour$Properties;strength(FF)Lnet/minecraft/world/level/block/state/BlockBehaviour$Properties;"
        ),
        index = 0
    )
    private static float infiniteDomain$mineableFoundation(float originalHardness) {
        return DARKNET_FOUNDATION_HARDNESS;
    }

    @ModifyArg(
        method = "<init>",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/level/block/state/BlockBehaviour$Properties;strength(FF)Lnet/minecraft/world/level/block/state/BlockBehaviour$Properties;"
        ),
        index = 1
    )
    private static float infiniteDomain$blastResistantFoundation(float originalResistance) {
        return DARKNET_FOUNDATION_BLAST_RESISTANCE;
    }
}

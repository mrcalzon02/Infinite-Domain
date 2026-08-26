package infinitedomain.lostcitiescompat.mixin;

import infinitedomain.lostcitiescompat.HighwayBarrier;
import mcjty.lostcities.worldgen.highway.HighwayHub;
import mcjty.lostcities.worldgen.highway.HighwaySegment;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.List;

@Mixin(targets = "mcjty.lostcities.worldgen.highway.IntercityHighwayPlanner", remap = false)
abstract class IntercityHighwayPlannerMixin {
    @Inject(method = "routePenalty", at = @At("RETURN"), cancellable = true)
    private void infiniteDomain$penalizeBarrierCrossings(
        List<HighwaySegment> segments,
        HighwayHub hubA,
        HighwayHub hubB,
        CallbackInfoReturnable<Long> callback
    ) {
        if (HighwayBarrier.crossesBarrier(segments)) {
            callback.setReturnValue(Long.MAX_VALUE);
        }
    }
}

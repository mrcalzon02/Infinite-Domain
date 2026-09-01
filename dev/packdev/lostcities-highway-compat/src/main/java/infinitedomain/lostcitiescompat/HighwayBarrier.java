package infinitedomain.lostcitiescompat;

import mcjty.lostcities.worldgen.highway.HighwaySegment;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.biome.Biome;
import net.neoforged.neoforge.server.ServerLifecycleHooks;

import java.util.List;

/**
 * Real-terrain check backing the highway-barrier compatibility Mixin.
 * <p>
 * Lost Cities' own route-selection penalty is based on an approximate,
 * seed-only city-potential model with no live biome access (see
 * {@code IntercityHighwayPlanner}/{@code ApproximateCityPotential}), so it
 * can still pick a route that crosses open ocean between two land hubs. This
 * class samples the actual Overworld biome along a proposed route and
 * reports whether it crosses {@code #infinite_domain:highway_barrier}
 * (ocean/abyssal terrain) so the Mixin can penalize that route out of
 * contention.
 */
public final class HighwayBarrier {
    private static final TagKey<Biome> BARRIER_TAG = TagKey.create(
        Registries.BIOME, ResourceLocation.fromNamespaceAndPath("infinite_domain", "highway_barrier"));
    private static final int SAMPLE_SPACING = 16;

    private HighwayBarrier() {
    }

    public static boolean crossesBarrier(List<HighwaySegment> segments) {
        ServerLevel overworld = overworld();
        if (overworld == null) {
            return false;
        }
        for (HighwaySegment segment : segments) {
            if (segmentCrossesBarrier(overworld, segment)) {
                return true;
            }
        }
        return false;
    }

    private static boolean segmentCrossesBarrier(ServerLevel level, HighwaySegment segment) {
        int startX = segment.startX();
        int startZ = segment.startZ();
        int endX = segment.endX();
        int endZ = segment.endZ();
        int length = Math.max(Math.abs(endX - startX), Math.abs(endZ - startZ));
        int steps = Math.max(1, length / SAMPLE_SPACING);
        for (int step = 0; step <= steps; step++) {
            double t = (double) step / steps;
            int x = startX + (int) Math.round((endX - startX) * t);
            int z = startZ + (int) Math.round((endZ - startZ) * t);
            Holder<Biome> biome = level.getBiome(new BlockPos(x, level.getSeaLevel(), z));
            if (biome.is(BARRIER_TAG)) {
                return true;
            }
        }
        return false;
    }

    private static ServerLevel overworld() {
        var server = ServerLifecycleHooks.getCurrentServer();
        return server == null ? null : server.overworld();
    }
}

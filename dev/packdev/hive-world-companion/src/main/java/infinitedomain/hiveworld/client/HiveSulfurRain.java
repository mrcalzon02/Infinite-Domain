package infinitedomain.hiveworld.client;

import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.Vec3;

import java.util.Optional;

/** Extra exposed-weather particulates for the Dead wastes and Stack apron. */
final class HiveSulfurRain {
    private static final ResourceLocation WASTES =
            ResourceLocation.fromNamespaceAndPath("infinite_domain", "hive_world_wastes");
    private static final ResourceLocation APRON =
            ResourceLocation.fromNamespaceAndPath("infinite_domain", "hive_world_apron");

    private HiveSulfurRain() {}

    static void tick(ClientLevel level, int ticks, Camera camera) {
        if ((ticks & 1) != 0) return;
        Vec3 position = camera.getPosition();
        BlockPos cameraPos = BlockPos.containing(position);
        if (!level.canSeeSky(cameraPos) || !isExposedBiome(level, cameraPos)) return;

        for (int i = 0; i < 5; i++) {
            int x = cameraPos.getX() + level.random.nextInt(33) - 16;
            int z = cameraPos.getZ() + level.random.nextInt(33) - 16;
            int surfaceY = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
            BlockPos surface = new BlockPos(x, surfaceY, z);
            if (!level.canSeeSky(surface)) continue;

            double y = Math.min(level.getMaxBuildHeight() - 2.0,
                    Math.max(position.y() + 8.0, surfaceY + 10.0)
                            + level.random.nextDouble() * 12.0);
            double vx = (level.random.nextDouble() - 0.5) * 0.035;
            double vz = (level.random.nextDouble() - 0.5) * 0.035;
            level.addParticle(ParticleTypes.FALLING_HONEY,
                    x + level.random.nextDouble(), y, z + level.random.nextDouble(),
                    vx, -0.72, vz);
            if (i < 2) {
                level.addParticle(ParticleTypes.WHITE_ASH,
                        x + level.random.nextDouble(), y + 2.0,
                        z + level.random.nextDouble(), vx * 0.4, -0.08, vz * 0.4);
            }
        }
    }

    private static boolean isExposedBiome(ClientLevel level, BlockPos pos) {
        Optional<ResourceLocation> id = level.getBiome(pos).unwrapKey().map(key -> key.location());
        return id.filter(value -> value.equals(WASTES) || value.equals(APRON)).isPresent();
    }
}

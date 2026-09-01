package infinitedomain.wastelandhexcaves;

import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;

public final class HexCaveFeature extends Feature<NoneFeatureConfiguration> {
    private static final double SQRT_3 = 1.7320508075688772;
    private static final double HEX_SIZE = 28.0;
    private static final int CHUNK_SIZE = 16;

    private static final long WARP_X_SALT = 0x6A09E667F3BCC909L;
    private static final long WARP_Z_SALT = 0xBB67AE8584CAA73BL;
    private static final long MACRO_SALT = 0x3C6EF372FE94F82BL;
    private static final long PLASMA_SALT = 0xA54FF53A5F1D36F1L;
    private static final long WIDTH_SALT = 0x510E527FADE682D1L;
    private static final long DEPTH_SALT = 0x9B05688C2B3E6C1FL;
    private static final long HEIGHT_SALT = 0x1F83D9ABFB41BD6BL;

    public HexCaveFeature() {
        super(NoneFeatureConfiguration.CODEC);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        WorldGenLevel level = context.level();
        long seed = level.getSeed();
        int minX = context.origin().getX() & ~(CHUNK_SIZE - 1);
        int minZ = context.origin().getZ() & ~(CHUNK_SIZE - 1);
        int minBuildY = level.getMinBuildHeight() + 5;
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        boolean carvedAny = false;

        for (int x = minX; x < minX + CHUNK_SIZE; x++) {
            for (int z = minZ; z < minZ + CHUNK_SIZE; z++) {
                CaveColumn column = sampleColumn(seed, x, z);
                if (!column.carve()) {
                    continue;
                }

                int surfaceY = level.getHeight(Heightmap.Types.WORLD_SURFACE_WG, x, z);
                int maximumCenterY = surfaceY - 10 - column.verticalRadius();
                if (maximumCenterY <= minBuildY) {
                    continue;
                }

                int centerY = Math.max(minBuildY, Math.min(surfaceY - column.depth(), maximumCenterY));
                int radius = column.verticalRadius();

                for (int y = centerY - radius; y <= centerY + radius; y++) {
                    if (y < minBuildY || y >= surfaceY - 10) {
                        continue;
                    }

                    double normalized = Math.abs(y - centerY) / (double) Math.max(1, radius);
                    double ceilingShape = 1.0 - normalized * normalized;
                    if (ceilingShape <= 0.0) {
                        continue;
                    }

                    cursor.set(x, y, z);
                    BlockState state = level.getBlockState(cursor);
                    if (!isNaturalCarvable(state)) {
                        continue;
                    }

                    level.setBlock(cursor, Blocks.CAVE_AIR.defaultBlockState(), 2);
                    carvedAny = true;
                }
            }
        }

        return carvedAny;
    }

    private static boolean isNaturalCarvable(BlockState state) {
        if (state.isAir() || state.hasBlockEntity() || !state.getFluidState().isEmpty()) {
            return false;
        }
        return state.is(BlockTags.BASE_STONE_OVERWORLD)
                || state.is(BlockTags.DIRT)
                || state.is(Blocks.GRAVEL);
    }

    private static CaveColumn sampleColumn(long seed, int blockX, int blockZ) {
        double x = blockX + 0.5;
        double z = blockZ + 0.5;

        double warpX = fbm(seed ^ WARP_X_SALT, x, z, 112.0, 4) * 7.0;
        double warpZ = fbm(seed ^ WARP_Z_SALT, x + 317.0, z - 191.0, 112.0, 4) * 7.0;
        HexMetrics hex = nearestHexBoundary(x + warpX, z + warpZ);

        double macro = fbm(seed ^ MACRO_SALT, x, z, 180.0, 5);
        double plasma = fbm(seed ^ PLASMA_SALT, x - 911.0, z + 613.0, 54.0, 4);
        double widthNoise = fbm(seed ^ WIDTH_SALT, x + 83.0, z + 47.0, 72.0, 3);
        double localWidth = 2.4 + (widthNoise + 1.0) * 1.3;

        boolean macroOccluded = macro > 0.18;
        boolean plasmaOccluded = plasma > 0.38 && macro > -0.25;
        boolean visibleHex = hex.boundaryDistance() <= localWidth && !macroOccluded && !plasmaOccluded;
        boolean fractalChamber = macro < -0.38
                && plasma < 0.22
                && hex.centerDistance() < HEX_SIZE * 0.72;

        double depthNoise = fbm(seed ^ DEPTH_SALT, x - 29.0, z + 101.0, 144.0, 4);
        int depth = 24 + (int) Math.round((depthNoise + 1.0) * 5.0);

        double heightNoise = fbm(seed ^ HEIGHT_SALT, x + 211.0, z - 73.0, 88.0, 3);
        int verticalRadius = 3 + (int) Math.round((heightNoise + 1.0) * 1.5);
        if (fractalChamber) {
            verticalRadius += 2;
        }

        return new CaveColumn(visibleHex || fractalChamber, depth, verticalRadius);
    }

    private static HexMetrics nearestHexBoundary(double x, double z) {
        double qf = (SQRT_3 / 3.0 * x - z / 3.0) / HEX_SIZE;
        double rf = (2.0 / 3.0 * z) / HEX_SIZE;
        Axial rounded = roundAxial(qf, rf);

        double best = Double.POSITIVE_INFINITY;
        double second = Double.POSITIVE_INFINITY;

        for (int dq = -2; dq <= 2; dq++) {
            for (int dr = -2; dr <= 2; dr++) {
                int q = rounded.q() + dq;
                int r = rounded.r() + dr;
                double centerX = HEX_SIZE * SQRT_3 * (q + r / 2.0);
                double centerZ = HEX_SIZE * 1.5 * r;
                double distance = Math.hypot(x - centerX, z - centerZ);

                if (distance < best) {
                    second = best;
                    best = distance;
                } else if (distance < second) {
                    second = distance;
                }
            }
        }

        double boundaryDistance = Math.max(0.0, (second - best) * 0.5);
        return new HexMetrics(boundaryDistance, best);
    }

    private static Axial roundAxial(double q, double r) {
        double x = q;
        double z = r;
        double y = -x - z;

        long rx = Math.round(x);
        long ry = Math.round(y);
        long rz = Math.round(z);

        double xDiff = Math.abs(rx - x);
        double yDiff = Math.abs(ry - y);
        double zDiff = Math.abs(rz - z);

        if (xDiff > yDiff && xDiff > zDiff) {
            rx = -ry - rz;
        } else if (yDiff > zDiff) {
            ry = -rx - rz;
        } else {
            rz = -rx - ry;
        }

        return new Axial((int) rx, (int) rz);
    }

    private static double fbm(long seed, double x, double z, double scale, int octaves) {
        double frequency = 1.0 / scale;
        double amplitude = 1.0;
        double value = 0.0;
        double normalization = 0.0;

        for (int octave = 0; octave < octaves; octave++) {
            value += valueNoise(seed + octave * 0x9E3779B97F4A7C15L, x * frequency, z * frequency) * amplitude;
            normalization += amplitude;
            amplitude *= 0.5;
            frequency *= 2.0;
        }

        return value / normalization;
    }

    private static double valueNoise(long seed, double x, double z) {
        int x0 = fastFloor(x);
        int z0 = fastFloor(z);
        int x1 = x0 + 1;
        int z1 = z0 + 1;
        double tx = smooth(x - x0);
        double tz = smooth(z - z0);

        double a = randomSigned(seed, x0, z0);
        double b = randomSigned(seed, x1, z0);
        double c = randomSigned(seed, x0, z1);
        double d = randomSigned(seed, x1, z1);

        double top = lerp(a, b, tx);
        double bottom = lerp(c, d, tx);
        return lerp(top, bottom, tz);
    }

    private static double randomSigned(long seed, int x, int z) {
        long mixed = seed
                ^ ((long) x * 0x632BE59BD9B4E019L)
                ^ ((long) z * 0x9E3779B185EBCA87L);
        mixed ^= mixed >>> 30;
        mixed *= 0xBF58476D1CE4E5B9L;
        mixed ^= mixed >>> 27;
        mixed *= 0x94D049BB133111EBL;
        mixed ^= mixed >>> 31;
        long mantissa = mixed >>> 11;
        return mantissa * 0x1.0p-53 * 2.0 - 1.0;
    }

    private static int fastFloor(double value) {
        int integer = (int) value;
        return value < integer ? integer - 1 : integer;
    }

    private static double smooth(double t) {
        return t * t * (3.0 - 2.0 * t);
    }

    private static double lerp(double a, double b, double t) {
        return a + (b - a) * t;
    }

    private record Axial(int q, int r) {}

    private record HexMetrics(double boundaryDistance, double centerDistance) {}

    private record CaveColumn(boolean carve, int depth, int verticalRadius) {}
}

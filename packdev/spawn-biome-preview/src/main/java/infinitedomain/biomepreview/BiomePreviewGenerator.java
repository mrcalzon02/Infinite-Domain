package infinitedomain.biomepreview;

import java.util.Locale;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.Mth;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.BiomeSource;
import net.minecraft.world.level.biome.Climate;
import net.minecraft.world.level.chunk.ChunkGenerator;

/** Samples the real resolved biome source; this class never asks for a chunk. */
final class BiomePreviewGenerator {
    static final int RADIUS_BLOCKS = 5_000;
    static final int SAMPLE_GRID = 129;
    static final int IMAGE_SIZE = 256;

    private BiomePreviewGenerator() {}

    static PreviewPayload generate(ServerLevel level) {
        BlockPos spawn = level.getSharedSpawnPos();
        ChunkGenerator generator = level.getChunkSource().getGenerator();
        BiomeSource biomeSource = generator.getBiomeSource();
        Climate.Sampler sampler = level.getChunkSource().randomState().sampler();
        int sampleY = generator.getSeaLevel();
        int quartY = QuartPos.fromBlock(sampleY);
        int[][] grid = new int[SAMPLE_GRID][SAMPLE_GRID];

        for (int gz = 0; gz < SAMPLE_GRID; gz++) {
            int blockZ = coordinate(spawn.getZ(), gz, SAMPLE_GRID);
            for (int gx = 0; gx < SAMPLE_GRID; gx++) {
                int blockX = coordinate(spawn.getX(), gx, SAMPLE_GRID);
                Holder<Biome> biome = biomeSource.getNoiseBiome(
                        QuartPos.fromBlock(blockX), quartY, QuartPos.fromBlock(blockZ), sampler);
                grid[gz][gx] = colorFor(biome);
            }
        }

        int[] pixels = interpolate(grid);
        decorate(pixels, IMAGE_SIZE, IMAGE_SIZE);
        return new PreviewPayload(
                IMAGE_SIZE,
                IMAGE_SIZE,
                RADIUS_BLOCKS,
                spawn.getX(),
                spawn.getZ(),
                sampleY,
                fingerprint(level.getSeed(), spawn),
                pixels);
    }

    static long fingerprint(long seed, BlockPos spawn) {
        long value = seed ^ 0x6A09E667F3BCC909L;
        value = Long.rotateLeft(value ^ spawn.getX(), 21);
        value = Long.rotateLeft(value ^ spawn.getZ(), 17);
        return value ^ 0xBB67AE8584CAA73BL;
    }

    private static int coordinate(int center, int index, int count) {
        double fraction = index / (double) (count - 1);
        return center - RADIUS_BLOCKS + (int) Math.round(fraction * RADIUS_BLOCKS * 2.0);
    }

    private static int[] interpolate(int[][] grid) {
        int[] pixels = new int[IMAGE_SIZE * IMAGE_SIZE];
        double maxGrid = SAMPLE_GRID - 1.0;
        for (int y = 0; y < IMAGE_SIZE; y++) {
            double gy = y * maxGrid / (IMAGE_SIZE - 1.0);
            int y0 = Math.min((int) gy, SAMPLE_GRID - 2);
            int y1 = y0 + 1;
            double ty = gy - y0;
            for (int x = 0; x < IMAGE_SIZE; x++) {
                double gx = x * maxGrid / (IMAGE_SIZE - 1.0);
                int x0 = Math.min((int) gx, SAMPLE_GRID - 2);
                int x1 = x0 + 1;
                double tx = gx - x0;
                int top = blend(grid[y0][x0], grid[y0][x1], tx);
                int bottom = blend(grid[y1][x0], grid[y1][x1], tx);
                pixels[y * IMAGE_SIZE + x] = blend(top, bottom, ty);
            }
        }
        return pixels;
    }

    private static int colorFor(Holder<Biome> holder) {
        ResourceLocation id = holder.unwrapKey().map(key -> key.location())
                .orElse(ResourceLocation.withDefaultNamespace("unknown"));
        String path = id.getPath().toLowerCase(Locale.ROOT);
        int color;

        if (path.contains("safe_zone")) color = 0x5E9B77;
        else if (containsAny(path, "hadal", "trench")) color = 0x071D37;
        else if (containsAny(path, "abyssal", "deep_ocean")) color = 0x123B5A;
        else if (containsAny(path, "fracture", "continental_slope")) color = 0x1A5870;
        else if (path.contains("ocean")) color = soften(holder.value().getWaterColor(), 0x287C9D, 0.60);
        else if (containsAny(path, "sulfur", "acid")) color = 0xB5A443;
        else if (containsAny(path, "radioactive", "toxic")) color = 0x788D3F;
        else if (containsAny(path, "city", "district", "industrial")) color = 0x6D6860;
        else if (containsAny(path, "apocalypse", "wasteland", "waste")) color = 0x78634A;
        else if (containsAny(path, "desert", "badlands")) color = 0xBA7744;
        else if (containsAny(path, "mountain", "upland", "peak", "slope")) color = 0x777B70;
        else if (containsAny(path, "frozen", "snow", "ice")) color = 0xC0D5D4;
        else if (containsAny(path, "jungle", "mangrove", "swamp")) color = 0x426A3B;
        else if (containsAny(path, "forest", "taiga", "grove")) color = soften(holder.value().getFoliageColor(), 0x48664A, 0.55);
        else if (containsAny(path, "plains", "meadow", "savanna", "steppe")) color = 0x89894E;
        else if (containsAny(path, "cave", "deep_dark")) color = 0x363F43;
        else color = soften(holder.value().getGrassColor(0.0, 0.0), 0x6F7653, 0.50);

        int variation = Math.floorMod(id.toString().hashCode(), 19) - 9;
        return shade(color, variation / 100.0);
    }

    private static boolean containsAny(String value, String... needles) {
        for (String needle : needles) {
            if (value.contains(needle)) return true;
        }
        return false;
    }

    private static int soften(int source, int anchor, double sourceWeight) {
        return blend(anchor, source & 0xFFFFFF, sourceWeight);
    }

    private static int blend(int first, int second, double amount) {
        double t = Mth.clamp(amount, 0.0, 1.0);
        int r = (int) Math.round(((first >> 16) & 255) * (1.0 - t) + ((second >> 16) & 255) * t);
        int g = (int) Math.round(((first >> 8) & 255) * (1.0 - t) + ((second >> 8) & 255) * t);
        int b = (int) Math.round((first & 255) * (1.0 - t) + (second & 255) * t);
        return 0xFF000000 | (r << 16) | (g << 8) | b;
    }

    private static int shade(int color, double amount) {
        double multiplier = 1.0 + amount;
        int r = Mth.clamp((int) Math.round(((color >> 16) & 255) * multiplier), 0, 255);
        int g = Mth.clamp((int) Math.round(((color >> 8) & 255) * multiplier), 0, 255);
        int b = Mth.clamp((int) Math.round((color & 255) * multiplier), 0, 255);
        return 0xFF000000 | (r << 16) | (g << 8) | b;
    }

    private static void decorate(int[] pixels, int width, int height) {
        int gridColor = 0x38212A2B;
        for (int kilometer = 1; kilometer < 10; kilometer++) {
            int line = (int) Math.round(kilometer * (width - 1) / 10.0);
            for (int p = 4; p < width - 4; p++) {
                pixels[line * width + p] = overlay(pixels[line * width + p], gridColor);
                pixels[p * width + line] = overlay(pixels[p * width + line], gridColor);
            }
        }

        int border = 0xFF171D1D;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (x < 4 || y < 4 || x >= width - 4 || y >= height - 4) {
                    pixels[y * width + x] = border;
                }
            }
        }

        int centerX = width / 2;
        int centerY = height / 2;
        int marker = 0xFFF2E5B5;
        int markerEdge = 0xFF342A20;
        for (int d = -6; d <= 6; d++) {
            set(pixels, width, centerX + d, centerY, markerEdge);
            set(pixels, width, centerX, centerY + d, markerEdge);
        }
        for (int d = -4; d <= 4; d++) {
            set(pixels, width, centerX + d, centerY, marker);
            set(pixels, width, centerX, centerY + d, marker);
        }

        // Small north pointer within the border.
        for (int row = 0; row < 8; row++) {
            for (int x = centerX - row; x <= centerX + row; x++) {
                set(pixels, width, x, 6 + row, marker);
            }
        }
    }

    private static int overlay(int base, int overlay) {
        double alpha = ((overlay >>> 24) & 255) / 255.0;
        return blend(base, overlay, alpha);
    }

    private static void set(int[] pixels, int width, int x, int y, int color) {
        if (x >= 0 && y >= 0 && x < width && y < pixels.length / width) {
            pixels[y * width + x] = color;
        }
    }
}

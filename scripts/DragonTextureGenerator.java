import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import javax.imageio.ImageIO;

/**
 * Produces UV-identical Darknet variants of the installed Ice and Fire dragon art.
 * The operation is deterministic so updated upstream textures can be regenerated.
 */
public final class DragonTextureGenerator {
    private DragonTextureGenerator() {}

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            throw new IllegalArgumentException("Usage: DragonTextureGenerator <source models dir> <output models dir>");
        }
        Path source = Path.of(args[0]);
        Path output = Path.of(args[1]);
        int[] count = {0};
        try (var paths = Files.walk(source)) {
            paths.filter(path -> path.toString().toLowerCase(Locale.ROOT).endsWith(".png"))
                .forEach(path -> {
                    try {
                        transform(path, output.resolve(source.relativize(path)));
                        count[0]++;
                    } catch (IOException exception) {
                        throw new RuntimeException(exception);
                    }
                });
        }
        System.out.println("Generated " + count[0] + " digitized dragon textures in " + output);
    }

    private static void transform(Path source, Path destination) throws IOException {
        BufferedImage input = ImageIO.read(source.toFile());
        BufferedImage output = new BufferedImage(input.getWidth(), input.getHeight(), BufferedImage.TYPE_INT_ARGB);
        String path = source.toString().toLowerCase(Locale.ROOT);
        int accent = path.contains("icedragon") ? 0x55D8FF : path.contains("lightningdragon") ? 0xE45CFF : 0xFF5538;
        int secondary = path.contains("icedragon") ? 0xD8F7FF : path.contains("lightningdragon") ? 0x69DBFF : 0xFFB04A;

        for (int y = 0; y < input.getHeight(); y++) {
            for (int x = 0; x < input.getWidth(); x++) {
                int argb = input.getRGB(x, y);
                int alpha = argb >>> 24;
                if (alpha == 0) {
                    output.setRGB(x, y, 0);
                    continue;
                }
                int red = (argb >>> 16) & 255;
                int green = (argb >>> 8) & 255;
                int blue = argb & 255;
                int luminance = (red * 54 + green * 183 + blue * 19) >>> 8;
                double shade = 0.20 + luminance / 510.0;
                int baseRed = clamp((int) (red * 0.48 + 45 * shade));
                int baseGreen = clamp((int) (green * 0.34 + 8 * shade));
                int baseBlue = clamp((int) (blue * 0.44 + 22 * shade));

                // Fine CRT scanlines, sparse packet faults, and circuit-like seams.
                if ((y & 3) == 3) {
                    baseRed = baseRed * 72 / 100;
                    baseGreen = baseGreen * 72 / 100;
                    baseBlue = baseBlue * 72 / 100;
                }
                int noise = hash(x, y, source.getFileName().toString().hashCode());
                boolean seam = (noise & 1023) < 8 && luminance > 24;
                boolean packet = y % 29 == 7 && (noise & 31) < 5 && luminance > 18;
                if (seam || packet) {
                    int glow = seam ? accent : secondary;
                    int amount = seam ? 78 : 58;
                    baseRed = mix(baseRed, (glow >>> 16) & 255, amount);
                    baseGreen = mix(baseGreen, (glow >>> 8) & 255, amount);
                    baseBlue = mix(baseBlue, glow & 255, amount);
                }
                output.setRGB(x, y, (alpha << 24) | (baseRed << 16) | (baseGreen << 8) | baseBlue);
            }
        }
        Files.createDirectories(destination.getParent());
        ImageIO.write(output, "png", destination.toFile());
    }

    private static int hash(int x, int y, int seed) {
        int value = seed ^ (x * 0x45d9f3b) ^ (y * 0x119de1f3);
        value ^= value >>> 16;
        value *= 0x45d9f3b;
        return value ^ (value >>> 16);
    }

    private static int mix(int from, int to, int percent) {
        return clamp((from * (100 - percent) + to * percent) / 100);
    }

    private static int clamp(int value) {
        return Math.max(0, Math.min(255, value));
    }
}

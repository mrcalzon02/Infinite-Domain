import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import javax.imageio.ImageIO;

/** Recolors exact Ice and Fire UV sheets; never invents or rearranges UV islands. */
public final class DatavoreSkinGenerator {
    private DatavoreSkinGenerator() {}

    public static void main(String[] args) throws IOException {
        if (args.length != 2) throw new IllegalArgumentException("Usage: DatavoreSkinGenerator <source-dir> <output-dir>");
        Path source = Path.of(args[0]), output = Path.of(args[1]);
        Files.createDirectories(output);
        transform(source.resolve("electric_5.png"), output.resolve("datavore.png"), false);
        transform(source.resolve("electric_5_eyes.png"), output.resolve("datavore_eyes.png"), true);
        transform(source.resolve("lightning_skeleton_5.png"), output.resolve("datavore_skeleton.png"), false);
        System.out.println("Generated exact-UV Datavore body, eyes, and skeleton textures in " + output);
    }

    private static void transform(Path inputPath, Path outputPath, boolean eyes) throws IOException {
        BufferedImage input = ImageIO.read(inputPath.toFile());
        BufferedImage output = new BufferedImage(input.getWidth(), input.getHeight(), BufferedImage.TYPE_INT_ARGB);
        int seed = inputPath.getFileName().toString().hashCode();
        for (int y = 0; y < input.getHeight(); y++) for (int x = 0; x < input.getWidth(); x++) {
            int argb = input.getRGB(x, y), alpha = argb >>> 24;
            if (alpha == 0) continue;
            int r = argb >>> 16 & 255, g = argb >>> 8 & 255, b = argb & 255;
            int lum = (r * 54 + g * 183 + b * 19) >>> 8;
            int hash = seed ^ x * 0x45d9f3b ^ y * 0x119de1f3;
            hash ^= hash >>> 16;
            int nr = Math.min(255, 18 + lum * (eyes ? 2 : 3) / 4);
            int ng = Math.min(255, 2 + lum / (eyes ? 3 : 9));
            int nb = Math.min(255, 12 + lum * (eyes ? 2 : 1) / 3);
            if ((hash & 511) < 9 || (y % 31 == 11 && (hash & 15) < 3)) {
                nr = 245; ng = (hash & 1) == 0 ? 24 : 52; nb = (hash & 1) == 0 ? 118 : 240;
            } else if ((y & 3) == 3) {
                nr = nr * 70 / 100; ng = ng * 70 / 100; nb = nb * 70 / 100;
            }
            output.setRGB(x, y, alpha << 24 | nr << 16 | ng << 8 | nb);
        }
        ImageIO.write(output, "png", outputPath.toFile());
    }
}

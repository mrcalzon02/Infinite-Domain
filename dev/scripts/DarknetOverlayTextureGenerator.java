import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import javax.imageio.ImageIO;

/** Builds sparse transparent circuitry and an eight-frame crimson shimmer. */
public final class DarknetOverlayTextureGenerator {
    private DarknetOverlayTextureGenerator() {}

    public static void main(String[] args) throws IOException {
        if (args.length != 1) throw new IllegalArgumentException("Usage: DarknetOverlayTextureGenerator <output-dir>");
        Path output = Path.of(args[0]);
        Files.createDirectories(output);
        ImageIO.write(circuitry(), "png", output.resolve("darknet_overlay_static.png").toFile());
        ImageIO.write(shimmer(), "png", output.resolve("darknet_overlay_shimmer.png").toFile());
        System.out.println("Generated Darknet entity overlay textures in " + output);
    }

    private static BufferedImage circuitry() {
        BufferedImage image = new BufferedImage(64, 64, BufferedImage.TYPE_INT_ARGB);
        int[][] starts = {{2,7},{18,1},{39,4},{57,0},{5,27},{23,20},{47,23},{1,49},{29,42},{52,45},{13,61},{42,59}};
        for (int i = 0; i < starts.length; i++) {
            int x = starts[i][0], y = starts[i][1];
            int seed = 17 + i * 31;
            for (int segment = 0; segment < 4; segment++) {
                int length = 3 + Math.floorMod(seed + segment * 7, 8);
                boolean horizontal = ((seed >>> segment) & 1) == 0;
                for (int step = 0; step < length; step++) {
                    set(image, x, y, 0x786A0616);
                    if ((step + segment) % 5 == 0) set(image, x, y, 0xA0C51B36);
                    x = Math.floorMod(x + (horizontal ? 1 : 0), 64);
                    y = Math.floorMod(y + (horizontal ? 0 : 1), 64);
                }
                set(image, x, y, 0xB0F0445E);
                seed = seed * 1103515245 + 12345;
            }
        }
        return image;
    }

    private static BufferedImage shimmer() {
        BufferedImage image = new BufferedImage(64, 64 * 8, BufferedImage.TYPE_INT_ARGB);
        for (int frame = 0; frame < 8; frame++) {
            for (int y = 0; y < 64; y++) {
                for (int x = 0; x < 64; x++) {
                    int diagonal = Math.floorMod(x + y * 2 - frame * 9, 43);
                    if (diagonal < 2) set(image, x, frame * 64 + y, diagonal == 0 ? 0x58FF3554 : 0x30A80D27);
                    if (Math.floorMod(x * 13 + y * 7 + frame * 11, 257) == 0) set(image, x, frame * 64 + y, 0x7AFF7188);
                }
            }
        }
        return image;
    }

    private static void set(BufferedImage image, int x, int y, int argb) {
        image.setRGB(x, y, argb);
    }
}

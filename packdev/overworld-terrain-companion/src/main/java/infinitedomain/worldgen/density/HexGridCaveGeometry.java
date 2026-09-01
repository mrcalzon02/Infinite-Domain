package infinitedomain.worldgen.density;

/** Pure geometry for the Wasteland's literal honeycomb cave network. */
public final class HexGridCaveGeometry {
    private static final double SQRT_3 = Math.sqrt(3.0);
    private static final double HEX_NORMAL_X = SQRT_3 * 0.5;

    private HexGridCaveGeometry() {}

    public static double sample(
            int blockX,
            int blockY,
            int blockZ,
            double cellRadius,
            double corridorHalfWidth,
            double chamberRadius,
            int layerSpacing,
            int layerOffset,
            double layerHalfHeight,
            int minY,
            int maxY,
            double originExclusionRadius,
            double feather
    ) {
        if (blockY < minY || blockY > maxY
                || Math.hypot(blockX, blockZ) < originExclusionRadius) {
            return 1.0;
        }

        Axial cell = nearestCell(blockX, blockZ, cellRadius);
        double centerX = cellRadius * 1.5 * cell.q();
        double centerZ = cellRadius * SQRT_3 * (cell.r() + cell.q() * 0.5);
        double localX = blockX - centerX;
        double localZ = blockZ - centerZ;

        // Nearest-cell folding makes the zero contour an exact repeated regular
        // hexagon. A narrow band inside that contour becomes the corridor loop;
        // a smaller concentric hexagon becomes the recognizable cell chamber.
        double outerHex = signedHex(localX, localZ, cellRadius);
        double edgeCorridor = -outerHex - corridorHalfWidth;
        double chamber = signedHex(localX, localZ, chamberRadius);
        double horizontal = Math.min(edgeCorridor, chamber);

        long layerIndex = Math.round((blockY - (double) layerOffset) / layerSpacing);
        double layerCenter = layerOffset + layerIndex * (double) layerSpacing;
        double vertical = Math.abs(blockY - layerCenter) - layerHalfHeight;

        return clamp(Math.max(horizontal, vertical) / feather, -1.0, 1.0);
    }

    private static double signedHex(double x, double z, double radius) {
        double ax = Math.abs(x);
        double az = Math.abs(z);
        double apothem = radius * HEX_NORMAL_X;
        return Math.max(ax * HEX_NORMAL_X + az * 0.5, az) - apothem;
    }

    private static Axial nearestCell(double x, double z, double radius) {
        double q = (2.0 / 3.0 * x) / radius;
        double r = (-x / 3.0 + SQRT_3 / 3.0 * z) / radius;
        double cubeX = q;
        double cubeZ = r;
        double cubeY = -cubeX - cubeZ;

        long roundedX = Math.round(cubeX);
        long roundedY = Math.round(cubeY);
        long roundedZ = Math.round(cubeZ);
        double dx = Math.abs(roundedX - cubeX);
        double dy = Math.abs(roundedY - cubeY);
        double dz = Math.abs(roundedZ - cubeZ);
        if (dx > dy && dx > dz) {
            roundedX = -roundedY - roundedZ;
        } else if (dy > dz) {
            roundedY = -roundedX - roundedZ;
        } else {
            roundedZ = -roundedX - roundedY;
        }
        return new Axial(roundedX, roundedZ);
    }

    private static double clamp(double value, double minimum, double maximum) {
        return Math.max(minimum, Math.min(maximum, value));
    }

    private record Axial(long q, long r) {}
}

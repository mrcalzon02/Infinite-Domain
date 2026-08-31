package infinitedomain.hiveworld.worldgen;

/** Shared deterministic cell centres and geometry for Stack and Trunk fields. */
final class HiveMacroLayout {
    private HiveMacroLayout() {}

    static int containingCell(int coordinate, int cellSize) {
        return Math.floorDiv(coordinate + cellSize / 2, cellSize);
    }

    static Point centre(int cellX, int cellZ, int cellSize, double jitter, int salt) {
        // The origin is the canonical central Spire. All other cells receive stable
        // offsets while retaining the accepted 2,000-4,000 block separation range.
        if (cellX == 0 && cellZ == 0) return new Point(0.0, 0.0);
        long h = mix(((long) cellX << 32) ^ (cellZ & 0xFFFFFFFFL) ^ salt);
        long h2 = mix(h ^ 0x9E3779B97F4A7C15L);
        double ox = signedUnit(h) * jitter * cellSize;
        double oz = signedUnit(h2) * jitter * cellSize;
        return new Point(cellX * (double) cellSize + ox, cellZ * (double) cellSize + oz);
    }

    static double distanceToSegment(double px, double pz, Point a, Point b) {
        double dx = b.x() - a.x();
        double dz = b.z() - a.z();
        double lengthSquared = dx * dx + dz * dz;
        if (lengthSquared <= 1.0e-9) return Math.hypot(px - a.x(), pz - a.z());
        double t = ((px - a.x()) * dx + (pz - a.z()) * dz) / lengthSquared;
        t = Math.max(0.0, Math.min(1.0, t));
        double qx = a.x() + t * dx;
        double qz = a.z() + t * dz;
        return Math.hypot(px - qx, pz - qz);
    }

    static double stackValue(int x, int y, int z, int cellSize, double radius,
                             double jitter, double verticalTaper, int salt) {
        int cellX = containingCell(x, cellSize);
        int cellZ = containingCell(z, cellSize);
        double nearest = Double.POSITIVE_INFINITY;
        for (int dz = -1; dz <= 1; dz++) {
            for (int dx = -1; dx <= 1; dx++) {
                Point centre = centre(cellX + dx, cellZ + dz, cellSize, jitter, salt);
                nearest = Math.min(nearest, Math.hypot(x - centre.x(), z - centre.z()));
            }
        }
        double height = Math.max(0.0, Math.min(1.0, y / 607.0));
        double effectiveRadius = radius * (1.0 - verticalTaper * height);
        return Math.max(-1.0, Math.min(1.0, 1.0 - nearest / effectiveRadius));
    }

    static double trunkValue(int x, int z, int cellSize, double halfWidth,
                             double jitter, int salt) {
        int cellX = containingCell(x, cellSize);
        int cellZ = containingCell(z, cellSize);
        double nearest = Double.POSITIVE_INFINITY;
        for (int dz = -1; dz <= 1; dz++) {
            for (int dx = -1; dx <= 1; dx++) {
                int gx = cellX + dx;
                int gz = cellZ + dz;
                Point origin = centre(gx, gz, cellSize, jitter, salt);
                Point east = centre(gx + 1, gz, cellSize, jitter, salt);
                Point south = centre(gx, gz + 1, cellSize, jitter, salt);
                nearest = Math.min(nearest, distanceToSegment(x, z, origin, east));
                nearest = Math.min(nearest, distanceToSegment(x, z, origin, south));
            }
        }
        return Math.max(-1.0, Math.min(1.0, 1.0 - nearest / halfWidth));
    }

    private static long mix(long value) {
        value ^= value >>> 30;
        value *= 0xBF58476D1CE4E5B9L;
        value ^= value >>> 27;
        value *= 0x94D049BB133111EBL;
        return value ^ (value >>> 31);
    }

    private static double signedUnit(long value) {
        return ((value >>> 11) * 0x1.0p-53) * 2.0 - 1.0;
    }

    record Point(double x, double z) {}
}

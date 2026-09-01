package infinitedomain.hiveworld.worldgen;

/** Executable geometry contract run by the companion build; not a runtime event. */
public final class HiveMacroLayoutSelfTest {
    private static final int CELL_SIZE = 3072;
    private static final double RADIUS = 520.0;
    private static final double JITTER = 0.15;
    private static final double TRUNK_HALF_WIDTH = 14.0;
    private static final int SALT = 927133;

    private HiveMacroLayoutSelfTest() {}

    public static void main(String[] args) {
        require(HiveMacroLayout.stackValue(0, 0, 0, CELL_SIZE, RADIUS, JITTER, 0.45, SALT) > 0.999,
                "origin is not the central Stack centre");
        require(Math.abs(HiveMacroLayout.stackValue(
                520, 0, 0, CELL_SIZE, RADIUS, JITTER, 0.45, SALT)) < 0.001,
                "base core radius is not 520 blocks");
        require(Math.abs(HiveMacroLayout.stackValue(
                286, 607, 0, CELL_SIZE, RADIUS, JITTER, 0.45, SALT)) < 0.01,
                "Crown taper does not reach the expected ~286-block radius");

        double minSeparation = Double.POSITIVE_INFINITY;
        double maxSeparation = 0.0;
        for (int z = -6; z <= 6; z++) {
            for (int x = -6; x <= 6; x++) {
                HiveMacroLayout.Point origin = HiveMacroLayout.centre(x, z, CELL_SIZE, JITTER, SALT);
                for (HiveMacroLayout.Point neighbour : new HiveMacroLayout.Point[] {
                        HiveMacroLayout.centre(x + 1, z, CELL_SIZE, JITTER, SALT),
                        HiveMacroLayout.centre(x, z + 1, CELL_SIZE, JITTER, SALT)}) {
                    double separation = Math.hypot(
                            neighbour.x() - origin.x(), neighbour.z() - origin.z());
                    minSeparation = Math.min(minSeparation, separation);
                    maxSeparation = Math.max(maxSeparation, separation);
                    for (int step = 0; step <= 64; step++) {
                        double t = step / 64.0;
                        int px = (int) Math.round(origin.x() +
                                (neighbour.x() - origin.x()) * t);
                        int pz = (int) Math.round(origin.z() +
                                (neighbour.z() - origin.z()) * t);
                        require(HiveMacroLayout.trunkValue(
                                px, pz, CELL_SIZE, TRUNK_HALF_WIDTH, JITTER, SALT) > 0.85,
                                "Trunk field breaks along a neighbour route");
                    }
                }
                require(HiveMacroLayout.trunkValue(
                        (int) Math.round(origin.x()), (int) Math.round(origin.z()),
                        CELL_SIZE, TRUNK_HALF_WIDTH, JITTER, SALT) > 0.90,
                        "Trunk field does not terminate at a Stack centre");
            }
        }
        require(minSeparation >= 2000.0, "minimum Stack separation below 2,000: " + minSeparation);
        require(maxSeparation <= 4000.0, "maximum Stack separation above 4,000: " + maxSeparation);

        double apronRadius = RADIUS * 1.35;
        double cellArea = CELL_SIZE * (double) CELL_SIZE;
        double apronShare = Math.PI * apronRadius * apronRadius / cellArea;
        // Conservatively count one complete east and one complete south strip per
        // cell. Their intersection and the portions inside aprons are deliberately
        // not subtracted, making this a lower bound on true exposed-waste share.
        double trunkShareUpperBound = 2.0 * (2.0 * TRUNK_HALF_WIDTH * CELL_SIZE) / cellArea;
        double wasteShareLowerBound = 1.0 - apronShare - trunkShareUpperBound;
        require(wasteShareLowerBound >= 0.70,
                "conservative dead-waste share below 70%: " + wasteShareLowerBound);
        System.out.printf("PASS - macro layout: separation %.1f..%.1f, conservative wastes >= %.1f%%%n",
                minSeparation, maxSeparation, wasteShareLowerBound * 100.0);
    }

    private static void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
}

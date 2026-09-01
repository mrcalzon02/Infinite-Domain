package infinitedomain.worldgen.density;

/** Dependency-free build-time regression checks for the cave signed-distance field. */
public final class HexGridCaveGeometrySelfTest {
    private static final double RADIUS = 48.0;
    private static final double APOTHEM = RADIUS * Math.sqrt(3.0) * 0.5;

    private HexGridCaveGeometrySelfTest() {}

    private static double sample(int x, int y, int z) {
        return HexGridCaveGeometry.sample(
                x, y, z, RADIUS, 4.0, 12.0,
                44, -40, 5.0, -48, 58, 288.0, 4.0
        );
    }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    public static void main(String[] args) {
        // Axial cell (q=14, r=-7): exact center (1008, 0), safely beyond
        // the protected origin radius.
        int remoteX = 1008;
        require(sample(remoteX, 4, 0) < 0.0, "hexagonal chamber center must carve");
        require(sample(remoteX, 4, (int) Math.round(APOTHEM)) < 0.0,
                "hexagonal cell boundary must form a corridor");
        require(sample(remoteX, 4, 24) > 0.0,
                "wall between chamber and edge corridor must remain solid");
        require(sample(remoteX, 26, 0) > 0.0,
                "rock band between cave layers must remain solid");
        require(sample(remoteX, 70, 0) > 0.0,
                "geometry must stop above the configured cave envelope");
        require(sample(0, 4, 0) > 0.0,
                "spawn-hospital exclusion must remain solid");

        int neighbourX = remoteX + (int) Math.round(RADIUS * 1.5);
        int neighbourZ = (int) Math.round(APOTHEM);
        require(sample(neighbourX, 4, neighbourZ) < 0.0,
                "adjacent axial cell chamber must repeat exactly");
        System.out.println("Wasteland hex-grid geometry self-test passed.");
    }
}

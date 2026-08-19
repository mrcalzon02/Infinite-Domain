import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public final class CyberwareTextureGenerator {
    private static final String[][] IDS = {
        {"fragmented_coprocessor", "reclaimed_reflex_cache", "calibrated_cortex_mesh", "darknet_ghost_coprocessor"},
        {"cracked_optic_rig", "reclaimed_spectrum_array", "calibrated_horizon_lens", "darknet_omnivision_array"},
        {"arrhythmic_aux_pump", "reclaimed_platelet_engine", "calibrated_aortic_turbine", "darknet_phylactery_pump"},
        {"leaky_oxygen_baffle", "reclaimed_gill_exchanger", "calibrated_hyperlung", "darknet_void_breather"},
        {"fouled_nutrient_reclaimer", "reclaimed_chem_filter", "calibrated_metabolic_forge", "darknet_entropy_gut"},
        {"seized_rightarm_servo", "reclaimed_rightarm_tooling", "calibrated_rightarm_mantis_drive", "darknet_rightarm_arc_limb"},
        {"seized_leftarm_servo", "reclaimed_leftarm_tooling", "calibrated_leftarm_mantis_drive", "darknet_leftarm_arc_limb"},
        {"bent_rightleg_actuator", "reclaimed_rightleg_tendon", "calibrated_rightleg_vector_drive", "darknet_rightleg_blink_stride"},
        {"bent_leftleg_actuator", "reclaimed_leftleg_tendon", "calibrated_leftleg_vector_drive", "darknet_leftleg_blink_stride"},
        {"frayed_myomer_bundle", "reclaimed_torque_fiber", "calibrated_reflex_myomer", "darknet_sandevistan_mesh"},
        {"warped_lattice_splint", "reclaimed_capacitor_frame", "calibrated_gravitic_lacing", "darknet_singularity_skeleton"},
        {"patchwork_dermal_mesh", "reclaimed_reactive_dermis", "calibrated_ablative_skin", "darknet_nullweave"}
    };
    private static final String[] BASE = {
        "brainupgrades_neuralprocessor", "eyeupgrades_targeting", "heartupgrades_platelets",
        "lungsupgrades_hyperoxygenation", "organsupgrades_metabolic", "basecyberware_rightarm_ironplated",
        "basecyberware_leftarm_ironplated", "basecyberware_rightleg_ironplated", "basecyberware_leftleg_ironplated",
        "muscleupgrades_wiredreflexes", "boneupgrades_bonelacing", "skinupgrades_subdermalarmor"
    };
    private static final String[] COMPONENTS = {
        "frayed_neural_bus", "cracked_optic_array", "arrhythmic_pump_core", "punctured_air_cell",
        "fouled_metabolic_mesh", "seized_rightarm_cluster", "seized_leftarm_cluster", "bent_rightleg_pair",
        "bent_leftleg_pair", "torn_myomer_bundle", "warped_frame_strut", "delaminated_dermis",
        "ghost_circuit_lattice", "quantum_synapse_matrix", "void_shield_mesh", "datavore_control_core"
    };
    private static final String[] COMPONENT_BASE = {
        "component_fiberoptics", "component_fiberoptics", "component_storage", "component_storage",
        "component_mesh", "component_actuator", "component_actuator", "component_actuator",
        "component_actuator", "component_synthnerves", "component_plating", "component_mesh",
        "component_wiring", "component_ssd", "component_mesh", "component_storage"
    };

    public static void main(String[] args) throws Exception {
        Path jar = Path.of(args[0]);
        Path output = Path.of(args[1]);
        Files.createDirectories(output);
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            for (int region = 0; region < IDS.length; region++) {
                BufferedImage source = read(zip, BASE[region]);
                for (int tier = 0; tier < 4; tier++) {
                    ImageIO.write(transform(source, tier, region), "png", output.resolve(IDS[region][tier] + ".png").toFile());
                }
            }
            for (int index = 0; index < COMPONENTS.length; index++) {
                ImageIO.write(transform(read(zip, COMPONENT_BASE[index]), index < 12 ? 0 : 3, index), "png", output.resolve(COMPONENTS[index] + ".png").toFile());
            }
        }
        System.out.println("Generated 64 Create Cybernetics-derived textures in " + output);
    }

    private static BufferedImage read(ZipFile zip, String name) throws IOException {
        ZipEntry entry = zip.getEntry("assets/createcybernetics/textures/item/" + name + ".png");
        if (entry == null) throw new IOException("Missing source texture " + name);
        return ImageIO.read(zip.getInputStream(entry));
    }

    private static BufferedImage transform(BufferedImage source, int tier, int seed) {
        BufferedImage out = new BufferedImage(source.getWidth(), source.getHeight(), BufferedImage.TYPE_INT_ARGB);
        int[][] accent = {{156, 48, 35}, {199, 137, 52}, {35, 207, 222}, {182, 42, 255}};
        for (int y = 0; y < source.getHeight(); y++) for (int x = 0; x < source.getWidth(); x++) {
            int argb = source.getRGB(x, y), a = argb >>> 24;
            if (a == 0) continue;
            int r = (argb >>> 16) & 255, g = (argb >>> 8) & 255, b = argb & 255;
            int lum = (r * 3 + g * 6 + b) / 10;
            double blend = new double[]{0.34, 0.27, 0.39, 0.50}[tier];
            if (tier == 0) lum = (int)(lum * 0.66);
            r = clamp((int)(lum * (1 - blend) + accent[tier][0] * blend));
            g = clamp((int)(lum * (1 - blend) + accent[tier][1] * blend));
            b = clamp((int)(lum * (1 - blend) + accent[tier][2] * blend));
            if (tier == 0 && ((x * 5 + y * 3 + seed) % 17 == 0)) { r = 220; g = 52; b = 30; }
            if (tier == 1 && ((x + y * 2 + seed) % 19 == 0)) { r = 238; g = 188; b = 91; }
            if (tier == 2 && ((x + y + seed) % 11 == 0)) { r = 150; g = 255; b = 255; }
            if (tier == 3 && ((x * 3 + y + seed) % 9 == 0)) { r = 30; g = 240; b = 255; }
            out.setRGB(x, y, (a << 24) | (r << 16) | (g << 8) | b);
        }
        return out;
    }

    private static int clamp(int value) { return Math.max(0, Math.min(255, value)); }
}

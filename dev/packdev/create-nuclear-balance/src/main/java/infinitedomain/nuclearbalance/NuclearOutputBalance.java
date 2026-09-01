package infinitedomain.nuclearbalance;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.neoforged.fml.loading.FMLPaths;

import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;

public final class NuclearOutputBalance {
    private static final double DEFAULT_CAPACITY_PER_RPM = 1024.0D;

    private NuclearOutputBalance() {
    }

    public static double capacityPerRpm(double installedValue) {
        Path config = FMLPaths.GAMEDIR.get()
            .resolve("kubejs")
            .resolve("config")
            .resolve("nuclear_fuel_cycle.json");

        try (Reader reader = Files.newBufferedReader(config)) {
            JsonObject root = JsonParser.parseReader(reader).getAsJsonObject();
            JsonObject output = root.getAsJsonObject("reactorOutput");
            double configured = output.get("stressCapacityPerRpm").getAsDouble();
            if (Double.isFinite(configured) && configured > 0.0D && configured <= installedValue) {
                return configured;
            }
        } catch (Exception exception) {
            System.err.println("[Infinite Domain Nuclear Balance] Could not read " + config + ": " + exception.getMessage());
        }

        return Math.min(DEFAULT_CAPACITY_PER_RPM, installedValue);
    }
}

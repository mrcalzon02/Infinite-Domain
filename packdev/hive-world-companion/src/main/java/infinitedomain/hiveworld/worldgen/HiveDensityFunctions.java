package infinitedomain.hiveworld.worldgen;

import com.mojang.serialization.MapCodec;
import infinitedomain.hiveworld.HiveWorldCompanion;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.DensityFunction;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Registers deterministic Hive macro-layout density functions on both sides. */
public final class HiveDensityFunctions {
    private static final DeferredRegister<MapCodec<? extends DensityFunction>> TYPES =
            DeferredRegister.create(Registries.DENSITY_FUNCTION_TYPE, HiveWorldCompanion.MOD_ID);

    static {
        TYPES.register("stack_field", () -> HiveStackField.DATA_CODEC);
        TYPES.register("trunk_axis", () -> HiveTrunkAxis.DATA_CODEC);
    }

    private HiveDensityFunctions() {}

    public static void register(IEventBus modBus) {
        TYPES.register(modBus);
    }
}

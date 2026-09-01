package infinitedomain.worldgen.density;

import com.mojang.serialization.MapCodec;
import infinitedomain.worldgen.InfiniteDomainWorldgen;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.DensityFunction;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Registers server-authoritative Overworld density-function codecs. */
public final class OverworldDensityFunctions {
    private static final DeferredRegister<MapCodec<? extends DensityFunction>> TYPES =
            DeferredRegister.create(Registries.DENSITY_FUNCTION_TYPE, InfiniteDomainWorldgen.MOD_ID);

    static {
        TYPES.register("hex_grid_cave", () -> WastelandHexGridCave.DATA_CODEC);
    }

    private OverworldDensityFunctions() {}

    public static void register(IEventBus modBus) {
        TYPES.register(modBus);
    }
}

package infinitedomain.hiveworld.worldgen;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.KeyDispatchDataCodec;
import net.minecraft.world.level.levelgen.DensityFunction;

/** Continuous route field connecting every Stack cell to its east and south neighbours. */
public record HiveTrunkAxis(int cellSize, double halfWidth, double jitter, int salt)
        implements DensityFunction.SimpleFunction {
    public static final MapCodec<HiveTrunkAxis> DATA_CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(
                    Codec.intRange(1024, 8192).fieldOf("cell_size").forGetter(HiveTrunkAxis::cellSize),
                    Codec.doubleRange(4.0, 64.0).fieldOf("half_width").forGetter(HiveTrunkAxis::halfWidth),
                    Codec.doubleRange(0.0, 0.45).fieldOf("jitter").forGetter(HiveTrunkAxis::jitter),
                    Codec.INT.optionalFieldOf("salt", 927133).forGetter(HiveTrunkAxis::salt)
            ).apply(instance, HiveTrunkAxis::new));
    private static final KeyDispatchDataCodec<HiveTrunkAxis> CODEC =
            KeyDispatchDataCodec.of(DATA_CODEC);

    @Override
    public double compute(FunctionContext context) {
        return HiveMacroLayout.trunkValue(context.blockX(), context.blockZ(),
                cellSize, halfWidth, jitter, salt);
    }

    @Override public double minValue() { return -1.0; }
    @Override public double maxValue() { return 1.0; }
    @Override public KeyDispatchDataCodec<? extends DensityFunction> codec() { return CODEC; }
}

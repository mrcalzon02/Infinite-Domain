package infinitedomain.hiveworld.worldgen;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.KeyDispatchDataCodec;
import net.minecraft.world.level.levelgen.DensityFunction;

/** Signed radial Stack field: positive core, shallow negative apron, -1 wastes. */
public record HiveStackField(int cellSize, double radius, double jitter,
                             double verticalTaper, int salt)
        implements DensityFunction.SimpleFunction {
    public static final MapCodec<HiveStackField> DATA_CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(
                    Codec.intRange(1024, 8192).fieldOf("cell_size").forGetter(HiveStackField::cellSize),
                    Codec.doubleRange(128.0, 1536.0).fieldOf("radius").forGetter(HiveStackField::radius),
                    Codec.doubleRange(0.0, 0.45).fieldOf("jitter").forGetter(HiveStackField::jitter),
                    Codec.doubleRange(0.0, 0.75).fieldOf("vertical_taper").forGetter(HiveStackField::verticalTaper),
                    Codec.INT.optionalFieldOf("salt", 927133).forGetter(HiveStackField::salt)
            ).apply(instance, HiveStackField::new));
    private static final KeyDispatchDataCodec<HiveStackField> CODEC =
            KeyDispatchDataCodec.of(DATA_CODEC);

    @Override
    public double compute(FunctionContext context) {
        return HiveMacroLayout.stackValue(context.blockX(), context.blockY(), context.blockZ(),
                cellSize, radius, jitter, verticalTaper, salt);
    }

    @Override public double minValue() { return -1.0; }
    @Override public double maxValue() { return 1.0; }
    @Override public KeyDispatchDataCodec<? extends DensityFunction> codec() { return CODEC; }
}

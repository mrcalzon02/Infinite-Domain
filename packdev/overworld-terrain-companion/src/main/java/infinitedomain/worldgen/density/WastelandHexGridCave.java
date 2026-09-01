package infinitedomain.worldgen.density;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.KeyDispatchDataCodec;
import net.minecraft.world.level.levelgen.DensityFunction;

/** Signed 3D field for repeated, layered hexagonal corridors and chambers. */
public record WastelandHexGridCave(
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
) implements DensityFunction.SimpleFunction {
    public static final MapCodec<WastelandHexGridCave> DATA_CODEC = RecordCodecBuilder.mapCodec(instance ->
            instance.group(
                    Codec.doubleRange(24.0, 128.0).fieldOf("cell_radius").forGetter(WastelandHexGridCave::cellRadius),
                    Codec.doubleRange(2.0, 10.0).fieldOf("corridor_half_width").forGetter(WastelandHexGridCave::corridorHalfWidth),
                    Codec.doubleRange(4.0, 24.0).fieldOf("chamber_radius").forGetter(WastelandHexGridCave::chamberRadius),
                    Codec.intRange(24, 96).fieldOf("layer_spacing").forGetter(WastelandHexGridCave::layerSpacing),
                    Codec.intRange(-128, 256).fieldOf("layer_offset").forGetter(WastelandHexGridCave::layerOffset),
                    Codec.doubleRange(2.0, 12.0).fieldOf("layer_half_height").forGetter(WastelandHexGridCave::layerHalfHeight),
                    Codec.intRange(-64, 256).fieldOf("min_y").forGetter(WastelandHexGridCave::minY),
                    Codec.intRange(-64, 320).fieldOf("max_y").forGetter(WastelandHexGridCave::maxY),
                    Codec.doubleRange(0.0, 1024.0).fieldOf("origin_exclusion_radius").forGetter(WastelandHexGridCave::originExclusionRadius),
                    Codec.doubleRange(1.0, 16.0).fieldOf("feather").forGetter(WastelandHexGridCave::feather)
            ).apply(instance, WastelandHexGridCave::new));
    private static final KeyDispatchDataCodec<WastelandHexGridCave> CODEC =
            KeyDispatchDataCodec.of(DATA_CODEC);

    @Override
    public double compute(FunctionContext context) {
        return HexGridCaveGeometry.sample(
                context.blockX(), context.blockY(), context.blockZ(),
                cellRadius, corridorHalfWidth, chamberRadius,
                layerSpacing, layerOffset, layerHalfHeight,
                minY, maxY, originExclusionRadius, feather
        );
    }

    @Override public double minValue() { return -1.0; }
    @Override public double maxValue() { return 1.0; }
    @Override public KeyDispatchDataCodec<? extends DensityFunction> codec() { return CODEC; }
}

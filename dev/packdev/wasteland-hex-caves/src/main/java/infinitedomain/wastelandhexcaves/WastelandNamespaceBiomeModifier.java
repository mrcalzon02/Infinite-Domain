package infinitedomain.wastelandhexcaves;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.Holder;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.neoforged.neoforge.common.world.BiomeModifier;
import net.neoforged.neoforge.common.world.ModifiableBiomeInfo;

import java.util.Set;

public record WastelandNamespaceBiomeModifier(Holder<PlacedFeature> feature) implements BiomeModifier {
    private static final Set<String> WASTELAND_NAMESPACES = Set.of(
            "the_wasteland_reworked",
            "wastelands"
    );

    public static final MapCodec<WastelandNamespaceBiomeModifier> CODEC =
            RecordCodecBuilder.mapCodec(instance -> instance.group(
                    PlacedFeature.CODEC.fieldOf("feature")
                            .forGetter(WastelandNamespaceBiomeModifier::feature)
            ).apply(instance, WastelandNamespaceBiomeModifier::new));

    @Override
    public void modify(
            Holder<Biome> biome,
            Phase phase,
            ModifiableBiomeInfo.BiomeInfo.Builder builder
    ) {
        if (phase != Phase.ADD) {
            return;
        }

        biome.unwrapKey().ifPresent(key -> {
            if (WASTELAND_NAMESPACES.contains(key.location().getNamespace())) {
                builder.getGenerationSettings().addFeature(
                        GenerationStep.Decoration.UNDERGROUND_DECORATION,
                        feature
                );
            }
        });
    }

    @Override
    public MapCodec<? extends BiomeModifier> codec() {
        return WastelandHexCaves.WASTELAND_NAMESPACE_MODIFIER.get();
    }
}

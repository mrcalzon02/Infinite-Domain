package infinitedomain.wastelandhexcaves;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.world.BiomeModifier;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.function.Supplier;

@Mod(WastelandHexCaves.MOD_ID)
public final class WastelandHexCaves {
    public static final String MOD_ID = "infinite_domain_wasteland_hex_caves";

    private static final DeferredRegister<Feature<?>> FEATURES =
            DeferredRegister.create(BuiltInRegistries.FEATURE, MOD_ID);

    private static final DeferredRegister<MapCodec<? extends BiomeModifier>> BIOME_MODIFIER_SERIALIZERS =
            DeferredRegister.create(NeoForgeRegistries.Keys.BIOME_MODIFIER_SERIALIZERS, MOD_ID);

    public static final Supplier<HexCaveFeature> HEX_CAVE_FEATURE =
            FEATURES.register("hex_caves", HexCaveFeature::new);

    public static final Supplier<MapCodec<WastelandNamespaceBiomeModifier>> WASTELAND_NAMESPACE_MODIFIER =
            BIOME_MODIFIER_SERIALIZERS.register(
                    "wasteland_namespace",
                    () -> WastelandNamespaceBiomeModifier.CODEC
            );

    public WastelandHexCaves(IEventBus modBus) {
        FEATURES.register(modBus);
        BIOME_MODIFIER_SERIALIZERS.register(modBus);
    }
}

package infinitedomain.darknet.mixin;

import net.minecraft.core.Holder;
import net.minecraft.core.QuartPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.LevelHeightAccessor;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.RandomState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/**
 * Lets Ice and Fire's native cave generator retain its own burial calculation
 * in the two-block-deep Darknet without changing the dimension's actual floor.
 */
@Mixin(targets = "com.github.alexthe666.iceandfire.neoforge.LegacyNeoForgeContentBootstrap$LegacyGeneratedStructure", remap = false)
abstract class LegacyGeneratedStructureMixin {
    private static final ResourceKey<Biome> DARKNET_BIOME = ResourceKey.create(
        Registries.BIOME,
        ResourceLocation.fromNamespaceAndPath("cyberspace", "darknet_biome")
    );

    private static final int DARKNET_CAVE_VIRTUAL_SURFACE_Y = 80;
    private static final int DARKNET_SAMPLE_Y = 2;

    @Redirect(
        method = "findGenerationPoint",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/world/level/chunk/ChunkGenerator;getBaseHeight(IILnet/minecraft/world/level/levelgen/Heightmap$Types;Lnet/minecraft/world/level/LevelHeightAccessor;Lnet/minecraft/world/level/levelgen/RandomState;)I"
        )
    )
    private int infiniteDomain$darknetCaveDatum(
        ChunkGenerator generator,
        int x,
        int z,
        Heightmap.Types heightmap,
        LevelHeightAccessor heightAccessor,
        RandomState randomState
    ) {
        if (heightmap == Heightmap.Types.OCEAN_FLOOR_WG && infiniteDomain$isDarknet(generator, randomState, x, z)) {
            return DARKNET_CAVE_VIRTUAL_SURFACE_Y;
        }
        return generator.getBaseHeight(x, z, heightmap, heightAccessor, randomState);
    }

    private static boolean infiniteDomain$isDarknet(ChunkGenerator generator, RandomState randomState, int x, int z) {
        Holder<Biome> biome = generator.getBiomeSource().getNoiseBiome(
            QuartPos.fromBlock(x),
            QuartPos.fromBlock(DARKNET_SAMPLE_Y),
            QuartPos.fromBlock(z),
            randomState.sampler()
        );
        return biome.is(DARKNET_BIOME);
    }
}

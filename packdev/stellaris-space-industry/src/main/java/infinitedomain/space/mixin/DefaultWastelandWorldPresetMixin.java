package infinitedomain.space.mixin;

import net.minecraft.client.gui.screens.worldselection.CreateWorldScreen;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.presets.WorldPreset;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

import java.util.Optional;

/** Selects the pack's Wasteland preset only when opening a fresh-world screen. */
@Mixin(CreateWorldScreen.class)
public abstract class DefaultWastelandWorldPresetMixin {
    private static final ResourceKey<WorldPreset> INFINITE_DOMAIN_WASTELAND = ResourceKey.create(
        Registries.WORLD_PRESET,
        ResourceLocation.fromNamespaceAndPath("wastelands", "wasteland")
    );

    @ModifyArg(
        method = "openFresh",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/client/gui/screens/worldselection/CreateWorldScreen;<init>(Lnet/minecraft/client/Minecraft;Lnet/minecraft/client/gui/screens/Screen;Lnet/minecraft/client/gui/screens/worldselection/WorldCreationContext;Ljava/util/Optional;Ljava/util/OptionalLong;)V"
        ),
        index = 3
    )
    private static Optional<ResourceKey<WorldPreset>> infiniteDomain$defaultWasteland(
        Optional<ResourceKey<WorldPreset>> original
    ) {
        return Optional.of(INFINITE_DOMAIN_WASTELAND);
    }
}

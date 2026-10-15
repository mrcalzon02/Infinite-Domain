package infinitedomain.bootcompat.mixin;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import infinitedomain.bootcompat.MisfiledPhysicsRepairs;
import java.io.IOException;
import java.io.Reader;
import java.util.Map;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.util.profiling.ProfilerFiller;
import org.slf4j.LoggerFactory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Pseudo
@Mixin(targets = "dev.ryanhcode.sable.physics.config.dimension_physics.DimensionPhysicsData$ReloadListener", remap = false)
public abstract class DimensionPhysicsLoaderMixin {
    @Inject(method = "apply(Ljava/util/Map;Lnet/minecraft/server/packs/resources/ResourceManager;Lnet/minecraft/util/profiling/ProfilerFiller;)V",
        at = @At("HEAD"), require = 1)
    private void infiniteDomain$quarantineMisfiledDuplicate(Map<ResourceLocation, JsonElement> entries,
            ResourceManager resources, ProfilerFiller profiler, CallbackInfo ci) {
        ResourceLocation key = ResourceLocation.parse("linearbearing:mechanical_linear_moving");
        if (!entries.containsKey(key)) return;
        Resource dimension = resources.getResource(ResourceLocation.parse(
            "linearbearing:dimension_physics/mechanical_linear_moving.json")).orElse(null);
        Resource block = resources.getResource(ResourceLocation.parse(
            "linearbearing:block_physics/mechanical_linear_moving.json")).orElse(null);
        if (dimension == null || block == null) return;
        try (Reader reader = block.openAsReader()) {
            if (!MisfiledPhysicsRepairs.shouldQuarantine(dimension.sourcePackId(), entries.get(key),
                    block.sourcePackId(), JsonParser.parseReader(reader))) return;
            entries.remove(key);
            LoggerFactory.getLogger("Infinite Domain Boot Compatibility").info(
                "[ID-PHYSICS-COMPAT] Quarantined Linear Bearing's exact duplicate block payload from the dimension loader; no dimension binding assigned. Legacy block physics still requires migration.");
        } catch (IOException exception) {
            // Leave the entry untouched so Sable reports its actual codec error.
            LoggerFactory.getLogger("Infinite Domain Boot Compatibility").warn(
                "Could not inspect the Linear Bearing duplicate; leaving it for the normal loader", exception);
        }
    }
}

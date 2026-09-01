package infinitedomain.hiveworld.client;

import com.mojang.blaze3d.shaders.FogShape;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Camera;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.DimensionSpecialEffects;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.material.FogType;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.RegisterDimensionSpecialEffectsEvent;
import net.neoforged.neoforge.client.event.ViewportEvent;
import net.neoforged.neoforge.client.extensions.IDimensionSpecialEffectsExtension;
import net.neoforged.neoforge.common.NeoForge;
import org.joml.Matrix4f;

public final class HiveAtmosphereClient {
    private static final ResourceLocation HIVE_DIMENSION =
            ResourceLocation.fromNamespaceAndPath("infinite_domain", "hive_world");
    private static final ResourceLocation HIVE_EFFECTS = HIVE_DIMENSION;

    private HiveAtmosphereClient() {}

    public static void register(IEventBus modBus) {
        modBus.addListener(HiveAtmosphereClient::registerDimensionEffects);
        NeoForge.EVENT_BUS.addListener(HiveAtmosphereClient::onRenderFog);
        NeoForge.EVENT_BUS.addListener(HiveAtmosphereClient::onFogColour);
    }

    private static void registerDimensionEffects(RegisterDimensionSpecialEffectsEvent event) {
        event.register(HIVE_EFFECTS, new HiveDimensionEffects());
    }

    private static void onRenderFog(ViewportEvent.RenderFog event) {
        if (!isHiveCamera(event.getCamera()) || event.getType() != FogType.NONE) return;
        LayeredFogProfile.Sample sample = LayeredFogProfile.sample(event.getCamera().getPosition().y());
        event.setNearPlaneDistance(sample.nearDistance());
        event.setFarPlaneDistance(sample.farDistance());
        event.setFogShape(FogShape.CYLINDER);
        event.setCanceled(true);
    }

    private static void onFogColour(ViewportEvent.ComputeFogColor event) {
        if (!isHiveCamera(event.getCamera()) || event.getCamera().getFluidInCamera() != FogType.NONE) return;
        LayeredFogProfile.Sample sample = LayeredFogProfile.sample(event.getCamera().getPosition().y());
        event.setRed(sample.red());
        event.setGreen(sample.green());
        event.setBlue(sample.blue());
    }

    private static boolean isHiveCamera(Camera camera) {
        return camera.getEntity() != null
                && HIVE_DIMENSION.equals(camera.getEntity().level().dimension().location());
    }

    private static final class HiveDimensionEffects extends DimensionSpecialEffects
            implements IDimensionSpecialEffectsExtension {
        private HiveDimensionEffects() {
            // This height is retained only as a compatibility fallback. The extension
            // renders the twelve accepted local decks itself.
            super(352.0F, true, SkyType.NORMAL, false, false);
        }

        @Override
        public boolean renderClouds(ClientLevel level, int ticks, float partialTick,
                                    PoseStack poseStack, double cameraX, double cameraY,
                                    double cameraZ, Matrix4f modelViewMatrix,
                                    Matrix4f projectionMatrix) {
            HiveCloudRenderer.render(ticks, partialTick, poseStack,
                    cameraX, cameraY, cameraZ);
            return true;
        }

        @Override
        public boolean tickRain(ClientLevel level, int ticks, Camera camera) {
            HiveSulfurRain.tick(level, ticks, camera);
            return true;
        }

        @Override
        public Vec3 getBrightnessDependentFogColor(Vec3 colour, float brightness) {
            double factor = 0.48D + 0.38D * brightness;
            return colour.multiply(factor, factor * 0.96D, factor * 0.82D);
        }

        @Override
        public boolean isFoggyAt(int x, int z) {
            return true;
        }
    }
}

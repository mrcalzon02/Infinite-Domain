package infinitedomain.hiveworld.client;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.BufferUploader;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexFormat;
import net.minecraft.client.renderer.GameRenderer;
import org.joml.Matrix4f;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Procedural multi-deck cloud renderer for the Hive dimension.
 *
 * The renderer intentionally uses broad, broken translucent cells rather than the
 * vanilla texture sheet. Depth testing lets Stack silhouettes occlude the clouds.
 * Surface alpha collapses before the camera reaches a deck, handing the view to the
 * matching LayeredFogProfile volume instead of drawing a plane at the player's feet.
 */
final class HiveCloudRenderer {
    private static final int TILE_SIZE = 28;
    private static final int TILE_RADIUS = 9;
    private static final double MAX_VERTICAL_DISTANCE = 300.0;

    private HiveCloudRenderer() {}

    static void render(int ticks, float partialTick, PoseStack poseStack,
                       double cameraX, double cameraY, double cameraZ) {
        double time = ticks + partialTick;
        List<LayeredFogProfile.CloudDeck> visible = new ArrayList<>();
        for (LayeredFogProfile.CloudDeck deck : LayeredFogProfile.cloudDecks()) {
            if (Math.abs(cameraY - deck.y()) <= MAX_VERTICAL_DISTANCE) visible.add(deck);
        }
        // Translucent surfaces render furthest first. This also keeps the nearer deck
        // visually dominant when two band layers overlap through a tall void.
        visible.sort(Comparator.comparingDouble(
                (LayeredFogProfile.CloudDeck d) -> Math.abs(cameraY - d.y())).reversed());

        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.enableDepthTest();
        RenderSystem.depthMask(false);
        RenderSystem.disableCull();
        RenderSystem.setShader(GameRenderer::getPositionColorShader);

        poseStack.pushPose();
        poseStack.translate(-cameraX, -cameraY, -cameraZ);
        Matrix4f pose = poseStack.last().pose();
        try {
            for (LayeredFogProfile.CloudDeck deck : visible) {
                renderDeck(deck, time,
                        cameraX, cameraY, cameraZ, pose);
            }
        } finally {
            poseStack.popPose();
            RenderSystem.depthMask(true);
            RenderSystem.enableCull();
            RenderSystem.disableBlend();
        }
    }

    private static void renderDeck(LayeredFogProfile.CloudDeck deck,
                                   double time, double cameraX, double cameraY,
                                   double cameraZ, Matrix4f pose) {
        float proximity = LayeredFogProfile.cloudSurfaceOpacity(
                cameraY, deck.y(), deck.innerFadeDistance(), deck.outerFadeDistance());
        float distanceFade = 1.0F - smoothstep((float) (
                Math.abs(cameraY - deck.y()) / MAX_VERTICAL_DISTANCE));
        float deckAlpha = deck.opacity() * proximity * distanceFade;
        if (deckAlpha < 0.008F) return;

        double driftedX = cameraX + time * deck.driftX();
        double driftedZ = cameraZ + time * deck.driftZ();
        int centerX = floorDiv(driftedX, TILE_SIZE);
        int centerZ = floorDiv(driftedZ, TILE_SIZE);
        double offsetX = time * deck.driftX();
        double offsetZ = time * deck.driftZ();

        BufferBuilder buffer = Tesselator.getInstance().begin(
                VertexFormat.Mode.QUADS, DefaultVertexFormat.POSITION_COLOR);
        int quads = 0;
        for (int dz = -TILE_RADIUS; dz <= TILE_RADIUS; dz++) {
            for (int dx = -TILE_RADIUS; dx <= TILE_RADIUS; dx++) {
                int cellX = centerX + dx;
                int cellZ = centerZ + dz;
                int hash = hash(cellX, cellZ, (int) Math.round(deck.y()), 0x51f15e);
                float coverage = ((hash >>> 8) & 0xFFFF) / 65535.0F;
                if (coverage < 0.20F) continue;

                float cellAlpha = deckAlpha * (0.56F + 0.44F * coverage);
                int alpha = clampByte(Math.round(cellAlpha * 255.0F));
                int red = clampByte(Math.round(deck.red() * 255.0F));
                int green = clampByte(Math.round(deck.green() * 255.0F));
                int blue = clampByte(Math.round(deck.blue() * 255.0F));

                double x0 = cellX * TILE_SIZE - offsetX - 2.0;
                double z0 = cellZ * TILE_SIZE - offsetZ - 2.0;
                double x1 = x0 + TILE_SIZE + 4.0;
                double z1 = z0 + TILE_SIZE + 4.0;
                double ripple = (((hash >>> 24) & 0x7F) / 127.0 - 0.5) * 3.0;
                float y = (float) (deck.y() + ripple);

                buffer.addVertex(pose, (float) x0, y, (float) z0).setColor(red, green, blue, alpha);
                buffer.addVertex(pose, (float) x0, y, (float) z1).setColor(red, green, blue, alpha);
                buffer.addVertex(pose, (float) x1, y, (float) z1).setColor(red, green, blue, alpha);
                buffer.addVertex(pose, (float) x1, y, (float) z0).setColor(red, green, blue, alpha);
                quads++;
            }
        }
        if (quads > 0) BufferUploader.drawWithShader(buffer.buildOrThrow());
    }

    private static int floorDiv(double value, int divisor) {
        return (int) Math.floor(value / divisor);
    }

    private static int hash(int x, int z, int deck, int y) {
        int h = x * 0x1f1f1f1f ^ z * 0x6d2b79f5 ^ deck * 0x45d9f3b ^ y * 0x119de1f3;
        h ^= h >>> 16;
        h *= 0x7feb352d;
        h ^= h >>> 15;
        h *= 0x846ca68b;
        return h ^ (h >>> 16);
    }

    private static float smoothstep(float value) {
        float t = Math.max(0.0F, Math.min(1.0F, value));
        return t * t * (3.0F - 2.0F * t);
    }

    private static int clampByte(int value) {
        return Math.max(0, Math.min(255, value));
    }
}

package infinitedomain.hiveworld.client;

import java.util.List;

/**
 * Height-aware Phase 5 fog model. Band visibility anchors implement Endgame.md
 * section 3.1; paired local layers keep the atmosphere from reading as one flat
 * biome fog value. Values remain tuning targets until EG-P05-S04-C0076.
 */
final class LayeredFogProfile {
    private static final List<BandAnchor> BAND_ANCHORS = List.of(
            new BandAnchor(-32.0, 34.0F, 0.090F, 0.105F, 0.075F),
            new BandAnchor(48.0, 56.0F, 0.115F, 0.125F, 0.090F),
            new BandAnchor(152.0, 88.0F, 0.155F, 0.135F, 0.090F),
            new BandAnchor(280.0, 116.0F, 0.150F, 0.155F, 0.135F),
            new BandAnchor(416.0, 156.0F, 0.105F, 0.125F, 0.150F),
            new BandAnchor(544.0, 208.0F, 0.120F, 0.145F, 0.175F)
    );

    // At least two independently tunable layers per accepted vertical band.
    private static final List<FogLayer> LOCAL_LAYERS = List.of(
            new FogLayer(-52.0, 10.0, 0.52F, 0.16F, 0.18F, 0.08F),
            new FogLayer(-16.0, 12.0, 0.44F, 0.18F, 0.20F, 0.09F),
            new FogLayer(24.0, 14.0, 0.36F, 0.20F, 0.19F, 0.10F),
            new FogLayer(72.0, 14.0, 0.31F, 0.22F, 0.20F, 0.11F),
            new FogLayer(124.0, 15.0, 0.29F, 0.25F, 0.19F, 0.09F),
            new FogLayer(180.0, 16.0, 0.26F, 0.24F, 0.17F, 0.09F),
            new FogLayer(240.0, 18.0, 0.22F, 0.20F, 0.18F, 0.14F),
            new FogLayer(320.0, 18.0, 0.19F, 0.18F, 0.18F, 0.16F),
            new FogLayer(384.0, 16.0, 0.17F, 0.13F, 0.16F, 0.20F),
            new FogLayer(448.0, 16.0, 0.14F, 0.14F, 0.17F, 0.22F),
            new FogLayer(512.0, 14.0, 0.11F, 0.16F, 0.19F, 0.23F),
            new FogLayer(576.0, 12.0, 0.09F, 0.17F, 0.20F, 0.24F)
    );

    private LayeredFogProfile() {}

    static Sample sample(double y) {
        BandAnchor lower = BAND_ANCHORS.get(0);
        BandAnchor upper = lower;
        for (BandAnchor candidate : BAND_ANCHORS) {
            if (candidate.y() <= y) {
                lower = candidate;
            }
            if (candidate.y() >= y) {
                upper = candidate;
                break;
            }
            upper = candidate;
        }

        double span = upper.y() - lower.y();
        float transition = span <= 0.0 ? 0.0F : smoothstep((float) ((y - lower.y()) / span));
        float visibility = lerp(lower.visibility(), upper.visibility(), transition);
        float red = lerp(lower.red(), upper.red(), transition);
        float green = lerp(lower.green(), upper.green(), transition);
        float blue = lerp(lower.blue(), upper.blue(), transition);

        for (FogLayer layer : LOCAL_LAYERS) {
            float influence = layer.influence(y);
            if (influence <= 0.0F) continue;
            visibility *= 1.0F - influence * layer.density() * 0.58F;
            float colourBlend = influence * layer.density() * 0.42F;
            red = lerp(red, layer.red(), colourBlend);
            green = lerp(green, layer.green(), colourBlend);
            blue = lerp(blue, layer.blue(), colourBlend);
        }

        // The lowest tiers never clear between local decks. This baseline becomes
        // progressively more oppressive near the bedrock floor, while the paired
        // FogLayer peaks provide the individually readable local volumes.
        if (y < 96.0) {
            float lowerPressure = smoothstep((float) ((96.0 - y) / 160.0));
            visibility *= 1.0F - 0.24F * lowerPressure;
            red = lerp(red, 0.105F, 0.16F * lowerPressure);
            green = lerp(green, 0.120F, 0.16F * lowerPressure);
            blue = lerp(blue, 0.075F, 0.16F * lowerPressure);
        }

        visibility = clamp(visibility, 20.0F, 256.0F);
        float near = clamp(visibility * 0.08F, 1.5F, 12.0F);
        return new Sample(near, visibility, red, green, blue);
    }

    private static float smoothstep(float value) {
        float t = clamp(value, 0.0F, 1.0F);
        return t * t * (3.0F - 2.0F * t);
    }

    private static float lerp(float from, float to, float amount) {
        return from + (to - from) * amount;
    }

    private static float clamp(float value, float min, float max) {
        return Math.max(min, Math.min(max, value));
    }

    /**
     * Shared rule for the later cloud-deck renderer. A distant deck is opaque
     * enough to read as a ceiling or poison sea; its surface disappears before
     * the camera reaches it, leaving the FogLayer influence to engulf the view.
     */
    static float cloudSurfaceOpacity(double cameraY, double layerY,
                                     double innerFadeDistance, double outerFadeDistance) {
        double distance = Math.abs(cameraY - layerY);
        if (distance <= innerFadeDistance) return 0.0F;
        if (distance >= outerFadeDistance) return 1.0F;
        return smoothstep((float) ((distance - innerFadeDistance)
                / (outerFadeDistance - innerFadeDistance)));
    }

    record Sample(float nearDistance, float farDistance, float red, float green, float blue) {}

    private record BandAnchor(double y, float visibility, float red, float green, float blue) {}

    private record FogLayer(double centerY, double halfThickness, float density,
                            float red, float green, float blue) {
        float influence(double y) {
            double distance = Math.abs(y - centerY);
            if (distance >= halfThickness) return 0.0F;
            return smoothstep(1.0F - (float) (distance / halfThickness));
        }
    }
}

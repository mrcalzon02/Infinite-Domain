package infinitedomain.biomepreview;

import infinitedomain.biomepreview.client.BiomePreviewClient;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/** The compact, server-authored painting image sent after the player joins. */
public record PreviewPayload(
        int width,
        int height,
        int radius,
        int spawnX,
        int spawnZ,
        int sampleY,
        long worldFingerprint,
        int[] pixels
) implements CustomPacketPayload {
    public static final Type<PreviewPayload> TYPE =
            new Type<>(SpawnBiomePreview.id("world_biome_preview"));
    public static final StreamCodec<RegistryFriendlyByteBuf, PreviewPayload> STREAM_CODEC =
            StreamCodec.ofMember(PreviewPayload::encode, PreviewPayload::decode);

    public PreviewPayload {
        if (width < 1 || height < 1 || width > 512 || height > 512) {
            throw new IllegalArgumentException("Invalid biome preview dimensions");
        }
        if (pixels.length != width * height) {
            throw new IllegalArgumentException("Biome preview pixel count does not match dimensions");
        }
    }

    private void encode(RegistryFriendlyByteBuf buffer) {
        buffer.writeVarInt(width);
        buffer.writeVarInt(height);
        buffer.writeVarInt(radius);
        buffer.writeInt(spawnX);
        buffer.writeInt(spawnZ);
        buffer.writeVarInt(sampleY);
        buffer.writeLong(worldFingerprint);
        buffer.writeVarInt(pixels.length);
        for (int pixel : pixels) {
            buffer.writeInt(pixel);
        }
    }

    private static PreviewPayload decode(RegistryFriendlyByteBuf buffer) {
        int width = buffer.readVarInt();
        int height = buffer.readVarInt();
        int radius = buffer.readVarInt();
        int spawnX = buffer.readInt();
        int spawnZ = buffer.readInt();
        int sampleY = buffer.readVarInt();
        long fingerprint = buffer.readLong();
        int length = buffer.readVarInt();
        if (width < 1 || height < 1 || width > 512 || height > 512 || length != width * height) {
            throw new IllegalArgumentException("Malformed biome preview payload");
        }
        int[] pixels = new int[length];
        for (int i = 0; i < length; i++) {
            pixels[i] = buffer.readInt();
        }
        return new PreviewPayload(width, height, radius, spawnX, spawnZ, sampleY, fingerprint, pixels);
    }

    public static void register(RegisterPayloadHandlersEvent event) {
        event.registrar("1").playToClient(TYPE, STREAM_CODEC, PreviewPayload::handle);
    }

    private static void handle(PreviewPayload payload, IPayloadContext context) {
        if (FMLEnvironment.dist == Dist.CLIENT) {
            context.enqueueWork(() -> BiomePreviewClient.accept(payload));
        }
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}

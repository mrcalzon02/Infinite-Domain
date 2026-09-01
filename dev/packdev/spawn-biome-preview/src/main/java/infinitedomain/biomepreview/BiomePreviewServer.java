package infinitedomain.biomepreview;

import com.mojang.brigadier.CommandDispatcher;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.CustomData;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/** Server-side lifecycle, cache, command, and dedicated painting-item creation. */
final class BiomePreviewServer {
    private static final String RECEIVED_KEY = SpawnBiomePreview.MOD_ID + ".painting_fingerprint";
    private static final Map<UUID, Integer> PENDING_PLAYERS = new HashMap<>();
    private static PreviewPayload cached;

    private BiomePreviewServer() {}

    static void onPlayerLogin(PlayerEvent.PlayerLoggedInEvent event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            // Let the level and client finish settling before generating/sending the image.
            PENDING_PLAYERS.put(player.getUUID(), 40);
        }
    }

    static void onServerTick(ServerTickEvent.Post event) {
        if (PENDING_PLAYERS.isEmpty()) return;
        MinecraftServer server = event.getServer();
        Iterator<Map.Entry<UUID, Integer>> iterator = PENDING_PLAYERS.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<UUID, Integer> pending = iterator.next();
            int ticks = pending.getValue() - 1;
            if (ticks > 0) {
                pending.setValue(ticks);
                continue;
            }
            iterator.remove();
            ServerPlayer player = server.getPlayerList().getPlayer(pending.getKey());
            if (player != null) {
                sendPreview(player, true);
            }
        }
    }

    static void onRegisterCommands(RegisterCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
        dispatcher.register(Commands.literal("biomepreview")
                .executes(context -> {
                    ServerPlayer player = context.getSource().getPlayerOrException();
                    sendPreview(player, false);
                    context.getSource().sendSuccess(
                            () -> Component.literal("Spawn biome preview synchronized."), false);
                    return 1;
                })
                .then(Commands.literal("painting")
                        .executes(context -> {
                            ServerPlayer player = context.getSource().getPlayerOrException();
                            givePainting(player);
                            context.getSource().sendSuccess(
                                    () -> Component.literal("Gave dedicated spawn biome survey painting."), false);
                            return 1;
                        })));
    }

    private static void sendPreview(ServerPlayer player, boolean automatic) {
        ServerLevel overworld = player.server.overworld();
        long fingerprint = BiomePreviewGenerator.fingerprint(overworld.getSeed(), overworld.getSharedSpawnPos());
        if (cached == null || cached.worldFingerprint() != fingerprint) {
            cached = BiomePreviewGenerator.generate(overworld);
        }
        PacketDistributor.sendToPlayer(player, cached);

        if (automatic) {
            CompoundTag persistent = player.getPersistentData();
            if (!persistent.contains(RECEIVED_KEY) || persistent.getLong(RECEIVED_KEY) != fingerprint) {
                givePainting(player);
                persistent.putLong(RECEIVED_KEY, fingerprint);
                player.sendSystemMessage(Component.literal("World survey complete: a spawn biome preview painting was issued. ")
                        .withStyle(ChatFormatting.AQUA)
                        .append(Component.literal("Use /biomepreview painting for another copy.")
                                .withStyle(ChatFormatting.GRAY)));
            }
        }
    }

    private static void givePainting(ServerPlayer player) {
        ItemStack stack = new ItemStack(Items.PAINTING);
        CompoundTag entityData = new CompoundTag();
        entityData.putString("id", "minecraft:painting");
        entityData.putString("variant", SpawnBiomePreview.PAINTING_ID.toString());
        stack.set(DataComponents.ENTITY_DATA, CustomData.of(entityData));
        stack.set(DataComponents.CUSTOM_NAME,
                Component.literal("Spawn Biome Survey").withStyle(ChatFormatting.AQUA));
        if (!player.getInventory().add(stack)) {
            player.drop(stack, false);
        }
    }
}

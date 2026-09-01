package infinitedomain.radiation;

import net.mcreator.thewastelandreworked.init.TheWastelandReworkedModGameRules;
import net.mcreator.thewastelandreworked.network.TheWastelandReworkedModVariables;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.attachment.IAttachmentHolder;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.fml.common.Mod;
import org.takesome.necrosteam.radiation.RadiationManager;
import org.takesome.necrosteam.config.WastelandConfig;
import org.takesome.necrosteam.world.WastelandWorlds;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

/**
 * Pack-level radiation adapter. Wastelands owns the persistent dose; all other
 * radiation implementations are translated into that dose and then suppressed.
 */
@Mod(InfiniteDomainRadiation.MOD_ID)
public final class InfiniteDomainRadiation {
    public static final String MOD_ID = "infinite_domain_radiation";

    private static final int DETECTOR_INTERVAL = 20;

    private static final ResourceLocation CNA_RADIATION = id("create_new_age", "radiation_poisoning");
    private static final ResourceLocation CN_RADIATION = id("createnuclear", "radiation");
    private static final ResourceLocation TWR_RADIATION = id("the_wasteland_reworked", "radiation_poisoning");

    private static final TagKey<net.minecraft.world.level.block.Block> SOURCE_LOW = blockTag("radiation_source_low");
    private static final TagKey<net.minecraft.world.level.block.Block> SOURCE_MEDIUM = blockTag("radiation_source_medium");
    private static final TagKey<net.minecraft.world.level.block.Block> SOURCE_HIGH = blockTag("radiation_source_high");
    private static final TagKey<net.minecraft.world.level.block.Block> SOURCE_EXTREME = blockTag("radiation_source_extreme");
    private static final TagKey<net.minecraft.world.level.block.Block> SHIELD_LIGHT = blockTag("radiation_shield_light");
    private static final TagKey<net.minecraft.world.level.block.Block> SHIELD_MEDIUM = blockTag("radiation_shield_medium");
    private static final TagKey<net.minecraft.world.level.block.Block> SHIELD_HEAVY = blockTag("radiation_shield_heavy");

    private static final TagKey<Item> CONTAMINATION_LOW = itemTag("contamination_low");
    private static final TagKey<Item> CONTAMINATION_MEDIUM = itemTag("contamination_medium");
    private static final TagKey<Item> CONTAMINATION_HIGH = itemTag("contamination_high");
    private static final TagKey<Item> CONTAMINATION_EXTREME = itemTag("contamination_extreme");
    private static final TagKey<Item> PPE_BASIC = itemTag("ppe_basic");
    private static final TagKey<Item> PPE_INDUSTRIAL = itemTag("ppe_industrial");
    private static final TagKey<Item> PPE_ADVANCED = itemTag("ppe_advanced");
    private static final TagKey<Item> PPE_LATE = itemTag("ppe_late");
    private static final TagKey<Item> DETECTORS = itemTag("radiation_detectors");
    private static final TagKey<Biome> RADIOACTIVE_AMBIENT = TagKey.create(
            Registries.BIOME, id(MOD_ID, "radioactive_ambient"));

    private static final Map<UUID, Reading> READINGS = new HashMap<>();
    private static final Map<UUID, Long> LAST_EFFECT_DOSE = new HashMap<>();

    public InfiniteDomainRadiation() {
        NeoForge.EVENT_BUS.addListener(InfiniteDomainRadiation::onPlayerTick);
        NeoForge.EVENT_BUS.addListener(InfiniteDomainRadiation::onUseDetector);
    }

    private static void onPlayerTick(PlayerTickEvent.Pre event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }

        migrateAndSuppressReworkedMeter(player);
        suppressForeignEffects(player);
        long time = player.level().getGameTime();
        int exposureInterval = WastelandConfig.RADIATION_EXPOSURE_INTERVAL.get();
        int decayInterval = WastelandConfig.RADIATION_DECAY_INTERVAL.get();

        if (time % exposureInterval == Math.floorMod(player.getId(), exposureInterval)) {
            disableReworkedRadiationRules(player);
            Reading reading = calculateReading(player);
            READINGS.put(player.getUUID(), reading);
            int raw = Math.min(12, reading.ambient() + reading.contamination());
            int exposure = (int) Math.ceil(raw * (1.0 - reading.protection()));
            if (raw > 0 && exposure > 0) {
                RadiationManager.add(player, exposure);
            }
        }

        if (time % decayInterval == Math.floorMod(player.getId(), decayInterval)) {
            Reading reading = READINGS.getOrDefault(player.getUUID(), Reading.CLEAR);
            if (reading.ambient() == 0 && reading.contamination() == 0) {
                RadiationManager.remove(player, 1);
            }
        }

        if (time % DETECTOR_INTERVAL == Math.floorMod(player.getId(), DETECTOR_INTERVAL)) {
            applyConsequences(player);
            if (hasDetectorEquipped(player)) {
                showReading(player);
            }
        }
    }

    private static void onUseDetector(PlayerInteractEvent.RightClickItem event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || !event.getItemStack().is(DETECTORS)) {
            return;
        }
        READINGS.put(player.getUUID(), calculateReading(player));
        showReading(player);
        event.setCanceled(true);
        event.setCancellationResult(InteractionResult.SUCCESS);
    }

    private static void migrateAndSuppressReworkedMeter(ServerPlayer player) {
        TheWastelandReworkedModVariables.PlayerVariables legacy =
                ((IAttachmentHolder) player).getData(TheWastelandReworkedModVariables.PLAYER_VARIABLES.get());
        if (legacy.playerRadiationAmount > 0.0) {
            RadiationManager.set(player, Math.max(RadiationManager.get(player), (int) Math.round(legacy.playerRadiationAmount)));
        }
        if (legacy.playerRadiationAmount != 0.0 || legacy.isPlayerExposedToRadiation) {
            legacy.playerRadiationAmount = 0.0;
            legacy.playerRadiationAmountDisplay = "0";
            legacy.playerRadiationTimer = 0.0;
            legacy.isPlayerExposedToRadiation = false;
            legacy.markSyncDirty();
        }
    }

    private static void disableReworkedRadiationRules(ServerPlayer player) {
        GameRules rules = player.serverLevel().getGameRules();
        rules.getRule(TheWastelandReworkedModGameRules.DO_PLAYER_PROXIMITY_RADIATION).set(false, player.getServer());
        rules.getRule(TheWastelandReworkedModGameRules.DO_BLOCK_RADIATION).set(false, player.getServer());
        rules.getRule(TheWastelandReworkedModGameRules.DO_INVENTORY_RADIATION).set(false, player.getServer());
        rules.getRule(TheWastelandReworkedModGameRules.DO_AMBIENT_RADIATION).set(false, player.getServer());
    }

    private static boolean suppressForeignEffects(ServerPlayer player) {
        boolean found = false;
        for (MobEffectInstance instance : player.getActiveEffects().toArray(MobEffectInstance[]::new)) {
            ResourceLocation effectId = net.minecraft.core.registries.BuiltInRegistries.MOB_EFFECT
                    .getKey(instance.getEffect().value());
            if (CNA_RADIATION.equals(effectId) || CN_RADIATION.equals(effectId) || TWR_RADIATION.equals(effectId)) {
                Holder<MobEffect> effect = instance.getEffect();
                player.removeEffect(effect);
                found = true;
            }
        }
        if (!found) {
            return false;
        }

        long now = player.level().getGameTime();
        long last = LAST_EFFECT_DOSE.getOrDefault(player.getUUID(), Long.MIN_VALUE / 2);
        if (now - last >= DETECTOR_INTERVAL) {
            Reading reading = READINGS.getOrDefault(player.getUUID(), Reading.CLEAR);
            if (reading.ambient() == 0) {
                int dose = Math.max(1, (int) Math.ceil(2.0 * (1.0 - protection(player))));
                RadiationManager.add(player, dose);
                READINGS.put(player.getUUID(), new Reading(2, reading.contamination(), reading.protection()));
            }
            LAST_EFFECT_DOSE.put(player.getUUID(), now);
        }
        return true;
    }

    private static Reading calculateReading(ServerPlayer player) {
        int ambient = wastelandAmbient(player) + nearbyBlockRadiation(player);
        int contamination = inventoryContamination(player);
        return new Reading(Math.min(12, ambient), Math.min(8, contamination), protection(player));
    }

    private static int wastelandAmbient(ServerPlayer player) {
        ServerLevel level = player.serverLevel();
        BlockPos pos = player.blockPosition();
        boolean exposedToSky = level.canSeeSky(pos.above());
        int intensity = exposedToSky && level.getBiome(pos).is(RADIOACTIVE_AMBIENT) ? 2 : 0;
        if (!WastelandWorlds.isWasteland(level, pos)) {
            return intensity;
        }
        intensity += exposedToSky ? 1 : 0;
        Optional<ResourceLocation> biome = level.getBiome(pos).unwrapKey().map(key -> key.location());
        if (exposedToSky && biome.filter(id -> id.getNamespace().equals("wastelands")
                && (id.getPath().equals("city") || id.getPath().equals("apocalypse"))).isPresent()) {
            intensity++;
        }
        return intensity;
    }

    private static int nearbyBlockRadiation(ServerPlayer player) {
        ServerLevel level = player.serverLevel();
        BlockPos origin = player.blockPosition();
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        int total = 0;

        for (int dx = -12; dx <= 12 && total < 12; dx++) {
            for (int dy = -6; dy <= 6 && total < 12; dy++) {
                for (int dz = -12; dz <= 12 && total < 12; dz++) {
                    cursor.set(origin.getX() + dx, origin.getY() + dy, origin.getZ() + dz);
                    BlockState state = level.getBlockState(cursor);
                    int strength = sourceStrength(state);
                    if (strength == 0) {
                        continue;
                    }
                    double distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
                    int range = switch (strength) {
                        case 1 -> 4;
                        case 2 -> 6;
                        case 4 -> 8;
                        default -> 12;
                    };
                    if (distance > range) {
                        continue;
                    }
                    double distanceFactor = Math.max(0.25, 1.0 - (distance / (range + 1.0)) * 0.65);
                    double shielding = shieldingBetween(level, cursor.immutable(), player.getEyePosition());
                    int contribution = (int) Math.ceil(strength * distanceFactor * Math.max(0.0, 1.0 - shielding));
                    total += contribution;
                }
            }
        }
        return Math.min(12, total);
    }

    private static int sourceStrength(BlockState state) {
        if (state.is(SOURCE_EXTREME)) return 8;
        if (state.is(SOURCE_HIGH)) return 4;
        if (state.is(SOURCE_MEDIUM)) return 2;
        if (state.is(SOURCE_LOW)) return 1;
        return 0;
    }

    private static double shieldingBetween(ServerLevel level, BlockPos source, Vec3 target) {
        Vec3 start = Vec3.atCenterOf(source);
        Vec3 delta = target.subtract(start);
        double length = delta.length();
        if (length < 1.0) return 0.0;
        int steps = Math.max(1, (int) Math.ceil(length * 2.0));
        BlockPos last = source;
        double attenuation = 0.0;
        for (int i = 1; i < steps; i++) {
            Vec3 point = start.add(delta.scale(i / (double) steps));
            BlockPos pos = BlockPos.containing(point);
            if (pos.equals(last)) continue;
            last = pos;
            BlockState state = level.getBlockState(pos);
            if (state.is(SHIELD_HEAVY)) attenuation += 0.65;
            else if (state.is(SHIELD_MEDIUM)) attenuation += 0.35;
            else if (state.is(SHIELD_LIGHT) || state.is(BlockTags.WOOL)) attenuation += 0.15;
            else if (state.getFluidState().is(FluidTags.WATER)) attenuation += 0.12;
            if (attenuation >= 1.0) return 1.0;
        }
        return attenuation;
    }

    private static int inventoryContamination(ServerPlayer player) {
        double total = 0.0;
        for (ItemStack stack : player.getInventory().items) {
            int strength = stack.is(CONTAMINATION_EXTREME) ? 8
                    : stack.is(CONTAMINATION_HIGH) ? 4
                    : stack.is(CONTAMINATION_MEDIUM) ? 2
                    : stack.is(CONTAMINATION_LOW) ? 1 : 0;
            if (strength > 0) {
                total += strength * Math.max(1.0, Math.sqrt(stack.getCount()) / 4.0);
            }
        }
        return (int) Math.ceil(Math.min(8.0, total));
    }

    private static double protection(ServerPlayer player) {
        int basic = 0;
        int industrial = 0;
        int advanced = 0;
        int late = 0;
        for (ItemStack armor : player.getArmorSlots()) {
            if (armor.is(PPE_LATE)) late++;
            else if (armor.is(PPE_ADVANCED)) advanced++;
            else if (armor.is(PPE_INDUSTRIAL)) industrial++;
            else if (armor.is(PPE_BASIC)) basic++;
        }
        double protection = basic * 0.0625 + industrial * 0.1875 + advanced * 0.225 + late * 0.2375;
        return Math.min(0.95, protection);
    }

    private static void applyConsequences(ServerPlayer player) {
        int dose = RadiationManager.get(player);
        if (dose >= 25) addEffect(player, MobEffects.WEAKNESS, 60);
        if (dose >= 50) addEffect(player, MobEffects.MOVEMENT_SLOWDOWN, 60);
        if (dose >= 70) addEffect(player, MobEffects.HUNGER, 60);
        if (dose >= 90) addEffect(player, MobEffects.POISON, 40);
    }

    private static void addEffect(ServerPlayer player, Holder<MobEffect> effect, int duration) {
        player.addEffect(new MobEffectInstance(effect, duration, 0, true, false));
    }

    private static boolean hasDetectorEquipped(ServerPlayer player) {
        return player.getMainHandItem().is(DETECTORS) || player.getOffhandItem().is(DETECTORS);
    }

    private static void showReading(ServerPlayer player) {
        Reading reading = READINGS.computeIfAbsent(player.getUUID(), ignored -> calculateReading(player));
        int percent = (int) Math.round(reading.protection() * 100.0);
        player.displayClientMessage(Component.literal("Radiation  Dose " + RadiationManager.get(player)
                + "/100  |  Ambient " + reading.ambient()
                + "  |  Carried " + reading.contamination()
                + "  |  PPE " + percent + "%"), true);
    }

    private static ResourceLocation id(String namespace, String path) {
        return ResourceLocation.fromNamespaceAndPath(namespace, path);
    }

    private static TagKey<net.minecraft.world.level.block.Block> blockTag(String path) {
        return TagKey.create(Registries.BLOCK, id(MOD_ID, path));
    }

    private static TagKey<Item> itemTag(String path) {
        return TagKey.create(Registries.ITEM, id(MOD_ID, path));
    }

    private record Reading(int ambient, int contamination, double protection) {
        private static final Reading CLEAR = new Reading(0, 0, 0.0);
    }
}

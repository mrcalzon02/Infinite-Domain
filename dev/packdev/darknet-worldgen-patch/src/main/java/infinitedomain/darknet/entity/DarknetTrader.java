package infinitedomain.darknet.entity;

import infinitedomain.darknet.DarknetGuard;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.AABB;

/** A Darknet-only wandering merchant with a fixed recovered-data economy. */
public final class DarknetTrader extends WanderingTrader {
    public static final int DESPAWN_TICKS = 72_000;
    public static final double EXCLUSION_RADIUS = 384.0;

    private static final String SCRIP = "kubejs:darknet_scrip";

    public DarknetTrader(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
        setDespawnDelay(DESPAWN_TICKS);
    }

    public static boolean canSpawn(EntityType<DarknetTrader> type, ServerLevelAccessor level, MobSpawnType reason,
                                   BlockPos pos, RandomSource random) {
        if (!DarknetGuard.isDarknet(level.getLevel()) || pos.getY() < 2) return false;
        if (!Mob.checkMobSpawnRules(type, level, reason, pos, random)) return false;
        return level.getLevel().getEntitiesOfClass(DarknetTrader.class,
            new AABB(pos).inflate(EXCLUSION_RADIUS)).isEmpty();
    }

    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType reason,
                                        SpawnGroupData spawnData) {
        SpawnGroupData result = super.finalizeSpawn(level, difficulty, reason, spawnData);
        setDespawnDelay(DESPAWN_TICKS);
        setHealth(getMaxHealth());
        return result;
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();

        // Wholesale acquisition: recovered intelligence is converted into the
        // Broker's anonymous bearer currency. Premium ore recoveries pay best.
        buy(offers, "kubejs:scraped_access_token", 16, 1, 12);
        buy(offers, "kubejs:darknet_data_cache", 8, 2, 12);
        buy(offers, "kubejs:encrypted_credential_bundle", 4, 3, 10);
        buy(offers, "kubejs:black_ice_kernel", 2, 5, 8);
        buy(offers, "kubejs:zero_day_archive", 1, 10, 6);
        buy(offers, "kubejs:root_authority_key", 1, 24, 4);
        buy(offers, "kubejs:ghost_market_cipher", 1, 16, 6);
        buy(offers, "kubejs:black_ledger_writ", 1, 48, 3);

        // Retail data and mineable nodes. Every retail rate exceeds its
        // corresponding wholesale return, preventing a currency loop.
        sell(offers, 1, "kubejs:scraped_access_token", 4, 16);
        sell(offers, 3, "kubejs:darknet_data_cache", 2, 12);
        sell(offers, 5, "kubejs:encrypted_credential_bundle", 1, 8);
        sell(offers, 9, "kubejs:black_ice_kernel", 1, 6);
        sell(offers, 18, "kubejs:zero_day_archive", 1, 4);
        sell(offers, 36, "kubejs:root_authority_key", 1, 2);

        sell(offers, 6, "kubejs:fragmented_data_node", 1, 12);
        sell(offers, 14, "kubejs:corrupted_data_node", 1, 8);
        sell(offers, 32, "kubejs:encrypted_data_node", 1, 4);
        sell(offers, 64, "kubejs:root_access_node", 1, 2);

        // Emergency luxury route: 64 Scrip plus eight Root Authority Keys.
        offers.add(new MerchantOffer(
            new ItemCost(resolve(SCRIP), 64),
            Optional.of(new ItemCost(resolve("kubejs:root_authority_key"), 8)),
            new ItemStack(resolve("ae2:spatial_anchor"), 1),
            1, 0, 0.0F
        ));
    }

    private static void buy(MerchantOffers offers, String payment, int paymentCount, int scripCount, int maxUses) {
        offers.add(new MerchantOffer(
            new ItemCost(resolve(payment), paymentCount),
            new ItemStack(resolve(SCRIP), scripCount),
            maxUses, 0, 0.0F
        ));
    }

    private static void sell(MerchantOffers offers, int scripCount, String result, int resultCount, int maxUses) {
        offers.add(new MerchantOffer(
            new ItemCost(resolve(SCRIP), scripCount),
            new ItemStack(resolve(result), resultCount),
            maxUses, 0, 0.0F
        ));
    }

    private static Item resolve(String id) {
        Item item = BuiltInRegistries.ITEM.get(ResourceLocation.parse(id));
        if (item == Items.AIR && !id.equals("minecraft:air")) {
            throw new IllegalStateException("Missing Darknet Broker trade item: " + id);
        }
        return item;
    }
}

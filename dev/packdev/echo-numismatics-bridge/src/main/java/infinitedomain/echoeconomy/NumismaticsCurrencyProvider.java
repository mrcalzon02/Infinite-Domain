package infinitedomain.echoeconomy;

import dev.ftb.mods.ftblibrary.integration.currency.CurrencyProvider;
import dev.ithundxr.createnumismatics.content.backend.Coin;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.ItemHandlerHelper;

public enum NumismaticsCurrencyProvider implements CurrencyProvider {
    INSTANCE;

    private static final Coin[] DESCENDING = {
        Coin.SUN, Coin.CROWN, Coin.COG, Coin.SPROCKET, Coin.BEVEL, Coin.SPUR
    };

    @Override
    public String getName() {
        return "Create: Numismatics";
    }

    @Override
    public int getTotalCurrency(Player player) {
        long total = 0L;
        Inventory inventory = player.getInventory();
        for (int slot = 0; slot < inventory.getContainerSize(); slot++) {
            ItemStack stack = inventory.getItem(slot);
            Coin coin = coinFor(stack);
            if (coin != null) {
                total += (long) stack.getCount() * coin.value;
            }
        }
        return (int) Math.min(Integer.MAX_VALUE, total);
    }

    @Override
    public boolean takeCurrency(Player player, int amount) {
        if (amount <= 0) {
            return true;
        }

        int total = getTotalCurrency(player);
        if (total < amount) {
            return false;
        }

        Inventory inventory = player.getInventory();
        for (int slot = 0; slot < inventory.getContainerSize(); slot++) {
            ItemStack stack = inventory.getItem(slot);
            if (coinFor(stack) != null) {
                inventory.setItem(slot, ItemStack.EMPTY);
            }
        }
        inventory.setChanged();
        giveCurrency(player, total - amount);
        return true;
    }

    @Override
    public void giveCurrency(Player player, int amount) {
        int remaining = Math.max(0, amount);
        for (Coin coin : DESCENDING) {
            int count = remaining / coin.value;
            remaining %= coin.value;
            while (count > 0) {
                int batch = Math.min(count, coin.asStack().getMaxStackSize());
                ItemHandlerHelper.giveItemToPlayer(player, coin.asStack(batch));
                count -= batch;
            }
        }
    }

    @Override
    public Component coinName(boolean plural) {
        return Component.literal(plural ? "Numismatics coins" : "Numismatics coin");
    }

    public static Component format(int spurValue) {
        if (spurValue <= 0) {
            return Component.literal("0 Spurs");
        }

        int remaining = spurValue;
        var result = Component.empty();
        boolean first = true;
        for (Coin coin : DESCENDING) {
            int count = remaining / coin.value;
            remaining %= coin.value;
            if (count == 0) {
                continue;
            }
            if (!first) {
                result.append(" + ");
            }
            result.append(Component.literal(count + " " + coin.getDisplayName() + (count == 1 ? "" : "s")));
            first = false;
        }
        return result;
    }

    private static Coin coinFor(ItemStack stack) {
        if (stack.isEmpty()) {
            return null;
        }
        for (Coin coin : DESCENDING) {
            if (stack.is(coin.asStack().getItem())) {
                return coin;
            }
        }
        return null;
    }
}

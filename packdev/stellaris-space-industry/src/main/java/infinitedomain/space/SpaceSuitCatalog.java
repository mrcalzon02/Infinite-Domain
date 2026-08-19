package infinitedomain.space;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.LinkedHashMap;
import java.util.Map;

public final class SpaceSuitCatalog {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(InfiniteDomainSpaceIndustry.MOD_ID);
    public static final Map<String, DeferredItem<RoleSpaceSuit>> SUITS = new LinkedHashMap<>();

    private static final SuitDefinition[] DEFINITIONS = {
        new SuitDefinition("emergency", "Emergency EVA", 1000, 240),
        new SuitDefinition("surveyor", "Surveyor EVA", 3500, 520),
        new SuitDefinition("lunar_prospector", "Lunar Prospector", 4000, 620),
        new SuitDefinition("radiation", "Radiation EVA", 4000, 720),
        new SuitDefinition("heavy", "Heavy EVA", 3500, 900),
        new SuitDefinition("mobility", "Mobility EVA", 3000, 560),
        new SuitDefinition("extended", "Extended Life-Support EVA", 8000, 640),
        new SuitDefinition("martian", "Martian Field EVA", 5000, 760),
        new SuitDefinition("venusian", "Venusian Extreme EVA", 6000, 1100)
    };

    static {
        for (SuitDefinition definition : DEFINITIONS) {
            registerPiece(definition, "helmet", ArmorItem.Type.HELMET);
            registerPiece(definition, "chestplate", ArmorItem.Type.CHESTPLATE);
            registerPiece(definition, "leggings", ArmorItem.Type.LEGGINGS);
            registerPiece(definition, "boots", ArmorItem.Type.BOOTS);
        }
    }

    private static void registerPiece(SuitDefinition definition, String suffix, ArmorItem.Type type) {
        String id = definition.id() + "_" + suffix;
        SUITS.put(id, ITEMS.register(id, () -> new RoleSpaceSuit(
                new Item.Properties().durability(definition.durability()),
                type, definition.id(), definition.displayName(), definition.oxygenCapacity())));
    }

    public static boolean isCompleteCustomSuit(net.minecraft.world.entity.LivingEntity entity) {
        String role = role(entity.getItemBySlot(EquipmentSlot.HEAD));
        return role != null
                && role.equals(role(entity.getItemBySlot(EquipmentSlot.CHEST)))
                && role.equals(role(entity.getItemBySlot(EquipmentSlot.LEGS)))
                && role.equals(role(entity.getItemBySlot(EquipmentSlot.FEET)));
    }

    public static String completeRole(net.minecraft.world.entity.LivingEntity entity) {
        return isCompleteCustomSuit(entity) ? role(entity.getItemBySlot(EquipmentSlot.CHEST)) : null;
    }

    private static String role(ItemStack stack) {
        return stack.getItem() instanceof RoleSpaceSuit suit ? suit.role() : null;
    }

    public static void register(IEventBus modBus) {
        ITEMS.register(modBus);
    }

    private record SuitDefinition(String id, String displayName, int oxygenCapacity, int durability) {}

    private SpaceSuitCatalog() {}
}

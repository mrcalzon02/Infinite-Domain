package infinitedomain.space;

import net.minecraft.core.Holder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.neoforged.neoforge.event.entity.living.LivingEquipmentChangeEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;

import java.util.List;

public final class SuitSpecializations {
    private static final List<Holder<Attribute>> MANAGED = List.of(
            Attributes.MOVEMENT_SPEED, Attributes.BLOCK_INTERACTION_RANGE, Attributes.MINING_EFFICIENCY,
            Attributes.ARMOR_TOUGHNESS, Attributes.KNOCKBACK_RESISTANCE, Attributes.SAFE_FALL_DISTANCE,
            Attributes.STEP_HEIGHT, Attributes.MAX_HEALTH, Attributes.MOVEMENT_EFFICIENCY,
            Attributes.BURNING_TIME, Attributes.EXPLOSION_KNOCKBACK_RESISTANCE);

    public static void onEquipmentChange(LivingEquipmentChangeEvent event) {
        refresh(event.getEntity());
    }

    public static void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
        refresh(event.getEntity());
    }

    private static void refresh(LivingEntity entity) {
        if (entity.level().isClientSide) return;
        removeManaged(entity);
        String role = SpaceSuitCatalog.completeRole(entity);
        if (role == null) return;
        switch (role) {
            case "emergency" -> {
                add(entity, Attributes.MOVEMENT_SPEED, role, -0.07, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                add(entity, Attributes.MAX_HEALTH, role, -2.0, AttributeModifier.Operation.ADD_VALUE);
            }
            case "surveyor" -> {
                add(entity, Attributes.MOVEMENT_SPEED, role, 0.10, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                add(entity, Attributes.BLOCK_INTERACTION_RANGE, role, 1.0, AttributeModifier.Operation.ADD_VALUE);
            }
            case "lunar_prospector" -> {
                add(entity, Attributes.MINING_EFFICIENCY, role, 3.0, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.BLOCK_INTERACTION_RANGE, role, 0.5, AttributeModifier.Operation.ADD_VALUE);
            }
            case "radiation" -> {
                add(entity, Attributes.MOVEMENT_SPEED, role, -0.08, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                add(entity, Attributes.EXPLOSION_KNOCKBACK_RESISTANCE, role, 0.25, AttributeModifier.Operation.ADD_VALUE);
            }
            case "heavy" -> {
                add(entity, Attributes.ARMOR_TOUGHNESS, role, 4.0, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.KNOCKBACK_RESISTANCE, role, 0.35, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.MOVEMENT_SPEED, role, -0.12, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
            }
            case "mobility" -> {
                add(entity, Attributes.MOVEMENT_SPEED, role, 0.15, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                add(entity, Attributes.SAFE_FALL_DISTANCE, role, 5.0, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.STEP_HEIGHT, role, 0.5, AttributeModifier.Operation.ADD_VALUE);
            }
            case "extended" -> {
                add(entity, Attributes.MAX_HEALTH, role, 4.0, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.MOVEMENT_SPEED, role, -0.05, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
            }
            case "martian" -> {
                add(entity, Attributes.MOVEMENT_EFFICIENCY, role, 0.20, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.MINING_EFFICIENCY, role, 2.0, AttributeModifier.Operation.ADD_VALUE);
            }
            case "venusian" -> {
                add(entity, Attributes.BURNING_TIME, role, -0.75, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                add(entity, Attributes.ARMOR_TOUGHNESS, role, 2.0, AttributeModifier.Operation.ADD_VALUE);
                add(entity, Attributes.MOVEMENT_SPEED, role, -0.08, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
            }
        }
    }

    private static void removeManaged(LivingEntity entity) {
        for (Holder<Attribute> attribute : MANAGED) {
            AttributeInstance instance = entity.getAttribute(attribute);
            if (instance == null) continue;
            for (String role : new String[]{"emergency", "surveyor", "lunar_prospector", "radiation", "heavy", "mobility", "extended", "martian", "venusian"}) {
                instance.removeModifier(id(role, attribute));
            }
        }
    }

    private static void add(LivingEntity entity, Holder<Attribute> attribute, String role, double amount, AttributeModifier.Operation operation) {
        AttributeInstance instance = entity.getAttribute(attribute);
        if (instance != null) instance.addOrUpdateTransientModifier(new AttributeModifier(id(role, attribute), amount, operation));
    }

    private static ResourceLocation id(String role, Holder<Attribute> attribute) {
        String name = attribute.unwrapKey().map(key -> key.location().getPath()).orElse("unknown");
        return ResourceLocation.fromNamespaceAndPath(InfiniteDomainSpaceIndustry.MOD_ID, "suit/" + role + "/" + name);
    }

    private SuitSpecializations() {}
}

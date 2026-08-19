package infinitedomain.cyberware;

import com.perigrine3.createcybernetics.api.CyberwareDurabilityCategory;
import com.perigrine3.createcybernetics.api.CyberwareRepairType;
import com.perigrine3.createcybernetics.api.CyberwareSlot;
import com.perigrine3.createcybernetics.api.ICyberwareItem;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;
import java.util.Set;

public final class BranchedCyberwareItem extends Item implements ICyberwareItem {
    private final CyberwareSlot slot;
    private final EffectFamily family;
    private final int tier;
    private final int humanity;
    private final TagKey<Item> branchTag;

    public BranchedCyberwareItem(Properties properties, CyberwareSlot slot, EffectFamily family, int tier, int humanity, String[] branchIds) {
        super(properties);
        this.slot = slot;
        this.family = family;
        this.tier = tier;
        this.humanity = humanity;
        this.branchTag = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(
            InfiniteDomainCyberware.MOD_ID, "branches/" + slot.name().toLowerCase()));
    }

    @Override
    public Set<CyberwareSlot> getSupportedSlots() { return Set.of(slot); }

    @Override
    public boolean replacesOrgan() { return false; }

    @Override
    public Set<CyberwareSlot> getReplacedOrgans() { return Set.of(); }

    @Override
    public int getHumanityCost() { return humanity; }

    @Override
    public int maxStacksPerSlotType(ItemStack stack, CyberwareSlot installedSlot) { return 1; }

    @Override
    public Set<TagKey<Item>> sameSlotIncompatibleCyberwareTags(ItemStack stack, CyberwareSlot installedSlot) {
        return Set.of(branchTag);
    }

    @Override
    public boolean matchesCyberwareTagAsInstalled(ItemStack stack, CyberwareSlot installedSlot, TagKey<Item> tag) {
        return tag.equals(branchTag) || ICyberwareItem.super.matchesCyberwareTagAsInstalled(stack, installedSlot, tag);
    }

    @Override
    public int getEnergyUsedPerTick(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot) {
        return tier == 0 ? 0 : tier == 1 ? 1 : tier == 2 ? 3 : 7;
    }

    @Override
    public boolean requiresEnergyToFunction(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot) {
        return tier > 0;
    }

    @Override
    public int getEnergyPriority(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot) {
        return 20 + tier * 10;
    }

    @Override
    public CyberwareDurabilityCategory getDurabilityCategory(ItemStack stack, CyberwareSlot installedSlot) {
        return CyberwareDurabilityCategory.CYBERNETIC;
    }

    @Override
    public CyberwareRepairType getRepairType(ItemStack stack, CyberwareSlot installedSlot) {
        return CyberwareRepairType.CYBERNETIC;
    }

    @Override
    public int getMaxCyberwareDurability(ItemStack stack, CyberwareSlot installedSlot) {
        return new int[]{320, 720, 1440, 2880}[tier];
    }

    @Override
    public boolean functionsWhenBroken(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot) { return false; }

    @Override
    public void onTick(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot, int index) {
        if (tier == 0) applyEffect(entity, family.penalty, 0);
    }

    @Override
    public void onPoweredTick(LivingEntity entity, ItemStack stack, CyberwareSlot installedSlot) {
        applyEffect(entity, family.benefit, tier == 3 ? 1 : 0);
    }

    private void applyEffect(LivingEntity entity, Holder<MobEffect> effect, int amplifier) {
        if (!entity.level().isClientSide && entity.tickCount % 20 == 0) {
            entity.addEffect(new MobEffectInstance(effect, 45, amplifier, true, false, true));
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltip, flag);
        tooltip.add(Component.translatable("tooltip.infinite_domain_cyberware.branch." + tier).withStyle(
            tier == 0 ? ChatFormatting.RED : tier == 1 ? ChatFormatting.GOLD : tier == 2 ? ChatFormatting.AQUA : ChatFormatting.LIGHT_PURPLE));
        tooltip.add(Component.translatable("tooltip.infinite_domain_cyberware.family." + family.name().toLowerCase()).withStyle(ChatFormatting.GRAY));
    }

    public enum EffectFamily {
        COGNITION(MobEffects.CONFUSION, MobEffects.DIG_SPEED),
        OPTICS(MobEffects.BLINDNESS, MobEffects.NIGHT_VISION),
        CIRCULATION(MobEffects.WEAKNESS, MobEffects.REGENERATION),
        RESPIRATION(MobEffects.DIG_SLOWDOWN, MobEffects.WATER_BREATHING),
        METABOLISM(MobEffects.HUNGER, MobEffects.DAMAGE_RESISTANCE),
        LIMB_POWER(MobEffects.DIG_SLOWDOWN, MobEffects.DIG_SPEED),
        LOCOMOTION(MobEffects.MOVEMENT_SLOWDOWN, MobEffects.MOVEMENT_SPEED),
        MUSCLE(MobEffects.WEAKNESS, MobEffects.DAMAGE_BOOST),
        SKELETON(MobEffects.MOVEMENT_SLOWDOWN, MobEffects.DAMAGE_RESISTANCE),
        DERMIS(MobEffects.WEAKNESS, MobEffects.FIRE_RESISTANCE);

        final Holder<MobEffect> penalty;
        final Holder<MobEffect> benefit;
        EffectFamily(Holder<MobEffect> penalty, Holder<MobEffect> benefit) {
            this.penalty = penalty;
            this.benefit = benefit;
        }
    }
}

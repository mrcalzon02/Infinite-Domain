package infinitedomain.bootcompat;

import net.neoforged.fml.common.Mod;
import net.neoforged.fml.ModList;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.DefaultAttributes;

@Mod(BootDataCompat.MOD_ID)
public final class BootDataCompat {
    public static final String MOD_ID = "infinite_domain_boot_data_compat";

    public BootDataCompat(IEventBus bus) {
        bus.addListener(EventPriority.LOWEST, this::registerJellyAttributes);
    }

    @SuppressWarnings("unchecked")
    private void registerJellyAttributes(EntityAttributeCreationEvent event) {
        // This release omits its supplier. Future releases need a fresh audit,
        // rather than having their own balance overwritten by a fallback.
        boolean affectedRelease = ModList.get().getModContainerById("jaffabricate")
            .map(mod -> "1.1.3".equals(mod.getModInfo().getVersion().toString())).orElse(false);
        if (!affectedRelease) return;
        EntityType<?> type = BuiltInRegistries.ENTITY_TYPE.getOptional(
            ResourceLocation.parse("jaffabricate:orange_jelly_slime")).orElse(null);
        if (type == null || DefaultAttributes.hasSupplier(type)) return;
        // Match vanilla slime's complete supplier. Jaffabricate's setSize then
        // owns health=size^2, speed=0.2+0.1*size, and attack=size as intended.
        event.put((EntityType<? extends LivingEntity>) type,
            DefaultAttributes.getSupplier(EntityType.SLIME));
    }
}

package infinitedomain.space;

import com.fej1fun.potentials.components.FluidAmountMapDataComponent;
import com.fej1fun.potentials.fluid.ItemFluidStorage;
import com.fej1fun.potentials.fluid.UniversalFluidItemStorage;
import com.st0x0ef.stellaris.common.items.armors.SpaceSuit;
import com.st0x0ef.stellaris.common.registry.ArmorMaterialsRegistry;
import com.st0x0ef.stellaris.common.registry.DataComponentsRegistry;
import com.st0x0ef.stellaris.common.registry.FluidRegistry;
import dev.architectury.fluid.FluidStack;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;

public final class RoleSpaceSuit extends SpaceSuit {
    private final String role;
    private final String displayName;
    private final int oxygenCapacity;

    public RoleSpaceSuit(Properties properties, ArmorItem.Type type, String role, String displayName, int oxygenCapacity) {
        super(ArmorMaterialsRegistry.SPACE_SUIT, type, properties);
        this.role = role;
        this.displayName = displayName;
        this.oxygenCapacity = oxygenCapacity;
    }

    public String role() {
        return role;
    }

    @Override
    public UniversalFluidItemStorage getFluidTank(ItemStack stack) {
        return new ItemFluidStorage(DataComponentsRegistry.FLUID_LIST.get(), stack, 2, oxygenCapacity) {
            @Override
            public boolean isFluidValid(int tank, FluidStack fluid) {
                if (tank == 0) {
                    return fluid.getFluid().isSame(FluidRegistry.OXYGEN_STILL.get());
                }
                return tank == 1 && fluid.getFluid().isSame(FluidRegistry.DIESEL_STILL.get());
            }
        };
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltip, flag);
        tooltip.add(Component.literal(displayName).withStyle(ChatFormatting.AQUA));
        tooltip.add(Component.translatable("tooltip.infinite_domain_space." + role).withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.literal("Stellaris oxygen capacity: " + oxygenCapacity + " mB").withStyle(ChatFormatting.DARK_GRAY));
        tooltip.add(Component.literal("Full matching set required for pressure protection").withStyle(ChatFormatting.DARK_GRAY));
    }
}

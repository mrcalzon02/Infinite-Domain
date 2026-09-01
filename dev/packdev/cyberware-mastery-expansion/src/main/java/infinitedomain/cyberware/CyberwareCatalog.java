package infinitedomain.cyberware;

import com.perigrine3.createcybernetics.api.CyberwareSlot;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.LinkedHashMap;
import java.util.Map;

public final class CyberwareCatalog {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(InfiniteDomainCyberware.MOD_ID);
    public static final Map<String, DeferredItem<? extends Item>> CATALOG = new LinkedHashMap<>();

    private static final Entry[] ENTRIES = {
        entry(CyberwareSlot.BRAIN, BranchedCyberwareItem.EffectFamily.COGNITION, "fragmented_coprocessor", "reclaimed_reflex_cache", "calibrated_cortex_mesh", "darknet_ghost_coprocessor"),
        entry(CyberwareSlot.EYES, BranchedCyberwareItem.EffectFamily.OPTICS, "cracked_optic_rig", "reclaimed_spectrum_array", "calibrated_horizon_lens", "darknet_omnivision_array"),
        entry(CyberwareSlot.HEART, BranchedCyberwareItem.EffectFamily.CIRCULATION, "arrhythmic_aux_pump", "reclaimed_platelet_engine", "calibrated_aortic_turbine", "darknet_phylactery_pump"),
        entry(CyberwareSlot.LUNGS, BranchedCyberwareItem.EffectFamily.RESPIRATION, "leaky_oxygen_baffle", "reclaimed_gill_exchanger", "calibrated_hyperlung", "darknet_void_breather"),
        entry(CyberwareSlot.ORGANS, BranchedCyberwareItem.EffectFamily.METABOLISM, "fouled_nutrient_reclaimer", "reclaimed_chem_filter", "calibrated_metabolic_forge", "darknet_entropy_gut"),
        entry(CyberwareSlot.RARM, BranchedCyberwareItem.EffectFamily.LIMB_POWER, "seized_rightarm_servo", "reclaimed_rightarm_tooling", "calibrated_rightarm_mantis_drive", "darknet_rightarm_arc_limb"),
        entry(CyberwareSlot.LARM, BranchedCyberwareItem.EffectFamily.LIMB_POWER, "seized_leftarm_servo", "reclaimed_leftarm_tooling", "calibrated_leftarm_mantis_drive", "darknet_leftarm_arc_limb"),
        entry(CyberwareSlot.RLEG, BranchedCyberwareItem.EffectFamily.LOCOMOTION, "bent_rightleg_actuator", "reclaimed_rightleg_tendon", "calibrated_rightleg_vector_drive", "darknet_rightleg_blink_stride"),
        entry(CyberwareSlot.LLEG, BranchedCyberwareItem.EffectFamily.LOCOMOTION, "bent_leftleg_actuator", "reclaimed_leftleg_tendon", "calibrated_leftleg_vector_drive", "darknet_leftleg_blink_stride"),
        entry(CyberwareSlot.MUSCLE, BranchedCyberwareItem.EffectFamily.MUSCLE, "frayed_myomer_bundle", "reclaimed_torque_fiber", "calibrated_reflex_myomer", "darknet_sandevistan_mesh"),
        entry(CyberwareSlot.BONE, BranchedCyberwareItem.EffectFamily.SKELETON, "warped_lattice_splint", "reclaimed_capacitor_frame", "calibrated_gravitic_lacing", "darknet_singularity_skeleton"),
        entry(CyberwareSlot.SKIN, BranchedCyberwareItem.EffectFamily.DERMIS, "patchwork_dermal_mesh", "reclaimed_reactive_dermis", "calibrated_ablative_skin", "darknet_nullweave")
    };

    private static final String[] COMPONENTS = {
        "frayed_neural_bus", "cracked_optic_array", "arrhythmic_pump_core", "punctured_air_cell",
        "fouled_metabolic_mesh", "seized_rightarm_cluster", "seized_leftarm_cluster", "bent_rightleg_pair",
        "bent_leftleg_pair", "torn_myomer_bundle", "warped_frame_strut", "delaminated_dermis",
        "ghost_circuit_lattice", "quantum_synapse_matrix", "void_shield_mesh", "datavore_control_core"
    };

    static {
        for (String component : COMPONENTS) {
            CATALOG.put(component, ITEMS.registerSimpleItem(component, new Item.Properties().stacksTo(64)));
        }
        for (Entry entry : ENTRIES) {
            for (int tier = 0; tier < entry.ids.length; tier++) {
                final int branchTier = tier;
                final String id = entry.ids[tier];
                CATALOG.put(id, ITEMS.register(id, () -> new BranchedCyberwareItem(
                    new Item.Properties().stacksTo(1), entry.slot, entry.family, branchTier, 2 + branchTier * 2, entry.ids
                )));
            }
        }
    }

    public static void register(IEventBus modBus) {
        ITEMS.register(modBus);
    }

    private static Entry entry(CyberwareSlot slot, BranchedCyberwareItem.EffectFamily family, String... ids) {
        return new Entry(slot, family, ids);
    }

    private record Entry(CyberwareSlot slot, BranchedCyberwareItem.EffectFamily family, String[] ids) {}

    private CyberwareCatalog() {}
}

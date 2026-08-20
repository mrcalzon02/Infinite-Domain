// [SYSTEM REPORT] Supplemental Old World lore items only.
// Canonical deterministic proof items are registered exclusively by
// kubejs/startup_scripts/old_world_evidence_items.js from
// kubejs/config/old_world_evidence.json. Do not duplicate those 64 IDs here.
StartupEvents.registry('item', event => {
    event.create('vcf_return_crate_log')
        .displayName('VCF Return-Crate Exception Log')
        .texture('minecraft:item/written_book').rarity('uncommon').maxStackSize(1)
        .tooltip('§aVCF Culture Services // early anomaly record')
        .tooltip('§7Spoiled seals and delayed returns begin appearing on an otherwise ordinary route')

    event.create('vcf_global_licensing_brief')
        .displayName('VCF Global Licensing Brief')
        .texture('minecraft:item/written_book').rarity('rare').maxStackSize(1)
        .tooltip('§aLOR-005 // worldwide Evercrop distribution')
        .tooltip('§7The cultures crossed every perimeter before the crisis had a name')

    event.create('atlas_transfer_maintenance_manual')
        .displayName('Automated Transfer Maintenance Manual')
        .texture('minecraft:item/written_book')
        .rarity('uncommon')
        .maxStackSize(1)
        .tooltip('§6Atlas Kinetic Industries // Field Edition 6')
        .tooltip('§7Service lanes, transfer gearing, lockout procedure, and spare-shaft tolerances')
        .tooltip('§8LOR-006 // Early Old World industrial record')

    event.create('polycore_service_interval_board')
        .displayName('PolyCore Seal Replacement Interval Board')
        .texture('create:item/clipboard').rarity('rare').maxStackSize(1)
        .tooltip('§dLOR-008 // shrinking service intervals')
        .tooltip('§7Twelve months. Six. Three. Weekly. Then blank.')

    event.create('polycore_exposure_test_04')
        .displayName('PolyCore Elastomer Exposure Test 04')
        .texture('minecraft:item/written_book').rarity('rare').maxStackSize(1)
        .tooltip('§dLOR-009 // repeat biological degradation')
        .tooltip('§7The fourth controlled repetition ended the argument about measurement error')
})

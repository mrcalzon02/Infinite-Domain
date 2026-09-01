$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root 'packdev\cyberware-mastery-expansion'
$resources = Join-Path $project 'src\main\resources'
$ns = 'infinite_domain_cyberware'
$assets = Join-Path $resources "assets\$ns"
$data = Join-Path $resources "data\$ns"

foreach ($generatedRoot in @($assets, $data, (Join-Path $resources 'data\cyber_ware_port'))) {
    if (Test-Path -LiteralPath $generatedRoot) {
        Remove-Item -LiteralPath $generatedRoot -Recurse -Force
    }
}

$regions = @(
    @{ slot='brain'; salvage='frayed_neural_bus'; port='brain_upgrades_neural_contextualizer'; create='brainupgrades_neuralprocessor'; component='component_ssd'; ids=@('fragmented_coprocessor','reclaimed_reflex_cache','calibrated_cortex_mesh','darknet_ghost_coprocessor') },
    @{ slot='eyes'; salvage='cracked_optic_array'; port='cybereye_upgrades_targeting'; create='eyeupgrades_targeting'; component='component_fiberoptics'; ids=@('cracked_optic_rig','reclaimed_spectrum_array','calibrated_horizon_lens','darknet_omnivision_array') },
    @{ slot='heart'; salvage='arrhythmic_pump_core'; port='heart_upgrades_platelets'; create='heartupgrades_platelets'; component='component_storage'; ids=@('arrhythmic_aux_pump','reclaimed_platelet_engine','calibrated_aortic_turbine','darknet_phylactery_pump') },
    @{ slot='lungs'; salvage='punctured_air_cell'; port='lungs_upgrades_hyperoxygenation'; create='lungsupgrades_hyperoxygenation'; component='component_storage'; ids=@('leaky_oxygen_baffle','reclaimed_gill_exchanger','calibrated_hyperlung','darknet_void_breather') },
    @{ slot='organs'; salvage='fouled_metabolic_mesh'; port='lower_organs_upgrades_metabolic'; create='organsupgrades_metabolic'; component='component_mesh'; ids=@('fouled_nutrient_reclaimer','reclaimed_chem_filter','calibrated_metabolic_forge','darknet_entropy_gut') },
    @{ slot='rarm'; salvage='seized_rightarm_cluster'; port='cyberlimbs_cyberarm_right'; create='basecyberware_rightarm_ironplated'; component='component_actuator'; ids=@('seized_rightarm_servo','reclaimed_rightarm_tooling','calibrated_rightarm_mantis_drive','darknet_rightarm_arc_limb') },
    @{ slot='larm'; salvage='seized_leftarm_cluster'; port='cyberlimbs_cyberarm_left'; create='basecyberware_leftarm_ironplated'; component='component_actuator'; ids=@('seized_leftarm_servo','reclaimed_leftarm_tooling','calibrated_leftarm_mantis_drive','darknet_leftarm_arc_limb') },
    @{ slot='rleg'; salvage='bent_rightleg_pair'; port='cyberlimbs_cyberleg_right'; create='basecyberware_rightleg_ironplated'; component='component_actuator'; ids=@('bent_rightleg_actuator','reclaimed_rightleg_tendon','calibrated_rightleg_vector_drive','darknet_rightleg_blink_stride') },
    @{ slot='lleg'; salvage='bent_leftleg_pair'; port='cyberlimbs_cyberleg_left'; create='basecyberware_leftleg_ironplated'; component='component_actuator'; ids=@('bent_leftleg_actuator','reclaimed_leftleg_tendon','calibrated_leftleg_vector_drive','darknet_leftleg_blink_stride') },
    @{ slot='muscle'; salvage='torn_myomer_bundle'; port='muscle_upgrades_wired_reflexes'; create='muscleupgrades_wiredreflexes'; component='component_synthnerves'; ids=@('frayed_myomer_bundle','reclaimed_torque_fiber','calibrated_reflex_myomer','darknet_sandevistan_mesh') },
    @{ slot='bone'; salvage='warped_frame_strut'; port='bone_upgrades_bonelacing'; create='boneupgrades_bonelacing'; component='component_plating'; ids=@('warped_lattice_splint','reclaimed_capacitor_frame','calibrated_gravitic_lacing','darknet_singularity_skeleton') },
    @{ slot='skin'; salvage='delaminated_dermis'; port='skin_upgrades_subdermal_spikes'; create='skinupgrades_subdermalarmor'; component='component_mesh'; ids=@('patchwork_dermal_mesh','reclaimed_reactive_dermis','calibrated_ablative_skin','darknet_nullweave') }
)
$components = @('frayed_neural_bus','cracked_optic_array','arrhythmic_pump_core','punctured_air_cell','fouled_metabolic_mesh','seized_rightarm_cluster','seized_leftarm_cluster','bent_rightleg_pair','bent_leftleg_pair','torn_myomer_bundle','warped_frame_strut','delaminated_dermis','ghost_circuit_lattice','quantum_synapse_matrix','void_shield_mesh','datavore_control_core')
$assemblies = @('ghost_circuit_lattice','quantum_synapse_matrix','void_shield_mesh','datavore_control_core')
$chems = @('stim_autoinjector','immunoboost_autoinjector','roid_autoinjector','warp_autoinjector')
$spaceParts = @('stellaris:heavy_metal_plate','stellaris:desh_ingot','stellaris:heavy_metal_plate')

function Write-Json([string]$path, $value) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $path) -Force | Out-Null
    $value | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $path -Encoding utf8
}
function Ingredient([string]$id) { return @{ item=$id } }
function Engineering([string]$output, [string[]]$inputs) {
    $letters = @('A','B','C','D','E')
    $key = [ordered]@{}
    for ($i=0; $i -lt $inputs.Count; $i++) { $key[$letters[$i]] = Ingredient $inputs[$i] }
    $patterns = @('  A  ',' ABC ',' BDB ',' CEC ','  A  ')
    if ($inputs.Count -eq 1) { $patterns=@('     ','     ','  A  ','     ','     ') }
    return [ordered]@{ type='createcybernetics:engineering_table'; accept_mirrored=$true; category='misc'; key=$key; pattern=$patterns; result=@{ count=1; id=$output } }
}

New-Item -ItemType Directory -Path (Join-Path $assets 'models\item'), (Join-Path $assets 'textures\item'), (Join-Path $assets 'lang') -Force | Out-Null
$lang = [ordered]@{
    'tooltip.infinite_domain_cyberware.branch.0'='Degraded: low-durability hardware with an active fault';
    'tooltip.infinite_domain_cyberware.branch.1'='Reclaimed: stabilized donor hardware';
    'tooltip.infinite_domain_cyberware.branch.2'='Calibrated: space-age specialist assembly';
    'tooltip.infinite_domain_cyberware.branch.3'='Darknet: end-era integration, high power and humanity burden';
    'tooltip.infinite_domain_cyberware.family.cognition'='Cognition and response processing';
    'tooltip.infinite_domain_cyberware.family.optics'='Environmental and targeting optics';
    'tooltip.infinite_domain_cyberware.family.circulation'='Circulatory reinforcement';
    'tooltip.infinite_domain_cyberware.family.respiration'='Respiratory adaptation';
    'tooltip.infinite_domain_cyberware.family.metabolism'='Metabolic regulation';
    'tooltip.infinite_domain_cyberware.family.limb_power'='Powered arm actuation';
    'tooltip.infinite_domain_cyberware.family.locomotion'='Powered leg actuation';
    'tooltip.infinite_domain_cyberware.family.muscle'='Synthetic muscle output';
    'tooltip.infinite_domain_cyberware.family.skeleton'='Skeletal stabilization';
    'tooltip.infinite_domain_cyberware.family.dermis'='Dermal environmental protection'
}
foreach ($component in $components) {
    $lang["item.$ns.$component"] = (Get-Culture).TextInfo.ToTitleCase(($component -replace '_',' '))
    Write-Json (Join-Path $assets "models\item\$component.json") @{ parent='minecraft:item/generated'; textures=@{ layer0="${ns}:item/$component" } }
}
foreach ($region in $regions) { foreach ($id in $region.ids) {
    $lang["item.$ns.$id"] = (Get-Culture).TextInfo.ToTitleCase(($id -replace '_',' '))
    Write-Json (Join-Path $assets "models\item\$id.json") @{ parent='minecraft:item/generated'; textures=@{ layer0="${ns}:item/$id" } }
} }
Write-Json (Join-Path $assets 'lang\en_us.json') $lang

# Port implants become the twelve degraded donor cores.
foreach ($region in $regions) {
    Write-Json (Join-Path $data "recipe\salvage_$($region.slot).json") (Engineering "${ns}:$($region.salvage)" @("cyber_ware_port:$($region.port)"))
}

# Component bridge: Port parts feed the richer Create Cybernetics engineering ecosystem.
$bridges = [ordered]@{
    component_actuator='component_actuator'; component_fiberoptics='component_fiberoptics'; component_plating='component_plating';
    component_storage='component_storage'; component_synthnerves='component_synthnerves'; component_microelectric='component_wiring';
    component_ssc='component_ssd'; component_titanium='titaniumingot'; component_fullerene='component_mesh'; component_reactor='component_storage'
}
foreach ($source in $bridges.Keys) {
    Write-Json (Join-Path $data "recipe\bridge_$source.json") (Engineering "createcybernetics:$($bridges[$source])" @("cyber_ware_port:$source"))
}

$assemblyInputs = [ordered]@{
    ghost_circuit_lattice=@('createcybernetics:brainupgrades_neuralprocessor','cyber_ware_port:component_fiberoptics','kubejs:darknet_data_cache','createcybernetics:component_wiring','stellaris:heavy_metal_plate');
    quantum_synapse_matrix=@("${ns}:ghost_circuit_lattice",'createcybernetics:component_ssd','kubejs:darknet_session_injector_tier_6','stellaris:desh_ingot','cyber_ware_port:component_ssc');
    void_shield_mesh=@("${ns}:delaminated_dermis",'createcybernetics:component_mesh','kubejs:darknet_session_injector_tier_7','stellaris:heavy_metal_plate','cyber_ware_port:component_fullerene');
    datavore_control_core=@("${ns}:quantum_synapse_matrix","${ns}:void_shield_mesh",'kubejs:darknet_temporal_core','kubejs:darknet_session_injector_tier_8','cyber_ware_port:component_reactor')
}
foreach ($assembly in $assemblies) {
    Write-Json (Join-Path $data "recipe\$assembly.json") (Engineering "${ns}:$assembly" $assemblyInputs[$assembly])
}

for ($ri=0; $ri -lt $regions.Count; $ri++) {
    $region=$regions[$ri]
    for ($tier=0; $tier -lt 4; $tier++) {
        $id=$region.ids[$tier]
        if ($tier -eq 0) {
            $inputs=@("${ns}:$($region.salvage)","createcybernetics:$($region.component)",'minecraft:iron_ingot',"cyber_ware_port:component_plating",'minecraft:redstone')
        } elseif ($tier -eq 1) {
            $inputs=@("${ns}:$($region.ids[0])","cyber_ware_port:$($region.port)","cyberchems:$($chems[$ri % 4])","createcybernetics:$($region.component)",'minecraft:gold_ingot')
        } elseif ($tier -eq 2) {
            $inputs=@("${ns}:$($region.ids[1])","createcybernetics:$($region.create)",$spaceParts[$ri % 3],'createcybernetics:component_synthnerves',"cyber_ware_port:$($region.port)")
        } else {
            $inputs=@("${ns}:$($region.ids[2])","${ns}:$($assemblies[$ri % 4])",('kubejs:darknet_session_injector_tier_' + (5 + ($ri % 4))),'kubejs:encrypted_credential_bundle','kubejs:darknet_temporal_core')
        }
        Write-Json (Join-Path $data "recipe\$id.json") (Engineering "${ns}:$id" $inputs)
    }
    Write-Json (Join-Path $data "tags\item\branches\$($region.slot).json") @{ replace=$false; values=($region.ids | ForEach-Object { "${ns}:$_" }) }
}
Write-Json (Join-Path $data 'tags\item\salvage_components.json') @{ replace=$false; values=($components[0..11] | ForEach-Object { "${ns}:$_" }) }
Write-Json (Join-Path $data 'tags\item\high_end_assemblies.json') @{ replace=$false; values=($assemblies | ForEach-Object { "${ns}:$_" }) }

# Recover obsolete Port clinic hardware into the authoritative Create Cybernetics machine.
Write-Json (Join-Path $data 'recipe\recover_legacy_clinic.json') (Engineering 'createcybernetics:robosurgeon' @('cyber_ware_port:robo_surgeon','cyber_ware_port:surgery_chamber','createcybernetics:component_actuator','createcybernetics:component_wiring','createcybernetics:component_plating'))

$javac='C:\Program Files\Pylo\MCreator\jdk\bin\javac.exe'
$java='C:\Program Files\Pylo\MCreator\jdk\bin\java.exe'
$toolClasses=Join-Path $project 'build\texture-tool'
New-Item -ItemType Directory -Path $toolClasses -Force | Out-Null
& $javac -d $toolClasses (Join-Path $root 'scripts\CyberwareTextureGenerator.java')
if ($LASTEXITCODE -ne 0) { throw 'Texture generator compilation failed' }
& $java -cp $toolClasses CyberwareTextureGenerator (Join-Path $root 'mods\createcybernetics-0.5.1-neoforge-1.21.1-HOTFIX.jar') (Join-Path $assets 'textures\item')
if ($LASTEXITCODE -ne 0) { throw 'Texture generation failed' }
Write-Output 'Generated 48 native implants, 16 custom parts, 75 recipes, models, language, tags, and textures.'

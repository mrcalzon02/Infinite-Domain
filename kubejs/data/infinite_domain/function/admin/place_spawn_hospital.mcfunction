# Destructive one-shot admin utility. Places the completed 48x48x48 spawn
# hospital lobby exactly where it was authored: X/Z -24..23, Y 56..103.
# Terrain preparation creates a dry hospital apron at Y=61 and grades it back
# into the untouched sea-level Wasteland surface through Y=62 and Y=63 bands.
function infinite_domain:admin/prepare_spawn_hospital_terrain
place template infinite_domain:spawn_hospital_lobby -24 56 -24
function infinite_domain:admin/set_spawn_hub
tellraw @a [{"text":"[Infinite Domain] ","color":"gold"},{"text":"The completed spawn hospital and its blended terrain apron have been placed. Hospital X/Z -24..23, Y 56..103; parking-lot spawn Y 64.","color":"yellow"}]

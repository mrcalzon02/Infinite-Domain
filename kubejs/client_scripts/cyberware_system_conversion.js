// KubeJS 1.21+ replaced viewer-specific JEIEvents with RecipeViewerEvents.
RecipeViewerEvents.removeEntries('item', event => {
    event.remove('cyber_ware_port:robo_surgeon')
    event.remove('cyber_ware_port:surgery_chamber')
})

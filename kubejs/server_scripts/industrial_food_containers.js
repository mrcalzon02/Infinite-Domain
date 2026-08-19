// FoodProperties.usingConvertsTo resolves ItemStacks before KubeJS custom items
// exist. Return containers after consumption instead, when every registry is live.
const industrialFoodContainers = JsonIO.read('kubejs/config/industrial_food.json')

industrialFoodContainers.consumables.forEach(product => {
    if (product.container) {
        ItemEvents.foodEaten(`kubejs:${product.id}`, event => {
            event.player.give(product.container)
        })
    }
})

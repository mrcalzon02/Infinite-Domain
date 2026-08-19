package infinitedomain.darknet.client;

import infinitedomain.darknet.entity.DarknetEntities;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

public final class DarknetClient {
    private DarknetClient() {}

    public static void register(IEventBus bus) {
        bus.addListener(DarknetClient::registerRenderers);
    }

    private static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(DarknetEntities.DARKNET_TRADER.get(), DarknetTraderRenderer::new);
        event.registerEntityRenderer(DarknetEntities.DARKNET_RABBIT.get(), DarknetRabbitRenderer::new);
        event.registerEntityRenderer(DarknetEntities.DARKNET_COW.get(), DarknetCowRenderer::new);
        event.registerEntityRenderer(DarknetEntities.DARKNET_HOUND.get(), DarknetWolfRenderer::new);
        event.registerEntityRenderer(DarknetEntities.DARKNET_FOX.get(), DarknetFoxRenderer::new);
        event.registerEntityRenderer(DarknetEntities.DARKNET_SLIME.get(), DarknetSlimeRenderer::new);
    }
}

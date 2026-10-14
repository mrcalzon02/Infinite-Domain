package infinitedomain.bootcompat.mixin;

import infinitedomain.bootcompat.TagJsonRepairs;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.tags.TagLoader;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(value = TagLoader.class, remap = false)
public abstract class TagLoaderMixin {
    @Redirect(method = "load", at = @At(value = "INVOKE",
        target = "Lnet/minecraft/server/packs/resources/Resource;openAsReader()Ljava/io/BufferedReader;"), require = 1)
    private BufferedReader infiniteDomain$repairUpstreamTag(Resource resource) throws IOException {
        String pack = resource.sourcePackId();
        BufferedReader reader = resource.openAsReader();
        if (!"mod/tracks".equals(pack) && !"mod/primitivestart".equals(pack)) return reader;
        StringBuilder json = new StringBuilder();
        try (reader) {
            char[] buffer = new char[4096];
            int length;
            while ((length = reader.read(buffer)) != -1) json.append(buffer, 0, length);
        }
        return new BufferedReader(new StringReader(TagJsonRepairs.repair(pack, json.toString())));
    }
}

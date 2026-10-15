package infinitedomain.bootcompat;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import java.nio.file.Files;
import java.nio.file.Path;

public final class PhysicsRepairSelfTest {
    public static void main(String[] args) throws Exception {
        JsonElement original = JsonParser.parseString(Files.readString(Path.of(args[0])));
        check(true, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", original,
            "mod/linearbearing", original), "exact installed duplicate");
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("file/user_pack", original,
            "mod/linearbearing", original), "user dimension override");
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", original,
            "file/user_pack", original), "user block override");
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", original,
            "mod/linearbearing", null), "missing counterpart");
        JsonElement changed = original.deepCopy();
        changed.getAsJsonObject().getAsJsonObject("physics_properties").addProperty("force_modifier", 200);
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", changed,
            "mod/linearbearing", changed), "changed legacy intent");
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", original,
            "mod/linearbearing", changed), "nonidentical counterpart");
        changed = original.deepCopy();
        changed.getAsJsonObject().addProperty("dimension", "minecraft:overworld");
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", changed,
            "mod/linearbearing", changed), "valid dimension binding");
        changed = original.deepCopy();
        changed.getAsJsonObject().addProperty("future_field", true);
        check(false, MisfiledPhysicsRepairs.shouldQuarantine("mod/linearbearing", changed,
            "mod/linearbearing", changed), "future payload shape");
        System.out.println("PASS: eight exact-payload, owner, counterpart and update-boundary checks.");
    }

    private static void check(boolean expected, boolean actual, String name) {
        if (actual != expected) throw new AssertionError(name);
    }
}

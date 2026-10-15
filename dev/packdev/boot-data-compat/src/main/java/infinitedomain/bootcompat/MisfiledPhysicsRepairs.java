package infinitedomain.bootcompat;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

/** Recognize the exact legacy payload, never arbitrary invalid physics data. */
public final class MisfiledPhysicsRepairs {
    private static final JsonElement LEGACY = JsonParser.parseString("""
        {"block":"linearbearing:mechanical_linear_moving","physics_properties":{
          "universal_drag":0.09,"apply_kinetic_force":true,
          "force_modifier":100.0,"axis_alignment":"facing"}}
        """);

    private MisfiledPhysicsRepairs() {}

    public static boolean shouldQuarantine(String dimensionOwner, JsonElement dimension,
                                            String blockOwner, JsonElement block) {
        return "mod/linearbearing".equals(dimensionOwner)
            && "mod/linearbearing".equals(blockOwner)
            && LEGACY.equals(dimension) && dimension.equals(block);
    }
}

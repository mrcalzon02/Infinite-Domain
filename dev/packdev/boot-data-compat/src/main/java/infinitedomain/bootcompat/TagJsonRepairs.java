package infinitedomain.bootcompat;

/** Exact upstream tag defects only; called exclusively by the tag loader. */
public final class TagJsonRepairs {
    private TagJsonRepairs() {}

    public static String repair(String pack, String json) {
        if ("mod/tracks".equals(pack)) {
            // Only track_mount is registered in the installed release. Preserve
            // compatibility with releases that also register the other two.
            return json.replace("\"Tracks:track_mount\"", "\"tracks:track_mount\"")
                .replace("\"Tracks:suspension_track\"", "{\"id\":\"tracks:suspension_track\",\"required\":false}")
                .replace("\"Tracks:track_drive_wheel\"", "{\"id\":\"tracks:track_drive_wheel\",\"required\":false}");
        }
        if ("mod/primitivestart".equals(pack)
                && json.contains("\"remove\"")
                && json.contains("\"minecraft:iron_ore\"")
                && json.contains("\"minecraft:deepslate_iron_ore\"")
                && !json.contains("\"values\"")) {
            // NeoForge's removal extension still requires the vanilla values
            // array. Retain replace/remove and all other contents verbatim.
            return json.replaceFirst("\\{", "{\"values\":[],");
        }
        return json;
    }
}

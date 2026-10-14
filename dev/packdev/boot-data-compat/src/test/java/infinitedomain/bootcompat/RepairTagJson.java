package infinitedomain.bootcompat;

import java.nio.file.Files;
import java.nio.file.Path;

/** Test adapter: exercise the same transformer shipped in the installed jar. */
public final class RepairTagJson {
    public static void main(String[] args) throws Exception {
        System.out.print(TagJsonRepairs.repair(args[0], Files.readString(Path.of(args[1]))));
    }
}

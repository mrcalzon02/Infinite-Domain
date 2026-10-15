"""Build the project-owned tag compatibility jar without modifying upstream jars."""
from pathlib import Path
import hashlib
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'dev/packdev/boot-data-compat'


def main():
    libraries = Path('C:/Users/Admin/curseforge/minecraft/Install/libraries')
    relative = [
        'net/minecraft/client/1.21.1-20240808.144430/client-1.21.1-20240808.144430-srg.jar',
        'net/neoforged/fancymodloader/loader/4.0.43/loader-4.0.43.jar',
        'net/neoforged/bus/8.0.5/bus-8.0.5.jar',
        'net/neoforged/neoforge/21.1.248/neoforge-21.1.248-universal.jar',
        'net/fabricmc/sponge-mixin/0.15.2+mixin.0.8.7/sponge-mixin-0.15.2+mixin.0.8.7.jar',
        'com/mojang/datafixerupper/8.0.16/datafixerupper-8.0.16.jar',
        'com/mojang/brigadier/1.3.10/brigadier-1.3.10.jar',
        'net/neoforged/mergetool/2.0.7/mergetool-2.0.7-api.jar',
    ]
    dependencies = [libraries / p for p in relative]
    dependencies += list(libraries.glob('net/neoforged/neoforgespi/*/*.jar'))
    dependencies += list(libraries.glob('org/apache/maven/maven-artifact/*/*.jar'))
    assert all(p.is_file() for p in dependencies), 'Missing compiler dependency'
    build = PROJECT / 'build'
    classes = build / 'classes'
    classes.mkdir(parents=True, exist_ok=True)
    javac = Path('C:/Program Files/Java/jdk-26.0.1/bin/javac.exe')
    sources = sorted((PROJECT / 'src/main/java').rglob('*.java'))
    subprocess.run([str(javac), '--release', '21', '-proc:none', '-classpath',
                    ';'.join(map(str, dependencies)), '-d', str(classes), *map(str, sources)], check=True)
    candidate = build / 'infinite-domain-boot-data-compat-1.0.0.jar'
    # Stable entry order/timestamps make identical source builds reproducible.
    with zipfile.ZipFile(candidate, 'w', zipfile.ZIP_DEFLATED) as jar:
        for base in [classes, PROJECT / 'src/main/resources']:
            for file in sorted(p for p in base.rglob('*') if p.is_file()):
                info = zipfile.ZipInfo(file.relative_to(base).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                jar.writestr(info, file.read_bytes())
    output = ROOT / 'mods' / candidate.name
    shutil.copyfile(candidate, output)
    print(f'Built {output.name}; sha256={hashlib.sha256(output.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    main()

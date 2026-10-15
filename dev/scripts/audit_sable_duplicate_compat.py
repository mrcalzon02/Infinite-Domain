"""Check the installed duplicate-resource guard against original source data."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'dev/packdev/boot-data-compat'


def main():
    jar = ROOT / 'mods/infinite-domain-boot-data-compat-1.0.0.jar'
    gson = next(Path('C:/Users/Admin/curseforge/minecraft/Install/libraries/com/google/code/gson/gson').glob('*/*.jar'))
    upstream = next((ROOT / 'mods').glob('linearbearing-*.jar'))
    dimension = 'data/linearbearing/dimension_physics/mechanical_linear_moving.json'
    block = 'data/linearbearing/block_physics/mechanical_linear_moving.json'
    with zipfile.ZipFile(upstream) as z:
        original = z.read(dimension)
        assert json.loads(original) == json.loads(z.read(block))
        assert 'dimension' not in json.loads(original)
    scratch = ROOT / 'tmp/sable-duplicate-audit'
    scratch.mkdir(parents=True, exist_ok=True)
    source_data = scratch / 'original.json'
    source_data.write_bytes(original)
    java = Path('C:/Program Files/Java/jdk-26.0.1/bin')
    classes = PROJECT / 'build/physics-test-classes'
    classes.mkdir(parents=True, exist_ok=True)
    source = PROJECT / 'src/test/java/infinitedomain/bootcompat/PhysicsRepairSelfTest.java'
    cp = str(jar) + ';' + str(gson)
    subprocess.run([str(java / 'javac.exe'), '--release', '21', '-classpath', cp, '-d', str(classes), str(source)], check=True)
    subprocess.run([str(java / 'java.exe'), '-classpath', cp + ';' + str(classes),
                    'infinitedomain.bootcompat.PhysicsRepairSelfTest', str(source_data)], check=True)
    out = ROOT / 'dev/docs/boot-dimension-audit/revision-4'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'duplicate-guard-tests.json').write_text(json.dumps({
        'source_jar': upstream.name, 'dimension_resource': dimension, 'block_resource': block,
        'source_resource_sha256': hashlib.sha256(original).hexdigest(),
        'compat_jar_sha256': hashlib.sha256(jar.read_bytes()).hexdigest(),
        'checks_passed': 8, 'identical_source_payloads': True,
        'scope': 'Pure guard from installed jar; live loader marker and generation require the server run.'}, indent=2) + '\n')


if __name__ == '__main__':
    main()

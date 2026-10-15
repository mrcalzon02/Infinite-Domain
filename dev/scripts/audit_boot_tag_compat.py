"""Inventory all contributors to repaired tags and test the shipped transformer."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'dev/packdev/boot-data-compat'
TAGS = [
    'data/minecraft/tags/block/mineable/axe.json',
    'data/minecraft/tags/block/mineable/pickaxe.json',
    'data/create/tags/block/safe_nbt.json',
    'data/minecraft/tags/block/needs_stone_tool.json',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'dev/docs/boot-dimension-audit/revision-2')
    args = parser.parse_args()
    installed = ROOT / 'mods/infinite-domain-boot-data-compat-1.0.0.jar'
    tests = PROJECT / 'build/test-classes'
    tests.mkdir(parents=True, exist_ok=True)
    java = Path('C:/Program Files/Java/jdk-26.0.1/bin')
    test_source = PROJECT / 'src/test/java/infinitedomain/bootcompat/RepairTagJson.java'
    subprocess.run([str(java / 'javac.exe'), '--release', '21', '-classpath', str(installed),
                    '-d', str(tests), str(test_source)], check=True)
    scratch = ROOT / 'tmp/boot-tag-compat-audit'
    scratch.mkdir(parents=True, exist_ok=True)
    def repair(pack, text):
        file = scratch / 'input.json'
        file.write_text(text, encoding='utf-8')
        return subprocess.check_output([str(java / 'java.exe'), '-classpath',
            str(installed) + ';' + str(tests), 'infinitedomain.bootcompat.RepairTagJson',
            pack, str(file)], text=True)

    inventory = []
    repaired = []
    for jar_path in sorted((ROOT / 'mods').glob('*.jar')):
        with zipfile.ZipFile(jar_path) as jar:
            for resource in TAGS:
                if resource not in jar.namelist():
                    continue
                raw = jar.read(resource)
                text = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
                data = json.loads(text)
                inventory.append({'jar': jar_path.name, 'resource': resource,
                    'sha256': hashlib.sha256(raw).hexdigest(),
                    'replace': data.get('replace', False),
                    'value_count': len(data.get('values', [])),
                    'remove_count': len(data.get('remove', []))})
                if jar_path.name.startswith(('tracks-', 'primitivestart-')):
                    pack = 'mod/tracks' if jar_path.name.startswith('tracks-') else 'mod/primitivestart'
                    output = repair(pack, text)
                    result = json.loads(output)
                    if pack == 'mod/primitivestart' and 'values' in data:
                        assert output == text, 'Valid Primitive Start contribution changed'
                        continue
                    if pack == 'mod/tracks':
                        expected = dict(data)
                        expected['values'] = [
                            value.replace('Tracks:', 'tracks:') if value == 'Tracks:track_mount'
                            else {'id': value.replace('Tracks:', 'tracks:'), 'required': False}
                            for value in data['values']]
                    else:
                        expected = dict(data, values=[])
                    assert result == expected, (jar_path.name, resource, result)
                    assert repair(pack, output) == output, 'Repair is not idempotent'
                    assert repair('mod/unrelated', text) == text, 'Unrelated owner changed'
                    repaired.append({'jar': jar_path.name, 'resource': resource,
                                     'before': data, 'after': result})
    assert len(repaired) == 4, f'Expected four audited upstream defects, got {len(repaired)}'
    trace = json.loads((ROOT / 'kubejs/data/createreautomatedtraces/data_maps/block/trace_block_for_node.json').read_text())
    assert trace == {'values': {'createreautomated:ancient_debris_node': {'trace_block': 'minecraft:ancient_debris'}}}
    blocks = set((ROOT / 'dev/docs/registry-inventory/block-ids.txt').read_text().splitlines())
    assert {'createreautomated:ancient_debris_node', 'minecraft:ancient_debris', 'tracks:track_mount'} <= blocks
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / 'tag-resource-inventory.json').write_text(json.dumps({
        'compat_jar_sha256': hashlib.sha256(installed.read_bytes()).hexdigest(),
        'resource_contributions': inventory, 'repairs': repaired,
        'tests': {'actual_installed_transformer': True, 'idempotence': True,
                  'unrelated_pack_preserved': True, 'trace_ids_registered': True},
        'scope': 'Installed top-level mod contributions to four target tags; not a full live registry inventory.'
    }, indent=2) + '\n')
    print(f'PASS: {len(inventory)} tag resource contributions inventoried; four actual-jar transforms, idempotence, owner isolation, and Nether trace IDs verified.')


if __name__ == '__main__':
    main()

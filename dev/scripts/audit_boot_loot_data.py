"""Verify repaired book sources match generated loot and compat IDs resolve."""
from pathlib import Path
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'dev/scripts'))
import old_world_narrative_core as core


def main():
    books = 0
    for site, expected in core.AUDIO_DIARY_POOLS_BY_SITE.items():
        paths = list((ROOT / 'kubejs/data/infinite_domain/loot_table/chests/old_world').glob(
            f'ows_{site.split("-")[1]}_*.json'))
        assert len(paths) == 1, f'{site}: expected one runtime loot table'
        path = paths[0]
        live = json.loads(path.read_text(encoding='utf-8'))
        actual = [pool for pool in live['pools']
                  if any(entry.get('name') == 'minecraft:written_book' for entry in pool.get('entries', []))]
        assert actual == list(expected), f'{site}: canonical diary payload differs from live loot'
        books += len(actual)
    assert books == 54, f'Expected 54 diaries, got {books}'

    items = set((ROOT / 'dev/docs/registry-inventory/item-ids.txt').read_text().splitlines())
    leaves = json.loads((ROOT / 'kubejs/data/jaffabricate/tags/item/orange_leaves.json').read_text())
    assert set(leaves['values']) == {'jaffabricate:orange_leaves', 'jaffabricate:orange_leaves_alt'}
    assert set(leaves['values']).issubset(items)
    with zipfile.ZipFile(next((ROOT / 'mods').glob('ISS-*.jar'))) as jar:
        for ship in ['pirate_junk', 'unicorn_galleon']:
            resource = f'data/dungeons_arise_seven_seas/loot_table/chests/{ship}/{ship}_supply.json'
            original = jar.read(resource).decode('utf-8')
            live = json.loads((ROOT / 'kubejs' / resource).read_text())
            assert live == json.loads(original.replace('upgrade_aquatic:pickerelweed', 'minecraft:kelp'))
            def check(value):
                if isinstance(value, dict):
                    if value.get('type') == 'minecraft:item':
                        assert value['name'] in items, f'Unregistered ship supply: {value["name"]}'
                    for child in value.values(): check(child)
                elif isinstance(value, list):
                    for child in value: check(child)
            check(live)
    print('Boot loot audit passed: 54 canonical/live diaries match; both ship tables preserve weights/counts and resolve items; orange-leaves item tag resolves.')


if __name__ == '__main__':
    main()

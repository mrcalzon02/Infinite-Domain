"""Repair the audited book codec and missing upstream loot/tag references.

Idempotent; preserve all book pages, rewards, and loot probabilities. Upstream
jars are read as inputs, never modified. Canonical book sources are repaired
alongside their runtime outputs so regeneration preserves the corrected codec.
"""
from pathlib import Path
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'kubejs/data'


def main():
    repaired = 0
    mode = re.compile(r'"mode"\s*:\s*\{\s*"type"\s*:\s*"replace_all"\s*\}')
    for directory in [ROOT / 'dev/old_world_narrative/audio_diary_books',
                      DATA / 'infinite_domain/loot_table/chests/old_world']:
        for path in sorted(directory.glob('*.json')):
            original = path.read_text(encoding='utf-8')
            updated = mode.sub('"mode": "replace_all"', original)
            if updated != original:
                json.loads(updated)
                path.write_text(updated, encoding='utf-8')
                repaired += 1

    # ISS ships compatibility tables that override the Seven Seas originals.
    jars = list((ROOT / 'mods').glob('ISS-*.jar'))
    if len(jars) != 1:
        raise ValueError(f'Expected exactly one ISS compatibility jar, found {len(jars)}')
    with zipfile.ZipFile(jars[0]) as jar:
        for ship in ['pirate_junk', 'unicorn_galleon']:
            resource = f'data/dungeons_arise_seven_seas/loot_table/chests/{ship}/{ship}_supply.json'
            original = jar.read(resource).decode('utf-8')
            if 'upgrade_aquatic:pickerelweed' not in original:
                raise ValueError(f'Upstream supply table changed: {resource}; review compatibility repair')
            write_json(DATA / resource.removeprefix('data/'), json.loads(
                original.replace('upgrade_aquatic:pickerelweed', 'minecraft:kelp')))

    jars = list((ROOT / 'mods').glob('jaffabricate*.jar'))
    if len(jars) != 1:
        raise ValueError('Expected exactly one Jaffabricate jar')
    with zipfile.ZipFile(jars[0]) as jar:
        leaves = json.loads(jar.read('data/jaffabricate/tags/block/orange_leaves.json'))
        items = set((ROOT / 'dev/docs/registry-inventory/item-ids.txt').read_text().splitlines())
        # Fruit-stage blocks have no inventory item; only the two actual leaf
        # items belong in an item tag (the block tag still includes every stage).
        leaves['values'] = [item for item in leaves['values'] if item in items]
        if not leaves['values']:
            raise ValueError('No orange leaf item IDs resolve against the item inventory')
        write_json(DATA / 'jaffabricate/tags/item/orange_leaves.json', leaves)
    print(f'Boot data repaired: {repaired} book files updated; two ship supply overlays and the orange-leaves item tag ensured.')


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()

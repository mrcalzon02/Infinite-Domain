"""Inventory authored spawner NBT, including records attached to air blocks."""
from pathlib import Path
import gzip
import json
from collections import Counter
from build_structure_qa_world import Reader

ROOT = Path(__file__).resolve().parents[2]


def main():
    files = sorted((ROOT / 'kubejs/data').glob('*/structure/**/*.nbt'))
    owners = []
    failures = []
    scanned = 0
    total = 0
    for path in files:
        raw = path.read_bytes()
        if raw[:2] == b'\x1f\x8b':
            raw = gzip.decompress(raw)
        if b'minecraft:mob_spawner' not in raw:
            continue
        scanned += 1
        _, root = Reader(raw).root()
        document = root.value
        if 'palette' not in document or 'blocks' not in document:
            failures.append({'file': str(path.relative_to(ROOT)), 'reason': 'Unsupported template layout'})
            continue
        palette = [state.value['Name'].value for state in document['palette'].value.values]
        mobs = Counter()
        count = 0
        for entry in document['blocks'].value.values:
            block = entry.value
            nbt = block.get('nbt')
            if nbt is None or nbt.value.get('id') is None or nbt.value['id'].value != 'minecraft:mob_spawner':
                continue
            count += 1
            state = palette[block['state'].value]
            if state != 'minecraft:spawner':
                failures.append({'file': str(path.relative_to(ROOT)),
                    'position': [v.value for v in block['pos'].value.values], 'block': state,
                    'reason': 'Spawner block entity attached to a non-spawner state'})
            spawn = nbt.value.get('SpawnData')
            if spawn is not None:
                entity = spawn.value.get('entity')
                if entity is not None and 'id' in entity.value:
                    mobs[entity.value['id'].value] += 1
        if count:
            owners.append({'file': str(path.relative_to(ROOT)), 'spawners': count, 'entities': dict(mobs)})
        total += count
    out = ROOT / 'dev/docs/boot-dimension-audit/revision-2/spawner-payload-inventory.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'structure_files_considered': len(files),
        'templates_parsed': scanned, 'spawner_payloads': total,
        'templates_with_spawners': owners, 'failures': failures,
        'scope': 'Project kubejs/data/*/structure NBT only; excludes mod templates, Lost Cities palettes, runtime block changes and old saved chunks.'}, indent=2) + '\n')
    print(f'Authored spawner audit: {len(files)} templates considered, {scanned} parsed, {total} payloads, {len(failures)} findings.')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())

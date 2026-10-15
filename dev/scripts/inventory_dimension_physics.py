"""Inventory installed dimension-physics resources without inventing bindings."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'dev/docs/boot-dimension-audit/revision-3')
    args = parser.parse_args()
    rows = []
    legacy_blocks = []
    supported_blocks = []
    block_ids = set((ROOT / 'dev/docs/registry-inventory/block-ids.txt').read_text().splitlines())
    for path in sorted((ROOT / 'mods').glob('*.jar')):
        with zipfile.ZipFile(path) as jar:
            for resource in sorted(jar.namelist()):
                if not resource.startswith('data/') or not resource.endswith('.json'):
                    continue
                if '/block_physics/' in resource or '/physics_block_properties/' in resource:
                    value = json.loads(jar.read(resource))
                    entry = {'jar': path.name, 'resource': resource,
                             'sha256': hashlib.sha256(jar.read(resource)).hexdigest(),
                             'fields': sorted(value) if isinstance(value, dict) else [],
                             'selector': value.get('selector') if isinstance(value, dict) else None,
                             'legacy_block': value.get('block') if isinstance(value, dict) else None,
                             'legacy_block_present_in_retained_registry':
                                 value.get('block') in block_ids if isinstance(value, dict) and 'block' in value else None}
                    (legacy_blocks if '/block_physics/' in resource else supported_blocks).append(entry)
                if '/dimension_physics/' not in resource:
                    continue
                raw = jar.read(resource)
                value = json.loads(raw)
                block_resource = resource.replace('/dimension_physics/', '/block_physics/')
                duplicate = block_resource in jar.namelist() and value == json.loads(jar.read(block_resource))
                rows.append({'jar': path.name, 'resource': resource,
                    'sha256': hashlib.sha256(raw).hexdigest(),
                    'dimension': value.get('dimension'), 'block': value.get('block'),
                    'duplicates_block_physics': duplicate,
                    'block_physics_resource': block_resource if duplicate else None})
    findings = [r for r in rows if r['dimension'] is None]
    out = args.out / 'dimension-physics-inventory.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'resources': rows, 'missing_dimension_bindings': findings,
        'legacy_block_physics_resources': legacy_blocks,
        'current_physics_block_properties_resources': supported_blocks,
        'scope': 'Top-level installed mod dimension_physics JSON; no inference of intended dimension and no runtime mutation.'}, indent=2) + '\n')
    print(f'Dimension physics inventory: {len(rows)} resources, {len(findings)} missing dimension bindings, {sum(r["duplicates_block_physics"] for r in rows)} duplicate block-physics payloads.')
    print(f'Block physics layout inventory: {len(legacy_blocks)} legacy resources; {len(supported_blocks)} current-layout resources.')


if __name__ == '__main__':
    main()

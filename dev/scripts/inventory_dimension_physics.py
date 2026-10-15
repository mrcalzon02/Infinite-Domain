"""Inventory installed dimension-physics resources without inventing bindings."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    rows = []
    for path in sorted((ROOT / 'mods').glob('*.jar')):
        with zipfile.ZipFile(path) as jar:
            for resource in sorted(jar.namelist()):
                if not resource.startswith('data/') or '/dimension_physics/' not in resource or not resource.endswith('.json'):
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
    out = ROOT / 'dev/docs/boot-dimension-audit/revision-3/dimension-physics-inventory.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'resources': rows, 'missing_dimension_bindings': findings,
        'scope': 'Top-level installed mod dimension_physics JSON; no inference of intended dimension and no runtime mutation.'}, indent=2) + '\n')
    print(f'Dimension physics inventory: {len(rows)} resources, {len(findings)} missing dimension bindings, {sum(r["duplicates_block_physics"] for r in rows)} duplicate block-physics payloads.')


if __name__ == '__main__':
    main()

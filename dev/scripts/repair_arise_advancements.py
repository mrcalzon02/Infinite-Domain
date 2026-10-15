"""Repair the installed Arise advancement graph and legacy display icons."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    jar_path = next((ROOT / 'mods').glob('DungeonsArise-*.jar'))
    resources = {}
    with zipfile.ZipFile(jar_path) as jar:
        for name in jar.namelist():
            if name.startswith('data/dungeons_arise/advancement/') and name.endswith('.json'):
                resources[name] = json.loads(jar.read(name))
    ids = {f'dungeons_arise:{name.removeprefix("data/dungeons_arise/advancement/").removesuffix(".json")}' for name in resources}
    assert 'dungeons_arise:wda_root' in ids
    items = set((ROOT / 'dev/docs/registry-inventory/item-ids.txt').read_text().splitlines())
    rows = []
    written = 0
    for name, source in sorted(resources.items()):
        value = json.loads(json.dumps(source))
        repairs = []
        parent = value.get('parent')
        if parent and parent not in ids:
            assert parent == 'dungeons_arise:find_small_prairie_house', f'Unexpected missing parent {parent}'
            value['parent'] = 'dungeons_arise:wda_root'
            repairs.append('Reconnect orphan to existing Arise root')
        icon = value.get('display', {}).get('icon', {})
        if 'item' in icon:
            assert 'id' not in icon
            icon['id'] = icon.pop('item')
            repairs.append('Use Minecraft 1.21 item-stack icon field')
        assert not icon or icon.get('id') in items, f'Unregistered icon in {name}'
        destination = ROOT / 'kubejs' / name
        if repairs:
            text = json.dumps(value, indent=2) + '\n'
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists() or destination.read_text() != text:
                destination.write_text(text)
                written += 1
        # Changed overlays must contain exactly these repairs and retain criteria,
        # requirements, rewards and all other upstream fields.
        if repairs:
            assert json.loads(destination.read_text()) == value
        rows.append({'resource': name, 'source_parent': parent,
                     'effective_parent': value.get('parent'), 'icon': icon.get('id'), 'repairs': repairs})
    out = ROOT / 'dev/docs/boot-dimension-audit/revision-3'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'arise-advancement-inventory.json').write_text(json.dumps({
        'source_jar': jar_path.name, 'source_sha256': hashlib.sha256(jar_path.read_bytes()).hexdigest(),
        'advancements': rows, 'orphan_repairs': sum(r['source_parent'] != r['effective_parent'] for r in rows),
        'icon_repairs': sum('Use Minecraft 1.21 item-stack icon field' in r['repairs'] for r in rows),
        'scope': 'Installed Arise jar; generated overlays checked against source-derived expected content.'}, indent=2) + '\n')
    print(f'Arise inventory: {len(rows)} advancements, {sum(r["source_parent"] != r["effective_parent"] for r in rows)} orphan repairs, {sum("Use Minecraft 1.21 item-stack icon field" in r["repairs"] for r in rows)} icon repairs; {written} files written.')


if __name__ == '__main__':
    main()

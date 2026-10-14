"""Retain grouped boot/chunk errors independently of benchmark completion."""
from pathlib import Path
from collections import Counter
import argparse
import csv
import json
import re


def category(message):
    if 'Failed to create block entity' in message:
        return 'chunk_block_entity'
    if 'KubeJS' in message:
        return 'kubejs_runtime'
    if "Couldn't parse element" in message and 'loot_table' in message:
        return 'loot_table_parse'
    if 'tag' in message.lower() and ('load' in message.lower() or 'read' in message.lower()):
        return 'tag_load'
    if 'recipe' in message.lower():
        return 'recipe_load_or_scan'
    if 'dimension data' in message or 'No key dimension' in message:
        return 'sable_dimension_data'
    if 'texture' in message.lower() or 'model' in message.lower() or 'Invalid path in pack' in message:
        return 'client_resource'
    if 'no attributes' in message:
        return 'entity_attributes'
    if 'advancement' in message.lower():
        return 'advancement_load'
    return 'other'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', type=Path, action='append', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    summaries = []
    for log in args.log:
        lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
        current = []
        for i, line in enumerate(lines):
            if not re.search(r'/(?:ERROR|FATAL)\]', line):
                continue
            row = {'log': str(log), 'line': i + 1, 'category': category(line),
                   'message': line.rstrip(),
                   'detail': '\n'.join(part.rstrip() for part in lines[i + 1:i + 4]) if i + 1 < len(lines) and
                   not lines[i + 1].startswith('[') else ''}
            rows.append(row)
            current.append(row)
        summaries.append({'log': str(log), 'error_lines': len(current),
                          'categories': dict(Counter(r['category'] for r in current)),
                          'benchmark_completed': any('"event":"benchmark_completed"' in line.replace(' ', '') for line in lines),
                          'kubejs_load_summaries': [line for line in lines if re.search(r'Loaded \d+/\d+ KubeJS', line)],
                          'generation_markers': [line for line in lines if '"event":"tile_completed"' in line.replace(' ', '')],
                          'limitations': 'Error-line counts include repeated failures; successful generation is not an error-free verdict.'})
    with (args.out / 'errors.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['log', 'line', 'category', 'message', 'detail'])
        writer.writeheader()
        writer.writerows(rows)
    (args.out / 'log-summary.json').write_text(json.dumps(summaries, indent=2) + '\n', encoding='utf-8')
    for summary in summaries:
        print(f"{summary['log']}: {summary['error_lines']} error lines; {summary['categories']}")


if __name__ == '__main__':
    main()

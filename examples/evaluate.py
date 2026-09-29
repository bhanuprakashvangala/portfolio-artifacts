"""Evaluate prediction CSVs, including per-language metrics and split leakage."""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path


def evaluate(rows):
    groups = defaultdict(list)
    seen_ids, split_groups = set(), defaultdict(set)
    for row in rows:
        for field in ('id', 'group', 'split', 'language', 'true', 'predicted'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f'Missing or empty field: {field}')
        if row['id'] in seen_ids:
            raise ValueError(f"Duplicate sample ID: {row['id']}")
        seen_ids.add(row['id'])
        split_groups[row['group']].add(row['split'])
        if row['split'] == 'test':
            groups[row['language']].append(row)
    leaks = sorted(group for group, splits in split_groups.items() if len(splits) > 1)
    if leaks:
        raise ValueError(f'Groups span multiple splits: {leaks}')
    test_rows = [row for group in groups.values() for row in group]
    if not test_rows:
        raise ValueError('No test rows')
    labels = sorted({row[key] for row in test_rows for key in ('true', 'predicted')})

    def metrics(items):
        counts = Counter((r['true'], r['predicted']) for r in items)
        actual, predicted = Counter(r['true'] for r in items), Counter(r['predicted'] for r in items)
        f1 = {label: 2 * counts[label, label] / (actual[label] + predicted[label])
              if actual[label] + predicted[label] else 0.0 for label in labels}
        return {'count': len(items),
                'accuracy': sum(counts[label, label] for label in labels) / len(items),
                'macro_f1': sum(f1.values()) / len(labels), 'f1': f1,
                'confusion': {a: {b: counts[a, b] for b in labels} for a in labels}}
    return {'labels': labels, 'overall': metrics(test_rows),
            'by_language': {language: metrics(items) for language, items in sorted(groups.items())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    args = parser.parse_args()
    try:
        with args.csv.open(encoding='utf-8-sig', newline='') as stream:
            print(json.dumps(evaluate(csv.DictReader(stream)), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')

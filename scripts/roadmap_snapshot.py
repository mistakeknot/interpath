#!/usr/bin/env python3
"""Validate a frozen Beads snapshot and derive deterministic roadmap items."""
import json
import re
import sys
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def items(rows, project, prefix=''):
    if not isinstance(rows, list):
        raise ValueError('Beads snapshot must be an array')
    by_id = {}
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get('id'), str)
                or not row['id'].strip() or row['id'] != row['id'].strip()):
            raise ValueError('invalid Beads record identity')
        key = row['id'].casefold()
        if prefix and not key.startswith(prefix.casefold() + '-'):
            raise ValueError('wrong portfolio in Beads snapshot: ' + row['id'])
        if key in by_id:
            raise ValueError('duplicate issue id: ' + row['id'])
        if (type(row.get('priority')) is not int or not 0 <= row['priority'] <= 4
                or row.get('status') not in {'open', 'closed', 'blocked', 'deferred', 'in_progress'}
                or not isinstance(row.get('title'), str) or not row['title'].strip()):
            raise ValueError('malformed Beads record: ' + row['id'])
        if not isinstance(row.get('dependencies', []), list) or not isinstance(row.get('labels', []), list):
            raise ValueError('malformed Beads relationships: ' + row['id'])
        if row.get('dependency_count', 0) and not row.get('dependencies'):
            raise ValueError('incomplete dependency coverage: ' + row['id'])
        by_id[key] = row
    result = []
    for key, row in sorted(by_id.items()):
        if row['status'] == 'closed':
            continue
        blocked, missing = [], []
        for dep in row.get('dependencies', []):
            if not isinstance(dep, dict) or not isinstance(dep.get('type'), str):
                raise ValueError('malformed dependency: ' + row['id'])
            if dep['type'] != 'blocks':
                continue
            target = dep.get('depends_on_id')
            if not isinstance(target, str) or not target:
                raise ValueError('missing dependency target: ' + row['id'])
            parent = by_id.get(target.casefold())
            if parent is None or parent['status'] != 'closed':
                blocked.append(target)
            if parent is None:
                missing.append(target)
        title = row['title']
        match = re.match(r'^\[([^]]+)\]\s*', title)
        labels = row.get('labels', [])
        if any(not isinstance(label, str) for label in labels):
            raise ValueError('malformed labels: ' + row['id'])
        module = (match.group(1).split('/')[0] if match else
                  next((label[4:] for label in sorted(labels) if label.startswith('mod:')), project))
        title = title[match.end():] if match else title
        status = row['status']
        if blocked and status not in {'deferred', 'in_progress'}:
            status = 'blocked'
        p = row['priority']
        result.append(dict(module=module, id=row['id'], title=title, phase='now' if p <= 1 else 'next' if p == 2 else 'later',
                           priority='P' + str(p), status=status, source='beads', source_file='beads',
                           blocked_by=sorted(set(blocked)), missing_dependencies=sorted(set(missing)), notes=title))
    return result


if __name__ == '__main__':
    try:
        rows = json.loads(Path(sys.argv[1]).read_text(), object_pairs_hook=unique_object)
        for item in items(rows, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ''):
            print(json.dumps(item, sort_keys=True))
    except (OSError, ValueError) as exc:
        print('roadmap-snapshot: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Stage and validate both generated views; retain identical artifact bytes."""
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


def publish(staged_json, output, backlog, renderer):
    if (output.resolve() == backlog.resolve() or output.is_symlink() or backlog.is_symlink()
            or (output.exists() and backlog.exists() and os.path.samefile(output, backlog))):
        raise ValueError('roadmap destinations must be distinct regular paths')
    data = json.loads(staged_json.read_text())
    if output.exists():
        try:
            previous = json.loads(output.read_text())
            semantic = lambda x: {k: v for k, v in x.items() if k != 'generated_at'}
            if isinstance(previous, dict) and semantic(previous) == semantic(data):
                data['generated_at'] = previous['generated_at']
        except (ValueError, KeyError):
            pass
    staged_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    staged_backlog = staged_json.parent / 'backlog.md'
    subprocess.run([sys.executable, str(renderer), str(staged_json), str(staged_backlog)], check=True)
    # No destination changes until both views validate. Individual replacements
    # are atomic; callers publish the pair together in a reviewed Git commit.
    prepared = []
    try:
        for source, target in [(staged_json, output), (staged_backlog, backlog)]:
            content = source.read_bytes()
            if target.exists() and target.read_bytes() == content:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix='.' + target.name + '.', dir=target.parent)
            prepared.append((Path(name), target))
            with os.fdopen(fd, 'wb') as f:
                f.write(content)
                os.fchmod(f.fileno(), stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o644)
                f.flush()
                os.fsync(f.fileno())
        for temp, target in prepared:
            os.replace(temp, target)
    finally:
        for temp, _ in prepared:
            if temp.exists():
                temp.unlink()


if __name__ == '__main__':
    try:
        publish(*(Path(p) for p in sys.argv[1:]))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('publish-roadmap: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)

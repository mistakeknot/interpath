"""Executable generator fixtures: no real tracker, network, or model calls."""
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fixture(tmp_path, rows):
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'docs').mkdir()
    source = tmp_path / 'snapshot.json'
    source.write_text(json.dumps(rows))
    env = dict(os.environ, ROADMAP_PROJECT='sylveste', ROADMAP_BEADS_FILE=str(source),
               ROADMAP_EXPECTED_PREFIX='sylveste', ROADMAP_SCAN_DIRS='empty')
    bin_dir = tmp_path / 'bin'
    bin_dir.mkdir()
    bd = bin_dir / 'bd'
    bd.write_text('#!/bin/sh\necho live-tracker-must-not-be-read >&2\nexit 77\n')
    bd.chmod(0o755)
    env['PATH'] = str(bin_dir) + os.pathsep + env['PATH']
    return project, source, env


def run(project, env, script=None):
    return subprocess.run(['bash', str(script or ROOT / 'scripts/sync-roadmap-json.sh'),
                           str(project / 'docs/roadmap.json'), str(project / 'docs/backlog.md')],
                          cwd=project, env=env, capture_output=True, text=True)


def bead(id='Sylveste-a', **kw):
    return dict(id=id, title='A useful task', priority=2, status='open', **kw)


def test_frozen_snapshot_and_stable_no_change(tmp_path):
    project, source, env = fixture(tmp_path, [bead(), bead('Sylveste-b')])
    first = run(project, env)
    assert first.returncode == 0, first.stderr
    before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in (project / 'docs').iterdir()}
    source.write_text(json.dumps([bead('Sylveste-b'), bead()]))
    second = run(project, env)
    assert second.returncode == 0, second.stderr
    assert before == {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in (project / 'docs').iterdir()}


def test_empty_is_valid(tmp_path):
    project, _, env = fixture(tmp_path, [])
    result = run(project, env)
    assert result.returncode == 0, result.stderr
    assert json.loads((project / 'docs/roadmap.json').read_text())['open_beads'] == 0


def test_wrong_portfolio_preserves_outputs(tmp_path):
    project, _, env = fixture(tmp_path, [bead('shadow-work-a')])
    for name in ['roadmap.json', 'backlog.md']:
        (project / 'docs' / name).write_text('previous')
    result = run(project, env)
    assert result.returncode != 0
    assert 'portfolio' in result.stderr.lower()
    assert all(p.read_text() == 'previous' for p in (project / 'docs').iterdir())


def test_duplicate_or_malformed_snapshot_fails_before_output(tmp_path):
    project, source, env = fixture(tmp_path, [bead(), bead('sylveste-A')])
    assert run(project, env).returncode != 0
    source.write_text('{broken')
    assert run(project, env).returncode != 0
    assert list((project / 'docs').iterdir()) == []


def test_only_unresolved_blocking_edges_block(tmp_path):
    a = bead(dependency_count=3, dependencies=[
        {'type': 'blocks', 'depends_on_id': 'Sylveste-done'},
        {'type': 'parent-child', 'depends_on_id': 'Sylveste-parent'}])
    b = bead('Sylveste-b', dependencies=[{'type': 'blocks', 'depends_on_id': 'Sylveste-missing'}])
    done = bead('Sylveste-done'); done['status'] = 'closed'
    project, _, env = fixture(tmp_path, [a, b, done, bead('Sylveste-parent')])
    result = run(project, env)
    assert result.returncode == 0, result.stderr
    items = {x['id']: x for x in json.loads((project / 'docs/roadmap.json').read_text())['roadmap']['next']}
    assert items['Sylveste-a']['status'] == 'open'
    assert items['Sylveste-a']['blocked_by'] == []
    assert items['Sylveste-b']['status'] == 'blocked'
    assert items['Sylveste-b']['blocked_by'] == ['Sylveste-missing']


def test_renderer_failure_does_not_replace_either_output(tmp_path):
    project, _, env = fixture(tmp_path, [bead()])
    scripts = tmp_path / 'scripts'
    shutil.copytree(ROOT / 'scripts', scripts)
    (scripts / 'render_backlog.py').write_text('raise SystemExit(23)\n')
    for name in ['roadmap.json', 'backlog.md']:
        (project / 'docs' / name).write_text('previous')
    result = run(project, env, scripts / 'sync-roadmap-json.sh')
    assert result.returncode != 0
    assert all(p.read_text() == 'previous' for p in (project / 'docs').iterdir())


def test_incomplete_relationships_fail_closed(tmp_path):
    project, source, env = fixture(tmp_path, [bead(dependency_count=1)])
    for relationships in [{}, {'dependencies': []}]:
        source.write_text(json.dumps([bead(dependency_count=1, **relationships)]))
        result = run(project, env)
        assert result.returncode != 0
        assert 'incomplete dependency coverage' in result.stderr


def test_aliased_outputs_are_rejected(tmp_path):
    project, _, env = fixture(tmp_path, [bead()])
    output = project / 'docs/roadmap.json'
    output.write_text('previous')
    alias = project / 'linked-docs'
    alias.symlink_to(project / 'docs', target_is_directory=True)
    for backlog in [project / 'docs/../docs/roadmap.json', alias / 'roadmap.json']:
        result = subprocess.run(['bash', str(ROOT / 'scripts/sync-roadmap-json.sh'), str(output), str(backlog)],
                                cwd=project, env=env, capture_output=True, text=True)
        assert result.returncode != 0
        assert 'distinct regular paths' in result.stderr
        assert output.read_text() == 'previous'

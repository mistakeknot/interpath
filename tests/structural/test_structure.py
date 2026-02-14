"""Tests for Interpath plugin structure."""

import json
from pathlib import Path


def test_plugin_json_valid(project_root):
    """plugin.json is valid JSON with required fields."""
    path = project_root / ".claude-plugin" / "plugin.json"
    assert path.exists(), "Missing .claude-plugin/plugin.json"
    data = json.loads(path.read_text())
    assert data["name"] == "interpath"
    assert "version" in data
    assert "description" in data


def test_marker_file_exists(project_root):
    """scripts/interpath.sh marker file exists."""
    marker = project_root / "scripts" / "interpath.sh"
    assert marker.exists(), "Missing scripts/interpath.sh marker file"


def test_required_directories_exist(project_root):
    """All expected directories exist."""
    for d in ["skills", "commands", "scripts", "tests"]:
        assert (project_root / d).is_dir(), f"Missing directory: {d}"


def test_claude_md_exists(project_root):
    """CLAUDE.md exists."""
    assert (project_root / "CLAUDE.md").exists()


def test_agents_md_exists(project_root):
    """AGENTS.md exists."""
    assert (project_root / "AGENTS.md").exists()


def test_license_exists(project_root):
    """LICENSE exists."""
    assert (project_root / "LICENSE").exists()

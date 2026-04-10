"""Tests for plugin structure."""

import sys
from pathlib import Path

# Add interverse/ to path so _shared package is importable
_interverse = Path(__file__).resolve().parents[3]
if str(_interverse) not in sys.path:
    sys.path.insert(0, str(_interverse))

from _shared.tests.structural.test_base import StructuralTests


class TestStructure(StructuralTests):
    """Structural tests -- inherits shared base, adds plugin-specific checks."""

    def test_plugin_name(self, plugin_json):
        assert plugin_json["name"] == "interpath"

    def test_marker_file_exists(self, project_root):
        """scripts/interpath.sh marker file exists."""
        marker = project_root / "scripts" / "interpath.sh"
        assert marker.exists(), "Missing scripts/interpath.sh marker file"

    def test_required_directories_exist(self, project_root):
        """All expected directories exist."""
        for d in ["skills", "commands", "scripts", "tests"]:
            assert (project_root / d).is_dir(), f"Missing directory: {d}"

    def test_claude_md_exists(self, project_root):
        """CLAUDE.md exists."""
        assert (project_root / "CLAUDE.md").exists()

    def test_agents_md_exists(self, project_root):
        """AGENTS.md exists."""
        assert (project_root / "AGENTS.md").exists()

    def test_license_exists(self, project_root):
        """LICENSE exists."""
        assert (project_root / "LICENSE").exists()

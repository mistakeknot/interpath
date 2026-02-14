# Interpath

> See `AGENTS.md` for full development guide.

## Overview

Product artifact generator — 1 skill, 5 commands, 0 agents, 0 hooks, 0 MCP servers. Companion plugin for Clavain. Generates roadmaps, PRDs, vision docs, changelogs, and status reports from beads state, brainstorms, and project context.

## Quick Commands

```bash
# Test locally
claude --plugin-dir /root/projects/interpath

# Validate structure
ls skills/*/SKILL.md | wc -l          # Should be 1
ls commands/*.md | wc -l              # Should be 5
bash -n scripts/interpath.sh          # Syntax check
python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"  # Manifest check
```

## Design Decisions (Do Not Re-Ask)

- Namespace: `interpath:` (companion to Clavain)
- All artifact types share a single skill (`artifact-gen`) with phase-based routing
- Discovery phase is shared across all artifact types
- Graceful degradation — missing sources (no beads, no PRD) are silently skipped
- Output goes to `docs/` in the target project
- No hooks — Interpath is invoked on-demand, not event-driven

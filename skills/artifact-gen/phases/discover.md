# Discovery Phase

Gather all available project context. Each source is optional — skip gracefully if unavailable.

## Source 1: Plugin Manifest

```bash
# Read plugin.json for version, name, description, component counts
cat .claude-plugin/plugin.json 2>/dev/null || cat plugin.json 2>/dev/null
```

Also count components:
```bash
echo "skills: $(ls skills/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
echo "commands: $(ls commands/*.md 2>/dev/null | wc -l | tr -d ' ')"
echo "agents: $(ls agents/*/*.md 2>/dev/null | wc -l | tr -d ' ')"
```

## Source 2: Beads State

```bash
# Project health
bd stats 2>/dev/null || echo "beads: not available"

# Open issues with priorities
bd list --status=open 2>/dev/null || echo "open issues: not available"

# Recent closures (last 40)
bd list --status=closed 2>/dev/null | head -40 || echo "closed issues: not available"

# Blocked issues
bd blocked 2>/dev/null || echo "blocked issues: not available"
```

## Source 3: Brainstorms

Use Glob to find brainstorms:
- Pattern: `docs/brainstorms/*.md`
- Read each file's first 20 lines for title and summary

## Source 4: PRDs and Plans

- Pattern: `docs/PRD.md` or `docs/prds/*.md`
- Pattern: `docs/plans/*.md`
- Read first 30 lines of each for context

## Source 5: Vision Doc

- Pattern: `docs/${module}-vision.md` (preferred), fallback to `docs/vision.md`
- Read if it exists (useful for roadmap/PRD cross-referencing)

## Source 6: Existing Artifacts

Read the current version of the artifact being generated (if it exists) to understand what's changing.

## Source 7: Flux-Drive Summaries

- Pattern: `docs/research/flux-drive/*/summary.md`
- Read first 20 lines of each for research findings

## Source 8: Git Activity

```bash
# Recent commits (last 20)
git log --oneline -20 2>/dev/null || echo "git: not available"

# Recent tags
git tag --sort=-version:refname 2>/dev/null | head -5 || echo "tags: none"
```

## Source 9: Companion Plugins

Check which companion plugins are installed:
```bash
for companion in interphase interline interflux interwatch interdoc; do
    if ls ~/.claude/plugins/cache/*/${companion}/*/scripts/*.sh 2>/dev/null | head -1 >/dev/null 2>&1; then
        echo "${companion}: installed"
    else
        echo "${companion}: not installed"
    fi
done
```

## Output

Collect all discovered sources into a mental model. Note which sources were available and which were skipped. Pass this context to the artifact-specific phase.

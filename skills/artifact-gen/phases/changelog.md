# Changelog Synthesis

Using the discovered sources, generate a changelog from closed beads and git history.

## Output Structure

### Header

```markdown
# [Project Name] — Changelog

**Generated:** [today's date]
**Current version:** [from plugin.json]
```

### Body

Group closed beads by version tag (from git tags) or by date range if no tags:

```markdown
## [version] — [date]

### Added
- [bead-id] Description of new feature

### Changed
- [bead-id] Description of modification

### Fixed
- [bead-id] Description of bug fix

### Removed
- [bead-id] Description of removal
```

### Categorization Rules

Derive category from bead type and title:
- `feature` type → **Added**
- `task` type with "refactor", "update", "change" → **Changed**
- `bug` type → **Fixed**
- `task` type with "remove", "delete", "drop" → **Removed**
- Default → **Changed**

### Ungrouped

If beads can't be mapped to a version, group them under "Unreleased".

## Writing Guidelines

- Use imperative mood: "Add X" not "Added X"
- One line per bead, include bead ID for traceability
- Most recent version first
- Keep under 200 lines (truncate older versions if needed)

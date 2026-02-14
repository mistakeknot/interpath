# PRD Synthesis

Using the discovered sources, generate or refresh a Product Requirements Document.

## Output Structure

### Header

```markdown
# [Project Name] — Product Requirements Document

**Version:** [from plugin.json]
**Last updated:** [today's date]
**Status:** Living document — regenerate with `/interpath:prd`
```

### Section 1: Problem Statement

Synthesize from vision doc and brainstorms:
- What problem does this project solve?
- Who experiences this problem?
- What's the current alternative?

### Section 2: Product Overview

From plugin manifest and component counts:
- One-paragraph description
- Component summary (skills, agents, commands, hooks, MCP servers)
- Target user profile

### Section 3: Core Capabilities

Enumerate from skills and commands, grouped by workflow stage:
- Planning & Strategy
- Execution & Building
- Review & Quality
- Learning & Improvement

For each capability: name, one-line description, key commands.

### Section 4: Architecture

#### 4.1 Plugin Structure
Component breakdown with counts.

#### 4.2 Routing
How users discover and invoke capabilities.

#### 4.3 Hook System
What hooks exist and what they do.

#### 4.4 Companion Ecosystem
Table of companion plugins:
- Name | Status | What It Adds | Install Command

### Section 5: Non-Goals

What this project explicitly does NOT do. Derive from design decisions and domain boundaries.

### Section 6: Success Metrics

From beads stats and project state:
- Quantitative: component counts, test counts, beads velocity
- Qualitative: workflow coverage, user friction points

### Section 7: Open Questions

From open beads and brainstorms — unresolved design decisions.

## Writing Guidelines

- Be specific — include actual component names, counts, versions
- Link to files: `skills/foo/SKILL.md`, `commands/bar.md`
- Distinguish shipped vs. planned capabilities
- Keep under 250 lines

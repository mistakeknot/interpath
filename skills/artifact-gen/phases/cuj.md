# CUJ Synthesis

Using the discovered sources, generate or refresh a Critical User Journey document.

## Output Structure

### Header

The CUJ frontmatter uses additional fields beyond the standard artifact header:

```yaml
---
artifact_type: cuj
journey: <journey-slug>
actor: <who>
criticality: <p0-p4>
bead: <bead-id or none>
---
```

Followed by the markdown header:

```markdown
# [Journey Name]

**Last updated:** [today's date]
**Status:** Living document — regenerate with `/interpath:cuj`
```

### Section 1: Why This Journey Matters

Synthesize from PRD, brainstorms, and vision doc:
- Why is this journey critical to the product?
- What breaks or degrades if this journey is poor?
- Who is the actor and what's their context?

Keep to 1-2 paragraphs.

### Section 2: The Journey

Prose narrative describing the expected end-to-end experience. This is freeform — it should read naturally for both linear flows (CLI tools) and exploratory flows (games, complex UIs).

For linear flows, describe the step-by-step sequence.
For exploratory flows, describe the intended discovery path, emotional beats, and key moments.

Authors may optionally embed step tables, mermaid diagrams, or other structured elements inline. The format does not prescribe a specific structure.

Synthesize from:
- PRD core capabilities (what the user does)
- Brainstorms (what the experience should feel like)
- Existing docs and README (current documented flows)
- Beads (what's shipped vs. planned)

### Section 3: Success Signals

A table of typed assertions that agents and tests can validate:

| Signal | Type | Assertion |
|--------|------|-----------|
| [name] | measurable/observable/qualitative | [what success looks like] |

**Signal types:**
- **measurable** — quantitative, automatable (HTTP 200, < 5min, no errors)
- **observable** — detectable with instrumentation (state change, event fired)
- **qualitative** — requires human judgment (feels intuitive, low friction)

Derive from:
- PRD success metrics
- Brainstorm acceptance criteria
- Beads with test/acceptance tags

### Section 4: Known Friction Points

Current pain points, gaps, or risks in this journey. Derive from:
- Open beads related to this flow
- Brainstorm friction discussions
- Known bugs or UX issues

## Writing Guidelines

- Be specific — reference actual commands, files, UI elements
- Describe the CURRENT journey, not the aspirational one
- Keep under 150 lines
- Link to sub-journey CUJ files where a step is complex enough to warrant its own document
- Prefer concrete success signals over vague ones ("HTTP 200 at /health" not "app works")

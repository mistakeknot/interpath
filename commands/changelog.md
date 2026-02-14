---
name: changelog
description: Generate a changelog from closed beads grouped by version and type
---

# Generate Changelog

Invoke the `artifact-gen` skill with artifact type **changelog**.

The changelog synthesizes:
- Closed beads grouped by git tag / version
- Categorized as Added/Changed/Fixed/Removed based on bead type
- Most recent version first
- Bead IDs included for traceability

Output: `docs/CHANGELOG.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a changelog artifact."

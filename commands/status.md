---
name: status
description: Generate a point-in-time status report with health metrics, shipped work, blockers, and risks
---

# Generate Status Report

Invoke the `artifact-gen` skill with artifact type **status**.

The status report provides:
- Health metrics table (open/closed/blocked counts, version)
- What shipped in the period
- What's in progress with owners
- What's blocked and why
- Risks (stale beads, long dependency chains)
- Next actions from available work

Output: `docs/status-report.md` (or print to conversation)

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a status report artifact."
